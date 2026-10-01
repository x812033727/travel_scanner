"use client";

import { useTranslations } from "next-intl";
import { useEffect, useRef, useState } from "react";
import { control, type Project, type ReviewFile } from "@/components/admin-video-review-card";
import { Button } from "@/components/community/ui";
import { api, ApiError } from "@/lib/api";

type RenewalState = { version: string; final_review_id: string; final_sha256: string };
type Candidate = {
  schema_version: 1; kind: "long-final-renewal"; slug: string; site: string;
  source: { final_review_id: string; final_sha256: string; body_sha256: string };
  candidate: { final_sha256: string; branding_hash: string; final_bytes: number };
  review: { gate: "final"; content_sha256: string; summary: string; payload: Record<string, unknown>; files: ReviewFile[] };
};
const HASH = /^[a-f0-9]{64}$/;
const UUID = /^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$/i;
const record = (value: unknown): Record<string, unknown> => value !== null && typeof value === "object" && !Array.isArray(value) ? value as Record<string, unknown> : {};

/** A receipt only names content already staged by the tool; it cannot pick endpoints or credentials. */
export function renewalCandidate(value: unknown, slug: string, site: string): Candidate | null {
  const receipt = record(value), source = record(receipt.source), candidate = record(receipt.candidate), review = record(receipt.review), payload = record(review.payload);
  if (receipt.schema_version !== 1 || receipt.kind !== "long-final-renewal" || receipt.slug !== slug || receipt.site !== site
    || !UUID.test(String(source.final_review_id)) || !HASH.test(String(source.final_sha256)) || !HASH.test(String(source.body_sha256))
    || !HASH.test(String(candidate.branding_hash)) || !Number.isSafeInteger(candidate.final_bytes) || Number(candidate.final_bytes) <= 0
    || review.gate !== "final" || review.subject != null || !HASH.test(String(review.content_sha256)) || review.content_sha256 !== candidate.final_sha256
    || source.final_sha256 === candidate.final_sha256 || typeof review.summary !== "string" || !review.summary.trim() || [...review.summary].length > 500
    || payload._final_renewal !== undefined || payload.branding_hash !== candidate.branding_hash
    || !Array.isArray(review.files) || review.files.length > 48) return null;
  const files = review.files.map(record);
  if (files.some((file) => !/^[a-z][A-Za-z0-9_-]{0,39}$/.test(String(file.role)) || !HASH.test(String(file.sha256)) || !Number.isSafeInteger(file.size) || Number(file.size) <= 0)
    || new Set(files.map((file) => file.role)).size !== files.length
    || !files.some((file) => file.role === "preview" && file.content_type === "video/mp4")
    || !files.some((file) => file.role === "final" && file.content_type === "video/mp4" && file.sha256 === candidate.final_sha256 && file.size === candidate.final_bytes)) return null;
  return receipt as Candidate;
}

function readFile(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result));
    reader.onerror = () => reject(new Error("candidate_file_unreadable"));
    reader.readAsText(file);
  });
}

/** Selecting a receipt is local. Checking is read-only; the separate submit button creates a pending final. */
export function AdminVideoRenewal({ project, canManage, onSubmitted }: { project: Project; canManage: boolean; onSubmitted: () => void }) {
  const t = useTranslations("admin.videoRenewal");
  const [candidate, setCandidate] = useState<Candidate | null>(null);
  const [checked, setChecked] = useState<RenewalState | null>(null);
  const [reason, setReason] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [sent, setSent] = useState(false);
  const [uncertain, setUncertain] = useState(false);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const previewGeneration = useRef(0);
  useEffect(() => () => { previewGeneration.current++; }, []);
  useEffect(() => () => { if (previewUrl) URL.revokeObjectURL(previewUrl); }, [previewUrl]);
  const final = project.reviews.find((review) => review.gate === "final" && !review.subject);
  if (!canManage || project.shorts_line || project.format === "shorts" || project.dropped_at || project.youtube_video_id || project.youtube_sync || project.youtube_publish_at || project.youtube_removed_at
    || !final || (final.status !== "approved" && !final.payload._final_renewal)) return null;
  const endpoint = `/admin/videos/${project.slug}/final-renewal`;
  const explain = (problem: unknown) => {
    if (problem instanceof ApiError) {
      if (problem.code === "video_final_renewal_stale") return t("stale");
      if (problem.status === 409 || problem.status === 503) return t("conflict", { message: problem.message });
    }
    return t("failed");
  };
  const select = async (file: File | undefined) => {
    previewGeneration.current++;
    setCandidate(null); setChecked(null); setError(""); setSent(false); setPreviewUrl(null);
    if (!file) return;
    setBusy(true);
    try {
      if (file.size > 350_000) throw new Error("receipt_too_large");
      const value = renewalCandidate(JSON.parse(await readFile(file)), project.slug, window.location.origin);
      if (!value) throw new Error("invalid_receipt");
      setCandidate(value);
    } catch { setError(t("invalid")); }
    finally { setBusy(false); }
  };
  const matches = (state: RenewalState, receipt: Candidate) => HASH.test(state.version) && state.final_review_id === receipt.source.final_review_id && state.final_sha256 === receipt.source.final_sha256;
  const preview = async (file: File | undefined) => {
    const generation = ++previewGeneration.current;
    setPreviewUrl(null); setError("");
    if (!file || !candidate) return;
    setBusy(true);
    try {
      const proof = candidate.review.files.find((item) => item.role === "preview")!;
      if (file.size !== proof.size || file.size > 256 * 1024 * 1024) throw new Error("preview_size");
      const bytes = await new Promise<ArrayBuffer>((resolve, reject) => {
        const reader = new FileReader(); reader.onload = () => resolve(reader.result as ArrayBuffer); reader.onerror = reject; reader.readAsArrayBuffer(file);
      });
      const digest = await crypto.subtle.digest("SHA-256", bytes);
      const actual = Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join("");
      if (actual !== proof.sha256) throw new Error("preview_sha");
      if (generation !== previewGeneration.current) return;
      setPreviewUrl(URL.createObjectURL(file));
    } catch { if (generation === previewGeneration.current) setError(t("previewInvalid")); }
    finally { if (generation === previewGeneration.current) setBusy(false); }
  };
  const check = async () => {
    if (!candidate || busy) return;
    setBusy(true); setChecked(null); setError("");
    try {
      const state = await api<RenewalState>(endpoint);
      if (!matches(state, candidate)) { setError(t("stale")); return; }
      setChecked(state); setUncertain(false);
    } catch (problem) { setError(explain(problem)); }
    finally { setBusy(false); }
  };
  const submit = async () => {
    if (!candidate || !checked || !reason.trim() || busy || uncertain) return;
    setBusy(true); setError("");
    let wrote = false;
    try {
      const fresh = await api<RenewalState>(endpoint);
      if (!matches(fresh, candidate) || fresh.version !== checked.version) { setChecked(null); setError(t("stale")); return; }
      wrote = true;
      const result = await api<{ id: string; status: string; content_sha256: string; payload: Record<string, unknown> }>(endpoint, { method: "POST", body: JSON.stringify({
        expected_version: fresh.version, expected_final_review_id: fresh.final_review_id,
        expected_final_sha256: fresh.final_sha256, reason: reason.trim(), review: candidate.review,
      }) });
      if (result.status !== "pending" || result.content_sha256 !== candidate.review.content_sha256 || result.payload?.manual_review !== true) throw new Error("unexpected_renewal_result");
      const persisted = await api<Project>(`/admin/videos/${project.slug}`);
      if (!persisted.reviews.some((review) => review.id === result.id && review.content_sha256 === result.content_sha256 && review.status === "pending" && review.payload.manual_review === true)) throw new Error("renewal_not_persisted");
      setSent(true); setCandidate(null); setChecked(null); setPreviewUrl(null); onSubmitted();
    } catch (problem) {
      setChecked(null);
      if (wrote && !(problem instanceof ApiError && problem.status >= 400 && problem.status < 500)) { setUncertain(true); setError(t("uncertain")); }
      else setError(explain(problem));
    } finally { setBusy(false); }
  };
  return <section aria-label={t("title")} className="rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4">
    <h3 className="font-bold">{t("title")}</h3>
    <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{t("help")}</p>
    {final.payload._final_renewal && final.status === "pending" ? <p role="status" className="mt-2 text-sm">{t("pending")}</p> : null}
    {sent && <p role="status" className="mt-2 text-sm">{t("submitted")}</p>}
    <label className="mt-3 grid gap-2 text-sm font-semibold">{t("file")}
      <input type="file" accept="application/json,.json" disabled={busy} onChange={(event) => void select(event.target.files?.[0])} />
    </label>
    {candidate && <div className="mt-3 grid gap-3 text-sm">
      <p>{candidate.review.summary}</p>
      {typeof candidate.review.payload.duration_seconds === "number" && <p>{t("duration", { seconds: candidate.review.payload.duration_seconds.toFixed(1) })}</p>}
      <label className="grid gap-2 font-semibold">{t("previewFile")}<input type="file" accept="video/mp4,.mp4" disabled={busy} onChange={(event) => void preview(event.target.files?.[0])} /></label>
      {previewUrl && <video aria-label={t("previewPlayer")} src={previewUrl} controls preload="metadata" className="w-full rounded-xl" />}
      <details><summary className="cursor-pointer font-semibold">{t("proof")}</summary><dl className="mt-2 grid gap-1 break-all">
        <dt className="font-semibold">{t("original")}</dt><dd>{candidate.source.final_sha256}</dd>
        <dt className="font-semibold">{t("replacement")}</dt><dd>{candidate.candidate.final_sha256}</dd>
        <dt className="font-semibold">{t("branding")}</dt><dd>{candidate.candidate.branding_hash}</dd>
      </dl></details>
      <p>{t("attachments", { count: candidate.review.files.length })}</p>
      <label className="grid gap-2 font-semibold">{t("reason")}<textarea className={control} rows={2} maxLength={2000} value={reason} disabled={busy} onChange={(event) => setReason(event.target.value)} /></label>
      <div className="flex flex-wrap gap-3">
        <Button secondary disabled={busy} onClick={() => void check()}>{t("check")}</Button>
        <Button disabled={busy || !checked || !reason.trim() || uncertain} onClick={() => void submit()}>{busy ? t("busy") : t("submit")}</Button>
      </div>
      {checked && <p role="status">{t("checked")}</p>}
    </div>}
    {error && <p role="alert" className="mt-2 text-sm text-red-800">{error}</p>}
  </section>;
}
