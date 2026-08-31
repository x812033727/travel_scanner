"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

type Me = { id: string; email: string; is_admin?: boolean };

const pillClass = "rounded-full border border-[var(--line)] bg-white px-4 py-2 text-[var(--ink)]";

export function HeaderAuth() {
  const router = useRouter();
  const [me, setMe] = useState<Me | null>(null);
  const [ready, setReady] = useState(false);
  useEffect(() => {
    let active = true;
    api<Me>("/auth/me")
      .then((user) => { if (active) setMe(user); })
      .catch(() => { if (active) setMe(null); })
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
  if (!me) return <Link className={pillClass} href="/login">登入</Link>;
  return (
    <span className="flex items-center gap-3">
      {me.is_admin && <Link className="font-semibold text-[var(--teal)]" href="/admin/settings">管理後台</Link>}
      <Link className="hidden max-w-48 truncate text-[var(--ink)] sm:inline" title={me.email} href="/account">{me.email}</Link>
      <button onClick={logout} className={pillClass}>登出</button>
    </span>
  );
}
