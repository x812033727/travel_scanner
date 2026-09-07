import { getTranslations } from "next-intl/server";
import { MessageCenter } from "@/components/community/messages";
import { CommunityPage } from "@/components/community/page";
export async function generateMetadata() {
  const t = await getTranslations("metadata");
  return { title: t("messagesTitle"), description: t("messagesDescription"), robots: { index: false, follow: true } };
}
export default async function Page({ searchParams }: { searchParams: Promise<{ conversation?: string; tab?:string }> }) {
 const { conversation, tab } = await searchParams;
 return <CommunityPage title="messages" member><MessageCenter conversationId={conversation} showReviews={tab === "reviews"} /></CommunityPage>;
}
