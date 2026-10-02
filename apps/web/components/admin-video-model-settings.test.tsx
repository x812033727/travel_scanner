import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { AdminVideoModelSettings } from "./admin-video-model-settings";
import type { AdminBootstrap } from "@/lib/admin-operations";

vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: null, sessionIdentity: null, status: undefined }) }));

function bootstrap(capabilities: string[]): AdminBootstrap {
  return { admin_roles: [], admin_capabilities: capabilities, navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false };
}

const sonnet = { provider: "anthropic", model: "claude-sonnet-5" };
const opus = { provider: "anthropic", model: "claude-opus-5-5" };
const tutorial = { planner: sonnet, writer: sonnet, verifier: opus, listener: opus, translator: sonnet, caption_reviewer: opus };
// Only what this block reads of the video settings: the tutorial's and the drama's models and the menus.
const video = {
  stage_models: tutorial,
  drama: { drama_stage_models: null },
  model_options: {
    claude_code: [{ value: "claude-opus-5-5", label: "Claude Opus 5.5", description: null, status: "stable" }],
    anthropic: [{ value: "claude-opus-5-5", label: "Claude Opus 5.5", description: null, status: "stable" }, { value: "claude-sonnet-5", label: "Claude Sonnet 5", description: null, status: "stable" }],
    codex: [], openai: [], minimax: [], gemini: [],
  },
  configured_providers: ["anthropic", "gemini"],
};

type Call = { path: string; body: Record<string, unknown> };

/** The two settings routes; a PUT answers the way the API merges: what was sent over what is stored. */
function stubFetch(shorts: Record<string, unknown>) {
  const puts: Call[] = [];
  let stored = { ...shorts };
  vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    const path = String(input).replace("/api/travel", "");
    if (init?.method === "PUT") {
      const body = JSON.parse(String(init.body)) as Record<string, unknown>;
      puts.push({ path, body });
      if (path === "/admin/video-shorts/settings") {
        stored = { ...stored, ...body };
        return Promise.resolve(Response.json(stored));
      }
      return Promise.resolve(Response.json({ ...video, ...body }));
    }
    if (path === "/admin/video-shorts/settings") return Promise.resolve(Response.json(stored));
    if (path === "/admin/video-automation/settings") return Promise.resolve(Response.json(video));
    return Promise.reject(new Error(`unexpected ${path}`));
  }));
  return puts;
}

const manager = () => render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "settings.manage"])}><AdminVideoModelSettings /></AdminOperationsProvider>);
const shortsBlock = () => screen.getByRole("region", { name: "Shorts 各階段" });

beforeEach(() => window.history.replaceState(null, "", "/zh-TW/admin/ai-settings"));
afterEach(() => vi.unstubAllGlobals());

describe("AdminVideoModelSettings, the Shorts block", () => {
  it("gives the Shorts their own stage models and sends only stage_models to the Shorts settings", async () => {
    const puts = stubFetch({ enabled: false, stock_days: 5, stage_models: null });
    manager();
    const follows = await screen.findByRole("checkbox", { name: "Shorts 各階段模型跟教學一樣" });
    expect(follows).toHaveProperty("checked", true);
    expect(screen.queryByRole("group", { name: "Shorts：撰稿" })).toBeNull();

    fireEvent.click(follows);
    const writer = within(shortsBlock()).getByRole("group", { name: "Shorts：撰稿" });
    // The Shorts' choices start as a copy of the tutorial's.
    expect((writer.querySelectorAll("select")[1] as HTMLSelectElement).value).toBe("claude-sonnet-5");
    fireEvent.change(writer.querySelectorAll("select")[1], { target: { value: "claude-opus-5-5" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存 Shorts 模型" }));
    await waitFor(() => expect(puts).toHaveLength(1));
    expect(puts[0]).toEqual({ path: "/admin/video-shorts/settings", body: { stage_models: { ...tutorial, writer: opus } } });
    expect(await within(shortsBlock()).findByRole("status")).toBeTruthy();

    fireEvent.click(screen.getByRole("checkbox", { name: "Shorts 各階段模型跟教學一樣" }));
    expect(screen.queryByRole("group", { name: "Shorts：撰稿" })).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "儲存 Shorts 模型" }));
    await waitFor(() => expect(puts).toHaveLength(2));
    expect(puts[1]).toEqual({ path: "/admin/video-shorts/settings", body: { stage_models: null } });
    expect(puts.every((call) => call.path !== "/admin/video-automation/settings/models")).toBe(true);
  });

  it("shows the Shorts' stored choice, leaves them out of the tutorial's save, and shows a refusal in the block", async () => {
    const shortsModels = { ...tutorial, planner: opus };
    const puts = stubFetch({ stage_models: shortsModels });
    manager();
    const planner = await within(await screen.findByRole("region", { name: "Shorts 各階段" })).findByRole("group", { name: "Shorts：企劃（選題與大綱）" });
    expect((planner.querySelectorAll("select")[1] as HTMLSelectElement).value).toBe("claude-opus-5-5");
    expect(screen.getByRole("checkbox", { name: "Shorts 各階段模型跟教學一樣" })).toHaveProperty("checked", false);

    fireEvent.click(screen.getByRole("button", { name: "儲存影片模型" }));
    await waitFor(() => expect(puts).toHaveLength(1));
    expect(puts[0].path).toBe("/admin/video-automation/settings/models");
    expect(puts[0].body).not.toHaveProperty("shorts_stage_models");

    vi.mocked(fetch).mockImplementationOnce(() => Promise.resolve(Response.json({ code: "video_shorts_settings_invalid", detail: "Shorts 的 writer：網站還沒有 anthropic 的金鑰" }, { status: 422 })));
    fireEvent.click(screen.getByRole("button", { name: "儲存 Shorts 模型" }));
    expect(await within(shortsBlock()).findByRole("alert")).toBeTruthy();
  });
});
