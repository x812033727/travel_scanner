import { NextRequest } from "next/server";
import { forwardToSpeech, problem } from "../../../../speech/forward";
import { SESSION_ID } from "../../../ids";

// The runner stops its pod at the end of a batch (failed or not); the API terminates it on
// RunPod and settles what it cost. Stopping twice is harmless.
type Context = { params: Promise<{ id: string }> };

export async function POST(request: NextRequest, context: Context) {
  const { id } = await context.params;
  if (!SESSION_ID.test(id)) return problem(404, "runpod_session_not_found", "找不到這個 RunPod pod");
  return forwardToSpeech(request, `runpod/pods/${id.toLowerCase()}/stop`, "POST");
}
