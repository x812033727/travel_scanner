#!/usr/bin/env node
/**
 * Zero-dependency MCP JSON-RPC 2.0 stdio server (`mokaair-flow-music`)
 * exposing 17 high-cohesion tools for Google Flow Music (Lyria 3.5)
 * production, auditioning, FFmpeg slicing/cutting, `_sfx/` v2 export,
 * `_music/` staging, and Google Drive Route B sync.
 *
 * Supports both newline-delimited JSON-RPC and `Content-Length` framing.
 */

import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  MCP_SERVER_NAME,
  MCP_SERVER_VERSION,
  SERIES_PRESETS,
  SUPPORTED_DOWNLOAD_FORMATS,
  TRACK_KINDS,
} from "./config.mjs";
import { FlowMusicOrchestrator } from "./orchestrator.mjs";

const SUPPORTED_PROTOCOL_VERSIONS = ["2025-03-26", "2024-11-05"];
const SERIES_ENUM = Object.keys(SERIES_PRESETS);

export const MCP_TOOLS = Object.freeze([
  {
    name: "music_status",
    description:
      "Check Google Flow Music (www.flowmusic.app) Chrome session auth, account/handle, local Chrome/FFmpeg availability, and profile lock state.",
    annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: true },
    inputSchema: {
      type: "object",
      properties: {
        profile: { type: "string", description: "Isolated Chrome profile name (default: 'default')." },
        probeRemote: { type: "boolean", description: "Probe www.flowmusic.app session via Chrome CDP (default: true)." },
      },
      additionalProperties: false,
    },
  },
  {
    name: "music_profiles",
    description:
      "List all local isolated Flow Music Chrome profiles, verified accounts/handles, and lock status.",
    annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false },
    inputSchema: { type: "object", properties: {}, additionalProperties: false },
  },
  {
    name: "music_init_collection",
    description:
      "Initialize a Route B local music collection under work/music-library/<collection>/, or import an existing Drive folder (e.g. flow-music-20261117) for measurement, slicing, and auditioning.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["collection"],
      properties: {
        collection: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
        importFromDir: { type: "string", description: "Optional existing local/Drive folder to import manifest & audio files from." },
        copyImportedFiles: { type: "boolean", description: "Copy imported audio files into work/music-library/<collection>/ instead of referencing in place." },
      },
      additionalProperties: false,
    },
  },
  {
    name: "music_preflight_plan",
    description:
      "Validate a batch of Flow Music prompts against Mokaair mixing rules (no vocals/no big drops on narration beds, copyright IP check, cue/sfx trim reminders, duplicate naming check) and save music-plan.json.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["tracks"],
      properties: {
        collection: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
        allowVocals: { type: "boolean" },
        autoEnforceBedGuard: { type: "boolean" },
        tracks: {
          type: "array",
          items: {
            type: "object",
            required: ["prompt"],
            properties: {
              cue: { type: "string" },
              name: { type: "string" },
              title: { type: "string" },
              kind: { type: "string", enum: TRACK_KINDS },
              prompt: { type: "string" },
              takes: { type: "integer", minimum: 1, maximum: 4 },
              allowVocals: { type: "boolean" },
              purpose: { type: "string" },
            },
          },
        },
      },
      additionalProperties: false,
    },
  },
  {
    name: "music_generate",
    description:
      "Enqueue async Flow Music (Lyria 3.5) track generation via isolated Chrome CDP with automatic M4A/WAV download, -takeN collision protection, and FFmpeg loudness measurement. Poll with music_wait.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: true },
    inputSchema: {
      type: "object",
      required: ["collection"],
      properties: {
        collection: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
        tracks: { type: "array", items: { type: "object" } },
        format: { type: "string", enum: SUPPORTED_DOWNLOAD_FORMATS },
        profile: { type: "string" },
        downloadImmediately: { type: "boolean" },
        measureAfterDownload: { type: "boolean" },
        allowVocals: { type: "boolean" },
        waitMs: { type: "integer", minimum: 0, maximum: 55000 },
      },
      additionalProperties: false,
    },
  },
  {
    name: "music_list_remote",
    description:
      "List tracks stored in your signed-in Flow Music account via same-origin /__api/clips/user/<id>?public_only=false without exporting credentials.",
    annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: true },
    inputSchema: {
      type: "object",
      properties: {
        profile: { type: "string" },
        userId: { type: "string" },
        limit: { type: "integer", minimum: 1, maximum: 500 },
        filterTitle: { type: "string" },
      },
      additionalProperties: false,
    },
  },
  {
    name: "music_download",
    description:
      "Batch-download specific Flow Music clip IDs (m4a/mp3/wav) via same-origin Chrome fetch with automatic -takeN naming and FFmpeg loudness measurement. Poll with music_wait.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: true },
    inputSchema: {
      type: "object",
      required: ["collection", "clips"],
      properties: {
        collection: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
        format: { type: "string", enum: SUPPORTED_DOWNLOAD_FORMATS },
        profile: { type: "string" },
        measureAfterDownload: { type: "boolean" },
        waitMs: { type: "integer", minimum: 0, maximum: 55000 },
        clips: {
          type: "array",
          items: {
            type: "object",
            required: ["clipId"],
            properties: {
              clipId: { type: "string" },
              title: { type: "string" },
              cue: { type: "string" },
              kind: { type: "string", enum: TRACK_KINDS },
              format: { type: "string", enum: SUPPORTED_DOWNLOAD_FORMATS },
              sound_prompt: { type: "string" },
            },
          },
        },
      },
      additionalProperties: false,
    },
  },
  {
    name: "music_measure",
    description:
      "Run local FFmpeg full-decode duration, EBU R128 loudness (lufs_i, lufs_m, peak_dbtp), silence count, near-silent & clipping checks, and SHA-256 on tracks in a collection.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["collection"],
      properties: {
        collection: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
        files: { type: "array", items: { type: "string" } },
      },
      additionalProperties: false,
    },
  },
  {
    name: "music_detect_slices",
    description:
      "Run FFmpeg silencedetect on long Lyria 3.5 cues and multi-hit SFX tracks to propose exact start/end cut timestamps.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["collection"],
      properties: {
        collection: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
        files: { type: "array", items: { type: "string" } },
        kinds: { type: "array", items: { type: "string", enum: TRACK_KINDS } },
        noiseDb: { type: "number" },
        minSilenceSec: { type: "number" },
        minSliceSec: { type: "number" },
      },
      additionalProperties: false,
    },
  },
  {
    name: "music_cut",
    description:
      "Trim cues (*-cut.m4a) or split single-hit SFX clips with clean fade-in/out, re-measure EBU R128 loudness, and record cut timestamps in manifest.json.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["collection", "cuts"],
      properties: {
        collection: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
        format: { type: "string", enum: SUPPORTED_DOWNLOAD_FORMATS },
        cuts: {
          type: "array",
          items: {
            type: "object",
            required: ["file", "startSec", "endSec"],
            properties: {
              file: { type: "string" },
              outputName: { type: "string" },
              soundName: { type: "string" },
              kind: { type: "string", enum: TRACK_KINDS },
              startSec: { type: "number", minimum: 0 },
              endSec: { type: "number", minimum: 0.1 },
              fadeInSec: { type: "number", minimum: 0 },
              fadeOutSec: { type: "number", minimum: 0 },
              format: { type: "string", enum: SUPPORTED_DOWNLOAD_FORMATS },
            },
          },
        },
      },
      additionalProperties: false,
    },
  },
  {
    name: "music_qa_gallery",
    description:
      "Generate an interactive local HTML audition & sign-off gallery (qa-gallery.html) with playable audio players, LUFS/peak warnings, and a one-click music_approve JSON copy button.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["collection"],
      properties: {
        collection: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
        includeCuts: { type: "boolean" },
      },
      additionalProperties: false,
    },
  },
  {
    name: "music_approve",
    description:
      "Record owner audition decisions (approved/rejected + reasons such as '有人聲' or '有爆點') from qa-gallery.html into manifest.json.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["collection"],
      properties: {
        collection: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
        approved: { type: "array", items: { type: "string" } },
        rejected: { type: "array", items: { type: "string" } },
        reasons: { type: "object", additionalProperties: { type: "string" } },
      },
      additionalProperties: false,
    },
  },
  {
    name: "music_export_sfx_set",
    description:
      "Export approved single-hit SFX cuts into a validated v2 _sfx/<set>/manifest.json (stamp, whoosh, pop + extras) checked by Mokaair's sfxSetProblems() and optionally run `assemble sfx-measure`.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["collection", "soundMapping"],
      properties: {
        collection: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
        setName: { type: "string" },
        soundMapping: { type: "object", additionalProperties: { type: "string" } },
        workBase: { type: "string" },
        account: { type: "string" },
        runSfxMeasure: { type: "boolean" },
      },
      additionalProperties: false,
    },
  },
  {
    name: "music_stage_for_episode",
    description:
      "Stage an approved bed or cue track into <workBase>/_music/ with MUSIC_TRACK naming & SHA-256 verification and return the exact video.json `music` snippet.",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["collection", "file"],
      properties: {
        collection: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
        file: { type: "string" },
        targetFilename: { type: "string" },
        workBase: { type: "string" },
        allowUnapproved: { type: "boolean" },
        allowOverwrite: { type: "boolean" },
      },
      additionalProperties: false,
    },
  },
  {
    name: "music_push_drive",
    description:
      "Sync a local music collection to Google Drive (AI/備份/AI劇/<series>/_共用/製作檔/...) with SHA-256 0-diff verification under Route B (0 GitHub commits).",
    annotations: { readOnlyHint: false, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["collection"],
      properties: {
        collection: { type: "string" },
        series: { type: "string", enum: SERIES_ENUM },
        driveSubdir: { type: "string" },
        driveRoot: { type: "string" },
        dryRun: { type: "boolean" },
      },
      additionalProperties: false,
    },
  },
  {
    name: "music_wait",
    description: "Wait up to timeoutMs for a running music_generate or music_download job_id.",
    annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false },
    inputSchema: {
      type: "object",
      required: ["job_id"],
      properties: {
        job_id: { type: "string" },
        timeoutMs: { type: "integer", minimum: 0, maximum: 55000 },
      },
      additionalProperties: false,
    },
  },
  {
    name: "music_cancel",
    description: "Cancel a queued or running Flow Music job_id cleanly without deleting completed files.",
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
]);

export function createToolDispatcher(orchestrator) {
  const handlers = {
    music_status: (args) => orchestrator.musicStatus(args),
    music_profiles: (args) => orchestrator.musicProfiles(args),
    music_init_collection: (args) => orchestrator.musicInitCollection(args),
    music_preflight_plan: (args) => orchestrator.musicPreflightPlan(args),
    music_generate: (args) => orchestrator.musicGenerate(args),
    music_list_remote: (args) => orchestrator.musicListRemote(args),
    music_download: (args) => orchestrator.musicDownload(args),
    music_measure: (args) => orchestrator.musicMeasure(args),
    music_detect_slices: (args) => orchestrator.musicDetectSlices(args),
    music_cut: (args) => orchestrator.musicCut(args),
    music_qa_gallery: (args) => orchestrator.musicQaGallery(args),
    music_approve: (args) => orchestrator.musicApprove(args),
    music_export_sfx_set: (args) => orchestrator.musicExportSfxSet(args),
    music_stage_for_episode: (args) => orchestrator.musicStageForEpisode(args),
    music_push_drive: (args) => orchestrator.musicPushDrive(args),
    music_wait: (args) => orchestrator.musicWait(args),
    music_cancel: (args) => orchestrator.musicCancel(args),
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
      const payload = err?.toJSON
        ? { ok: false, error: err.toJSON() }
        : { ok: false, error: { message: err?.message || String(err) } };
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
          capabilities: { tools: { listChanged: false } },
          serverInfo: { name: MCP_SERVER_NAME, version: MCP_SERVER_VERSION },
          instructions:
            "Mokaair Google Flow Music MCP (www.flowmusic.app, Lyria 3.5). Workflow: music_status/music_profiles -> music_init_collection -> music_preflight_plan -> music_generate or music_list_remote + music_download -> music_measure -> music_detect_slices + music_cut -> music_qa_gallery -> owner audition -> music_approve -> music_export_sfx_set / music_stage_for_episode -> music_push_drive.",
        },
      };
    }
    case "ping":
      return { jsonrpc: "2.0", id, result: {} };
    case "tools/list":
      return { jsonrpc: "2.0", id, result: { tools: MCP_TOOLS } };
    case "tools/call": {
      const result = await dispatch(params?.name, params?.arguments || {});
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
  orchestrator = new FlowMusicOrchestrator(),
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
    } catch {
      send({ jsonrpc: "2.0", id: null, error: { code: -32700, message: "Parse error" } });
      return;
    }
    try {
      const response = await handleJsonRpcMessage(msg, { dispatch });
      if (response) send(response);
    } catch (err) {
      stderr.write(`[${MCP_SERVER_NAME}] Unhandled error: ${err?.stack || err}\n`);
      if (msg?.id !== undefined && msg?.id !== null) {
        send({ jsonrpc: "2.0", id: msg.id, error: { code: -32603, message: err?.message || "Internal error" } });
      }
    }
  };

  const drainBuffer = () => {
    while (buffer.length > 0) {
      const textStart = buffer.subarray(0, Math.min(32, buffer.length)).toString("utf8");
      if (/^Content-Length:/i.test(textStart)) {
        useContentLength = true;
        const headerEnd = buffer.indexOf("\r\n\r\n");
        if (headerEnd === -1) return;
        const headerText = buffer.subarray(0, headerEnd).toString("utf8");
        const lenMatch = headerText.match(/Content-Length:\s*(\d+)/i);
        if (!lenMatch) {
          buffer = buffer.subarray(headerEnd + 4);
          continue;
        }
        const contentLength = Number(lenMatch[1]);
        const bodyStart = headerEnd + 4;
        if (buffer.length < bodyStart + contentLength) return;
        const body = buffer.subarray(bodyStart, bodyStart + contentLength).toString("utf8");
        buffer = buffer.subarray(bodyStart + contentLength);
        void processMessage(body);
        continue;
      }

      const newlineIdx = buffer.indexOf("\n");
      if (newlineIdx === -1) return;
      const line = buffer.subarray(0, newlineIdx).toString("utf8").trim();
      buffer = buffer.subarray(newlineIdx + 1);
      if (line) void processMessage(line);
    }
  };

  stdin.on("data", (chunk) => {
    buffer = Buffer.concat([buffer, Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk, "utf8")]);
    drainBuffer();
  });
}

if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) {
  startStdioServer();
}
