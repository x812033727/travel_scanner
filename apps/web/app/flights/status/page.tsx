import type { Metadata } from "next";
import { FlightStatusSearch } from "@/components/flight-status-search";
import { SiteHeader } from "@/components/site-header";

export const metadata: Metadata = {
  title: "即時航班動態｜Travel Scanner",
  description: "以班號或航線查詢 FlightAware 航班班表、延誤、取消、航廈與登機門。",
};

export default function FlightStatusPage() {
  return <><SiteHeader /><FlightStatusSearch /></>;
}
