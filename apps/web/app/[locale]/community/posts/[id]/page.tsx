import { PostDetails } from "@/components/community/post";
import { CommunityPage, communityMetadata } from "@/components/community/page";
export const generateMetadata = () => communityMetadata("post");
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return <CommunityPage title="post" member={false}><PostDetails id={id} /></CommunityPage>;
}
