"use client";

import { createContext, useCallback, useContext, useEffect, useRef, useState, type ReactNode } from "react";
import { useLocale } from "next-intl";
import { useSearchParams } from "next/navigation";
import { usePathname, useRouter } from "@/i18n/navigation";
import { isLocale } from "@/i18n/routing";
import { ApiError, api } from "@/lib/api";

/**
 * What `/auth/me` answers. Every field the page needs lives here rather than in each
 * component's own copy, because the point of the provider is that one request answers the
 * question for all of them: a signed-out /account used to send three.
 */
export type HeaderUser = {
  id: string;
  email: string;
  is_admin?: boolean;
  can_deploy?: boolean;
  preferred_locale?: string;
  preferred_currency?: string;
  has_password?: boolean;
  auth_methods?: string[];
  identity_count?: number;
  email_verified?: boolean;
};

type HeaderSessionValue = {
  status: "loading" | "authenticated" | "signed_out" | "unavailable";
  user: HeaderUser | null;
  setUser: (user: HeaderUser) => void;
  clearSession: () => void;
  logout: () => Promise<void>;
};

const HeaderSessionContext = createContext<HeaderSessionValue>({
  status: "loading",
  user: null,
  setUser: () => undefined,
  clearSession: () => undefined,
  logout: async () => undefined,
});

/** See SavedItemsProvider for what `hasSession` is and why an absent cookie is proof. */
export function HeaderSessionProvider({
  children,
  hasSession = true,
}: {
  children: ReactNode;
  hasSession?: boolean;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const locale = useLocale();
  const loadedLocale = useRef<string | undefined>(undefined);
  const requestId = useRef(0);
  const [status, setStatus] = useState<HeaderSessionValue["status"]>(
    hasSession ? "loading" : "signed_out",
  );
  const [user, setUser] = useState<HeaderUser | null>(null);

  useEffect(() => {
    if (!hasSession) return;
    if (loadedLocale.current === locale) return;
    loadedLocale.current = locale;
    const currentRequest = ++requestId.current;
    setStatus("loading");
    api<HeaderUser>("/auth/me")
      .then((currentUser) => {
        if (requestId.current !== currentRequest) return;
        setUser(currentUser);
        setStatus("authenticated");
        let pickedLocale = false;
        try {
          pickedLocale = window.sessionStorage.getItem("travel-locale-picked") === "1";
        } catch { /* storage can be blocked */ }
        if (
          isLocale(currentUser.preferred_locale) &&
          currentUser.preferred_locale !== locale &&
          // A locale the visitor picked this session wins over the stored
          // preference: the PATCH may still be in flight, and snapping back
          // to the old language right after they switched reads as a bug.
          !pickedLocale
        ) {
          document.cookie = `travel_locale=${currentUser.preferred_locale}; path=/; max-age=31536000; samesite=lax`;
          // usePathname carries no query or fragment; dropping them here used
          // to strip ?destination_id=... from deep links during the redirect.
          const query = searchParams?.toString() || "";
          router.replace(
            `${pathname}${query ? `?${query}` : ""}${window.location.hash}`,
            { locale: currentUser.preferred_locale },
          );
        }
      })
      .catch((reason) => {
        if (requestId.current !== currentRequest) return;
        setUser(null);
        setStatus(reason instanceof ApiError && reason.status === 401 ? "signed_out" : "unavailable");
      });
  }, [hasSession, locale, pathname, router, searchParams]);

  const clearSession = useCallback(() => {
    requestId.current += 1;
    // The offline worker holds this member's trip payload — hotel addresses and private
    // notes. Signing out on a shared phone has to take it with it.
    navigator.serviceWorker?.controller?.postMessage({ type: "signed-out" });
    setUser(null);
    setStatus("signed_out");
  }, []);

  const authenticate = useCallback((currentUser: HeaderUser) => {
    requestId.current += 1;
    setUser(currentUser);
    setStatus("authenticated");
  }, []);

  async function logout() {
    requestId.current += 1;
    try { await api("/auth/logout", { method: "POST" }); } catch { /* BFF clears the cookie. */ }
    clearSession();
    router.push("/");
    router.refresh();
  }

  return (
    <HeaderSessionContext.Provider value={{ status, user, clearSession, logout, setUser: authenticate }}>
      {children}
    </HeaderSessionContext.Provider>
  );
}

export function useHeaderSession() {
  return useContext(HeaderSessionContext);
}
