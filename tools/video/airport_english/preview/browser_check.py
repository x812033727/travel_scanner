#!/usr/bin/env python3
"""Exercise the preview with real media via localhost; never use file://.

Requires Python Playwright and Chromium. --bundle is an existing unpacked bundle
with lessons.js and relative media; media are symlinked into a temporary wrapper.
Nothing in the supplied bundle is modified or copied into the repository.
"""

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    bundle = args.bundle.resolve()
    catalog_source = (bundle / "lessons.js").read_text()
    catalog = json.loads(catalog_source.split("window.LESSONS=", 1)[1].strip().removesuffix(";"))
    days = {episode["day"]: episode for episode in catalog}
    assert 2 in days and 3 in days, "Regression fixture requires Day02 and Day03"
    checks = []
    errors = []
    with tempfile.TemporaryDirectory(prefix="airport-preview-browser-") as temporary:
        wrapper = Path(temporary)
        for child in bundle.iterdir():
            (wrapper / child.name).symlink_to(child, target_is_directory=child.is_dir())
        for name in ["START_HERE.html", "player.mjs", "controller.mjs", "style.css"]:
            (wrapper / name).unlink(missing_ok=True)
            (wrapper / name).symlink_to(source / name)
        server = subprocess.Popen(["python3", str(source / "serve.py"), "--directory", str(wrapper), "--port", "0"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        try:
            url = server.stdout.readline().strip()
            assert url.startswith("http://127.0.0.1:"), url
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(executable_path=shutil.which("chromium"), headless=True, args=["--no-sandbox"])
                page = browser.new_page(viewport={"width": 1280, "height": 1024})
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.route("**/*", lambda route: route.continue_() if urlparse(route.request.url).hostname == "127.0.0.1" else route.abort())
                page.goto(url + "#day2")
                page.wait_for_function("document.querySelector('#player').readyState >= 1")

                def snapshot():
                    return page.evaluate("""() => {
                      const v = document.querySelector('#player'), a = document.querySelector('#alternate');
                      return { voice: document.querySelector('#voice').value, videoMuted: v.muted,
                        audioMuted: a.muted, videoRate: v.playbackRate, audioRate: a.playbackRate,
                        videoTime: v.currentTime, audioTime: a.currentTime, paused: v.paused,
                        audioPaused: a.paused, label: v.getAttribute('aria-label'),
                        cc: document.querySelector('#caption-text').textContent,
                        tracks: Array.from(v.textTracks).map(t => ({ language: t.language, count: t.cues.length })) };
                    }""")

                page.select_option("#speed", "1.25")
                for day in [2, 3, 2]:
                    page.select_option("#episode", str(day))
                    page.wait_for_function("document.querySelector('#player').readyState >= 1")
                    state = snapshot()
                    assert f"第 {day} 集" in state["label"]
                    assert state["videoRate"] == state["audioRate"] == 1.25
                    for track in state["tracks"]:
                        assert track["count"] == len(days[day]["captions"][track["language"]]), state
                    page.evaluate("document.querySelector('#player').currentTime = 46")
                    page.wait_for_function("!document.querySelector('#player').seeking")
                    for locale in ["zh-Hant", "zh-Hans", "ja", "ko"]:
                        page.select_option("#captions", locale)
                        expected = "\n".join(text for start, end, text in days[day]["captions"][locale] if start <= 46 < end)
                        assert snapshot()["cc"] == expected
                checks.append("Day02→03→02: all four track cue counts and displayed translations match only the current lesson; speed and accessible episode label persist")

                page.select_option("#voice", "ja")
                page.wait_for_function("!document.querySelector('#voice').disabled")
                assert snapshot()["voice"] == "ja"
                page.click("#play")
                page.wait_for_function("!document.querySelector('#alternate').paused")
                page.evaluate("document.querySelector('#player').currentTime = 480")
                page.wait_for_function("!document.querySelector('#player').seeking && !document.querySelector('#alternate').paused")
                state = snapshot()
                assert abs(state["videoTime"] - state["audioTime"]) < .3, state
                assert state["videoRate"] == state["audioRate"] == 1.25
                assert state["videoMuted"] and not state["audioMuted"]
                page.click("#play")
                page.wait_for_function("document.querySelector('#alternate').paused")
                checks.append("Japanese alternate plays; seek to 480s and 1.25× rate stay synchronized within 0.3s; pause stops both streams")

                page.route("**/" + days[2]["audio"]["ko"], lambda route: route.abort())
                for muted in [False, True]:
                    if muted:
                        page.click("#mute-audio")
                    page.select_option("#voice", "ko")
                    page.wait_for_function("!document.querySelector('#voice').disabled")
                    state = snapshot()
                    assert state["voice"] == "en" and state["videoMuted"] == muted, state
                    assert page.evaluate("document.querySelector('#alternate').getAttribute('src')") is None
                checks.append("Aborted Korean audio recovers actual English routing, clears failed source, and preserves both unmuted and muted user intent")

                page.set_viewport_size({"width": 390, "height": 844})
                page.select_option("#captions", "zh-Hant")
                page.evaluate("document.querySelector('#player').currentTime = 46")
                page.wait_for_function("!document.querySelector('#player').seeking")
                layout = page.evaluate("""() => {
                  const video = document.querySelector('video').getBoundingClientRect();
                  const caption = document.querySelector('#caption-band').getBoundingClientRect();
                  const controls = document.querySelector('.transport').getBoundingClientRect();
                  return { videoBottom: video.bottom, captionTop: caption.top, captionBottom: caption.bottom,
                    controlsTop: controls.top, pageWidth: document.documentElement.scrollWidth, width: innerWidth };
                }""")
                assert layout["videoBottom"] <= layout["captionTop"] + 1
                assert layout["captionBottom"] <= layout["controlsTop"] + 1
                assert layout["pageWidth"] <= layout["width"]
                args.report.parent.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(args.report.with_suffix(".mobile.png")), full_page=True)
                checks.append("390px mobile: translation band is below the picture and above controls, with no horizontal overflow")
                assert not errors, errors
                browser.close()
        finally:
            server.terminate()
            server.wait(timeout=5)
    report = {"transport": "localhost HTTP byte ranges; external browser requests blocked", "file_protocol": "unsupported; not attempted", "media": "existing prototype used only as functional fixture; this does not approve production media", "checks": checks, "page_errors": errors}
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
