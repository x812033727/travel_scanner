import Link from "next/link";
import { AuthForm } from "@/components/auth-form";
import { SiteHeader } from "@/components/site-header";

export default function LoginPage() { return <><SiteHeader /><main className="mx-auto max-w-md px-5 py-14"><div className="rounded-[2rem] border border-[var(--line)] bg-white p-8"><p className="text-sm font-semibold text-[var(--teal)]">歡迎回來</p><h1 className="mt-2 text-3xl font-bold">登入 Travel Scanner</h1><AuthForm mode="login" /><p className="mt-5 text-center text-sm text-[var(--muted)]">還沒有帳號？ <Link className="text-[var(--teal)] underline" href="/register">免費註冊</Link></p></div></main></>; }

