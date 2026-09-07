"use client";
import { useCallback, useEffect, useRef, useState } from "react";
import { api } from "@/lib/api";
import { useHeaderSession } from "@/components/header-session";

/** Responses stay bound to their URL and request generation. */
export function useResource<T>(path: string | null, fetcher: (path: string) => Promise<T> = api) {
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
  return {data: current?.data, error: current?.error, loading: Boolean(path && !current), reload};
}
