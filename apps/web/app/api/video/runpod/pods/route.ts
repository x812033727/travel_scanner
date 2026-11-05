import { NextRequest } from "next/server";
import { forwardToSpeech, type LostAnswer } from "../../speech/forward";

// A runner (skill minimax-h3-runpod) asks the site to start a RunPod GPU pod, or lists its own
// pods still running. Only a video tool token is forwarded, never cookies; the API answers only
// a token marked for RunPod, and the RunPod key never leaves the API.

// A start whose answer is lost may still have started a pod that is billing: the runner lists
// its pods (GET here) before it asks again, and the reaper stops what nobody beats for.
const START_LOST: LostAnswer = {
  status: 504,
  code: "runpod_answer_lost",
  detail: "請求已送到 API，回覆沒有回來；pod 可能已經開了，先查 GET /api/video/runpod/pods 再決定要不要重開",
};

export async function GET(request: NextRequest) {
  return forwardToSpeech(request, "runpod/pods", "GET");
}

export async function POST(request: NextRequest) {
  return forwardToSpeech(request, "runpod/pods", "POST", undefined, undefined, START_LOST);
}
