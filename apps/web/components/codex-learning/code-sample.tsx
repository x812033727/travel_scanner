"use client";

import { useState, useSyncExternalStore } from "react";

const subscribe = () => () => {};

export function CodeSample({ language, code, copyLabel = "Copy", copiedLabel = "Copied", failedLabel = "Select and copy the code" }: {
  language: string; code: string; copyLabel?: string; copiedLabel?: string; failedLabel?: string;
}) {
  const [status, setStatus] = useState("");
  const interactive = useSyncExternalStore(subscribe, () => true, () => false);
  async function copy() {
    try { await navigator.clipboard.writeText(code); setStatus(copiedLabel); }
    catch { setStatus(failedLabel); }
  }
  return <figure className="min-w-0 overflow-hidden rounded-xl border border-[var(--line)]">
    <figcaption className="flex flex-wrap items-center justify-between gap-2 bg-[var(--paper)] px-4">
      <span className="font-mono text-xs">{language}</span>
      <button disabled={!interactive} type="button" onClick={copy} className="min-h-11 px-3 text-sm underline disabled:opacity-50">{copyLabel}</button>
      <span role="status" className="text-xs">{status}</span>
    </figcaption>
    <pre className="max-w-full overflow-x-auto p-4 text-sm leading-6" tabIndex={0}><code>{code}</code></pre>
  </figure>;
}
