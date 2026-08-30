"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { api } from "@/lib/api";

export function AuthForm({ mode }: { mode: "login" | "register" }) {
  const router = useRouter();
  const [error, setError] = useState<string>();
  const [busy, setBusy] = useState(false);
  async function submit(form: FormData) {
    setBusy(true); setError(undefined);
    try { await api(`/auth/${mode}`, { method: "POST", body: JSON.stringify({ email: form.get("email"), password: form.get("password") }) }); router.push("/"); router.refresh(); } catch (reason) { setError((reason as Error).message); setBusy(false); }
  }
  return <form action={submit} className="mt-7 space-y-4"><label className="block text-sm font-semibold">Email<input required type="email" name="email" className="mt-2 w-full rounded-xl border border-[var(--line)] p-3 font-normal" /></label><label className="block text-sm font-semibold">密碼<input required minLength={10} type="password" name="password" className="mt-2 w-full rounded-xl border border-[var(--line)] p-3 font-normal" /></label>{error && <p role="alert" className="text-sm text-red-700">{error}</p>}<button disabled={busy} className="w-full rounded-xl bg-[var(--teal)] p-3.5 font-semibold text-white disabled:opacity-50">{busy ? "處理中…" : mode === "login" ? "登入" : "建立免費帳號"}</button></form>;
}

