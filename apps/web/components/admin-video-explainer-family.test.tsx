import { fireEvent, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { AdminBootstrap } from "@/lib/admin-operations";
import { EXPLAINER_PRESETS, isExplainerPreset } from "@/lib/video-presets";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { AdminVideoSeries } from "./admin-video-series";
import { STYLE_PRESETS } from "./admin-video-settings";
import { DefaultStyleSelect } from "./admin-video-settings-drama";

vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: null, sessionIdentity: null, status: undefined }) }));

const STORY_PRESETS = ["cinematic-3d", "anime-2d", "ink-wash", "custom"];

function mount(requests: Record<string, unknown>[] = []) {
  vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL) => {
    const url = String(input);
    if (url.endsWith("/drama-requests")) return Promise.resolve(Response.json({ requests }));
    if (url.includes("/series?")) return Promise.resolve(Response.json({ series: [] }));
    if (url.includes("/series/binge-quote")) return Promise.resolve(Response.json({ episodes: 40, chapters: 4, episodes_per_chapter: 10, clip_seconds: 0, images: 10, judge_calls: 10, usd: 1, budgets: {}, ok: true }));
    if (url.endsWith("/settings")) return Promise.resolve(Response.json({ detail: "Not in this fixture" }, { status: 503 }));
    return Promise.resolve(Response.json([]));
  }));
  const bootstrap: AdminBootstrap = { admin_roles: [], admin_capabilities: ["content.read", "content.manage"], navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false };
  render(<AdminOperationsProvider bootstrap={bootstrap}><AdminVideoSeries onOpenVideo={() => undefined} /></AdminOperationsProvider>);
}

/** The option values of the one select in `form` that picks a style preset. */
function styleOptions(form: HTMLElement): string[] {
  const selects = within(form).getAllByRole("combobox").filter((select) => within(select).queryAllByRole("option").some((option) => (option as HTMLOptionElement).value === "cinematic-3d"));
  expect(selects).toHaveLength(1);
  return within(selects[0]).getAllByRole("option").map((option) => (option as HTMLOptionElement).value);
}

function openForm(summary: string): HTMLElement {
  fireEvent.click(screen.getByText(summary, { selector: "summary" }));
  return screen.getByRole("form", { name: summary });
}

afterEach(() => {
  vi.unstubAllGlobals();
  window.history.replaceState(null, "", "/");
});

describe("the explainer family of style presets", () => {
  it("is three presets, all of them stored presets", () => {
    expect([...EXPLAINER_PRESETS]).toEqual(["flat-explainer", "cute-cartoon", "cute-mystery"]);
    for (const preset of EXPLAINER_PRESETS) {
      expect(isExplainerPreset(preset)).toBe(true);
      expect(STYLE_PRESETS as readonly string[]).toContain(preset);
    }
    for (const other of ["cinematic-3d", "anime-2d", "ink-wash", "custom", ""]) expect(isExplainerPreset(other)).toBe(false);
    // The API's order (apps/api/app/video_automation/models.py STYLE_PRESETS).
    expect([...STYLE_PRESETS]).toEqual(["cinematic-3d", "anime-2d", "ink-wash", "flat-explainer", "cute-cartoon", "cute-mystery", "custom"]);
  });

  // A preset the API can answer with is shown by its label wherever one is shown: the settings
  // tab's default-style list, a queued request, a one-off's card and the series page.
  it("has a label for every stored preset in the three blocks of the five locales", async () => {
    const catalogs = await Promise.all([
      import("@/messages/zh-TW/admin.json"), import("@/messages/zh-CN/admin.json"),
      import("@/messages/en/admin.json"), import("@/messages/ja/admin.json"), import("@/messages/ko/admin.json"),
    ]);
    for (const catalog of catalogs) {
      const blocks: Record<string, string>[] = [catalog.default.videoReviews.presets, catalog.default.videoSettings.stylePresets, catalog.default.videoSeries.presets];
      for (const block of blocks) {
        expect(Object.keys(block)).toEqual([...STYLE_PRESETS]);
        for (const preset of STYLE_PRESETS) expect(block[preset].trim()).not.toBe("");
        expect(new Set(Object.values(block)).size).toBe(STYLE_PRESETS.length);
      }
    }
  });

  // The hold: the two cute presets are filed from the site only once each has its own prompts.
  // The pull request that adds those prompts changes this list on purpose.
  it("does not offer the cute presets in the request form yet", () => {
    mount();
    expect(styleOptions(openForm("新的漫劇"))).toEqual(["cinematic-3d", "anime-2d", "ink-wash", "flat-explainer", "custom"]);
  });

  it("offers a series and a binge series the story presets only", () => {
    mount();
    expect(styleOptions(openForm("新的作品"))).toEqual(STORY_PRESETS);
    expect(styleOptions(openForm("一鍵開拍"))).toEqual(STORY_PRESETS);
  });

  it("lists a queued cute request by its label, not its key", async () => {
    mount([{ id: "8b2e3d4c-5b6a-4f7e-9b8c-0d1e2f3a4b5c", premise: "瑪麗·賽勒斯特號上的人去了哪裡？", title: null, source_guide: null, style_preset: "cute-mystery", target_minutes: 10, note: null, status: "queued", slug: null, created_at: "2026-10-11T01:00:00Z", started_at: null, finished_at: null, cancelled_at: null }]);
    const queue = await screen.findByRole("region", { name: "發起的漫劇" });
    expect(queue.textContent).toContain("可愛卡通解說（奇聞檔案局）");
    expect(queue.textContent).not.toContain("cute-mystery");
  });

  // The second hold: a drama with no preset of its own takes the settings' default, so the two
  // cute presets are not a default either until they have prompts (lib/video-presets.ts).
  it("leaves the cute presets out of the settings' default-style select, a saved one kept", () => {
    const values = () => within(screen.getByRole("combobox")).getAllByRole("option").map((option) => (option as HTMLOptionElement).value);
    const first = render(<DefaultStyleSelect presets={STYLE_PRESETS} value="flat-explainer" onChange={() => undefined} />);
    expect(values()).toEqual(["cinematic-3d", "anime-2d", "ink-wash", "flat-explainer", "custom"]);
    expect((screen.getByRole("combobox") as HTMLSelectElement).value).toBe("flat-explainer");
    first.unmount();
    render(<DefaultStyleSelect presets={STYLE_PRESETS} value="cute-mystery" onChange={() => undefined} />);
    expect(values()).toEqual(["cinematic-3d", "anime-2d", "ink-wash", "flat-explainer", "cute-mystery", "custom"]);
    expect((screen.getByRole("combobox") as HTMLSelectElement).value).toBe("cute-mystery");
  });
});
