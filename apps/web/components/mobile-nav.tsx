"use client";

import { Menu, X } from "lucide-react";
import Link from "next/link";
import { useEffect, useRef, useState } from "react";

const links = [
  ["首頁", "/"],
  ["熱門景點", "/hotspots"],
  ["我的旅程", "/trips"],
  ["價格通知", "/alerts"],
  ["航班動態", "/flights/status"],
  ["航空票價", "/labs/airlines"],
  ["方案", "/pricing"],
  ["會員帳號", "/account"],
] as const;

export function MobileNav() {
  const [open, setOpen] = useState(false);
  const closeButton = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (!open) return;
    closeButton.current?.focus();
    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") setOpen(false);
    };
    window.addEventListener("keydown", closeOnEscape);
    return () => window.removeEventListener("keydown", closeOnEscape);
  }, [open]);

  return <div className="md:hidden">
    <button type="button" aria-label="開啟導覽選單" aria-expanded={open} aria-controls="mobile-navigation" onClick={() => setOpen(true)} className="rounded-xl border border-[var(--line)] bg-white p-2.5 text-[var(--ink)]"><Menu size={21} /></button>
    {open && <div className="fixed inset-0 z-50 bg-black/30" onMouseDown={() => setOpen(false)}>
      <nav id="mobile-navigation" aria-label="手機主要導覽" onMouseDown={(event) => event.stopPropagation()} className="ml-auto flex h-full w-[min(84vw,22rem)] flex-col bg-white p-5 shadow-2xl">
        <div className="mb-5 flex items-center justify-between"><strong>Travel Scanner</strong><button ref={closeButton} type="button" aria-label="關閉導覽選單" onClick={() => setOpen(false)} className="rounded-xl border border-[var(--line)] p-2"><X size={20} /></button></div>
        <div className="grid gap-2">{links.map(([label, href]) => <Link key={href} href={href} onClick={() => setOpen(false)} className="rounded-xl px-4 py-3 font-semibold text-[var(--ink)] hover:bg-[var(--teal-soft)] focus:bg-[var(--teal-soft)]">{label}</Link>)}</div>
        <Link href="/login" onClick={() => setOpen(false)} className="mt-auto rounded-xl bg-[var(--teal)] px-4 py-3 text-center font-semibold text-white">登入／切換帳號</Link>
      </nav>
    </div>}
  </div>;
}
