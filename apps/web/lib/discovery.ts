"use client";

import { useEffect, useState, useSyncExternalStore } from "react";
import { api } from "@/lib/api";
import { useHeaderSession } from "@/components/header-session";

export const discoveryKinds = ["hotspot", "food", "merchant", "hotel", "article", "video", "post", "itinerary"] as const;
export type DiscoveryKind = typeof discoveryKinds[number];
export type DiscoveryVideo = { provider: "youtube"; video_id: string; source_url: string; status: "link_only" | "embeddable"; embed_url: string | null };
export type DiscoveryItem = {
  id: string; kind: DiscoveryKind; title: string; summary: string; locale: string; href: string;
  destination: { id: string; name: string; country_code?: string } | null;
  source: { label: string; url: string | null; kind: "editorial" | "official" | "community" };
  published_at: string | null; updated_at: string | null; thumbnail_url: string | null;
  author?: { display_name: string; handle?: string } | null;
  recommendation_reason?: string | null; video?: DiscoveryVideo | null;
  collection_ref?: { kind: "guide" | "hotel" | "hotspot" | "food" | "merchant" | "post"; id: string } | null;
  place_ref?: { kind: "hotspot" | "merchant" | "food"; id: string; selection_path?: string; merchant_id?: string } | null;
  content?: { text: string; format?: "plain"; media?: Array<{ id: string; alt: string; width: number; height: number }>; video_refs?: DiscoveryVideo[]; itinerary?: import("@/lib/community/types").PublicItinerary | null };
};
export type DiscoveryPage = { enabled: boolean; items: DiscoveryItem[]; next_cursor: string | null; query: string;
  filters: { kinds: string[]; destinations: Array<string | { id: string; name: string }>; topics: string[] } };
export type DiscoveryPreferences = { version: number; destinations: string[]; topics: string[]; include_saved: boolean; include_following: boolean };
export type DiscoveryQuery = { q?: string; type?: string; destination?: string; topic?: string; locale?: string; mode?: string };

export function discoveryQuery(value: DiscoveryQuery) {
  const params = new URLSearchParams();
  for (const key of ["q", "type", "destination", "topic", "locale", "mode"] as const) {
    const text = value[key]?.trim();
    if (text && !(key === "type" && text === "all")) params.set(key, text);
  }
  return params.toString();
}

const closed = { enabled: false, loading: true };
let status = closed;
let request: Promise<void> | undefined;
let checkedAt = 0;
const listeners = new Set<() => void>();
const onStatusFocus = () => { if (Date.now() - checkedAt > 15_000) void refreshStatus(); };
function refreshStatus() {
  if (request) return request;
  request = api<{ enabled: boolean }>("/discovery/status").then((result) => {
    status = { enabled: result.enabled === true, loading: false };
  }).catch(() => { status = { enabled: false, loading: false }; }).finally(() => {
    checkedAt = Date.now(); request = undefined; listeners.forEach((listener) => listener());
  });
  return request;
}
function subscribe(listener: () => void) {
  listeners.add(listener);
  if (listeners.size === 1) window.addEventListener("focus", onStatusFocus);
  if (!checkedAt || Date.now() - checkedAt > 30_000) void refreshStatus();
  return () => { listeners.delete(listener); if (!listeners.size) window.removeEventListener("focus", onStatusFocus); };
}
/** Public flag only. No personal state is cached across accounts or server requests. */
export function useDiscoveryStatus() {
  return useSyncExternalStore(subscribe, () => status, () => closed);
}

/** Abort and key responses by login identity as well as URL; never show stale private feeds. */
export function useDiscoveryResource<T>(path: string | null) {
  const { sessionIdentity } = useHeaderSession();
  const [attempt, setAttempt] = useState(0);
  const [result, setResult] = useState<{ path: string; identity: object | null; data?: T; error?: unknown }>();
  useEffect(() => {
    if (!path) return;
    const controller = new AbortController();
    api<T>(path, { signal: controller.signal }).then((data) => {
      if (!controller.signal.aborted) setResult({ path, identity: sessionIdentity, data });
    }).catch((error: unknown) => {
      if (!controller.signal.aborted) setResult({ path, identity: sessionIdentity, error });
    });
    return () => controller.abort();
  }, [path, sessionIdentity, attempt]);
  const current = result?.path === path && result.identity === sessionIdentity ? result : undefined;
  return { data: current?.data, error: current?.error, loading: Boolean(path && !current), reload: () => setAttempt((value) => value + 1) };
}

export function youtubeId(value: string): string | null {
  try {
    const url = new URL(value);
    if (url.protocol !== "https:" || url.username || url.password || url.port) return null;
    const host = url.hostname;
    const id = host === "youtu.be" ? url.pathname.slice(1) : ["www.youtube.com", "youtube.com", "m.youtube.com"].includes(host)
      ? url.pathname === "/watch" ? url.searchParams.get("v") : url.pathname.match(/^\/(?:shorts|embed)\/([^/]+)$/)?.[1] : null;
    return id && /^[A-Za-z0-9_-]{11}$/.test(id) ? id : null;
  } catch { return null; }
}
