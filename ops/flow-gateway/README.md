# Mokaair Flow & Flow Music MCP Gateway (`ops/flow-gateway`)

Runs both `mokaair-flow` (18 tools) and `mokaair-flow-music` (17 tools) as a
non-root host service (`flowbot`), listening on a host Unix domain socket
(`/run/mokaair-flow-gateway/gateway.sock`, mode `0660`, group `travel-api`)
behind HMAC-SHA256 signed requests from `apps/api` (`POST /api/v1/video/mcp/{flow|flow-music}`).

Locally (outside Docker), the gateway also supports loopback-only TCP
(`127.0.0.1:8792`) when `FLOW_MCP_GATEWAY_SOCKET` is unset.

## Security model

- Cloud environments pair once via `node tools/video/cli.mjs login --flow`
  (RFC 8628 device flow; owner approves on `/admin/settings`) and receive a
  video tool token (`mkv_...`) with `flow_access = true`.
- `apps/web/app/api/video/mcp/[service]/route.ts` forwards only `Authorization: Bearer mkv_...`
  (never cookies) to `apps/api`.
- `apps/api` verifies the token, enforces `token.flow_access`, rate-limits,
  audits every `tools/call` in `admin_audit_logs`, signs the body with
  `FLOW_MCP_GATEWAY_SECRET`, and forwards over the mounted Unix socket
  (`/run/mokaair-flow-gateway/gateway.sock`, read-only bind mount opened via
  the `travel-api` group) to `tools/video/flow-mcp/gateway.mjs`.
- The gateway never binds to a public network interface.

## Installation on production host

```bash
bash ops/flow-gateway/install.sh --runtime-env /root/travel_scanner/.env
```

This creates `/etc/travel-scanner/flow-gateway.env` (`0600 flowbot:flowbot`),
syncs `tools/video` to `/opt/mokaair-flow-gateway/travel_scanner`, writes
`FLOW_MCP_GATEWAY_ENABLED`, `FLOW_MCP_GATEWAY_SOCKET`, and the shared
`FLOW_MCP_GATEWAY_SECRET` into `/root/travel_scanner/.env` (keeping mode `0600`),
and enables `mokaair-flow-gateway.service`.

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
