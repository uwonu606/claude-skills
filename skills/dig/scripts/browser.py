#!/usr/bin/env -S uv run --quiet
# /// script
# requires-python = ">=3.10"
# dependencies = ["playwright==1.58.0"]
# ///
"""로그인 상태를 만들고, 그 상태로 페이지 하나를 읽는다.

  browser.py login <url>               창을 연다. 로그인하고 창을 닫으면 auth/<host>.json 이 남는다.
                                       창은 Playwright 가 조종하지 않는 보통 크로미움이라 Google 로그인이 막히지 않는다.
                                       프로필은 auth/profiles/<host>/ 에 남아 다음 login 이 물려받는다
  browser.py list                      auth/ 의 호스트·쿠키 수·가장 이른 만료
  browser.py open <url> [--html] [--out FILE] [--no-auth] [--net DIR]
                                       URL 의 호스트에 맞는 auth 가 있으면 그 상태로, 헤드리스로 페이지 하나를 읽는다.
                                       stdout(또는 --out) 에 제목·최종 URL·본문 텍스트(--html 이면 HTML). 어느 auth 를 썼는지는 stderr.
                                       --net 은 같은 호스트에서 온 JSON 응답을 DIR 에 NNN.json 과 index.tsv 로 남긴다.

auth/ 는 현재 디렉토리(데이터 디렉토리) 바로 아래다. 상태 파일의 내용은 이 스크립트만 읽는다.
종료 0 정상 / 2 페이지를 못 열음 / 3 크로미움 없음 / 5 인자 오류
"""
import argparse
import datetime as dt
import glob
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

AUTH_DIR = Path("auth")
NAV_TIMEOUT_MS = 30_000
SETTLE_MS = 1_500
LOGIN_FLAGS = ["--no-first-run", "--no-default-browser-check"]
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{} Safari/537.36"


def chromium_path() -> Path:
    env = os.environ.get("CHROMIUM_PATH")
    if env and Path(env).exists():
        return Path(env)
    hits = sorted(glob.glob(str(Path.home() / ".cache/ms-playwright/chromium-*/chrome-linux64/chrome")))
    if hits:
        return Path(hits[-1])
    sys.stderr.write(
        "크로미움이 없습니다. `uv run --with playwright playwright install chromium` 으로 받거나 "
        "CHROMIUM_PATH 에 실행 파일 경로를 넣으세요.\n"
    )
    sys.exit(3)


def host_of(url: str) -> str:
    h = (urlparse(url).hostname or "").lower()
    if not h:
        sys.stderr.write(f"URL 에 호스트가 없습니다: {url}\n")
        sys.exit(5)
    return h[4:] if h.startswith("www.") else h


def auth_file_for(host: str) -> Path | None:
    """host 와 같거나 host 의 상위 도메인인 파일 중 가장 긴 것. 없으면 None."""
    best = None
    for f in AUTH_DIR.glob("*.json"):
        name = f.stem
        if host == name or host.endswith("." + name):
            if best is None or len(name) > len(best.stem):
                best = f
    return best


def summarize(state: dict) -> tuple[int, str]:
    cookies = state.get("cookies", [])
    exp = [c["expires"] for c in cookies if c.get("expires", -1) > 0]
    earliest = dt.datetime.fromtimestamp(min(exp)).strftime("%Y-%m-%d") if exp else "세션"
    return len(cookies), earliest


def pw_cookie(c: dict) -> dict:
    out = {k: c[k] for k in ("name", "value", "domain", "path", "expires", "httpOnly", "secure")}
    if c.get("sameSite") in ("Strict", "Lax", "None"):
        out["sameSite"] = c["sameSite"]
    return out


def cmd_login(url: str) -> int:
    from playwright.sync_api import Error as PwError, sync_playwright

    exe = chromium_path()
    host = host_of(url)
    AUTH_DIR.mkdir(exist_ok=True)
    target = AUTH_DIR / f"{host}.json"
    profile = (AUTH_DIR / "profiles" / host).resolve()
    if not profile.exists() and target.exists():
        # 프로필 없이 남은 상태 파일은 쿠키를 프로필에 옮겨 물려받는다
        with sync_playwright() as p:
            ctx = p.chromium.launch_persistent_context(str(profile), executable_path=str(exe), headless=True)
            ctx.add_cookies([pw_cookie(c) for c in json.loads(target.read_text())["cookies"]])
            ctx.close()
    profile.mkdir(parents=True, exist_ok=True)

    # Playwright 가 조종하는 창은 navigator.webdriver 가 켜져 Google 이 로그인을 막는다.
    # 로그인하는 동안에는 아무것도 붙이지 않은 보통 프로세스로 띄우고, 닫힌 뒤 프로필에서 상태를 꺼낸다.
    # 브라우저를 닫으면 지워지는 세션 쿠키는 남지 않는다
    proc = subprocess.Popen(
        [str(exe), f"--user-data-dir={profile}", *LOGIN_FLAGS, url],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    sys.stderr.write(f"창에서 로그인한 뒤 창을 닫으세요. 닫히면 {target} 이 남습니다.\n")
    proc.wait()

    # localStorage 는 그 오리진을 한 번 열어야 담긴다. UA 의 "HeadlessChrome" 은 세션을 끊을 수 있어 보통 UA 로 연다
    version = subprocess.run([str(exe), "--version"], capture_output=True, text=True).stdout.split()[-1]
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(profile), executable_path=str(exe), headless=True, user_agent=UA.format(version)
        )
        page = ctx.new_page()
        try:
            page.goto(url, timeout=NAV_TIMEOUT_MS, wait_until="load")
        except PwError:
            pass
        state = ctx.storage_state()
        ctx.close()
    target.write_text(json.dumps(state))
    n, earliest = summarize(state)
    print(f"{target} 저장 — 쿠키 {n}개, 가장 이른 만료 {earliest}")
    return 0


def cmd_list() -> int:
    chromium_path()
    files = sorted(AUTH_DIR.glob("*.json"))
    if not files:
        print("auth/ 비어 있음")
        return 0
    for f in files:
        n, earliest = summarize(json.loads(f.read_text()))
        print(f"{f.stem}\t쿠키 {n}개\t가장 이른 만료 {earliest}")
    return 0


def cmd_open(url: str, html: bool, out: str | None, no_auth: bool, net: str | None) -> int:
    from playwright.sync_api import Error as PwError, sync_playwright

    exe = chromium_path()
    host = host_of(url)
    auth = None if no_auth else auth_file_for(host)
    sys.stderr.write(f"auth: {auth}\n" if auth else "auth: 없음\n")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=str(exe), headless=True)
        # 기본 UA 의 "HeadlessChrome" 은 CloudFront 같은 봇 차단에 403 을 받는다
        ctx = browser.new_context(
            storage_state=str(auth) if auth else None,
            user_agent=UA.format(browser.version),
            locale="ko-KR",
        )
        page = ctx.new_page()
        rows = []
        if net:
            Path(net).mkdir(parents=True, exist_ok=True)

            def keep(r):
                if "json" not in r.headers.get("content-type", "") or not r.url.startswith("http"):
                    return
                h = host_of(r.url)
                if h != host and not h.endswith("." + host):
                    return
                try:
                    data = r.body()
                except PwError:
                    return
                n = f"{len(rows) + 1:03d}"
                (Path(net) / f"{n}.json").write_bytes(data)
                rows.append(f"{n}\t{r.status}\t{r.request.method}\t{len(data)}\t{r.url}\n")

            page.on("response", keep)
        try:
            resp = page.goto(url, timeout=NAV_TIMEOUT_MS, wait_until="load")
        except PwError as e:
            sys.stderr.write(f"못 열음: {e.message.splitlines()[0]}\n")
            browser.close()
            return 2
        try:
            page.wait_for_load_state("networkidle", timeout=10_000)
        except PwError:
            pass
        page.wait_for_timeout(SETTLE_MS)
        status = resp.status if resp else "~"
        body = page.content() if html else page.inner_text("body")
        head = f"# {page.title()}\nURL: {page.url}\nHTTP: {status}\n\n"
        browser.close()
    if net:
        (Path(net) / "index.tsv").write_text("".join(rows))
        sys.stderr.write(f"net: {net} 에 {len(rows)}개\n")
    text = head + body
    if out:
        Path(out).write_text(text)
        sys.stderr.write(f"{out} 에 {len(text)}자\n")
    else:
        sys.stdout.write(text)
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="browser.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("login"); s.add_argument("url")
    sub.add_parser("list")
    s = sub.add_parser("open"); s.add_argument("url")
    s.add_argument("--html", action="store_true"); s.add_argument("--out"); s.add_argument("--no-auth", action="store_true")
    s.add_argument("--net", metavar="DIR", help="같은 호스트에서 온 JSON 응답을 DIR 에 NNN.json 과 index.tsv 로 남긴다")
    a = ap.parse_args(argv)
    if a.cmd == "login":
        return cmd_login(a.url)
    if a.cmd == "list":
        return cmd_list()
    return cmd_open(a.url, a.html, a.out, a.no_auth, a.net)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
