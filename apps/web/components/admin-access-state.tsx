import { ShieldAlert, Unplug } from "lucide-react";
import { Link } from "@/i18n/navigation";
import { adminOperationsCopy } from "@/lib/admin-operations-copy";

export function AdminAccessState({ locale, status }: { locale: string; status: "forbidden" | "unavailable" }) {
  const copy = adminOperationsCopy(locale);
  const Icon = status === "forbidden" ? ShieldAlert : Unplug;
  return <main className="mx-auto grid min-h-[70dvh] max-w-2xl place-items-center px-5 py-16">
    <section className="w-full rounded-[2rem] border border-[var(--line)] bg-[var(--surface)] p-8 text-center shadow-[var(--shadow-md)] md:p-12">
      <span className="mx-auto grid size-14 place-items-center rounded-2xl bg-[var(--coral-soft)] text-[var(--coral)]"><Icon aria-hidden size={28} /></span>
      <h1 className="mt-6 text-2xl font-black md:text-3xl">{status === "forbidden" ? copy.forbiddenTitle : copy.serviceTitle}</h1>
      <p className="mx-auto mt-3 max-w-lg leading-7 text-[var(--muted)]">{status === "forbidden" ? copy.forbiddenBody : copy.serviceBody}</p>
      <Link href={status === "forbidden" ? "/" : "/admin"} className="mt-7 inline-flex min-h-12 items-center justify-center rounded-2xl bg-[var(--ink)] px-6 font-bold text-white">{status === "forbidden" ? copy.nav.dashboard : copy.retry}</Link>
    </section>
  </main>;
}
