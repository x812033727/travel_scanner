import Link from "next/link";
import { AuthForm } from "@/components/auth-form";
import { SiteHeader } from "@/components/site-header";

import { safeNextPath } from "@/lib/navigation";
import { getRegistrationAvailability } from "@/lib/registration";

export default async function RegisterPage({ searchParams }: { searchParams: Promise<{ next?: string | string[] }> }) {
  const [params, registration] = await Promise.all([searchParams, getRegistrationAvailability()]);
  const nextPath = safeNextPath(params.next);
  if (registration !== "open") {
    const unavailable = registration === "unavailable";
    return <><SiteHeader /><main className="mx-auto max-w-md px-5 py-14"><div className="rounded-[2rem] border border-[var(--line)] bg-white p-8"><p className="text-sm font-semibold text-[var(--teal)]">{unavailable ? "註冊狀態無法確認" : "公開註冊暫停"}</p><h1 className="mt-2 text-3xl font-bold">{unavailable ? "暫時無法確認註冊狀態" : "目前暫停開放註冊"}</h1><p className="mt-3 text-sm leading-6 text-[var(--muted)]">{unavailable ? "狀態服務目前無法使用，為避免送出無法完成的註冊，請稍後再試。" : "系統目前不接受新帳號申請；既有會員仍可正常登入與使用服務。"}</p><Link className="mt-6 inline-flex rounded-xl bg-[var(--teal)] px-5 py-3 font-semibold text-white" href={`/login?next=${encodeURIComponent(nextPath)}`}>前往登入</Link></div></main></>;
  }
  return <><SiteHeader /><main className="mx-auto max-w-md px-5 py-14"><div className="rounded-[2rem] border border-[var(--line)] bg-white p-8"><p className="text-sm font-semibold text-[var(--teal)]">註冊免費取得 3 次</p><h1 className="mt-2 text-3xl font-bold">建立你的旅行帳號</h1><p className="mt-3 text-sm leading-6 text-[var(--muted)]">成功取得可用查價結果才扣 1 次，失敗不扣；剩餘次數不會按月歸零。</p><AuthForm mode="register" nextPath={nextPath} /><p className="mt-5 text-center text-sm text-[var(--muted)]">已經有帳號？ <Link className="text-[var(--teal)] underline" href={`/login?next=${encodeURIComponent(nextPath)}`}>直接登入</Link></p></div></main></>;
}

