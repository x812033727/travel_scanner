export type RequestBodyRejection = "invalid_length" | "too_large";

export class RequestBodyError extends Error {
  constructor(readonly reason: RequestBodyRejection) {
    super(reason === "too_large" ? "request body too large" : "invalid content-length header");
    this.name = "RequestBodyError";
  }
}

/**
 * Buffer a request body without trusting `Content-Length`.
 *
 * The declared size is checked first, then the stream is counted chunk by chunk and cancelled as
 * soon as it exceeds `maxBytes`, so a chunked or mislabelled upload can never be read into memory
 * in full before the limit applies.
 */
export async function limitedRequestBody(
  request: Request,
  maxBytes: number,
): Promise<ArrayBuffer | undefined> {
  const declared = request.headers.get("content-length");
  if (declared !== null && declared.trim() !== "") {
    const length = Number(declared);
    if (!Number.isInteger(length) || length < 0) throw new RequestBodyError("invalid_length");
    if (length > maxBytes) throw new RequestBodyError("too_large");
  }
  if (!request.body) return undefined;
  const reader = request.body.getReader();
  const chunks: Uint8Array[] = [];
  let size = 0;
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      size += value.byteLength;
      if (size > maxBytes) {
        await reader.cancel();
        throw new RequestBodyError("too_large");
      }
      chunks.push(value);
    }
  } finally {
    reader.releaseLock();
  }
  const result = new Uint8Array(size);
  let offset = 0;
  for (const chunk of chunks) {
    result.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return result.buffer;
}
