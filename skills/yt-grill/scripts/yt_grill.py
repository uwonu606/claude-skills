# /// script
# requires-python = ">=3.10"
# dependencies = ["yt-dlp", "youtube-transcript-api>=1.0"]
# ///
"""yt-grill 원문 저장 도구.

    uv run yt_grill.py info <url>                 메타데이터·자막 유무·이미 저장됐는지·원문 계획 (JSON)
    uv run yt_grill.py save <url> <slug> [플래그]  transcript.md + notes.md 생성 (JSON)
    uv run yt_grill.py list                       저장된 영상 목록 (markdown 표)

원문 계획(plan): GPU(nvidia-smi)가 있으면 whisper large-v3-turbo 로 전사(1시간에 1~2분),
없으면 유튜브 자막(원어 수동 > 자동), 자막도 없으면 CPU whisper small(1시간에 7~12분).
  --whisper   자막을 무시하고 전사. 이미 저장된 영상이면 transcript.md 만 갈아 끼우고 notes.md 는 둔다
  --captions  GPU 가 있어도 자막을 먼저 쓴다
  YT_GRILL_GPU=0  GPU 를 없는 것으로 친다

저장 위치는 $YT_GRILL_HOME, 없으면 ~/video-notes.
"""
import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
USER_LANGS = ["ko", "en"]  # 원어를 못 알아냈을 때의 우선순위


def home() -> Path:
    return Path(os.environ.get("YT_GRILL_HOME") or "~/video-notes").expanduser()


def die(msg: str, code: int = 1):
    print(json.dumps({"error": msg}, ensure_ascii=False))
    sys.exit(code)


# ---------- 유튜브 ----------

def video_id(url: str) -> str:
    m = re.search(r"(?:v=|youtu\.be/|shorts/|live/|embed/)([A-Za-z0-9_-]{11})", url)
    if m:
        return m.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url):
        return url
    die(f"유튜브 URL 이 아니다: {url}")


def metadata(url: str) -> dict:
    import yt_dlp
    opts = {"quiet": True, "no_warnings": True, "skip_download": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
    up = info.get("upload_date") or ""
    return {
        "id": info["id"],
        "url": f"https://www.youtube.com/watch?v={info['id']}",
        "title": info.get("title") or "",
        "channel": info.get("channel") or info.get("uploader") or "",
        "duration": int(info.get("duration") or 0),
        "upload_date": f"{up[:4]}-{up[4:6]}-{up[6:8]}" if len(up) == 8 else None,
        "language": info.get("language"),
        "chapters": [(int(c.get("start_time") or 0), c.get("title") or "") for c in (info.get("chapters") or [])],
    }


def transcript_list(vid: str):
    from youtube_transcript_api import YouTubeTranscriptApi
    try:
        return list(YouTubeTranscriptApi().list(vid))
    except Exception as e:  # 자막 기능 자체가 꺼진 영상 등
        sys.stderr.write(f"transcript list 실패: {type(e).__name__}: {e}\n")
        return []


def base_lang(code: str) -> str:
    return code.split("-")[0].lower()


def pick_transcript(transcripts, language):
    """원어 수동 > 원어 자동 > 사용자 언어 수동 > 사용자 언어 자동. 번역본은 안 쓴다."""
    def find(lang, generated):
        for t in transcripts:
            if base_lang(t.language_code) == lang and t.is_generated == generated:
                return t
        return None
    langs = ([base_lang(language)] if language else []) + USER_LANGS
    for lang in langs:
        for generated in (False, True):
            t = find(lang, generated)
            if t:
                return t
    return None


def hms(sec: float) -> str:
    s = int(sec)
    h, m, s = s // 3600, (s % 3600) // 60, s % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def fetch_lines(t) -> list:
    out = []
    for snip in t.fetch():
        text = " ".join(snip.text.split())
        if text:
            out.append(f"[{hms(snip.start)}] {text}")
    return out


CUDA_WITH = ["--with", "nvidia-cublas-cu12", "--with", "nvidia-cudnn-cu12"]


def gpu_available() -> bool:
    if os.environ.get("YT_GRILL_GPU") == "0":
        return False
    try:
        r = subprocess.run(["nvidia-smi", "-L"], capture_output=True, text=True, timeout=10)
        return r.returncode == 0 and "GPU" in r.stdout
    except (OSError, subprocess.TimeoutExpired):
        return False


def whisper_lines(url: str, device: str):
    """scripts/transcribe.py 를 uv 로 돌린다. 성공하면 (줄 목록, 언어, 모델), 실패하면 None."""
    cmd = ["uv", "run", "-q"] + (CUDA_WITH if device == "cuda" else []) + [str(HERE / "transcribe.py"), url, "--device", device]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)  # stderr 는 진행 상황이라 그대로 흘린다
    if proc.returncode != 0:
        sys.stderr.write(f"whisper({device}) 실패, exit {proc.returncode}\n")
        return None
    lang, model, lines = None, None, []
    for line in proc.stdout.splitlines():
        if line.startswith("# lang "):
            lang = line.split()[2]
        elif line.startswith("# model "):
            model = line.split()[2]
        elif "\t" in line:
            start, text = line.split("\t", 1)
            text = " ".join(text.split())
            if text:
                lines.append(f"[{hms(float(start))}] {text}")
    return (lines, lang, model) if lines else None


def plan_for(gpu: bool, has_captions: bool, force_whisper: bool, prefer_captions: bool) -> str:
    """save 가 무엇을 할지. whisper-turbo(GPU) | captions | whisper-small(CPU)."""
    if force_whisper:
        return "whisper-turbo" if gpu else "whisper-small"
    if gpu and not prefer_captions:
        return "whisper-turbo"
    if has_captions:
        return "captions"
    return "whisper-turbo" if gpu else "whisper-small"


def estimate_seconds(plan: str, duration: int) -> int:
    # 실측 rtf: turbo GPU 0.016~0.022(+로드·다운로드), small CPU 0.11~0.20
    return {"captions": 2, "whisper-turbo": int(duration * 0.02) + 20, "whisper-small": int(duration * 0.2) + 10}[plan]


# ---------- 저장소 ----------

def read_frontmatter(path: Path) -> dict:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        k, v = line.split(":", 1)
        v = v.strip()
        if v.startswith('"'):
            try:
                v = json.loads(v)
            except Exception:
                pass
        fm[k.strip()] = v
    return fm


def yaml_str(s) -> str:
    if s is None:
        return "~"
    return json.dumps(s, ensure_ascii=False)


def saved_videos() -> list:
    root = home()
    if not root.exists():
        return []
    out = []
    for d in sorted(root.iterdir()):
        if not d.is_dir() or d.name.startswith("."):
            continue
        t = read_frontmatter(d / "transcript.md")
        if not t.get("id"):
            continue
        n = read_frontmatter(d / "notes.md")
        out.append({"slug": d.name, **t, "status": n.get("status", "transcribed"),
                    "discussed": n.get("discussed", "[]")})
    return out


def find_saved(vid: str):
    for v in saved_videos():
        if v["id"] == vid:
            return v
    return None


# ---------- 명령 ----------

def cmd_info(url: str):
    vid = video_id(url)
    meta = metadata(url)
    meta.pop("chapters")  # 챕터는 transcript.md frontmatter 가 갖는다
    ts = transcript_list(vid)
    pick = pick_transcript(ts, meta["language"])
    existing = find_saved(vid)
    gpu = gpu_available()
    plan = plan_for(gpu, pick is not None, False, False)
    print(json.dumps({
        **meta,
        "duration_hms": hms(meta["duration"]),
        "transcripts": {
            "manual": [t.language_code for t in ts if not t.is_generated],
            "generated": [t.language_code for t in ts if t.is_generated],
        },
        "pick": {"language": pick.language_code, "source": "auto" if pick.is_generated else "manual"} if pick else None,
        "gpu": gpu,
        "plan": plan,
        "estimate_seconds": estimate_seconds(plan, meta["duration"]),
        "existing": {"slug": existing["slug"], "status": existing["status"]} if existing else None,
        "home": str(home()),
    }, ensure_ascii=False, indent=2))


def cmd_save(url: str, slug: str, force_whisper: bool, prefer_captions: bool):
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
        die(f"slug 는 소문자·숫자·하이픈만: {slug}")
    vid = video_id(url)
    existing = find_saved(vid)
    if existing and not force_whisper:
        die(f"이미 저장됨: {existing['slug']} (status={existing['status']})", 2)
    meta = metadata(url)

    root = home()
    created_home = not root.exists()
    root.mkdir(parents=True, exist_ok=True)
    if created_home:
        (root / ".gitignore").write_text(
            "# 자막·전사 원문은 남의 저작물이라 올리지 않는다. URL 이 살아 있으면 다시 받는다.\n"
            "*/transcript.md\n", encoding="utf-8")

    if existing:  # --whisper 로 원문만 갈아 끼운다. notes.md 는 건드리지 않는다
        slug = existing["slug"]
        target = root / slug
    else:
        target = root / slug
        if target.exists():
            slug = f"{slug}-{re.sub(r'[^a-z0-9]', '', vid.lower())[:4]}"
            target = root / slug
            if target.exists():
                die(f"디렉토리 충돌: {target}")

    pick = None if force_whisper else pick_transcript(transcript_list(vid), meta["language"])
    gpu = gpu_available()
    plan = plan_for(gpu, pick is not None, force_whisper, prefer_captions)
    source, lang, model, lines = None, None, None, []

    def use_captions():
        nonlocal source, lang, lines
        lines = fetch_lines(pick)
        source = "auto" if pick.is_generated else "manual"
        lang = base_lang(pick.language_code)

    def use_whisper(device):
        nonlocal source, lang, model, lines
        sys.stderr.write(f"whisper({device}) 전사, 예상 {estimate_seconds('whisper-turbo' if device == 'cuda' else 'whisper-small', meta['duration'])}초\n")
        got = whisper_lines(url, device)
        if got:
            lines, lang, model = got
            source = "whisper"

    if plan == "captions":
        use_captions()
    elif plan == "whisper-turbo":
        use_whisper("cuda")
        if not lines and pick:  # GPU 가 죽으면 자막으로. 자막도 없으면 CPU 로
            sys.stderr.write("GPU 전사 실패, 자막을 쓴다.\n")
            use_captions()
        elif not lines:
            sys.stderr.write("GPU 전사 실패, CPU 로 다시 돈다.\n")
            use_whisper("cpu")
    else:
        use_whisper("cpu")
    if not lines:
        die("원문을 한 줄도 얻지 못했다")

    target.mkdir(exist_ok=True)
    fm = [
        "---",
        f"id: {meta['id']}",
        f"url: {meta['url']}",
        f"title: {yaml_str(meta['title'])}",
        f"channel: {yaml_str(meta['channel'])}",
        f"duration: {meta['duration']}",
        f"upload_date: {meta['upload_date'] or '~'}",
        f"language: {lang or meta['language'] or '~'}",
        f"source: {source}",
        f"model: {model or '~'}",
        f"saved: {date.today().isoformat()}",
    ]
    if meta["chapters"]:
        fm.append("chapters:")
        fm += ["  - " + yaml_str(f"[{hms(t)}] {title}") for t, title in meta["chapters"]]
    else:
        fm.append("chapters: []")
    fm += ["---", ""]
    (target / "transcript.md").write_text("\n".join(fm) + "\n".join(lines) + "\n", encoding="utf-8")
    if existing:
        print(json.dumps({"slug": slug, "dir": str(target), "replaced": "transcript.md", "source": source,
                          "model": model, "language": lang, "lines": len(lines), "chars": sum(len(l) for l in lines)},
                         ensure_ascii=False, indent=2))
        return
    notes = [
        "---",
        f"id: {meta['id']}",
        f"url: {meta['url']}",
        f"title: {yaml_str(meta['title'])}",
        "status: transcribed",
        "discussed: []",
        "---",
        "",
        "## open_questions",
        "",
    ]
    (target / "notes.md").write_text("\n".join(notes), encoding="utf-8")
    print(json.dumps({
        "slug": slug, "dir": str(target), "title": meta["title"], "channel": meta["channel"],
        "duration_hms": hms(meta["duration"]), "language": lang or meta["language"],
        "source": source, "model": model, "lines": len(lines), "chars": sum(len(l) for l in lines),
        "created_home": created_home,
    }, ensure_ascii=False, indent=2))


def cmd_list():
    vids = saved_videos()
    if not vids:
        print(f"저장된 영상이 없다. ({home()})")
        return
    vids.sort(key=lambda v: (v.get("saved", ""), v["slug"]), reverse=True)
    print("| slug | 제목 | 길이 | status | 저장일 | 자막 |")
    print("|---|---|---|---|---|---|")
    for v in vids:
        d = str(v.get("duration", ""))
        length = hms(int(d)) if d.isdigit() else "?"
        title = str(v.get("title", "")).replace("|", "\\|")
        src = v.get("source", "?")
        if src == "whisper" and v.get("model") not in (None, "~"):
            src = f"whisper:{v['model']}"
        print(f"| {v['slug']} | {title} | {length} | {v['status']} | {v.get('saved', '?')} | {src} |")


def main(argv):
    if len(argv) >= 2 and argv[0] == "info":
        cmd_info(argv[1])
    elif len(argv) >= 3 and argv[0] == "save":
        cmd_save(argv[1], argv[2], "--whisper" in argv[3:], "--captions" in argv[3:])
    elif argv[:1] == ["list"]:
        cmd_list()
    else:
        print(__doc__)
        sys.exit(64)


if __name__ == "__main__":
    main(sys.argv[1:])
