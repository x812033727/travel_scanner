import { LineLinkPanel } from "@/components/line-link-panel";
import { SiteHeader } from "@/components/site-header";

export default async function LineLinkPage({ searchParams }: { searchParams: Promise<{ linkToken?: string | string[] }> }) {
  const value = (await searchParams).linkToken;
  const linkToken = Array.isArray(value) ? value[0] : value;
  return <><SiteHeader /><main className="mx-auto max-w-md px-5 py-14"><div className="rounded-[2rem] border border-[var(--line)] bg-white p-8"><p className="text-sm font-semibold text-[#06a847]">LINE PRICE ALERTS</p><h1 className="mb-5 mt-2 text-3xl font-bold">連結 LINE 價格通知</h1><LineLinkPanel linkToken={linkToken} /></div></main></>;
}
