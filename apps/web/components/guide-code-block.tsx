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
  return <figure className="min-w-0 max-w-full overflow-hidden rounded-2xl border border-[var(--line)] bg-[var(--surface)] shadow-[var(--shadow-sm)]">
    <figcaption className="flex flex-wrap items-center justify-between gap-2 border-b border-[var(--line)] bg-[var(--surface-tint)] px-4 py-2 text-sm">
      <span className="font-medium text-[var(--ink)]">{block.label} <span className="font-mono text-[var(--muted)]">· {block.language}</span></span>
      <button type="button" disabled={!ready} onClick={() => void copy()} className="min-h-11 rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3.5 font-semibold text-[var(--ink)] transition-colors hover:border-[var(--teal)] hover:text-[var(--teal)] disabled:opacity-50">
        {labels.copy}
      </button>
    </figcaption>
    <pre tabIndex={0} aria-label={block.label} className="max-w-full overflow-x-auto bg-[var(--paper)]/55 p-4 text-sm leading-7 [overflow-wrap:normal] [tab-size:2]"><code>{block.code}</code></pre>
    {status !== "idle" ? <p role="status" className="border-t border-[var(--line)] px-4 py-2 text-sm text-[var(--teal-dark)]">{status === "copied" ? labels.copied : labels.copyFailed}</p> : null}
  </figure>;
}
