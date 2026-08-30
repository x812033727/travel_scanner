import type { Metadata } from "next";
import { SiteHeader } from "@/components/site-header";
import { TripEditor } from "@/components/trip-editor";

export const metadata: Metadata = {
  title: "編輯旅程｜Travel Scanner",
  description: "調整每日安排、重新最佳化並分享完整旅程。",
};

export default async function TripPage({ params }: PageProps<"/trips/[id]">) {
  const { id } = await params;
  return <><SiteHeader /><TripEditor tripId={id} /></>;
}
