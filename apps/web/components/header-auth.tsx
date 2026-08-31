"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { ApiError, api } from "@/lib/api";

type Me = { id: string; email: string; is_admin?: boolean };

const pillClass = "rounded-full border border-[var(--line)] bg-white px-4 py-2 text-[var(--ink)]";

export function HeaderAuth() {
  const router = useRouter();
  const [me, setMe] = useState<Me | null>(null);
  const [ready, setReady] = useState(false);
  const [serviceError, setServiceError] = useState(false);
  useEffect(() => {
    let active = true;
    api<Me>("/auth/me")
      .then((user) => { if (active) setMe(user); })
      .catch((reason) => {
        if (!active) return;
        if (reason instanceof ApiError && reason.status === 401) setMe(null);
        else setServiceError(true);
      })
      .finally(() => { if (active) setReady(true); });
    return () => { active = false; };
  }, []);
  async function logout() {
    try { await api("/auth/logout", { method: "POST" }); } catch { /* BFF 已清除 cookie */ }
    setMe(null);
    router.push("/");
    router.refresh();
  }
  if (!ready) return <span aria-hidden className={`${pillClass} invisible`}>登入</span>;
  if (serviceError) return <span role="status" title="目前無法確認登入狀態，請稍後重試" className={`${pillClass} border-red-200 bg-red-50 text-red-800`}>登入狀態異常</span>;
  if (!me) return <Link className={pillClass} href="/login">登入</Link>;
  return (
    <span className="flex items-center gap-3">
      {me.is_admin && <Link className="font-semibold text-[var(--teal)]" href="/admin/settings">管理後台</Link>}
      <Link className="hidden max-w-48 truncate text-[var(--ink)] sm:inline" title={me.email} href="/account">{me.email}</Link>
      <button onClick={logout} className={pillClass}>登出</button>
    </span>
  );
}
