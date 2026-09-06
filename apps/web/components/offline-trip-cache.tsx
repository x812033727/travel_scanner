"use client";

import { useEffect } from "react";
import { api } from "@/lib/api";

/**
 * Registers the worker that keeps the trip on screen readable without a signal.
 *
 * The worker is told which member is signed in, because a trip payload carries hotel
 * addresses and private notes and a shared phone must not mix two people's trips. It
 * caches nothing until that message arrives, and signing out deletes what it has (see
 * the sign-out path in `header-session.tsx`).
 */
export function OfflineTripCache() {
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
        worker.postMessage({ type: "signed-in", member: member.id });
      } catch {
        // No worker, no session, or no network: the page works exactly as before.
      }
    })();
    return () => { cancelled = true; };
  }, []);

  return null;
}
