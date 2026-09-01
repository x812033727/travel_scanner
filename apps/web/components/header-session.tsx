"use client";

import { createContext, useContext, useEffect, useRef, useState, type ReactNode } from "react";
import { useLocale } from "next-intl";
import { usePathname, useRouter } from "@/i18n/navigation";
import { isLocale } from "@/i18n/routing";
import { ApiError, api } from "@/lib/api";

export type HeaderUser = {
  id: string;
  email: string;
  is_admin?: boolean;
  preferred_locale?: string;
};

type HeaderSessionValue = {
  status: "loading" | "authenticated" | "signed_out" | "unavailable";
  user: HeaderUser | null;
  logout: () => Promise<void>;
};

const HeaderSessionContext = createContext<HeaderSessionValue>({
  status: "loading",
  user: null,
  logout: async () => undefined,
});

export function HeaderSessionProvider({ children }: { children: ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const locale = useLocale();
  const loadedLocale = useRef<string | undefined>(undefined);
  const requestId = useRef(0);
  const [status, setStatus] = useState<HeaderSessionValue["status"]>("loading");
  const [user, setUser] = useState<HeaderUser | null>(null);

  useEffect(() => {
    if (loadedLocale.current === locale) return;
    loadedLocale.current = locale;
    const currentRequest = ++requestId.current;
    setStatus("loading");
    api<HeaderUser>("/auth/me")
      .then((currentUser) => {
        if (requestId.current !== currentRequest) return;
        setUser(currentUser);
        setStatus("authenticated");
        if (
          isLocale(currentUser.preferred_locale) &&
          currentUser.preferred_locale !== locale
        ) {
          document.cookie = `travel_locale=${currentUser.preferred_locale}; path=/; max-age=31536000; samesite=lax`;
          router.replace(pathname, { locale: currentUser.preferred_locale });
        }
      })
      .catch((reason) => {
        if (requestId.current !== currentRequest) return;
        setUser(null);
        setStatus(reason instanceof ApiError && reason.status === 401 ? "signed_out" : "unavailable");
      });
  }, [locale, pathname, router]);

  async function logout() {
    requestId.current += 1;
    try { await api("/auth/logout", { method: "POST" }); } catch { /* BFF clears the cookie. */ }
    setUser(null);
    setStatus("signed_out");
    router.push("/");
    router.refresh();
  }

  return (
    <HeaderSessionContext.Provider value={{ status, user, logout }}>
      {children}
    </HeaderSessionContext.Provider>
  );
}

export function useHeaderSession() {
  return useContext(HeaderSessionContext);
}
