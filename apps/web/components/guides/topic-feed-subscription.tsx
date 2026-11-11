"use client";

import { useId, useState } from "react";
import { TOPIC_FEED_SIZE, topicFeedCopy } from "@/lib/topic-feed";

export function TopicFeedSubscription({ locale, href }: { locale: string; href: string }) {
  const copy = topicFeedCopy(locale);
  const id = useId();
  const [status, setStatus] = useState<"copied" | "copyFailed" | null>(null);
  async function copyAddress() {
    try {
      if (!navigator.clipboard?.writeText) throw new Error("clipboard unavailable");
      await navigator.clipboard.writeText(href);
      setStatus("copied");
    } catch { setStatus("copyFailed"); }
  }
  return <details className="mt-6 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4" data-testid="topic-feed-subscription">
    <summary className="min-h-11 cursor-pointer content-center font-semibold">{copy.title}</summary>
    <div className="mt-3 space-y-3">
      <p className="max-w-2xl text-sm leading-6 text-[var(--muted)]">{copy.help}</p>
      <p className="max-w-2xl text-sm leading-6 text-[var(--muted)]">{copy.limit.replace("{limit}", String(TOPIC_FEED_SIZE))}</p>
      <div className="flex flex-wrap items-center gap-3">
        <a className="inline-flex min-h-11 items-center text-[var(--teal)] underline underline-offset-4" href={href} type="application/atom+xml">{copy.open}</a>
        <button type="button" className="min-h-11 rounded-lg border border-[var(--line)] px-4 text-sm" onClick={() => void copyAddress()}>{copy.copy}</button>
      </div>
      <label className="block text-sm" htmlFor={id}>{copy.url}</label>
      <input id={id} className="min-h-11 w-full min-w-0 rounded-lg border border-[var(--line)] bg-[var(--paper)] px-3 text-sm" value={href} readOnly onFocus={(event) => event.currentTarget.select()} />
      {status ? <p role="status" className="text-sm">{copy[status]}</p> : null}
    </div>
  </details>;
}
