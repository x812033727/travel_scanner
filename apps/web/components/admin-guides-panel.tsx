"use client";

import { Fragment, useCallback, useEffect, useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import { AdminReadOnlyNotice, useAdminActionGuard } from "@/components/admin-action-guard";
import { AdminGuidesList, GuideVisibilityDialog, updateAdminQuery, visibilityError, type VisibilityAction } from "@/components/admin-guides-list";
import { Button, Dialog } from "@/components/community/ui";
import { ContentBlocks, type ContentBlockLabels } from "@/components/content-blocks";
import { useAdminQueryValue } from "@/lib/admin-workspace-navigation";
import { api, ApiError } from "@/lib/api";
import { calloutTones, type ImageBlock, type ImageCredit, type TableBlock } from "@/lib/content-blocks";
import { useNavigationGuard } from "@/lib/navigation-guard";
import {
  guideKinds, guideSection, offerModules, splitGuideBlocks,
  type GuideBlock, type GuideDocument, type GuideHero, type GuideKind, type GuideSource, type GuideTopic,
} from "@/lib/guides";
import { isUuid, type ArticleDetail, type ArticleSummary } from "@/lib/guides-admin";
import { sitePageLocales, type SitePageLocale } from "@/lib/site-pages";

const control = "min-h-11 w-full rounded-xl border border-[var(--control-border,var(--line))] bg-[var(--surface)] px-3 py-2 text-[var(--ink)]";
const languages: Record<SitePageLocale, string> = { "zh-TW": "繁體中文", "zh-CN": "简体中文", en: "English", ja: "日本語", ko: "한국어" };

const emptyDocument = (): GuideDocument => ({
  title: "", description: "", hero: null, blocks: [{ type: "paragraph", text: "" }], sources: [],
});
const isSiteLocale = (value: string): value is SitePageLocale => (sitePageLocales as readonly string[]).includes(value);

/** Every block an editor can add, in the order the buttons appear. */
const blockTypes = ["heading", "paragraph", "list", "link", "image", "table", "callout", "offer"] as const;
type BlockType = typeof blockTypes[number];

function newBlock(type: BlockType): GuideBlock {
  switch (type) {
    case "heading": return { type, level: 2, text: "" };
    case "list": return { type, items: [""], ordered: false };
    case "link": return { type, text: "", url: "" };
    case "image": return { type, src: "", alt: "", width: 1600, height: 900, caption: "", credit: null };
    case "table": return { type, header: ["", ""], rows: [["", ""]], caption: "" };
    case "callout": return { type, tone: "tip", title: "", text: "" };
    case "offer": return { type, module: "activities", destination_id: null, heading: "" };
    default: return { type: "paragraph", text: "" };
  }
}

const emptyCredit = (): ImageCredit => ({ author: "", license: "", source_url: null });
const emptyHero = (): GuideHero => ({ src: "", alt: "", width: 1600, height: 900, credit: null });

/** A credit with nothing in it is no credit; the API refuses blank author or licence. */
function packCredit(credit: ImageCredit): ImageCredit | null {
  return credit.author || credit.license || credit.source_url ? credit : null;
}

/** The table as the editor types it: header on the first line, cells split by `|`. Split and
 *  joined without trimming so the text round-trips exactly and the caret never jumps; the API
 *  strips each cell when the draft is saved. */
function tableText(block: TableBlock): string {
  return [block.header, ...block.rows].map((row) => row.join("|")).join("\n");
}

function parseTable(text: string): Pick<TableBlock, "header" | "rows"> {
  const [first = "", ...rest] = text.split("\n");
  return {
    header: first.split("|"),
    rows: rest.filter((line) => line !== "").map((line) => line.split("|")),
  };
}

const sizeValue = (value: string) => Math.max(0, Math.min(4000, Number.parseInt(value, 10) || 0));

/** How the affiliate modules are named everywhere else on the site (`travelServices`). */
const moduleLabelKeys: Record<typeof offerModules[number], string> = {
  flight: "affiliateFlight",
  hotel: "affiliateHotel",
  activities: "affiliateActivities",
  transport: "affiliateTransport",
  connectivity: "affiliateConnectivity",
};

/**
 * The URL owns the workspace: no `?article=` is the list, `?article=<id>&lang=<locale>` is
 * the editor for one translation. "Back to the list" therefore returns to the same filters,
 * and a filtered view or an open article can be bookmarked or shared.
 */
export function AdminGuidesPanel() {
  const t = useTranslations("admin.guides");
  const ts = useTranslations("travelServices");
  const interfaceLocale = useLocale();
  const manage = useAdminActionGuard("content.manage");
  const [selected] = useAdminQueryValue("article", "", isUuid);
  const [requestedLocale] = useAdminQueryValue("lang", "", isSiteLocale);
  const locale: SitePageLocale = isSiteLocale(requestedLocale) ? requestedLocale : isSiteLocale(interfaceLocale) ? interfaceLocale : "zh-TW";
  const [topics, setTopics] = useState<GuideTopic[]>([]);
  const [reload, setReload] = useState(0);
  // The loaded article is keyed by what it was loaded for, so a change of article, language
  // or reload shows the loading state without an effect having to reset anything.
  const key = `${selected}|${locale}|${reload}`;
  const [loaded, setLoaded] = useState<{ key: string; detail: ArticleDetail | null }>();
  const detail = loaded?.key === key ? loaded.detail : undefined;
  const setDetail = (value: ArticleDetail | null) => setLoaded({ key, detail: value });
  const [draft, setDraft] = useState<GuideDocument | null>(null);
  // What the editor has typed into each table so far, by block position. The parsed block is
  // what gets saved; the raw text is what stays on screen, so a half-typed row survives.
  const [tableDrafts, setTableDrafts] = useState<Record<number, string>>({});
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [preview, setPreview] = useState<GuideDocument | null>(null);
  const [gate, setGate] = useState<"publish" | "unpublish" | null>(null);
  const [visibility, setVisibility] = useState<VisibilityAction | null>(null);
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

  const showError = (problem: unknown) => setError(visibilityError(problem, t));
  const suffix = `?locale=${encodeURIComponent(locale)}`;
  // A topic may only be attached to an article of its own section; the API refuses the rest
  // with `guide_topic_section_mismatch`. A row served by an API that predates the column is
  // read as travel, which is what it was.
  const detailSection = detail ? guideSection(detail.kind) : "travel";
  const sectionTopics = topics.filter((topic) => (topic.section ?? "travel") === detailSection);
  // Kind is part of the URL, so moving an article between sections moves its URL. The API
  // refuses that with 409 once any translation is published; this mirrors it in the editor
  // rather than letting a save discover it.
  const kindLocked = Boolean(detail?.locales.some((entry) => entry.published_version !== null));
  const row = detail?.locales.find((entry) => entry.locale === locale) ?? null;
  const blockLabels: ContentBlockLabels = {
    imageCredit: t("imageCredit"), tip: t("toneTip"), warning: t("toneWarning"), info: t("toneInfo"),
  };

  useEffect(() => {
    if (!selected) return;
    const controller = new AbortController();
    api<{ topics: GuideTopic[] }>(`/admin/guides/topics${suffix}`, { signal: controller.signal })
      .then((vocabulary) => { if (!controller.signal.aborted) setTopics(vocabulary.topics); })
      .catch(() => { /* the taxonomy chips stay empty; the detail request reports the outage */ });
    return () => controller.abort();
  }, [selected, suffix]);

  useEffect(() => {
    if (!selected) return;
    const controller = new AbortController();
    api<ArticleDetail>(`/admin/guides/${selected}${suffix}`, { signal: controller.signal })
      .then((value) => {
        if (controller.signal.aborted) return;
        setDetail(value); setDraft(value.draft); setTableDrafts({});
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

  async function run<T>(work: () => Promise<T>): Promise<T | undefined> {
    if (!manage.allowed || busy) return undefined;
    setBusy(true); setError("");
    try { return await work(); } catch (problem) { showError(problem); return undefined; } finally { setBusy(false); }
  }

  const refresh = (value: ArticleDetail) => { setDetail(value); setDraft(value.draft); setTableDrafts({}); };

  const create = async () => {
    const value = await run(async () => api<ArticleDetail>("/admin/guides", {
      method: "POST",
      body: JSON.stringify({ slug: newSlug, kind: newKind, topics: [], document: emptyDocument(), locale }),
    }));
    if (!value) return;
    setCreating(false); setNewSlug("");
    setNotice(t("saved"));
    // Navigating while `busy` would be refused by the guard, so it happens after `run`.
    updateAdminQuery({ article: value.id, lang: locale });
  };

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

  const setHidden = (action: VisibilityAction, why: string) => run(async () => {
    if (!detail) return;
    const summary = await api<ArticleSummary>(`/admin/guides/${detail.id}/${action}${suffix}`, {
      method: "POST", body: JSON.stringify({ expected_version: detail.version, confirmed: true, reason: why }),
    });
    setLoaded((current) => (current?.detail ? { ...current, detail: { ...current.detail, ...summary } } : current));
    setVisibility(null);
    setNotice(t(action === "hide" ? "hideSuccess" : "unhideSuccess"));
  });

  const saveTaxonomy = () => run(async () => {
    if (!detail) return;
    refresh(await api<ArticleDetail>(`/admin/guides/${detail.id}${suffix}`, {
      method: "PUT",
      body: JSON.stringify({
        expected_version: detail.version, kind: detail.kind, destination_id: detail.destination_id,
        topics: detail.topics.map((topic) => topic.slug), valid_until: detail.valid_until,
        featured: detail.featured, display_order: detail.display_order,
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

  function updateBlock(index: number, block: GuideBlock) {
    if (draft) setDraft({ ...draft, blocks: draft.blocks.map((entry, i) => (i === index ? block : entry)) });
  }
  function setBlocks(blocks: GuideBlock[]) {
    if (!draft) return;
    // Positions change, so the raw table text keyed by position is thrown away; what comes
    // back is the saved shape of each table, which is what was parsed from it anyway.
    setTableDrafts({});
    setDraft({ ...draft, blocks });
  }
  function moveBlock(index: number, offset: number) {
    if (!draft || index + offset < 0 || index + offset >= draft.blocks.length) return;
    const blocks = [...draft.blocks];
    [blocks[index], blocks[index + offset]] = [blocks[index + offset], blocks[index]];
    setBlocks(blocks);
  }
  function updateSource(index: number, source: GuideSource) {
    if (draft) setDraft({ ...draft, sources: draft.sources.map((entry, i) => (i === index ? source : entry)) });
  }
  function setHero(hero: GuideHero | null) {
    if (draft) setDraft({ ...draft, hero });
  }

  /** The credit fields shared by the hero and every image block. */
  function creditFields(credit: ImageCredit | null, apply: (credit: ImageCredit | null) => void) {
    const current = credit ?? emptyCredit();
    return (
      <div className="grid gap-3 sm:grid-cols-3">
        <label className="grid gap-2">{t("creditAuthor")}
          <input className={control} value={current.author} onChange={(event) => apply(packCredit({ ...current, author: event.target.value }))} />
        </label>
        <label className="grid gap-2">{t("creditLicense")}
          <input className={control} value={current.license} onChange={(event) => apply(packCredit({ ...current, license: event.target.value }))} />
        </label>
        <label className="grid gap-2">{t("creditUrl")}
          <input className={control} value={current.source_url ?? ""} onChange={(event) => apply(packCredit({ ...current, source_url: event.target.value || null }))} />
        </label>
        <p className="text-sm leading-6 text-[var(--muted)] sm:col-span-3">{t("creditHelp")}</p>
      </div>
    );
  }

  function imageFields(image: Pick<ImageBlock, "src" | "alt" | "width" | "height">, apply: (patch: Partial<Pick<ImageBlock, "src" | "alt" | "width" | "height">>) => void) {
    return (
      <div className="grid gap-3 sm:grid-cols-2">
        <label className="grid gap-2">{t("imageSrc")}
          <input className={control} value={image.src} placeholder="/guides/narita-to-tokyo/hero.jpg" onChange={(event) => apply({ src: event.target.value })} />
        </label>
        <label className="grid gap-2">{t("imageAlt")}
          <input className={control} value={image.alt} onChange={(event) => apply({ alt: event.target.value })} />
        </label>
        <label className="grid gap-2">{t("imageWidth")}
          <input type="number" min={1} max={4000} className={control} value={image.width || ""} onChange={(event) => apply({ width: sizeValue(event.target.value) })} />
        </label>
        <label className="grid gap-2">{t("imageHeight")}
          <input type="number" min={1} max={4000} className={control} value={image.height || ""} onChange={(event) => apply({ height: sizeValue(event.target.value) })} />
        </label>
      </div>
    );
  }

  function blockFields(block: GuideBlock, index: number) {
    switch (block.type) {
      case "heading":
        return <>
          <label className="grid gap-2">{t("level")}
            <select className={control} value={block.level} onChange={(event) => updateBlock(index, { ...block, level: Number(event.target.value) as 2 | 3 })}>
              <option value={2}>2</option><option value={3}>3</option>
            </select>
          </label>
          <label className="grid gap-2">{t("text")}
            <textarea className={control} rows={2} value={block.text} onChange={(event) => updateBlock(index, { ...block, text: event.target.value })} />
          </label>
        </>;
      case "paragraph":
        return <label className="grid gap-2">{t("text")}
          <textarea className={control} rows={4} value={block.text} onChange={(event) => updateBlock(index, { ...block, text: event.target.value })} />
        </label>;
      case "list":
        return <>
          <label className="grid gap-2">{t("itemsHelp")}
            <textarea className={control} rows={4} value={block.items.join("\n")} onChange={(event) => updateBlock(index, { ...block, items: event.target.value.split("\n") })} />
          </label>
          <label className="flex min-h-11 items-center gap-3">
            <input type="checkbox" checked={block.ordered} onChange={(event) => updateBlock(index, { ...block, ordered: event.target.checked })} />{t("ordered")}
          </label>
        </>;
      case "link":
        return <>
          <label className="grid gap-2">{t("text")}
            <textarea className={control} rows={2} value={block.text} onChange={(event) => updateBlock(index, { ...block, text: event.target.value })} />
          </label>
          <label className="grid gap-2">{t("url")}
            <input className={control} value={block.url} onChange={(event) => updateBlock(index, { ...block, url: event.target.value })} />
          </label>
        </>;
      case "image":
        return <>
          {imageFields(block, (patch) => updateBlock(index, { ...block, ...patch }))}
          <label className="grid gap-2">{t("imageCaption")}
            <input className={control} value={block.caption ?? ""} onChange={(event) => updateBlock(index, { ...block, caption: event.target.value })} />
          </label>
          {creditFields(block.credit ?? null, (credit) => updateBlock(index, { ...block, credit }))}
        </>;
      case "table":
        return <>
          <label className="grid gap-2">{t("tableHelp")}
            <textarea className={`${control} font-mono`} rows={6} value={tableDrafts[index] ?? tableText(block)} onChange={(event) => {
              setTableDrafts((current) => ({ ...current, [index]: event.target.value }));
              updateBlock(index, { ...block, ...parseTable(event.target.value) });
            }} />
          </label>
          <label className="grid gap-2">{t("tableCaption")}
            <input className={control} value={block.caption ?? ""} onChange={(event) => updateBlock(index, { ...block, caption: event.target.value })} />
          </label>
        </>;
      case "callout":
        return <>
          <label className="grid gap-2">{t("tone")}
            <select className={control} value={block.tone} onChange={(event) => updateBlock(index, { ...block, tone: event.target.value as typeof block.tone })}>
              {calloutTones.map((tone) => <option key={tone} value={tone}>{blockLabels[tone]}</option>)}
            </select>
          </label>
          <label className="grid gap-2">{t("calloutTitle")}
            <input className={control} value={block.title ?? ""} onChange={(event) => updateBlock(index, { ...block, title: event.target.value })} />
          </label>
          <label className="grid gap-2">{t("text")}
            <textarea className={control} rows={3} value={block.text} onChange={(event) => updateBlock(index, { ...block, text: event.target.value })} />
          </label>
        </>;
      case "offer":
        return <>
          <label className="grid gap-2">{t("module")}
            <select className={control} value={block.module} onChange={(event) => updateBlock(index, { ...block, module: event.target.value as typeof block.module })}>
              {offerModules.map((module) => <option key={module} value={module}>{ts(moduleLabelKeys[module])}</option>)}
            </select>
          </label>
          <label className="grid gap-2">{t("offerDestination")}
            <input className={control} value={block.destination_id ?? ""} placeholder={detail?.destination_id ?? ""} onChange={(event) => updateBlock(index, { ...block, destination_id: event.target.value || null })} />
          </label>
          <label className="grid gap-2">{t("offerHeading")}
            <input className={control} value={block.heading ?? ""} onChange={(event) => updateBlock(index, { ...block, heading: event.target.value })} />
          </label>
          <p className="text-sm leading-6 text-[var(--muted)]">{t("offerHelp")}</p>
        </>;
      default:
        return null;
    }
  }

  return <div className="space-y-6">
    <header>
      <h1 className="text-3xl font-bold">{t("title")}</h1>
      <p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">{t("intro")}</p>
    </header>
    <AdminReadOnlyNotice capability="content.manage" />

    <div className="flex flex-wrap items-end gap-3">
      {selected && <Button secondary disabled={busy} onClick={() => updateAdminQuery({ article: "" })}>{t("backToList")}</Button>}
      <Button secondary disabled={busy || !manage.allowed} onClick={() => change(() => setCreating(true))}>{t("newArticle")}</Button>
      {selected && <label className="grid min-w-[12rem] gap-2">{t("documentLanguage")}
        <select className={control} disabled={busy} value={locale} onChange={(event) => updateAdminQuery({ lang: event.target.value })}>
          {sitePageLocales.map((value) => <option key={value} value={value}>{languages[value]}</option>)}
        </select>
      </label>}
    </div>

    {!selected && <AdminGuidesList
      onOpen={(id) => updateAdminQuery({ article: id, lang: locale })}
      onCreate={() => change(() => setCreating(true))}
    />}

    {error && !visibility && <div role="alert" className="space-y-3">
      <p>{error}</p>
      <Button secondary disabled={busy} onClick={() => change(() => setReload((value) => value + 1))}>{t("reload")}</Button>
    </div>}
    {notice && <p role="status">{notice}</p>}
    {selected && detail === undefined && !error && <p role="status">{t("loading")}</p>}

    {selected && detail === null && !error && <section className="space-y-4 rounded-2xl border border-[var(--line)] p-5">
      <p>{t("noTranslation")}</p>
      <Button disabled={busy || !manage.allowed} onClick={() => void startTranslation()}>{t("addTranslation")}</Button>
    </section>}

    {detail && draft && row && <>
      <p className="text-sm text-[var(--muted)]">{detail.slug} · {t(detail.kind)} · {t(`statuses.${detail.status}`)}</p>
      {!detail.is_active && <p role="status" className="rounded-xl border border-[var(--line)] bg-[var(--paper)] p-3 text-sm leading-6">{t("hiddenNotice")}</p>}

      <section className="space-y-4 rounded-2xl border border-[var(--line)] p-4">
        <h2 className="text-xl font-bold">{t("taxonomy")}</h2>
        <fieldset disabled={!manage.allowed || busy} className="grid gap-4 sm:grid-cols-2">
          <label className="grid gap-2">{t("kind")}
            <select className={control} value={detail.kind} onChange={(event) => {
              const kind = event.target.value as GuideKind;
              const moved = guideSection(kind) !== guideSection(detail.kind);
              setDetail({ ...detail, kind, topics: moved ? [] : detail.topics });
            }}>
              {guideKinds.map((value) => (
                <option key={value} value={value}
                  disabled={kindLocked && guideSection(value) !== guideSection(detail.kind)}>
                  {t(value)}
                </option>
              ))}
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
          <fieldset className="grid gap-2 sm:col-span-2">
            <legend className="font-semibold">{t("topics")}</legend>
            <div className="flex flex-wrap gap-2">
              {sectionTopics.map((topic) => {
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
        {detail.kind === "life" && <p className="text-sm leading-7 text-[var(--muted)]">{t("lifeDestinationHelp")}</p>}
        {kindLocked && <p className="text-sm leading-7 text-[var(--muted)]">{t("kindLocked")}</p>}
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

          <section className="space-y-3 rounded-2xl border border-[var(--line)] p-4">
            <h2 className="font-semibold">{t("hero")}</h2>
            <p className="text-sm leading-6 text-[var(--muted)]">{t("heroHelp")}</p>
            {draft.hero ? <>
              {imageFields(draft.hero, (patch) => setHero({ ...(draft.hero ?? emptyHero()), ...patch }))}
              {creditFields(draft.hero.credit, (credit) => setHero({ ...(draft.hero ?? emptyHero()), credit }))}
              <Button secondary onClick={() => setHero(null)}>{t("removeHero")}</Button>
            </> : <Button secondary onClick={() => setHero(emptyHero())}>{t("addHero")}</Button>}
          </section>

          <div className="space-y-5">{draft.blocks.map((block, index) => <fieldset key={index} className="space-y-3 rounded-2xl border border-[var(--line)] p-4">
            <legend className="px-2 font-semibold">{t(`blocks.${block.type}`)} {index + 1}</legend>
            {blockFields(block, index)}
            <div className="flex flex-wrap gap-2">
              <Button secondary disabled={index === 0} onClick={() => moveBlock(index, -1)}>{t("moveUp")}</Button>
              <Button secondary disabled={index === draft.blocks.length - 1} onClick={() => moveBlock(index, 1)}>{t("moveDown")}</Button>
              <Button secondary onClick={() => setBlocks(draft.blocks.filter((_, i) => i !== index))}>{t("removeBlock")}</Button>
            </div>
          </fieldset>)}</div>

          <div className="flex flex-wrap gap-2">{blockTypes.map((type) =>
            <Button secondary key={type} onClick={() => setBlocks([...draft.blocks, newBlock(type)])}>{t("addBlock")} · {t(`blocks.${type}`)}</Button>)}
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
          <Button secondary disabled={busy || dirty || !manage.allowed || !detail.is_active} onClick={() => { setConfirmed(false); setReason(""); setGate("publish"); }}>{t("publish")}</Button>
          {row.published_version !== null && <Button secondary disabled={busy || !manage.allowed} onClick={() => { setConfirmed(false); setReason(""); setGate("unpublish"); }}>{t("unpublish")}</Button>}
          <Button secondary disabled={busy || !manage.allowed} onClick={() => { setError(""); setVisibility(detail.is_active ? "hide" : "unhide"); }}>
            {detail.is_active ? t("hide") : t("unhide")}
          </Button>
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
      {/* The reader's renderer, not a second one, so the preview cannot flatter the draft. A
          partner block shows where its buttons will go; the buttons themselves come from the
          catalog at read time and are never fetched from the editor. */}
      <div lang={locale} className="space-y-6">
        <h1 className="text-3xl font-bold">{preview.title}</h1>
        <p className="leading-7 text-[var(--muted)]">{preview.description}</p>
        {/* eslint-disable-next-line @next/next/no-img-element -- the reader's own plain <img> */}
        {preview.hero?.src ? <img src={preview.hero.src} alt={preview.hero.alt} width={preview.hero.width} height={preview.hero.height} className="h-auto w-full rounded-2xl" /> : null}
        {splitGuideBlocks(preview.blocks).map((segment, index) => <Fragment key={index}>
          {segment.blocks.length ? <ContentBlocks blocks={segment.blocks} labels={blockLabels} headingStart={segment.headingStart} /> : null}
          {segment.offer ? <p role="note" className="rounded-xl border border-dashed border-[var(--line)] p-3 text-sm">
            {t("offerPreview")} · {ts(moduleLabelKeys[segment.offer.module])}{segment.offer.destination_id ? ` · ${segment.offer.destination_id}` : ""}
          </p> : null}
        </Fragment>)}
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

    {visibility && <GuideVisibilityDialog action={visibility} count={1} busy={busy} error={error}
      onConfirm={(why) => void setHidden(visibility, why)} onClose={() => { setVisibility(null); setError(""); }} />}
  </div>;
}
