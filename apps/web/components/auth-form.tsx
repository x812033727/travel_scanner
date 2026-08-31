"use client";

import { useRouter } from "next/navigation";
import { type FormEvent, useState, useSyncExternalStore } from "react";
import { ApiError, api } from "@/lib/api";
import { safeNextPath } from "@/lib/navigation";

export function AuthForm({ mode, nextPath = "/" }: { mode: "login" | "register"; nextPath?: string }) {
  const router = useRouter();
  const [error, setError] = useState<string>();
  const [busy, setBusy] = useState(false);
  const ready = useSyncExternalStore(
    () => () => undefined,
    () => true,
    () => false,
  );
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBusy(true); setError(undefined);
    try {
      await api(`/auth/${mode}`, { method: "POST", body: JSON.stringify({ email, password }) });
      router.push(safeNextPath(nextPath));
      router.refresh();
    } catch (reason) {
      setError((reason as Error).message);
      if (reason instanceof ApiError && [401, 409, 422].includes(reason.status)) setPassword("");
      setBusy(false);
    }
  }
  return <form onSubmit={submit} className="mt-7 space-y-4"><label className="block text-sm font-semibold">Email<input required disabled={!ready} autoComplete="email" type="email" name="email" value={email} onChange={(event) => setEmail(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] p-3 font-normal disabled:opacity-60" /></label><label className="block text-sm font-semibold">密碼<input required disabled={!ready} minLength={10} autoComplete={mode === "login" ? "current-password" : "new-password"} type="password" name="password" value={password} onChange={(event) => setPassword(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] p-3 font-normal disabled:opacity-60" /><span className="mt-1 block text-xs font-normal text-[var(--muted)]">至少 10 個字元</span></label>{error && <p role="alert" className="text-sm text-red-700">{error}</p>}<button disabled={!ready || busy} className="w-full rounded-xl bg-[var(--teal)] p-3.5 font-semibold text-white disabled:opacity-50">{busy ? "處理中…" : mode === "login" ? "登入" : "建立免費帳號"}</button></form>;
}
