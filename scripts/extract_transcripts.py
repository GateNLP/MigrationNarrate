
#!/usr/bin/env python3

import os
import sys
import subprocess
from pathlib import Path

try:
    from tqdm import tqdm
except Exception:
    def tqdm(x, **k): return x

from faster_whisper import WhisperModel


def transcribe_to_txt(model, media_path: Path) -> bool:
    """
    Transcribe a single media file to <same_name>.txt.
    Always converts input to 16k mono WAV first for more stable decoding.
    """
    base = media_path.with_suffix("")
    txt_path = Path(str(base) + ".txt")
    wav_path = Path(str(base) + ".tmp_16k_mono.wav")

    try:
        # Convert everything to a clean WAV first
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(media_path), "-vn", "-ac", "1", "-ar", "16000", str(wav_path)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        segments, info = model.transcribe(
            str(wav_path),
            language=None,                    # auto-detect
            vad_filter=False,
            beam_size=1,
            temperature=0.0,
            condition_on_previous_text=False,
            word_timestamps=False,
        )

        segments = list(segments)

        with txt_path.open("w", encoding="utf-8") as f:
            f.write(f"Language: {info.language} (p={info.language_probability:.2f})\n\n")
            for s in segments:
                text = (s.text or "").strip()
                if text:
                    f.write(text + "\n")

        return True

    except FileNotFoundError:
        print(f"[WARN] ffmpeg not found; cannot process {media_path.name}.", file=sys.stderr)
    except Exception as e:
        print(f"[ERROR] {media_path.name}: {e}", file=sys.stderr)
    finally:
        try:
            if wav_path.exists():
                wav_path.unlink()
        except Exception:
            pass

    return False


def load_model(model_size: str, prefer_gpu: bool = True):
    """
    Try GPU first if requested, otherwise fall back to CPU.
    """
    if prefer_gpu:
        try:
            print(f"Loading model '{model_size}' on GPU...", file=sys.stderr)
            model = WhisperModel(
                model_size,
                device="cuda",
                compute_type="float16",
            )
            print("Using GPU (cuda, float16).", file=sys.stderr)
            return model
        except Exception as e:
            print(f"[WARN] GPU load failed: {e}", file=sys.stderr)
            print("Falling back to CPU.", file=sys.stderr)

    cpu_count = os.cpu_count() or 2
    cpu_threads = max(1, cpu_count // 2)

    print(f"Loading model '{model_size}' on CPU (int8, {cpu_threads} threads)...", file=sys.stderr)
    model = WhisperModel(
        model_size,
        device="cpu",
        compute_type="int8",
        cpu_threads=cpu_threads,
        num_workers=1,
    )
    return model


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_transcripts.py /path/to/media [model_size] [--cpu]", file=sys.stderr)
        print("model_size: tiny | base | small | medium | large-v3 (default: large-v3)", file=sys.stderr)
        sys.exit(1)

    root = Path(sys.argv[1]).expanduser().resolve()
    model_size = "large-v3"
    force_cpu = False

    # Parse optional args
    extra_args = sys.argv[2:]
    for arg in extra_args:
        if arg == "--cpu":
            force_cpu = True
        elif not arg.startswith("--"):
            model_size = arg

    if not root.exists():
        print(f"Folder not found: {root}", file=sys.stderr)
        sys.exit(1)

    model = load_model(model_size=model_size, prefer_gpu=not force_cpu)

    exts = (".mp4", ".mkv", ".mov", ".avi", ".mp3", ".wav", ".m4a")
    files = sorted([p for p in root.rglob("*") if p.suffix.lower() in exts])

    if not files:
        print(f"No media files found under {root}", file=sys.stderr)
        sys.exit(0)

    pending = []
    for p in files:
        txt_path = Path(str(p.with_suffix("")) + ".txt")
        if not txt_path.exists():
            pending.append(p)

    total = len(files)
    todo = len(pending)
    already = total - todo

    print(
        f"Found {total} media file(s) under {root}.\n"
        f"→ {todo} need transcription, {already} already have .txt.",
        file=sys.stderr,
    )

    if todo == 0:
        print("Nothing to do. All files already have .txt.", file=sys.stderr)
        sys.exit(0)

    ok = 0
    for p in tqdm(pending, total=todo):
        try:
            if transcribe_to_txt(model, p):
                ok += 1
                print(f"[SAVED] {p.name}")
        except KeyboardInterrupt:
            print("\nInterrupted.", file=sys.stderr)
            break
        except Exception as e:
            print(f"[ERROR] {p.name}: {e}", file=sys.stderr)

    print(
        f"Done. New transcriptions: {ok}/{todo}. "
        f"Total media files: {total} (already had .txt: {already}).",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
