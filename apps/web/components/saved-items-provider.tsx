"use client";

import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { ApiError, api } from "@/lib/api";

type SavedType = "hotspot" | "food" | "restaurant";
type SavedItem = { type: SavedType; id: string };
type SavedContextValue = {
  status: "loading" | "authenticated" | "signed_out" | "unavailable";
  isSaved: (type: SavedType, id: string) => boolean;
  toggle: (type: SavedType, id: string) => Promise<boolean>;
};

const fallbackContext: SavedContextValue = {
  status: "signed_out",
  isSaved: () => false,
  toggle: async () => false,
};
const SavedContext = createContext<SavedContextValue>(fallbackContext);

export function SavedItemsProvider({ children }: { children: ReactNode }) {
  const [status, setStatus] = useState<SavedContextValue["status"]>("loading");
  const [keys, setKeys] = useState<Set<string>>(new Set());
  useEffect(() => {
    api<{ items: SavedItem[] }>("/saved-items?limit=100")
      .then((result) => {
        setKeys(new Set(result.items.map((item) => `${item.type}:${item.id}`)));
        setStatus("authenticated");
      })
      .catch((reason) => setStatus(reason instanceof ApiError && reason.status === 401 ? "signed_out" : "unavailable"));
  }, []);
  const isSaved = useCallback((type: SavedType, id: string) => keys.has(`${type}:${id}`), [keys]);
  const toggle = useCallback(async (type: SavedType, id: string) => {
    if (status !== "authenticated") throw new ApiError("請先登入後再繼續", 401, "authentication_required");
    const key = `${type}:${id}`;
    const next = !keys.has(key);
    await api(`/saved-items/${type}/${encodeURIComponent(id)}`, { method: next ? "PUT" : "DELETE" });
    setKeys((current) => {
      const updated = new Set(current);
      if (next) updated.add(key); else updated.delete(key);
      return updated;
    });
    return next;
  }, [keys, status]);
  const value = useMemo(() => ({ status, isSaved, toggle }), [status, isSaved, toggle]);
  return <SavedContext.Provider value={value}>{children}</SavedContext.Provider>;
}

export function useSavedItems() {
  return useContext(SavedContext);
}
