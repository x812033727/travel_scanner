import { getTranslations } from "next-intl/server";
import { Collections } from "@/components/community/collections";
import { CommunityPage } from "@/components/community/page";
export async function generateMetadata() {
  const t = await getTranslations("metadata");
  return { title: t("collectionsTitle"), description: t("collectionsDescription"), robots: { index: false, follow: true } };
}
export default function Page() { return <CommunityPage title="collections" member={true} verified={false}><Collections /></CommunityPage>; }
