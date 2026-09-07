import { PetAdmin } from "@/components/community/pet-admin";
import { communityMetadata } from "@/components/community/page";
export const generateMetadata = () => communityMetadata("adminPets");
export default function Page() { return <PetAdmin />; }
