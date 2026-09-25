# syntax=docker/dockerfile:1
# The video worker (docs/videos/AUTOMATION.md): tools/video with Chromium, ffmpeg and the fonts,
# running `node tools/video/cli.mjs auto` in a loop. Built from the repository root;
# ops/video/Dockerfile.dockerignore replaces the root .dockerignore, which keeps tools/ and docs/
# out of the web image.
#
# Playwright's image already holds the browsers for its version, so the npm package below must be
# the same version (package-lock.json pins @playwright/test 1.63.0).
FROM mcr.microsoft.com/playwright:v1.63.0-noble AS worker

RUN apt-get update \
 && apt-get install -y --no-install-recommends ffmpeg \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/mokaair
COPY ops/video/package.json ./package.json
RUN npm install --omit=dev --no-audit --no-fund && npm cache clean --force

COPY tools/video ./tools/video
COPY .agents/skills/youtube-video ./.agents/skills/youtube-video
# The channel spec, the pronunciation dictionary and the earlier videos, so a new draft does not
# repeat one; the volume mounted here keeps what the worker adds to them.
COPY docs/videos ./docs/videos
# Content packs, so a script can name the site article it comes from and lint can check it.
COPY apps/api/app/guides/content ./apps/api/app/guides/content
COPY ops/video/worker.sh /usr/local/bin/video-worker

# pwuser (uid 1001) comes with the image. Named volumes start from what the image has at their
# mount points, owner included.
RUN chmod 0755 /usr/local/bin/video-worker \
 && mkdir -p /var/lib/mokaair/video-work /var/lib/mokaair/video-home \
 && chown -R pwuser:pwuser /var/lib/mokaair /opt/mokaair/docs/videos

USER pwuser
ENV VIDEO_WORKDIR=/var/lib/mokaair/video-work \
    HOME=/var/lib/mokaair/video-home \
    NODE_ENV=production
CMD ["/usr/local/bin/video-worker"]

# CI builds this target (.github/workflows/video-worker-image.yml): the example video through
# render, assemble and package inside the image, as the worker user, so a missing font, codec
# or browser fails the build here instead of on the host. Chromium needs more /dev/shm than a
# build step gets by default for 1080p pages.
FROM worker AS smoke
RUN --mount=type=tmpfs,target=/dev/shm \
    set -e; \
    sh -n /usr/local/bin/video-worker; \
    test "$(id -un)" = pwuser; \
    ffmpeg -hide_banner -encoders | grep -q libx264; \
    test -f .agents/skills/youtube-video/references/script-writing.md; \
    test -f docs/videos/README.md; \
    test ! -e "$HOME/.mokaair/video-tool.json"; \
    ! find /opt/mokaair -name '.env*' | grep -q .; \
    node tools/video/assemble/smoke.mjs --workdir /tmp/video-smoke

# The image compose builds: the worker itself, without the smoke test's files.
FROM worker
