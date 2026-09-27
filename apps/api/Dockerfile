FROM python:3.13-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv && uv sync --frozen --no-dev --no-install-project
COPY . .
RUN uv sync --frozen --no-dev
RUN groupadd --system --gid 10001 app && useradd --system --uid 10001 --gid app --home-dir /nonexistent --shell /usr/sbin/nologin app
# Video review previews (docker-compose.prod.yml mounts a volume here); a new named volume takes
# the ownership of the directory it is mounted over, so the app user can write to it.
RUN mkdir -p /var/lib/mokaair/video-reviews /var/lib/mokaair/video-media && chown -R app:app /var/lib/mokaair
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
USER 10001:10001
EXPOSE 8000
