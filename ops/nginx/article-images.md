# Article image rate limits

On 2026-09-14 the existing browser resource timing entries recorded HTTP 429 for six
`/guides/<slug>/hero.jpg` covers. The images stayed broken until another request.

`10-rate-limit.conf` now maps only the local image path contract to an empty request
limit key. Nginx does not count empty keys. The new `mokaair_content_pages` zone keeps
the existing 5 requests/second and burst 20 for HTML. API and connection limits remain
unchanged. Query parameters do not affect `$uri` matching.

The frontend preserves the original server-rendered URL, dimensions and eager/lazy
loading. A failed image retries after 2 and 5 seconds, plus up to 0.5 seconds of jitter.
Retry query parameters avoid reusing a cached failed response. There are at most two
retries per mounted source, including errors before hydration; navigation cancels timers.

## Host activation (separate from the web release)

Do not assume the template is the enabled host configuration. Before activation, inspect
`nginx -T` to identify the enabled server and its current page limit zone. Back up the
active nginx configuration. Install the updated `10-rate-limit.conf` using the normal
installer, then change the active site's page location from
`limit_req zone=mokaair_pages burst=20 nodelay;` to
`limit_req zone=mokaair_content_pages burst=20 nodelay;`.

The installer leaves existing site files alone, so installing the snippet by itself does
not activate this fix. Retaining the legacy zone keeps that intermediate state valid.
The new zone name also allows a graceful reload without attempting to change the key
of an existing shared-memory zone. Preserve API/connection limits and upstream settings.

Run `nginx -t`, then reload as a separate activation step. Verify normal list-to-article
navigation and the image response statuses in a browser. Do not load-test production.
The web image retry component requires a separate web build/release.

Rollback: restore the backed-up config, run `nginx -t`, then reload. Restore the web
release separately if needed. No host changes have been performed by this implementation.

## Local validation

`python3 tools/test-guide-image-rate-limit.py /path/to/nginx` starts a temporary local
nginx and fixture upstream using the real CI harness. It checks image bursts, a still
available page budget afterward, page 429s and paths that must not receive the exemption.
