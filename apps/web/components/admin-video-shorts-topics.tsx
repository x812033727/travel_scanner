"use client";

import { useTranslations } from "next-intl";
import { type FormEvent, useCallback, useMemo, useRef, useState } from "react";
import { AdminEmptyState, AdminErrorState, AdminStatusPill } from "@/components/admin-ui";
import { useRefresh, useWhen } from "@/components/admin-video-review-card";
import {
  type AssetNeed, type AssetPart, EDITABLE_TOPICS, message, PART_BYTES, PROTOCOL_FIELDS, sha256Hex, SHORTS_LINES, type ShortsLine, shrinkImage,
  type Topic, type TopicsWritten, topicTone,
} from "@/components/admin-video-shorts-data";
import { Button, fieldClass } from "@/components/community/ui";
import { api } from "@/lib/api";

// The topic library of the Shorts tab (docs/videos/SHORTS.md, the sections on the tab and the three
// lines): the topics grouped by line in the order they are made, each with its spec, what it still
// waits for and the box for the owner's material; an idea in a sentence; and the fifteen-topic
// campaign imported from its campaign.json. The server decides every status (topics.py settle):
// the page shows it and never works it out itself.

const PATH = "/admin/video-shorts/topics";
const REQUIREMENTS = ["vision", "image_edit", "sandbox", "image_generation"] as const;

const editable = (topic: Topic) => EDITABLE_TOPICS.includes(topic.status);

/**
 * The release order that puts a topic before every other one of its line still to be made, and the
 * topics that must move one place back first because nothing is left below them. The pool is made
 * in release order, the unordered ones last (topics.py order_key).
 */
export function frontOrder(topic: Topic, topics: Topic[]): { order: number; shift: Topic[] } {
  const others = topics.filter((each) => each.slug !== topic.slug && each.line === topic.line && editable(each) && each.release_order !== null);
  if (others.length === 0) return { order: topic.release_order ?? 0, shift: [] };
  const first = Math.min(...others.map((each) => each.release_order ?? 0));
  // Already before all of them: it stays where it is.
  if (topic.release_order !== null && topic.release_order < first) return { order: topic.release_order, shift: [] };
  if (first > 0) return { order: first - 1, shift: [] };
  return { order: 0, shift: others };
}

/** "Add an idea": a sentence and its line, kept as an idea the planner completes on its next round. */
function IdeaForm({ onAdded }: { onAdded: () => void }) {
  const t = useTranslations("admin.videoShorts");
  const [text, setText] = useState("");
  const [line, setLine] = useState<ShortsLine>("lab");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [saved, setSaved] = useState(false);
  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setBusy(true);
    setError("");
    setSaved(false);
    try {
      await api<Topic>(PATH, { method: "POST", body: JSON.stringify({ title: text.trim(), line }) });
      setText("");
      setSaved(true);
      onAdded();
    } catch (problem) {
      setError(t("topics.idea.error", { message: message(problem) }));
    } finally {
      setBusy(false);
    }
  };
  return <form onSubmit={(event) => void submit(event)} aria-label={t("topics.idea.title")} className="grid gap-3 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4">
    <h3 className="font-bold">{t("topics.idea.title")}</h3>
    <p className="text-sm leading-6 text-[var(--muted)]">{t("topics.idea.help")}</p>
    <label className="block text-sm font-semibold">{t("topics.idea.text")}
      <textarea className={fieldClass} rows={2} maxLength={200} value={text} disabled={busy} onChange={(event) => { setText(event.target.value); setSaved(false); }} />
    </label>
    <label className="block text-sm font-semibold md:w-1/2">{t("topics.idea.line")}
      <select className={fieldClass} value={line} disabled={busy} onChange={(event) => setLine(event.target.value as ShortsLine)}>
        {SHORTS_LINES.map((each) => <option key={each} value={each}>{t(`lines.${each}`)}</option>)}
      </select>
    </label>
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    {saved && <p role="status" className="text-sm text-[var(--teal)]">{t("topics.idea.saved")}</p>}
    <div><Button type="submit" disabled={busy || !text.trim()}>{busy ? t("saving") : t("topics.idea.submit")}</Button></div>
  </form>;
}

/** The campaign's fifteen topics, sent as campaign.json holds them; topics already in the library are skipped. */
function CampaignImport({ onImported }: { onImported: () => void }) {
  const t = useTranslations("admin.videoShorts");
  const input = useRef<HTMLInputElement>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<TopicsWritten | null>(null);
  const send = async (file: File) => {
    setBusy(true);
    setError("");
    setResult(null);
    try {
      const text = await file.text();
      try {
        JSON.parse(text);
      } catch {
        setError(t("topics.import.notJson"));
        return;
      }
      setResult(await api<TopicsWritten>(`${PATH}/import`, { method: "POST", body: text }));
      onImported();
    } catch (problem) {
      setError(t("topics.import.error", { message: message(problem) }));
    } finally {
      setBusy(false);
      if (input.current) input.current.value = "";
    }
  };
  return <div className="grid gap-3 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4">
    <h3 className="font-bold">{t("topics.import.title")}</h3>
    <p className="text-sm leading-6 text-[var(--muted)]">{t("topics.import.help")}</p>
    <input ref={input} type="file" accept="application/json,.json" className="sr-only" aria-label={t("topics.import.file")} disabled={busy}
      onChange={(event) => { const file = event.target.files?.[0]; if (file) void send(file); }} />
    <div><Button secondary disabled={busy} onClick={() => input.current?.click()}>{busy ? t("topics.import.busy") : t("topics.import.button")}</Button></div>
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    {result && <p role="status" className="text-sm text-[var(--teal)]">{t("topics.import.done", { created: result.created, skipped: result.skipped })}</p>}
  </div>;
}

/** One thing the owner supplies for a topic: what is in, and the upload with who made it and on what terms. */
function NeedBox({ topic, need, canManage, onTopic }: { topic: Topic; need: AssetNeed; canManage: boolean; onTopic: (topic: Topic) => void }) {
  const t = useTranslations("admin.videoShorts");
  const [file, setFile] = useState<File | null>(null);
  const [author, setAuthor] = useState("");
  const [takenOn, setTakenOn] = useState("");
  const [rights, setRights] = useState("");
  const [progress, setProgress] = useState<{ part: number; parts: number } | null>(null);
  const [error, setError] = useState("");
  const [done, setDone] = useState(false);
  const fileInput = useRef<HTMLInputElement>(null);
  const have = topic.assets.filter((asset) => asset.need === need.key);
  const count = need.count ?? 1;
  const ready = Boolean(file && author.trim() && takenOn && rights.trim());
  const upload = async (event: FormEvent) => {
    event.preventDefault();
    if (!file || !ready) return;
    setError("");
    setDone(false);
    setProgress({ part: 0, parts: 1 });
    try {
      const { blob, filename } = await shrinkImage(file);
      const sha256 = await sha256Hex(blob);
      const parts = Math.max(1, Math.ceil(blob.size / PART_BYTES));
      let answer: AssetPart | null = null;
      for (let part = 0; part < parts; part += 1) {
        setProgress({ part: part + 1, parts });
        const query = new URLSearchParams({
          sha256, part: String(part), parts: String(parts), size: String(blob.size), need: need.key, filename,
          author: author.trim(), rights_note: rights.trim(), taken_on: takenOn,
        });
        answer = await api<AssetPart>(`${PATH}/${topic.slug}/assets?${query}`, {
          method: "POST", headers: { "Content-Type": "application/octet-stream" }, body: blob.slice(part * PART_BYTES, (part + 1) * PART_BYTES),
        });
      }
      if (answer?.topic) onTopic(answer.topic);
      setFile(null);
      if (fileInput.current) fileInput.current.value = "";
      setDone(true);
    } catch (problem) {
      setError(t("topics.assets.error", { message: message(problem) }));
    } finally {
      setProgress(null);
    }
  };
  return <section aria-label={need.label} className="grid gap-2 rounded-xl border border-[var(--line)] p-3">
    <p className="flex flex-wrap items-center gap-2 text-sm"><span className="font-semibold">{need.label}</span>
      <AdminStatusPill status={have.length >= count ? "ok" : "warning"}>{t("topics.assets.count", { have: have.length, count })}</AdminStatusPill>
    </p>
    {have.length > 0 && <ul className="grid gap-1 text-sm">{have.map((asset) => <li key={asset.id} className="break-words">
      <span className="font-mono text-xs">{asset.filename}</span> · {t("topics.assets.madeBy", { author: asset.author })}{asset.taken_on && ` · ${asset.taken_on}`} · <span className="text-[var(--muted)]">{asset.rights_note}</span>
    </li>)}</ul>}
    {canManage && <form onSubmit={(event) => void upload(event)} className="grid gap-2 md:grid-cols-2">
      <label className="block text-sm font-semibold">{t("topics.assets.file")}
        <input ref={fileInput} type="file" accept="image/png,image/jpeg,image/webp" className={fieldClass} disabled={Boolean(progress)} onChange={(event) => { setFile(event.target.files?.[0] ?? null); setDone(false); }} />
      </label>
      <label className="block text-sm font-semibold">{t("topics.assets.author")}
        <input className={fieldClass} maxLength={120} value={author} required disabled={Boolean(progress)} onChange={(event) => setAuthor(event.target.value)} />
      </label>
      <label className="block text-sm font-semibold">{t("topics.assets.takenOn")}
        <input type="date" className={fieldClass} value={takenOn} required disabled={Boolean(progress)} onChange={(event) => setTakenOn(event.target.value)} />
      </label>
      <label className="block text-sm font-semibold md:col-span-2">{t("topics.assets.rights")}
        <textarea className={fieldClass} rows={2} maxLength={2000} value={rights} required disabled={Boolean(progress)} onChange={(event) => setRights(event.target.value)} />
      </label>
      <p className="text-xs leading-5 text-[var(--muted)] md:col-span-2">{t("topics.assets.help")}</p>
      {error && <p role="alert" className="text-sm text-red-800 md:col-span-2">{error}</p>}
      {done && <p role="status" className="text-sm text-[var(--teal)] md:col-span-2">{t("topics.assets.done")}</p>}
      <div className="md:col-span-2"><Button type="submit" disabled={!ready || Boolean(progress)}>{progress ? t("topics.assets.sending", { part: progress.part, parts: progress.parts }) : t("topics.assets.upload")}</Button></div>
    </form>}
  </section>;
}

/** The spec the topic is made from: the protocol, the truth check, what makes it done. */
function Spec({ topic }: { topic: Topic }) {
  const t = useTranslations("admin.videoShorts");
  const brief = topic.brief ?? {};
  const protocol = brief.test_protocol ?? {};
  const lines = (title: string, items: string[] | undefined) => <div className="grid gap-1">
    <h4 className="text-xs font-black tracking-[.12em] text-[var(--teal)]">{title}</h4>
    {items && items.length > 0 ? <ul className="grid list-disc gap-1 pl-5">{items.map((item, index) => <li key={index}>{item}</li>)}</ul> : <p className="text-[var(--muted)]">{t("topics.spec.none")}</p>}
  </div>;
  return <div className="grid gap-3 rounded-xl bg-[var(--paper)] p-4 text-sm leading-6" aria-label={t("topics.spec.title", { title: topic.title })}>
    {topic.line === "lab" ? <>
      <div className="grid gap-1">
        <h4 className="text-xs font-black tracking-[.12em] text-[var(--teal)]">{t("topics.spec.protocol")}</h4>
        <dl className="grid gap-1 md:grid-cols-[10rem_1fr]">{PROTOCOL_FIELDS.map((field) => <div key={field} className="contents">
          <dt className="font-semibold">{t(`topics.protocol.${field}`)}</dt>
          <dd className={protocol[field] ? "whitespace-pre-wrap" : "text-[var(--muted)]"}>{protocol[field] || t("topics.spec.missing")}</dd>
        </div>)}</dl>
      </div>
      {lines(t("topics.spec.truthCheck"), brief.truth_check)}
      {lines(t("topics.spec.acceptance"), brief.acceptance)}
    </> : <p>{topic.source_slug ? t("topics.spec.source", { slug: topic.source_slug }) : t("topics.spec.noSource")}</p>}
    {brief.requires && brief.requires.length > 0 && <p>{t("topics.spec.requires")} {brief.requires.map((name) => ((REQUIREMENTS as readonly string[]).includes(name) ? t(`topics.requires.${name as (typeof REQUIREMENTS)[number]}`) : name)).join("、")}</p>}
    {brief.notes && <p className="whitespace-pre-wrap">{brief.notes}</p>}
  </div>;
}

function TopicCard({ topic, canManage, busy, onAct, onTopic }: {
  topic: Topic; canManage: boolean; busy: boolean;
  onAct: (topic: Topic, action: "front" | "drop" | "restore") => void; onTopic: (topic: Topic) => void;
}) {
  const t = useTranslations("admin.videoShorts");
  const when = useWhen();
  const [open, setOpen] = useState(false);
  const takes = editable(topic);
  return <li className="grid gap-3 rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-4 shadow-[var(--shadow-sm)]" aria-label={topic.title}>
    <div className="flex flex-wrap items-center gap-2">
      <span className="font-bold">{topic.title}</span>
      <AdminStatusPill status={topicTone[topic.status]}>{t(`topics.statuses.${topic.status}`)}</AdminStatusPill>
      <AdminStatusPill status="inactive">{t(`topics.origins.${topic.origin}`)}</AdminStatusPill>
      {topic.paid && <AdminStatusPill status="pending">{t("topics.paid")}</AdminStatusPill>}
    </div>
    <p className="text-sm text-[var(--muted)]">{[
      topic.series && t("library.series", { series: topic.series }),
      topic.release_order !== null && t("topics.order", { order: topic.release_order }),
      topic.project_slug && t("topics.project", { slug: topic.project_slug }),
      t("topics.updated", { time: when(topic.updated_at) }),
    ].filter(Boolean).join(" · ")}</p>
    {topic.hook && <p className="text-sm leading-6"><span className="font-semibold">{t("topics.hook")}</span> {topic.hook}</p>}
    {takes && topic.waiting_for.length > 0 && <div className="grid gap-1 rounded-xl border border-amber-600 bg-amber-50 p-3 text-sm leading-6">
      <p className="font-semibold">{t("topics.waitingFor")}</p>
      <ul className="grid list-disc gap-1 pl-5">{topic.waiting_for.map((reason) => <li key={reason}>{reason}</li>)}</ul>
    </div>}
    {topic.note && <p className="text-sm text-[var(--muted)]">{t("topics.note", { note: topic.note })}</p>}
    <div className="flex flex-wrap gap-2">
      <Button secondary aria-expanded={open} onClick={() => setOpen((current) => !current)}>{open ? t("topics.hideSpec") : t("topics.showSpec")}</Button>
      {canManage && takes && <Button secondary disabled={busy} onClick={() => onAct(topic, "front")}>{t("topics.front")}</Button>}
      {canManage && takes && <Button secondary disabled={busy} onClick={() => onAct(topic, "drop")}>{t("topics.drop")}</Button>}
      {canManage && topic.status === "dropped" && <Button secondary disabled={busy} onClick={() => onAct(topic, "restore")}>{t("topics.restore")}</Button>}
    </div>
    {open && <Spec topic={topic} />}
    {takes && topic.assets_needed.length > 0 && <div className="grid gap-2" aria-label={t("topics.assets.title", { title: topic.title })}>
      <h4 className="text-xs font-black tracking-[.12em] text-[var(--teal)]">{t("topics.assets.box")}</h4>
      {topic.assets_needed.map((need) => <NeedBox key={need.key} topic={topic} need={need} canManage={canManage} onTopic={onTopic} />)}
    </div>}
  </li>;
}

export function ShortsTopics({ canManage }: { canManage: boolean }) {
  const t = useTranslations("admin.videoShorts");
  const [topics, setTopics] = useState<Topic[] | null>(null);
  const [error, setError] = useState("");
  const [actionError, setActionError] = useState("");
  const [busy, setBusy] = useState(false);
  const load = useCallback(() => {
    api<{ items: Topic[] }>(PATH).then((value) => { setTopics(value.items); setError(""); }).catch((problem: unknown) => setError(message(problem)));
  }, []);
  useRefresh(load);
  const groups = useMemo(() => SHORTS_LINES.map((line) => ({ line, items: (topics ?? []).filter((topic) => topic.line === line) })).filter((group) => group.items.length > 0), [topics]);
  const replace = useCallback((changed: Topic) => setTopics((current) => current?.map((each) => (each.slug === changed.slug ? changed : each)) ?? current), []);
  const patch = (slug: string, body: Record<string, unknown>) => api<Topic>(`${PATH}/${slug}`, { method: "PATCH", body: JSON.stringify(body) });
  const act = async (topic: Topic, action: "front" | "drop" | "restore") => {
    if (action === "drop" && !window.confirm(t("topics.dropConfirm", { title: topic.title }))) return;
    setBusy(true);
    setActionError("");
    try {
      if (action === "front") {
        const { order, shift } = frontOrder(topic, topics ?? []);
        for (const other of shift) replace(await patch(other.slug, { release_order: (other.release_order ?? 0) + 1 }));
        replace(await patch(topic.slug, { release_order: order }));
      } else {
        replace(await patch(topic.slug, { dropped: action === "drop" }));
      }
      load();
    } catch (problem) {
      setActionError(t("topics.actionError", { message: message(problem) }));
    } finally {
      setBusy(false);
    }
  };
  if (error) return <AdminErrorState title={t("loadError")} detail={error} retry={load} retryLabel={t("retry")} />;
  if (!topics) return <p className="text-[var(--muted)]">{t("loading")}</p>;
  return <div className="grid gap-6" aria-label={t("views.topics")}>
    <p className="text-sm leading-6 text-[var(--muted)]">{t("topics.help")}</p>
    {canManage && <div className="grid gap-4 md:grid-cols-2"><IdeaForm onAdded={load} /><CampaignImport onImported={load} /></div>}
    {actionError && <p role="alert" className="text-sm text-red-800">{actionError}</p>}
    {groups.length === 0 ? <AdminEmptyState title={t("topics.empty")} detail={t("topics.emptyDetail")} /> : groups.map(({ line, items }) => <section key={line} aria-label={t(`lines.${line}`)} className="grid gap-3">
      <h2 className="text-xs font-black tracking-[.16em] text-[var(--teal)]">{t(`lines.${line}`)} · {items.length}</h2>
      <ul className="grid gap-4">{items.map((topic) => <TopicCard key={topic.slug} topic={topic} canManage={canManage} busy={busy} onAct={(each, action) => void act(each, action)} onTopic={replace} />)}</ul>
    </section>)}
  </div>;
}
