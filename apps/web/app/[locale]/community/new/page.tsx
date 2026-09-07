import { getTranslations } from "next-intl/server";
import { PostEditor } from "@/components/community/editor";
import { CommunityPage } from "@/components/community/page";
export async function generateMetadata() {
  const t = await getTranslations("metadata");
  return { title: t("publishTitle"), description: t("publishDescription"), robots: { index: false, follow: true } };
}
export default function Page() { return <CommunityPage title="publish" member={true} verified={true}><PostEditor /></CommunityPage>; }
