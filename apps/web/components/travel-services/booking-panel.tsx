"use client";

import { ExternalLink, X } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useCallback, useEffect, useId, useRef, useState } from "react";
import { useModalSheet } from "@/lib/modal-sheet";
import type { HotelBookingPlacement } from "@/lib/hotel-booking-placement";
import { stay22AllezCopy, stay22AllezText } from "@/lib/stay22-allez-copy";
import { useStay22BookingContext, type BookingContext } from "@/lib/stay22-booking-context";
import type { Product } from "./catalog";
import { HotelQuotes } from "./hotel-quotes";

export type BookingOption = {
  id: string;
  provider: string;
  name: string | null;
  mode: "direct" | "affiliate";
  affiliate_channel?: "existing" | "stay22" | null;
  quote_status: string;
};
export type SourceCredit = {
  title: string;
  publisher: string;
  url: string;
  license_name: string;
  license_url: string;
  changes: string;
};

export function SourceCredits({ credits }: { credits?: SourceCredit[] }) {
  const t = useTranslations("travelServices");
  if (!credits?.length) return null;
  return (
    <details className="mt-3 text-xs text-[var(--muted)]">
      <summary className="min-h-11 cursor-pointer py-3">
        {t("sourceCredits")}
      </summary>
      <ul className="space-y-3">
        {credits.map((credit, i) => (
          <li key={`${credit.url}:${i}`} className="break-words">
            <a
              className="underline"
              href={credit.url}
              target="_blank"
              rel="noopener noreferrer"
              aria-label={`${credit.title} · ${t("newTab")}`}
            >
              {credit.title}
            </a>
            <p>
              {credit.publisher} ·{" "}
              <a
                className="underline"
                href={credit.license_url}
                target="_blank"
                rel="noopener noreferrer"
                aria-label={`${credit.license_name} · ${t("newTab")}`}
              >
                {credit.license_name}
              </a>
            </p>
            <p>{credit.changes}</p>
          </li>
        ))}
      </ul>
    </details>
  );
}

export function BookingPanel({
  product,
  startDate,
  endDate,
  bookingContext,
  placement,
  onClose,
}: {
  product: Product;
  startDate?: string;
  endDate?: string;
  bookingContext?: BookingContext | null;
  placement: HotelBookingPlacement;
  onClose: () => void;
}) {
  const t = useTranslations("travelServices");
  const common = useTranslations("common");
  const locale = useLocale();
  const copy = stay22AllezCopy(locale);
  const inheritedContext = useStay22BookingContext();
  const context = bookingContext ?? inheritedContext;
  // Preserve the saved trip dates, even if invalid/past, for explicit correction.
  const [checkIn, setCheckIn] = useState(context?.check_in ?? startDate ?? "");
  const [checkOut, setCheckOut] = useState(context?.check_out ?? endDate ?? "");
  const [adults, setAdults] = useState(context?.adults == null ? "" : String(context.adults));
  const [children, setChildren] = useState(context?.children == null ? "" : String(context.children));
  const [omitDates, setOmitDates] = useState(false);
  const [quotesOpen, setQuotesOpen] = useState(false);
  const validDate = (value: string) => /^\d{4}-\d{2}-\d{2}$/.test(value) && !Number.isNaN(Date.parse(value)) && new Date(value).toISOString().slice(0, 10) === value;
  const now = new Date();
  const today = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}-${String(now.getDate()).padStart(2, "0")}`;
  const dateError = omitDates || (!checkIn && !checkOut) ? ""
    : !validDate(checkIn) || !validDate(checkOut) || checkOut <= checkIn ? copy.invalidDates
    : checkIn < today ? copy.pastDates : "";
  const guestError = (adults !== "" && (!/^\d+$/.test(adults) || Number(adults) < 1 || Number(adults) > 9)) || (children !== "" && (!/^\d+$/.test(children) || Number(children) > 9)) ? copy.invalidGuests : "";
  const formError = dateError || guestError;
  const id = useId();
  const onCloseRef = useRef(onClose);
  const touch = useRef<number | undefined>(undefined);
  useEffect(() => {
    onCloseRef.current = onClose;
  }, [onClose]);
  const close = useCallback(() => {
    if (window.history.state?.hotelBooking === id) window.history.back();
    else onCloseRef.current();
  }, [id]);
  const ref = useModalSheet<HTMLDivElement>(true, close);
  useEffect(() => {
    const previous = window.history.state;
    const url = window.location.href;
    window.history.pushState({ ...previous, hotelBooking: id }, "");
    const back = () => {
      if (window.history.state?.hotelBooking !== id) onCloseRef.current();
    };
    // The parent catalog may itself be a sheet; Escape closes only this top sheet.
    const escape = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        event.preventDefault();
        event.stopImmediatePropagation();
        close();
      }
    };
    window.addEventListener("popstate", back);
    window.addEventListener("keydown", escape, true);
    return () => {
      window.removeEventListener("popstate", back);
      window.removeEventListener("keydown", escape, true);
      if (
        window.history.state?.hotelBooking === id &&
        window.location.href === url
      )
        window.history.replaceState(previous, "", url);
    };
  }, [id, close]);
  const options = product.booking_options || [];
  const areaOffers = product.offers.filter(
    (offer) => offer.scope === "destination",
  );
  return (
    <div
      className="fixed inset-0 z-[1200] bg-black/45 md:flex md:justify-end"
      onMouseDown={(event) => {
        if (event.target === event.currentTarget) close();
      }}
    >
      <div
        ref={ref}
        role="dialog"
        aria-modal="true"
        aria-labelledby={id}
        className="flex h-dvh w-full min-w-0 flex-col bg-[var(--surface-raised)] shadow-2xl md:max-w-lg"
      >
        <header
          className="shrink-0 border-b border-[var(--line)] px-5 pb-4 pt-[max(1rem,env(safe-area-inset-top))]"
          onTouchStart={(e) => {
            touch.current = e.touches[0].clientY;
          }}
          onTouchEnd={(e) => {
            if (
              touch.current != null &&
              e.changedTouches[0].clientY - touch.current > 100
            )
              close();
          }}
        >
          <div className="flex items-start justify-between gap-3">
            <div className="min-w-0">
              <p className="text-sm text-[var(--muted)]">{t("platforms")}</p>
              <h2 id={id} className="break-words text-xl font-bold">
                {product.title}
              </h2>
            </div>
            <button
              type="button"
              className="flex min-h-11 min-w-11 items-center justify-center rounded-xl border border-[var(--line)]"
              aria-label={common("close")}
              onClick={close}
            >
              <X size={20} />
            </button>
          </div>
          <p className="mt-1 text-xs text-[var(--muted)]">
            {t("conditionsAtPlatform")}
          </p>
        </header>
        <div className="min-h-0 flex-1 space-y-4 overflow-y-auto overscroll-contain p-5">
          <fieldset className="min-w-0 space-y-3 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4">
            <legend className="px-1 font-semibold">{copy.conditions}</legend>
            <p className="text-xs text-[var(--muted)]">{copy.optional}</p>
            <div className="grid min-w-0 grid-cols-1 gap-3 sm:grid-cols-2">
              <label className="min-w-0 text-sm">{copy.checkIn}<input type="date" value={checkIn} disabled={omitDates} aria-invalid={Boolean(dateError)} aria-describedby={dateError ? `${id}-error` : undefined} onChange={(event) => setCheckIn(event.target.value)} className="mt-1 min-h-11 w-full min-w-0 rounded-xl border border-[var(--line)] bg-[var(--surface-raised)] p-3 disabled:opacity-50" /></label>
              <label className="min-w-0 text-sm">{copy.checkOut}<input type="date" value={checkOut} disabled={omitDates} aria-invalid={Boolean(dateError)} aria-describedby={dateError ? `${id}-error` : undefined} onChange={(event) => setCheckOut(event.target.value)} className="mt-1 min-h-11 w-full min-w-0 rounded-xl border border-[var(--line)] bg-[var(--surface-raised)] p-3 disabled:opacity-50" /></label>
              <label className="min-w-0 text-sm">{copy.adults}<input type="number" inputMode="numeric" min={1} max={9} step={1} value={adults} aria-invalid={Boolean(guestError)} aria-describedby={guestError ? `${id}-error` : undefined} onChange={(event) => setAdults(event.target.value)} className="mt-1 min-h-11 w-full min-w-0 rounded-xl border border-[var(--line)] bg-[var(--surface-raised)] p-3" /></label>
              <label className="min-w-0 text-sm">{copy.children}<input type="number" inputMode="numeric" min={0} max={9} step={1} value={children} aria-invalid={Boolean(guestError)} aria-describedby={guestError ? `${id}-error` : undefined} onChange={(event) => setChildren(event.target.value)} className="mt-1 min-h-11 w-full min-w-0 rounded-xl border border-[var(--line)] bg-[var(--surface-raised)] p-3" /></label>
            </div>
            <label className="flex min-h-11 cursor-pointer items-center gap-2 text-sm"><input type="checkbox" checked={omitDates} onChange={(event) => setOmitDates(event.target.checked)} />{copy.omitDates}</label>
            {formError && <p id={`${id}-error`} role="alert" className="text-sm text-[var(--coral)]">{formError}</p>}
            {context?.rooms != null && <p className="text-xs">{stay22AllezText(copy.rooms, { rooms: context.rooms })}</p>}
            {!!context?.children_ages?.length && <p className="text-xs">{stay22AllezText(copy.ages, { ages: context.children_ages.join(", ") })}</p>}
            <p className="text-xs text-[var(--muted)]">{copy.confirmOccupancy}</p>
          </fieldset>
          {!options.length && <p>{copy.noExactLink}</p>}
          {options.map((option) => {
            const name =
              option.provider === "official" ? t("officialHotel") : option.name || option.provider;
            return (
              <form
                key={option.id}
                action={`/api/travel/travel-services/${product.id}/booking-options/${option.id}/clickout?locale=${locale}&placement=${placement}`}
                method="post"
                target="_blank"
                rel="noopener"
                onSubmit={(event) => {
                  if (formError) {
                    event.preventDefault();
                    ref.current?.querySelector<HTMLInputElement>('[aria-invalid="true"]')?.focus();
                    return;
                  }
                  // BFF-only error recovery hint; the BFF validates it and never forwards it to a partner.
                  const action = new URL(event.currentTarget.action, window.location.origin);
                  action.searchParams.set("return_to", `${window.location.pathname}${window.location.search}`);
                  event.currentTarget.action = `${action.pathname}${action.search}`;
                }}
              >
                {!omitDates && checkIn && <input type="hidden" aria-hidden="true" name="check_in" value={checkIn} />}
                {!omitDates && checkOut && <input type="hidden" aria-hidden="true" name="check_out" value={checkOut} />}
                {adults !== "" && <input type="hidden" aria-hidden="true" name="adults" value={adults} />}
                {children !== "" && <input type="hidden" aria-hidden="true" name="children" value={children} />}
                <button
                  type="submit"
                  className="flex min-h-16 w-full items-center justify-between gap-3 rounded-2xl border border-[var(--line)] bg-[var(--surface-raised)] p-4 text-left hover:bg-[var(--paper)] focus-visible:outline-2 focus-visible:outline-[var(--teal)]"
                  aria-label={`${stay22AllezText(copy.openPlatform, { platform: name })} · ${t("newTab")}`}
                >
                  <span className="min-w-0 break-words">
                    <strong className="block">{name}</strong>
                    <span className="text-sm text-[var(--muted)]">
                      {stay22AllezText(copy.openPlatform, { platform: name })}
                    </span>
                    {option.affiliate_channel === "stay22" && <span className="mt-1 block text-xs font-semibold text-[var(--teal)]">{copy.viaStay22}</span>}
                  </span>
                  <ExternalLink size={18} className="shrink-0" />
                </button>
              </form>
            );
          })}
          {options.length > 0 && <p className="text-xs text-[var(--muted)]">{copy.directConditions}</p>}
          {options.some((o) => o.quote_status === "ready") && <details onToggle={(event) => setQuotesOpen(event.currentTarget.open)} className="rounded-2xl border border-[var(--line)] p-4">
            <summary tabIndex={0} className="min-h-11 cursor-pointer py-3 font-semibold">{copy.quotesTitle}</summary>
            <p className="mb-3 text-xs text-[var(--muted)]">{copy.quotesNote}</p>
            {quotesOpen && <HotelQuotes productId={product.id} enabled startDate={startDate} endDate={endDate} />}
          </details>}
          {areaOffers.length > 0 && (
            <section className="space-y-3 border-t border-[var(--line)] pt-4">
              <h3 className="font-semibold">{t("destinationScope")}</h3>
              {areaOffers.map((offer) => (
                <form
                  key={offer.id}
                  method="post"
                  target="_blank"
                  rel="noopener"
                  action={`/api/travel/affiliates/offers/${offer.id}/clickout?locale=${locale}&placement=${placement}`}
                >
                  <button
                    type="submit"
                    className="flex min-h-11 w-full items-center justify-between gap-2 rounded-xl border border-[var(--line)] p-3 text-left"
                    aria-label={`${offer.brand_name} · ${t("destinationScope")} · ${t("newTab")}`}
                  >
                    <span>
                      {offer.brand_name} · {t("destinationScope")}
                    </span>
                    <ExternalLink size={18} className="shrink-0" />
                  </button>
                </form>
              ))}
            </section>
          )}
          <SourceCredits credits={product.facts.source_credits} />
        </div>
        <footer className="shrink-0 border-t border-[var(--line)] px-5 pt-3 pb-[max(1rem,env(safe-area-inset-bottom))] text-xs text-[var(--muted)]">
          <p>
            {options.some((o) => o.mode === "affiliate") ||
            areaOffers.length > 0
              ? copy.disclosure
              : t("directDisclosure")}
          </p>
        </footer>
      </div>
    </div>
  );
}
