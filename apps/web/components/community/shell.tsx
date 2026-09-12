"use client";

import { Fragment, type ReactNode } from "react";
import { useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";
import { useHeaderSession } from "@/components/header-session";
import { useCommunity } from "./provider";
import { Button, Empty, ErrorNotice } from "./ui";

export function CommunityGate({ children, member = false, verified = false }: { children: ReactNode; member?: boolean; verified?: boolean }) {
  const t = useTranslations("community");
  const community = useCommunity();
  const session = useHeaderSession();
  if (community.status !== "ready") return <Empty>{t("statusUnavailable")} <Button secondary onClick={() => void community.refreshFlags()}>{t("retry")}</Button></Empty>;
  if (!community.flags.enabled) return <Empty>{t("closed")}</Empty>;
  // A known session cookie is still resolving its identity. Mounting a guest
  // form now would discard early input when the account-bound key resolves.
  // Anonymous visitors start as signed_out and can read immediately.
  if (session.status === "loading") return <Empty>{t("loading")}</Empty>;
  if (member) {
    if (community.loading) return <Empty>{t("loading")}</Empty>;
    if (session.status === "signed_out") return <Empty><Link href="/login" className="text-[var(--teal)] underline">{t("loginRequired")}</Link></Empty>;
    if (community.error || session.status === "unavailable") return <ErrorNotice error={community.error || new Error()} />;
    if (!community.me?.profile) return <Empty><Link href="/community/settings" className="text-[var(--teal)] underline">{t("createProfile")}</Link></Empty>;
    if (community.me.restricted) return <Empty>{t("errors.community_restricted")}</Empty>;
    if (verified && !community.me.verified) return <Empty><Link href="/account" className="text-[var(--teal)] underline">{t("verifyRequired")}</Link></Empty>;
  }
  return <Fragment key={session.user?.id || "guest"}>{children}</Fragment>;
}

export function CommunityLinks() {
  const t = useTranslations("community");
  const { flags, unread } = useCommunity();
  if (!flags.enabled) return null;
  return <nav aria-label={t("title")} className="mb-6 flex flex-wrap items-center gap-2 text-sm">
    {[ ["/community", "feed"], ["/community/search", "search"], ["/pet-friendly", "pets"],
      ["/community/collections", "collections"], ["/community/drafts", "drafts"], ["/community/settings", "profileSettings"] ].map(([href, key]) => <Link key={key} href={href} className="inline-flex min-h-11 items-center rounded-xl border border-[var(--line)] px-3 py-2.5 hover:bg-[var(--paper)]">{t(key)}</Link>)}
    {flags.posting_enabled && <Link href="/community/new" className="inline-flex min-h-11 items-center rounded-xl bg-[var(--teal)] px-3 py-2.5 font-semibold text-white">{t("publish")}</Link>}
    <Link href="/community/messages" className="inline-flex min-h-11 items-center rounded-xl border border-[var(--line)] px-3 py-2.5">{t("messages")}{unread > 0 && <span className="ml-2 rounded-full bg-[var(--teal)] px-2 text-white">{unread}</span>}</Link>
  </nav>;
}
