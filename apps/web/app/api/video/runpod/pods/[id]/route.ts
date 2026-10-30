import { NextRequest } from "next/server";
import { forwardToSpeech, problem } from "../../../speech/forward";
import { SESSION_ID } from "../../ids";

// One of the token's RunPod pods: its state and what it has cost so far.
type Context = { params: Promise<{ id: string }> };

export async function GET(request: NextRequest, context: Context) {
  const { id } = await context.params;
  if (!SESSION_ID.test(id)) return problem(404, "runpod_session_not_found", "找不到這個 RunPod pod");
  return forwardToSpeech(request, `runpod/pods/${id.toLowerCase()}`, "GET");
}
