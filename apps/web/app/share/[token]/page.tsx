import type { Metadata } from "next";
import { SharedTripView } from "@/components/shared-trip-view";
import { SiteHeader } from "@/components/site-header";

export const metadata: Metadata = {
  title: "共享旅程｜Travel Scanner",
  description: "查看旅伴分享的每日行程與費用摘要。",
  openGraph: { images: [] },
  twitter: { images: [] },
};

export default async function SharePage({
  params,
}: {
  params: Promise<{ token: string }>;
}) {
  const { token } = await params;
  return <><SiteHeader /><SharedTripView token={token} /></>;
}
