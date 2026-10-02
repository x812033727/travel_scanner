import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { patternSize, ShortsSettingsPanel } from "./admin-video-shorts-settings";
import type { AdminBootstrap } from "@/lib/admin-operations";

vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: null, sessionIdentity: null, status: undefined }) }));

function bootstrap(capabilities: string[], roles: string[] = []): AdminBootstrap {
  return { admin_roles: roles, admin_capabilities: capabilities, navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false };
}

const SHA = "a".repeat(64);
const scope = { channel_id: "UCfixturechannel0000000", channel_title: "Mokaair", lines: ["lab", "cut", "drama"], max_per_day: 2, slot_times: ["12:30", "19:30"], timezone: "Asia/Taipei" };
const offer = {
  text: ["我同意 Mokaair 網站在下面的範圍內，替我在 YouTube 頻道「Mokaair」上架 Shorts，不用每一支再問我：", "一、內容線：實測、長片精華、漫劇直式短篇。", "二、一天最多 2 支，公開時間是 12:30、19:30（Asia/Taipei）。"].join("\n"),
  text_sha256: SHA, scope,
};
const none = { state: "none", problem: null, granted_at: null, granted_by_user_id: null, expires_at: null, text_sha256: null, scope: null, offer };
const valid = { ...none, state: "valid", granted_at: "2026-10-01T03:00:00Z", expires_at: "2026-12-30T03:00:00Z", text_sha256: SHA, scope };
const settings = {
  enabled: false, lines: ["lab", "cut", "drama"], weekly_quota: { lab: 5, cut: 2, drama: 0 },
  daily_pattern: [{ days: 30, counts: [1] }, { days: 60, counts: [2, 1] }], slot_times: ["19:30", "12:30"], timezone: "Asia/Taipei",
  stock_days: 5, lock_hours: 24, upload_ahead_days: 10, max_per_day: 2, seconds_min: 25, seconds_max: 55,
  voice: { provider: "gemini", name: "Sulafat", style: null, model: null, rate: "+0%" }, locales: [], made_for_kids: false, auto_approve: true,
  budget_ntd_30d: 3000, budget_soft_ntd: 2400, budget_total_ntd: 9000,
  subject_models: { a: { provider: "claude_code", model: "claude-opus-5-5" } }, max_per_month: 120,
  campaign_start: null, autopublish: false, paused_at: null, consent: none, updated_at: "2026-10-01T00:00:00Z",
};
const option = (value: string) => ({ value, label: value, description: null, status: "ok" });
const tutorial = {
  voice_options: { gemini: ["Sulafat", "Kore"], gemini_models: ["gemini-3.8-flash-tts"], azure: [] },
  model_options: { claude_code: [option("claude-opus-5-5"), option("claude-sonnet-5")], codex: [option("gpt-6-codex")], anthropic: [], openai: [option("gpt-6"), option("gpt-6-mini")], gemini: [option("gemini-3.5-pro")], minimax: [] },
  configured_providers: ["claude_code", "codex", "gemini"],
};

type Call = { url: string; method: string; body: unknown };

function stubFetch(view: Record<string, unknown> = settings, refuse?: { status: number; code: string; detail: string }) {
  const calls: Call[] = [];
  vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    const call = { url: String(input), method: init?.method ?? "GET", body: init?.body ? JSON.parse(String(init.body)) : undefined };
    calls.push(call);
    if (call.method !== "GET" && refuse) return Promise.resolve(Response.json({ code: refuse.code, detail: refuse.detail }, { status: refuse.status }));
    if (call.url.endsWith("/admin/video-automation/settings")) return Promise.resolve(Response.json(tutorial));
    if (call.url.endsWith("/campaign/start")) return Promise.resolve(Response.json({ campaign_start: "2026-10-05", last_day: "2027-01-02", slots: 120, assigned: 3 }));
    if (call.url.endsWith("/autopublish")) return Promise.resolve(Response.json({ ...view, autopublish: call.method === "POST", consent: call.method === "POST" ? valid : none }));
    if (call.method === "PUT") return Promise.resolve(Response.json({ ...view, ...(call.body as object) }));
    return Promise.resolve(Response.json(view));
  }));
  return calls;
}

const writes = (calls: Call[]) => calls.filter((call) => call.method !== "GET");

function mount(capabilities = ["content.read", "content.manage", "settings.manage"], roles = ["owner"]) {
  const onChanged = vi.fn();
  render(<AdminOperationsProvider bootstrap={bootstrap(capabilities, roles)}><ShortsSettingsPanel onChanged={onChanged} /></AdminOperationsProvider>);
  return onChanged;
}

afterEach(() => vi.unstubAllGlobals());

describe("the pace of the run", () => {
  it("is thirty days of one and sixty of two and one in turn: 120 slots in ninety days", () => {
    expect(patternSize([{ days: 30, counts: [1] }, { days: 60, counts: [2, 1] }])).toEqual({ days: 90, slots: 120 });
    expect(patternSize([{ days: 7, counts: [0, 3] }])).toEqual({ days: 7, slots: 9 });
    expect(patternSize([])).toEqual({ days: 0, slots: 0 });
  });
});

describe("ShortsSettingsPanel", () => {
  it("shows the settings as they are stored and saves the whole of them", async () => {
    const calls = stubFetch();
    const onChanged = mount();
    const pace = await screen.findByRole("region", { name: "節奏與時段" });
    expect(pace.textContent).toContain("這樣排是 90 天、120 格。");
    const save = screen.getByRole("button", { name: "儲存 Shorts 設定" });
    expect(save).toHaveProperty("disabled", true);
    expect((within(pace).getByLabelText("公開時間（24 小時制，用逗號分開）") as HTMLInputElement).value).toBe("19:30, 12:30");

    fireEvent.change(within(pace).getAllByLabelText("每天幾支（輪流的話用逗號分開）")[1], { target: { value: "2，1, 1" } });
    fireEvent.change(within(pace).getByLabelText("片庫希望有幾天的量"), { target: { value: "7" } });
    expect(pace.textContent).toContain("這樣排是 90 天、110 格。");
    fireEvent.click(within(screen.getByRole("region", { name: "製作" })).getByLabelText("日文"));
    expect(save).toHaveProperty("disabled", false);
    fireEvent.click(save);
    await waitFor(() => expect(writes(calls)).toHaveLength(1));
    expect(writes(calls)[0]).toMatchObject({ method: "PUT" });
    expect(writes(calls)[0].url).toContain("/admin/video-shorts/settings");
    expect(writes(calls)[0].body).toEqual({
      enabled: false, lines: ["lab", "cut", "drama"], weekly_quota: { lab: 5, cut: 2, drama: 0 },
      daily_pattern: [{ days: 30, counts: [1] }, { days: 60, counts: [2, 1, 1] }], slot_times: ["19:30", "12:30"], timezone: "Asia/Taipei",
      stock_days: 7, lock_hours: 24, upload_ahead_days: 10, max_per_day: 2, seconds_min: 25, seconds_max: 55,
      voice: settings.voice, locales: ["ja"], made_for_kids: false, auto_approve: true,
      budget_ntd_30d: 3000, budget_soft_ntd: 2400, budget_total_ntd: 9000,
      subject_models: settings.subject_models, max_per_month: 120,
    });
    expect(await screen.findByRole("status")).toBeTruthy();
    expect(onChanged).toHaveBeenCalledTimes(1);
  });

  it("chooses the models under test from the AI settings page's menus, and how many Shorts a month", async () => {
    const calls = stubFetch();
    mount();
    const panel = await screen.findByRole("region", { name: "受測模型" });
    const a = within(panel).getByRole("group", { name: "A 組" });
    const b = within(panel).getByRole("group", { name: "B 組" });
    await waitFor(() => expect(within(a).getByLabelText("模型")).toHaveProperty("value", "claude-opus-5-5"));
    expect(within(b).getByLabelText("供應商")).toHaveProperty("value", "");
    expect(within(b).queryByLabelText("模型")).toBeNull();
    // A vendor the site has no key for says so in the menu, as on the AI settings page.
    expect(within(within(b).getByLabelText("供應商")).getByRole("option", { name: "OpenAI API (還不能用)" })).toBeTruthy();

    fireEvent.change(within(b).getByLabelText("供應商"), { target: { value: "openai" } });
    expect(within(b).getByLabelText("模型")).toHaveProperty("value", "gpt-6");
    fireEvent.change(within(b).getByLabelText("模型"), { target: { value: "gpt-6-mini" } });
    fireEvent.change(within(panel).getByLabelText("一個月最多開始做幾支"), { target: { value: "90" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存 Shorts 設定" }));
    await waitFor(() => expect(writes(calls)).toHaveLength(1));
    expect(writes(calls)[0].body).toMatchObject({
      subject_models: { a: { provider: "claude_code", model: "claude-opus-5-5" }, b: { provider: "openai", model: "gpt-6-mini" } },
      max_per_month: 90,
    });

    // Back to "same as A": b is left out, and the server tests a's model both ways.
    await screen.findByRole("status");
    fireEvent.change(within(b).getByLabelText("供應商"), { target: { value: "" } });
    fireEvent.change(within(a).getByLabelText("供應商"), { target: { value: "" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存 Shorts 設定" }));
    await waitFor(() => expect(writes(calls)).toHaveLength(2));
    expect((writes(calls)[1].body as { subject_models: unknown }).subject_models).toEqual({});
  });

  it("does not save a pattern it cannot read, and a line that is off carries no quota", async () => {
    const calls = stubFetch();
    mount();
    const pace = await screen.findByRole("region", { name: "節奏與時段" });
    const counts = within(pace).getAllByLabelText("每天幾支（輪流的話用逗號分開）")[0];
    fireEvent.change(counts, { target: { value: "5" } });
    expect(pace.textContent).toContain("每天幾支要是 0 到 4 的整數。");
    expect(screen.getByRole("button", { name: "儲存 Shorts 設定" })).toHaveProperty("disabled", true);
    fireEvent.change(counts, { target: { value: "1" } });
    fireEvent.click(within(screen.getByRole("region", { name: "內容線" })).getByLabelText("漫劇直式短篇"));
    fireEvent.click(screen.getByRole("button", { name: "儲存 Shorts 設定" }));
    await waitFor(() => expect(writes(calls)).toHaveLength(1));
    expect(writes(calls)[0].body).toMatchObject({ lines: ["lab", "cut"], weekly_quota: { lab: 5, cut: 2 } });
  });

  it("says what the server said when it refuses the settings", async () => {
    stubFetch(settings, { status: 422, code: "video_shorts_settings_invalid", detail: "daily_pattern asks for more a day than max_per_day" });
    mount();
    const pace = await screen.findByRole("region", { name: "節奏與時段" });
    fireEvent.change(within(pace).getByLabelText("一天最多幾支"), { target: { value: "1" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存 Shorts 設定" }));
    expect((await screen.findByRole("alert")).textContent).toContain("max_per_day");
  });

  it("warns that a change of what the consent names can end it, and asks again before saving it", async () => {
    const calls = stubFetch({ ...settings, autopublish: true, consent: valid });
    const confirm = vi.spyOn(window, "confirm").mockReturnValueOnce(false).mockReturnValue(true);
    mount();
    const pace = await screen.findByRole("region", { name: "節奏與時段" });
    expect(screen.queryByText(/自動上架授權可能失效/)).toBeNull();
    fireEvent.change(within(pace).getByLabelText("片庫希望有幾天的量"), { target: { value: "6" } });
    expect(screen.queryByText(/自動上架授權可能失效/)).toBeNull();
    // Not a field the consent names: saved without a question.
    fireEvent.click(screen.getByRole("button", { name: "儲存 Shorts 設定" }));
    await waitFor(() => expect(writes(calls)).toHaveLength(1));
    expect(confirm).not.toHaveBeenCalled();

    await screen.findByRole("status");
    fireEvent.change(within(pace).getByLabelText("公開時間（24 小時制，用逗號分開）"), { target: { value: "19:30, 13:00" } });
    expect(screen.getByText(/自動上架授權可能失效/)).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "儲存 Shorts 設定" }));
    expect(confirm).toHaveBeenCalledWith(expect.stringContaining("存了之後要重新授權"));
    expect(writes(calls)).toHaveLength(1);
    fireEvent.click(screen.getByRole("button", { name: "儲存 Shorts 設定" }));
    await waitFor(() => expect(writes(calls)).toHaveLength(2));
    expect(writes(calls)[1].body).toMatchObject({ slot_times: ["19:30", "13:00"] });
    confirm.mockRestore();
  });

  it("takes the owner's agreement only to the wording they read, named by its hash", async () => {
    const calls = stubFetch();
    const onChanged = mount();
    const card = await screen.findByRole("region", { name: "自動上架授權" });
    expect(card.textContent).toContain("還沒有授權");
    const wording = within(card).getByLabelText("你會同意的內容");
    expect(wording.textContent).toContain("替我在 YouTube 頻道「Mokaair」上架 Shorts");
    expect(within(wording).getAllByRole("listitem")).toHaveLength(2);
    const agree = within(card).getByRole("button", { name: "我同意，開始自動上架" });
    expect(agree).toHaveProperty("disabled", true);
    fireEvent.click(within(card).getByLabelText("我讀過上面每一項"));
    expect(agree).toHaveProperty("disabled", false);
    fireEvent.click(agree);
    await waitFor(() => expect(writes(calls)).toHaveLength(1));
    expect(writes(calls)[0]).toMatchObject({ method: "POST", body: { text_sha256: SHA } });
    expect(writes(calls)[0].url).toContain("/admin/video-shorts/autopublish");
    await waitFor(() => expect(card.textContent).toContain("有效"));
    expect(within(card).queryByRole("button", { name: "我同意，開始自動上架" })).toBeNull();
    expect(onChanged).toHaveBeenCalledTimes(1);

    const confirm = vi.spyOn(window, "confirm").mockReturnValue(true);
    fireEvent.click(within(card).getByRole("button", { name: "撤銷這份同意" }));
    await waitFor(() => expect(writes(calls)).toHaveLength(2));
    expect(writes(calls)[1]).toMatchObject({ method: "DELETE" });
    expect(confirm).toHaveBeenCalledOnce();
    await waitFor(() => expect(card.textContent).toContain("還沒有授權"));
    confirm.mockRestore();
  });

  it("asks for the settings to be saved before the wording is agreed to or the run is started", async () => {
    stubFetch();
    mount();
    const card = await screen.findByRole("region", { name: "自動上架授權" });
    const run = screen.getByRole("region", { name: "開跑" });
    fireEvent.change(within(run).getByLabelText("第一支公開的日期"), { target: { value: "2026-10-05" } });
    expect(within(run).getByRole("button", { name: "開跑" })).toHaveProperty("disabled", false);
    fireEvent.change(within(screen.getByRole("region", { name: "節奏與時段" })).getByLabelText("一天最多幾支"), { target: { value: "3" } });
    expect(card.textContent).toContain("先儲存，條文才會是新的");
    expect(within(card).getByLabelText("我讀過上面每一項")).toHaveProperty("disabled", true);
    expect(within(run).getByRole("button", { name: "開跑" })).toHaveProperty("disabled", true);
    expect(run.textContent).toContain("先儲存再開跑");
  });

  it("requires a fresh acknowledgement when saving settings changes the offered wording", async () => {
    const calls = stubFetch();
    const originalFetch = globalThis.fetch;
    const nextHash = "b".repeat(64);
    const nextOffer = { ...offer, text: offer.text + "\n三、更新後的公開時段。", text_sha256: nextHash, scope: { ...scope, slot_times: ["13:00", "19:30"] } };
    vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const answer = await originalFetch(input, init);
      if (init?.method !== "PUT") return answer;
      return Response.json({ ...settings, ...JSON.parse(String(init.body)), consent: { ...none, offer: nextOffer } });
    }));
    mount();
    const card = await screen.findByRole("region", { name: "自動上架授權" });
    fireEvent.click(within(card).getByLabelText("我讀過上面每一項"));
    expect(within(card).getByRole("button", { name: "我同意，開始自動上架" })).toHaveProperty("disabled", false);
    fireEvent.change(within(screen.getByRole("region", { name: "節奏與時段" })).getByLabelText("公開時間（24 小時制，用逗號分開）"), { target: { value: "19:30, 13:00" } });
    expect(within(card).getByRole("button", { name: "我同意，開始自動上架" })).toHaveProperty("disabled", true);
    fireEvent.click(screen.getByRole("button", { name: "儲存 Shorts 設定" }));
    await waitFor(() => expect(within(card).getByLabelText("你會同意的內容").textContent).toContain("更新後的公開時段"));
    const read = within(card).getByLabelText("我讀過上面每一項");
    expect(read).toHaveProperty("checked", false);
    const agree = within(card).getByRole("button", { name: "我同意，開始自動上架" });
    expect(agree).toHaveProperty("disabled", true);
    fireEvent.click(agree);
    expect(writes(calls).filter((call) => call.method === "POST")).toHaveLength(0);
    fireEvent.click(read);
    expect(agree).toHaveProperty("disabled", false);
    fireEvent.click(agree);
    await waitFor(() => expect(writes(calls).filter((call) => call.method === "POST")).toHaveLength(1));
    expect(writes(calls).find((call) => call.method === "POST")?.body).toEqual({ text_sha256: nextHash });
  });

  it("has nothing to agree to before a channel is linked, and offers a consent that ends soon again", async () => {
    stubFetch({ ...settings, consent: { ...none, offer: null } });
    const { unmount } = render(<ShortsSettingsPanel onChanged={vi.fn()} />);
    const card = await screen.findByRole("region", { name: "自動上架授權" });
    expect(card.textContent).toContain("要先在設定分頁連結 YouTube 頻道");
    expect(within(card).queryByRole("button")).toBeNull();
    unmount();
    stubFetch({ ...settings, autopublish: true, consent: { ...valid, state: "expiring", problem: "自動上架授權再 5 天到期" } });
    render(<ShortsSettingsPanel onChanged={vi.fn()} />);
    const again = await screen.findByRole("region", { name: "自動上架授權" });
    expect(again.textContent).toContain("快到期");
    expect(again.textContent).toContain("自動上架授權再 5 天到期");
    expect(within(again).getByRole("button", { name: "我同意，開始自動上架" })).toBeTruthy();
  });

  it("starts the run from the day the first Short goes public", async () => {
    const calls = stubFetch();
    const onChanged = mount();
    const run = await screen.findByRole("region", { name: "開跑" });
    const start = within(run).getByRole("button", { name: "開跑" });
    expect(start).toHaveProperty("disabled", true);
    fireEvent.change(within(run).getByLabelText("第一支公開的日期"), { target: { value: "2026-10-05" } });
    fireEvent.click(start);
    await waitFor(() => expect(writes(calls)).toHaveLength(1));
    expect(writes(calls)[0]).toMatchObject({ method: "POST", body: { first_day: "2026-10-05" } });
    expect(writes(calls)[0].url).toContain("/admin/video-shorts/campaign/start");
    expect((await within(run).findByRole("status")).textContent).toBe("建好了 120 格，排進 3 支，最後一天是 2027-01-02。");
    expect(onChanged).toHaveBeenCalledTimes(1);
  });

  it("asks before building a run again, and says why the server would not", async () => {
    const calls = stubFetch({ ...settings, campaign_start: "2026-10-05" }, { status: 409, code: "video_shorts_campaign_running", detail: "這一輪已經開始了，不能整個重排" });
    const confirm = vi.spyOn(window, "confirm").mockReturnValueOnce(false).mockReturnValue(true);
    mount();
    const run = await screen.findByRole("region", { name: "開跑" });
    expect(run.textContent).toContain("這一輪從 2026-10-05 開始。");
    const rebuild = within(run).getByRole("button", { name: "換日期重排" });
    fireEvent.click(rebuild);
    expect(writes(calls)).toHaveLength(0);
    fireEvent.click(rebuild);
    expect((await within(run).findByRole("alert")).textContent).toBe("沒有開跑：這一輪已經開始了，不能整個重排");
    confirm.mockRestore();
  });

  it("is read-only without the right to manage settings, and says which role has it", async () => {
    const calls = stubFetch();
    mount(["content.read", "content.manage"], ["content"]);
    const pace = await screen.findByRole("region", { name: "節奏與時段" });
    expect(screen.getByRole("note").textContent).toContain("要有「管理設定」權限才能修改");
    for (const input of pace.querySelectorAll("input")) expect(input).toHaveProperty("disabled", true);
    expect(screen.getByRole("button", { name: "儲存 Shorts 設定" })).toHaveProperty("disabled", true);
    expect(within(screen.getByRole("region", { name: "開跑" })).getByRole("button", { name: "開跑" })).toHaveProperty("disabled", true);
    const card = screen.getByRole("region", { name: "自動上架授權" });
    expect(within(card).queryByRole("button")).toBeNull();
    expect(within(card).queryByRole("checkbox")).toBeNull();
    // The wording can still be read by someone who may not agree to it.
    expect(within(card).getByLabelText("你會同意的內容")).toBeTruthy();
    expect(writes(calls)).toHaveLength(0);
  });
});
