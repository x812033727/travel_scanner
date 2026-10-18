# Tag and digest: a tag moved on the registry cannot change this image without a diff here.
# Dependabot (.github/dependabot.yml, docker) moves the digest by pull request.
FROM node:24-bookworm-slim@sha256:d6aa754f16b3197301076f047b5def2f02ea1dbbc2ca920407d46d7ec7f87b20
ENV NODE_ENV=production DISPLAY=:99 UPLOADER_BIND=0.0.0.0 UPLOADER_DATA_DIR=/var/lib/mokaair-uploader
WORKDIR /opt/uploader
COPY services/youtube-uploader/package*.json ./
RUN npm ci --omit=dev --no-audit --no-fund \
 && npx playwright install --with-deps chromium \
 && apt-get update \
 && apt-get install -y --no-install-recommends xvfb x11-utils x11vnc openbox novnc websockify \
 && rm -rf /var/lib/apt/lists/* \
 && mkdir -p /var/lib/mokaair-uploader \
 && chown -R node:node /var/lib/mokaair-uploader /opt/uploader /root/.cache/ms-playwright \
 && mv /root/.cache/ms-playwright /opt/uploader/browsers
ENV PLAYWRIGHT_BROWSERS_PATH=/opt/uploader/browsers
COPY --chown=node:node services/youtube-uploader/src ./src
COPY ops/youtube-uploader/start.sh /usr/local/bin/start-uploader
RUN chmod 0755 /usr/local/bin/start-uploader
USER node
CMD ["/usr/local/bin/start-uploader"]
