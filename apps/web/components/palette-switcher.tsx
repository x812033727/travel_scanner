"use client";

import { useId } from "react";
import { useTranslations } from "next-intl";
import { palettes } from "@/lib/theme";
import { useTheme } from "@/components/theme-provider";

export function PaletteSwitcher() {
  const t = useTranslations("navigation");
  const { palette, setPalette, resolvedTheme, ready } = useTheme();
  const id = useId();
  return (
    <fieldset className="palette-switcher" disabled={!ready} aria-describedby={`${id}-help`}>
      <legend className="text-sm font-bold">{t("paletteLabel")}</legend>
      <p id={`${id}-help`} className="mt-1 text-sm text-[var(--muted)]">{t("paletteHelp")}</p>
      <div className="mt-3 grid gap-3 sm:grid-cols-3">
        {palettes.map((choice) => (
          <label key={choice} className="palette-choice">
            <input type="radio" name={id} value={choice} checked={palette === choice} onChange={() => setPalette(choice)} />
            <span className="palette-preview" data-preview-palette={choice} data-preview-theme={resolvedTheme} aria-hidden="true">
              <span /><span /><span />
            </span>
            <span>{t(`palette_${choice}`)}</span>
          </label>
        ))}
      </div>
    </fieldset>
  );
}
