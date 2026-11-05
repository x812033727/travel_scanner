import { NextRequest } from "next/server";
import { forwardToSpeech, problem } from "../../../../speech/forward";
import { SESSION_ID } from "../../../ids";

// The runner beats once a minute while its pod works; a pod without beats is stopped by the
// reaper after the admin's idle limit. A 409 answer means the pod was stopped meanwhile.
type Context = { params: Promise<{ id: string }> };

export async function POST(request: NextRequest, context: Context) {
  const { id } = await context.params;
  if (!SESSION_ID.test(id)) return problem(404, "runpod_session_not_found", "找不到這個 RunPod pod");
  return forwardToSpeech(request, `runpod/pods/${id.toLowerCase()}/heartbeat`, "POST");
}
