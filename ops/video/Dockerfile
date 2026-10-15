# syntax=docker/dockerfile:1
# The video worker (docs/videos/AUTOMATION.md): tools/video with Chromium, ffmpeg and the fonts,
# running `node tools/video/cli.mjs auto` in a loop. Built from the repository root;
# ops/video/Dockerfile.dockerignore replaces the root .dockerignore, which keeps tools/ and docs/
# out of the web image.
#
# Playwright's image already holds the browsers for its version, so the npm package below must be
# the same version (package-lock.json pins @playwright/test 1.63.0). Tag and digest: a tag moved
# on the registry cannot change this image without a diff here; Dependabot (.github/dependabot.yml,
# docker) moves the digest by pull request.
FROM mcr.microsoft.com/playwright:v1.63.0-noble@sha256:eff16c30e6f3f4af0a03fa4b706120d5e9b0891c344a27d64559aff5900a4a27 AS worker

RUN apt-get update \
 && apt-get install -y --no-install-recommends ffmpeg python3-venv \
 && rm -rf /var/lib/apt/lists/*

# The second-opinion transcriber for `check-audio` (docs/videos/DUBS.md §聲音會唸錯的地方):
# faster-whisper on the CPU, in its own venv so it never touches the image's Python. Without it
# every line Gemini doubts counts as misheard, and on 2026-10-09 that was the reason behind 31 of
# the 49 dub tracks the worker had given up on. The model itself (WHISPER_MODEL, compose sets
# medium) is fetched on first use into HF_HOME, which compose keeps on the video_home volume so
# a rebuilt container does not fetch it again.
RUN python3 -m venv /opt/whisper \
 && /opt/whisper/bin/pip install --no-cache-dir "faster-whisper==1.2.1" \
 && /opt/whisper/bin/python -c "import faster_whisper"

WORKDIR /opt/mokaair
COPY ops/video/package.json ./package.json
RUN npm install --omit=dev --no-audit --no-fund && npm cache clean --force

COPY tools/video ./tools/video
COPY .agents/skills/youtube-video ./.agents/skills/youtube-video
# Keep the image's source outside the writable docs volume. The entrypoint refreshes that
# volume from this snapshot while preserving the worker's existing folders and dictionary.
COPY docs/videos ./docs-seed/videos
COPY ops/video/sync-docs.mjs ops/video/sync-docs.test.mjs ./ops/video/
# Content packs, so a script can name the site article it comes from and lint can check it.
COPY apps/api/app/guides/content ./apps/api/app/guides/content
COPY ops/video/worker.sh /usr/local/bin/video-worker

# pwuser (uid 1001) comes with the image. Named volumes start from what the image has at their
# mount points, owner included.
RUN chmod 0755 /usr/local/bin/video-worker \
 && mkdir -p /var/lib/mokaair/video-work /var/lib/mokaair/video-home /opt/mokaair/docs/videos \
 && chown -R pwuser:pwuser /var/lib/mokaair /opt/mokaair/docs/videos

USER pwuser
ENV VIDEO_WORKDIR=/var/lib/mokaair/video-work \
    HOME=/var/lib/mokaair/video-home \
    NODE_ENV=production
CMD ["/usr/local/bin/video-worker"]

# CI builds this target (.github/workflows/video-worker-image.yml): the example video through
# render, assemble and package inside the image, as the worker user, so a missing font, codec
# or browser fails the build here instead of on the host. The example draws no caption locale's
# thumbnail, so every font tools/video/render/fonts.mjs names is resolved and its coverage read
# on its own: a font added there but not to ops/video/package.json fails here too. Chromium needs
# more /dev/shm than a build step gets by default for 1080p pages.
FROM worker AS smoke
RUN --mount=type=tmpfs,target=/dev/shm \
    set -e; \
    sh -n /usr/local/bin/video-worker; \
    test "$(id -un)" = pwuser; \
    node --test ops/video/sync-docs.test.mjs; \
    node ops/video/sync-docs.mjs; \
    ffmpeg -hide_banner -encoders | grep -q libx264; \
    /opt/whisper/bin/python -c 'import faster_whisper'; \
    /opt/whisper/bin/python tools/video/tts/whisper_second_opinion.py 2>&1 | grep -q usage; \
    test -f .agents/skills/youtube-video/references/script-writing.md; \
    test -f docs/videos/README.md; \
    test ! -e "$HOME/.mokaair/video-tool.json"; \
    ! find /opt/mokaair -name '.env*' | grep -q .; \
    node --input-type=module -e 'const f = await import("./tools/video/render/fonts.mjs"); for (const name of Object.keys(f.FONT_PACKAGES)) console.log(f.fontDir(name)); for (const locale of [null, ...Object.keys(f.LOCALE_FONTS)]) f.bundledCoverage(locale);'; \
    node tools/video/assemble/smoke.mjs --workdir /tmp/video-smoke

# The image compose builds: the worker itself, without the smoke test's files.
FROM worker
