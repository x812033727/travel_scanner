import { NextRequest } from "next/server";
import { SPEECH_LOST, TRANSCRIBE_MAX_BODY_BYTES, forwardToSpeech } from "../forward";

/**
 * When each character of a phrase is spoken (apps/api/app/video_speech/align_api.py): a clip as
 * base64 for the server's aligner, or a `speech` body an Azure voice synthesizes with its word
 * boundaries in one call. That second shape is paid, so a lost answer is SPEECH_LOST like the
 * speech route's; the clip shape carries a WAV, so the body cap is the transcription's.
 */
export async function POST(request: NextRequest) {
  return forwardToSpeech(request, "speech/align", "POST", TRANSCRIBE_MAX_BODY_BYTES, undefined, SPEECH_LOST);
}
