/** Pure helpers; no catalogue, editorial drafts, environment or server imports here. */
export type GeminiStage = 1 | 2;
export type GeminiTrack = "work" | "research" | "creative" | "md" | "automation" | "api";
export type GeminiLesson = {
  number: number; slug: string; title: string; purpose: string; group: string;
  level: string; platforms: readonly string[]; keywords: readonly string[];
  minutes: number; prerequisites: readonly number[]; related: readonly number[];
  stage?: number; track?: string; labMinutes?: number;
};
export type GeminiPath = {
  id: string; title: string; description: string; articles: readonly number[]; stage?: number;
};
export type GeminiCommand = { command: string; description: string; kind: string; article: number; anchor?: string };
export type GeminiCatalogue = {
  id: string; locale: string; hubSlug: string; title: string;
  groups: readonly { id: string; title: string }[];
  articles: readonly GeminiLesson[]; paths: readonly GeminiPath[]; commands: readonly GeminiCommand[];
};
export type VisibleGeminiLesson = GeminiLesson & { stage: GeminiStage; track?: GeminiTrack };
export type VisibleGeminiSeries = Omit<GeminiCatalogue, "articles" | "paths"> & {
  articles: readonly VisibleGeminiLesson[];
  paths: readonly (GeminiPath & { stage: GeminiStage })[];
  advancedEnabled: boolean;
};
const tracks = new Set<string>(["work", "research", "creative", "md", "automation", "api"]);

function lessonStage(lesson: GeminiLesson): GeminiStage {
  const stage = lesson.number <= 50 ? 1 : 2;
  // Number is an additional guard: a missing or forged stage never exposes a draft.
  if (!Number.isInteger(lesson.number) || lesson.number < 1 || lesson.number > 86
    || (lesson.stage !== undefined && lesson.stage !== stage)) throw new Error("Invalid Gemini lesson stage");
  return stage;
}

/** Run on the server before serializing props. Never pass the source catalogue to a client. */
export function projectGeminiSeries(source: GeminiCatalogue, advancedEnabled = false): VisibleGeminiSeries {
  const numbers = new Set<number>();
  const slugs = new Set<string>([source.hubSlug]);
  for (const lesson of source.articles) {
    lessonStage(lesson);
    if (numbers.has(lesson.number) || slugs.has(lesson.slug)) throw new Error("Duplicate Gemini lesson identity");
    numbers.add(lesson.number); slugs.add(lesson.slug);
  }
  const selected = source.articles.filter(lesson => lessonStage(lesson) === 1 || advancedEnabled)
    .sort((left, right) => left.number - right.number);
  const expectedCount = advancedEnabled && source.articles.some(lesson => lesson.number > 50) ? 86 : 50;
  if (selected.length !== expectedCount || selected.some((lesson, index) => lesson.number !== index + 1)) {
    throw new Error("Incomplete visible Gemini series");
  }
  const visible = new Set(selected.map(lesson => lesson.number));
  const references = (values: readonly number[]) => [...new Set(values.filter(number => visible.has(number)))];
  const articles: VisibleGeminiLesson[] = selected.map(lesson => {
    const stage = lessonStage(lesson);
    if (stage === 2 && (!tracks.has(lesson.track ?? "") || !Number.isInteger(lesson.labMinutes) || (lesson.labMinutes ?? 0) < 1)) {
      throw new Error("Advanced Gemini lesson requires track and lab time");
    }
    // Pick public fields explicitly: future editorial metadata must not enter serialized props.
    return {
      number: lesson.number, slug: lesson.slug, title: lesson.title, purpose: lesson.purpose,
      group: lesson.group, level: lesson.level, platforms: [...lesson.platforms], keywords: [...lesson.keywords],
      minutes: lesson.minutes, stage,
      ...(stage === 2 ? { track: lesson.track as GeminiTrack, labMinutes: lesson.labMinutes } : {}),
      prerequisites: references(lesson.prerequisites).filter(number => number !== lesson.number),
      related: references(lesson.related).filter(number => number !== lesson.number),
    };
  });
  const paths = source.paths.flatMap(route => {
    const stage = route.stage ?? (route.articles.some(number => number > 50) ? 2 : 1);
    if (stage !== 1 && stage !== 2) throw new Error("Invalid Gemini path stage");
    if (stage === 2 && !advancedEnabled) return [];
    const members = references(route.articles);
    return members.length ? [{ id: route.id, title: route.title, description: route.description, stage: stage as GeminiStage, articles: members }] : [];
  });
  const commands = source.commands.filter(command => visible.has(command.article)).map(command => ({
    command: command.command, description: command.description, kind: command.kind, article: command.article,
    ...(command.anchor ? { anchor: command.anchor } : {}),
  }));
  return {
    id: source.id, locale: source.locale, hubSlug: source.hubSlug, title: source.title,
    groups: source.groups.map(group => ({ id: group.id, title: group.title })),
    articles, paths, commands, advancedEnabled: articles.some(lesson => lesson.stage === 2),
  };
}

export function visibleGeminiMember(series: VisibleGeminiSeries, slug: string, locale: string, kind: string) {
  if (locale !== series.locale || kind !== "life") return undefined;
  return series.articles.find(lesson => lesson.slug === slug);
}

export function visibleGeminiNavigation(series: VisibleGeminiSeries, number: number) {
  const index = series.articles.findIndex(lesson => lesson.number === number);
  if (index === -1) return undefined;
  const current = series.articles[index];
  const related = (refs: readonly number[]) => refs.flatMap(ref => {
    const lesson = series.articles.find(entry => entry.number === ref);
    return lesson ? [lesson] : [];
  });
  return { current, previous: series.articles[index - 1], next: series.articles[index + 1],
    prerequisites: related(current.prerequisites), related: related(current.related) };
}

export type GeminiFilters = { query?: string; group?: string; path?: string; stage?: GeminiStage; track?: GeminiTrack };
export function filterVisibleGeminiLessons(series: VisibleGeminiSeries, filters: GeminiFilters = {}) {
  const route = filters.path ? series.paths.find(entry => entry.id === filters.path) : undefined;
  if (filters.path && !route) return [];
  const words = (filters.query ?? "").normalize("NFKC").trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
  return series.articles.filter(lesson => {
    const text = [lesson.title, lesson.purpose, lesson.level, ...lesson.platforms, ...lesson.keywords].join(" ").normalize("NFKC").toLocaleLowerCase();
    return (!filters.stage || lesson.stage === filters.stage) && (!filters.track || lesson.track === filters.track)
      && (!filters.group || lesson.group === filters.group) && (!route || route.articles.includes(lesson.number))
      && words.every(word => text.includes(word));
  });
}

export const visibleGeminiHref = (series: VisibleGeminiSeries, slug: string, anchor?: string) => {
  if (slug !== series.hubSlug && !series.articles.some(article => article.slug === slug)) return undefined;
  return `/${series.locale}/life/${slug}${anchor ? `#${anchor}` : ""}`;
};
