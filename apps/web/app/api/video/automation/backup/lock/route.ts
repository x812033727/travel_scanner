import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../../speech/forward";

// The video worker reports the Drive folder its rclone remote is locked to (VIDEO_BACKUP_LOCK_PATH),
// or that the host has no backup remote, as it starts (docs/videos/BACKUP.md).
export async function POST(request: NextRequest) {
  return forwardToSpeech(request, "automation/backup/lock", "POST");
}
