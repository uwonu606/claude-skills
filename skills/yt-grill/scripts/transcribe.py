# /// script
# requires-python = ">=3.10,<3.13"
# dependencies = ["yt-dlp", "faster-whisper"]
# ///
"""자막이 없는 영상을 로컬 whisper 로 전사한다. 과금 없음, CPU 만 쓴다.

    uv run transcribe.py <url> [--model small]

stdout: 첫 줄 "# lang <code>", 이후 "<시작초>\\t<텍스트>" 한 줄씩. 진행 상황은 stderr.
실측(2026-09-06, Core Ultra 9 185H): small 은 실시간의 0.11~0.13 배, 1시간 영상 7~8분.
한국어는 base 로는 단어가 날아가서 small 이 하한. 언어는 강제하지 않는다 —
제목만 한국어고 음성이 영어인 영상에서 강제가 한영 뒤섞인 결과를 냈다.
"""
import sys
import tempfile
from pathlib import Path


def download_audio(url: str, tmp: Path) -> Path:
    import yt_dlp
    opts = {
        "quiet": True, "no_warnings": True,
        "noprogress": True,  # quiet 만으로는 진행 표시가 stdout 에 섞여 "# lang" 줄을 깨뜨린다 (실측)
        "format": "bestaudio[ext=m4a]/bestaudio",
        "outtmpl": str(tmp / "audio.%(ext)s"),
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.extract_info(url, download=True)
    files = list(tmp.glob("audio.*"))
    if not files:
        sys.exit("오디오 다운로드 실패")
    return files[0]


def transcribe(audio: Path, model_name: str):
    from faster_whisper import WhisperModel
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    for vad in (True, False):  # 음악·무음 위주 영상은 VAD 가 전부 걸러 0 줄이 된다 (실측)
        segments, info = model.transcribe(str(audio), vad_filter=vad)
        segs = [(s.start, s.text.strip()) for s in segments]
        segs = [s for s in segs if s[1]]
        if segs:
            return info.language, segs
        sys.stderr.write("VAD 가 전부 걸러냈다. VAD 없이 다시 돈다.\n")
    return None, []


def main(argv):
    if not argv:
        print(__doc__)
        sys.exit(64)
    url = argv[0]
    model_name = argv[argv.index("--model") + 1] if "--model" in argv else "small"
    with tempfile.TemporaryDirectory(prefix="yt-grill-") as d:
        tmp = Path(d)
        sys.stderr.write("오디오 내려받는 중\n")
        audio = download_audio(url, tmp)
        sys.stderr.write(f"whisper {model_name} 전사 중 ({audio.stat().st_size // 1024} KiB)\n")
        lang, segs = transcribe(audio, model_name)
    print(f"# lang {lang}")
    for start, text in segs:
        print(f"{start:.1f}\t{text}")


if __name__ == "__main__":
    main(sys.argv[1:])
