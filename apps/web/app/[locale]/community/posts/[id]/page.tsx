import type { Metadata } from "next";
import type { Locale } from "@/i18n/routing";
import { PostDetails } from "@/components/community/post";
import { CommunityPage, communityMetadata } from "@/components/community/page";
import { getPost, metaDescription } from "@/lib/community/public.server";

type Props = { params: Promise<{ locale: Locale; id: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale, id } = await params;
  const post = await getPost(locale, id);
  // The endpoint answers 404 for anything but a published post, so an absent record is a
  // draft, a hidden post or an outage -- none of them something to offer a crawler.
  if (!post) return communityMetadata("post");
  return communityMetadata("post", { index: true, name: post.title, description: metaDescription(post.body) });
}

export default async function Page({ params }: Props) {
  const { locale, id } = await params;
  const post = await getPost(locale, id);
  return <CommunityPage title="post" heading={false} member={false}><PostDetails id={id} initial={post ?? undefined} /></CommunityPage>;
}
