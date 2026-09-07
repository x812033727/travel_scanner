"use client";

import {
  ExternalLink,
  Heart,
  LoaderCircle,
  MapPin,
  Trash2,
} from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useMemo, useState } from "react";
import { useSavedItems } from "@/components/saved-items-provider";
import { api } from "@/lib/api";
import { safeExternalHref } from "@/lib/navigation";

type SavedType = "hotspot" | "food" | "restaurant" | "merchant";
type CopyFilter = "all" | "hotspot" | "food" | "restaurant";
type SavedItem = {
  type: SavedType;
  id: string;
  title: string;
  subtitle: string;
  map_links: { url: string; label: string }[];
};
type Filter = "all" | SavedType;

export function AccountSavedItems() {
  const tAccount = useTranslations("account");
  const filterLabel = (key: Filter) =>
    key === "merchant" ? tAccount("savedMerchants") : tAccount(`savedItems.filters.${key as CopyFilter}`);
  const saved = useSavedItems();
  const [items, setItems] = useState<SavedItem[]>([]);
  const [filter, setFilter] = useState<Filter>("all");
  const [loaded, setLoaded] = useState(false);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState("");

  // The provider has already asked /saved-items and knows the answer to "is anyone signed
  // in", so wait for it rather than sending a second request that can only 401. A signed-out
  // reader used to get this card's zero counts, its own alert, and the account panel's sign-in
  // notice all at once: three statements about the same fact.
  // Resolved before the effect so the dependency stays a plain string the linter can
  // check, as it was when this copy lived in a table inside the file.
  const loadError = tAccount("savedItems.error");
  useEffect(() => {
    if (saved.status !== "authenticated") return;
    api<{ items: SavedItem[] }>("/saved-items?limit=100")
      .then((result) => setItems(result.items))
      .catch((reason: unknown) =>
        setError(reason instanceof Error ? reason.message : loadError),
      )
      .finally(() => setLoaded(true));
  }, [saved.status, loadError]);
  // Nothing is on its way when the provider says the reader is not signed in, so the
  // skeleton should not keep spinning for a list that will never arrive.
  const ready = loaded || saved.status !== "authenticated";

  const visible = useMemo(
    () =>
      filter === "all" ? items : items.filter((item) => item.type === filter),
    [filter, items],
  );
  const counts = useMemo(
    () => ({
      all: items.length,
      hotspot: items.filter((item) => item.type === "hotspot").length,
      food: items.filter((item) => item.type === "food").length,
      restaurant: items.filter((item) => item.type === "restaurant").length,
      merchant: items.filter((item) => item.type === "merchant").length,
    }),
    [items],
  );

  // The account panel below says it once, with a button. Saying it again here — zero
  // counts, an alert, and a third sentence — is what made a logged-out page look broken.
  if (saved.status === "signed_out") return null;

  async function remove(item: SavedItem) {
    const key = `${item.type}:${item.id}`;
    setBusy(key);
    setError("");
    try {
      await saved.setSaved(item.type, item.id, false);
      setItems((current) =>
        current.filter(
          (candidate) =>
            candidate.type !== item.type || candidate.id !== item.id,
        ),
      );
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setBusy("");
    }
  }

  return (
    <section className="app-surface mb-6 p-5 md:p-8">
      <div className="flex items-center gap-3">
        <span className="grid h-11 w-11 place-items-center rounded-2xl bg-[var(--coral-soft)] text-[var(--coral)]">
          <Heart size={20} fill="currentColor" />
        </span>
        <div>
          <h2 className="text-xl font-bold">{tAccount("savedItems.title")}</h2>
          <p className="text-sm text-[var(--muted)]">{tAccount("savedItems.description")}</p>
        </div>
      </div>
      <div className="app-chip-row mt-5" role="tablist" aria-label={tAccount("savedItems.title")}>
        {(["all", "hotspot", "food", "merchant", "restaurant"] as Filter[]).map((key) => (
          <button
            key={key}
            type="button"
            role="tab"
            aria-selected={filter === key}
            onClick={() => setFilter(key)}
            className={`app-filter-chip ${filter === key ? "app-filter-chip-active" : ""}`}
          >
            <span>{filterLabel(key)}</span>
            <span className="app-filter-count">{counts[key]}</span>
          </button>
        ))}
      </div>
      {error && (
        <p
          role="alert"
          className="mt-4 rounded-2xl bg-red-50 p-4 text-sm text-red-800"
        >
          {tAccount("savedItems.errorWithDetail", { detail: error })}
        </p>
      )}
      {!ready ? (
        <div role="status" className="mt-5 grid gap-3 sm:grid-cols-2">
          <span className="app-skeleton h-20" />
          <span className="app-skeleton h-20" />
          <span className="sr-only">{tAccount("savedItems.loading")}</span>
        </div>
      ) : visible.length === 0 ? (
        <div className="app-empty-state mt-5">
          <Heart size={24} />
          <p>{tAccount("savedItems.empty")}</p>
        </div>
      ) : (
        <div className="mt-5 grid gap-3 sm:grid-cols-2">
          {visible.map((item) => {
            const map = item.map_links[0];
            const key = `${item.type}:${item.id}`;
            return (
              <article key={key} className="saved-item-card">
                <span className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-[var(--teal-soft)] text-[var(--teal-dark)]">
                  <MapPin size={18} />
                </span>
                <div className="min-w-0 flex-1">
                  <strong className="block truncate text-sm">
                    {item.title}
                  </strong>
                  <span className="block truncate text-xs text-[var(--muted)]">
                    {item.subtitle}
                  </span>
                </div>
                {map && (
                  <a
                    href={safeExternalHref(map.url)}
                    target="_blank"
                    rel="noopener noreferrer"
                    aria-label={`${tAccount("savedItems.map")}：${item.title}`}
                    className="app-icon-button"
                  >
                    <ExternalLink size={17} />
                  </a>
                )}
                <button
                  type="button"
                  disabled={busy === key}
                  onClick={() => void remove(item)}
                  aria-label={`${tAccount("savedItems.remove")}：${item.title}`}
                  className="app-icon-button text-[var(--coral)]"
                >
                  {busy === key ? (
                    <LoaderCircle className="animate-spin" size={17} />
                  ) : (
                    <Trash2 size={17} />
                  )}
                </button>
              </article>
            );
          })}
        </div>
      )}
    </section>
  );
}
