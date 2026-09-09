import { Suspense } from "react";
import { getLocale } from "next-intl/server";
import { adminDomainsCopy } from "@/lib/admin-domains-copy";
import { AdminFoodsWorkspace } from "@/components/admin-foods-workspace";

export default async function AdminFoodsPage() {
  const copy = adminDomainsCopy(await getLocale());
  return <main className="admin-page"><h1 className="text-3xl font-bold md:text-4xl">{copy.foods}</h1><p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">{copy.foodsDescription}</p><Suspense fallback={<p>{copy.loading}</p>}><AdminFoodsWorkspace /></Suspense></main>;
}
