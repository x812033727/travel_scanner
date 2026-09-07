import { getTranslations } from "next-intl/server";
import { Drafts } from "@/components/community/editor";
import { CommunityPage } from "@/components/community/page";
export async function generateMetadata() {
  const t = await getTranslations("metadata");
  return { title: t("draftsTitle"), description: t("draftsDescription"), robots: { index: false, follow: true } };
}
export default function Page() { return <CommunityPage title="drafts" member={true} verified={false}><Drafts /></CommunityPage>; }
