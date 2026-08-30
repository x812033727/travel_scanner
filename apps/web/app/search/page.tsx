import { Suspense } from "react";
import { SearchExperience } from "@/components/search-experience";
import { SiteHeader } from "@/components/site-header";

export default function SearchPage() {
  return <><SiteHeader /><Suspense fallback={<main className="mx-auto max-w-6xl px-5">正在理解旅行需求…</main>}><SearchExperience /></Suspense></>;
}

