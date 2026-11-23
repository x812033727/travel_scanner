import { NextRequest } from "next/server";
import { forwardToSpeech, problem } from "../../../speech/forward";

// Lease one Colab account to an agent (`auto`: the free one with the most compute units), or
// renew the lease it holds. The API keeps the lease in Redis and refuses a taken account.
type Context = { params: Promise<{ slot: string }> };
const LEASE_SLOT = /^([a-e]|auto)$/;

export async function POST(request: NextRequest, context: Context) {
  const { slot } = await context.params;
  if (!LEASE_SLOT.test(slot)) return problem(422, "colab_slot_invalid", "帳號只能是 a–e 或 auto");
  return forwardToSpeech(request, `colab-accounts/${slot}/lease`, "POST", 4 * 1024);
}
