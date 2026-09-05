"use client";

import { AlertCircle, LogIn } from "lucide-react";
import { Link } from "@/i18n/navigation";
import { useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { ApiError, api } from "@/lib/api";
import { loginPath } from "@/lib/navigation";
import { NewTripForm } from "@/components/new-trip-form";

type AuthState = "checking" | "authenticated" | "signed_out" | "unavailable";

export function NewTripAuthGate() {
  const t = useTranslations("newTrip.gate");
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
    return <div role="status" className="rounded-[2rem] border border-[var(--line)] bg-white p-8 text-[var(--muted)]">{t("checking")}</div>;
  }
  if (state === "signed_out") {
    return <section className="mx-auto max-w-xl rounded-[2rem] border border-[var(--line)] bg-white p-8 text-center shadow-[var(--shadow-lg)]">
      <LogIn className="mx-auto text-[var(--teal)]" size={36} />
      <h1 className="mt-4 text-3xl font-bold">{t("signInTitle")}</h1>
      <p className="mt-3 leading-7 text-[var(--muted)]">{t("signInBody")}</p>
      {/* Every other sign-in entry carries `next`; without it the member lands on the
          home page after signing in and has to find this page again. */}
      <Link href={loginPath("/trips/new")} className="mt-6 inline-flex rounded-xl bg-[var(--teal)] px-6 py-3 font-semibold text-white">{t("signIn")}</Link>
    </section>;
  }
  if (state === "unavailable") {
    return <section role="alert" className="mx-auto max-w-xl rounded-[2rem] border border-red-200 bg-red-50 p-8 text-center text-red-900">
      <AlertCircle className="mx-auto" size={36} />
      <h1 className="mt-4 text-2xl font-bold">{t("unavailableTitle")}</h1>
      <p className="mt-3 leading-7">{t("unavailableBody")}</p>
    </section>;
  }
  return <NewTripForm />;
}
