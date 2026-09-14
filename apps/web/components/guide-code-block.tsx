"use client";

import { useState, useSyncExternalStore } from "react";
import type { CodeBlock } from "@/lib/content-blocks";

export type CodeLabels = { copy: string; copied: string; copyFailed: string };
const defaults: CodeLabels = { copy: "Copy", copied: "Copied", copyFailed: "Copy failed. Select the code and copy it manually." };
const subscribe = () => () => {};

export function GuideCodeBlock({ block, labels = defaults }: { block: CodeBlock; labels?: CodeLabels }) {
  const [status, setStatus] = useState<"idle" | "copied" | "failed">("idle");
  const ready = useSyncExternalStore(subscribe, () => true, () => false);
  async function copy() {
    try {
      await navigator.clipboard.writeText(block.code);
      setStatus("copied");
    } catch { setStatus("failed"); }
  }
  return <figure className="min-w-0 max-w-full overflow-hidden rounded-2xl border border-[var(--line)]">
    <figcaption className="flex flex-wrap items-center justify-between gap-2 bg-[var(--paper)] px-4 py-2 text-sm">
      <span>{block.label} <span className="text-[var(--muted)]">· {block.language}</span></span>
      <button type="button" disabled={!ready} onClick={() => void copy()} className="min-h-11 rounded-lg border border-[var(--line)] px-3 font-semibold disabled:opacity-50">
        {labels.copy}
      </button>
    </figcaption>
    <pre tabIndex={0} aria-label={block.label} className="max-w-full overflow-x-auto bg-[var(--surface)] p-4 text-sm leading-7 [overflow-wrap:normal] [tab-size:2]"><code>{block.code}</code></pre>
    {status !== "idle" ? <p role="status" className="px-4 pb-3 text-sm">{status === "copied" ? labels.copied : labels.copyFailed}</p> : null}
  </figure>;
}
