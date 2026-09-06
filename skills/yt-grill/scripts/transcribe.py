# /// script
# requires-python = ">=3.10,<3.13"
# dependencies = ["yt-dlp", "faster-whisper"]
# ///
"""유튜브 영상을 로컬 whisper 로 전사한다. 과금 없음.

    uv run transcribe.py <url> --device cpu                       small int8, CPU
    uv run --with nvidia-cublas-cu12 --with nvidia-cudnn-cu12 \\
           transcribe.py <url> --device cuda                      large-v3-turbo fp16 배치, GPU

stdout: "# lang <code>", "# model <name>", "# device <cpu|cuda>", 이후 "<시작초>\\t<텍스트>" 한 줄씩.
진행 상황은 stderr.

실측(2026-09-06, RTX 4070 Laptop / Core Ultra 9 185H):
- GPU large-v3-turbo fp16 + BatchedInferencePipeline: 28분 영상 26~30초(rtf 0.016~0.018), VRAM 3.3GB(batch 8).
  비배치 fp16 은 turbo·large-v3 모두 "CUDA illegal memory access" 로 결정적으로 죽는다 — 배치만 쓴다.
  배치 출력은 세그먼트가 약 30초 단위다.
- CPU small int8: 실시간의 0.11~0.20 배, 1시간 영상 7~12분. base 는 한국어 단어가 날아가 small 이 하한.
- 언어는 강제하지 않는다 — 제목만 한국어인 영어 영상에서 강제가 한영 뒤섞인 결과를 냈다.
- 사람 자막 대비 글자 오류율: 자동자막 0.31, small 0.22, turbo 0.15~0.20 (한국어 기술 강연 3개).
"""
import sys
import tempfile
from pathlib import Path

CUDA_MODEL, CUDA_COMPUTE, CUDA_BATCH = "large-v3-turbo", "float16", 8
CPU_MODEL, CPU_COMPUTE = "small", "int8"


def preload_cuda_libs() -> int:
    """pip 휠로 받은 CUDA 라이브러리는 로더 경로에 없다. RTLD_GLOBAL 로 미리 올리면 LD_LIBRARY_PATH 없이 된다 (실측)."""
    import ctypes
    import glob
    import importlib.util
    import os
    n = 0
    for pkg in ("nvidia.cublas.lib", "nvidia.cuda_nvrtc.lib", "nvidia.cudnn.lib"):
        spec = importlib.util.find_spec(pkg)
        if not spec:
            continue
        for d in spec.submodule_search_locations or []:
            for so in sorted(glob.glob(os.path.join(d, "*.so*"))):
                try:
                    ctypes.CDLL(so, mode=ctypes.RTLD_GLOBAL)
                    n += 1
                except OSError:
                    pass
    return n


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


SENTENCE_END = (".", "?", "!", "。", "？", "！")
MAX_SPAN = 15.0  # 구두점이 한참 없으면 이 길이에서 끊는다


def split_sentences(segments):
    """배치 파이프라인은 세그먼트가 30초 단위라 인용 위치가 굵다. 단어 타임스탬프로 문장마다 끊는다."""
    for s in segments:
        words = getattr(s, "words", None)
        if not words:
            if s.text.strip():
                yield s.start, s.text.strip()
            continue
        buf, start = [], None
        for w in words:
            if start is None:
                start = w.start
            buf.append(w.word)
            if w.word.rstrip().endswith(SENTENCE_END) or (w.end - start) >= MAX_SPAN:
                text = "".join(buf).strip()
                if text:
                    yield start, text
                buf, start = [], None
        if buf:
            text = "".join(buf).strip()
            if text:
                yield start, text


def run(audio: Path, device: str):
    import time
    from faster_whisper import WhisperModel
    t0 = time.time()
    if device == "cuda":
        model = WhisperModel(CUDA_MODEL, device="cuda", compute_type=CUDA_COMPUTE)
        from faster_whisper import BatchedInferencePipeline
        pipe = BatchedInferencePipeline(model=model)

        def transcribe(vad):
            segs, info = pipe.transcribe(str(audio), vad_filter=vad, batch_size=CUDA_BATCH, word_timestamps=True)
            return split_sentences(segs), info
        name = CUDA_MODEL
    else:
        model = WhisperModel(CPU_MODEL, device="cpu", compute_type=CPU_COMPUTE)

        def transcribe(vad):
            segs, info = model.transcribe(str(audio), vad_filter=vad)
            return ((s.start, s.text.strip()) for s in segs), info
        name = CPU_MODEL
    sys.stderr.write(f"모델 로드 {time.time() - t0:.1f}초\n")

    for vad in (True, False):  # 음악·무음 위주 영상은 VAD 가 전부 걸러 0 줄이 된다 (실측)
        t1 = time.time()
        segments, info = transcribe(vad)
        segs = [(st, tx) for st, tx in segments if tx]
        sys.stderr.write(f"전사 {time.time() - t1:.1f}초, {len(segs)}줄, 언어 {info.language}\n")
        if segs:
            return info.language, name, segs
        sys.stderr.write("VAD 가 전부 걸러냈다. VAD 없이 다시 돈다.\n")
    return None, name, []


def main(argv):
    if not argv:
        print(__doc__)
        sys.exit(64)
    url = argv[0]
    device = argv[argv.index("--device") + 1] if "--device" in argv else "cpu"
    if device not in ("cpu", "cuda"):
        sys.exit(f"--device 는 cpu 또는 cuda: {device}")
    if device == "cuda":
        n = preload_cuda_libs()
        sys.stderr.write(f"CUDA 라이브러리 {n}개 preload\n")

    with tempfile.TemporaryDirectory(prefix="yt-grill-") as d:
        tmp = Path(d)
        sys.stderr.write("오디오 내려받는 중\n")
        audio = download_audio(url, tmp)
        sys.stderr.write(f"whisper {CUDA_MODEL if device == 'cuda' else CPU_MODEL} ({device}) 전사 중, {audio.stat().st_size // 1024} KiB\n")
        lang, name, segs = run(audio, device)
    print(f"# lang {lang}")
    print(f"# model {name}")
    print(f"# device {device}")
    for start, text in segs:
        print(f"{start:.1f}\t{text}")


if __name__ == "__main__":
    main(sys.argv[1:])
