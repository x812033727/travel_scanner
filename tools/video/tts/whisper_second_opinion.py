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
"""

import os
import sys

LANGUAGES = {"zh-TW": "zh", "zh-CN": "zh", "en": "en", "ja": "ja", "ko": "ko"}
# Whisper writes Mandarin in Simplified characters unless the prompt is in Traditional ones.
PROMPTS = {"zh-TW": "以下是繁體中文的句子。", "zh-CN": "以下是简体中文的句子。"}


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("usage: whisper_second_opinion.py <locale> <clip.wav>...", file=sys.stderr)
        return 2
    locale, files = argv[1], argv[2:]
    from faster_whisper import WhisperModel

    model = WhisperModel(os.environ.get("WHISPER_MODEL", "large-v3"), device="cpu", compute_type="int8")
    for file in files:
        segments, _ = model.transcribe(
            file, language=LANGUAGES.get(locale), beam_size=5, initial_prompt=PROMPTS.get(locale)
        )
        text = " ".join("".join(segment.text for segment in segments).split())
        print(f"{os.path.basename(file)} {text}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
