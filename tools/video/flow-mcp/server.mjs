#!/usr/bin/env node
/**
 * Zero-dependency MCP (Model Context Protocol) JSON-RPC 2.0 stdio server for
 * Mokaair's subscription-backed Google Flow workflow (`mokaair-flow`).
 *
 * Compatible with Claude Code, Claude Desktop, Codex, Antigravity, Cursor, and
 * VS Code. Handles both newline-delimited JSON-RPC (MCP 2024-11-05 / 2025-03-26)
 * and Content-Length framed messages cleanly. Never writes non-JSON to stdout.
 */

import { fileURLToPath } from "node:url";
import { MCP_SERVER_NAME, MCP_SERVER_VERSION } from "./config.mjs";
import { FlowOrchestrator } from "./orchestrator.mjs";

const SUPPORTED_PROTOCOL_VERSIONS = ["2025-03-26", "2024-11-05"];

export const MCP_TOOLS = Object.freeze([
  {
    name: "flow_status",
    description:
      "Check Google Flow Chrome session authentication, subscription credit balance, and cross-client profile lock status. Spends 0 credits.",
    annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      properties: {
        profile: { type: "string", description: "Optional gflow profile name." },
        refreshCredits: { type: "boolean", description: "Force live credit balance refresh." },
      },
      additionalProperties: false,
    },
  },
  {
    name: "flow_init_episode",
    description:
      "Initialize or bind dual isolated Google Flow projects (character vs scenery) for work/video-episodes/<slug>/ and discover locked canon character sheets. Spends 0 credits.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: true },
    inputSchema: {
      type: "object",
      required: ["slug"],
      properties: {
        slug: { type: "string", description: "Episode slug (e.g. curio-w31-topic or sothatswhy-p03-topic)." },
        series: { type: "string", enum: ["sothatswhy", "curio", "shorts", "custom"] },
        characterProjectId: { type: "string", description: "Existing Flow project ID for character shots." },
        sceneryProjectId: { type: "string", description: "Existing Flow project ID for zero-character scenery shots." },
        createProjects: { type: "boolean", description: "Auto-create missing character/scenery projects in Flow." },
        uploadCanonRefs: { type: "boolean", description: "Upload series canon sheets to the character project." },
        extraCharacterRefs: { type: "array", items: { type: "string" }, description: "Extra local character ref paths." },
        profile: { type: "string" },
      },
      additionalProperties: false,
    },
  },
  {
    name: "flow_preflight_shotlist",
    description:
      "Run 0-credit preflight on work/video-episodes/<slug>/flow-shot-list.json: full-axis safety prompt scan (minor/violence/IP terms), dual-project isolation, retention redlines (<=3 consecutive stills, <=8s still), and series credit cap check.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["slug"],
      properties: {
        slug: { type: "string" },
        series: { type: "string", enum: ["sothatswhy", "curio", "shorts", "custom"] },
      },
      additionalProperties: false,
    },
  },
  {
    name: "flow_generate_stills",
    description:
      "Generate 0-credit 16:9 stills/keyframes with Nano Banana 2.1 (nano2.1), enforce 1376x768 binary dimensions (quarantining silent 1:1 resets), and build stills/qa-gallery.html. Returns job_id immediately for flow_wait.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: true },
    inputSchema: {
      type: "object",
      required: ["slug"],
      properties: {
        slug: { type: "string" },
        series: { type: "string", enum: ["sothatswhy", "curio", "shorts", "custom"] },
        shotIds: { type: "array", items: { type: "string" }, description: "Optional subset of shot IDs to generate." },
        model: { type: "string", description: "Image model alias (default: nano2.1)." },
        overwriteApproved: { type: "boolean", description: "Regenerate even if already QA-approved (default: false)." },
        profile: { type: "string" },
        waitMs: { type: "number", description: "Optional bounded wait in ms before returning (max 45000)." },
      },
      additionalProperties: false,
    },
  },
  {
    name: "flow_approve_stills",
    description:
      "Record visual QA approvals/rejections for generated stills (re-verifying 1376x768 on disk) to unlock paid clip generation. Spends 0 credits.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["slug"],
      properties: {
        slug: { type: "string" },
        series: { type: "string", enum: ["sothatswhy", "curio", "shorts", "custom"] },
        approved: {
          type: "array",
          items: {
            oneOf: [
              { type: "string" },
              { type: "object", required: ["shotId"], properties: { shotId: { type: "string" }, note: { type: "string" } } },
            ],
          },
        },
        rejected: {
          type: "array",
          items: {
            oneOf: [
              { type: "string" },
              { type: "object", required: ["shotId"], properties: { shotId: { type: "string" }, note: { type: "string" } } },
            ],
          },
        },
        reviewer: { type: "string" },
      },
      additionalProperties: false,
    },
  },
  {
    name: "flow_plan_clips",
    description:
      "Dry-run paid video generation for QA-approved clip shots: verifies Stills-First gate, checks series credit cap (sothatswhy<=500, curio<=550/600), and mints a single-use confirm_token for owner confirmation. Spends 0 credits.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["slug"],
      properties: {
        slug: { type: "string" },
        series: { type: "string", enum: ["sothatswhy", "curio", "shorts", "custom"] },
        shotIds: { type: "array", items: { type: "string" } },
        model: { type: "string", description: "Video model alias (default: omni-1.2-flash)." },
        creditsPerClip: { type: "number", description: "Expected credits per clip (default: 12)." },
        budgetHardCapOverride: { type: "number", description: "Optional explicit owner budget override." },
        checkLiveBalance: { type: "boolean", description: "Verify live account credit balance via gflow." },
        profile: { type: "string" },
      },
      additionalProperties: false,
    },
  },
  {
    name: "flow_generate_clips",
    description:
      "PAID TOOL (spends Google AI subscription Flow credits). Requires a single-use confirm_token from flow_plan_clips after owner approval. Generates 4s Omni 1.2 Flash clips, downloads free 720p raw MP4, locally upscales to 1080p30 bt709 tv -an via FFmpeg, and writes 4-frame QA sheets + SHA-256 manifest. Returns job_id for flow_wait.",
    annotations: { readOnlyHint: false, destructiveHint: true, openWorldHint: true },
    inputSchema: {
      type: "object",
      required: ["slug", "confirm_token"],
      properties: {
        slug: { type: "string" },
        confirm_token: { type: "string", description: "Single-use token from flow_plan_clips after owner approval." },
        series: { type: "string", enum: ["sothatswhy", "curio", "shorts", "custom"] },
        shotIds: { type: "array", items: { type: "string" } },
        model: { type: "string" },
        durationSec: { type: "number" },
        creditsPerClip: { type: "number" },
        maxCreditsPerClip: { type: "number" },
        skipPostprocess: { type: "boolean" },
        profile: { type: "string" },
        waitMs: { type: "number" },
      },
      additionalProperties: false,
    },
  },
  {
    name: "flow_wait",
    description:
      "Wait up to 45s for a background stills or clips job_id to progress or complete without tripping MCP client 60s timeouts. Spends 0 credits.",
    annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["job_id"],
      properties: {
        job_id: { type: "string" },
        timeout_ms: { type: "number", description: "Max wait milliseconds (default 25000, max 45000)." },
      },
      additionalProperties: false,
    },
  },
  {
    name: "flow_cancel",
    description:
      "Cancel a queued or running Flow job_id cleanly without deleting already completed files. Spends 0 credits.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["job_id"],
      properties: {
        job_id: { type: "string" },
      },
      additionalProperties: false,
    },
  },
  {
    name: "flow_episode_ledger",
    description:
      "Inspect an episode's full Flow credit ledger, stills QA summary, missing clips, and readiness for `npm run vdrive -- push-episode`. Spends 0 credits.",
    annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["slug"],
      properties: {
        slug: { type: "string" },
        series: { type: "string", enum: ["sothatswhy", "curio", "shorts", "custom"] },
      },
      additionalProperties: false,
    },
  },
]);

export function createToolDispatcher(orchestrator) {
  const handlers = {
    flow_status: (args) => orchestrator.flowStatus(args),
    flow_init_episode: (args) => orchestrator.flowInitEpisode(args),
    flow_preflight_shotlist: (args) => orchestrator.flowPreflightShotlist(args),
    flow_generate_stills: (args) => orchestrator.flowGenerateStills(args),
    flow_approve_stills: (args) => orchestrator.flowApproveStills(args),
    flow_plan_clips: (args) => orchestrator.flowPlanClips(args),
    flow_generate_clips: (args) => orchestrator.flowGenerateClips(args),
    flow_wait: (args) => orchestrator.flowWait(args),
    flow_cancel: (args) => orchestrator.flowCancel(args),
    flow_episode_ledger: (args) => orchestrator.flowEpisodeLedger(args),
  };

  return async function dispatch(name, args = {}) {
    const fn = handlers[name];
    if (!fn) {
      return {
        isError: true,
        content: [{ type: "text", text: JSON.stringify({ ok: false, error: `Unknown tool "${name}"` }, null, 2) }],
      };
    }
    try {
      const result = await fn(args || {});
      const isError = result?.ok === false || result?.found === false;
      return {
        isError,
        content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      };
    } catch (err) {
      const payload = err.toJSON
        ? { ok: false, error: err.toJSON() }
        : { ok: false, error: { message: err.message } };
      return {
        isError: true,
        content: [{ type: "text", text: JSON.stringify(payload, null, 2) }],
      };
    }
  };
}

export async function handleJsonRpcMessage(msg, { dispatch }) {
  if (!msg || typeof msg !== "object" || msg.jsonrpc !== "2.0") {
    return {
      jsonrpc: "2.0",
      id: msg?.id ?? null,
      error: { code: -32600, message: "Invalid JSON-RPC 2.0 Request" },
    };
  }

  // Notifications have no `id` and expect no response
  if (msg.id === undefined || msg.id === null) {
    return null;
  }

  const { id, method, params } = msg;

  switch (method) {
    case "initialize": {
      const requested = params?.protocolVersion;
      const protocolVersion = SUPPORTED_PROTOCOL_VERSIONS.includes(requested)
        ? requested
        : SUPPORTED_PROTOCOL_VERSIONS[0];
      return {
        jsonrpc: "2.0",
        id,
        result: {
          protocolVersion,
          capabilities: {
            tools: { listChanged: false },
          },
          serverInfo: {
            name: MCP_SERVER_NAME,
            version: MCP_SERVER_VERSION,
          },
          instructions:
            "Mokaair Google Flow production MCP. Always run flow_preflight_shotlist -> flow_generate_stills (0 credits) -> flow_approve_stills -> flow_plan_clips -> owner confirmation -> flow_generate_clips(confirm_token). Never invent or bypass confirm_token.",
        },
      };
    }

    case "ping":
      return { jsonrpc: "2.0", id, result: {} };

    case "tools/list":
      return { jsonrpc: "2.0", id, result: { tools: MCP_TOOLS } };

    case "tools/call": {
      const name = params?.name;
      const args = params?.arguments || {};
      const result = await dispatch(name, args);
      return { jsonrpc: "2.0", id, result };
    }

    case "resources/list":
      return { jsonrpc: "2.0", id, result: { resources: [] } };

    case "prompts/list":
      return { jsonrpc: "2.0", id, result: { prompts: [] } };

    default:
      return {
        jsonrpc: "2.0",
        id,
        error: { code: -32601, message: `Method not found: ${method}` },
      };
  }
}

/**
 * Starts the stdio transport supporting both newline-delimited JSON-RPC and
 * `Content-Length` framed input. Echoes back in the same framing style the
 * client used.
 */
export function startStdioServer({
  orchestrator = new FlowOrchestrator(),
  stdin = process.stdin,
  stdout = process.stdout,
  stderr = process.stderr,
} = {}) {
  const dispatch = createToolDispatcher(orchestrator);
  let buffer = Buffer.alloc(0);
  let useContentLength = false;

  const send = (obj) => {
    const json = JSON.stringify(obj);
    if (useContentLength) {
      const byteLen = Buffer.byteLength(json, "utf8");
      stdout.write(`Content-Length: ${byteLen}\r\n\r\n${json}`);
    } else {
      stdout.write(`${json}\n`);
    }
  };

  const processMessage = async (rawText) => {
    let msg;
    try {
      msg = JSON.parse(rawText);
    } catch (err) {
      send({
        jsonrpc: "2.0",
        id: null,
        error: { code: -32700, message: `Parse error: ${err.message}` },
      });
      return;
    }

    try {
      const response = await handleJsonRpcMessage(msg, { dispatch });
      if (response) send(response);
    } catch (err) {
      stderr.write(`[mokaair-flow] unhandled error: ${err.stack || err.message}\n`);
      if (msg.id !== undefined && msg.id !== null) {
        send({
          jsonrpc: "2.0",
          id: msg.id,
          error: { code: -32603, message: err.message },
        });
      }
    }
  };

  const drain = () => {
    while (buffer.length > 0) {
      // Check for Content-Length framing
      const headPreview = buffer.subarray(0, Math.min(buffer.length, 64)).toString("ascii");
      if (/^Content-Length:\s*\d+/i.test(headPreview)) {
        useContentLength = true;
        const sepIdx = buffer.indexOf("\r\n\r\n");
        if (sepIdx === -1) return;
        const headerStr = buffer.subarray(0, sepIdx).toString("ascii");
        const match = /Content-Length:\s*(\d+)/i.exec(headerStr);
        if (!match) {
          buffer = buffer.subarray(sepIdx + 4);
          continue;
        }
        const length = Number(match[1]);
        const bodyStart = sepIdx + 4;
        if (buffer.length < bodyStart + length) return;
        const body = buffer.subarray(bodyStart, bodyStart + length).toString("utf8");
        buffer = buffer.subarray(bodyStart + length);
        void processMessage(body);
        continue;
      }

      // Newline-delimited JSON-RPC framing
      const nlIdx = buffer.indexOf("\n");
      if (nlIdx === -1) return;
      const line = buffer.subarray(0, nlIdx).toString("utf8").trim();
      buffer = buffer.subarray(nlIdx + 1);
      if (line) {
        void processMessage(line);
      }
    }
  };

  stdin.on("data", (chunk) => {
    buffer = Buffer.concat([buffer, Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk, "utf8")]);
    drain();
  });

  stdin.on("error", (err) => {
    stderr.write(`[mokaair-flow] stdin error: ${err.message}\n`);
  });

  return { dispatch };
}

const isMain = process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1];
if (isMain) {
  startStdioServer();
}
