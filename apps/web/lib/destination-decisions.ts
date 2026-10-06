import type { Locale } from "@/i18n/routing";
import data from "./destination-decisions.json";

type Source = { label: string; url: string };
type AreaCopy = { name: string; suitable: string; tradeoff: string; check: string };
type DecisionCopy = {
  title: string;
  intro: string;
  suitableLabel: string;
  tradeoffLabel: string;
  checkLabel: string;
  sourceLabel: string;
  checkedLabel: string;
  areas: Record<string, AreaCopy>;
};
type CityDecisions = {
  checkedOn: string;
  /** Card order; every id has copy in each locale and its own sources. */
  areaIds: string[];
  sources: Record<string, Source[]>;
  locales: Record<Locale, DecisionCopy>;
};
const cities = new Map<string, CityDecisions>(Object.entries(data.destinations));

/** Sourced editorial comparisons, distinct from hotel reviews or partner offers. */
export function destinationDecisions(locale: Locale, destinationId: string) {
  const city = cities.get(destinationId);
  if (!city) return null;
  const { areas, ...copy } = city.locales[locale];
  return {
    ...copy,
    checkedOn: city.checkedOn,
    areas: city.areaIds.map((id) => ({ id, ...areas[id], sources: city.sources[id] })),
  };
}

/** The destinations that carry sourced stay decisions. */
export const decisionDestinationIds = [...cities.keys()];
