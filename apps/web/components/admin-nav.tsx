import Link from "next/link";

export function AdminNav({ current }: { current: "users" | "settings" }) {
  const linkClass = (active: boolean) => `rounded-xl px-4 py-2.5 text-sm font-semibold ${active ? "bg-[var(--ink)] text-white" : "hover:bg-[var(--paper)]"}`;
  return <nav aria-label="管理後台功能" className="mt-6 flex flex-wrap gap-2 rounded-2xl border border-[var(--line)] bg-white p-2">
    <Link href="/admin/users" aria-current={current === "users" ? "page" : undefined} className={linkClass(current === "users")}>會員與次數</Link>
    <Link href="/admin/settings" aria-current={current === "settings" ? "page" : undefined} className={linkClass(current === "settings")}>API 與金鑰</Link>
  </nav>;
}
