import { NextRequest } from "next/server";
import { forwardToSpeech, problem } from "../../../../speech/forward";

// Give a leased Colab account back; only the agent that holds it can.
type Context = { params: Promise<{ slot: string }> };
const SLOT = /^[a-e]$/;

export async function POST(request: NextRequest, context: Context) {
  const { slot } = await context.params;
  if (!SLOT.test(slot)) return problem(422, "colab_slot_invalid", "帳號只能是 a–e");
  return forwardToSpeech(request, `colab-accounts/${slot}/lease/release`, "POST", 4 * 1024);
}
