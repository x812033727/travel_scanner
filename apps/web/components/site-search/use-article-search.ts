"use client";

import { useEffect, useState } from "react";
import { api, ApiError } from "@/lib/api";
import type { GuideSearchHit, GuideSearchResult, GuideSummary } from "@/lib/guides";

export type ArticleSearchStatus = "idle" | "loading" | "ready" | "error";

export type ArticleSearchState = {
  status: ArticleSearchStatus;
  /** The words the answer is for; a reader who kept typing sees the older answer marked stale. */
  query: string;
  hits: GuideSearchHit[];
  bestMatch: GuideSummary | null;
};

type Answer = ArticleSearchState & { status: "ready" | "error" };

export const SUGGESTION_LIMIT = 6;
export const MIN_QUERY_LENGTH = 2;
export const DEBOUNCE_MS = 200;

const IDLE: ArticleSearchState = { status: "idle", query: "", hits: [], bestMatch: null };

/**
 * The typeahead behind the header's search box: one debounced read of `/guides/search`
 * per pause in typing, aborted by the next keystroke so a slow early answer can never
 * overwrite a fast later one. A 422 (nothing searchable in the words) is an empty answer,
 * not an error: the reader is mid-word, and a red message would flash on every keystroke.
 *
 * Only the last answer is kept in state; everything else is derived from it and the words
 * in the box. So closing the list (`enabled` false) stops the fetching, not the
 * remembering, and reopening it on the same words shows the answer without a round trip.
 */
export function useArticleSearch(query: string, locale: string, enabled: boolean): ArticleSearchState {
  const trimmed = query.trim();
  const [answer, setAnswer] = useState<Answer | null>(null);
  const answered = answer !== null && answer.query === trimmed;
  useEffect(() => {
    if (!enabled || answered || trimmed.length < MIN_QUERY_LENGTH) return;
    const controller = new AbortController();
    const timer = window.setTimeout(() => {
      const params = new URLSearchParams({ locale, q: trimmed, limit: String(SUGGESTION_LIMIT) });
      api<GuideSearchResult>(`/guides/search?${params.toString()}`, { signal: controller.signal })
        .then((result) => {
          if (controller.signal.aborted) return;
          setAnswer({
            status: "ready", query: trimmed,
            hits: Array.isArray(result.results) ? result.results : [],
            bestMatch: result.best_match ?? null,
          });
        })
        .catch((error: unknown) => {
          if (controller.signal.aborted) return;
          const refused = error instanceof ApiError && error.status === 422;
          setAnswer({ status: refused ? "ready" : "error", query: trimmed, hits: [], bestMatch: null });
        });
    }, DEBOUNCE_MS);
    return () => {
      window.clearTimeout(timer);
      controller.abort();
    };
  }, [trimmed, locale, enabled, answered]);
  if (trimmed.length < MIN_QUERY_LENGTH) return IDLE;
  if (answered) return answer;
  return { status: enabled ? "loading" : "idle", query: trimmed, hits: [], bestMatch: null };
}
