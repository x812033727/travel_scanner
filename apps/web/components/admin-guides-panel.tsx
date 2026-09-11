"use client";

import { useCallback, useEffect, useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import { AdminReadOnlyNotice, useAdminActionGuard } from "@/components/admin-action-guard";
import { Button, Dialog } from "@/components/community/ui";
import { ContentBlocks } from "@/components/content-blocks";
import { api, ApiError } from "@/lib/api";
import type { ContentBlock } from "@/lib/content-blocks";
import { useNavigationGuard } from "@/lib/navigation-guard";
import { guideKinds, type GuideDocument, type GuideKind, type GuideSource, type GuideTopic } from "@/lib/guides";
import { sitePageLocales, type SitePageLocale } from "@/lib/site-pages";

const control = "min-h-11 w-full rounded-xl border border-[var(--control-border,var(--line))] bg-[var(--surface)] px-3 py-2 text-[var(--ink)]";
const languages: Record<SitePageLocale, string> = { "zh-TW": "繁體中文", "zh-CN": "简体中文", en: "English", ja: "日本語", ko: "한국어" };

type LocaleState = {
  locale: SitePageLocale; version: number; published_version: number | null;
  published_at: string | null; title: string; updated_at: string;
};
type Revision = { id: string; version: number; action: string; created_at: string };
type ArticleSummary = {
  id: string; slug: string; kind: GuideKind; destination_id: string | null;
  destination_label: string | null; topics: GuideTopic[]; valid_until: string | null;
  expired: boolean; featured: boolean; display_order: number; is_active: boolean;
  version: number; locales: LocaleState[]; updated_at: string;
};
type ArticleDetail = ArticleSummary & {
  locale: SitePageLocale; draft: GuideDocument;
  published: (GuideDocument & { version: number; published_at: string }) | null;
  revisions: Revision[];
};

const emptyDocument = (): GuideDocument => ({
  title: "", description: "", blocks: [{ type: "paragraph", text: "" }], sources: [],
});

export function AdminGuidesPanel() {
  const t = useTranslations("admin.guides");
  const interfaceLocale = useLocale();
  const manage = useAdminActionGuard("content.manage");
  const [articles, setArticles] = useState<ArticleSummary[]>();
  const [topics, setTopics] = useState<GuideTopic[]>([]);
  const [selected, setSelected] = useState<string | null>(null);
  const [locale, setLocale] = useState<SitePageLocale>(
    sitePageLocales.includes(interfaceLocale as SitePageLocale) ? (interfaceLocale as SitePageLocale) : "zh-TW",
  );
  const [detail, setDetail] = useState<ArticleDetail | null>();
  const [draft, setDraft] = useState<GuideDocument | null>(null);
  const [reload, setReload] = useState(0);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [preview, setPreview] = useState<GuideDocument | null>(null);
  const [gate, setGate] = useState<"publish" | "unpublish" | null>(null);
  const [confirmed, setConfirmed] = useState(false);
  const [reason, setReason] = useState("");
  const [restoreReason, setRestoreReason] = useState("");
  const [creating, setCreating] = useState(false);
  const [newSlug, setNewSlug] = useState("");
  const [newKind, setNewKind] = useState<GuideKind>("howto");

  const dirty = Boolean(draft && detail && JSON.stringify(draft) !== JSON.stringify(detail.draft));
  const requestLeave = useCallback((proceed: () => void) => {
    if (busy || (dirty && !window.confirm(t("discard")))) return false;
    proceed(); return true;
  }, [busy, dirty, t]);
  useNavigationGuard(dirty || busy, requestLeave);

  const showError = (problem: unknown) => setError(
    problem instanceof ApiError && problem.code === "guide_version_conflict" ? t("conflict")
      : problem instanceof Error ? problem.message : t("error"),
  );
  const suffix = `?locale=${encodeURIComponent(locale)}`;
  const row = detail?.locales.find((entry) => entry.locale === locale) ?? null;

  useEffect(() => {
    const controller = new AbortController();
    Promise.all([
      api<{ articles: ArticleSummary[] }>(`/admin/guides${suffix}`, { signal: controller.signal }),
      api<{ topics: GuideTopic[] }>(`/admin/guides/topics${suffix}`, { signal: controller.signal }),
    ]).then(([list, vocabulary]) => {
      if (controller.signal.aborted) return;
      setArticles(list.articles);
      setTopics(vocabulary.topics);
    }).catch((problem: unknown) => {
      if (!controller.signal.aborted) { setArticles([]); showError(problem); }
    });
    return () => controller.abort();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [suffix, reload]);

  // The loading and empty states are set where the selection actually changes -- an event
  // handler -- so this effect only fetches.
  useEffect(() => {
    if (!selected) return;
    const controller = new AbortController();
    api<ArticleDetail>(`/admin/guides/${selected}${suffix}`, { signal: controller.signal })
      .then((value) => {
        if (controller.signal.aborted) return;
        setDetail(value); setDraft(value.draft);
      })
      .catch((problem: unknown) => {
        if (controller.signal.aborted) return;
        // A language nobody has started is not an error; it is an offer to start one.
        if (problem instanceof ApiError && problem.code === "guide_locale_not_found") {
          setDetail(null); setDraft(null);
        } else { setDetail(null); showError(problem); }
      });
    return () => controller.abort();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selected, suffix, reload]);

  function change(apply: () => void) {
    requestLeave(() => { setError(""); setNotice(""); apply(); });
  }

  /** Switching article or language throws away the open draft, so it clears it here. */
  function reselect(apply: () => void, hasTarget: boolean) {
    change(() => { setDetail(hasTarget ? undefined : null); setDraft(null); apply(); });
  }

  async function run(work: () => Promise<void>) {
    if (!manage.allowed || busy) return;
    setBusy(true); setError("");
    try { await work(); } catch (problem) { showError(problem); } finally { setBusy(false); }
  }

  const refresh = (value: ArticleDetail) => {
    setDetail(value); setDraft(value.draft);
    setArticles((current) => current?.map((entry) => (entry.id === value.id ? { ...entry, ...value } : entry)));
  };

  const create = () => run(async () => {
    const value = await api<ArticleDetail>("/admin/guides", {
      method: "POST",
      body: JSON.stringify({ slug: newSlug, kind: newKind, topics: [], document: emptyDocument(), locale }),
    });
    setCreating(false); setNewSlug("");
    setArticles((current) => [value, ...(current ?? [])]);
    setSelected(value.id); setDetail(value); setDraft(value.draft);
    setNotice(t("saved"));
  });

  const startTranslation = () => run(async () => {
    const value = await api<ArticleDetail>(`/admin/guides/${selected}/${locale}`, {
      method: "POST", body: JSON.stringify(emptyDocument()),
    });
    refresh(value); setNotice(t("saved"));
  });

  const save = () => run(async () => {
    if (!detail || !draft || !row) return;
    refresh(await api<ArticleDetail>(`/admin/guides/${detail.id}/${locale}/draft`, {
      method: "PUT", body: JSON.stringify({ expected_version: row.version, document: draft }),
    }));
    setNotice(t("saved"));
  });

  const gated = (action: "publish" | "unpublish") => run(async () => {
    if (!detail || !row || !confirmed || !reason.trim()) return;
    refresh(await api<ArticleDetail>(`/admin/guides/${detail.id}/${locale}/${action}`, {
      method: "POST", body: JSON.stringify({ expected_version: row.version, confirmed: true, reason }),
    }));
    setGate(null); setConfirmed(false); setReason("");
    setNotice(t(action === "publish" ? "publishSuccess" : "unpublishSuccess"));
  });

  const saveTaxonomy = () => run(async () => {
    if (!detail) return;
    refresh(await api<ArticleDetail>(`/admin/guides/${detail.id}${suffix}`, {
      method: "PUT",
      body: JSON.stringify({
        expected_version: detail.version, kind: detail.kind, destination_id: detail.destination_id,
        topics: detail.topics.map((topic) => topic.slug), valid_until: detail.valid_until,
        featured: detail.featured, display_order: detail.display_order, is_active: detail.is_active,
      }),
    }));
    setNotice(t("taxonomySaved"));
  });

  const viewRevision = (id: string) => run(async () => {
    if (!detail) return;
    const result = await api<{ document: GuideDocument }>(`/admin/guides/${detail.id}/${locale}/revisions/${id}`);
    setPreview(result.document);
  });

  const restore = (id: string) => run(async () => {
    if (!detail || !row || !restoreReason.trim() || !window.confirm(t("restoreConfirm"))) return;
    refresh(await api<ArticleDetail>(`/admin/guides/${detail.id}/${locale}/restore`, {
      method: "POST",
      body: JSON.stringify({ expected_version: row.version, revision_id: id, reason: restoreReason }),
    }));
    setNotice(t("restored"));
  });

  function updateBlock(index: number, block: ContentBlock) {
    if (draft) setDraft({ ...draft, blocks: draft.blocks.map((entry, i) => (i === index ? block : entry)) });
  }
  function moveBlock(index: number, offset: number) {
    if (!draft || index + offset < 0 || index + offset >= draft.blocks.length) return;
    const blocks = [...draft.blocks];
    [blocks[index], blocks[index + offset]] = [blocks[index + offset], blocks[index]];
    setDraft({ ...draft, blocks });
  }
  function updateSource(index: number, source: GuideSource) {
    if (draft) setDraft({ ...draft, sources: draft.sources.map((entry, i) => (i === index ? source : entry)) });
  }

  return <div className="space-y-6">
    <header>
      <h1 className="text-3xl font-bold">{t("title")}</h1>
      <p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">{t("intro")}</p>
    </header>
    <AdminReadOnlyNotice capability="content.manage" />

    <div className="grid gap-4 sm:grid-cols-2">
      <label className="grid gap-2">{t("articleList")}
        <select className={control} disabled={busy} value={selected ?? ""} onChange={(event) => reselect(() => setSelected(event.target.value || null), Boolean(event.target.value))}>
          <option value="">—</option>
          {(articles ?? []).map((article) => (
            <option key={article.id} value={article.id}>
              {article.slug} · {t(article.kind)}{article.is_active ? "" : ` · ${t("archived")}`}
            </option>
          ))}
        </select>
      </label>
      <label className="grid gap-2">{t("documentLanguage")}
        <select className={control} disabled={busy} value={locale} onChange={(event) => reselect(() => setLocale(event.target.value as SitePageLocale), Boolean(selected))}>
          {sitePageLocales.map((value) => <option key={value} value={value}>{languages[value]}</option>)}
        </select>
      </label>
    </div>
    <div className="flex flex-wrap gap-3">
      <Button secondary disabled={busy || !manage.allowed} onClick={() => change(() => setCreating(true))}>{t("newArticle")}</Button>
    </div>

    {articles?.length === 0 && <p role="status">{t("noArticles")}</p>}
    {error && <div role="alert" className="space-y-3">
      <p>{error}</p>
      <Button secondary disabled={busy} onClick={() => reselect(() => setReload((value) => value + 1), Boolean(selected))}>{t("reload")}</Button>
    </div>}
    {notice && <p role="status">{notice}</p>}
    {selected && detail === undefined && !error && <p role="status">{t("loading")}</p>}

    {selected && detail === null && !error && <section className="space-y-4 rounded-2xl border border-[var(--line)] p-5">
      <p>{t("noTranslation")}</p>
      <Button disabled={busy || !manage.allowed} onClick={() => void startTranslation()}>{t("addTranslation")}</Button>
    </section>}

    {detail && draft && row && <>
      <section className="space-y-4 rounded-2xl border border-[var(--line)] p-4">
        <h2 className="text-xl font-bold">{t("taxonomy")}</h2>
        <fieldset disabled={!manage.allowed || busy} className="grid gap-4 sm:grid-cols-2">
          <label className="grid gap-2">{t("kind")}
            <select className={control} value={detail.kind} onChange={(event) => setDetail({ ...detail, kind: event.target.value as GuideKind })}>
              {guideKinds.map((value) => <option key={value} value={value}>{t(value)}</option>)}
            </select>
          </label>
          <label className="grid gap-2">{t("destination")}
            <input className={control} value={detail.destination_id ?? ""} placeholder={t("noDestination")}
              onChange={(event) => setDetail({ ...detail, destination_id: event.target.value || null })} />
          </label>
          <label className="grid gap-2">{t("validUntil")}
            <input type="date" className={control} value={detail.valid_until ?? ""}
              onChange={(event) => setDetail({ ...detail, valid_until: event.target.value || null })} />
          </label>
          <label className="flex min-h-11 items-center gap-3">
            <input type="checkbox" checked={detail.featured} onChange={(event) => setDetail({ ...detail, featured: event.target.checked })} />{t("featured")}
          </label>
          <label className="flex min-h-11 items-center gap-3">
            <input type="checkbox" checked={detail.is_active} onChange={(event) => setDetail({ ...detail, is_active: event.target.checked })} />{t("active")}
          </label>
          <fieldset className="grid gap-2 sm:col-span-2">
            <legend className="font-semibold">{t("topics")}</legend>
            <div className="flex flex-wrap gap-2">
              {topics.map((topic) => {
                const on = detail.topics.some((entry) => entry.slug === topic.slug);
                return <label key={topic.slug} className="inline-flex min-h-11 items-center gap-2 rounded-full border border-[var(--line)] px-3">
                  <input type="checkbox" checked={on} onChange={(event) => setDetail({
                    ...detail,
                    topics: event.target.checked
                      ? [...detail.topics, topic]
                      : detail.topics.filter((entry) => entry.slug !== topic.slug),
                  })} />
                  {topic.label}
                </label>;
              })}
            </div>
          </fieldset>
        </fieldset>
        <p className="text-sm leading-7 text-[var(--muted)]">{t("validUntilHelp")}</p>
        <Button secondary disabled={busy || !manage.allowed} onClick={() => void saveTaxonomy()}>{t("saveTaxonomy")}</Button>
      </section>

      <div className="flex flex-wrap items-center gap-4 text-sm">
        <span>{t("draft")} · {t("revision")} {row.version}</span>
        <span>{row.published_version ? `${t("published")} · ${t("revision")} ${row.published_version}` : t("unpublished")}</span>
      </div>

      <form onSubmit={(event) => { event.preventDefault(); void save(); }} className="space-y-6">
        <fieldset disabled={!manage.allowed || busy} className="space-y-5">
          <label className="grid gap-2">{t("documentTitle")}
            <input className={control} required maxLength={200} value={draft.title} onChange={(event) => setDraft({ ...draft, title: event.target.value })} />
          </label>
          <label className="grid gap-2">{t("seoDescription")}
            <textarea className={control} required maxLength={500} value={draft.description} onChange={(event) => setDraft({ ...draft, description: event.target.value })} />
          </label>

          <div className="space-y-5">{draft.blocks.map((block, index) => <fieldset key={index} className="space-y-3 rounded-2xl border border-[var(--line)] p-4">
            <legend className="px-2 font-semibold">{t(block.type)} {index + 1}</legend>
            {block.type === "heading" && <label className="grid gap-2">{t("level")}
              <select className={control} value={block.level} onChange={(event) => updateBlock(index, { ...block, level: Number(event.target.value) as 2 | 3 })}>
                <option value={2}>2</option><option value={3}>3</option>
              </select>
            </label>}
            {block.type === "list" ? <>
              <label className="grid gap-2">{t("itemsHelp")}
                <textarea className={control} rows={4} value={block.items.join("\n")} onChange={(event) => updateBlock(index, { ...block, items: event.target.value.split("\n") })} />
              </label>
              <label className="flex min-h-11 items-center gap-3">
                <input type="checkbox" checked={block.ordered} onChange={(event) => updateBlock(index, { ...block, ordered: event.target.checked })} />{t("ordered")}
              </label>
            </> : <label className="grid gap-2">{t("text")}
              <textarea className={control} rows={block.type === "paragraph" ? 4 : 2} value={block.text} onChange={(event) => updateBlock(index, { ...block, text: event.target.value })} />
            </label>}
            {block.type === "link" && <label className="grid gap-2">{t("url")}
              <input className={control} value={block.url} onChange={(event) => updateBlock(index, { ...block, url: event.target.value })} />
            </label>}
            <div className="flex flex-wrap gap-2">
              <Button secondary disabled={index === 0} onClick={() => moveBlock(index, -1)}>{t("moveUp")}</Button>
              <Button secondary disabled={index === draft.blocks.length - 1} onClick={() => moveBlock(index, 1)}>{t("moveDown")}</Button>
              <Button secondary onClick={() => setDraft({ ...draft, blocks: draft.blocks.filter((_, i) => i !== index) })}>{t("removeBlock")}</Button>
            </div>
          </fieldset>)}</div>

          <div className="flex flex-wrap gap-2">{(["heading", "paragraph", "list", "link"] as const).map((type) =>
            <Button secondary key={type} onClick={() => setDraft({
              ...draft,
              blocks: [...draft.blocks, type === "list" ? { type, items: [""], ordered: false }
                : type === "heading" ? { type, level: 2 as const, text: "" }
                : type === "link" ? { type, text: "", url: "" } : { type, text: "" }],
            })}>{t("addBlock")} · {t(type)}</Button>)}
          </div>

          <section className="space-y-4 rounded-2xl border border-[var(--line)] p-4">
            <h2 className="text-xl font-bold">{t("sources")}</h2>
            {draft.sources.map((source, index) => <div key={index} className="grid gap-3 sm:grid-cols-3">
              <label className="grid gap-2">{t("sourceTitle")}
                <input className={control} value={source.title} onChange={(event) => updateSource(index, { ...source, title: event.target.value })} />
              </label>
              <label className="grid gap-2">{t("sourceUrl")}
                <input className={control} value={source.url} onChange={(event) => updateSource(index, { ...source, url: event.target.value })} />
              </label>
              <label className="grid gap-2">{t("sourceCheckedOn")}
                <input type="date" className={control} value={source.checked_on ?? ""} onChange={(event) => updateSource(index, { ...source, checked_on: event.target.value || null })} />
              </label>
              <Button secondary onClick={() => setDraft({ ...draft, sources: draft.sources.filter((_, i) => i !== index) })}>{t("removeSource")}</Button>
            </div>)}
            <Button secondary onClick={() => setDraft({ ...draft, sources: [...draft.sources, { title: "", url: "", checked_on: null }] })}>{t("addSource")}</Button>
          </section>
        </fieldset>

        <div className="sticky bottom-3 z-10 flex flex-wrap gap-3 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-3 shadow-sm">
          <Button type="submit" disabled={busy || !manage.allowed || !dirty}>{t("save")}</Button>
          <Button secondary disabled={busy} onClick={() => setPreview(draft)}>{t("preview")}</Button>
          <Button secondary disabled={busy || dirty || !manage.allowed} onClick={() => { setConfirmed(false); setReason(""); setGate("publish"); }}>{t("publish")}</Button>
          {row.published_version !== null && <Button secondary disabled={busy || !manage.allowed} onClick={() => { setConfirmed(false); setReason(""); setGate("unpublish"); }}>{t("unpublish")}</Button>}
        </div>
      </form>

      <section className="space-y-4">
        <h2 className="text-xl font-bold">{t("history")}</h2>
        <label className="grid gap-2">{t("restoreReason")}
          <input className={control} disabled={busy || !manage.allowed} value={restoreReason} onChange={(event) => setRestoreReason(event.target.value)} />
        </label>
        {!detail.revisions.length && <p>{t("noHistory")}</p>}
        <ul className="space-y-3">{detail.revisions.map((revision) => <li key={revision.id} className="flex flex-wrap items-center gap-3 rounded-xl border border-[var(--line)] p-3">
          <span>{t("revision")} {revision.version} · {revision.action}</span>
          <time className="text-sm text-[var(--muted)]" dateTime={revision.created_at}>{new Date(revision.created_at).toLocaleString(interfaceLocale)}</time>
          <Button secondary disabled={busy} onClick={() => void viewRevision(revision.id)}>{t("viewRevision")}</Button>
          <Button secondary disabled={busy || !manage.allowed || !restoreReason.trim()} onClick={() => void restore(revision.id)}>{t("restore")}</Button>
        </li>)}</ul>
      </section>
    </>}

    {creating && <Dialog title={t("newArticle")} onClose={() => { if (!busy) setCreating(false); }}>
      <div className="space-y-5">
        <label className="grid gap-2">{t("slug")}
          <input className={control} disabled={busy} value={newSlug} onChange={(event) => setNewSlug(event.target.value)} />
        </label>
        <p className="text-sm leading-7 text-[var(--muted)]">{t("slugHelp")}</p>
        <label className="grid gap-2">{t("kind")}
          <select className={control} disabled={busy} value={newKind} onChange={(event) => setNewKind(event.target.value as GuideKind)}>
            {guideKinds.map((value) => <option key={value} value={value}>{t(value)}</option>)}
          </select>
        </label>
        {error && <p role="alert">{error}</p>}
        <Button disabled={busy || !newSlug.trim()} onClick={() => void create()}>{t("newArticle")}</Button>
      </div>
    </Dialog>}

    {preview && <Dialog title={t("preview")} onClose={() => setPreview(null)}>
      {/* The reader's renderer, not a second one, so the preview cannot flatter the draft. */}
      <div lang={locale} className="space-y-6">
        <h1 className="text-3xl font-bold">{preview.title}</h1>
        <p className="leading-7 text-[var(--muted)]">{preview.description}</p>
        <ContentBlocks blocks={preview.blocks} />
      </div>
    </Dialog>}

    {gate && <Dialog title={t(gate === "publish" ? "confirmPublish" : "confirmUnpublish")} onClose={() => { if (!busy) setGate(null); }}>
      <div className="space-y-5">
        <p className="leading-7">{t(gate === "publish" ? "publishHelp" : "unpublishHelp")}</p>
        <label className="grid gap-2">{t("reason")}
          <input className={control} disabled={busy} value={reason} onChange={(event) => setReason(event.target.value)} />
        </label>
        <label className="flex min-h-11 items-start gap-3">
          <input type="checkbox" className="mt-1" disabled={busy} checked={confirmed} onChange={(event) => setConfirmed(event.target.checked)} />{t("confirmed")}
        </label>
        {error && <p role="alert">{error}</p>}
        <Button disabled={busy || !confirmed || !reason.trim()} onClick={() => void gated(gate)}>
          {t(gate === "publish" ? "confirmPublish" : "confirmUnpublish")}
        </Button>
      </div>
    </Dialog>}
  </div>;
}
