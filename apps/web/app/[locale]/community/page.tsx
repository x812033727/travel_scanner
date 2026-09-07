import { getTranslations } from "next-intl/server";
import { Feed } from "@/components/community/feed";
import { CommunityPage } from "@/components/community/page";
export async function generateMetadata() {
  const t = await getTranslations("metadata");
  return { title: t("communityTitle"), description: t("communityDescription"), robots: { index: false, follow: true } };
}
export default function Page() { return <CommunityPage title="feed" member={false} verified={false}><Feed /></CommunityPage>; }
