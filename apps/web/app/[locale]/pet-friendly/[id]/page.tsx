import { PetDetails } from "@/components/community/pets";
import { CommunityPage, communityMetadata } from "@/components/community/page";
export const generateMetadata = () => communityMetadata("pets");
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return <CommunityPage title="pets" member={false}><PetDetails id={id} /></CommunityPage>;
}
