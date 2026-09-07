import { CommunityAdmin } from "@/components/community/admin";
import { communityMetadata } from "@/components/community/page";
export const generateMetadata = () => communityMetadata("adminCommunity");
export default function Page() { return <CommunityAdmin />; }
