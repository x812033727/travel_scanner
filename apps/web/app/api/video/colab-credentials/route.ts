import { NextRequest } from "next/server";
import { forwardToSpeech } from "../speech/forward";

/**
 * A paired cloud session (skill minimax-h3-colab) fetches the Colab CLI token of an account the
 * owner signed in on /admin/ai-accounts. Only a video tool token is forwarded, never cookies,
 * and the API answers only a token marked for Colab; the body is a credential, so nothing
 * caches it (forwardToSpeech answers with Cache-Control: no-store).
 */
export async function GET(request: NextRequest) {
  const slot = request.nextUrl.searchParams.get("slot");
  const path = slot && /^[a-e]$|^default$/.test(slot) ? `colab-credentials?slot=${slot}` : "colab-credentials";
  return forwardToSpeech(request, path, "GET");
}
