import { NextRequest } from "next/server";
import { forwardToSpeech, problem } from "../speech/forward";

/**
 * A paired cloud session (skill minimax-h3-colab) fetches the Colab CLI token of an account the
 * owner signed in on /admin/ai-accounts. Only a video tool token is forwarded, never cookies,
 * and the API answers only a token marked for Colab; the body is a credential, so nothing
 * caches it (forwardToSpeech answers with Cache-Control: no-store).
 */
export async function GET(request: NextRequest) {
  const query = new URLSearchParams();
  const slot = request.nextUrl.searchParams.get("slot");
  if (slot && /^([a-e]|default)$/.test(slot)) query.set("slot", slot);
  // The agent's lease name (scripts/accounts.py): the API hands a leased account only to its holder.
  const holder = request.nextUrl.searchParams.get("holder");
  if (holder) {
    if (!/^[A-Za-z0-9][A-Za-z0-9._:@-]{0,79}$/.test(holder)) {
      return problem(422, "colab_holder_invalid", "holder 只能用英數字與 . _ : @ -，最多 80 字");
    }
    query.set("holder", holder);
  }
  const search = query.toString();
  return forwardToSpeech(request, search ? `colab-credentials?${search}` : "colab-credentials", "GET");
}
