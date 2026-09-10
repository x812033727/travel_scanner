"use client";

import { useCallback, useEffect, useId, useRef, useState } from "react";
import { useLocale } from "next-intl";
import { api } from "@/lib/api";
import { safeExternalHref } from "@/lib/navigation";
import { mapIdentityCopy, mapIdentityStatus } from "@/lib/map-identity-copy";
import {
  availableMapLinks,
  type CatalogMapKind,
  type CatalogMapRow,
  type MapIdentityBatch,
  type MapIdentityCandidates,
} from "@/lib/map-identities";
import { useAdminActionGuard } from "./admin-action-guard";

const field =
  "mt-1 min-h-11 w-full min-w-0 rounded-xl border border-[var(--line)] bg-white px-3 py-2";
const button =
  "min-h-11 rounded-xl border border-[var(--line)] bg-white px-4 py-2 text-sm font-semibold disabled:opacity-40";
const endpoint = "/admin/map-identities";

/** Supplemental review only. No canonical edits, publication or batch approval. */
export function AdminMapIdentitiesPanel({
  initialKind = "hotspot",
  canManage = true,
}: {
  initialKind?: CatalogMapKind;
  canManage?: boolean;
}) {
  const copy = mapIdentityCopy(useLocale());
  const manage = useAdminActionGuard("content.manage");
  const allowed = canManage && manage.allowed;
  const headingId = useId();
  const [open, setOpen] = useState(false);
  const [kind, setKind] = useState<CatalogMapKind>(initialKind);
  const [city, setCity] = useState("");
  const [missing, setMissing] = useState("all");
  const [query, setQuery] = useState({
    kind: initialKind,
    city: "",
    missing: "all",
    offset: 0,
  });
  const [rows, setRows] = useState<CatalogMapRow[]>([]);
  const [total, setTotal] = useState(0);
  const [configured, setConfigured] = useState(true);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [batch, setBatch] = useState<MapIdentityBatch | null>(null);
  const [review, setReview] = useState<MapIdentityCandidates | null>(null);
  const [candidateId, setCandidateId] = useState("");
  const [checked, setChecked] = useState(false);
  const [note, setNote] = useState("");
  const [reviewLoading, setReviewLoading] = useState(false);
  const requestSequence = useRef(0);
  const reviewSequence = useRef(0);
  const reviewTrigger = useRef<HTMLButtonElement | null>(null);
  const reviewHeading = useRef<HTMLHeadingElement | null>(null);
  const batchKey = useRef<string | null>(null);
  const reviewKey = useRef<string | null>(null);

  const load = useCallback(async () => {
    const sequence = ++requestSequence.current;
    setBusy(true);
    setError("");
    try {
      const params = new URLSearchParams({
        kind: query.kind,
        limit: "50",
        offset: String(query.offset),
        missing_status: query.missing,
      });
      if (query.city.trim()) params.set("destination_id", query.city.trim());
      const result = await api<{
        items: CatalogMapRow[];
        total: number;
        capabilities?: { google_places_configured: boolean };
      }>(`${endpoint}?${params}`);
      if (sequence !== requestSequence.current) return;
      setRows(result.items);
      setTotal(result.total);
      setConfigured(result.capabilities?.google_places_configured !== false);
      setSelected(new Set());
    } catch (reason) {
      if (sequence === requestSequence.current)
        setError((reason as Error).message);
    } finally {
      if (sequence === requestSequence.current) setBusy(false);
    }
  }, [query]);

  useEffect(() => {
    if (!open) return;
    const timer = window.setTimeout(() => void load(), 0);
    return () => {
      window.clearTimeout(timer);
      requestSequence.current += 1;
    };
  }, [open, load]);

  useEffect(() => {
    if (
      !open ||
      !batch ||
      !["queued", "running", "started"].includes(batch.status)
    )
      return;
    let cancelled = false;
    const timer = window.setTimeout(async () => {
      try {
        const next = await api<MapIdentityBatch>(
          `${endpoint}/batches/${batch.id}`,
        );
        if (cancelled) return;
        setBatch(next);
        if (!["queued", "running", "started"].includes(next.status))
          void load();
      } catch (reason) {
        if (!cancelled) setError((reason as Error).message);
      }
    }, 2500);
    return () => {
      cancelled = true;
      window.clearTimeout(timer);
    };
  }, [open, batch, load]);

  useEffect(() => {
    if (review) reviewHeading.current?.focus();
  }, [review]);

  async function createBatch() {
    if (!selected.size || selected.size > 50 || !allowed) return;
    setBusy(true);
    setError("");
    batchKey.current ??= crypto.randomUUID();
    try {
      const result = await api<MapIdentityBatch>(`${endpoint}/batches`, {
        method: "POST",
        headers: { "Idempotency-Key": batchKey.current },
        body: JSON.stringify({
          targets: rows
            .filter((row) => selected.has(row.id))
            .map((row) => ({ kind: row.kind, id: row.id })),
        }),
      });
      setBatch(result);
      batchKey.current = null;
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setBusy(false);
    }
  }

  async function openReview(row: CatalogMapRow, trigger?: HTMLButtonElement) {
    // Candidate details perform a paid provider lookup, not just a local read.
    if (!allowed || !configured) return;
    if (trigger) reviewTrigger.current = trigger;
    const sequence = ++reviewSequence.current;
    setReviewLoading(true);
    setReview(null);
    setError("");
    setNotice("");
    setChecked(false);
    setNote("");
    setCandidateId("");
    reviewKey.current = null;
    try {
      const result = await api<MapIdentityCandidates>(
        `${endpoint}/${row.kind}/${row.id}/candidates`,
      );
      if (sequence !== reviewSequence.current) return;
      setReview(result);
    } catch (reason) {
      if (sequence === reviewSequence.current)
        setError((reason as Error).message);
    } finally {
      if (sequence === reviewSequence.current) setReviewLoading(false);
    }
  }

  async function submitReview(action: "confirm" | "reject") {
    if (
      !review ||
      !candidateId ||
      !note.trim() ||
      !allowed ||
      (action === "confirm" && !checked)
    )
      return;
    if (Date.parse(review.expires_at) <= Date.now()) {
      setError(copy.expired);
      return;
    }
    setBusy(true);
    setError("");
    reviewKey.current ??= crypto.randomUUID();
    try {
      const item = await api<CatalogMapRow>(
        `${endpoint}/${review.item.kind}/${review.item.id}/review`,
        {
          method: "POST",
          headers: { "Idempotency-Key": reviewKey.current },
          body: JSON.stringify({
            action,
            expected_revision: review.item.revision,
            expected_fingerprint: review.item.canonical_fingerprint,
            snapshot_id: review.snapshot_id,
            place_id: candidateId,
            note: note.trim(),
          }),
        },
      );
      setRows((current) =>
        current.map((row) =>
          row.id === item.id && row.kind === item.kind ? item : row,
        ),
      );
      setReview(null);
      setNotice(copy.success);
      reviewKey.current = null;
      reviewTrigger.current?.focus();
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setBusy(false);
    }
  }

  function closeReview() {
    reviewSequence.current += 1;
    setReview(null);
    setReviewLoading(false);
    reviewTrigger.current?.focus();
  }

  return (
    <details
      className="my-5 min-w-0 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4"
      onToggle={(event) => setOpen(event.currentTarget.open)}
    >
      <summary className="min-h-11 cursor-pointer py-3 font-semibold">
        {copy.title}
      </summary>
      {open && (
        <div className="min-w-0 space-y-4">
          <p className="max-w-3xl text-sm leading-6 text-[var(--muted)]">
            {copy.hint}
          </p>
          <form
            className="grid min-w-0 gap-3 md:grid-cols-4"
            onSubmit={(event) => {
              event.preventDefault();
              setQuery({ kind, city, missing, offset: 0 });
              batchKey.current = null;
            }}
          >
            <label className="min-w-0 text-sm font-semibold">
              {copy.kind}
              <select
                className={field}
                value={kind}
                onChange={(event) =>
                  setKind(event.target.value as CatalogMapKind)
                }
              >
                {(["hotspot", "merchant", "hotel"] as const).map((value) => (
                  <option key={value} value={value}>
                    {copy[value]}
                  </option>
                ))}
              </select>
            </label>
            <label className="min-w-0 text-sm font-semibold">
              {copy.city}
              <input
                className={field}
                value={city}
                placeholder={copy.allCities}
                maxLength={80}
                onChange={(event) => setCity(event.target.value)}
              />
            </label>
            <label className="min-w-0 text-sm font-semibold">
              {copy.missing}
              <select
                className={field}
                value={missing}
                onChange={(event) => setMissing(event.target.value)}
              >
                <option value="all">{copy.all}</option>
                <option value="missing">{copy.missingId}</option>
                <option value="pending">{copy.pending}</option>
                <option value="confirmed">{copy.confirmed}</option>
              </select>
            </label>
            <button
              type="submit"
              className={`${button} self-end`}
              disabled={busy}
            >
              {copy.filter}
            </button>
          </form>
          <div className="flex flex-wrap items-center gap-2">
            <button
              type="button"
              className={button}
              disabled={busy || !rows.length}
              onClick={() => {
                batchKey.current = null;
                setSelected(new Set(rows.slice(0, 50).map((row) => row.id)));
              }}
            >
              {copy.selectAll}
            </button>
            <button
              type="button"
              className={button}
              disabled={busy || !selected.size}
              onClick={() => {
                batchKey.current = null;
                setSelected(new Set());
              }}
            >
              {copy.clear}
            </button>
            <span className="text-sm">
              {selected.size} {copy.selected}
            </span>
            <button
              type="button"
              className={`${button} text-[var(--teal)]`}
              disabled={
                !allowed ||
                !configured ||
                busy ||
                !selected.size ||
                ["queued", "running", "started"].includes(batch?.status ?? "")
              }
              onClick={() => void createBatch()}
            >
              {copy.batch}
            </button>
          </div>
          {!configured && (
            <p role="status" className="text-sm text-[var(--muted)]">
              Google Places · {copy.unavailable}
            </p>
          )}
          {batch && (
            <div
              className="rounded-xl border border-[var(--line)] bg-white p-3"
              role="status"
            >
              <p className="text-sm font-semibold">
                {copy.progress} · {mapIdentityStatus(batch.status, copy)} ·{" "}
                {batch.processed}/{batch.total}
              </p>
              <progress
                aria-label={copy.progress}
                max={Math.max(1, batch.total)}
                value={batch.processed}
                className="mt-2 w-full accent-[var(--teal)]"
              />
              <button
                type="button"
                className={button}
                onClick={() =>
                  void api<MapIdentityBatch>(`${endpoint}/batches/${batch.id}`)
                    .then(setBatch)
                    .catch((reason: Error) => setError(reason.message))
                }
              >
                {copy.refresh}
              </button>
            </div>
          )}
          {error && (
            <p
              role="alert"
              className="break-words rounded-xl bg-red-50 p-3 text-sm text-red-800"
            >
              {error}
              <button
                type="button"
                className={`${button} ml-2`}
                onClick={() => void load()}
              >
                {copy.refresh}
              </button>
            </p>
          )}
          {notice && (
            <p
              role="status"
              className="rounded-xl bg-emerald-50 p-3 text-sm text-emerald-900"
            >
              {notice}
            </p>
          )}
          <div aria-busy={busy} className="grid min-w-0 gap-3">
            {!busy && !rows.length && (
              <p className="rounded-xl bg-white p-4 text-sm">{copy.empty}</p>
            )}
            {rows.map((row) => (
              <article
                key={`${row.kind}:${row.id}`}
                className="min-w-0 rounded-xl border border-[var(--line)] bg-white p-3"
              >
                <div className="flex min-w-0 flex-wrap items-center gap-3">
                  <label className="flex min-h-11 min-w-0 flex-1 items-center gap-3 font-semibold">
                    <input
                      type="checkbox"
                      disabled={
                        busy || (!selected.has(row.id) && selected.size >= 50)
                      }
                      checked={selected.has(row.id)}
                      aria-label={`${copy.select} ${row.name}`}
                      onChange={(event) => {
                        batchKey.current = null;
                        setSelected((current) => {
                          const next = new Set(current);
                          if (event.target.checked) next.add(row.id);
                          else next.delete(row.id);
                          return next;
                        });
                      }}
                    />
                    <span className="break-words">
                      {row.name}
                      <span className="ml-2 text-xs font-normal text-[var(--muted)]">
                        {row.destination_id} · {copy[row.kind]}
                      </span>
                    </span>
                  </label>
                  <button
                    type="button"
                    className={button}
                    disabled={!allowed || !configured || busy || reviewLoading}
                    onClick={(event) =>
                      void openReview(row, event.currentTarget)
                    }
                    aria-label={`${copy.review} ${row.name}`}
                  >
                    {copy.review}
                  </button>
                </div>
                <div className="mt-2 flex flex-wrap gap-2 text-xs">
                  {(["naver_maps", "google_places"] as const).map(
                    (provider) => {
                      const identity = row.map_identities?.[provider];
                      const url = safeExternalHref(identity?.map_url);
                      return (
                        <span
                          key={provider}
                          className="flex flex-wrap items-center gap-2 rounded-lg bg-[var(--paper)] px-3 py-2"
                        >
                          {provider === "naver_maps" ? "NAVER" : "Google"} ·{" "}
                          {mapIdentityStatus(identity?.status, copy)}
                          {identity?.verified_at && (
                            <time dateTime={identity.verified_at}>
                              {identity.verified_at.slice(0, 10)}
                            </time>
                          )}
                          {url && (
                            <a
                              href={url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex min-h-11 items-center underline"
                            >
                              {provider === "naver_maps"
                                ? "NAVER Maps"
                                : "Google Maps"}
                            </a>
                          )}
                        </span>
                      );
                    },
                  )}
                </div>
              </article>
            ))}
          </div>
          <div className="flex flex-wrap items-center justify-between gap-2 text-sm">
            <button
              type="button"
              className={button}
              disabled={busy || query.offset === 0}
              onClick={() =>
                setQuery((current) => ({
                  ...current,
                  offset: Math.max(0, current.offset - 50),
                }))
              }
            >
              {copy.previous}
            </button>
            <span>
              {total ? query.offset + 1 : 0}–
              {Math.min(query.offset + 50, total)} / {total}
            </span>
            <button
              type="button"
              className={button}
              disabled={busy || query.offset + 50 >= total}
              onClick={() =>
                setQuery((current) => ({
                  ...current,
                  offset: current.offset + 50,
                }))
              }
            >
              {copy.next}
            </button>
          </div>
          {reviewLoading && <p role="status">{copy.reviewing}</p>}
          {review && (
            <section
              className="min-w-0 rounded-2xl border border-amber-300 bg-amber-50 p-4"
              aria-labelledby={headingId}
              onKeyDown={(event) => {
                if (event.key === "Escape") closeReview();
              }}
            >
              <div className="flex flex-wrap items-center justify-between gap-2">
                <h3
                  ref={reviewHeading}
                  id={headingId}
                  tabIndex={-1}
                  className="font-bold outline-none"
                >
                  {copy.review}
                </h3>
                <button
                  type="button"
                  className={button}
                  onClick={closeReview}
                  disabled={busy}
                >
                  {copy.close}
                </button>
              </div>
              <div className="mt-3 rounded-xl bg-white p-3">
                <p className="text-xs font-semibold">{copy.canonical}</p>
                <p className="mt-1 font-semibold">{review.item.name}</p>
                <p className="break-words text-sm">
                  {review.item.local_name} · {review.item.destination_id}
                </p>
                <p className="break-words text-sm">{review.item.address}</p>
                <div className="flex flex-wrap gap-2">
                  {availableMapLinks(review.item.map_links).map((map) => (
                    <a
                      key={map.url}
                      href={safeExternalHref(map.url)}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex min-h-11 items-center text-sm underline"
                    >
                      {map.label}
                    </a>
                  ))}
                </div>
              </div>
              <p className="my-3 text-sm">{copy.compare}</p>
              <fieldset className="min-w-0 space-y-2" disabled={busy}>
                <legend className="mb-2 font-semibold">
                  {copy.candidates}
                </legend>
                {!review.candidates.length && (
                  <p className="text-sm">{copy.none}</p>
                )}
                {review.candidates.map((candidate) => (
                  <label
                    key={candidate.place_id}
                    className="flex min-w-0 cursor-pointer items-start gap-3 rounded-xl border border-[var(--line)] bg-white p-3"
                  >
                    <input
                      type="radio"
                      name="map-candidate"
                      className="mt-1"
                      value={candidate.place_id}
                      checked={candidateId === candidate.place_id}
                      onChange={() => {
                        setCandidateId(candidate.place_id);
                        setChecked(false);
                        reviewKey.current = null;
                      }}
                    />
                    <span className="min-w-0">
                      <strong className="block break-words">
                        {candidate.name}
                      </strong>
                      <span className="block break-words text-sm">
                        {candidate.address}
                      </span>
                      <span className="block text-xs">
                        {candidate.country_code}
                      </span>
                      {safeExternalHref(candidate.google_maps_url) && (
                        <a
                          href={safeExternalHref(candidate.google_maps_url)}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex min-h-11 items-center text-sm underline"
                        >
                          Google Maps
                        </a>
                      )}
                    </span>
                  </label>
                ))}
              </fieldset>
              {review.candidates.length > 0 && (
                <div className="mt-4 space-y-3">
                  <label className="flex min-h-11 items-start gap-3 text-sm">
                    <input
                      type="checkbox"
                      className="mt-1"
                      checked={checked}
                      disabled={busy}
                      onChange={(event) => setChecked(event.target.checked)}
                    />
                    {copy.checked}
                  </label>
                  <label className="block text-sm font-semibold">
                    {copy.note}
                    <textarea
                      className={`${field} min-h-24`}
                      value={note}
                      maxLength={500}
                      disabled={busy}
                      onChange={(event) => {
                        setNote(event.target.value);
                        reviewKey.current = null;
                      }}
                    />
                  </label>
                  <div className="flex flex-wrap gap-2">
                    <button
                      type="button"
                      className={`${button} text-[var(--teal)]`}
                      disabled={
                        !allowed ||
                        busy ||
                        !checked ||
                        !candidateId ||
                        !note.trim()
                      }
                      onClick={() => void submitReview("confirm")}
                    >
                      {copy.confirm}
                    </button>
                    <button
                      type="button"
                      className={button}
                      disabled={
                        !allowed || busy || !candidateId || !note.trim()
                      }
                      onClick={() => void submitReview("reject")}
                    >
                      {copy.reject}
                    </button>
                    <button
                      type="button"
                      className={button}
                      disabled={busy}
                      onClick={() => void openReview(review.item)}
                    >
                      {copy.refresh}
                    </button>
                  </div>
                </div>
              )}
            </section>
          )}
        </div>
      )}
    </details>
  );
}
