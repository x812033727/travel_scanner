import { readFile } from "node:fs/promises";
import { expect, test, type Locator, type Page } from "@playwright/test";
import type { Project, Review } from "../components/admin-video-review-card";
import en from "../messages/en/admin.json" with { type: "json" };
import ja from "../messages/ja/admin.json" with { type: "json" };
import ko from "../messages/ko/admin.json" with { type: "json" };
import zhCN from "../messages/zh-CN/admin.json" with { type: "json" };
import zhTW from "../messages/zh-TW/admin.json" with { type: "json" };
import { pretendSignedIn } from "./session";

// Isolated UI evidence: no actual upload, real channel, production auth or media.
test.use({ trace: "retain-on-failure" });
const slug = "manual-upload-fixture";
const videoId = "abcdefghijk";
const hash = (value: number) => value.toString(16).padStart(2, "0").repeat(32);
const locales = ["zh-TW", "zh-CN", "en", "ja", "ko"] as const;
const catalogs = { "zh-TW": zhTW, "zh-CN": zhCN, en, ja, ko };
const original = { title: "Synthetic approved video", description: "Synthetic approved description\n00:00 Introduction\n00:30 Demonstration\nhttps://example.test/source" };
const translations = Object.fromEntries(locales.filter((locale) => locale !== "zh-TW").map((locale) => [locale, {
  title: `${locale} synthetic title`, description: `${locale} synthetic description\n00:00 Introduction\n00:30 Demonstration\nhttps://example.test/${locale}`,
}]));
const metadata = { ...original, default_language: "zh-TW", localizations: translations, tags: ["Synthetic", "UI fixture"], made_for_kids: false, contains_synthetic_media: true, category_id: 28 };
const review: Review = {
  id: "synthetic-approved-package", gate: "publish", status: "approved", content_sha256: hash(1), summary: "Synthetic approved package",
  payload: { zh: original, locales: [...locales], disclosure: { synthetic: true } },
  files: [
    { role: "final", sha256: hash(2), size: 100, content_type: "video/mp4" },
    { role: "thumbnail", sha256: hash(3), size: 100, content_type: "image/png" },
    { role: "metadata", sha256: hash(4), size: 100, content_type: "application/json" },
    ...locales.map((locale, index) => ({ role: `captions_${locale === "zh-TW" ? "zh_tw" : locale}`, sha256: hash(5 + index), size: 100, content_type: locale === "ja" ? "text/vtt" : "text/plain" })),
  ],
  choice: null, note: null, created_at: "2026-09-28T00:00:00Z", decided_at: "2026-09-28T00:00:00Z",
};

async function fixture(page: Page, baseURL: string | undefined, existing: boolean) {
  const origin = new URL(baseURL || "http://127.0.0.1:3000").origin;
  expect(["127.0.0.1", "localhost"]).toContain(new URL(origin).hostname);
  await pretendSignedIn(page);
  await page.context().grantPermissions(["clipboard-read", "clipboard-write"], { origin });
  const writes: string[] = [], external: string[] = [], downloads: string[] = [];
  const project: Project = {
    slug, title: "Synthetic manual-upload validation", stage: "publish", checklist: [], pending: 0,
    youtube_video_id: existing ? videoId : null, last_synced_at: "2026-09-28T00:00:00Z",
    publish_approved_at: "2026-09-28T00:00:00Z", reviews: [review],
    youtube_sync: existing ? {
      status: "failed", interrupted: false, request: { mode: "upload", title: original.title, description: original.description },
      steps: [{ id: "upload", state: "done", detail: videoId, at: null }, { id: "captions", state: "failed", detail: "quotaExceeded", at: null }],
      progress: null, error: "quotaExceeded", started_at: null, finished_at: null,
    } : null,
  };
  const fileContent = new Map(review.files.filter((file) => file.role !== "metadata").map((file) => [file.sha256, `Synthetic download fixture: ${file.role}\n`]));
  await page.context().route("**/*", async (route) => {
    const request = route.request(), url = new URL(request.url());
    if (url.origin !== origin) { external.push(url.origin + url.pathname); return route.abort("blockedbyclient"); }
    if (!url.pathname.startsWith("/api/")) return route.fallback();
    if (request.method() !== "GET") {
      writes.push(`${request.method()} ${url.pathname}`);
      return route.fulfill({ status: 403, json: { code: "unexpected_fixture_write" } });
    }
    if (url.pathname === `/api/admin-video-files/${slug}/${hash(4)}`) return route.fulfill({ json: metadata });
    if (url.pathname.startsWith(`/api/admin-video-files/${slug}/`)) {
      const sha = url.pathname.split("/").at(-1)!;
      const body = fileContent.get(sha);
      if (!body) return route.fulfill({ status: 404, body: "Unknown synthetic file" });
      downloads.push(sha);
      return route.fulfill({ contentType: "application/octet-stream", body });
    }
    const path = url.pathname.replace("/api/travel", "");
    if (path === `/admin/videos/${slug}`) return route.fulfill({ json: project });
    if (path === "/admin/videos") return route.fulfill({ json: [project] });
    if (path === "/admin/video-youtube") return route.fulfill({ json: {
      configured: true, linked: true, audited: false, channel_id: "synthetic-channel", channel_title: "Synthetic channel",
      client_id: null, client_secret_set: false, redirect_uri: "", scope: "", channel_url: null,
      linked_at: null, verified_at: null, problem: null,
    } });
    if (path === "/auth/me") return route.fulfill({ json: { id: "fixture-admin", email: "admin@example.test", is_admin: true } });
    if (path === "/analytics/config") return route.fulfill({ json: { first_party_enabled: false, ga4_enabled: false } });
    return route.fallback();
  });
  return { writes, external, downloads, fileContent };
}

async function download(link: Locator, page: Page, name: string, contents: string) {
  await expect(link).toHaveAttribute("download", name);
  const received = page.waitForEvent("download");
  await link.click();
  const result = await received;
  expect(await result.failure()).toBeNull();
  expect(result.suggestedFilename()).toBe(name);
  const path = await result.path();
  expect(path).not.toBeNull();
  expect(await readFile(path!, "utf8")).toBe(contents);
}

for (const locale of locales) {
  for (const existing of [false, true]) {
    test(`${locale} manual upload ${existing ? "existing quota failure" : "new video"} preserves approved files and form edits`, async ({ page, baseURL }, info) => {
      const state = await fixture(page, baseURL, existing);
      const copy = catalogs[locale].videoYoutube, m = copy.manual;
      const errors: string[] = [];
      page.on("pageerror", (error) => errors.push(error.message));
      await page.goto(`/${locale}/admin/videos?video=${slug}`);
      if (!existing) {
        const form = page.getByRole("form", { name: copy.publishTitle });
        await form.getByRole("textbox", { name: copy.videoTitle, exact: true }).fill("Synthetic unsent title");
        await form.getByRole("textbox", { name: copy.videoDescription, exact: true }).fill("Synthetic unsent description\n00:00 Draft chapter");
      }
      await page.getByRole("button", { name: m.open, exact: true }).first().click();
      const manual = page.getByRole("region", { name: m.title, exact: true });
      for (const heading of [m.videoStep, m.textStep, m.thumbnailStep, m.captionsStep, m.settingsStep]) {
        await expect(manual.getByRole("region", { name: heading, exact: true })).toBeVisible();
      }
      const video = manual.getByRole("region", { name: m.videoStep });
      if (existing) {
        await expect(video.getByRole("link", { name: m.openExisting })).toHaveAttribute("href", `https://studio.youtube.com/video/${videoId}/edit`);
        await expect(video.locator("a[download]")).toHaveCount(0);
      } else {
        await expect(manual.getByRole("textbox", { name: m.videoTitle, exact: true })).toHaveValue("Synthetic unsent title");
        await download(video.getByRole("link", { name: m.downloadVideo }), page, "final.mp4", state.fileContent.get(hash(2))!);
      }
      for (const language of locales) {
        await manual.getByRole("combobox", { name: m.language, exact: true }).selectOption(language);
        const description = language === "zh-TW" ? existing ? original.description : "Synthetic unsent description\n00:00 Draft chapter" : translations[language].description;
        await expect(manual.getByRole("textbox", { name: m.description, exact: true })).toHaveValue(description);
        await manual.getByRole("button", { name: m.copyField.replace("{label}", m.description), exact: true }).click();
        await expect.poll(() => page.evaluate(() => navigator.clipboard.readText())).toBe(description);
        const captionName = `${language}.${language === "ja" ? "vtt" : "srt"}`;
        const caption = manual.getByRole("region", { name: m.captionsStep }).locator(`a[download="${captionName}"]`);
        await download(caption, page, captionName, state.fileContent.get(hash(5 + locales.indexOf(language)))!);
      }
      await download(manual.getByRole("link", { name: m.downloadThumbnail }), page, "thumbnail.png", state.fileContent.get(hash(3))!);
      await manual.getByRole("combobox", { name: m.language, exact: true }).selectOption("zh-TW");
      for (const theme of ["light", "dark"] as const) {
        await page.emulateMedia({ colorScheme: theme, reducedMotion: "reduce" });
        await page.evaluate((value) => { document.documentElement.dataset.theme = value; }, theme);
        expect(await page.locator("html").evaluate((node) => node.scrollWidth <= node.clientWidth + 1)).toBe(true);
        expect(await manual.evaluate((node) => node.scrollWidth <= node.clientWidth + 1)).toBe(true);
        if (locale === "zh-TW") {
          await manual.scrollIntoViewIfNeeded();
          await page.screenshot({ path: info.outputPath(`youtube-manual-${existing ? "existing" : "new"}-${theme}.jpg`), type: "jpeg", quality: 70, fullPage: true });
        }
      }
      if (!existing) {
        await page.getByRole("button", { name: m.backToAutomatic, exact: true }).click();
        const form = page.getByRole("form", { name: copy.publishTitle });
        await expect(form.getByRole("textbox", { name: copy.videoTitle, exact: true })).toHaveValue("Synthetic unsent title");
        await expect(form.getByRole("textbox", { name: copy.videoDescription, exact: true })).toHaveValue("Synthetic unsent description\n00:00 Draft chapter");
      }
      expect(state.downloads).toContain(hash(3));
      expect(state.writes).toEqual([]);
      expect(state.external).toEqual([]);
      expect(errors).toEqual([]);
    });
  }
}
