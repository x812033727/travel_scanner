"use client";

import { useEffect, useState, useSyncExternalStore } from "react";
import {
  isSafeStay22Referrer, isStay22LmaId, isStay22ScriptOrigin, privacyBlocksStay22, STAY22_SCRIPT_ELEMENT_ID,
  STAY22_SCRIPT_URL,
} from "@/lib/stay22-script";
import { stay22ScriptCopy } from "@/lib/stay22-script-copy";

declare global {
  interface Window {
    Stay22?: { params?: Record<string, unknown>; [key: string]: unknown };
  }
}

const subscribeToDocumentReferrer = () => () => undefined;

/** Mount only in the isolated public document root, never in the private SPA root. */
export function Stay22Script({ enabled, lmaId, locale }: { enabled: boolean; lmaId: string | null; locale: string }) {
  const [failed, setFailed] = useState(false);
  const unsafeReferrer = useSyncExternalStore(subscribeToDocumentReferrer,
    () => enabled && isStay22LmaId(lmaId) && !isSafeStay22Referrer(document.referrer, window.location.origin),
    () => false);
  useEffect(() => {
    if (!enabled || !isStay22LmaId(lmaId) || !isStay22ScriptOrigin(window.location.origin)
      || window.location.search || window.location.hash || privacyBlocksStay22(navigator)
      || !isSafeStay22Referrer(document.referrer, window.location.origin)) return;
    if (document.getElementById(STAY22_SCRIPT_ELEMENT_ID)) return;
    window.Stay22 = window.Stay22 || {};
    window.Stay22.params = { ...window.Stay22.params, lmaID: lmaId };
    const script = document.createElement("script");
    script.id = STAY22_SCRIPT_ELEMENT_ID;
    script.src = STAY22_SCRIPT_URL;
    script.async = true;
    script.addEventListener("error", () => setFailed(true), { once: true });
    document.head.appendChild(script);
    // Unmounting a script cannot undo vendor handlers. The separate root layout
    // forces a new document when leaving this page; never pretend removal is cleanup.
  }, [enabled, lmaId]);
  return failed || unsafeReferrer ? <p role="status" className="mx-auto max-w-6xl px-5 py-3 text-sm text-[var(--muted)]">{stay22ScriptCopy(locale).scriptUnavailable}</p> : null;
}
