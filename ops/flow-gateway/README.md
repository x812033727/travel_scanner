# Mokaair Flow & Flow Music MCP Gateway (`ops/flow-gateway`)

Runs both `mokaair-flow` (18 tools) and `mokaair-flow-music` (17 tools) on a
non-root host service bound strictly to `127.0.0.1:8792`, behind HMAC-SHA256
signed requests from `apps/api` (`POST /api/v1/video/mcp/{flow|flow-music}`).

## Security model

- Cloud environments pair once via `node tools/video/cli.mjs login --flow`
  (RFC 8628 device flow; owner approves on `/admin/settings`) and receive a
  video tool token (`mkv_...`) with `flow_access = true`.
- `apps/web/app/api/video/mcp/[service]/route.ts` forwards only `Authorization: Bearer mkv_...`
  (never cookies) to `apps/api`.
- `apps/api` verifies the token, enforces `token.flow_access`, rate-limits,
  audits every `tools/call` in `admin_audit_logs`, signs the body with
  `FLOW_MCP_GATEWAY_SECRET`, and forwards to `FLOW_MCP_GATEWAY_URL`.
- The gateway never binds to a public interface (`127.0.0.1` only).

## Required environment variables

In `apps/api` (`.env`):

```env
FLOW_MCP_GATEWAY_ENABLED=true
FLOW_MCP_GATEWAY_URL=http://host.docker.internal:8792
FLOW_MCP_GATEWAY_SECRET=<at-least-32-random-hex-chars>
```

In `/etc/mokaair/flow-gateway.env` (mode `0600`, owned by `flowbot`):

```env
FLOW_MCP_GATEWAY_SECRET=<same-32+-char-secret>
MOKAAIR_FLOW_HOME=/home/flowbot/.mokaair-flow
MOKAAIR_FLOW_MUSIC_HOME=/home/flowbot/.mokaair-flow-music
```

## Pairing from any cloud environment

```bash
node tools/video/cli.mjs login --flow
```

Then either point a Streamable HTTP MCP client at:
- `https://mokaair.com/api/video/mcp/flow`
- `https://mokaair.com/api/video/mcp/flow-music`
with header `Authorization: Bearer <mkv_token>`, or use the zero-config stdio
bridge:

```bash
npm run flow -- remote-mcp
npm run flow-music -- remote-mcp
```
