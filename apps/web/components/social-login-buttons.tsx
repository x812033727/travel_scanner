"use client";

import { useLocale, useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import type { Locale } from "@/i18n/routing";
import { api } from "@/lib/api";

type Provider = "google" | "line" | "apple";
type ProviderStatus = { providers: Record<Provider, boolean> };

const providers: Array<{ id: Provider; mark: string; className: string }> = [
  { id: "google", mark: "G", className: "border-[var(--line)] bg-white text-[#3c4043]" },
  { id: "line", mark: "LINE", className: "border-[#06c755] bg-[#06c755] text-white" },
  { id: "apple", mark: "", className: "border-black bg-black text-white" },
];

const knownErrors = new Set([
  "oauth_cancelled",
  "oauth_state_invalid",
  "oauth_nonce_invalid",
  "oauth_token_invalid",
  "oauth_email_required",
  "oauth_account_exists",
  "oauth_identity_conflict",
  "oauth_identity_revoked",
  "oauth_provider_unavailable",
  "oauth_link_session_invalid",
  "registration_closed",
]);

export function SocialLoginButtons({
  nextPath,
  intent = "login",
  oauthError,
}: {
  nextPath: string;
  intent?: "login" | "link";
  oauthError?: string;
}) {
  const locale = useLocale() as Locale;
  const t = useTranslations("auth");
  const [status, setStatus] = useState<ProviderStatus>();
  useEffect(() => {
    api<ProviderStatus>("/auth/oauth/providers").then(setStatus).catch(() => undefined);
  }, []);
  const available = providers.filter((provider) => status?.providers[provider.id]);
  return (
    <div className="mt-7 space-y-3">
      {oauthError && (
        <p role="alert" className="rounded-xl bg-red-50 p-3 text-sm text-red-800">
          {t(`oauthErrors.${knownErrors.has(oauthError) ? oauthError : "oauth_token_invalid"}`)}
        </p>
      )}
      {available.map((provider) => (
        <a
          key={provider.id}
          href={`/api/auth/oauth/${provider.id}/start?intent=${intent}&locale=${locale}&next=${encodeURIComponent(nextPath)}`}
          className={`flex min-h-12 w-full items-center justify-center gap-3 rounded-xl border px-4 font-semibold shadow-sm transition active:scale-[.99] ${provider.className}`}
        >
          <span aria-hidden="true" className={`min-w-7 text-center font-black ${provider.id === "apple" ? "text-xl" : "text-sm"}`}>{provider.mark}</span>
          {t(`continueWith.${provider.id}`)}
        </a>
      ))}
      {available.length > 0 && (
        <div className="flex items-center gap-3 py-2 text-xs text-[var(--muted)]" aria-hidden="true">
          <span className="h-px flex-1 bg-[var(--line)]" />
          {t("orUseEmail")}
          <span className="h-px flex-1 bg-[var(--line)]" />
        </div>
      )}
    </div>
  );
}
