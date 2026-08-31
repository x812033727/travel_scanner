import Link from "next/link";
import { AuthForm } from "@/components/auth-form";
import { SiteHeader } from "@/components/site-header";

import { safeNextPath } from "@/lib/navigation";

export default async function RegisterPage({ searchParams }: { searchParams: Promise<{ next?: string | string[] }> }) {
  const nextPath = safeNextPath((await searchParams).next);
  return <><SiteHeader /><main className="mx-auto max-w-md px-5 py-14"><div className="rounded-[2rem] border border-[var(--line)] bg-white p-8"><p className="text-sm font-semibold text-[var(--teal)]">註冊免費取得 3 次</p><h1 className="mt-2 text-3xl font-bold">建立你的旅行帳號</h1><p className="mt-3 text-sm leading-6 text-[var(--muted)]">成功取得可用查價結果才扣 1 次，失敗不扣；剩餘次數不會按月歸零。</p><AuthForm mode="register" nextPath={nextPath} /><p className="mt-5 text-center text-sm text-[var(--muted)]">已經有帳號？ <Link className="text-[var(--teal)] underline" href={`/login?next=${encodeURIComponent(nextPath)}`}>直接登入</Link></p></div></main></>;
}

