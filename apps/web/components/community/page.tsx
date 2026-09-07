import type { ReactNode } from "react";
import { getTranslations } from "next-intl/server";
import { CommunityGate } from "./shell";
export async function CommunityPage({ title, children, member = false, verified = false }: { title: string; children: ReactNode; member?: boolean; verified?: boolean }) {
  const t = await getTranslations("community");
  return <><h1 className="mb-6 text-3xl font-bold">{t(title)}</h1><CommunityGate member={member} verified={verified}>{children}</CommunityGate></>;
}
export async function communityMetadata(title: string) {
  const t = await getTranslations("community");
  return { title: `${t(title)} | Mokaair`, robots: { index: false, follow: true } };
}
