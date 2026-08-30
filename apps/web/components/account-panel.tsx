"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

type Me = { id: string; email: string; plan: string };
type Usage = { plan: string; credits_remaining: number; monthly_credits: number; period_start: string; period_end: string };

const dateFormat = new Intl.DateTimeFormat("zh-TW", { dateStyle: "medium" });
const inputClass = "mt-2 w-full rounded-xl border border-[var(--line)] p-3 font-normal";

export function AccountPanel() {
  const [me, setMe] = useState<Me>();
  const [usage, setUsage] = useState<Usage>();
  const [loadError, setLoadError] = useState<string>();
  const [formError, setFormError] = useState<string>();
  const [done, setDone] = useState(false);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    api<Me>("/auth/me").then(setMe).catch((reason: Error) => setLoadError(reason.message));
    api<Usage>("/usage").then(setUsage).catch(() => undefined);
  }, []);

  async function changePassword(form: FormData) {
    setBusy(true); setFormError(undefined); setDone(false);
    const newPassword = form.get("new_password");
    if (newPassword !== form.get("confirm_password")) {
      setFormError("兩次輸入的新密碼不一致"); setBusy(false); return;
    }
    try {
      await api("/auth/change-password", {
        method: "POST",
        body: JSON.stringify({ current_password: form.get("current_password"), new_password: newPassword }),
      });
      setDone(true);
    } catch (reason) {
      setFormError((reason as Error).message);
    } finally {
      setBusy(false);
    }
  }

  if (loadError) return <p className="rounded-xl bg-red-50 p-4 text-red-700">{loadError}，請先<Link className="underline" href="/login">登入</Link>。</p>;
  if (!me) return <p className="text-[var(--muted)]">正在載入帳號資料…</p>;

  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-[var(--line)] bg-white p-8">
        <h2 className="text-xl font-bold">帳號資訊</h2>
        <dl className="mt-5 grid gap-4 sm:grid-cols-3">
          <div><dt className="text-sm text-[var(--muted)]">Email</dt><dd className="mt-1 font-semibold break-all">{me.email}</dd></div>
          <div><dt className="text-sm text-[var(--muted)]">方案</dt><dd className="mt-1 font-semibold">{me.plan}</dd></div>
          <div>
            <dt className="text-sm text-[var(--muted)]">本期 credits</dt>
            <dd className="mt-1 font-semibold">
              {usage ? `${usage.credits_remaining} / ${usage.monthly_credits}` : "—"}
              {usage && <span className="ml-2 text-sm font-normal text-[var(--muted)]">至 {dateFormat.format(new Date(usage.period_end))}</span>}
            </dd>
          </div>
        </dl>
      </section>
      <section className="rounded-[2rem] border border-[var(--line)] bg-white p-8">
        <h2 className="text-xl font-bold">修改密碼</h2>
        <form action={changePassword} className="mt-5 max-w-md space-y-4">
          <label className="block text-sm font-semibold">目前密碼<input required type="password" name="current_password" autoComplete="current-password" className={inputClass} /></label>
          <label className="block text-sm font-semibold">新密碼（至少 10 個字元）<input required minLength={10} maxLength={128} type="password" name="new_password" autoComplete="new-password" className={inputClass} /></label>
          <label className="block text-sm font-semibold">確認新密碼<input required minLength={10} maxLength={128} type="password" name="confirm_password" autoComplete="new-password" className={inputClass} /></label>
          {formError && <p role="alert" className="text-sm text-red-700">{formError}</p>}
          {done && <p role="status" className="text-sm text-[var(--teal)]">密碼已更新，下次登入請使用新密碼。</p>}
          <button disabled={busy} className="rounded-xl bg-[var(--teal)] px-6 py-3.5 font-semibold text-white disabled:opacity-50">{busy ? "處理中…" : "更新密碼"}</button>
        </form>
      </section>
    </div>
  );
}
