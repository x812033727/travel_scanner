import { NextRequest } from "next/server";
import { forwardToSpeech, problem } from "../../speech/forward";

const MCP_MAX_BODY_BYTES = 1024 * 1024;
const MCP_SERVICES = new Set(["flow", "flow-music"]);

/**
 * Paired cloud sessions (Claude, Codex, Antigravity, Colab) reach the host Flow & Flow Music
 * MCP gateway through here with their `Bearer mkv_...` video tool token (`flow_access = true`).
 * Only the video tool token is forwarded, never browser cookies, and nothing caches the answer.
 */
export async function GET(
  request: NextRequest,
  context: { params: Promise<{ service: string }> },
) {
  const { service } = await context.params;
  if (service !== "health") {
    return problem(404, "flow_mcp_service_unknown", "僅支援 GET /api/video/mcp/health");
  }
  return forwardToSpeech(request, "mcp/health", "GET");
}

export async function POST(
  request: NextRequest,
  context: { params: Promise<{ service: string }> },
) {
  const { service } = await context.params;
  if (!MCP_SERVICES.has(service)) {
    return problem(404, "flow_mcp_service_unknown", "不支援的 MCP 服務名稱，僅接受 flow 或 flow-music");
  }
  return forwardToSpeech(request, `mcp/${service}`, "POST", MCP_MAX_BODY_BYTES);
}
