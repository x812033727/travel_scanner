import type { Locale } from "@/i18n/routing";
import data from "./destination-decisions.json";

const areaIds = ["shinjuku", "uenoAsakusa", "tokyoGinza", "shibuya"] as const;
type AreaId = typeof areaIds[number];
type AreaCopy = { name: string; suitable: string; tradeoff: string; check: string };
type DecisionCopy = {
  title: string;
  intro: string;
  suitableLabel: string;
  tradeoffLabel: string;
  checkLabel: string;
  sourceLabel: string;
  checkedLabel: string;
  areas: Record<AreaId, AreaCopy>;
};
const copies: Record<Locale, DecisionCopy> = data.locales;

/** Sourced editorial comparisons, distinct from hotel reviews or partner offers. */
export function destinationDecisions(locale: Locale, destinationId: string) {
  if (destinationId !== "tokyo") return null;
  const { areas, ...copy } = copies[locale];
  return {
    ...copy,
    checkedOn: data.checkedOn,
    areas: areaIds.map((id) => ({ id, ...areas[id], sources: data.sources[id] })),
  };
}
