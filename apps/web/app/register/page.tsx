import Link from "next/link";
import { AuthForm } from "@/components/auth-form";
import { SiteHeader } from "@/components/site-header";

export default function RegisterPage() { return <><SiteHeader /><main className="mx-auto max-w-md px-5 py-14"><div className="rounded-[2rem] border border-[var(--line)] bg-white p-8"><p className="text-sm font-semibold text-[var(--teal)]">20 credits 免費開始</p><h1 className="mt-2 text-3xl font-bold">建立你的旅行帳號</h1><AuthForm mode="register" /><p className="mt-5 text-center text-sm text-[var(--muted)]">已經有帳號？ <Link className="text-[var(--teal)] underline" href="/login">直接登入</Link></p></div></main></>; }

