import type { Metadata } from "next";
import type { Locale } from "@/i18n/routing";
import { ProfileView } from "@/components/community/profile";
import { CommunityPage, communityMetadata } from "@/components/community/page";
import { getPublicProfile, metaDescription } from "@/lib/community/public.server";

type Props = { params: Promise<{ locale: Locale; handle: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale, handle } = await params;
  const profile = await getPublicProfile(locale, handle);
  if (!profile) return communityMetadata("profile");
  // The handle rides along in the title because display names are not unique and two
  // authors sharing one is exactly the case a result list has to separate.
  return communityMetadata("profile", {
    index: true,
    name: `${profile.display_name} (@${profile.handle})`,
    description: metaDescription(profile.bio),
  });
}

export default async function Page({ params }: Props) {
  const { locale, handle } = await params;
  const profile = await getPublicProfile(locale, handle);
  return <CommunityPage title="profile" heading={false} member={false}><ProfileView handle={handle} initial={profile ?? undefined} /></CommunityPage>;
}
