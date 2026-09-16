"use client";

import { Search } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useEffect, useId, useRef, useState, type FormEvent, type KeyboardEvent, type RefObject } from "react";
import { useRouter } from "@/i18n/navigation";
import { articleSearchHref, guideHref, type GuideSummary } from "@/lib/guides";
import { useArticleSearch } from "./use-article-search";

type Option = { id: string; href: string; title: string; tag: string | null; kind: "best" | "hit" | "all" };

/**
 * The site's article search box, in two sizes: `inline` sits in the desktop header,
 * `dialog` fills the sheet the phone icon and ⌘K open. Both are the same GET form to
 * `/search/articles`, so with JavaScript off the words still go somewhere; with it on,
 * the list under the box is a WAI-ARIA combobox: arrow keys walk it, Enter follows the
 * marked row or, with none marked, submits, and Escape closes the list before it closes
 * anything around it.
 */
export function SiteSearch({
  variant, className = "", inputRef, onNavigate,
}: {
  variant: "inline" | "dialog";
  className?: string;
  inputRef?: RefObject<HTMLInputElement | null>;
  /** Called after a choice or a submit, so a dialog can close itself. */
  onNavigate?: () => void;
}) {
  const nav = useTranslations("navigation");
  const common = useTranslations("common");
  const locale = useLocale();
  const router = useRouter();
  const id = useId();
  const listId = `${id}-listbox`;
  const container = useRef<HTMLDivElement>(null);
  const [query, setQuery] = useState("");
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(-1);
  const search = useArticleSearch(query, locale, open);
  const trimmed = query.trim();

  useEffect(() => {
    const dismiss = (event: PointerEvent) => {
      if (event.target instanceof Node && !container.current?.contains(event.target)) setOpen(false);
    };
    document.addEventListener("pointerdown", dismiss);
    return () => document.removeEventListener("pointerdown", dismiss);
  }, []);

  const kindLabels: Record<GuideSummary["kind"], string> = {
    intel: common("guides.intel"), howto: common("guides.howto"), life: common("guides.life"),
  };
  const answered = search.status === "ready" && search.query === trimmed;
  const options: Option[] = answered
    ? [
        ...(search.bestMatch
          ? [{ id: `${id}-best`, href: guideHref(search.bestMatch.kind, search.bestMatch.slug), title: search.bestMatch.title, tag: nav("searchBestMatch"), kind: "best" as const }]
          : []),
        ...search.hits
          .filter((hit) => hit.slug !== search.bestMatch?.slug || hit.kind !== search.bestMatch?.kind)
          .map((hit) => ({ id: `${id}-${hit.kind}-${hit.slug}`, href: guideHref(hit.kind, hit.slug), title: hit.title, tag: kindLabels[hit.kind], kind: "hit" as const })),
        ...(search.hits.length || search.bestMatch
          ? [{ id: `${id}-all`, href: articleSearchHref(trimmed), title: nav("searchAllResults", { query: trimmed }), tag: null, kind: "all" as const }]
          : []),
      ]
    : [];
  const expanded = open && trimmed.length >= 2 && (options.length > 0 || search.status !== "idle");
  const activeOption = active >= 0 && active < options.length ? options[active] : null;

  const go = (href: string) => {
    setOpen(false);
    setActive(-1);
    router.push(href);
    onNavigate?.();
  };
  const submit = (event: FormEvent) => {
    event.preventDefault();
    if (activeOption) { go(activeOption.href); return; }
    if (trimmed) go(articleSearchHref(trimmed));
  };
  const onKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.nativeEvent.isComposing) return;
    if (event.key === "ArrowDown" || event.key === "ArrowUp") {
      if (!options.length) return;
      event.preventDefault();
      setOpen(true);
      setActive((current) => {
        if (event.key === "ArrowDown") return current + 1 >= options.length ? 0 : current + 1;
        return current <= 0 ? options.length - 1 : current - 1;
      });
    } else if (event.key === "Escape" && expanded) {
      // Closes the list only. The sheet around a dialog listens for the same key and
      // stands down when it sees the event already handled, so one Escape does one thing.
      event.preventDefault();
      event.stopPropagation();
      setOpen(false);
      setActive(-1);
    } else if (event.key === "Home" && activeOption) {
      event.preventDefault();
      setActive(0);
    } else if (event.key === "End" && activeOption) {
      event.preventDefault();
      setActive(options.length - 1);
    }
  };

  const inline = variant === "inline";
  return (
    <div
      ref={container}
      className={`relative ${className}`}
      onBlur={(event) => { if (!event.currentTarget.contains(event.relatedTarget)) setOpen(false); }}
    >
      <form role="search" method="get" action={`/${locale}/search/articles`} onSubmit={submit} className="flex items-center gap-2">
        <label className="sr-only" htmlFor={`${id}-input`}>{nav("search")}</label>
        <div className="relative min-w-0 flex-1">
          <Search size={inline ? 16 : 20} aria-hidden className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-[var(--muted)]" />
          <input
            ref={inputRef}
            id={`${id}-input`}
            type="search"
            name="q"
            role="combobox"
            aria-expanded={expanded}
            aria-controls={listId}
            aria-autocomplete="list"
            aria-activedescendant={activeOption?.id}
            autoComplete="off"
            enterKeyHint="search"
            maxLength={100}
            value={query}
            placeholder={nav("searchPlaceholder")}
            onFocus={() => setOpen(true)}
            onChange={(event) => { setQuery(event.target.value); setActive(-1); setOpen(true); }}
            onKeyDown={onKeyDown}
            className={inline
              ? "app-field min-h-11 w-56 pl-9 pr-3 text-sm xl:w-72"
              : "app-field min-h-14 w-full pl-11 pr-3 text-base"}
          />
        </div>
        {inline ? null : (
          <button type="submit" className="app-primary-button min-h-14 px-5">{common("guides.searchSubmit")}</button>
        )}
      </form>
      <ul
        id={listId}
        role="listbox"
        aria-label={nav("searchResultsLabel")}
        hidden={!expanded || !options.length}
        className={`${inline ? "absolute left-0 right-0 z-50 mt-2 shadow-lg" : "mt-3"} max-h-[60vh] overflow-y-auto rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-2`}
      >
        {options.map((option, index) => (
          <li
            key={option.id}
            id={option.id}
            role="option"
            aria-selected={index === active}
            onMouseDown={(event) => event.preventDefault()}
            onMouseEnter={() => setActive(index)}
            onClick={() => go(option.href)}
            className={`flex min-h-11 cursor-pointer items-center justify-between gap-3 rounded-xl px-3 py-2 text-sm ${index === active ? "bg-[var(--teal-soft)]" : ""} ${option.kind === "all" ? "font-semibold text-[var(--teal)]" : ""}`}
          >
            <span className="min-w-0 truncate">{option.title}</span>
            {option.tag ? <span className="flex-none rounded-full bg-[var(--line)] px-2 py-0.5 text-xs text-[var(--muted)]">{option.tag}</span> : null}
          </li>
        ))}
      </ul>
      {expanded && !options.length ? (
        <p role="status" className={`${inline ? "absolute left-0 right-0 z-50 mt-2 shadow-lg" : "mt-3"} rounded-2xl border border-[var(--line)] bg-[var(--surface)] px-4 py-3 text-sm text-[var(--muted)]`}>
          {search.status === "error" ? nav("searchUnavailable") : answered ? nav("searchNoResults") : nav("searchLoading")}
        </p>
      ) : null}
    </div>
  );
}
