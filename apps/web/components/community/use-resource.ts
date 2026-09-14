"use client";
import { useCallback, useEffect, useRef, useState } from "react";
import { api } from "@/lib/api";
import { useHeaderSession } from "@/components/header-session";

/** Responses stay bound to their URL and request generation. */
export function useResource<T>(path: string | null, fetcher: (path: string) => Promise<T> = api, initial?: T) {
  const { user } = useHeaderSession();
  const owner = user?.id || "guest";
  const [result, setResult] = useState<{path: string; owner: string; data?: T; error?: unknown}>();
  const generation = useRef(0);
  const cancel = useCallback(() => { generation.current += 1; }, []);
  const reload = useCallback(async () => {
    if (!path) return;
    const id = ++generation.current;
    return fetcher(path)
      .then((data) => { if (id === generation.current) setResult({path,owner,data}); })
      .catch((error) => { if (id === generation.current) setResult({path,owner,error}); });
  }, [path, owner, fetcher]);
  useEffect(() => { void reload(); return cancel; }, [reload, cancel]);
  useEffect(() => {
    const update = () => { void reload(); };
    window.addEventListener("community-refresh", update);
    return () => window.removeEventListener("community-refresh", update);
  }, [reload]);
  const current = result?.path === path && result?.owner === owner ? result : undefined;
  // The server's copy of whichever path this hook was first asked for. It answers until the
  // client's own request does, so a server-rendered page does not blank back to "loading" on
  // hydration. Bound to that first path on purpose: the directory changes `path` when the
  // reader submits a filter, and answering a filtered query with the unfiltered first page
  // would show them the list they just filtered away.
  // State, not a ref: this is read while rendering, and a ref read during render is both a
  // lint error and a value React does not promise is current.
  const [seededPath] = useState(path);
  const seed = initial !== undefined && path === seededPath ? initial : undefined;
  return {data: current?.data ?? seed, error: current?.error, loading: Boolean(path && !current && seed === undefined), reload};
}
