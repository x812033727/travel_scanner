"use client";

import {
  CloudRain,
  CloudSun,
  Droplets,
  RefreshCw,
  Snowflake,
  Sun,
  Umbrella,
  Wind,
} from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { api, ApiError } from "@/lib/api";

type Condition = { description: string; type: string };
type CurrentWeather = {
  observed_at: string;
  is_daytime: boolean;
  condition: Condition;
  temperature_c: number;
  feels_like_c: number;
  relative_humidity_percent?: number | null;
  precipitation_probability_percent?: number | null;
  wind_speed_kph?: number | null;
  uv_index?: number | null;
};
type DailyWeather = {
  date: string;
  condition: Condition;
  min_temperature_c: number;
  max_temperature_c: number;
  relative_humidity_percent?: number | null;
  precipitation_probability_percent?: number | null;
  precipitation_mm?: number | null;
  wind_speed_kph?: number | null;
  uv_index?: number | null;
};
type TripWeather = {
  attribution: string;
  location_name: string;
  current?: CurrentWeather | null;
  days: DailyWeather[];
  retrieved_at: string;
  cache_status: "fresh" | "hit";
  warnings: string[];
};

function WeatherIcon({ type, size = 20, className = "" }: { type: string; size?: number; className?: string }) {
  if (/SNOW|ICE|SLEET/.test(type)) return <Snowflake size={size} className={className} aria-hidden="true" />;
  if (/RAIN|SHOWER|THUNDER/.test(type)) return <CloudRain size={size} className={className} aria-hidden="true" />;
  if (/CLEAR|SUNNY/.test(type)) return <Sun size={size} className={className} aria-hidden="true" />;
  return <CloudSun size={size} className={className} aria-hidden="true" />;
}

function dayLabel(value: string, locale: string) {
  return new Intl.DateTimeFormat(locale, {
    month: "numeric",
    day: "numeric",
    weekday: "short",
    timeZone: "UTC",
  }).format(new Date(`${value}T00:00:00Z`));
}

function valueOrDash(value?: number | null, suffix = "") {
  return value == null ? "—" : `${Math.round(value)}${suffix}`;
}

/** A chance of rain when the source gives one, otherwise the forecast amount. */
function rainValue(day: DailyWeather) {
  if (day.precipitation_probability_percent != null) return valueOrDash(day.precipitation_probability_percent, "%");
  if (day.precipitation_mm != null) return `${day.precipitation_mm} mm`;
  return "—";
}

export function TripWeatherPanel({
  tripId,
  activeDay,
}: {
  tripId: string;
  activeDay: string;
}) {
  const [weather, setWeather] = useState<TripWeather>();
  const [error, setError] = useState<{ message: string; code?: string }>();
  const [attempt, setAttempt] = useState(0);
  const t = useTranslations("trips.weather");
  const locale = useLocale();

  useEffect(() => {
    let active = true;
    api<TripWeather>(`/trips/${tripId}/weather`)
      .then((result) => {
        if (!active) return;
        if (!Array.isArray(result.days)) throw new Error(t("malformed"));
        setWeather(result);
      })
      .catch((reason: unknown) => {
        if (!active) return;
        setError({
          message: reason instanceof Error ? reason.message : t("unavailable"),
          code: reason instanceof ApiError ? reason.code : undefined,
        });
      })
    return () => {
      active = false;
    };
  }, [attempt, tripId, t]);

  if (!weather && !error) {
    return (
      <section aria-label={t("title")} className="mb-5 animate-pulse rounded-2xl border border-[var(--line)] bg-white p-4">
        <div className="h-4 w-28 rounded bg-slate-100" />
        <div className="mt-3 h-16 rounded-xl bg-slate-100" />
      </section>
    );
  }

  if (error) {
    const notConfigured = error.code === "weather_not_configured" || error.code === "weather_api_not_enabled";
    return (
      <section aria-label={t("title")} className="mb-5 flex items-center justify-between gap-4 rounded-2xl border border-[var(--line)] bg-white p-4">
        <div>
          <p className="text-sm font-bold">{notConfigured ? t("notConfigured") : t("loadFailed")}</p>
          <p className="mt-1 text-xs leading-5 text-[var(--muted)]">{error.message}</p>
        </div>
        {!notConfigured && (
          <button type="button" onClick={() => { setWeather(undefined); setError(undefined); setAttempt((value) => value + 1); }} className="flex min-h-11 shrink-0 items-center gap-1.5 rounded-xl border border-[var(--line)] px-3 text-sm font-semibold">
            <RefreshCw size={15} />{t("retry")}
          </button>
        )}
      </section>
    );
  }

  if (!weather) return null;
  const activeForecast = weather.days.find((day) => day.date === activeDay);

  return (
    <section aria-label={t("title")} className="mb-5 overflow-hidden rounded-2xl border border-sky-100 bg-[linear-gradient(135deg,#f8fcff,#eef8f8)] p-4 shadow-sm sm:p-5">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-xs font-semibold tracking-[.14em] text-sky-800">{weather.attribution.toUpperCase()}</p>
          <h2 className="mt-1 text-lg font-bold">{t("locationTitle", { location: weather.location_name })}</h2>
          <p className="mt-1 text-xs text-[var(--muted)]">{t("subtitle")}</p>
        </div>
        {weather.current && (
          <div className="flex items-center gap-3 rounded-2xl bg-white/80 px-4 py-3">
            <WeatherIcon type={weather.current.condition.type} size={28} className="text-sky-700" />
            <div>
              <p className="text-2xl font-bold tabular-nums">{Math.round(weather.current.temperature_c)}°C</p>
              <p className="text-xs text-[var(--muted)]">{weather.current.condition.description} · {t("feelsLike", { value: Math.round(weather.current.feels_like_c) })}</p>
            </div>
          </div>
        )}
      </div>

      {activeForecast ? (
        <div className="mt-4 grid grid-cols-2 gap-2 rounded-2xl bg-white/75 p-3 sm:grid-cols-4" aria-label={t("summaryLabel", { day: activeDay })}>
          <div className="flex items-center gap-2"><Umbrella size={16} className="text-sky-700" /><span className="text-xs">{t("rain")} <strong>{rainValue(activeForecast)}</strong></span></div>
          <div className="flex items-center gap-2"><Droplets size={16} className="text-sky-700" /><span className="text-xs">{t("humidity")} <strong>{valueOrDash(activeForecast.relative_humidity_percent, "%")}</strong></span></div>
          <div className="flex items-center gap-2"><Wind size={16} className="text-sky-700" /><span className="text-xs">{t("wind")} <strong>{valueOrDash(activeForecast.wind_speed_kph, " km/h")}</strong></span></div>
          <div className="flex items-center gap-2"><Sun size={16} className="text-amber-600" /><span className="text-xs">UV <strong>{valueOrDash(activeForecast.uv_index)}</strong></span></div>
        </div>
      ) : (
        <p className="mt-4 rounded-xl bg-amber-50 px-4 py-3 text-sm text-amber-900">
          {activeDay ? t("outOfRange", { day: activeDay }) : t("pickDay")}
        </p>
      )}

      {weather.days.length > 0 && (
        <div className="mt-4 flex gap-2 overflow-x-auto pb-1" aria-label={t("forecastLabel")}>
          {weather.days.map((day) => {
            const selected = day.date === activeDay;
            return (
              <article key={day.date} aria-current={selected ? "date" : undefined} className={`min-w-[7.4rem] rounded-2xl border px-3 py-3 ${selected ? "border-sky-500 bg-white shadow-sm" : "border-white/70 bg-white/60"}`}>
                <p className="text-xs font-semibold">{dayLabel(day.date, locale)}</p>
                <WeatherIcon type={day.condition.type} className="my-2 text-sky-700" />
                <p className="truncate text-xs text-[var(--muted)]" title={day.condition.description}>{day.condition.description}</p>
                <p className="mt-1 text-sm font-bold tabular-nums">{Math.round(day.min_temperature_c)}°–{Math.round(day.max_temperature_c)}°</p>
                <p className="mt-1 flex items-center gap-1 text-xs text-sky-800"><Umbrella size={12} />{rainValue(day)}</p>
              </article>
            );
          })}
        </div>
      )}

      {weather.warnings.map((warning) => <p key={warning} className="mt-3 text-xs text-amber-900">{warning}</p>)}
      <p className="mt-3 text-xs text-[var(--muted)]">{t("sourceLine", { attribution: weather.attribution, freshness: weather.cache_status === "hit" ? t("cached") : t("fresh") })}</p>
    </section>
  );
}
