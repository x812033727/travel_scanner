"use client";

import { Download } from "lucide-react";
import { useTranslations } from "next-intl";
import { useId, useState } from "react";

// The 9:16 preview of a Short (docs/videos/SHORTS.md, the section on one Short's page), and the
// list of the raw evidence an experiment was written from. The player never crops: the frame is
// as tall as four fifths of the window at most and keeps its proportions. A switch lays over it
// what the Shorts interface covers, against the safe area the build measures
// (tools/video/shorts/build.mjs): content between x 78 and 902 and above y 1380, the caption bar
// above y 1600, in a frame of 1080 by 1920.
//
// This file imports no page and no card, so both can import it.
export const FRAME = { width: 1080, height: 1920 } as const;
export const SAFE = { left: 78, right: 902, contentBottom: 1380, captionBottom: 1600 } as const;
const percent = (value: number, of: number) => `${Number(((value / of) * 100).toFixed(3))}%`;
/** The covered strips and the content's box, as CSS insets of the frame. */
export const OVERLAY = {
  buttons: { left: percent(SAFE.right, FRAME.width), top: "0%", right: "0%", bottom: "0%" },
  titles: { left: "0%", top: percent(SAFE.captionBottom, FRAME.height), right: "0%", bottom: "0%" },
  content: { left: percent(SAFE.left, FRAME.width), top: "0%", right: percent(FRAME.width - SAFE.right, FRAME.width), bottom: percent(FRAME.height - SAFE.contentBottom, FRAME.height) },
} as const;
// 22.5rem by 40rem at the most; 45vh wide is 80vh tall at nine to sixteen.
export const FRAME_CLASS = "relative mx-auto aspect-[9/16] w-full max-w-[min(22.5rem,45vh)] overflow-hidden rounded-xl bg-black";
const sizeOf = (bytes: number) => (bytes >= 1_000_000 ? `${(bytes / 1_000_000).toFixed(1)} MB` : `${Math.max(1, Math.round(bytes / 1000))} KB`);

export function ShortsPlayer({ src, poster }: { src: string; poster?: string }) {
  const t = useTranslations("admin.videoShorts");
  const [covered, setCovered] = useState(false);
  const help = useId();
  return <div className="grid gap-3">
    <p className="font-bold">{t("player.title")}</p>
    <div className={FRAME_CLASS} data-testid="shorts-frame">
      <video controls playsInline preload="metadata" src={src} poster={poster} aria-label={t("player.title")} className="h-full w-full object-contain" />
      {covered && <div aria-hidden className="pointer-events-none absolute inset-0" data-testid="shorts-cover">
        <span className="absolute bg-red-600/35" style={OVERLAY.buttons} />
        <span className="absolute bg-red-600/35" style={OVERLAY.titles} />
        <span className="absolute border-2 border-dashed border-white/80" style={OVERLAY.content} />
      </div>}
    </div>
    <label className="flex min-h-11 items-center gap-2 text-sm font-semibold"><input type="checkbox" checked={covered} aria-describedby={help} onChange={(event) => setCovered(event.target.checked)} />{t("player.cover")}</label>
    <p id={help} className="text-sm leading-6 text-[var(--muted)]">{t("player.coverHelp")}</p>
  </div>;
}

export type EvidenceFile = { role: string; sha256: string; size: number; content_type: string };

/** The files an experiment's claims rest on, each named by its hash so it can be checked. */
export function ShortsEvidence({ files, urlOf }: { files: EvidenceFile[]; urlOf: (file: EvidenceFile) => string | undefined }) {
  const t = useTranslations("admin.videoShorts");
  if (files.length === 0) return null;
  return <details className="rounded-2xl border border-[var(--line)] p-4" aria-label={t("evidence.title")}>
    <summary className="cursor-pointer font-bold">{t("evidence.title")} · {files.length}</summary>
    <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{t("evidence.help")}</p>
    <div className="mt-3 overflow-x-auto"><table className="w-full min-w-[40rem] text-left text-sm">
      <thead><tr className="text-xs text-[var(--muted)]">{(["file", "sha256", "size"] as const).map((column) => <th key={column} scope="col" className="py-1 pr-3 font-semibold">{t(`evidence.${column}`)}</th>)}<th scope="col" className="sr-only">{t("evidence.download")}</th></tr></thead>
      <tbody>{files.map((file) => <tr key={`${file.role}-${file.sha256}`} className="border-t border-[var(--line)]">
        <th scope="row" className="py-2 pr-3 font-mono text-xs font-semibold">{file.role.replace(/^evidence_/, "")}</th>
        <td className="break-all py-2 pr-3 font-mono text-xs">{file.sha256}</td>
        <td className="py-2 pr-3">{sizeOf(file.size)}</td>
        <td className="py-2"><a href={urlOf(file)} download className="inline-flex min-h-11 items-center gap-2 text-sm font-semibold text-[var(--teal)] underline"><Download aria-hidden size={16} />{t("evidence.download")}</a></td>
      </tr>)}</tbody>
    </table></div>
  </details>;
}
