import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { AdminBootstrap } from "@/lib/admin-operations";
import { PRESET_IMAGE_MODEL } from "@/lib/video-presets";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { AdminVideoSeries, requestImageModel } from "./admin-video-series";
import { imageModelOptions } from "./admin-video-settings";

vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: null, sessionIdentity: null, status: undefined }) }));

const FIELD = "這一支的圖片模型";
const FOLLOWS = "跟漫劇設定一樣";
const option = (value: string, label: string, usd: number, status = "stable") => ({ value, label, description: null, status, resolutions: [], durations: [], reference_images: 1, native_audio: false, usd_per_second: null, usd_per_image: usd, usd_per_track: null });
const GEMINI = option("gemini-3-pro-image", "Gemini 3 Pro Image", 0.134);
const MINIMAX = option("image-01", "MiniMax image-01", 0.0035);
const CATALOGUE = { gemini: [GEMINI], minimax: [MINIMAX] };

/** The settings view the drama tab reads: the drama route on, and the image catalogue under test. */
function videoSettings(images: Record<string, unknown>, configured: string[]) {
  return {
    enabled: false, draft_interval_hours: 72, topics_per_run: 1, max_waiting_drafts: 3, topic_scope: ["AI"], topic_avoid: [], topic_from_site: true, topic_from_search: true,
    stage_models: Object.fromEntries(["planner", "writer", "verifier", "listener", "translator", "caption_reviewer"].map((stage) => [stage, { provider: "anthropic", model: "claude-sonnet-5" }])),
    voice: { provider: "gemini", name: "Sulafat", style: null, model: null, rate: "+0%" }, target_minutes_min: 8, target_minutes_max: 12,
    caption_locales: ["en"], max_drafts_per_month: 8, monthly_token_budget_millions: 20, max_verify_rounds: 3, max_retake_rounds: 2, auto_approve_audio: true,
    stage_instructions: {}, channel_stance: "", auto_pick_outline: true, auto_approve_final: true,
    drama: {
      drama_enabled: true, image_provider: "gemini", image_model: "gemini-3-pro-image", clip_provider: "gemini", clip_model: "gemini-omni-1.1-flash",
      music_provider: "gemini", music_model: "lyria-3.5", clip_resolution: "1080p", clip_seconds_default: 8, clip_native_audio: false, drama_aspect: "16:9",
      max_clips_per_video: 40, max_retakes_per_shot: 2, monthly_clip_seconds_budget: 3000, monthly_images_budget: 1500, monthly_judge_calls_budget: 3000,
      monthly_music_budget: 60, max_usd_per_video: 200, judge_min_score: 7, auto_approve_storyboard: false, auto_pick_look: false, character_voice_pool: [],
      music_enabled: true, subtitle_burn_in: true, style_preset: "cinematic-3d", drama_topic_scope: [],
    },
    media_options: { images, clips: {}, music: {} }, style_presets: ["cinematic-3d", "flat-explainer"], model_options: {}, configured_providers: configured,
    voice_options: { gemini: ["Kore"], gemini_models: [], azure: [] }, usage: null, updated_at: "2026-10-11T08:00:00Z",
  };
}

const oneOff = (slug: string, title: string, imageModel: string | null) => ({
  id: slug, slug, kind: "one-off", title, premise: "p", aspects: [], tone: "no-romance", style_preset: "flat-explainer", target_minutes: 10, planned_episodes: 1,
  episodes_per_chapter: 1, chapters: 1, open_ended: false, status: "setting", note: null, requested_chapter: null, force_next: false, episodes_done: 0, episodes_started: 0,
  episodes_ready: 0, docs_pending: 0, media_usd: 0, clip_seconds: 0, created_at: "2026-10-11T00:00:00Z", updated_at: "2026-10-11T01:00:00Z", image_model: imageModel,
});

type Site = { images?: Record<string, unknown>; configured?: string[]; settingsDown?: boolean; refuse?: { code: string; detail: string }; oneOffs?: ReturnType<typeof oneOff>[] };

function mount(site: Site = {}) {
  const posts: Record<string, unknown>[] = [];
  const oneOffs = site.oneOffs ?? [];
  vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith("/drama-requests") && init?.method === "POST") {
      posts.push(JSON.parse(String(init.body)) as Record<string, unknown>);
      if (site.refuse) return Promise.resolve(Response.json(site.refuse, { status: 409 }));
      return Promise.resolve(Response.json({ series_slug: null }, { status: 201 }));
    }
    if (url.endsWith("/drama-requests")) return Promise.resolve(Response.json({ requests: [] }));
    if (url.endsWith("/series?kind=one-off")) return Promise.resolve(Response.json({ series: oneOffs }));
    if (url.includes("/series?")) return Promise.resolve(Response.json({ series: [] }));
    if (url.includes("/series/binge-quote")) return Promise.resolve(Response.json({ episodes: 40, chapters: 4, episodes_per_chapter: 10, clip_seconds: 0, images: 10, judge_calls: 10, usd: 1, budgets: {}, ok: true }));
    if (url.includes("/messages?subject=")) return Promise.resolve(Response.json({ messages: [] }));
    const opened = oneOffs.find((each) => url.endsWith(`/series/${each.slug}`));
    if (opened) return Promise.resolve(Response.json({ ...opened, docs: [], episodes: [] }));
    if (url.endsWith("/settings")) {
      if (site.settingsDown) return Promise.resolve(Response.json({ detail: "Not in this fixture" }, { status: 503 }));
      return Promise.resolve(Response.json(videoSettings(site.images ?? CATALOGUE, site.configured ?? ["gemini", "minimax"])));
    }
    return Promise.resolve(Response.json([]));
  }));
  const bootstrap: AdminBootstrap = { admin_roles: [], admin_capabilities: ["content.read", "content.manage"], navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false };
  render(<AdminOperationsProvider bootstrap={bootstrap}><AdminVideoSeries onOpenVideo={() => undefined} /></AdminOperationsProvider>);
  return { posts };
}

/** The request form opened with a premise typed, once the settings read has settled. */
async function openForm(site: Site = {}) {
  const { posts } = mount(site);
  // The settings read settles either way: answered, the drama's settings panel is on the page.
  if (!site.settingsDown) await screen.findByRole("combobox", { name: "圖片模型" });
  fireEvent.click(screen.getByText("新的漫劇", { selector: "summary" }));
  const form = within(screen.getByRole("form", { name: "新的漫劇" }));
  // Filing clears the premise, so each filing types it again.
  const premise = () => fireEvent.change(form.getByRole("textbox", { name: "故事前提（必填）" }), { target: { value: "為什麼雷聲比閃電晚？" } });
  premise();
  const style = (preset: string) => fireEvent.change(form.getByRole("combobox", { name: "風格" }), { target: { value: preset } });
  const file = async () => {
    const before = posts.length;
    premise();
    fireEvent.click(form.getByRole("button", { name: "排進製作" }));
    await waitFor(() => expect(posts).toHaveLength(before + 1));
    return posts[before];
  };
  return { form, posts, style, file };
}

afterEach(() => {
  vi.unstubAllGlobals();
  window.history.replaceState(null, "", "/");
});

describe("the image model of a one-off explainer request", () => {
  it("shows no field for a cast preset and sends no image_model", async () => {
    const { form, file } = await openForm();
    expect(form.queryByRole("combobox", { name: FIELD })).toBeNull();
    const body = await file();
    expect(body).toMatchObject({ style_preset: "cinematic-3d", target_minutes: 3 });
    expect(Object.hasOwn(body, "image_model")).toBe(false);
  });

  it("offers the catalogue for flat-explainer, follows the drama settings until a model is chosen, and sends the chosen one", async () => {
    const { form, style, file } = await openForm();
    style("flat-explainer");
    const field = form.getByRole("combobox", { name: FIELD }) as HTMLSelectElement;
    expect(field.value).toBe("");
    expect(within(field).getAllByRole("option").map((each) => each.textContent)).toEqual([FOLLOWS, "Gemini 3 Pro Image · Google Gemini API · US$0.134", "MiniMax image-01 · MiniMax API · US$0.0035"]);
    const follows = await file();
    expect(follows).toMatchObject({ style_preset: "flat-explainer", target_minutes: 10 });
    expect(Object.hasOwn(follows, "image_model")).toBe(false);
    fireEvent.change(field, { target: { value: "image-01" } });
    expect(await file()).toMatchObject({ style_preset: "flat-explainer", image_model: "image-01" });
    // Leaving the explainer family drops the pick with the field.
    style("ink-wash");
    expect(form.queryByRole("combobox", { name: FIELD })).toBeNull();
    expect(Object.hasOwn(await file(), "image_model")).toBe(false);
    style("flat-explainer");
    expect((form.getByRole("combobox", { name: FIELD }) as HTMLSelectElement).value).toBe("");
  });

  it("marks a model whose vendor has no key, leaves it selectable, and shows the server's refusal", async () => {
    const refusal = { code: "video_drama_image_model_not_configured", detail: "網站還沒有 minimax 的金鑰，圖片模型 image-01 畫不了這支解說" };
    const { form, posts, style } = await openForm({ configured: ["gemini"], refuse: refusal });
    style("flat-explainer");
    const field = form.getByRole("combobox", { name: FIELD }) as HTMLSelectElement;
    expect(within(field).getAllByRole("option").map((each) => each.textContent)).toEqual([FOLLOWS, "Gemini 3 Pro Image · Google Gemini API · US$0.134", "MiniMax image-01 · MiniMax API (沒有金鑰) · US$0.0035"]);
    fireEvent.change(field, { target: { value: "image-01" } });
    expect(field.value).toBe("image-01");
    fireEvent.click(form.getByRole("button", { name: "排進製作" }));
    expect((await form.findByRole("alert")).textContent).toContain(refusal.detail);
    expect(posts[0]).toMatchObject({ image_model: "image-01" });
  });

  it.each([
    ["the settings read fails", { settingsDown: true }],
    ["the site sends no image catalogue", { images: {} }],
  ] as [string, Site][])("shows no field when %s, and an explainer files with no image_model", async (_name, site) => {
    const { form, style, file } = await openForm(site);
    style("flat-explainer");
    expect(form.queryByRole("combobox", { name: FIELD })).toBeNull();
    const body = await file();
    expect(body).toMatchObject({ style_preset: "flat-explainer", target_minutes: 10 });
    expect(Object.hasOwn(body, "image_model")).toBe(false);
  });

  it("leaves out a retired model", async () => {
    const { form, style } = await openForm({ images: { gemini: [GEMINI, option("old-image", "Old", 0.1, "retired")], minimax: [MINIMAX] } });
    style("flat-explainer");
    expect(within(form.getByRole("combobox", { name: FIELD })).getAllByRole("option").map((each) => (each as HTMLOptionElement).value)).toEqual(["", "gemini-3-pro-image", "image-01"]);
  });

  it("keeps one number input and the style select's own name beside the drama settings panel", async () => {
    const { form, style } = await openForm();
    style("flat-explainer");
    expect(form.getAllByRole("spinbutton")).toHaveLength(1);
    expect(form.getByRole("combobox", { name: "風格" })).toBeTruthy();
    // The settings panel's own select is named 圖片模型; the form's is a different whole name.
    expect(screen.getAllByRole("combobox", { name: FIELD })).toHaveLength(1);
    expect(screen.getAllByRole("combobox", { name: "圖片模型" })).toHaveLength(1);
  });

  it("shows the stored model on the one-off's card and on its page, and nothing for one that names none", async () => {
    mount({ oneOffs: [oneOff("one-off-aaaa1111", "雷聲", "image-01"), oneOff("one-off-bbbb2222", "潮汐", null)] });
    const cards = await screen.findByRole("region", { name: "單集漫劇" });
    const named = within(cards).getByRole("button", { name: /雷聲/ });
    expect(named.textContent).toContain("圖片模型 image-01");
    expect(within(cards).getByRole("button", { name: /潮汐/ }).textContent).not.toContain("圖片模型");
    fireEvent.click(named);
    await waitFor(() => expect(window.location.search).toContain("series=one-off-aaaa1111"));
    expect(await screen.findByText(/每集 10 分鐘 · 圖片模型 image-01/)).toBeTruthy();
  });
});

// The request form does not offer the cute presets until each has its own prompts, so what the
// field does for them is held on the helper the form is built on.
describe("requestImageModel", () => {
  const models = imageModelOptions({ images: CATALOGUE, clips: { gemini: [], minimax: [] }, music: { gemini: [], minimax: [] } });

  it("lists every vendor's image models with their vendor, and nothing without a catalogue", () => {
    expect(models.map((each) => [each.provider, each.value])).toEqual([["gemini", "gemini-3-pro-image"], ["minimax", "image-01"]]);
    expect(imageModelOptions(undefined)).toEqual([]);
    expect(imageModelOptions({ images: {}, clips: {}, music: {} } as never)).toEqual([]);
  });

  it.each(["cute-cartoon", "cute-mystery"])("starts %s on image-01 with no entry to follow the settings", (preset) => {
    expect(PRESET_IMAGE_MODEL[preset]).toBe("image-01");
    expect(requestImageModel(preset, null, models)).toEqual({ offered: true, presetDefault: "image-01", value: "image-01" });
  });

  it("keeps the owner's pick over a cute preset's default, across both cute presets", () => {
    for (const preset of ["cute-cartoon", "cute-mystery"]) expect(requestImageModel(preset, "gemini-3-pro-image", models)).toEqual({ offered: true, presetDefault: "image-01", value: "gemini-3-pro-image" });
    // The form drops a pick only when the default changes or the family is left: the two share one.
    expect(PRESET_IMAGE_MODEL["cute-cartoon"]).toBe(PRESET_IMAGE_MODEL["cute-mystery"]);
    expect(PRESET_IMAGE_MODEL["flat-explainer"]).toBeUndefined();
  });

  it("has no default to preselect when the catalogue lacks image-01, and offers the settings' entry instead", () => {
    const geminiOnly = models.filter((each) => each.provider === "gemini");
    expect(requestImageModel("cute-mystery", null, geminiOnly)).toEqual({ offered: true, presetDefault: "", value: "" });
  });

  it("follows the settings for flat-explainer, and offers nothing to a cast preset or without models", () => {
    expect(requestImageModel("flat-explainer", null, models)).toEqual({ offered: true, presetDefault: "", value: "" });
    expect(requestImageModel("flat-explainer", "image-01", models)).toEqual({ offered: true, presetDefault: "", value: "image-01" });
    expect(requestImageModel("cinematic-3d", null, models).offered).toBe(false);
    expect(requestImageModel("custom", null, models).offered).toBe(false);
    expect(requestImageModel("cute-cartoon", null, [])).toEqual({ offered: false, presetDefault: "", value: "" });
  });
});
