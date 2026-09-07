"use client";

import { useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";
import { useSiteVisibility } from "@/components/site-visibility-provider";
import { featureVisible } from "@/lib/site-features";
import type { CatalogPlace, Page } from "@/lib/community/types";
import { Button, Empty, ErrorNotice, fieldClass } from "./ui";
import { useResource } from "./use-resource";

export function PlacePicker({ value, onChange }: {
  value: CatalogPlace[]; onChange: (places: CatalogPlace[]) => void;
}) {
  const t = useTranslations("community");
  const locale = useLocale();
  const visibility = useSiteVisibility();
  const [text, setText] = useState("");
  const [query, setQuery] = useState<string>();
  const search = useResource<Page<CatalogPlace>>(query === undefined ? null :
    `/community/search/places?q=${encodeURIComponent(query)}&locale=${locale}`);
  const results = search.data?.items.filter((place) =>
    place.kind !== "hotspot" || featureVisible(visibility, "hotspots"));
  function submit() {
    if (query === text.trim()) void search.reload();
    else setQuery(text.trim());
  }
  return <section className="space-y-3" aria-label={t("relatedPlaces")}>
    <h2 className="text-xl font-bold">{t("relatedPlaces")}</h2>
    <p className="text-sm text-[var(--muted)]">{t("placePickerHelp")}</p>
    <ul className="space-y-2">{value.map((place) => {
      const name = place.names?.[locale] || place.name;
      return <li key={`${place.kind}:${place.id}`} className="flex items-center justify-between gap-3 rounded-xl border border-[var(--line)] p-3">
        <span className="break-words">{name}</span>
        <Button secondary onClick={() => onChange(value.filter((item) => item.kind !== place.kind || item.id !== place.id))} aria-label={t("removeRelatedPlace", { name })}>{t("remove")}</Button>
      </li>;
    })}</ul>
    <div className="flex flex-wrap items-end gap-3">
      <label className="min-w-0 flex-1 font-semibold">{t("searchPlaces")}<input type="search" maxLength={160} className={fieldClass} value={text} onChange={(event) => setText(event.target.value)} onKeyDown={(event) => { if (event.key === "Enter") { event.preventDefault(); submit(); } }} /></label>
      <Button secondary onClick={submit}>{t("search")}</Button>
    </div>
    <ErrorNotice error={search.error} />
    {search.error ? <Button secondary onClick={() => void search.reload()}>{t("retry")}</Button> : null}
    {search.loading && <Empty>{t("loading")}</Empty>}
    {results?.length === 0 && <Empty>{t("noResults")}</Empty>}
    <ul className="max-h-80 space-y-2 overflow-y-auto">{results?.map((place) => {
      const selected = value.some((item) => item.kind === place.kind && item.id === place.id);
      return <li key={`${place.kind}:${place.id}`} className="flex items-center justify-between gap-3 border-b border-[var(--line)] py-2">
        <div><p className="font-semibold">{place.name}</p><p className="text-sm text-[var(--muted)]">{place.destination}</p></div>
        <Button secondary disabled={selected || value.length >= 20} onClick={() => onChange([...value, place])} aria-label={t("addRelatedPlace", { name: place.name })}>{selected ? t("placeSelected") : t("add")}</Button>
      </li>;
    })}</ul>
  </section>;
}

export function RelatedPlaces({ places }: { places: CatalogPlace[] }) {
  const t = useTranslations("community");
  const locale = useLocale();
  const visibility = useSiteVisibility();
  const visible = places.filter((place) => place.kind !== "hotspot" || featureVisible(visibility, "hotspots"));
  if (!visible.length) return null;
  return <section><h2 className="mb-2 text-lg font-bold">{t("relatedPlaces")}</h2>
    <div className="flex flex-wrap gap-2">{visible.map((place) =>
      <Link key={`${place.kind}:${place.id}`} href={place.href} className="rounded-xl border border-[var(--line)] p-3 text-[var(--teal)]">{place.names?.[locale] || place.name}</Link>)}</div>
  </section>;
}
