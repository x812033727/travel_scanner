import type { Metadata } from "next";
import { AirlineFareLab } from "@/components/airline-fare-lab";
import { SiteHeader } from "@/components/site-header";

export const metadata: Metadata = {
  title: "航空票價實驗室｜Travel Scanner",
  description: "比較華航、長榮與星宇航空公開頁面的近期快取票價與來源狀態。",
};

export default function AirlineFareLabPage() {
  return (
    <>
      <SiteHeader />
      <AirlineFareLab />
    </>
  );
}
