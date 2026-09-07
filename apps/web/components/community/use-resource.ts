"use client";
import { useCallback, useEffect, useRef, useState } from "react";
import { api } from "@/lib/api";

/** Responses stay bound to their URL and request generation. */
export function useResource<T>(path: string | null, fetcher: (path: string) => Promise<T> = api) {
  const [result, setResult] = useState<{path: string; data?: T; error?: unknown}>();
  const generation = useRef(0);
  const cancel = useCallback(() => { generation.current += 1; }, []);
  const reload = useCallback(async () => {
    if (!path) return;
    const id = ++generation.current;
    return fetcher(path)
      .then((data) => { if (id === generation.current) setResult({path,data}); })
      .catch((error) => { if (id === generation.current) setResult({path,error}); });
  }, [path, fetcher]);
  useEffect(() => { void reload(); return cancel; }, [reload, cancel]);
  useEffect(() => {
    const update = () => { void reload(); };
    window.addEventListener("community-refresh", update);
    return () => window.removeEventListener("community-refresh", update);
  }, [reload]);
  const current = result?.path === path ? result : undefined;
  return {data: current?.data, error: current?.error, loading: Boolean(path && !current), reload};
}
