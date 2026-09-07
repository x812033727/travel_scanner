import { ProfileView } from "@/components/community/profile";
import { CommunityPage, communityMetadata } from "@/components/community/page";
export const generateMetadata = () => communityMetadata("profile");
export default async function Page({ params }: { params: Promise<{ handle: string }> }) {
  const { handle } = await params;
  return <CommunityPage title="profile" member={false}><ProfileView handle={handle} /></CommunityPage>;
}
