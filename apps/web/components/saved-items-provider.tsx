"use client";
import { createContext, useCallback, useContext, useEffect, useLayoutEffect, useMemo, useRef, useState, type ReactNode } from "react";
import { ApiError, api } from "@/lib/api";
import { useHeaderSession } from "@/components/header-session";
import { parseSavedKey, savedReference, type SavedState, type SavedType } from "@/lib/saved-items";
export type { SavedType } from "@/lib/saved-items";
type Status = "loading" | "authenticated" | "signed_out" | "unavailable";
type SavedContextValue = {
  status: Status; revision: number;
  isSaved: (type: SavedType, id: string) => boolean;
  state: (key: string) => SavedState | undefined;
  ensureStates: (keys: string[], force?: boolean) => Promise<void>;
  acceptStates: (states: SavedState[], changed?: boolean) => void;
  setSaved: (type: SavedType, id: string, saved: boolean) => Promise<void>;
  toggle: (type: SavedType, id: string) => Promise<boolean>;
};
const fallback: SavedContextValue = { status: "signed_out", revision: 0, isSaved: () => false, state: () => undefined, ensureStates: async () => undefined, acceptStates: () => undefined, setSaved: async () => undefined, toggle: async () => false };
const SavedContext = createContext<SavedContextValue>(fallback);
type Snapshot = { identity: object | null; status: Status; states: Map<string, SavedState>; revision: number };

/** Canonical saved state belongs to a login, never to browser storage or a previous account. */
export function SavedItemsProvider({ children, hasSession = true }: { children: ReactNode; hasSession?: boolean }) {
  const session = useHeaderSession();
  const identity = session.sessionIdentity;
  const [snapshot, setSnapshot] = useState<Snapshot>({ identity, status: hasSession ? "loading" : "signed_out", states: new Map(), revision: 0 });
  const controllers = useRef(new Set<AbortController>());
  const latest = useRef({ identity, userId: session.user?.id });
  const statesRef = useRef(snapshot.states);
  const generations = useRef(new Map<string, number>());
  const probeSequences = useRef(new Map<string, number>());
  const checked = useRef(new Set<string>());
  const queued = useRef<{ keys: Set<string>; promise: Promise<void> } | null>(null);
  useLayoutEffect(() => { latest.current = { identity, userId: session.user?.id }; statesRef.current = snapshot.identity === identity ? snapshot.states : new Map(); }, [identity, session.user?.id, snapshot]);
  const current = snapshot.identity === identity ? snapshot : undefined;
  const signedOut = session.status === "signed_out" || (!hasSession && !session.user);
  const status: Status = signedOut ? "signed_out" : session.status === "unavailable" ? "unavailable" : current?.status || "loading";
  useEffect(() => {
    if (signedOut) return;
    const controller = new AbortController(); controllers.current.add(controller);
    // Keep the bounded legacy bootstrap; visible cards also look up their exact
    // keys through /states, so favourites beyond the first 100 are not lost.
    api<{ items: Array<{ type: SavedType; id: string }> }>("/saved-items?limit=100", { signal: controller.signal }).then((result) => {
      if (controller.signal.aborted || latest.current.identity !== identity) return;
      setSnapshot((prior) => {
        const states = new Map(prior.identity === identity ? prior.states : []);
        for (const item of result.items || []) { const ref = savedReference(item.type, item.id); if (ref && !states.has(ref.key)) states.set(ref.key, { key: ref.key, saved: true, collection_ids: [] }); }
        return { identity, status: "authenticated", states, revision: prior.revision };
      });
    }).catch((reason) => {
      if (!controller.signal.aborted && latest.current.identity === identity) setSnapshot({ identity, status: reason instanceof ApiError && reason.status === 401 ? "signed_out" : "unavailable", states: new Map(), revision: 0 });
    }).finally(() => controllers.current.delete(controller));
    const active = controllers.current; const currentGenerations = generations.current; const currentChecked = checked.current; const currentProbes = probeSequences.current;
    return () => { for (const request of active) request.abort(); active.clear(); currentGenerations.clear(); currentChecked.clear(); currentProbes.clear(); queued.current = null; };
  }, [identity, signedOut]);
  const acceptStates = useCallback((items: SavedState[], changed = false) => {
    if (latest.current.identity !== identity) return;
    for (const item of items) checked.current.add(item.key);
    setSnapshot((prior) => {
      const states = new Map(prior.identity === identity ? prior.states : []);
      for (const item of items) states.set(item.key, item);
      return { identity, status: "authenticated", states, revision: prior.revision + (changed ? 1 : 0) };
    });
  }, [identity]);
  const ensureStates = useCallback(async (keys: string[], force = false) => {
    if (signedOut || latest.current.identity !== identity) return;
    const unique = [...new Set(keys.map((key) => parseSavedKey(key)?.key).filter((key): key is string => Boolean(key)))];
    const missing = unique.filter((key) => force || !checked.current.has(key));
    if (!missing.length) return;
    if (queued.current) { for (const key of missing) queued.current.keys.add(key); return queued.current.promise; }
    const keysToCheck = new Set(missing);
    const promise = Promise.resolve().then(async () => {
    if (latest.current.identity !== identity) return;
    queued.current = null;
    const missing = [...keysToCheck];
    for (let offset = 0; offset < missing.length; offset += 100) {
      const batch = missing.slice(offset, offset + 100);
      const generation = new Map(batch.map((key) => [key, generations.current.get(key) || 0]));
      const probes = new Map(batch.map((key) => { const next = (probeSequences.current.get(key) || 0) + 1; probeSequences.current.set(key, next); return [key, next]; }));
      const controller = new AbortController(); controllers.current.add(controller);
      try {
        const result = await api<{ items: SavedState[] }>("/saved-items/states", { method: "POST", body: JSON.stringify({ keys: batch }), signal: controller.signal });
        if (controller.signal.aborted || latest.current.identity !== identity) return;
        acceptStates((result.items || []).filter((item) => generation.get(item.key) === (generations.current.get(item.key) || 0) && probes.get(item.key) === probeSequences.current.get(item.key)));
      } finally { controllers.current.delete(controller); }
    }
    });
    queued.current = { keys: keysToCheck, promise };
    return promise;
  }, [identity, signedOut, acceptStates]);
  const setSaved = useCallback(async (type: SavedType, id: string, saved: boolean) => {
    if (status !== "authenticated" || latest.current.identity !== identity) throw new ApiError("Authentication required", 401, "authentication_required");
    const ref = savedReference(type, id)!;
    const generation = (generations.current.get(ref.key) || 0) + 1; generations.current.set(ref.key, generation);
    const controller = new AbortController(); controllers.current.add(controller);
    const expected = latest.current.userId ? `?expected_user_id=${encodeURIComponent(latest.current.userId)}` : "";
    try {
      const result = await api<{ collection_ids?: string[] } | undefined>(`/saved-items/${ref.type}/${encodeURIComponent(ref.id)}${expected}`, { method: saved ? "PUT" : "DELETE", signal: controller.signal });
      if (controller.signal.aborted || latest.current.identity !== identity) throw new DOMException("Session changed", "AbortError");
      if (generations.current.get(ref.key) === generation) acceptStates([{ key: ref.key, saved, collection_ids: saved ? result?.collection_ids || [] : [] }], true);
    } finally { controllers.current.delete(controller); }
  }, [status, identity, acceptStates]);
  const state = useCallback((key: string) => signedOut ? undefined : current?.states.get(parseSavedKey(key)?.key || key), [current, signedOut]);
  const isSaved = useCallback((type: SavedType, id: string) => Boolean(state(savedReference(type, id)?.key || "")?.saved), [state]);
  const toggle = useCallback(async (type: SavedType, id: string) => { const next = !isSaved(type, id); await setSaved(type, id, next); return next; }, [isSaved, setSaved]);
  const value = useMemo(() => ({ status, revision: current?.revision || 0, isSaved, state, ensureStates, acceptStates, setSaved, toggle }), [status, current?.revision, isSaved, state, ensureStates, acceptStates, setSaved, toggle]);
  return <SavedContext.Provider value={value}>{children}</SavedContext.Provider>;
}
export function useSavedItems() { return useContext(SavedContext); }
