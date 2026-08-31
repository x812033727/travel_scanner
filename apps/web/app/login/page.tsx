import Link from "next/link";
import { AuthForm } from "@/components/auth-form";
import { SiteHeader } from "@/components/site-header";

import { safeNextPath } from "@/lib/navigation";

export default async function LoginPage({ searchParams }: { searchParams: Promise<{ next?: string | string[] }> }) {
  const nextPath = safeNextPath((await searchParams).next);
  return <><SiteHeader /><main className="mx-auto max-w-md px-5 py-14"><div className="rounded-[2rem] border border-[var(--line)] bg-white p-8"><p className="text-sm font-semibold text-[var(--teal)]">歡迎回來</p><h1 className="mt-2 text-3xl font-bold">登入 Travel Scanner</h1><AuthForm mode="login" nextPath={nextPath} /><p className="mt-5 text-center text-sm text-[var(--muted)]">還沒有帳號？ <Link className="text-[var(--teal)] underline" href={`/register?next=${encodeURIComponent(nextPath)}`}>免費註冊</Link></p></div></main></>;
}
