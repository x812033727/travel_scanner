import { getTranslations } from "next-intl/server";
import { CommunitySearch } from "@/components/community/feed";
import { CommunityPage } from "@/components/community/page";
export async function generateMetadata() {
  const t = await getTranslations("metadata");
  return { title: t("communitySearchTitle"), description: t("communitySearchDescription"), robots: { index: false, follow: true } };
}
export default function Page() { return <CommunityPage title="search" member={false} verified={false}><CommunitySearch /></CommunityPage>; }
