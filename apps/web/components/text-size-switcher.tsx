"use client";

import { ALargeSmall } from "lucide-react";
import { useTranslations } from "next-intl";
import { useCallback, useEffect, useState } from "react";
import {
  isTextSize,
  TEXT_SIZE_CHANGE_EVENT,
  TEXT_SIZE_STORAGE_KEY,
  textSizes,
  type TextSize,
} from "@/lib/text-size";

const labelKeys = {
  standard: "textSizeStandard",
  large: "textSizeLarge",
  largest: "textSizeLargest",
} as const;

function readStored(): TextSize {
  const bootstrapped = document.documentElement.dataset.textSize;
  try {
    const stored = localStorage.getItem(TEXT_SIZE_STORAGE_KEY);
    if (isTextSize(stored)) return stored;
  } catch {
    // The attribute the bootstrap script wrote is still right.
  }
  return isTextSize(bootstrapped) ? bootstrapped : "standard";
}

/**
 * One preference, two shapes. The phone menu gets three labelled buttons because
 * a reader who needs bigger text is exactly the reader who will not find a
 * 44px icon that opens a select; the desktop header gets the same compact
 * icon-over-select the theme control uses.
 */
export function TextSizeSwitcher({ variant = "compact" }: { variant?: "compact" | "expanded" }) {
  const t = useTranslations("navigation");
  const [size, setSize] = useState<TextSize>("standard");
  const [ready, setReady] = useState(false);

  useEffect(() => {
    let cancelled = false;
    const sync = () => {
      if (cancelled) return;
      setSize(readStored());
      setReady(true);
    };
    // Reading storage during the effect and setting state straight away would
    // cascade a render; the theme control defers for the same reason.
    queueMicrotask(sync);
    window.addEventListener(TEXT_SIZE_CHANGE_EVENT, sync);
    window.addEventListener("storage", sync);
    return () => {
      cancelled = true;
      window.removeEventListener(TEXT_SIZE_CHANGE_EVENT, sync);
      window.removeEventListener("storage", sync);
    };
  }, []);

  const apply = useCallback((next: TextSize) => {
    document.documentElement.dataset.textSize = next;
    try {
      localStorage.setItem(TEXT_SIZE_STORAGE_KEY, next);
    } catch {
      // The choice still applies to this page without storage.
    }
    setSize(next);
    // Both the phone sheet and the desktop header mount a copy of this control.
    window.dispatchEvent(new Event(TEXT_SIZE_CHANGE_EVENT));
  }, []);

  if (variant === "expanded") {
    return (
      <div>
        <p className="mb-2 text-sm font-bold text-[var(--muted)]">{t("textSizeLabel")}</p>
        <div role="radiogroup" aria-label={t("textSizeLabel")} className="grid grid-cols-3 gap-2">
          {textSizes.map((value) => (
            <button
              key={value}
              type="button"
              role="radio"
              aria-checked={size === value}
              disabled={!ready}
              onClick={() => apply(value)}
              className={`min-h-12 rounded-xl border font-semibold transition ${
                size === value
                  ? "border-[var(--teal)] bg-[var(--teal-fill)] text-white"
                  : "border-[var(--line)] bg-[var(--surface)] text-[var(--ink)]"
              }`}
            >
              {t(labelKeys[value])}
            </button>
          ))}
        </div>
      </div>
    );
  }

  return (
    <label className="theme-switcher" title={t("textSizeCurrent", { size: t(labelKeys[size]) })}>
      <ALargeSmall aria-hidden size={20} />
      <span className="sr-only">{t("textSizeLabel")}</span>
      <select
        aria-label={t("textSizeLabel")}
        disabled={!ready}
        value={size}
        onChange={(event) => apply(event.target.value as TextSize)}
      >
        {textSizes.map((value) => (
          <option key={value} value={value}>{t(labelKeys[value])}</option>
        ))}
      </select>
    </label>
  );
}
