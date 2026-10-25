"use client";

import { Copy, Download, ExternalLink, Hand } from "lucide-react";
import { useTranslations } from "next-intl";
import { type ReactNode, useEffect, useState } from "react";
import { control, downloadUrl, fileFor, fileUrl, list, mp4Retired, type Project, record, type Review, type ReviewFile, text, useWhen, youtubeVideoId } from "@/components/admin-video-review-card";
import { Button } from "@/components/community/ui";
import { api } from "@/lib/api";

type Draft = { title: string; description: string; video_id: string | null };
// `files` is the upload confirmation's, with the newest approved language batch's over them: a
// language added after the upload has its captions, description and thumbnail only there.
type Package = { project: Project; review: Review; languages: Review | null; files: ReviewFile[]; metadata: Record<string, unknown>; metadataFailed: boolean };
const DUB = "dub_";
const UNCHECKED_DUB = "dub_unchecked_";
// The dub formats the review store takes (docs/videos/DUBS.md: m4a, mp3 or wav).
const AUDIO_EXTENSIONS: Record<string, string> = { "audio/mp4": "m4a", "audio/mpeg": "mp3", "audio/wav": "wav" };
const strings = (value: unknown) => list(value).filter((item): item is string => typeof item === "string");
const canonical = (locale: string) => {
  const key = locale.toLowerCase().replaceAll("_", "-");
  return ({ "zh-tw": "zh-TW", "zh-hant": "zh-TW", "zh-cn": "zh-CN", "zh-hans": "zh-CN" } as Record<string, string>)[key] ?? key;
};

function CopyField({ label, value, rows = 2 }: { label: string; value: string; rows?: number }) {
  const t = useTranslations("admin.videoYoutube.manual");
  const [result, setResult] = useState<"copied" | "copyFailed" | null>(null);
  const copy = async () => {
    try {
      await navigator.clipboard.writeText(value);
      setResult("copied");
    } catch {
      setResult("copyFailed");
    }
  };
  return <div className="grid min-w-0 gap-2">
    <div className="flex flex-wrap items-center justify-between gap-2">
      <span className="text-sm font-semibold">{label}</span>
      <Button secondary onClick={() => void copy()} aria-label={t("copyField", { label })}><Copy aria-hidden size={16} />{t("copy")}</Button>
    </div>
    <textarea aria-label={label} readOnly value={value} rows={rows} className={`${control} text-sm font-normal`} onFocus={(event) => event.currentTarget.select()} />
    {result && <p role={result === "copied" ? "status" : "alert"} className="text-sm text-[var(--muted)]">{t(result)}</p>}
  </div>;
}

function DownloadFile({ slug, file, label, name }: { slug: string; file: ReviewFile; label: string; name: string }) {
  return <a href={fileUrl(slug, file)} download={name} className="inline-flex min-h-11 items-center gap-2 rounded-xl border border-[var(--line)] px-3 py-2 text-sm font-semibold hover:border-[var(--teal)]">
    <Download aria-hidden size={16} />{label}
  </a>;
}

function ManualGuide({ data, draft }: { data: Package; draft?: Draft }) {
  const t = useTranslations("admin.videoYoutube.manual");
  const reviewText = useTranslations("admin.videoReviews");
  const when = useWhen();
  const { project, review, languages, files, metadata, metadataFailed } = data;
  const zh = record(review.payload.zh);
  const previous = project.youtube_sync?.request;
  const id = youtubeVideoId(project.youtube_video_id ?? "") ?? youtubeVideoId(previous?.video_id ?? "") ?? youtubeVideoId(draft?.video_id ?? "");
  const original = canonical(text(metadata.default_language) || "zh-TW");
  const translations = Object.fromEntries(Object.entries(record(metadata.localizations)).map(([locale, values]) => [canonical(locale), record(values)]));
  const captionFiles = files.filter((file) => file.role.startsWith("captions_"));
  const descriptionFiles = files.filter((file) => file.role.startsWith("description_"));
  const locales = [...new Set([original, ...strings(review.payload.locales).map(canonical), ...Object.keys(record(languages?.payload.locales)).map(canonical), ...Object.keys(translations),
    ...captionFiles.map((file) => canonical(file.role.slice("captions_".length))), ...descriptionFiles.map((file) => canonical(file.role.slice("description_".length)))])];
  const localeName = (locale: string) => t.has(`languages.${locale}`) ? t(`languages.${locale}`) : locale;
  const [selected, setSelected] = useState(original);
  const values = selected === original ? {
    title: draft?.title ?? previous?.title ?? text(metadata.title ?? zh.title),
    description: draft?.description ?? previous?.description ?? text(metadata.description ?? zh.description),
  } : translations[selected] ?? {};
  const tags = strings(metadata.tags ?? zh.tags);
  const thumbnail = fileFor(review, "thumbnail");
  // Each language's own thumbnail, for Studio's language page (thumbnail_<locale>; a hyphen is a Test & compare variant).
  const localeThumbnails = files.filter((file) => file.role.startsWith("thumbnail_"));
  const final = mp4Retired(project) ? undefined : fileFor(review, "final");
  const disclosure = record(review.payload.disclosure);
  const synthetic = typeof metadata.contains_synthetic_media === "boolean" ? metadata.contains_synthetic_media : disclosure.synthetic;
  const studio = id ? `https://studio.youtube.com/video/${id}/edit` : "https://studio.youtube.com";
  const requestTime = previous?.visibility === "scheduled" ? previous.publish_at : project.youtube_publish_at;
  const stepClass = "grid min-w-0 gap-3 rounded-xl border border-[var(--line)] bg-[var(--surface)] p-4";
  const captionName = (file: ReviewFile) => `${canonical(file.role.slice("captions_".length))}.${file.content_type === "text/vtt" ? "vtt" : "srt"}`;
  const descriptionName = (file: ReviewFile) => `description.${canonical(file.role.slice("description_".length))}.txt`;
  // Every file the steps below offer one by one, under the same names, as one archive.
  const archive = new Map<string, ReviewFile>();
  if (!id && final) archive.set("final.mp4", final);
  if (thumbnail) archive.set(thumbnail.content_type === "image/png" ? "thumbnail.png" : "thumbnail.jpg", thumbnail);
  for (const file of localeThumbnails) archive.set(`thumbnail.${canonical(file.role.slice("thumbnail_".length))}.${file.content_type === "image/png" ? "png" : "jpg"}`, file);
  for (const file of captionFiles) archive.set(captionName(file), file);
  for (const file of descriptionFiles) archive.set(descriptionName(file), file);
  // Dub tracks: dub_<locale> is a ready track, dub_unchecked_<locale> one the check gave up on.
  const uncheckedDubs = files.filter((file) => file.role.startsWith(UNCHECKED_DUB));
  const readyDubs = files.filter((file) => file.role.startsWith(DUB) && !file.role.startsWith(UNCHECKED_DUB));
  const dubLocale = (file: ReviewFile) => canonical(file.role.slice((file.role.startsWith(UNCHECKED_DUB) ? UNCHECKED_DUB : DUB).length));
  const dubName = (file: ReviewFile) => `dub.${dubLocale(file)}${file.role.startsWith(UNCHECKED_DUB) ? ".unchecked" : ""}.${AUDIO_EXTENSIONS[file.content_type] ?? "m4a"}`;
  for (const file of [...readyDubs, ...uncheckedDubs]) archive.set(dubName(file), file);
  const metadataFile = files.find((file) => file.role === "metadata");
  if (metadataFile) archive.set("metadata.json", metadataFile);
  const archiveUrl = `/api/admin-video-package/${project.slug}?${new URLSearchParams([...archive].map(([name, file]) => ["file", `${file.sha256}:${name}`]))}`;

  return <div className="grid min-w-0 gap-4">
    <p className="text-sm leading-6 text-[var(--muted)]">{t("intro")}</p>
    {archive.size > 0 && <div className="grid gap-2 rounded-xl border border-[var(--teal)] p-4">
      <div><a href={archiveUrl} download={`${project.slug}-upload.zip`} className="inline-flex min-h-11 items-center gap-2 rounded-xl bg-[var(--teal)] px-4 py-2 text-sm font-semibold text-white"><Download aria-hidden size={16} />{t("downloadAll", { count: archive.size })}</a></div>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("downloadAllHelp")}</p>
      {!id && !final && project.compilation && project.download_available && <p className="text-sm text-amber-900">{t("downloadAllNoVideo")}</p>}
    </div>}
    {metadataFailed && <p role="alert" className="rounded-xl bg-amber-50 p-3 text-sm text-amber-900">{t("metadataFailed")}</p>}
    <section className={stepClass} aria-label={t("videoStep")}>
      <h3 className="font-bold">{t("videoStep")}</h3>
      <p className="text-sm leading-6">{id ? t("existingVideo", { id }) : t("newVideo")}</p>
      {!id && project.youtube_sync && <p className="text-sm text-amber-900">{t("checkExisting")}</p>}
      <div className="flex flex-wrap gap-2">
        <a href={studio} target="_blank" rel="noreferrer" className="inline-flex min-h-11 items-center gap-2 rounded-xl bg-[var(--teal)] px-4 py-2 text-sm font-semibold text-white"><ExternalLink aria-hidden size={16} />{id ? t("openExisting") : t("openStudio")}</a>
        {!id && final && <DownloadFile slug={project.slug} file={final} label={t("downloadVideo")} name="final.mp4" />}
        {!id && !final && project.compilation && project.download_available && <a className="inline-flex min-h-11 items-center gap-2 rounded-xl border border-[var(--line)] px-3 py-2 text-sm font-semibold" href={downloadUrl(project.slug)} download="final.mp4"><Download aria-hidden size={16} />{t("downloadVideo")}</a>}
      </div>
      {!id && !final && !(project.compilation && project.download_available) && <p role="status" className="text-sm text-amber-900">{t("videoMissing")}</p>}
    </section>
    <section className={stepClass} aria-label={t("textStep")}>
      <h3 className="font-bold">{t("textStep")}</h3>
      <label className="grid gap-2 text-sm font-semibold">{t("language")}
        <select className={control} value={selected} onChange={(event) => setSelected(event.target.value)}>{locales.map((locale) => <option value={locale} key={locale}>{localeName(locale)}</option>)}</select>
      </label>
      <p className="text-sm leading-6 text-[var(--muted)]">{selected === original ? t("originalHelp") : t("translationHelp")}</p>
      {text(values.title) ? <CopyField key={`${selected}-title-${text(values.title)}`} label={t("videoTitle")} value={text(values.title)} rows={2} /> : <p className="text-sm text-amber-900">{t("titleMissing")}</p>}
      {text(values.description) ? <CopyField key={`${selected}-description-${text(values.description)}`} label={t("description")} value={text(values.description)} rows={7} /> : <p className="text-sm text-amber-900">{t("descriptionMissing")}</p>}
      {tags.length > 0 && <CopyField label={t("tags")} value={tags.join(", ")} />}
      <p className="text-xs leading-5 text-[var(--muted)]">{t("tagsHelp")}</p>
    </section>
    <section className={stepClass} aria-label={t("thumbnailStep")}>
      <h3 className="font-bold">{t("thumbnailStep")}</h3>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("thumbnailHelp")}</p>
      <div>{thumbnail ? <DownloadFile slug={project.slug} file={thumbnail} label={t("downloadThumbnail")} name={thumbnail.content_type === "image/png" ? "thumbnail.png" : "thumbnail.jpg"} /> : <p className="text-sm">{t("thumbnailMissing")}</p>}</div>
      {localeThumbnails.length > 0 && <ul className="flex flex-wrap gap-2">{localeThumbnails.map((file) => {
        const locale = canonical(file.role.slice("thumbnail_".length));
        return <li key={file.role}><DownloadFile slug={project.slug} file={file} label={reviewText("downloadLocaleThumbnail", { locale: localeName(locale) })} name={`thumbnail.${locale}.${file.content_type === "image/png" ? "png" : "jpg"}`} /></li>;
      })}</ul>}
    </section>
    <section className={stepClass} aria-label={t("captionsStep")}>
      <h3 className="font-bold">{t("captionsStep")}</h3>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("captionsHelp")}</p>
      <ul className="flex flex-wrap gap-2">{captionFiles.map((file) => {
        const locale = canonical(file.role.slice("captions_".length));
        return <li key={file.role}><DownloadFile slug={project.slug} file={file} label={t("downloadCaption", { language: localeName(locale) })} name={captionName(file)} /></li>;
      })}</ul>
      {captionFiles.length === 0 && <p className="text-sm text-amber-900">{t("captionsMissing")}</p>}
      {id && <a href={`https://studio.youtube.com/video/${id}/translations`} target="_blank" rel="noreferrer" className="inline-flex min-h-11 items-center gap-2 text-sm font-semibold text-[var(--teal)] underline"><ExternalLink aria-hidden size={16} />{t("openCaptions")}</a>}
    </section>
    <section className={stepClass} aria-label={t("settingsStep")}>
      <h3 className="font-bold">{t("settingsStep")}</h3>
      <dl className="grid gap-3 text-sm">
        <div><dt className="font-semibold">{t("language")}</dt><dd>{localeName(original)}</dd></div>
        <div><dt className="font-semibold">{t("audience")}</dt><dd>{typeof metadata.made_for_kids === "boolean" ? t(metadata.made_for_kids ? "kidsYes" : "kidsNo") : t("settingUnknown")}</dd></div>
        <div><dt className="font-semibold">{t("synthetic")}</dt><dd>{typeof synthetic === "boolean" ? t(synthetic ? "yes" : "no") : t("settingUnknown")}</dd>{text(metadata.disclosure_reason ?? disclosure.reason) && <dd className="text-[var(--muted)]">{text(metadata.disclosure_reason ?? disclosure.reason)}</dd>}</div>
        {text(metadata.category_id) && <div><dt className="font-semibold">{t("category")}</dt><dd>{text(metadata.category_id) === "28" ? t("scienceCategory") : t("categoryId", { id: text(metadata.category_id) })}</dd></div>}
      </dl>
      <p className="text-sm leading-6">{t("finishHelp")}</p>
      {requestTime && <p className="text-sm">{t("requestedTime", { time: when(requestTime) })}</p>}
      <p className="text-sm leading-6 text-[var(--muted)]">{t("statusHelp")}</p>
    </section>
    {readyDubs.length + uncheckedDubs.length > 0 && <section className={stepClass} aria-label={t("dubStep")}>
      <h3 className="font-bold">{t("dubStep")}</h3>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("dubHelp")}</p>
      <ul className="flex flex-wrap gap-2">{readyDubs.map((file) => <li key={file.role}><DownloadFile slug={project.slug} file={file} label={t("downloadDub", { language: localeName(dubLocale(file)) })} name={dubName(file)} /></li>)}</ul>
      {uncheckedDubs.length > 0 && <>
        <ul className="flex flex-wrap gap-2">{uncheckedDubs.map((file) => <li key={file.role}><DownloadFile slug={project.slug} file={file} label={t("downloadUncheckedDub", { language: localeName(dubLocale(file)) })} name={dubName(file)} /></li>)}</ul>
        <p className="text-sm leading-6 text-amber-900">{t("uncheckedDubHelp")}</p>
      </>}
    </section>}
    <details className="rounded-xl border border-[var(--line)] p-4">
      <summary className="cursor-pointer text-sm font-semibold">{t("backupTitle")}</summary>
      <p className="mt-3 text-sm leading-6 text-[var(--muted)]">{t("backupHelp")}</p>
      <ul className="mt-3 flex flex-wrap gap-2">{[...descriptionFiles, ...(metadataFile ? [metadataFile] : [])].map((file) => {
        const name = file.role === "metadata" ? "metadata.json" : descriptionName(file);
        return <li key={file.role}><DownloadFile slug={project.slug} file={file} label={name} name={name} /></li>;
      })}</ul>
    </details>
  </div>;
}

/** A new mount reads the current approved package; closing or reloading aborts that read. */
function ManualPackage({ slug, draft, onReload }: { slug: string; draft?: Draft; onReload: () => void }) {
  const t = useTranslations("admin.videoYoutube.manual");
  const [data, setData] = useState<Package | null>(null);
  const [error, setError] = useState<"loadFailed" | "noPackage" | "running" | null>(null);
  useEffect(() => {
    let current = true;
    const controller = new AbortController();
    const load = async () => {
      try {
        const project = await api<Project>(`/admin/videos/${slug}`, { signal: controller.signal });
        if (!current) return;
        const sync = project.youtube_sync;
        if (sync && !sync.interrupted && ["queued", "running"].includes(sync.status)) { setError("running"); return; }
        const review = project.reviews.find((item) => item.gate === "publish" && item.status === "approved");
        if (!review || project.dropped_at) { setError("noPackage"); return; }
        // The newest approved batch of languages (reviews come newest first), as YouTube sync reads it.
        // One older than the confirmation belongs to an earlier package, whose own files are newer.
        const newestLanguages = project.reviews.find((item) => item.gate === "languages" && !item.subject && item.status === "approved");
        const languages = newestLanguages && Date.parse(newestLanguages.created_at) > Date.parse(review.created_at) ? newestLanguages : null;
        // Dub tracks wait on a card the owner approves only after uploading them in Studio, so they
        // also come from the newest languages or dubs card not sent back, pending ones included.
        const newestDubs = project.reviews.find((item) => (item.gate === "languages" || item.gate === "dubs") && !item.subject && (item.status === "approved" || item.status === "pending"));
        const dubFiles = newestDubs && Date.parse(newestDubs.created_at) > Date.parse(review.created_at) ? newestDubs.files.filter((file) => file.role.startsWith(DUB)) : [];
        const files = [...new Map([...review.files, ...(languages?.files ?? []), ...dubFiles].map((file) => [file.role, file])).values()];
        // Its metadata.json is the package's own, written again with every language translated since.
        const metadataUrl = fileUrl(slug, (languages && fileFor(languages, "metadata")) || fileFor(review, "metadata"));
        let metadata: Record<string, unknown> = {};
        let metadataFailed = !metadataUrl;
        if (metadataUrl) {
          try {
            const response = await fetch(metadataUrl, { credentials: "same-origin", cache: "no-store", signal: controller.signal });
            if (!response.ok) throw new Error("metadata");
            const value: unknown = await response.json();
            if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error("metadata");
            metadata = record(value);
          } catch {
            metadataFailed = true;
          }
        }
        if (current) setData({ project, review, languages, files, metadata, metadataFailed });
      } catch {
        if (current) setError("loadFailed");
      }
    };
    void load();
    return () => { current = false; controller.abort(); };
  }, [slug]);

  return <section aria-label={t("title")} className="grid min-w-0 gap-4 rounded-2xl border border-[var(--teal)] bg-[var(--paper)] p-4">
    <h2 className="text-lg font-bold">{t("title")}</h2>
    {error ? <p role="alert" className="text-sm text-amber-900">{t(error)}</p> : data ? <ManualGuide data={data} draft={draft} /> : <p role="status" className="text-sm">{t("loading")}</p>}
    {(error || data?.metadataFailed) && <div><Button secondary onClick={onReload}>{t("reload")}</Button></div>}
  </section>;
}

/** Read only: this mode reads the approved package from our site and never calls YouTube. */
export function YoutubeManualUpload({ slug, draft, children, disabled = false }: { slug: string; draft?: Draft; children?: ReactNode; disabled?: boolean }) {
  const t = useTranslations("admin.videoYoutube.manual");
  const [open, setOpen] = useState(false);
  const [attempt, setAttempt] = useState(0);
  return <div className="grid min-w-0 gap-3">
    <div><Button secondary disabled={disabled} aria-expanded={open} onClick={() => setOpen((value) => !value)}><Hand aria-hidden size={16} />{open ? t(children ? "backToAutomatic" : "close") : t("open")}</Button></div>
    {open ? <ManualPackage key={`${slug}-${attempt}`} slug={slug} draft={draft} onReload={() => setAttempt((value) => value + 1)} /> : children}
  </div>;
}
