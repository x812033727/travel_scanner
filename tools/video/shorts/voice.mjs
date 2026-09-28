// An episode's Short read by the channel's own voice: the long video's `voice`, through the same
// narration server the long video used (tools/video/tts), one phrase per request so each phrase's
// measured length times its caption. The phrases go through the lexicon like the long video's
// lines, so a product name sounds the same in both.
import { readCredentials } from '../tts/credentials.mjs';
import { SpeechError, synthesize } from '../tts/client.mjs';
import { spokenParts, voiceFields } from '../tts/requests.mjs';
import { trimSilence } from '../tts/split.mjs';
import { encodeWav, parseWav, requireNarrationFormat } from '../tts/wav.mjs';

/** The request body for one phrase in the episode's voice. */
export function phraseBody(voice, text, lexicon) {
  return { ...voiceFields(voice), segments: [{ parts: spokenParts(text, lexicon), break_after_ms: 0 }] };
}

/**
 * One WAV per phrase, in narration order, as the build's external audio expects them (48 kHz
 * mono PCM). `options` are the tts client's: site, token, fetchImpl, sleep.
 */
export async function serverPhrases({ phrases, voice, lexicon, ...options }) {
  const wavs = [];
  let billable = 0;
  for (const text of phrases) {
    const result = await synthesize({ body: phraseBody(voice, text, lexicon), ...options });
    billable += result.billable;
    wavs.push(encodeWav(trimSilence(requireNarrationFormat(parseWav(result.wav)))));
  }
  return { wavs, billable };
}

/** The tts client's options from the video tool token, or the owner is told to log in. */
export function serverOptions({ env = process.env, home, fetchImpl = globalThis.fetch, sleep } = {}) {
  const credentials = readCredentials({ env, home });
  if (!credentials.token) throw new SpeechError('no video tool token yet: run `node tools/video/cli.mjs login` first', { who: 'owner' });
  return { site: credentials.site, token: credentials.token, fetchImpl, ...(sleep ? { sleep } : {}) };
}
