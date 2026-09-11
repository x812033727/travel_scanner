"use client";

import { useLocale, useTranslations } from "next-intl";
import { useEffect, useState, type ComponentType } from "react";
import { AppleMark, GoogleMark, LineMark } from "@/components/brand-marks";
import type { Locale } from "@/i18n/routing";
import { api } from "@/lib/api";

type Provider = "google" | "line" | "apple";
type ProviderStatus = { providers: Record<Provider, boolean> };

// Each provider's sign-in guidelines fix its button as well as its logo: Google's
// light button is white with dark text, LINE's is its own #06C755, Apple's is
// black. These are brand assets, not palette choices, so they stay fixed in both
// themes instead of following the site's CSS variables.
const providers: Array<{ id: Provider; Mark: ComponentType<{ className?: string }>; className: string }> = [
  { id: "google", Mark: GoogleMark, className: "border-[#747775] bg-white text-[#1f1f1f]" },
  { id: "line", Mark: LineMark, className: "border-[#06c755] bg-[#06c755] text-white" },
  { id: "apple", Mark: AppleMark, className: "border-black bg-black text-white" },
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
  "admin_email_reserved",
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
  const [settled, setSettled] = useState(false);
  useEffect(() => {
    let active = true;
    api<ProviderStatus>("/auth/oauth/providers")
      .then((result) => { if (active) setStatus(result); })
      .catch(() => undefined)
      .finally(() => { if (active) setSettled(true); });
    return () => { active = false; };
  }, []);
  const available = providers.filter((provider) => status?.providers[provider.id]);
  return (
    <div className="mt-7 space-y-3">
      {oauthError && (
        <p role="alert" className="rounded-xl bg-red-50 p-3 text-sm text-red-800">
          {t(`oauthErrors.${knownErrors.has(oauthError) ? oauthError : "oauth_token_invalid"}`)}
        </p>
      )}
      {/* Which providers exist is only known after a request, and the email form
          sits directly below: without this the form is laid out at the top of the
          card and then shoved down as the buttons arrive under the reader's
          pointer. One placeholder row holds that space until the answer lands. */}
      {!settled && <div aria-hidden="true" className="h-12 w-full animate-pulse rounded-xl bg-[var(--paper)]" />}
      {available.map(({ id, Mark, className }) => (
        <a
          key={id}
          href={`/api/auth/oauth/${id}/start?intent=${intent}&locale=${locale}&next=${encodeURIComponent(nextPath)}`}
          className={`flex min-h-12 w-full items-center justify-center gap-3 rounded-xl border px-4 font-semibold shadow-sm transition active:scale-[.99] ${className}`}
        >
          <Mark />
          {t(`continueWith.${id}`)}
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
