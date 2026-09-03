export function preserveRequestId<T extends Response>(response: T, upstream: Response): T {
  const requestId = upstream.headers.get("x-request-id");
  if (requestId) response.headers.set("X-Request-ID", requestId);
  return response;
}
