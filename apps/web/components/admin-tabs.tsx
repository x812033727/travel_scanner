"use client";

import {
  type KeyboardEvent,
  type ReactNode,
  useCallback,
  useSyncExternalStore,
} from "react";

const listeners = new Set<() => void>();

function subscribe(listener: () => void) {
  listeners.add(listener);
  window.addEventListener("hashchange", listener);
  window.addEventListener("popstate", listener);
  return () => {
    listeners.delete(listener);
    window.removeEventListener("hashchange", listener);
    window.removeEventListener("popstate", listener);
  };
}

function readHash() {
  return window.location.hash.replace(/^#/, "");
}

function serverHash() {
  return "";
}

/**
 * Keeps the active tab in the URL hash so a panel can be deep-linked
 * (for example `/admin/hotspots#guides`). The server render always shows
 * `defaultKey`; the hash is applied after hydration.
 *
 * Known limit: a same-route <Link> that only changes the hash does not fire
 * `hashchange` or `popstate`, so it would not update this store.
 */
export function useHashTab<K extends string>(
  keys: readonly K[],
  defaultKey: K,
): [K, (key: string) => void] {
  const hash = useSyncExternalStore(subscribe, readHash, serverHash);
  const active = (keys as readonly string[]).includes(hash) ? (hash as K) : defaultKey;
  const select = useCallback((key: string) => {
    // replaceState never fires hashchange, so notify subscribers by hand.
    window.history.replaceState(window.history.state, "", `#${key}`);
    listeners.forEach((listener) => listener());
  }, []);
  return [active, select];
}

export type AdminTab = { key: string; label: string; count?: number };

type AdminTabsProps = {
  idPrefix: string;
  label: string;
  mobileLabel: string;
  tabs: AdminTab[];
  active: string;
  onSelect: (key: string) => void;
};

const navigationKeys = ["ArrowLeft", "ArrowRight", "Home", "End"];

export function AdminTabs({
  idPrefix,
  label,
  mobileLabel,
  tabs,
  active,
  onSelect,
}: AdminTabsProps) {
  function moveTab(event: KeyboardEvent<HTMLButtonElement>, index: number) {
    if (!navigationKeys.includes(event.key)) return;
    event.preventDefault();
    const nextIndex =
      event.key === "Home"
        ? 0
        : event.key === "End"
          ? tabs.length - 1
          : (index + (event.key === "ArrowRight" ? 1 : -1) + tabs.length) % tabs.length;
    const next = tabs[nextIndex].key;
    onSelect(next);
    requestAnimationFrame(() =>
      document.getElementById(`${idPrefix}-tab-${next}`)?.focus(),
    );
  }

  return (
    <>
      <label className="block md:hidden">
        <span className="mb-2 block text-sm font-semibold">{mobileLabel}</span>
        <select
          value={active}
          onChange={(event) => onSelect(event.target.value)}
          className="min-h-12 w-full rounded-xl border border-[var(--line)] bg-white px-3"
        >
          {tabs.map((tab) => (
            <option key={tab.key} value={tab.key}>
              {tab.label}
              {tab.count != null ? ` (${tab.count})` : ""}
            </option>
          ))}
        </select>
      </label>
      <div
        role="tablist"
        aria-label={label}
        className="hidden gap-2 overflow-x-auto pb-2 md:flex"
      >
        {tabs.map((tab, index) => {
          const selected = tab.key === active;
          return (
            <button
              key={tab.key}
              id={`${idPrefix}-tab-${tab.key}`}
              type="button"
              role="tab"
              aria-selected={selected}
              aria-controls={`${idPrefix}-panel-${tab.key}`}
              tabIndex={selected ? 0 : -1}
              onClick={() => onSelect(tab.key)}
              onKeyDown={(event) => moveTab(event, index)}
              className={`flex shrink-0 items-center gap-2 rounded-full border px-4 py-2 text-sm font-semibold transition ${
                selected
                  ? "border-[var(--teal)] bg-[var(--teal)] text-white"
                  : "border-[var(--line)] bg-white text-[var(--ink)] hover:border-[var(--teal)]"
              }`}
            >
              {tab.label}
              {tab.count != null && (
                <span
                  className={`rounded-full px-2 py-0.5 text-[.65rem] tabular-nums ${
                    selected ? "bg-white/20" : "bg-[var(--paper)] text-[var(--muted)]"
                  }`}
                >
                  {tab.count}
                </span>
              )}
            </button>
          );
        })}
      </div>
    </>
  );
}

type AdminTabPanelProps = {
  idPrefix: string;
  tabKey: string;
  active: string;
  children: ReactNode;
};

export function AdminTabPanel({ idPrefix, tabKey, active, children }: AdminTabPanelProps) {
  return (
    <div
      id={`${idPrefix}-panel-${tabKey}`}
      role="tabpanel"
      aria-labelledby={`${idPrefix}-tab-${tabKey}`}
      hidden={tabKey !== active}
    >
      {children}
    </div>
  );
}
