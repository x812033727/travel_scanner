"use client";

import { useEffect, useRef } from "react";

type LeaveRequest = (proceed: () => void) => boolean;
const guards: Array<{ request: LeaveRequest }> = [];
const marker = "mokaairNavigationGuard";

/** Programmatic navigation must defer all related writes until the owner allows leaving. */
export function requestNavigation(proceed: () => void): boolean {
  const guard = guards.at(-1);
  if (guard) return guard.request(() => requestNavigation(proceed));
  proceed(); return true;
}

/** Protect route-local drafts without replacing Next's history state or dropping query strings. */
export function useNavigationGuard(enabled: boolean, requestLeave: LeaveRequest) {
  const requestRef = useRef(requestLeave);
  useEffect(() => { requestRef.current = requestLeave; });
  useEffect(() => {
    if (!enabled) return;
    const token = crypto.randomUUID();
    const url = window.location.href;
    const original = window.history.state;
    let armed = true;
    let inserted = false;
    let bypassClick = false;
    const guardState = { ...original, [marker]: token };
    // Do not enqueue a history traversal during Strict Mode's setup/cleanup probe.
    const insertTimer = window.setTimeout(() => { if (armed) { window.history.pushState(guardState, "", url); inserted = true; } }, 0);

    const removeGuard = () => { const index = guards.indexOf(guard); if (index >= 0) guards.splice(index, 1); };
    const leave = (proceed: () => void) => {
      if (!armed) return;
      armed = false; removeGuard();
      // Consume only our same-URL entry. Waiting for its pop avoids a phantom extra Back.
      if (window.history.state?.[marker] === token && window.location.href === url) {
        const resume = () => {
          // Child drawers copy Next state, including our marker. Consume their entries first.
          if (window.history.state?.[marker] === token) { window.history.back(); return; }
          window.removeEventListener("popstate", resume); proceed();
        };
        window.addEventListener("popstate", resume);
        window.history.back();
      } else proceed();
    };
    const guard = { request: (proceed: () => void) => requestRef.current(() => leave(proceed)) };
    guards.push(guard);
    const onPop = (event: PopStateEvent) => {
      if (!armed || !inserted || guards.at(-1) !== guard || window.history.state?.[marker] === token) return;
      // A route-owned child may have consumed its own entry. Only our base entry is guarded.
      // Capture before Next handles popstate, including a history-menu jump past our sentinel.
      // Restoring our URL keeps the current component and its draft mounted during confirmation.
      event.stopImmediatePropagation();
      const destinationUrl = window.location.href;
      window.history.pushState(guardState, "", url);
      // Consuming the restored guard already reaches a different-URL destination.
      // Only the same-URL base entry needs another Back to leave the editor.
      guard.request(() => { if (destinationUrl === url) window.history.back(); });
    };
    const onClick = (event: MouseEvent) => {
      if (!armed || bypassClick || guards.at(-1) !== guard || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      const anchor = event.target instanceof Element ? event.target.closest<HTMLAnchorElement>("a[href]") : null;
      if (!anchor || anchor.hasAttribute("download") || (anchor.target && anchor.target !== "_self")) return;
      const destination = new URL(anchor.href, window.location.href);
      if (!['http:', 'https:'].includes(destination.protocol) || destination.href === window.location.href) return;
      if (destination.pathname === window.location.pathname && destination.search === window.location.search && destination.hash) return;
      event.preventDefault(); event.stopPropagation();
      requestNavigation(() => { bypassClick = true; anchor.click(); bypassClick = false; });
    };
    const onUnload = (event: BeforeUnloadEvent) => { if (armed) { event.preventDefault(); event.returnValue = ""; } };
    window.addEventListener("popstate", onPop, true);
    document.addEventListener("click", onClick, true);
    window.addEventListener("beforeunload", onUnload);
    return () => {
      removeGuard();
      window.clearTimeout(insertTimer);
      window.removeEventListener("popstate", onPop, true);
      document.removeEventListener("click", onClick, true);
      window.removeEventListener("beforeunload", onUnload);
      if (armed && inserted && window.location.href === url && window.history.state?.[marker] === token) window.history.back();
      armed = false;
    };
  }, [enabled]);
}
