export type LearningFilters = { q: string; level: string; platform: string; goal: string; unit: string };
export const emptyFilters: LearningFilters = { q: "", level: "", platform: "", goal: "", unit: "" };

export function readLearningFilters(search: string): LearningFilters {
  const params = new URLSearchParams(search);
  const option = (name: string, max: number) => {
    const value = params.get(name) ?? "";
    return /^[0-9]$/.test(value) && Number(value) <= max ? value : "";
  };
  return { q: (params.get("q") ?? "").slice(0, 200), level: option("level", 2), platform: option("platform", 4), goal: option("goal", 5), unit: /^[A-J]$/.test(params.get("unit") ?? "") ? params.get("unit")! : "" };
}

/** Preserve unrelated query parameters and fragments when editing shareable filters. */
export function learningFilterUrl(current: string, values: LearningFilters) {
  const url = new URL(current);
  const normalized = readLearningFilters(new URLSearchParams(values).toString());
  for (const key of Object.keys(emptyFilters) as (keyof LearningFilters)[]) {
    if (normalized[key]) url.searchParams.set(key, normalized[key]);
    else url.searchParams.delete(key);
  }
  return url.pathname + url.search + url.hash;
}
