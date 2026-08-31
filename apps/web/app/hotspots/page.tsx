import type { Metadata } from "next";
import { HotspotExplorer } from "@/components/hotspot-explorer";
import { SiteHeader } from "@/components/site-header";

export const metadata: Metadata = {
  title: "熱門景點排行榜｜Travel Scanner",
  description: "搜尋日本、韓國與泰國景點，查看最近 30 天關注度與升溫趨勢。",
};

export default function HotspotsPage() {
  return <><SiteHeader /><HotspotExplorer /></>;
}
