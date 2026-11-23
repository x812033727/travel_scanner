import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../../speech/forward";

// The video worker reads every video and its Drive copy by series for the daily index sheets it
// writes into Drive's _總表/ (tools/video/automation/drive-index.mjs). Like config, it needs the
// video tool token; the speech forwarder keeps cookies out.
export async function GET(request: NextRequest) {
  return forwardToSpeech(request, "automation/backup/index", "GET");
}
