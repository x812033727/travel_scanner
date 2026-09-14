import type { ReactNode } from "react";
import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import { CommunityGate } from "./shell";

/**
 * `heading` is the section label, and a detail route turns it off. Those pages render the
 * record's own name as an `<h1>` -- the place, the post title, the display name -- so with
 * the label on they shipped two `<h1>` elements, one of them identical on every record in
 * the section. The directory keeps it: there the label is the only heading on the page.
 */
export async function CommunityPage({ title, children, member = false, verified = false, heading = true }: { title: string; children: ReactNode; member?: boolean; verified?: boolean; heading?: boolean }) {
  const t = await getTranslations("community");
  return <>{heading ? <h1 className="mb-6 text-3xl font-bold">{t(title)}</h1> : null}<CommunityGate member={member} verified={verified}>{children}</CommunityGate></>;
}

/**
 * `index` defaults to `false` so that every caller which does not think about indexing --
 * the admin consoles and the post editor -- keeps the `noindex` it has always had. Only a
 * route that has server-rendered the record it is describing passes `true`.
 *
 * `name` and `description` come from that record. Without them each page in a section shared
 * one fixed title ("Travel post | Mokaair"), which no crawler and no reader can tell apart.
 */
export async function communityMetadata(
  title: string,
  { index = false, name, description }: { index?: boolean; name?: string; description?: string } = {},
): Promise<Metadata> {
  const t = await getTranslations("community");
  return {
    title: `${name?.trim() || t(title)} | Mokaair`,
    ...(description ? { description } : {}),
    robots: { index, follow: true },
  };
}
