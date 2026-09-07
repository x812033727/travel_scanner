"use client";
import { useEffect, useState } from "react";
import { useFormatter, useTranslations } from "next-intl";
import { api } from "@/lib/api";

type Occupancy = { adults: number; children_ages: number[] };
export type QuoteResults = {
  status: string;
  providers: { provider: string; status: string }[];
  quotes: {
    provider: string;
    rate_id: string;
    room_name: string;
    bed_description?: string | null;
    meal_description?: string | null;
    cancellation_description?: string | null;
    payment_description?: string | null;
    total: string;
    currency: string;
    taxes: string | null;
    pay_at_property: string | null;
    expires_at: string;
    comparable: boolean;
    lowest_in_group: boolean;
    comparison_group: string | null;
  }[];
};
const brands: Record<string, string> = {
  booking: "Booking.com",
  trip_com: "Trip.com",
  agoda: "Agoda",
  expedia: "Expedia",
  rakuten: "Rakuten Travel",
};
const field =
  "mt-1 min-h-11 w-full min-w-0 rounded-xl border border-[var(--line)] bg-[var(--surface-raised)] p-3 text-sm";
const button =
  "min-h-11 rounded-xl border border-[var(--line)] px-3 py-2 text-sm font-semibold disabled:opacity-50";
export function HotelQuotes({
  productId,
  enabled,
  startDate,
  endDate,
}: {
  productId: string;
  enabled: boolean;
  startDate?: string;
  endDate?: string;
}) {
  const t = useTranslations("travelServices");
  const fmt = useFormatter();
  const [start, setStart] = useState(startDate || "");
  const [end, setEnd] = useState(endDate || "");
  const [rooms, setRooms] = useState<Occupancy[]>([
    { adults: 2, children_ages: [] },
  ]);
  const [currency, setCurrency] = useState("TWD");
  const [country, setCountry] = useState("");
  const [data, setData] = useState<QuoteResults>();
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [now, setNow] = useState(() => Date.now());
  useEffect(() => {
    if (!data?.quotes.length) return;
    const timer = window.setInterval(() => setNow(Date.now()), 1000);
    return () => window.clearInterval(timer);
  }, [data]);
  if (!enabled)
    return (
      <p role="status" className="rounded-xl bg-[var(--paper)] p-3 text-sm">
        {t("quoteNotConfigured")}
      </p>
    );
  const changeRoom = (index: number, patch: Partial<Occupancy>) => {
    setRooms(rooms.map((r, i) => (i === index ? { ...r, ...patch } : r)));
    setData(undefined);
  };
  const quotes =
    data?.quotes.filter((q) => Date.parse(q.expires_at) > now) || [];
  return (
    <section
      aria-label={t("quoteSearch")}
      className="space-y-3 rounded-2xl border border-[var(--line)] p-3"
    >
      <h3 className="font-semibold">{t("quoteSearch")}</h3>
      <form
        className="space-y-3"
        onChange={() => setData(undefined)}
        onSubmit={async (event) => {
          event.preventDefault();
          setBusy(true);
          setError("");
          setData(undefined);
          try {
            const result = await api<QuoteResults>(
              `/travel-services/${productId}/hotel-quotes`,
              {
                method: "POST",
                body: JSON.stringify({
                  check_in: start,
                  check_out: end,
                  rooms,
                  currency,
                  booker_country: country,
                }),
              },
            );
            setData(result);
            setNow(Date.now());
          } catch (e) {
            setError((e as Error).message);
          } finally {
            setBusy(false);
          }
        }}
      >
        <fieldset disabled={busy} className="min-w-0 space-y-3">
          <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
            <label>
              {t("quoteCheckIn")}
              <input
                className={field}
                type="date"
                required
                value={start}
                onChange={(e) => setStart(e.target.value)}
              />
            </label>
            <label>
              {t("quoteCheckOut")}
              <input
                className={field}
                type="date"
                required
                min={start}
                value={end}
                onChange={(e) => setEnd(e.target.value)}
              />
            </label>
          </div>
          {rooms.map((room, i) => (
            <fieldset
              key={i}
              className="min-w-0 rounded-xl border border-[var(--line)] p-3"
            >
              <legend className="px-1">
                {t("quoteRoom", { number: i + 1 })}
              </legend>
              <label>
                {t("quoteAdults")}
                <input
                  className={field}
                  type="number"
                  required
                  min={1}
                  max={10}
                  value={room.adults}
                  onChange={(e) =>
                    changeRoom(i, { adults: Number(e.target.value) })
                  }
                />
              </label>
              {room.children_ages.map((age, j) => (
                <label className="mt-2 block" key={j}>
                  {t("quoteChildAge", { number: j + 1 })}
                  <input
                    type="number"
                    required
                    min={0}
                    max={17}
                    className={field}
                    value={age}
                    onChange={(e) =>
                      changeRoom(i, {
                        children_ages: room.children_ages.map((a, k) =>
                          k === j ? Number(e.target.value) : a,
                        ),
                      })
                    }
                  />
                </label>
              ))}
              <div className="mt-2 flex flex-wrap gap-2">
                <button
                  type="button"
                  className={button}
                  disabled={room.children_ages.length >= 10}
                  onClick={() =>
                    changeRoom(i, { children_ages: [...room.children_ages, 0] })
                  }
                >
                  {t("quoteAddChild")}
                </button>
                <button
                  type="button"
                  className={button}
                  disabled={!room.children_ages.length}
                  onClick={() =>
                    changeRoom(i, {
                      children_ages: room.children_ages.slice(0, -1),
                    })
                  }
                >
                  {t("quoteRemoveChild")}
                </button>
              </div>
            </fieldset>
          ))}
          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              className={button}
              disabled={rooms.length >= 10}
              onClick={() => {
                setRooms([...rooms, { adults: 2, children_ages: [] }]);
                setData(undefined);
              }}
            >
              {t("quoteAddRoom")}
            </button>
            <button
              type="button"
              className={button}
              disabled={rooms.length === 1}
              onClick={() => {
                setRooms(rooms.slice(0, -1));
                setData(undefined);
              }}
            >
              {t("quoteRemoveRoom")}
            </button>
          </div>
          <label className="block">
            {t("quoteCurrency")}
            <select
              className={field}
              value={currency}
              onChange={(e) => setCurrency(e.target.value)}
            >
              {["TWD", "JPY", "KRW", "USD", "EUR", "CNY"].map((c) => (
                <option key={c}>{c}</option>
              ))}
            </select>
          </label>
          <label className="block">
            {t("quoteCountry")}
            <input
              className={field}
              required
              pattern="[A-Z]{2}"
              maxLength={2}
              value={country}
              onChange={(e) => setCountry(e.target.value.toUpperCase())}
            />
          </label>
          <button
            className={`${button} w-full bg-[var(--teal)] text-white`}
            type="submit"
          >
            {busy ? t("loading") : t("quoteSearch")}
          </button>
        </fieldset>
      </form>
      {error && <p role="alert">{error}</p>}
      {data && <p role="status">{t(`quoteState.${data.status}`)}</p>}
      {data && (
        <ul
          className="text-xs text-[var(--muted)]"
          aria-label={t("quoteProviderStatus")}
        >
          {data.providers.map((p) => (
            <li key={p.provider}>
              {brands[p.provider] || p.provider} ·{" "}
              {t(`quoteProviderState.${p.status}`)}
            </li>
          ))}
        </ul>
      )}
      {data?.quotes.length && !quotes.length ? (
        <p role="status">{t("quoteExpired")}</p>
      ) : null}
      {quotes.map((q) => (
        <article
          key={`${q.provider}:${q.rate_id}`}
          className="rounded-xl bg-[var(--paper)] p-3 text-sm"
        >
          <h4 className="break-words font-semibold">
            {brands[q.provider] || q.provider} · {q.room_name}
          </h4>
          <p className="mt-2 text-lg font-bold">
            {fmt.number(Number(q.total), {
              style: "currency",
              currency: q.currency,
            })}
          </p>
          <p>{t("quoteTotal")}</p>
          <dl className="my-3 space-y-2 break-words">
            {(["bed", "meal", "cancellation", "payment"] as const).map(
              (key) => (
                <div key={key}>
                  <dt className="font-semibold">{t(`quoteTerms.${key}`)}</dt>
                  <dd>{q[`${key}_description`] || t("unknown")}</dd>
                </div>
              ),
            )}
          </dl>
          <p>
            {t("quoteTaxes")}:{" "}
            {q.taxes === null
              ? t("unknown")
              : fmt.number(Number(q.taxes), {
                  style: "currency",
                  currency: q.currency,
                })}
          </p>
          <p>
            {t("quotePayAtProperty")}:{" "}
            {q.pay_at_property === null
              ? t("unknown")
              : fmt.number(Number(q.pay_at_property), {
                  style: "currency",
                  currency: q.currency,
                })}
          </p>
          <p className="mt-2">
            {q.comparison_group &&
            new Set(
              quotes
                .filter((p) => p.comparison_group === q.comparison_group)
                .map((p) => p.provider),
            ).size >= 2 &&
            Number(q.total) ===
              Math.min(
                ...quotes
                  .filter((p) => p.comparison_group === q.comparison_group)
                  .map((p) => Number(p.total)),
              )
              ? t("quoteLowest")
              : t("quoteDifferent")}
          </p>
          <time dateTime={q.expires_at}>
            {t("quoteValidUntil", {
              time: fmt.dateTime(new Date(q.expires_at), {
                hour: "2-digit",
                minute: "2-digit",
              }),
            })}
          </time>
        </article>
      ))}
    </section>
  );
}
