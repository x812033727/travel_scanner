"use client";

import { useState } from "react";
import { useFormatter, useTranslations } from "next-intl";
import { api } from "@/lib/api";

export type HotelOptionRow = {
  id: string;
  provider: string;
  url: string | null;
  property_id: string | null;
  evidence_url: string | null;
  identity_note: string;
  discovery_status: string;
  status: string;
  version: number;
  health_status: string;
  verified_at: string | null;
};
const providers = [
  "official",
  "booking",
  "trip_com",
  "agoda",
  "expedia",
  "rakuten",
  "klook",
  "kkday",
];
const field =
  "mt-1 min-h-11 w-full min-w-0 rounded-xl border border-[var(--line)] bg-[var(--surface-raised)] p-3 text-sm";
const button =
  "min-h-11 rounded-xl border border-[var(--line)] px-4 py-2 text-sm font-semibold disabled:opacity-50";

export function HotelOptionsAdmin({
  productId,
  options,
  brands,
  busy,
  run,
}: {
  productId: string;
  options: HotelOptionRow[];
  brands: Record<string, { name: string }>;
  busy: boolean;
  run: (work: () => Promise<unknown>) => Promise<void>;
}) {
  const t = useTranslations("travelServices");
  const fmt = useFormatter();
  const [provider, setProvider] = useState("official");
  const initial = options.find((o) => o.provider === "official");
  const [url, setUrl] = useState(
    options.find((o) => o.provider === "official")?.url || "",
  );
  const [propertyId, setPropertyId] = useState(initial?.property_id || "");
  const [evidence, setEvidence] = useState(
    options.find((o) => o.provider === "official")?.evidence_url || "",
  );
  const [note, setNote] = useState(initial?.identity_note || "");
  const [discovery, setDiscovery] = useState(
    initial?.discovery_status || "found",
  );
  const [browserVerified, setBrowserVerified] = useState(false);
  const current = options.find((o) => o.provider === provider);
  function choose(code: string) {
    const option = options.find((o) => o.provider === code);
    setProvider(code);
    setUrl(option?.url || "");
    setEvidence(option?.evidence_url || "");
    setPropertyId(option?.property_id || "");
    setNote(option?.identity_note || "");
    setDiscovery(option?.discovery_status || "found");
    setBrowserVerified(false);
  }
  function review(status: string) {
    if (!current) return;
    void run(() =>
      api(
        `/admin/travel-services/products/${productId}/booking-options/${current.id}/review`,
        {
          method: "POST",
          body: JSON.stringify({
            version: current.version,
            status,
            identity_note: note,
            browser_verified: browserVerified,
          }),
        },
      ),
    );
  }
  return (
    <details className="mt-4 rounded-xl border border-[var(--line)] p-3">
      <summary className="min-h-11 cursor-pointer py-2 font-semibold">
        {t("platformReview")}
      </summary>
      <p className="mb-3 text-sm text-[var(--muted)]">
        {t("independentReview")}
      </p>
      <ul className="mb-4 space-y-2">
        {providers.map((code) => {
          const option = options.find((o) => o.provider === code);
          return (
            <li
              key={code}
              className="flex flex-wrap items-center justify-between gap-2 border-b border-[var(--line)] py-2 text-sm"
            >
              <button
                type="button"
                className={button}
                onClick={() => choose(code)}
              >
                {code === "official"
                  ? t("officialHotel")
                  : brands[code]?.name || code}
              </button>
              <span>
                {option
                  ? t(
                      option.discovery_status !== "found"
                        ? option.discovery_status
                        : option.status === "disabled"
                          ? "disabledStatus"
                          : option.status,
                    )
                  : t("unconfirmed")}
              </span>
              {option?.verified_at && (
                <time className="text-xs" dateTime={option.verified_at}>
                  {fmt.dateTime(new Date(option.verified_at))}
                </time>
              )}
            </li>
          );
        })}
      </ul>
      <form
        className="space-y-3"
        onSubmit={(event) => {
          event.preventDefault();
          void run(() =>
            api(
              `/admin/travel-services/products/${productId}/booking-options`,
              {
                method: "PUT",
                body: JSON.stringify({
                  provider,
                  version: current?.version || 0,
                  discovery_status: discovery,
                  url: discovery === "found" ? url : null,
                  property_id:
                    discovery === "found" ? propertyId || null : null,
                  evidence_url: evidence || null,
                  identity_note: note,
                }),
              },
            ),
          );
        }}
      >
        <fieldset disabled={busy} className="min-w-0 space-y-3">
          <label className="block">
            {t("bookingProvider")}
            <select
              className={field}
              value={provider}
              onChange={(e) => choose(e.target.value)}
            >
              {providers.map((code) => (
                <option key={code} value={code}>
                  {code === "official"
                    ? t("officialHotel")
                    : brands[code]?.name || code}
                </option>
              ))}
            </select>
          </label>
          <label className="block">
            {t("discoveryStatus")}
            <select
              className={field}
              value={discovery}
              onChange={(e) => setDiscovery(e.target.value)}
            >
              {["found", "not_found", "unconfirmed"].map((s) => (
                <option key={s} value={s}>
                  {t(s)}
                </option>
              ))}
            </select>
          </label>
          {discovery === "found" && (
            <>
              <label className="block">
                {t("hotelPageUrl")}
                <input
                  type="url"
                  required
                  className={field}
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                />
              </label>
              <label className="block">
                {t("platformPropertyId")}
                <input
                  className={field}
                  value={propertyId}
                  onChange={(e) => setPropertyId(e.target.value)}
                />
              </label>
            </>
          )}
          <label className="block">
            {t("hotelLinkEvidence")}
            <input
              type="url"
              required={discovery === "found"}
              className={field}
              value={evidence}
              onChange={(e) => setEvidence(e.target.value)}
            />
          </label>
          <label className="block">
            {t("identityNote")}
            <textarea
              className={field}
              maxLength={1000}
              value={note}
              onChange={(e) => setNote(e.target.value)}
            />
          </label>
          <button className={button} type="submit">
            {t("saveHotelLinks")}
          </button>
        </fieldset>
      </form>
      {current && (
        <div className="mt-4 space-y-3 border-t border-[var(--line)] pt-3">
          {current.url && (
            <a
              href={current.url}
              target="_blank"
              rel="noopener noreferrer"
              className="block min-h-11 break-all py-3 text-sm underline"
              aria-label={`${t("preview")} · ${t("newTab")}`}
            >
              {current.url}
            </a>
          )}
          <p className="text-sm">
            {t("healthStatus")}:{" "}
            {t(
              [
                "healthy",
                "unavailable",
                "unsafe",
                "unchecked",
                "unconfirmed",
              ].includes(current.health_status)
                ? current.health_status
                : "unconfirmed",
            )}
          </p>
          <label className="flex min-h-11 items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={browserVerified}
              onChange={(e) => setBrowserVerified(e.target.checked)}
            />
            {t("browserVerified")}
          </label>
          <div className="flex flex-wrap gap-2">
            <button
              disabled={
                busy || !note.trim() || current.discovery_status !== "found"
              }
              className={button}
              onClick={() => review("approved")}
            >
              {t("verifyOffer")}
            </button>
            <button
              disabled={busy}
              className={button}
              onClick={() => review("disabled")}
            >
              {t("disable")}
            </button>
          </div>
        </div>
      )}
    </details>
  );
}
