import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { AdminVideoSettings, linesToList, settingsBody, STAGES } from "./admin-video-settings";
import type { AdminBootstrap } from "@/lib/admin-operations";

vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: null, sessionIdentity: null, status: undefined }) }));

function bootstrap(capabilities: string[]): AdminBootstrap {
  return { admin_roles: [], admin_capabilities: capabilities, navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false };
}

const sonnet = { provider: "anthropic", model: "claude-sonnet-5" };
const opus = { provider: "anthropic", model: "claude-opus-5-5" };
const view = {
  enabled: false, draft_interval_hours: 72, topics_per_run: 1, max_waiting_drafts: 3,
  topic_scope: ["AI", "Tech"], topic_avoid: ["Stocks"], topic_from_site: true, topic_from_search: true,
  stage_models: { planner: sonnet, writer: sonnet, verifier: opus, listener: opus, translator: sonnet, caption_reviewer: opus },
  voice: { provider: "gemini", name: "Sulafat", style: "Relaxed", model: null, rate: "+0%" },
  target_minutes_min: 8, target_minutes_max: 12, caption_locales: ["en", "ja", "ko", "zh-CN"],
  max_drafts_per_month: 8, monthly_token_budget_millions: 20, max_verify_rounds: 3, max_retake_rounds: 2,
  auto_approve_audio: true,
  model_options: {
    anthropic: [{ value: "claude-opus-5-5", label: "Claude Opus 5.5", description: null, status: "stable" }, { value: "claude-sonnet-5", label: "Claude Sonnet 5", description: null, status: "stable" }],
    openai: [], minimax: [],
    gemini: [{ value: "gemini-3.8-flash", label: "Gemini 3.8 Flash", description: null, status: "stable" }],
  },
  configured_providers: ["anthropic", "gemini"],
  voice_options: { gemini: ["Sulafat", "Kore"], gemini_models: ["gemini-3.8-flash-tts"], azure: [] },
  usage: { tokens: 1500, token_budget: 20_000_000, drafts: 1, draft_budget: 8, calls: 3, failed_calls: 1 },
  updated_at: "2026-09-25T08:00:00Z",
};

function stubFetch() {
  const puts: unknown[] = [];
  vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    expect(String(input)).toContain("/api/travel/admin/video-automation/settings");
    if (init?.method === "PUT") {
      const body = JSON.parse(String(init.body));
      puts.push(body);
      return Promise.resolve(Response.json({ ...view, ...body }));
    }
    return Promise.resolve(Response.json(view));
  }));
  return puts;
}

afterEach(() => vi.unstubAllGlobals());

describe("AdminVideoSettings", () => {
  it("keeps one topic per line and sends only what the API stores", () => {
    expect(linesToList(" AI \n\nAI 工具教學\r\n")).toEqual(["AI", "AI 工具教學"]);
    const body = settingsBody(view as never);
    expect(Object.keys(body)).not.toContain("model_options");
    expect(Object.keys(body)).not.toContain("updated_at");
    expect(Object.keys(body.stage_models)).toEqual([...STAGES]);
  });

  it("lets a settings manager turn drafts on, pick a model and save", async () => {
    const puts = stubFetch();
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "settings.manage"])}><AdminVideoSettings /></AdminOperationsProvider>);
    const enabled = await screen.findByRole("checkbox", { name: "自動產生草稿" });
    fireEvent.click(enabled);
    fireEvent.change(screen.getByRole("spinbutton", { name: "多久產生一次新草稿（小時）" }), { target: { value: "48" } });
    const writer = screen.getByRole("group", { name: "撰稿" });
    fireEvent.change(writer.querySelectorAll("select")[1], { target: { value: "claude-opus-5-5" } });
    fireEvent.change(screen.getByRole("textbox", { name: "要避開的題材" }), { target: { value: "Stocks\n  Elections  \n" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存設定" }));
    await waitFor(() => expect(puts).toHaveLength(1));
    const body = puts[0] as Record<string, unknown>;
    expect(body).toMatchObject({ enabled: true, draft_interval_hours: 48, topic_avoid: ["Stocks", "Elections"] });
    expect((body.stage_models as Record<string, unknown>).writer).toEqual(opus);
    expect(body).not.toHaveProperty("model_options");
    expect((await screen.findByRole("status")).textContent).toBe("已儲存");
  });

  it("shows a vendor without a key and keeps a reader from saving", async () => {
    stubFetch();
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read"])}><AdminVideoSettings /></AdminOperationsProvider>);
    expect(await screen.findByText(/要有「管理設定」權限才能修改/)).toBeTruthy();
    expect(screen.getByRole("button", { name: "儲存設定" })).toHaveProperty("disabled", true);
    expect(screen.getAllByRole("option", { name: "OpenAI (沒有金鑰)" }).length).toBe(STAGES.length);
    expect(screen.getByText(/1 \/ 8 支草稿，呼叫模型 3 次（其中 1 次失敗）/)).toBeTruthy();
  });
});
