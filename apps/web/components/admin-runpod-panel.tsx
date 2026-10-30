"use client";

import { Cpu, HardDrive, LoaderCircle, Play, Square, Trash2 } from "lucide-react";
import { useLocale } from "next-intl";
import { useCallback, useEffect, useMemo, useState } from "react";
import { ApiError, api } from "@/lib/api";
import { runpodCopy } from "@/lib/runpod-copy";

export type RunpodPod = {
  session_id: string;
  pod_id: string | null;
  label: string;
  slug: string | null;
  gpu: string;
  cloud_type: string;
  data_center_id: string | null;
  cost_per_hr: string | null;
  started_at: string;
  last_heartbeat_at: string | null;
  stopped_at: string | null;
  stop_reason: "manual" | "idle" | "max_hours" | "cap" | "gone" | "failed" | null;
  // Settled once stopped; while running, what it has cost so far.
  usd: string;
  token_prefix: string | null;
};

export type RunpodOverview = {
  running: RunpodPod[];
  recent: RunpodPod[];
  month_usd: string;
  monthly_usd_cap: number;
  configured: boolean;
};

export type RunpodVolume = {
  id: string;
  name: string | null;
  size_gb: number;
  data_center_id: string | null;
  stock: string | null;
  usable: boolean;
};

export type RunpodVolumes = {
  gpu: string;
  volumes: RunpodVolume[];
  new_volume_gb: number;
  new_volume_usd_per_month: string;
};

const ENDPOINT = "/admin/provider-settings/runpod/sessions";
const VOLUMES = "/admin/provider-settings/runpod/volumes";
// Running pods cost by the second; a minute is fresh enough to see one and stop it.
const REFRESH_MS = 60_000;

function usd(value: string | number) {
  return `US$${Number(value).toFixed(2)}`;
}

/**
 * What the RunPod broker is doing: pods running now (with a stop button), this month's spend
 * against the admin's cap, and the last stopped pods with why they stopped. The site starts and
 * stops pods for video tools; this is where the owner sees it and can stop one by hand.
 */
export function AdminRunpodPanel({ canManage }: { canManage: boolean }) {
  const locale = useLocale();
  // The RunPod words live outside admin.json (lib/runpod-copy.ts says why).
  const copy = runpodCopy(locale).panel;
  const dateTime = useMemo(() => new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeStyle: "short" }), [locale]);
  const [overview, setOverview] = useState<RunpodOverview | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [confirming, setConfirming] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [storage, setStorage] = useState<RunpodVolumes | null>(null);
  const [asking, setAsking] = useState<string | null>(null);

  const loadStorage = useCallback(async () => {
    try {
      // Reads stock per data centre, so it is loaded on demand and not on the minute refresh.
      setStorage(await api<RunpodVolumes>(VOLUMES));
    } catch (problem) {
      setError(problem instanceof ApiError ? problem.message : copy.loadFailed);
    }
  }, [copy]);

  const load = useCallback(async () => {
    try {
      const next = await api<RunpodOverview>(ENDPOINT);
      setOverview(next);
      setError(null);
      // A pod started here has no runner beating for it: the open panel does, so it is not reaped.
      if (canManage) {
        await Promise.all(next.running.filter((pod) => !pod.token_prefix).map((pod) => api<RunpodPod>(`${ENDPOINT}/${pod.session_id}/heartbeat`, { method: "POST" })));
      }
    } catch (problem) {
      setError(problem instanceof ApiError ? problem.message : copy.loadFailed);
    }
  }, [copy, canManage]);

  useEffect(() => {
    // Loaded after mount, like the token list: running pods are not part of the settings snapshot.
    const first = window.setTimeout(() => {
      void load();
      void loadStorage();
    }, 0);
    const timer = window.setInterval(() => void load(), REFRESH_MS);
    return () => {
      window.clearTimeout(first);
      window.clearInterval(timer);
    };
  }, [load, loadStorage]);

  async function act(run: () => Promise<unknown>) {
    setBusy(true);
    try {
      await run();
      setAsking(null);
      await Promise.all([load(), loadStorage()]);
    } catch (problem) {
      setError(problem instanceof ApiError ? problem.message : copy.actionFailed);
    } finally {
      setBusy(false);
    }
  }

  const confirmRow = (key: string, run: () => Promise<unknown>) => <div className="flex gap-2">
    <button type="button" disabled={busy} onClick={() => void act(run)} className="min-h-11 rounded-xl bg-red-700 px-3 text-sm font-semibold text-white disabled:opacity-50">{key === "start" ? copy.confirmStart : key === "create" ? copy.confirmCreate : copy.confirmDelete}</button>
    <button type="button" onClick={() => setAsking(null)} className="min-h-11 rounded-xl px-3 text-sm font-semibold">{copy.cancel}</button>
  </div>;

  async function stop(id: string) {
    setBusy(true);
    try {
      await api<RunpodPod>(`${ENDPOINT}/${id}/stop`, { method: "POST" });
      setConfirming(null);
      await load();
    } catch (problem) {
      setError(problem instanceof ApiError ? problem.message : copy.stopFailed);
    } finally {
      setBusy(false);
    }
  }

  const spent = overview ? Number(overview.month_usd) : 0;
  const cap = overview?.monthly_usd_cap ?? 0;
  const share = cap > 0 ? Math.min(spent / cap, 1) : 1;

  return <section className="mt-6 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-5" aria-labelledby="runpod-panel-title" data-testid="runpod-panel">
    <h3 id="runpod-panel-title" className="flex items-center gap-2 text-base font-bold"><Cpu size={17} />{copy.title}</h3>
    <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{copy.intro}</p>
    {error && <p role="alert" className="mt-3 text-sm font-semibold text-red-700">{error}</p>}
    {!overview && !error && <p className="mt-3 flex items-center gap-2 text-sm text-[var(--muted)]"><LoaderCircle size={15} className="animate-spin" />{copy.loading}</p>}
    {overview && <>
      {!overview.configured && <p className="mt-3 rounded-lg bg-amber-50 px-3 py-2 text-xs font-semibold leading-5 text-amber-900">{copy.notConfigured}</p>}
      <div className="mt-4">
        <p className="text-sm font-semibold">{copy.month.replace("{spent}", usd(spent)).replace("{cap}", usd(cap))}</p>
        <div className="mt-2 h-2 w-full overflow-hidden rounded-full bg-gray-100" role="meter" aria-valuemin={0} aria-valuemax={cap} aria-valuenow={spent} aria-label={copy.monthLabel}>
          <div className={`h-full ${share >= 1 ? "bg-red-600" : share >= 0.8 ? "bg-amber-500" : "bg-[var(--teal)]"}`} style={{ width: `${share * 100}%` }} />
        </div>
      </div>

      {storage?.volumes && <div data-testid="runpod-volumes">
        <h4 className="mt-5 flex items-center gap-2 text-sm font-bold"><HardDrive size={15} />{copy.storage}</h4>
        {storage.volumes.length === 0 && <p className="mt-2 text-sm text-[var(--muted)]">{copy.noVolume}</p>}
        {storage.volumes.length > 0 && <ul className="mt-2 divide-y divide-[var(--line)] rounded-xl border border-[var(--line)] bg-white">
          {storage.volumes.map((volume) => <li key={volume.id} className="flex flex-wrap items-center justify-between gap-3 px-4 py-3 text-sm">
            <div className="min-w-0">
              <p className="font-semibold">{volume.name ?? volume.id}</p>
              <p className="mt-0.5 text-xs text-[var(--muted)]"><code>{volume.id}</code> · {volume.size_gb} GB · {volume.data_center_id ?? "—"} · {copy.stockLabel} {volume.stock ?? copy.noStock}{!volume.usable && <> · {copy.tooSmall}</>}</p>
            </div>
            {canManage && (asking === `delete:${volume.id}`
              ? confirmRow("delete", () => api<void>(`${VOLUMES}/${volume.id}`, { method: "DELETE" }))
              : <button type="button" onClick={() => setAsking(`delete:${volume.id}`)} className="flex min-h-11 items-center gap-2 rounded-xl border border-red-200 px-3 text-sm font-semibold text-red-700"><Trash2 size={15} />{copy.deleteVolume}</button>)}
          </li>)}
        </ul>}
      </div>}

      {canManage && storage?.volumes && <div className="mt-3 flex flex-wrap items-center gap-2">
        {asking === "start"
          ? <>{<p className="w-full text-xs text-[var(--muted)]">{copy.startNote}</p>}{confirmRow("start", () => api(ENDPOINT, { method: "POST", body: JSON.stringify({}) }))}</>
          : <button type="button" disabled={overview.running.length > 0 || !overview.configured} onClick={() => setAsking("start")} className="flex min-h-11 items-center gap-2 rounded-xl bg-[var(--teal)] px-3 text-sm font-semibold text-white disabled:opacity-50"><Play size={15} />{copy.startPod}</button>}
        {storage.volumes.every((volume) => !volume.usable) && (asking === "create"
          ? <>{<p className="w-full text-xs text-[var(--muted)]">{copy.createNote.replace("{gb}", String(storage.new_volume_gb)).replace("{usd}", usd(storage.new_volume_usd_per_month))}</p>}{confirmRow("create", () => api(VOLUMES, { method: "POST", body: JSON.stringify({}) }))}</>
          : <button type="button" onClick={() => setAsking("create")} className="flex min-h-11 items-center gap-2 rounded-xl border border-[var(--line)] px-3 text-sm font-semibold"><HardDrive size={15} />{copy.createVolume}</button>)}
      </div>}

      <h4 className="mt-5 text-sm font-bold">{copy.running}</h4>
      {overview.running.length === 0 && <p className="mt-2 text-sm text-[var(--muted)]">{copy.noneRunning}</p>}
      {overview.running.length > 0 && <ul className="mt-2 divide-y divide-[var(--line)] rounded-xl border border-[var(--line)] bg-white">
        {overview.running.map((pod) => <li key={pod.session_id} className="flex flex-wrap items-center justify-between gap-3 px-4 py-3 text-sm" data-testid="runpod-running">
          <div className="min-w-0">
            <p className="font-semibold">{pod.label}{pod.slug && <span className="ml-2 text-xs font-normal text-[var(--muted)]">{pod.slug}</span>}</p>
            <p className="mt-0.5 text-xs text-[var(--muted)]">{pod.gpu} · {pod.cloud_type} · {pod.data_center_id ?? "—"} · {pod.cost_per_hr ? `${usd(pod.cost_per_hr)}/h` : copy.pricePending} · {copy.startedAt} {dateTime.format(new Date(pod.started_at))} · {copy.lastBeat} {pod.last_heartbeat_at ? dateTime.format(new Date(pod.last_heartbeat_at)) : copy.never} · {copy.soFar} {usd(pod.usd)}{pod.token_prefix && <> · <code>{pod.token_prefix}…</code></>}</p>
          </div>
          {canManage && (confirming === pod.session_id
            ? <div className="flex gap-2"><button type="button" disabled={busy} onClick={() => void stop(pod.session_id)} className="min-h-11 rounded-xl bg-red-700 px-3 text-sm font-semibold text-white disabled:opacity-50">{copy.confirmStop}</button><button type="button" onClick={() => setConfirming(null)} className="min-h-11 rounded-xl px-3 text-sm font-semibold">{copy.cancel}</button></div>
            : <button type="button" onClick={() => setConfirming(pod.session_id)} className="flex min-h-11 items-center gap-2 rounded-xl border border-red-200 px-3 text-sm font-semibold text-red-700"><Square size={15} />{copy.stop}</button>)}
        </li>)}
      </ul>}

      <h4 className="mt-5 text-sm font-bold">{copy.recent}</h4>
      {overview.recent.length === 0 && <p className="mt-2 text-sm text-[var(--muted)]">{copy.noneRecent}</p>}
      {overview.recent.length > 0 && <ul className="mt-2 divide-y divide-[var(--line)] rounded-xl border border-[var(--line)] bg-white">
        {overview.recent.map((pod) => <li key={pod.session_id} className="px-4 py-2 text-sm">
          <p><span className="font-semibold">{pod.label}</span> · {usd(pod.usd)} · {pod.stop_reason ? copy.reasons[pod.stop_reason] : ""}</p>
          <p className="text-xs text-[var(--muted)]">{dateTime.format(new Date(pod.started_at))} → {pod.stopped_at ? dateTime.format(new Date(pod.stopped_at)) : "—"} · {pod.gpu}</p>
        </li>)}
      </ul>}
    </>}
  </section>;
}
