import { NextRequest } from "next/server";
import { forwardToSpeech } from "../speech/forward";

/**
 * Several agents, one Colab account each (skill minimax-h3-colab, scripts/accounts.py): the
 * accounts the owner signed in on /admin/ai-accounts, their compute units and who leases each.
 * No credentials pass here; only a video tool token is forwarded, never cookies.
 */
export async function GET(request: NextRequest) {
  return forwardToSpeech(request, "colab-accounts", "GET");
}
