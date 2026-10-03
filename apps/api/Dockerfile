# Tag and digest: a tag moved on the registry cannot change this image without a diff here.
# Dependabot (.github/dependabot.yml, docker) moves the digest by pull request.
FROM python:3.13-slim@sha256:bb2988715db2cf7ace7b53f38f3cffbef7c7046a656bee66245eb0ed386e2e81
WORKDIR /app
COPY pyproject.toml uv.lock ./
# The uv CI's setup-uv installed when this was pinned (2026-10-02). Dependabot does not read a pip
# pin inside RUN, so it is bumped by hand; CI's containers job builds this image, so a uv.lock
# this uv cannot read fails there, not on the host.
RUN pip install --no-cache-dir uv==0.12.22 && uv sync --frozen --no-dev --no-install-project
COPY . .
RUN uv sync --frozen --no-dev
RUN groupadd --system --gid 10001 app && useradd --system --uid 10001 --gid app --home-dir /nonexistent --shell /usr/sbin/nologin app
# Video review previews (docker-compose.prod.yml mounts a volume here); a new named volume takes
# the ownership of the directory it is mounted over, so the app user can write to it.
RUN mkdir -p /var/lib/mokaair/video-reviews /var/lib/mokaair/video-media && chown -R app:app /var/lib/mokaair
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
USER 10001:10001
EXPOSE 8000
