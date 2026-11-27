#!/usr/bin/env node
/**
 * Zero-dependency MCP (Model Context Protocol) JSON-RPC 2.0 stdio server for
 * Mokaair's subscription-backed Google Flow workflow (`mokaair-flow` v2).
 *
 * Supports explainers (`sothatswhy`, `curio`), AI dramas (`drama-16x9`,
 * `drama-9x16`), and zero-dialogue vertical Shorts (`shorts`) across
 * Claude Code, Claude Desktop, Codex, Antigravity, Cursor, and VS Code.
 */

import { fileURLToPath } from "node:url";
import { MCP_SERVER_NAME, MCP_SERVER_VERSION } from "./config.mjs";
import { FlowOrchestrator } from "./orchestrator.mjs";

const SUPPORTED_PROTOCOL_VERSIONS = ["2025-03-26", "2024-11-05"];
const SERIES_ENUM = ["sothatswhy", "curio", "drama-16x9", "drama-9x16", "shorts", "custom"];

export const MCP_TOOLS = Object.freeze([
  {
    name: "flow_status",
    description:
      "Check Google Flow Chrome session auth, gflow-cli version, subscription credit balance, and per-profile lock status. Spends 0 credits.",
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
    name: "flow_profiles",
    description:
      "List all signed-in Google AI subscription profiles, their remaining Flow credits, and per-profile lock states for multi-account production. Spends 0 credits.",
    annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      properties: {
        refreshCredits: { type: "boolean" },
      },
      additionalProperties: false,
    },
  },
  {
    name: "flow_init_episode",
    description:
      "Initialize or bind dual isolated Google Flow projects (character vs scenery) for work/video-episodes/<slug>/ across explainers, AI dramas, or Shorts. Spends 0 credits.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: true },
    inputSchema: {
      type: "object",
      required: ["slug"],
      properties: {
        slug: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
        dramaName: { type: "string", description: "Optional Drive series folder/code (e.g. zhong-tian-qu-qi, tai-nainai)." },
        episodeLabel: { type: "string", description: "Optional Drive episode folder (e.g. 第033集)." },
        characterProjectId: { type: "string" },
        sceneryProjectId: { type: "string" },
        createProjects: { type: "boolean" },
        uploadCanonRefs: { type: "boolean" },
        extraCharacterRefs: { type: "array", items: { type: "string" } },
        profile: { type: "string" },
      },
      additionalProperties: false,
    },
  },
  {
    name: "flow_register_character",
    description:
      "Register a character in episode cast.json (multiple wardrobe looks, noAccessories anti-bleed notes, local ref sheets) and optionally mint a reusable Flow @Name Character entity. Spends 0 credits.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: true },
    inputSchema: {
      type: "object",
      required: ["slug", "id"],
      properties: {
        slug: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
        dramaName: { type: "string", description: "Drama series identifier for shared cross-episode Cast." },
        saveToSeries: { type: "boolean", description: "Also save this character to shared work/video-episodes/_series/<dramaName>/cast.json." },
        id: { type: "string", description: "Character key used in shot.characters[] (e.g. protagonist, ada)." },
        name: { type: "string", description: "Display or @Name for Flow Character." },
        appearance: { type: "string" },
        refs: { type: "array", items: { type: "string" }, description: "Local paths to face/body reference sheets." },
        looks: { type: "object", description: "Map of named outfit/look keys to local reference image paths." },
        noAccessories: {
          type: "array",
          items: { type: "string" },
          description: "Items this character NEVER wears (e.g. ['glasses', 'hat']) to prevent multi-character bleed.",
        },
        voice: { type: "string" },
        createFlowEntity: { type: "boolean", description: "Call gflow character create to mint a Flow @Name character." },
        facePrompt: { type: "string" },
        bodyPrompt: { type: "string" },
        profile: { type: "string" },
      },
      additionalProperties: false,
    },
  },
  {
    name: "flow_import_video_json",
    description:
      "Convert a Mokaair video.json drama/shorts/explainer script into flow-shot-list.json + cast.json (stripping H3 <Picture N> tags, preserving data.source 0-credit cuts, end_frame, and silent comedy guards). Spends 0 credits.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["slug"],
      properties: {
        slug: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
        videoJsonPath: { type: "string", description: "Optional explicit path to video.json (defaults to work/video-episodes/<slug>/video.json)." },
        defaultModel: { type: "string" },
        defaultDurationSec: { type: "number" },
        silentAudioGuard: { type: "boolean" },
      },
      additionalProperties: false,
    },
  },
  {
    name: "flow_preflight_shotlist",
    description:
      "Run 0-credit preflight on flow-shot-list.json: safety scan, dual-project isolation, edit_from/continue_from/cut continuity validation, multi-character anti-bleed warnings, retention redlines, 3-shot pilot checks, and variable per-shot credit estimate.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["slug"],
      properties: {
        slug: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
        pilot: { type: "boolean", description: "Check as a 3-shot pilot run." },
      },
      additionalProperties: false,
    },
  },
  {
    name: "flow_generate_stills",
    description:
      "Generate 0-credit stills/keyframes with Nano Banana 2.1 (supports multi-character cast refs, same-camera edit_from i2i chaining, 3-shot pilot mode, 16:9/9:16 binary dimension check quarantining 1:1 resets, and interactive HTML QA gallery with one-click copy). Returns job_id.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: true },
    inputSchema: {
      type: "object",
      required: ["slug"],
      properties: {
        slug: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
        shotIds: { type: "array", items: { type: "string" } },
        pilot: { type: "boolean", description: "Run only the first 3 non-cut shots for a pilot." },
        model: { type: "string" },
        overwriteApproved: { type: "boolean" },
        profile: { type: "string" },
        waitMs: { type: "number" },
      },
      additionalProperties: false,
    },
  },
  {
    name: "flow_approve_stills",
    description:
      "Record visual QA approvals/rejections for generated stills (re-verifying target dimensions on disk) to unlock paid clip generation. Spends 0 credits.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["slug"],
      properties: {
        slug: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
        approved: {
          type: "array",
          items: {
            oneOf: [
              { type: "string" },
              {
                type: "object",
                required: ["shotId"],
                properties: {
                  shotId: { type: "string" },
                  note: { type: "string" },
                  relPath: { type: "string", description: "Optional relative path inside episode workdir (e.g. stills/B38.jpg)." },
                },
              },
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
      "Dry-run paid video generation: verifies Stills-First gate, MAX_CLIP_TAKES=2 cap, variable per-shot model/duration credits, pilot or resumeMissingOnly filtering, series hard caps, and mints a single-use confirm_token. Spends 0 credits.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["slug"],
      properties: {
        slug: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
        shotIds: { type: "array", items: { type: "string" } },
        pilot: { type: "boolean", description: "Plan only the first 3 clip shots for a pilot." },
        resumeMissingOnly: { type: "boolean", description: "Plan only clips not yet present in flow-clips/manifest.json." },
        forceRetake: { type: "boolean", description: "Allow exceeding MAX_CLIP_TAKES=2 after prompt redesign." },
        model: { type: "string" },
        creditsPerClip: { type: "number" },
        budgetHardCapOverride: { type: "number" },
        checkLiveBalance: { type: "boolean" },
        profile: { type: "string" },
      },
      additionalProperties: false,
    },
  },
  {
    name: "flow_generate_clips",
    description:
      "PAID TOOL (spends Google AI subscription Flow credits). Requires single-use confirm_token from flow_plan_clips. Supports i2v (start/end frame), r2v (multi-ref), Exact-Join continue_from last-frame extraction, multi-take archival in takes/, local FFmpeg 1080p30 bt709 tv -an + optional raw-audio WAV sidecar + PSNR/hard-cut QC + import-bridge.json.",
    annotations: { readOnlyHint: false, destructiveHint: true, openWorldHint: true },
    inputSchema: {
      type: "object",
      required: ["slug", "confirm_token"],
      properties: {
        slug: { type: "string" },
        confirm_token: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
        shotIds: { type: "array", items: { type: "string" } },
        model: { type: "string" },
        durationSec: { type: "number" },
        creditsPerClip: { type: "number" },
        maxCreditsPerClip: { type: "number" },
        forceRetake: { type: "boolean" },
        runQc: { type: "boolean", description: "Run FFmpeg frame-0 PSNR & mid-clip hard-cut QC (auto-on for drama series)." },
        skipPostprocess: { type: "boolean" },
        profile: { type: "string" },
        waitMs: { type: "number" },
      },
      additionalProperties: false,
    },
  },
  {
    name: "flow_select_take",
    description:
      "Promote a chosen take (e.g. take 1 or 2) from flow-clips/takes/ as the active clip while preserving all rejected takes for Google Drive backup, and refresh import-bridge.json. Spends 0 credits.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["slug", "shotId", "take"],
      properties: {
        slug: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
        shotId: { type: "string" },
        take: { type: "number" },
      },
      additionalProperties: false,
    },
  },
  {
    name: "flow_plan_extend",
    description:
      "Dry-run a seamless clip extension: checks series credit cap, live balance (suggesting alternate profiles on spillover), and mints a single-use confirm_token for flow_extend_clip. Spends 0 credits.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["slug", "shotId"],
      properties: {
        slug: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
        shotId: { type: "string" },
        durationSec: { type: "number", description: "Extension seconds (default 5)." },
        creditsEstimate: { type: "number" },
        budgetHardCapOverride: { type: "number" },
        checkLiveBalance: { type: "boolean" },
        profile: { type: "string" },
      },
      additionalProperties: false,
    },
  },
  {
    name: "flow_upscale_still",
    description:
      "Upscale a generated still via gflow image upscale to 2k (or 4k on Google AI Ultra) for high-res thumbnails/key art and record verified dimensions in stills/qa-manifest.json. Spends 0 Veo credits.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: true },
    inputSchema: {
      type: "object",
      required: ["slug", "shotId"],
      properties: {
        slug: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
        shotId: { type: "string" },
        scale: { type: "string", enum: ["2k", "4k"], description: "Target scale (default 2k; 4k requires Ultra)." },
        profile: { type: "string" },
      },
      additionalProperties: false,
    },
  },
  {
    name: "flow_extend_clip",
    description:
      "PAID TOOL (spends Flow credits). Requires confirm_token from flow_plan_extend. Extends an existing clip seamlessly via gflow video extend, archives as a new take, and upscales to 1080p30 bt709 tv.",
    annotations: { readOnlyHint: false, destructiveHint: true, openWorldHint: true },
    inputSchema: {
      type: "object",
      required: ["slug", "shotId", "prompt", "confirm_token"],
      properties: {
        slug: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
        shotId: { type: "string" },
        prompt: { type: "string" },
        confirm_token: { type: "string" },
        durationSec: { type: "number" },
        refs: { type: "array", items: { type: "string" } },
        creditsEstimate: { type: "number" },
        maxCredits: { type: "number" },
        skipPostprocess: { type: "boolean" },
        profile: { type: "string" },
        waitMs: { type: "number" },
      },
      additionalProperties: false,
    },
  },
  {
    name: "flow_reconcile",
    description:
      "Reconcile any `charged: maybe` ledger entries against Flow's catalog (`gflow data list videos`), download orphaned billed clips without double-paying, and list remaining missing clips for resume. Spends 0 credits.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: true },
    inputSchema: {
      type: "object",
      required: ["slug"],
      properties: {
        slug: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
        downloadMissing: { type: "boolean" },
        skipPostprocess: { type: "boolean" },
        recoverMediaIds: {
          type: "array",
          description: "Optional list of already-billed { shotId, mediaId } clips to download for free via `gflow data download` and normalize to 1080p30.",
          items: {
            type: "object",
            required: ["shotId", "mediaId"],
            properties: {
              shotId: { type: "string" },
              mediaId: { type: "string" },
            },
          },
        },
        profile: { type: "string" },
      },
      additionalProperties: false,
    },
  },
  {
    name: "flow_wait",
    description:
      "Wait up to 45s for a background stills/clips/extend job_id to progress or complete without tripping MCP client 60s timeouts. Spends 0 credits.",
    annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["job_id"],
      properties: {
        job_id: { type: "string" },
        timeout_ms: { type: "number" },
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
      "Inspect an episode's full Flow credit ledger, multi-take count, 0-credit cuts, stills QA summary, import-bridge.json path, and exact series-aware `npm run vdrive -- push-episode` command. Spends 0 credits.",
    annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["slug"],
      properties: {
        slug: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
      },
      additionalProperties: false,
    },
  },
  {
    name: "flow_list_files",
    description:
      "List files inside work/video-episodes/<slug>/ (optionally filtered to a relative subdir, with optional SHA-256 digests) for 0-diff remote episode sync. Spends 0 credits.",
    annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["slug"],
      properties: {
        slug: { type: "string" },
        subdir: { type: "string", description: "Optional relative subdirectory (e.g. 'stills' or 'flow-clips')." },
        includeSha256: { type: "boolean", description: "Compute SHA-256 for each listed file (default: false)." },
      },
      additionalProperties: false,
    },
  },
  {
    name: "flow_write_file",
    description:
      "Upload a file into work/video-episodes/<slug>/<relPath> (single-shot <= 512 KiB via mode='replace', or chunked via mode='begin'/'append'/'commit' with SHA-256 verification and atomic rename). Strictly jailed to safe episode extensions. Spends 0 credits.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["slug", "relPath"],
      properties: {
        slug: { type: "string" },
        relPath: { type: "string", description: "Relative file path inside work/video-episodes/<slug>/ (e.g. 'flow-shot-list.json', 'stills/B38.jpg')." },
        contentBase64: { type: "string", description: "Base64-encoded chunk (<= 512 KiB decoded)." },
        mode: { type: "string", enum: ["replace", "begin", "append", "commit"], description: "Single-shot atomic write ('replace') or chunked upload ('begin'/'append'/'commit')." },
        uploadId: { type: "string", description: "Transfer session id returned by mode='begin' (required for 'append' and 'commit')." },
        expectedSha256: { type: "string", description: "Optional 64-char hex SHA-256 verified before atomic rename." },
      },
      additionalProperties: false,
    },
  },
  {
    name: "flow_read_file",
    description:
      "Download a chunk (<= 512 KiB decoded) of a file inside work/video-episodes/<slug>/<relPath> as base64 with byte offset pagination and SHA-256 digest. Spends 0 credits.",
    annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["slug", "relPath"],
      properties: {
        slug: { type: "string" },
        relPath: { type: "string", description: "Relative file path inside work/video-episodes/<slug>/ (e.g. 'flow-clips/B38.mp4')." },
        offset: { type: "integer", minimum: 0, description: "Byte offset to start reading from (default: 0)." },
        maxBytes: { type: "integer", minimum: 1, maximum: 524288, description: "Maximum raw bytes to read (default and max: 524288)." },
      },
      additionalProperties: false,
    },
  },
  {
    name: "flow_push_drive",
    description:
      "Push work/video-episodes/<slug>/ from the gateway host to Google Drive via vdrive.mjs push-episode (SHA-256 0-diff) after verifying 0 unresolved maybe credits. Spends 0 credits.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: true },
    inputSchema: {
      type: "object",
      required: ["slug", "drivePath"],
      properties: {
        slug: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
        drivePath: { type: "string", description: "Relative Drive destination under the series folder (e.g. '物理化學與日常材料/G790/製作檔/sothatswhy-g790-dehumidifier-winter')." },
        dryRun: { type: "boolean" },
        force: { type: "boolean", description: "Allow push even if unresolved maybe credits exist (default: false)." },
      },
      additionalProperties: false,
    },
  },
]);

export function createToolDispatcher(orchestrator) {
  const handlers = {
    flow_status: (args) => orchestrator.flowStatus(args),
    flow_profiles: (args) => orchestrator.flowProfiles(args),
    flow_init_episode: (args) => orchestrator.flowInitEpisode(args),
    flow_register_character: (args) => orchestrator.flowRegisterCharacter(args),
    flow_import_video_json: (args) => orchestrator.flowImportVideoJson(args),
    flow_preflight_shotlist: (args) => orchestrator.flowPreflightShotlist(args),
    flow_generate_stills: (args) => orchestrator.flowGenerateStills(args),
    flow_approve_stills: (args) => orchestrator.flowApproveStills(args),
    flow_plan_clips: (args) => orchestrator.flowPlanClips(args),
    flow_generate_clips: (args) => orchestrator.flowGenerateClips(args),
    flow_select_take: (args) => orchestrator.flowSelectTake(args),
    flow_plan_extend: (args) => orchestrator.flowPlanExtend(args),
    flow_upscale_still: (args) => orchestrator.flowUpscaleStill(args),
    flow_extend_clip: (args) => orchestrator.flowExtendClip(args),
    flow_reconcile: (args) => orchestrator.flowReconcile(args),
    flow_wait: (args) => orchestrator.flowWait(args),
    flow_cancel: (args) => orchestrator.flowCancel(args),
    flow_episode_ledger: (args) => orchestrator.flowEpisodeLedger(args),
    flow_list_files: (args) => orchestrator.flowListFiles(args),
    flow_write_file: (args) => orchestrator.flowWriteFile(args),
    flow_read_file: (args) => orchestrator.flowReadFile(args),
    flow_push_drive: (args) => orchestrator.flowPushDrive(args),
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
            "Mokaair Google Flow MCP v2 (explainers + AI dramas + vertical Shorts). Workflow: flow_status/flow_profiles -> flow_init_episode -> flow_register_character or flow_import_video_json -> flow_preflight_shotlist -> flow_generate_stills (0 credits, pilot first for AI dramas) -> flow_approve_stills -> flow_plan_clips -> owner confirmation -> flow_generate_clips(confirm_token) -> flow_select_take / flow_reconcile -> flow_episode_ledger.",
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
