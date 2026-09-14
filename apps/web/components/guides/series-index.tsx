"use client";

import { useState } from "react";
import { geminiCopy as copy, geminiSeries, matchesSeriesArticle, seriesArticle, seriesHref } from "@/lib/gemini-series";

const anchor = "text-[var(--teal)] underline underline-offset-4";

/** Initial render includes every lesson and link; filters only enhance the server HTML. */
export function GeminiSeriesIndex() {
  const [query, setQuery] = useState("");
  const [group, setGroup] = useState("");
  const [path, setPath] = useState("");
  const route = geminiSeries.paths.find((entry) => entry.id === path);
  const articles = geminiSeries.articles.filter((article) => (!group || article.group === group)
    && (!route || route.articles.includes(article.number)) && matchesSeriesArticle(article, query));
  const commands = geminiSeries.commands.filter((entry) => !query.trim() || `${entry.command} ${entry.description} ${entry.kind}`.toLowerCase().includes(query.trim().toLowerCase()));
  return <section id="series-directory" aria-label={copy.directory} className="min-w-0 scroll-mt-24 space-y-7" data-testid="gemini-series-index">
    <div className="space-y-4 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4 sm:p-6">
      <h2 className="text-xl font-bold">{copy.find}</h2>
      <label className="grid gap-2 text-sm font-semibold">{copy.search}
        <input type="search" value={query} onChange={(event) => setQuery(event.target.value)} placeholder={copy.placeholder} className="min-h-11 min-w-0 w-full rounded-lg border border-[var(--line)] bg-[var(--surface)] px-3" />
      </label>
      <div className="grid gap-3 sm:grid-cols-2">
        <label className="grid gap-2 text-sm">{copy.group}<select value={group} onChange={(event) => setGroup(event.target.value)} className="min-h-11 w-full rounded-lg border border-[var(--line)] bg-[var(--surface)] px-2"><option value="">{copy.allGroups}</option>{geminiSeries.groups.map((entry) => <option key={entry.id} value={entry.id}>{entry.title}</option>)}</select></label>
        <label className="grid gap-2 text-sm">{copy.path}<select value={path} onChange={(event) => setPath(event.target.value)} className="min-h-11 w-full rounded-lg border border-[var(--line)] bg-[var(--surface)] px-2"><option value="">{copy.allPaths}</option>{geminiSeries.paths.map((entry) => <option key={entry.id} value={entry.id}>{entry.title}</option>)}</select></label>
      </div>
      <button type="button" onClick={() => { setQuery(""); setGroup(""); setPath(""); }} className={`min-h-11 ${anchor}`}>{copy.clear}</button>
      <p role="status" className="text-sm text-[var(--muted)]">{copy.count.replace("{count}", String(articles.length)).replace("{total}", String(geminiSeries.articles.length))}</p>
    </div>
    <nav aria-label={copy.suggestedPaths} className="space-y-4">
      <h2 className="text-xl font-bold">{copy.byGoal}</h2>
      {geminiSeries.paths.filter((entry) => !path || entry.id === path).map((entry) => <details key={entry.id} open={Boolean(path)} className="rounded-xl border border-[var(--line)] p-4">
        <summary className="cursor-pointer py-2 font-semibold">{entry.title} · {entry.articles.length} {copy.lessons}</summary>
        <p className="my-3 leading-7 text-[var(--muted)]">{entry.description}</p>
        <ol className="list-decimal space-y-2 pl-5">{entry.articles.map((number) => {
          const article = seriesArticle(number);
          return article ? <li key={number}><a href={seriesHref(article.slug)} className={anchor}>{article.title}</a></li> : null;
        })}</ol>
      </details>)}
    </nav>
    <div className="space-y-7" data-testid="series-lessons">
      {geminiSeries.groups.map((entry) => {
        const members = articles.filter((article) => article.group === entry.id);
        if (!members.length) return null;
        return <section key={entry.id} id={`chapter-${entry.id.toLowerCase()}`} className="scroll-mt-24 space-y-3">
          <h2 className="text-xl font-bold">{entry.id}. {entry.title}</h2>
          <ol className="grid gap-3">{members.map((article) => <li key={article.slug} className="min-w-0 rounded-xl border border-[var(--line)] p-4">
            <a href={seriesHref(article.slug)} className={`block text-lg font-semibold ${anchor}`}><span className="mr-2 font-mono text-sm">{String(article.number).padStart(2, "0")}</span>{article.title}</a>
            <p className="mt-2 leading-7">{copy.outcome}{article.purpose}</p>
            <p className="mt-2 flex flex-wrap gap-x-3 gap-y-1 text-sm text-[var(--muted)]"><span>{article.level}</span><span>{article.platforms.join("、")}</span><span>{copy.minutes.replace("{minutes}", String(article.minutes))}</span></p>
          </li>)}</ol>
        </section>;
      })}
      {!articles.length ? <p className="leading-7">{copy.noResults}</p> : null}
    </div>
    <section id="commands" className="scroll-mt-24 space-y-3" aria-label={copy.commands}>
      <h2 className="text-xl font-bold">{copy.commandTitle}</h2>
      <p className="leading-7">{copy.commandHelp}</p>
      <ul className="space-y-2">{commands.map((entry) => {
        const article = seriesArticle(entry.article);
        return article ? <li key={entry.command} className="rounded-xl border border-[var(--line)] p-3"><a href={seriesHref(article.slug, entry.anchor)} className={anchor}><code className="break-all">{entry.command}</code> · {entry.description}</a><p className="mt-1 text-sm text-[var(--muted)]">{entry.kind}</p></li> : null;
      })}</ul>
    </section>
  </section>;
}
