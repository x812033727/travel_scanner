"use client";

import { useEffect } from "react";
import { api } from "@/lib/api";

/** Tells the worker who is signed in and waits for it to say it has a cache name. */
function announce(worker: ServiceWorker, member: string) {
  return new Promise<void>((resolve) => {
    const channel = new MessageChannel();
    channel.port1.onmessage = () => resolve();
    // Never hang the priming fetch on a worker that predates the reply.
    window.setTimeout(resolve, 1_000);
    worker.postMessage({ type: "signed-in", member }, [channel.port2]);
  });
}

/**
 * Registers the worker that keeps the trip on screen readable without a signal.
 *
 * The worker is told which member is signed in, because a trip payload carries hotel
 * addresses and private notes and a shared phone must not mix two people's trips. It
 * caches nothing until that message arrives, and signing out deletes what it has (see
 * the sign-out path in `header-session.tsx`).
 *
 * It also fetches the trip once itself, after that message has landed. TodayView asks
 * for the trip the moment it mounts — before the worker is registered, let alone told
 * who is signed in — and the worker's fetch handler returns early while it has no
 * cache name. So the first online visit used to store nothing at all, and the worker's
 * `cacheName` is module state that resets every time the browser restarts it, which
 * made that true again and again. One extra GET here is what makes the page work on
 * the platform with no signal, which is the only reason it exists.
 */
export function OfflineTripCache({ tripId }: { tripId?: string }) {
  useEffect(() => {
    if (typeof navigator === "undefined" || !("serviceWorker" in navigator)) return;
    let cancelled = false;
    void (async () => {
      try {
        const registration = await navigator.serviceWorker.register("/sw.js");
        await navigator.serviceWorker.ready;
        const member = await api<{ id: string }>("/auth/me");
        const worker = registration.active || navigator.serviceWorker.controller;
        if (cancelled || !worker || !member?.id) return;
        await announce(worker, member.id);
        if (cancelled || !tripId) return;
        await api(`/trips/${tripId}`).catch(() => undefined);
      } catch {
        // No worker, no session, or no network: the page works exactly as before.
      }
    })();
    return () => { cancelled = true; };
  }, [tripId]);

  return null;
}
