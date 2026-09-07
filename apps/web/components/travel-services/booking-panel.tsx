"use client";

import { ExternalLink, X } from "lucide-react";
import { useFormatter, useLocale, useTranslations } from "next-intl";
import { useCallback, useEffect, useId, useRef } from "react";
import { useModalSheet } from "@/lib/modal-sheet";
import type { Product } from "./catalog";
import { HotelQuotes } from "./hotel-quotes";

export type BookingOption = {
  id: string;
  provider: string;
  name: string | null;
  mode: "direct" | "affiliate";
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
  placement,
  onClose,
}: {
  product: Product;
  startDate?: string;
  endDate?: string;
  placement: string;
  onClose: () => void;
}) {
  const t = useTranslations("travelServices");
  const common = useTranslations("common");
  const locale = useLocale();
  const fmt = useFormatter();
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
          <p className="mt-3 text-sm">
            {startDate && endDate
              ? `${fmt.dateTime(new Date(`${startDate}T12:00:00Z`), { dateStyle: "medium", timeZone: "UTC" })} — ${fmt.dateTime(new Date(`${endDate}T12:00:00Z`), { dateStyle: "medium", timeZone: "UTC" })}`
              : t("datesAtPlatform")}
          </p>
          <p className="mt-1 text-xs text-[var(--muted)]">
            {t("conditionsAtPlatform")}
          </p>
        </header>
        <div className="min-h-0 flex-1 space-y-4 overflow-y-auto overscroll-contain p-5">
          <HotelQuotes
            productId={product.id}
            enabled={options.some((o) => o.quote_status === "ready")}
            startDate={startDate}
            endDate={endDate}
          />
          {!options.length && <p>{t("noOffers")}</p>}
          {options.map((option) => {
            const name =
              option.provider === "official" ? t("officialHotel") : option.name;
            return (
              <form
                key={option.id}
                action={`/api/travel/travel-services/${product.id}/booking-options/${option.id}/clickout?locale=${locale}&placement=${placement}`}
                method="post"
                target="_blank"
                rel="noopener noreferrer"
              >
                <button
                  type="submit"
                  className="flex min-h-16 w-full items-center justify-between gap-3 rounded-2xl border border-[var(--line)] bg-[var(--surface-raised)] p-4 text-left hover:bg-[var(--paper)] focus-visible:outline-2 focus-visible:outline-[var(--teal)]"
                  aria-label={`${name} · ${t("checkPlatformPrice")} · ${t("newTab")}`}
                >
                  <span className="min-w-0 break-words">
                    <strong className="block">{name}</strong>
                    <span className="text-sm text-[var(--muted)]">
                      {t("checkPlatformPrice")}
                    </span>
                  </span>
                  <ExternalLink size={18} className="shrink-0" />
                </button>
              </form>
            );
          })}
          {areaOffers.length > 0 && (
            <section className="space-y-3 border-t border-[var(--line)] pt-4">
              <h3 className="font-semibold">{t("destinationScope")}</h3>
              {areaOffers.map((offer) => (
                <form
                  key={offer.id}
                  method="post"
                  target="_blank"
                  rel="noopener noreferrer"
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
              ? t("disclosure")
              : t("directDisclosure")}
          </p>
        </footer>
      </div>
    </div>
  );
}
