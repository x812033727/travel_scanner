import { linkSync, existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { LANGUAGES, Refused, VIDEO } from "./contract.mjs";

// Only DOM controls are used. No private Studio endpoints, cookie extraction or stealth flags.
// Studio is not a stable API: ambiguous/missing controls pause instead of choosing a fallback.
export const DEFAULT_SELECTORS = {
  title: "#title-textarea #textbox",
  description: "#description-textarea #textbox",
  thumbnail: 'input[type="file"][accept*="image"]',
  tags: "#tags-container input",
  category: "#category",
  language: "#video-language",
  visibility: "ytcp-video-visibility-select",
  translations: "ytcp-video-translation-row, ytgn-video-translation-row",
  captionsCell: "#captions, #subtitles",
  localizationCell: "#metadata, #title-description",
  syntheticGroup: "ytcp-video-metadata-editor-advanced",
};
export class Studio {
  constructor({ store, profile, selectors = {}, chromium, headless = false }) {
    this.store = store; this.profile = profile; this.selectors = { ...DEFAULT_SELECTORS, ...selectors };
    this.chromium = chromium; this.headless = headless; this.context = null;
  }
  async connect() {
    if (this.context) return;
    this.context = await this.chromium.launchPersistentContext(this.profile, {
      headless: this.headless, locale: "en-US", viewport: { width: 1440, height: 1000 },
      acceptDownloads: false,
    });
    this.page = this.context.pages()[0] || await this.context.newPage();
    this.page.setDefaultTimeout(15_000);
    this.context.on("close", () => { this.context = null; this.page = null; });
  }
  async close() { await this.context?.close(); }
  async guard() {
    const url = new URL(this.page.url());
    if (url.hostname === "accounts.google.com") throw new Refused("login_required");
    if (url.hostname !== "studio.youtube.com") throw new Refused("login_required");
    if (await this.page.locator('iframe[src*="recaptcha"], iframe[src*="challenge"]').count()) throw new Refused("verification_required");
  }
  async goto(suffix) {
    await this.page.goto("https://studio.youtube.com" + suffix, { waitUntil: "domcontentloaded" });
    await this.guard();
  }
  async unique(locator) {
    await locator.first().waitFor({ state: "attached" });
    if (await locator.count() !== 1) throw new Refused("studio_changed");
    return locator;
  }
  async click(locator) { await (await this.unique(locator)).click(); await this.guard(); }
  async fill(locator, value) { await this.guard(); await (await this.unique(locator)).fill(value); }
  button(name, root = this.page) { return root.getByRole("button", { name, exact: true }); }
  control(name, root = this.page) { return root.locator(this.selectors[name]); }
  async channel(id) {
    this.channelId = id;
    await this.goto("/channel/" + id);
    await this.confirmChannel();
  }
  async confirmChannel() {
    if (!this.channelId) throw new Refused("channel_unconfirmed");
    const link = this.page.locator('a[href^="/channel/' + this.channelId + '/videos"]');
    try { await this.unique(link); } catch { await this.guard(); throw new Refused("channel_unconfirmed"); }
  }
  asset(job, role) {
    const file = job.manifest.files.find((f) => f.role === role);
    if (!file) throw new Refused("file_missing");
    const extension = role === "final" ? ".mp4" : role === "thumbnail" ? (file.content_type === "image/png" ? ".png" : ".jpg") : file.content_type === "text/vtt" ? ".vtt" : ".srt";
    const target = path.join(this.store.directory, job.id, role + extension);
    if (!existsSync(target)) linkSync(this.store.file(job, file.sha256), target);
    return target;
  }
  async privateVisible() {
    const selector = await this.unique(this.control("visibility"));
    if (!/\bPrivate\b/.test(await selector.innerText())) throw new Refused("private_required");
  }
  async openPrivate(id) {
    if (!VIDEO.test(id)) throw new Refused("video_id_required");
    await this.goto("/video/" + id + "/edit");
    await this.unique(this.control("title"));
    await this.confirmChannel();
    await this.privateVisible();
  }
  async dropdown(name, value) {
    const control = await this.unique(this.control(name));
    const tag = await control.evaluate((element) => element.tagName);
    if (tag === "SELECT") await control.selectOption({ label: value });
    else {
      await this.click(control);
      await this.click(this.page.getByRole("option", { name: value, exact: true }));
    }
  }
  async details(metadata) {
    await this.fill(this.control("title"), metadata.title);
    await this.fill(this.control("description"), metadata.description);
    await this.click(this.page.getByRole("radio", { name: metadata.made_for_kids ? "Yes, it's made for kids" : "No, it's not made for kids", exact: true }));
    const more = this.button("Show more");
    if (await more.count() === 1 && await more.isVisible()) await this.click(more);
    // Never infer the audience/disclosure answer. A changed form needs owner review.
    const altered = this.control("syntheticGroup").locator('ytcp-form-input-container, fieldset, [role="group"]').filter({ hasText: "Altered content" })
      .getByRole("radio", { name: metadata.contains_synthetic_media ? "Yes" : "No", exact: true });
    await this.click(altered);
    {
      const input = await this.unique(this.control("tags"));
      // Replacing tags through their field only; existing chips must be cleared by Studio's
      // remove-all control, otherwise stop so a retry cannot silently append duplicates.
      const clear = this.button("Clear all tags");
      if (await clear.count() === 1 && await clear.isVisible()) await this.click(clear);
      else {
        const chips = this.page.locator("#tags-container ytcp-chip");
        const count = await chips.count();
        if (count > 100) throw new Refused("tags_need_review");
        for (let i = 0; i < count; i++) await this.click(chips.first().locator("#delete-button"));
      }
      await input.fill(metadata.tags.join(","));
      if (metadata.tags.length) await input.press("Enter");
    }
    await this.dropdown("language", LANGUAGES[metadata.default_language]);
    // Category labels are maintained explicitly, with no invented label for unknown IDs.
    const categories = { "1": "Film & Animation", "2": "Autos & Vehicles", "10": "Music", "15": "Pets & Animals",
      "17": "Sports", "19": "Travel & Events", "20": "Gaming", "22": "People & Blogs", "23": "Comedy",
      "24": "Entertainment", "25": "News & Politics", "26": "Howto & Style", "27": "Education", "28": "Science & Technology", "29": "Nonprofits & Activism" };
    if (!categories[metadata.category_id]) throw new Refused("category_need_review");
    await this.dropdown("category", categories[metadata.category_id]);
  }
  async saved() {
    const save = this.button("Save");
    if (await save.isEnabled()) {
      await this.click(save);
      await save.waitFor({ state: "attached" });
      // Wait for Studio's disabled Save as acknowledgement; clicking alone is not completion.
      for (let i = 0; i < 60; i++) {
        if (!await save.isEnabled()) return;
        await this.page.waitForTimeout(500);
      }
      throw new Refused("save_unconfirmed");
    }
  }
  async upload(job, checkpoint) {
    await this.click(this.button("Create"));
    await this.click(this.page.getByRole("menuitem", { name: "Upload videos", exact: true }));
    const input = await this.unique(this.page.locator('input[type="file"][accept*="video"]'));
    checkpoint.started(); // durable BEFORE the first upload side effect
    await input.setInputFiles(this.asset(job, "final"));
    const link = this.page.locator('a[href^="https://youtu.be/"]');
    await this.unique(link);
    const match = /^https:\/\/youtu\.be\/([A-Za-z0-9_-]{11})(?:[?#].*)?$/.exec(await link.getAttribute("href"));
    if (!match) throw new Refused("video_id_required");
    checkpoint.identified(match[1]);
    await this.details(job.manifest.metadata);
    // Upload wizard: Details -> Video elements -> Checks -> Visibility.
    for (let i = 0; i < 3; i++) await this.click(this.button("Next"));
    await this.click(this.page.getByRole("radio", { name: "Private", exact: true }));
    const privateChoice = this.page.getByRole("radio", { name: "Private", exact: true });
    if (await privateChoice.getAttribute("aria-checked") !== "true" && !await privateChoice.isChecked()) throw new Refused("private_required");
    await this.click(this.button("Save"));
    // Large uploads may remain here for hours; Studio can show a separate confirmation
    // dialog with Close. Do not close the upload wizard while it is still transferring.
    const until = Date.now() + 4 * 60 * 60 * 1000;
    while (await this.page.getByRole("dialog").count()) {
      await this.guard();
      const dialogs = this.page.getByRole("dialog");
      if (await dialogs.count() !== 1) throw new Refused("studio_changed");
      if (!await dialogs.isVisible()) break;
      const close = this.button("Close", dialogs);
      const confirmed = /Video (published|saved|uploaded)/i.test(await dialogs.innerText());
      if (confirmed && await close.count() === 1 && await close.isVisible()) {
        await this.click(close);
        await dialogs.waitFor({ state: "hidden" });
        break;
      }
      if (Date.now() >= until) throw new Refused("save_unconfirmed");
      await this.page.waitForTimeout(1000);
    }
    await this.openPrivate(match[1]);
  }
  async languageRow(locale) {
    let row = this.control("translations").filter({ hasText: LANGUAGES[locale] });
    if (await row.count() === 0) {
      await this.click(this.button("Add language"));
      await this.click(this.page.getByRole("option", { name: LANGUAGES[locale], exact: true }));
      row = this.control("translations").filter({ hasText: LANGUAGES[locale] });
    }
    return this.unique(row);
  }
  async step(step, job) {
    const id = job.video_id;
    if (step === "details") {
      await this.openPrivate(id); await this.details(job.manifest.metadata); await this.saved(); return;
    }
    if (step === "thumbnail") {
      await this.openPrivate(id);
      await (await this.unique(this.control("thumbnail"))).setInputFiles(this.asset(job, "thumbnail"));
      await this.saved(); return;
    }
    if (step === "verify") {
      await this.openPrivate(id);
      const title = await this.control("title").innerText();
      const description = await this.control("description").innerText();
      if (title.trim() !== job.manifest.metadata.title.trim() || description.replaceAll("\r\n", "\n").trim() !== job.manifest.metadata.description.replaceAll("\r\n", "\n").trim()) throw new Refused("save_unconfirmed");
      return;
    }
    // Verify privacy before opening each language editor.
    await this.openPrivate(id);
    await this.goto("/video/" + id + "/translations");
    const captions = step.startsWith("captions_");
    const locale = step.slice(captions ? 9 : 13);
    const row = await this.languageRow(locale);
    const cell = await this.unique(this.control(captions ? "captionsCell" : "localizationCell", row));
    // An existing published track is edited too: it may belong to an older package.
    // Only this job's durable completed-step receipt permits skipping a track.
    const edit = cell.getByRole("button", { name: /^(Add|Edit)$/ });
    await this.click(edit);
    const dialog = await this.unique(this.page.getByRole("dialog"));
    if (captions) {
      await this.click(this.button("Upload file", dialog));
      const timing = this.page.getByRole("radio", { name: "With timing", exact: true });
      await this.click(timing);
      const next = this.button("Continue");
      if (await next.count() === 1) await this.click(next);
      await (await this.unique(this.page.locator('input[type="file"][accept*=".srt"]'))).setInputFiles(this.asset(job, step));
      // This publishes a subtitle track, not the video's visibility.
      await this.click(this.button("Publish"));
    } else {
      const metadata = job.manifest.metadata.localizations[locale];
      await this.fill(dialog.getByRole("textbox", { name: "Title", exact: true }), metadata.title);
      await this.fill(dialog.getByRole("textbox", { name: "Description", exact: true }), metadata.description);
      await this.click(this.button("Publish", dialog));
    }
    await dialog.waitFor({ state: "hidden" });
    if (!/\bPublished\b/.test(await cell.innerText())) throw new Refused("save_unconfirmed");
  }
}
export function readSelectors(file) {
  if (!file) return {};
  const selectors = JSON.parse(readFileSync(file, "utf8"));
  if (!selectors || typeof selectors !== "object" || Array.isArray(selectors)
      || Object.entries(selectors).some(([key, value]) => !Object.hasOwn(DEFAULT_SELECTORS, key) || typeof value !== "string" || !value || value.length > 500)) throw new Error("Invalid selector configuration");
  return selectors;
}
