"use client";

import { useCallback, useEffect, useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import { AdminReadOnlyNotice, useAdminActionGuard } from "@/components/admin-action-guard";
import { Button, Dialog } from "@/components/community/ui";
import { SitePageContent } from "@/components/site-page-content";
import { api, ApiError } from "@/lib/api";
import { useNavigationGuard } from "@/lib/navigation-guard";
import { requirementKeys, sitePageLocales, sitePageSlugs, type SitePageBlock, type SitePageDetail, type SitePageDocument, type SitePageLocale, type SitePageSlug } from "@/lib/site-pages";

const control = "min-h-11 w-full rounded-xl border border-[var(--control-border,var(--line))] bg-[var(--surface)] px-3 py-2 text-[var(--ink)]";
const languages: Record<SitePageLocale, string> = { "zh-TW": "繁體中文", "zh-CN": "简体中文", en: "English", ja: "日本語", ko: "한국어" };

export function AdminSitePagesPanel() {
  const t = useTranslations("admin.sitePages");
  const interfaceLocale = useLocale();
  const manage = useAdminActionGuard("settings.manage");
  const [slug, setSlug] = useState<SitePageSlug>("privacy");
  const [locale, setLocale] = useState<SitePageLocale>(sitePageLocales.includes(interfaceLocale as SitePageLocale) ? interfaceLocale as SitePageLocale : "en");
  const [snapshot, setSnapshot] = useState<SitePageDetail | null>();
  const [draft, setDraft] = useState<SitePageDocument | null>(null);
  const [reload, setReload] = useState(0);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [preview, setPreview] = useState<SitePageDocument | null>(null);
  const [publishing, setPublishing] = useState(false);
  const [confirmed, setConfirmed] = useState(false);
  const [reason, setReason] = useState("");
  const dirty = Boolean(draft && snapshot && JSON.stringify(draft) !== JSON.stringify(snapshot.draft));
  const requestLeave = useCallback((proceed: () => void) => {
    if (busy || (dirty && !window.confirm(t("discard")))) return false;
    proceed(); return true;
  }, [busy, dirty, t]);
  useNavigationGuard(dirty || busy, requestLeave);
  const path = `/admin/site-pages/${slug}`;
  const suffix = `?locale=${encodeURIComponent(locale)}`;
  const labels = Object.fromEntries([...requirementKeys, "effectiveDate"].map((key) => [key, t(key)])) as Record<typeof requirementKeys[number] | "effectiveDate", string>;

  const apply = (value: SitePageDetail) => { setSnapshot(value); setDraft(value.draft); };
  const showError = (problem: unknown) => setError(problem instanceof ApiError && problem.code === "site_page_version_conflict" ? t("conflict") : problem instanceof Error ? problem.message : t("error"));

  useEffect(() => {
    const controller = new AbortController();
    api<SitePageDetail>(`${path}${suffix}`, { signal: controller.signal }).then((value) => {
      if (!controller.signal.aborted) { setSnapshot(value); setDraft(value.draft); }
    }).catch((problem: unknown) => {
      if (controller.signal.aborted) return;
      if (problem instanceof ApiError && problem.code === "site_page_not_found") { setSnapshot(null); setDraft(null); }
      else { setSnapshot(undefined); setError(problem instanceof Error ? problem.message : t("error")); }
    });
    return () => controller.abort();
  }, [path, suffix, reload, t]);

  function changeSelection(change: () => void) {
    requestLeave(() => { setSnapshot(undefined); setDraft(null); setError(""); setNotice(""); change(); });
  }
  async function initialize() {
    if (!manage.allowed || busy) return;
    setBusy(true); setError("");
    try { await api("/admin/site-pages/initialize", { method: "POST" }); setNotice(t("initialized")); setReload((value) => value + 1); }
    catch (problem) { showError(problem); }
    finally { setBusy(false); }
  }
  async function save() {
    if (!manage.allowed || busy || !snapshot || !draft) return;
    setBusy(true); setError(""); setNotice("");
    try { apply(await api<SitePageDetail>(`${path}/draft${suffix}`, { method: "PUT", body: JSON.stringify({ expected_version: snapshot.version, document: draft }) })); setNotice(t("saved")); }
    catch (problem) { showError(problem); }
    finally { setBusy(false); }
  }
  async function publish() {
    if (!manage.allowed || busy || dirty || !snapshot || !confirmed || !reason.trim()) return;
    setBusy(true); setError("");
    try { apply(await api<SitePageDetail>(`${path}/publish${suffix}`, { method: "POST", body: JSON.stringify({ expected_version: snapshot.version, confirmed: true, reason }) })); setPublishing(false); setNotice(t("publishSuccess")); }
    catch (problem) { showError(problem); }
    finally { setBusy(false); }
  }
  async function historyPreview(id: string) {
    setBusy(true); setError("");
    try { const result = await api<{ document: SitePageDocument }>(`${path}/revisions/${id}${suffix}`); setPreview(result.document); }
    catch (problem) { showError(problem); }
    finally { setBusy(false); }
  }
  async function restore(id: string) {
    if (!manage.allowed || busy || !snapshot || !reason.trim() || !window.confirm(t("restoreConfirm"))) return;
    setBusy(true); setError("");
    try { apply(await api<SitePageDetail>(`${path}/restore${suffix}`, { method: "POST", body: JSON.stringify({ expected_version: snapshot.version, revision_id: id, reason }) })); setNotice(t("restored")); }
    catch (problem) { showError(problem); }
    finally { setBusy(false); }
  }
  function updateBlock(index: number, block: SitePageBlock) {
    if (draft) setDraft({ ...draft, blocks: draft.blocks.map((entry, i) => i === index ? block : entry) });
  }
  function moveBlock(index: number, offset: number) {
    if (!draft || index + offset < 0 || index + offset >= draft.blocks.length) return;
    const blocks = [...draft.blocks];
    [blocks[index], blocks[index + offset]] = [blocks[index + offset], blocks[index]];
    setDraft({ ...draft, blocks });
  }

  return <div className="space-y-6">
    <header><h1 className="text-3xl font-bold">{t("title")}</h1><p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">{t("intro")}</p></header>
    <AdminReadOnlyNotice capability="settings.manage" />
    <div className="grid gap-4 sm:grid-cols-2">
      <label className="grid gap-2">{t("documentPage")}<select className={control} disabled={busy} value={slug} onChange={(event) => changeSelection(() => setSlug(event.target.value as SitePageSlug))}>{sitePageSlugs.map((value) => <option value={value} key={value}>{t(value)}</option>)}</select></label>
      <label className="grid gap-2">{t("documentLanguage")}<select className={control} disabled={busy} value={locale} onChange={(event) => changeSelection(() => setLocale(event.target.value as SitePageLocale))}>{sitePageLocales.map((value) => <option value={value} key={value}>{languages[value]}</option>)}</select></label>
    </div>
    {error && <div role="alert" className="space-y-3"><p>{error}</p><Button secondary disabled={busy} onClick={() => changeSelection(() => setReload((value) => value + 1))}>{t("reload")}</Button></div>}
    {notice && <p role="status">{notice}</p>}
    {snapshot === undefined && !error && <p role="status">{t("loading")}</p>}
    {snapshot === null && <section className="space-y-4 rounded-2xl border border-[var(--line)] p-5"><p>{t("notInitialized")}</p><Button disabled={busy || !manage.allowed} onClick={() => void initialize()}>{t("initialize")}</Button></section>}
    {snapshot && draft && <>
      <div className="flex flex-wrap items-center gap-4 text-sm"><span>{t("draft")} · {t("revision")} {snapshot.version}</span>{snapshot.published && <><span>{t("published")} · {t("revision")} {snapshot.published.version}</span><Button secondary onClick={() => setPreview(snapshot.published)}>{t("published")}</Button></>}</div>
      <form onSubmit={(event) => { event.preventDefault(); void save(); }} className="space-y-6">
        <fieldset disabled={!manage.allowed || busy} className="space-y-5">
          <label className="grid gap-2">{t("documentTitle")}<input className={control} required maxLength={200} value={draft.title} onChange={(event) => setDraft({ ...draft, title: event.target.value })} /></label>
          <label className="grid gap-2">{t("seoDescription")}<textarea className={control} required maxLength={500} value={draft.description} onChange={(event) => setDraft({ ...draft, description: event.target.value })} /></label>
          <label className="grid gap-2">{t("effectiveDate")}<input type="date" className={control} value={draft.effective_date || ""} onChange={(event) => setDraft({ ...draft, effective_date: event.target.value || null })} /></label>
          <section className="space-y-4 rounded-2xl border border-[var(--line)] p-4"><h2 className="text-xl font-bold">{t("pending")}</h2><p className="text-sm leading-7 text-[var(--muted)]">{t("requirementsHelp")}</p>
            {requirementKeys.map((key) => <label key={key} className="grid gap-2">{t(key)}<textarea className={control} value={draft.requirements[key]} onChange={(event) => setDraft({ ...draft, requirements: { ...draft.requirements, [key]: event.target.value } })} /></label>)}
          </section>
          <div className="space-y-5">{draft.blocks.map((block, index) => <fieldset key={index} className="space-y-3 rounded-2xl border border-[var(--line)] p-4">
            <legend className="px-2 font-semibold">{t(block.type)} {index + 1}</legend>
            {block.type === "heading" && <label className="grid gap-2">{t("level")}<select className={control} value={block.level} onChange={(event) => updateBlock(index, { ...block, level: Number(event.target.value) as 2 | 3 })}><option value={2}>2</option><option value={3}>3</option></select></label>}
            {block.type === "list" ? <><label className="grid gap-2">{t("itemsHelp")}<textarea className={control} rows={4} value={block.items.join("\n")} onChange={(event) => updateBlock(index, { ...block, items: event.target.value.split("\n") })} /></label><label className="flex min-h-11 items-center gap-3"><input type="checkbox" checked={block.ordered} onChange={(event) => updateBlock(index, { ...block, ordered: event.target.checked })} />{t("ordered")}</label></> : <label className="grid gap-2">{t("text")}<textarea className={control} rows={block.type === "paragraph" ? 4 : 2} value={block.text} onChange={(event) => updateBlock(index, { ...block, text: event.target.value })} /></label>}
            {block.type === "link" && <label className="grid gap-2">{t("url")}<input className={control} value={block.url} onChange={(event) => updateBlock(index, { ...block, url: event.target.value })} /></label>}
            <div className="flex flex-wrap gap-2"><Button secondary disabled={index === 0} onClick={() => moveBlock(index, -1)}>{t("moveUp")}</Button><Button secondary disabled={index === draft.blocks.length - 1} onClick={() => moveBlock(index, 1)}>{t("moveDown")}</Button><Button secondary onClick={() => setDraft({ ...draft, blocks: draft.blocks.filter((_, i) => i !== index) })}>{t("removeBlock")}</Button></div>
          </fieldset>)}</div>
          <div className="flex flex-wrap gap-2">{(["heading", "paragraph", "list", "link"] as const).map((type) => <Button secondary key={type} onClick={() => setDraft({ ...draft, blocks: [...draft.blocks, type === "list" ? { type, items: [""], ordered: false } : type === "heading" ? { type, level: 2, text: "" } : type === "link" ? { type, text: "", url: "" } : { type, text: "" }] })}>{t("addBlock")} · {t(type)}</Button>)}</div>
        </fieldset>
        <div className="sticky bottom-3 z-10 flex flex-wrap gap-3 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-3 shadow-sm"><Button type="submit" disabled={busy || !manage.allowed || !dirty}>{t("save")}</Button><Button secondary disabled={busy} onClick={() => setPreview(draft)}>{t("preview")}</Button><Button secondary disabled={busy || dirty || !manage.allowed || snapshot.pending_requirements.length > 0} onClick={() => { setConfirmed(false); setReason(""); setPublishing(true); }}>{t("publish")}</Button></div>
        {snapshot.pending_requirements.length > 0 && <p className="text-sm text-[var(--muted)]">{t("pending")}: {snapshot.pending_requirements.map((key) => t(key === "effective_date" ? "effectiveDate" : key)).join(" · ")}</p>}
      </form>
      <section className="space-y-4"><h2 className="text-xl font-bold">{t("history")}</h2>
        <label className="grid gap-2">{t("reason")}<input className={control} disabled={busy || !manage.allowed} value={reason} onChange={(event) => setReason(event.target.value)} /></label>
        {!snapshot.revisions.length && <p>{t("noHistory")}</p>}
        <ul className="space-y-3">{snapshot.revisions.map((revision) => <li className="flex flex-wrap items-center gap-3 rounded-xl border border-[var(--line)] p-3" key={revision.id}><span>{t("revision")} {revision.version}</span><time className="text-sm text-[var(--muted)]" dateTime={revision.created_at}>{new Date(revision.created_at).toLocaleString(interfaceLocale)}</time><Button secondary disabled={busy} onClick={() => void historyPreview(revision.id)}>{t("viewRevision")}</Button><Button secondary disabled={busy || !manage.allowed || !reason.trim()} onClick={() => void restore(revision.id)}>{t("restore")}</Button></li>)}</ul>
      </section>
    </>}
    {preview && <Dialog title={t("preview")} onClose={() => setPreview(null)}><div lang={locale}><SitePageContent document={preview} labels={labels} /></div></Dialog>}
    {publishing && <Dialog title={t("confirmPublish")} onClose={() => { if (!busy) setPublishing(false); }}><div className="space-y-5"><p className="leading-7">{t("publishHelp")}</p><label className="grid gap-2">{t("reason")}<input className={control} disabled={busy} value={reason} onChange={(event) => setReason(event.target.value)} /></label><label className="flex min-h-11 items-start gap-3"><input type="checkbox" className="mt-1" disabled={busy} checked={confirmed} onChange={(event) => setConfirmed(event.target.checked)} />{t("confirmed")}</label>{error && <p role="alert">{error}</p>}<Button disabled={busy || !confirmed || !reason.trim()} onClick={() => void publish()}>{t("confirmPublish")}</Button></div></Dialog>}
  </div>;
}
