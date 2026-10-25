"""A second-opinion transcriber for `check-audio --second-opinion` (docs/videos/DUBS.md).

It runs faster-whisper on the CPU and never sees the script, so a line it hears as written was
misheard by Gemini, and a line both transcribers miss the same way was really said wrong.

Setup, once, outside the repository:

    python3 -m venv ~/whisper && ~/whisper/bin/pip install faster-whisper

Then:

    node tools/video/cli.mjs check-audio --slug <slug> \
        --second-opinion "$HOME/whisper/bin/python tools/video/tts/whisper_second_opinion.py"

or set VIDEO_SECOND_OPINION to the same command. The tool appends the locale and the clips; this
prints one line per clip, "<clip file name> <transcript>". WHISPER_MODEL picks the model
(default large-v3, about 3 GB on first use; medium is faster and was enough for zh-TW).

The English words each line says (the hints Gemini gets too) arrive as a JSON file named in
VIDEO_SECOND_OPINION_HINTS; they go into Whisper's prompt so that Veo is not written VO or Viu.
The script's sentences are never passed.

The clips are read here, not by faster-whisper: its decoder calls PyAV with a keyword PyAV 19
removed (``av.open(..., metadata_errors=...)``), and on 2026-10-10 that made the production
second opinion fail on every clip, so every line Gemini doubted stayed flagged. The tool's clips
are 16-bit PCM WAV, which the standard library reads; the samples go to Whisper at 16 kHz. The
transcripts are written as UTF-8 whatever the console's code page (Windows' cp1252 could not
print Japanese).
"""

import array
import json
import os
import sys
import wave

# Whisper's own codes; es, pt, id, vi and th are dubs since 2026-10-20 (large-v3 has all five).
LANGUAGES = {"zh-TW": "zh", "en": "en", "ja": "ja", "ko": "ko", "es": "es", "pt": "pt", "id": "id", "vi": "vi", "th": "th"}
# Whisper writes Mandarin in Simplified characters unless the prompt is in Traditional ones.
PROMPTS = {"zh-TW": "以下是繁體中文的句子。"}
# The rate Whisper's models are trained on.
WHISPER_RATE = 16_000


def read_wav(path: str) -> tuple[list[float], int]:
    """A 16-bit PCM WAV's samples as floats in [-1, 1], channels averaged, with its rate."""
    with wave.open(path, "rb") as clip:
        if clip.getsampwidth() != 2 or clip.getcomptype() != "NONE":
            raise ValueError(f"{os.path.basename(path)}: expected 16-bit PCM WAV")
        channels, rate = clip.getnchannels(), clip.getframerate()
        frames = array.array("h", clip.readframes(clip.getnframes()))
    if sys.byteorder == "big":
        frames.byteswap()
    if channels > 1:
        mono = [sum(frames[i : i + channels]) / channels for i in range(0, len(frames), channels)]
    else:
        mono = list(frames)
    return [sample / 32768.0 for sample in mono], rate


def resample(samples: list[float], rate: int, target: int = WHISPER_RATE) -> list[float]:
    """Samples at ``target`` Hz, linearly interpolated; enough for speech recognition."""
    if rate == target or not samples:
        return list(samples)
    count = max(1, round(len(samples) * target / rate))
    step = (len(samples) - 1) / max(1, count - 1)
    out = []
    for index in range(count):
        position = index * step
        left = int(position)
        right = min(left + 1, len(samples) - 1)
        fraction = position - left
        out.append(samples[left] * (1 - fraction) + samples[right] * fraction)
    return out


def emit(name: str, text: str, stream=None) -> None:
    """One output line, "<clip file name> <transcript>", as UTF-8 bytes."""
    target = stream if stream is not None else sys.stdout.buffer
    target.write(f"{name} {text}\n".encode("utf-8"))
    target.flush()


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("usage: whisper_second_opinion.py <locale> <clip.wav>...", file=sys.stderr)
        return 2
    locale, files = argv[1], argv[2:]
    hints: dict[str, list[str]] = {}
    if os.environ.get("VIDEO_SECOND_OPINION_HINTS"):
        with open(os.environ["VIDEO_SECOND_OPINION_HINTS"], encoding="utf-8") as handle:
            hints = json.load(handle)
    import numpy
    from faster_whisper import WhisperModel

    model = WhisperModel(os.environ.get("WHISPER_MODEL", "large-v3"), device="cpu", compute_type="int8")
    for file in files:
        words = hints.get(os.path.basename(file)) or []
        prompt = " ".join(part for part in (PROMPTS.get(locale, ""), "、".join(words)) if part) or None
        samples, rate = read_wav(file)
        audio = numpy.asarray(resample(samples, rate), dtype=numpy.float32)
        segments, _ = model.transcribe(audio, language=LANGUAGES.get(locale), beam_size=5, initial_prompt=prompt)
        text = " ".join("".join(segment.text for segment in segments).split())
        emit(os.path.basename(file), text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
