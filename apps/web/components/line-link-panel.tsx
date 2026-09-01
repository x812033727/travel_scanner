"use client";

import { CheckCircle2, LoaderCircle } from "lucide-react";
import { Link } from "@/i18n/navigation";
import { useState } from "react";
import { ApiError, api } from "@/lib/api";
import { loginPath } from "@/lib/navigation";

export function LineLinkPanel({ linkToken }: { linkToken?: string }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>();

  async function linkAccount() {
    if (!linkToken) return;
    setLoading(true);
    setError(undefined);
    try {
      const result = await api<{ redirect_url: string }>("/line/link-session", {
        method: "POST",
        body: JSON.stringify({ link_token: linkToken }),
      });
      window.location.assign(result.redirect_url);
    } catch (reason) {
      if (reason instanceof ApiError && reason.status === 401) return;
      setError((reason as Error).message);
      setLoading(false);
    }
  }

  if (!linkToken) {
    return <p role="alert" className="rounded-xl bg-amber-50 p-4 text-amber-900">連結已失效。請回到 LINE 官方帳號重新輸入「綁定」。</p>;
  }
  const returnPath = `/line/link?linkToken=${encodeURIComponent(linkToken)}`;
  return <div className="space-y-4">
    <p className="flex gap-3 text-sm text-[var(--muted)]"><CheckCircle2 className="shrink-0 text-[var(--teal)]" size={20} />確認後，這個網站帳號會與目前的 LINE 帳號一對一連結，用來接收到價通知。</p>
    <button type="button" disabled={loading} onClick={linkAccount} className="flex w-full items-center justify-center gap-2 rounded-xl bg-[#06c755] px-4 py-3 font-semibold text-white disabled:opacity-60">{loading && <LoaderCircle className="animate-spin" size={18} />}確認連結 LINE</button>
    <Link href={loginPath(returnPath)} className="block text-center text-sm text-[var(--teal)] underline">尚未登入？先登入網站帳號</Link>
    {error && <p role="alert" className="rounded-xl bg-red-50 p-3 text-sm text-red-800">{error}</p>}
  </div>;
}
