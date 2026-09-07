import { PostEditor } from "@/components/community/editor";
import { CommunityPage, communityMetadata } from "@/components/community/page";
export const generateMetadata = () => communityMetadata("editPost");
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return <CommunityPage title="editPost" member={true}><PostEditor id={id} /></CommunityPage>;
}
