import { getTranslations } from "next-intl/server";
import { BlockedProfiles, ProfileEditor } from "@/components/community/profile";
import { CommunityPage } from "@/components/community/page";
export async function generateMetadata() {
  const t = await getTranslations("metadata");
  return { title: t("publicProfileTitle"), description: t("publicProfileDescription"), robots: { index: false, follow: true } };
}
export default function Page() { return <CommunityPage title="profileSettings" member={false} verified={false}><ProfileEditor /><BlockedProfiles /></CommunityPage>; }
