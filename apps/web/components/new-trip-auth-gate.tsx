"use client";

import { AlertCircle, LogIn } from "lucide-react";
import { Link } from "@/i18n/navigation";
import { useEffect, useState } from "react";
import { ApiError, api } from "@/lib/api";
import { NewTripForm } from "@/components/new-trip-form";

type AuthState = "checking" | "authenticated" | "signed_out" | "unavailable";

export function NewTripAuthGate() {
  const [state, setState] = useState<AuthState>("checking");

  useEffect(() => {
    let active = true;
    api("/auth/me")
      .then(() => { if (active) setState("authenticated"); })
      .catch((reason) => {
        if (!active) return;
        setState(reason instanceof ApiError && reason.status === 401 ? "signed_out" : "unavailable");
      });
    return () => { active = false; };
  }, []);

  if (state === "checking") {
    return <div role="status" className="rounded-[2rem] border border-[var(--line)] bg-white p-8 text-[var(--muted)]">正在確認登入狀態…</div>;
  }
  if (state === "signed_out") {
    return <section className="mx-auto max-w-xl rounded-[2rem] border border-[var(--line)] bg-white p-8 text-center shadow-[var(--shadow-lg)]">
      <LogIn className="mx-auto text-[var(--teal)]" size={36} />
      <h1 className="mt-4 text-3xl font-bold">先登入，再建立你的行程</h1>
      <p className="mt-3 leading-7 text-[var(--muted)]">登入後才能保存旅伴、預算、住宿偏好與每日行程，避免填完才發現無法建立。</p>
      <Link href="/login" className="mt-6 inline-flex rounded-xl bg-[var(--teal)] px-6 py-3 font-semibold text-white">前往登入</Link>
    </section>;
  }
  if (state === "unavailable") {
    return <section role="alert" className="mx-auto max-w-xl rounded-[2rem] border border-red-200 bg-red-50 p-8 text-center text-red-900">
      <AlertCircle className="mx-auto" size={36} />
      <h1 className="mt-4 text-2xl font-bold">目前無法確認登入狀態</h1>
      <p className="mt-3 leading-7">服務暫時異常，請稍後重新整理。系統不會把這種錯誤誤判成登出。</p>
    </section>;
  }
  return <NewTripForm />;
}
