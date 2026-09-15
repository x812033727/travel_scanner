"use client";

import { useState } from "react";
import type { GeminiSeriesCopy } from "@/lib/gemini-series-copy";
import { filterVisibleGeminiLessons, visibleGeminiHref, type GeminiStage, type GeminiTrack, type VisibleGeminiSeries } from "@/lib/gemini-series-projection";

const anchor = "text-[var(--teal)] underline underline-offset-4 [overflow-wrap:anywhere]";
const control = "min-h-11 min-w-0 w-full rounded-lg border border-[var(--line)] bg-[var(--surface)] px-2";

/** The server supplies the entire allowed list; there is no catalogue or feature-flag lookup here. */
export function GeminiDirectory({ series, copy }: { series: VisibleGeminiSeries; copy: GeminiSeriesCopy }) {
  const [query, setQuery] = useState("");
  const [group, setGroup] = useState("");
  const [path, setPath] = useState("");
  const [stage, setStage] = useState<GeminiStage>();
  const [track, setTrack] = useState<GeminiTrack>();
  const filters = { query, group, path, stage, track };
  const articles = filterVisibleGeminiLessons(series, filters);
  const numbers = new Set(articles.map(article => article.number));
  const commandNumbers = new Set(filterVisibleGeminiLessons(series, { ...filters, query: "" }).map(article => article.number));
  const words = query.normalize("NFKC").trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
  const commands = series.commands.filter(entry => commandNumbers.has(entry.article)
    && words.every(word => `${entry.command} ${entry.description} ${entry.kind}`.normalize("NFKC").toLocaleLowerCase().includes(word)));
  const routes = series.paths.filter(entry => (!path || entry.id === path) && (!stage || entry.stage === stage))
    .map(entry => ({ ...entry, articles: entry.articles.filter(number => numbers.has(number)) })).filter(entry => entry.articles.length);
  const tracks = [...new Set(series.articles.flatMap(article => article.track ? [article.track] : []))];

  return <section id="series-directory" aria-label={copy.directory} className="min-w-0 scroll-mt-24 space-y-7 [overflow-wrap:anywhere]" data-testid="gemini-series-index">
    <div className="space-y-4 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4 sm:p-6">
      <h2 className="text-xl font-bold">{copy.find}</h2>
      <label className="grid min-w-0 gap-2 text-sm font-semibold">{copy.search}
        <input type="search" value={query} onChange={event => setQuery(event.target.value)} placeholder={copy.placeholder} className={control} />
      </label>
      <div className="grid min-w-0 gap-3 sm:grid-cols-2">
        <label className="grid min-w-0 gap-2 text-sm">{copy.group}<select value={group} onChange={event => setGroup(event.target.value)} className={control}><option value="">{copy.allGroups}</option>{series.groups.map(entry => <option key={entry.id} value={entry.id}>{entry.title}</option>)}</select></label>
        <label className="grid min-w-0 gap-2 text-sm">{copy.path}<select value={path} onChange={event => setPath(event.target.value)} className={control}><option value="">{copy.allPaths}</option>{series.paths.map(entry => <option key={entry.id} value={entry.id}>{entry.title}</option>)}</select></label>
        {series.advancedEnabled ? <>
          <label className="grid min-w-0 gap-2 text-sm">{copy.stage}<select value={stage ?? ""} onChange={event => setStage(event.target.value ? Number(event.target.value) as GeminiStage : undefined)} className={control}><option value="">{copy.allStages}</option><option value="1">{copy.baseStage}</option><option value="2">{copy.advancedStage}</option></select></label>
          <label className="grid min-w-0 gap-2 text-sm">{copy.track}<select value={track ?? ""} onChange={event => setTrack((event.target.value || undefined) as GeminiTrack | undefined)} className={control}><option value="">{copy.allTracks}</option>{tracks.map(value => <option key={value} value={value}>{copy.tracks[value]}</option>)}</select></label>
        </> : null}
      </div>
      <button type="button" onClick={() => { setQuery(""); setGroup(""); setPath(""); setStage(undefined); setTrack(undefined); }} className={`min-h-11 ${anchor}`}>{copy.clear}</button>
      <p role="status" className="text-sm text-[var(--muted)]">{copy.count.replace("{count}", String(articles.length)).replace("{total}", String(series.articles.length))}</p>
    </div>
    <nav aria-label={copy.suggestedPaths} className="space-y-4">
      <h2 className="text-xl font-bold">{copy.byGoal}</h2>
      {routes.map(entry => <details key={entry.id} open={Boolean(path)} className="min-w-0 rounded-xl border border-[var(--line)] p-4">
        <summary className="cursor-pointer py-2 font-semibold">{entry.title} · {entry.articles.length} {copy.lessons}</summary>
        <p className="my-3 leading-7 text-[var(--muted)]">{entry.description}</p>
        <ol className="list-decimal space-y-2 pl-5">{entry.articles.map(number => {
          const article = series.articles.find(item => item.number === number);
          return article ? <li key={number}><a href={visibleGeminiHref(series, article.slug)} className={anchor}>{article.title}</a></li> : null;
        })}</ol>
      </details>)}
    </nav>
    <div className="space-y-7" data-testid="series-lessons">
      {series.groups.map(entry => {
        const members = articles.filter(article => article.group === entry.id);
        return members.length ? <section key={entry.id} id={`chapter-${entry.id.toLowerCase()}`} className="scroll-mt-24 space-y-3">
          <h2 className="text-xl font-bold">{entry.id}. {entry.title}</h2>
          <ol className="grid gap-3">{members.map(article => <li key={article.slug} className="min-w-0 rounded-xl border border-[var(--line)] p-4">
            <a href={visibleGeminiHref(series, article.slug)} className={`block text-lg font-semibold ${anchor}`}><span className="mr-2 font-mono text-sm">{String(article.number).padStart(2, "0")}</span>{article.title}</a>
            <p className="mt-2 leading-7">{copy.outcome}{article.purpose}</p>
            <p className="mt-2 flex flex-wrap gap-x-3 gap-y-1 text-sm text-[var(--muted)]"><span>{article.level}</span><span>{article.platforms.join("、")}</span><span>{copy.minutes.replace("{minutes}", String(article.minutes))}</span>{article.stage === 2 ? <><span>{copy.advancedStage}</span><span>{article.track ? copy.tracks[article.track] : null}</span><span>{copy.labMinutes.replace("{minutes}", String(article.labMinutes))}</span></> : null}</p>
          </li>)}</ol>
        </section> : null;
      })}
      {!articles.length ? <p className="leading-7">{copy.noResults}</p> : null}
    </div>
    <section id="commands" className="scroll-mt-24 space-y-3" aria-label={copy.commands}>
      <h2 className="text-xl font-bold">{copy.commandTitle}</h2><p className="leading-7">{copy.commandHelp}</p>
      <ul className="space-y-2">{commands.map(entry => {
        const article = series.articles.find(item => item.number === entry.article);
        return article ? <li key={`${entry.command}-${entry.article}`} className="min-w-0 rounded-xl border border-[var(--line)] p-3"><a href={visibleGeminiHref(series, article.slug, entry.anchor)} className={anchor}><code className="break-all">{entry.command}</code> · {entry.description}</a><p className="mt-1 text-sm text-[var(--muted)]">{entry.kind}</p></li> : null;
      })}</ul>
      {!commands.length ? <p>{copy.noCommands}</p> : null}
    </section>
  </section>;
}
