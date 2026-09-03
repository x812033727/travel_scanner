"use client";

import { MapPin } from "lucide-react";
import { sortCitiesByMerchants, type FoodCountry } from "@/lib/foods";

export function FoodCitySelect({
  countries,
  value,
  onChange,
  label,
  allLabel,
}: {
  countries: FoodCountry[];
  value: string;
  onChange: (destinationId: string) => void;
  label: string;
  allLabel: string;
}) {
  return (
    <select
      aria-label={label}
      value={value}
      onChange={(event) => onChange(event.target.value)}
      className="h-12 rounded-xl border border-[var(--line)] bg-[var(--paper)] px-3"
    >
      <option value="">{allLabel}</option>
      {countries.map((country) => (
        <optgroup key={country.code} label={country.name}>
          {country.cities.map((city) => (
            <option key={city.id} value={city.id}>
              {city.name} ({city.merchant_count})
            </option>
          ))}
        </optgroup>
      ))}
    </select>
  );
}

export function FoodCityGrid({
  countries,
  onSelect,
  countLabel,
}: {
  countries: FoodCountry[];
  onSelect: (destinationId: string) => void;
  countLabel: (count: number) => string;
}) {
  return (
    <div className="grid gap-6">
      {countries.map((country) => (
        <section key={country.code} aria-label={country.name}>
          <h3 className="text-sm font-bold uppercase tracking-[.14em] text-[var(--coral)]">
            {country.name}
          </h3>
          <div className="mt-3 grid gap-2 sm:grid-cols-2 lg:grid-cols-4">
            {sortCitiesByMerchants(country.cities).map((city) => (
              <button
                key={city.id}
                type="button"
                onClick={() => onSelect(city.id)}
                aria-label={`${city.name} · ${countLabel(city.merchant_count)}`}
                className={`flex min-h-14 items-center justify-between gap-3 rounded-2xl border border-[var(--line)] bg-white px-4 text-left ${city.merchant_count === 0 ? "opacity-60" : ""}`}
              >
                <span className="flex items-center gap-2 font-semibold">
                  <MapPin size={16} className="text-[var(--teal)]" />
                  {city.name}
                </span>
                <span className="text-xs text-[var(--muted)]">{countLabel(city.merchant_count)}</span>
              </button>
            ))}
          </div>
        </section>
      ))}
    </div>
  );
}
