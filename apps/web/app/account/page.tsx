import { AccountPanel } from "@/components/account-panel";
import { SiteHeader } from "@/components/site-header";

export default function AccountPage() {
  return <><SiteHeader /><main className="mx-auto max-w-6xl px-5 py-12"><p className="text-sm font-semibold text-[var(--teal)]">MY ACCOUNT</p><h1 className="mb-8 mt-2 text-4xl font-bold">會員專區</h1><AccountPanel /></main></>;
}
