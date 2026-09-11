"use client";

import { useEffect, useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import { api, ApiError } from "@/lib/api";
import { stay22AllezCopy } from "@/lib/stay22-allez-copy";
import { BookingPanel } from "./booking-panel";
import type { Product } from "./catalog";

type State =
  | { status: "loading" | "unavailable" | "error" }
  | { status: "ready"; product: Product };

export function HotelBookingPage({ productId }: { productId: string }) {
  const locale = useLocale();
  return <HotelBookingContent key={`${locale}:${productId}`} productId={productId} locale={locale} />;
}

function HotelBookingContent({ productId, locale }: { productId: string; locale: string }) {
  const t = useTranslations("travelServices");
  const copy = stay22AllezCopy(locale);
  const [state, setState] = useState<State>({ status: "loading" });
  const [attempt, setAttempt] = useState(0);
  const [open, setOpen] = useState(true);
  useEffect(() => {
    const abort = new AbortController();
    api<Product>(`/travel-services/${encodeURIComponent(productId)}/booking-details`, { signal: abort.signal })
      .then((product) => {
        if (abort.signal.aborted) return;
        if (product?.kind !== "hotel" || product.id !== productId ||
            typeof product.title !== "string" || typeof product.destination_id !== "string" ||
            !product.destination_id || !product.facts || !Array.isArray(product.offers)) {
          setState({ status: "unavailable" });
          return;
        }
        setState({ status: "ready", product });
      })
      .catch((error: unknown) => {
        if (!abort.signal.aborted) setState({ status: error instanceof ApiError && error.status === 404 ? "unavailable" : "error" });
      });
    return () => abort.abort();
  }, [productId, attempt]);

  const product = state.status === "ready" ? state.product : null;
  const catalog = product
    ? `/${encodeURIComponent(locale)}/destinations/${encodeURIComponent(product.destination_id)}/services?type=hotel`
    : `/${encodeURIComponent(locale)}/destinations`;
  return <main className="mx-auto min-h-[60dvh] max-w-3xl space-y-5 px-5 py-8">
    <h1 className="break-words text-2xl font-bold">{product?.title || t("hotel")}</h1>
    {state.status === "loading" && <p role="status">{t("loading")}</p>}
    {state.status === "unavailable" && <p role="status">{t("noOffers")}</p>}
    {state.status === "error" && <div className="space-y-3">
      <p role="alert">{copy.errorTitle}</p>
      <button type="button" className="min-h-11 rounded-xl border border-[var(--line)] px-4 py-2" onClick={() => { setState({ status: "loading" }); setAttempt((value) => value + 1); }}>{t("retry")}</button>
    </div>}
    {product && <>
      <p className="text-sm text-[var(--muted)]">{t("conditionsAtPlatform")}</p>
      <button type="button" className="min-h-11 rounded-xl border border-[var(--line)] px-4 py-2 font-semibold" onClick={() => setOpen(true)}>{t("platforms")}</button>
    </>}
    {/* Native navigation discards this date draft before returning to a possible SDK document. */}
    <a href={catalog} className="flex min-h-11 w-fit items-center rounded-xl px-1 py-2 text-[var(--teal)] underline">{copy.back}</a>
    {product && open && <BookingPanel product={product} bookingContext={{}} placement="destination" onClose={() => setOpen(false)} />}
  </main>;
}
