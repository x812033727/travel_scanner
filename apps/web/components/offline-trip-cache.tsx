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
 * On a first visit the worker activates while this page is already running and claims it
 * a moment later. A request sent before that moment never reaches the worker, so it is
 * never stored either.
 */
function controlled() {
  const container = navigator.serviceWorker;
  if (container.controller) return Promise.resolve();
  return new Promise<void>((resolve) => {
    container.addEventListener("controllerchange", () => resolve(), { once: true });
    window.setTimeout(resolve, 3_000);
  });
}

/**
 * Registers the worker that keeps the day view readable without a signal, including a
 * cold open after the phone has closed the tab (see `public/sw.js`).
 *
 * The worker is told which member is signed in, because a trip payload carries hotel
 * addresses and private notes and a shared phone must not mix two people's trips. It
 * caches nothing until that message arrives, and signing out deletes what it has (see
 * the sign-out path in `header-session.tsx`).
 *
 * After that message has landed, two things are stored:
 *
 * - The trip, fetched once more from here. TodayView asks for it the moment it mounts —
 *   before the worker is registered, let alone told who is signed in — and the worker's
 *   `cacheName` is module state that resets every time the browser restarts it, so
 *   TodayView's own request is usually not stored.
 * - This page and the scripts and styles it needs (`keep-day`), which the worker fetches
 *   itself. Without them the browser has nothing to draw on a cold open, and the stored
 *   trip is never read.
 *
 * That is two extra requests per visit to the day view, and none anywhere else.
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
        await controlled();
        if (cancelled) return;
        await api(`/trips/${tripId}`).catch(() => undefined);
        if (cancelled) return;
        worker.postMessage({ type: "keep-day", url: window.location.href });
      } catch {
        // No worker, no session, or no network: the page works exactly as before.
      }
    })();
    return () => { cancelled = true; };
  }, [tripId]);

  return null;
}
