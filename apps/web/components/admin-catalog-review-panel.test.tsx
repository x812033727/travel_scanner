import { act, cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminCatalogReviewPanel } from "./admin-catalog-review-panel";
import { ADMIN_REVIEW_COPY } from "@/lib/admin-review-copy";

const root = "/api/travel/admin/catalog-review";
const run = {
  id: "review-1", version: 3, mode: "review_pending", status: "completed", phase: "review_pending",
  model: "gemini-review-model", scope: "hotspots", requested_counts: { hotspot: 40, food: 0, merchant: 0 },
  counts: { total: 101, assessed: 101, approved: 2, rejected: 0, needs_review: 99, created: 0, duplicates: 0, failed: 0, applied: 0 },
  usage: { calls: 4, input_tokens: 123, output_tokens: 45 }, error_code: null, error_message: null,
  created_at: "2026-09-07T00:00:00Z", completed_at: "2026-09-07T00:01:00Z", review_complete: true, can_resume: false,
  max_calls: 80, can_extend_budget: false,
};
const overview = {
  configured: true, model: "gemini-configured-model", daily_call_limit: 300, run_call_limit: 80,
  pending_counts: { hotspot: 101, food: 20, merchant: 49, total: 170 },
  can_start_review: true, can_start_discovery: true, blocking_reasons: [], runs: [run],
};
const candidate = (id: string, name: string) => ({
  id, name, kind: "hotspot", entity_id: id, destination_id: "tokyo", phase: "review_pending",
  decision: "approve" as string | null, reason: "Official identity evidence matches.", evidence: [{ url: "https://example.org/official", quote: "Official attraction description." }],
  gaps: [] as string[], allowed_actions: ["approve", "reject", "keep_pending"], applied_action: null, status: "assessed", confidence: 0.98,
  error_code: null as string | null | undefined,
});
const response = (value: unknown, status = 200) => Promise.resolve(new Response(JSON.stringify(value), { status }));
const listing = (items: ReturnType<typeof candidate>[], page = 1, hasMore = false) => ({ items, total: hasMore ? 31 : items.length, page, page_size: 30, has_more: hasMore });
type FetchHandler = (url: string, init?: RequestInit) => Promise<Response> | undefined;

function mockApi(handler: FetchHandler = () => undefined) {
  const mock = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input).replace(/([?&])scope=[^&]+(&?)/, (_match, separator, trailing) => trailing ? separator : "").replace(/[?&]$/, "");
    const custom = handler(url, init);
    if (custom) return custom;
    if (url === root) return response(overview);
    if (url === root + "/runs/review-1") return response(run);
    if (url.includes("/items?")) return response(listing([]));
    throw new Error("Unexpected request: " + url);
  });
  vi.stubGlobal("fetch", mock);
  return mock;
}

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  vi.useRealTimers();
  window.history.replaceState(null, "", "/");
});

describe("AdminCatalogReviewPanel", () => {
  it("starts with the server-configured budget and shows the selected run's separate historical cap", async () => {
    const fetchMock = mockApi((url, init) => {
      if (url === root) return response({ ...overview, run_call_limit: 200 });
      if (url === root + "/runs" && init?.method === "POST") return response({ ...run, status: "queued", max_calls: 200 });
      return undefined;
    });
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    expect(await screen.findByText("新工作呼叫上限 200 次；共用每日上限 300 次。")).toBeTruthy();
    expect(await screen.findByText("此工作原有累計上限 80 次；已使用 4 次。")).toBeTruthy();
    expect(screen.getByRole("link", { name: "設定審核呼叫上限" }).getAttribute("href")).toBe("/zh-TW/admin/settings?provider=gemini_guides&field=catalog_review_max_calls");
    fireEvent.click(screen.getByRole("button", { name: "開始審核現有待審" }));
    await waitFor(() => expect(fetchMock.mock.calls.some(([, init]) => init?.method === "POST")).toBe(true));
    expect(JSON.parse(String(fetchMock.mock.calls.find(([, init]) => init?.method === "POST")![1]!.body)).max_calls).toBe(200);
  });

  it.each([undefined, 0, 1001])("does not start without a valid server budget (%s)", async (limit) => {
    const fetchMock = mockApi((url) => url === root ? response({ ...overview, run_call_limit: limit }) : undefined);
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    await screen.findByText("此工作原有累計上限 80 次；已使用 4 次。");
    const start = screen.getByRole("button", { name: "開始審核現有待審" });
    expect((start as HTMLButtonElement).disabled).toBe(true);
    fireEvent.click(start);
    expect(fetchMock.mock.calls.filter(([, init]) => init?.method === "POST")).toHaveLength(0);
  });

  it("requires explicit focused confirmation to extend a stopped run without resetting cumulative calls", async () => {
    let current = { ...run, status: "partial", can_resume: false, can_extend_budget: true, usage: { ...run.usage, calls: 80 } };
    const fetchMock = mockApi((url, init) => {
      if (url === root) return response({ ...overview, run_call_limit: 200, runs: [current] });
      if (url === root + "/runs/review-1") return response(current);
      if (url.endsWith("/resume") && init?.method === "POST") {
        current = { ...current, status: "queued", can_extend_budget: false, max_calls: 200 };
        return response(current);
      }
      return undefined;
    });
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    const opener = await screen.findByRole("button", { name: "提高上限並續跑…" });
    opener.focus();
    fireEvent.click(opener);
    const dialog = screen.getByRole("dialog", { name: "確認提高此工作的呼叫上限並續跑" });
    const cancel = within(dialog).getByRole("button", { name: "返回檢查" });
    const confirm = within(dialog).getByRole("button", { name: "確認提高並續跑" });
    expect(document.activeElement).toBe(cancel);
    expect(within(dialog).getByText("120")).toBeTruthy();
    expect(within(dialog).getByText(/累計呼叫、已完成評估及套用結果不會歸零/)).toBeTruthy();
    fireEvent.keyDown(cancel, { key: "Tab", shiftKey: true });
    expect(document.activeElement).toBe(confirm);
    fireEvent.keyDown(confirm, { key: "Escape" });
    expect(screen.queryByRole("dialog")).toBeNull();
    expect(document.activeElement).toBe(opener);
    expect(fetchMock.mock.calls.filter(([, init]) => init?.method === "POST")).toHaveLength(0);
    fireEvent.click(opener);
    fireEvent.click(screen.getByRole("button", { name: "確認提高並續跑" }));
    await waitFor(() => expect(fetchMock.mock.calls.some(([, init]) => init?.method === "POST")).toBe(true));
    const writes = fetchMock.mock.calls.filter(([, init]) => init?.method === "POST");
    expect(writes).toHaveLength(1);
    expect(String(writes[0][0])).toBe(root + "/runs/review-1/resume?scope=hotspots");
    expect(JSON.parse(String(writes[0][1]!.body))).toEqual({ expected_version: 3, max_calls: 200 });
    expect(await screen.findByText("此工作原有累計上限 200 次；已使用 80 次。")).toBeTruthy();
  });

  it("discards budget consent on browser navigation and scope changes without resuming", async () => {
    const partial = { ...run, status: "partial", can_extend_budget: true, usage: { ...run.usage, calls: 80 } };
    const second = { ...partial, id: "review-2", version: 8 };
    const fetchMock = mockApi((url) => {
      if (url === root) return response({ ...overview, run_call_limit: 200, runs: [partial, second] });
      if (url === root + "/runs/review-1") return response(partial);
      if (url === root + "/runs/review-2") return response(second);
      return undefined;
    });
    const view = render(<AdminCatalogReviewPanel scope="hotspots" />);
    fireEvent.click(await screen.findByRole("button", { name: "提高上限並續跑…" }));
    expect(screen.getByRole("dialog")).toBeTruthy();
    await act(async () => {
      window.history.pushState(null, "", "/?run=review-2");
      window.dispatchEvent(new PopStateEvent("popstate"));
    });
    expect(screen.queryByRole("dialog")).toBeNull();
    fireEvent.click(await screen.findByRole("button", { name: "提高上限並續跑…" }));
    view.rerender(<AdminCatalogReviewPanel scope="foods" />);
    expect(screen.queryByRole("dialog")).toBeNull();
    expect(fetchMock.mock.calls.filter(([, init]) => init?.method === "POST")).toHaveLength(0);
  });

  it.each([409, 422, 503])("refreshes failed budget extensions (%s) and requires fresh confirmation", async (status) => {
    const partial = { ...run, status: "partial", can_extend_budget: true, usage: { ...run.usage, calls: 80 } };
    const fetchMock = mockApi((url, init) => {
      if (url === root) return response({ ...overview, run_call_limit: 200, runs: [partial] });
      if (url === root + "/runs/review-1") return response(partial);
      if (url.endsWith("/resume") && init?.method === "POST") return response({ detail: "Budget request needs confirmation." }, status);
      return undefined;
    });
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    fireEvent.click(await screen.findByRole("button", { name: "提高上限並續跑…" }));
    fireEvent.click(screen.getByRole("button", { name: "確認提高並續跑" }));
    await waitFor(() => expect(screen.queryByRole("dialog")).toBeNull());
    await screen.findByRole("button", { name: "提高上限並續跑…" });
    expect(fetchMock.mock.calls.filter(([, init]) => init?.method === "POST")).toHaveLength(1);
  });

  it.each(["running", "queued", "completed", "cancelled"])("never infers budget extension permission from %s status", async (status) => {
    mockApi((url) => url === root ? response({ ...overview, run_call_limit: 200 }) : url === root + "/runs/review-1" ? response({ ...run, status, can_extend_budget: false }) : undefined);
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    await screen.findByText("此工作原有累計上限 80 次；已使用 4 次。");
    expect(screen.queryByRole("button", { name: "提高上限並續跑…" })).toBeNull();
  });

  it("allows explicitly server-authorized orphaned worker recovery without starting it automatically", async () => {
    const fetchMock = mockApi((url) => url === root ? response({ ...overview, run_call_limit: 200, active_run: { id: run.id, scope: run.scope, status: "running" } }) : url === root + "/runs/review-1" ? response({ ...run, status: "running", can_extend_budget: true }) : undefined);
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    fireEvent.click(await screen.findByRole("button", { name: "提高上限並續跑…" }));
    expect(screen.getByRole("dialog")).toBeTruthy();
    expect(fetchMock.mock.calls.filter(([, init]) => init?.method === "POST")).toHaveLength(0);
  });

  it("offers budget settings and confirmed extension for old mixed history without creating a mixed run", async () => {
    const partial = { ...run, scope: undefined, status: "partial", can_extend_budget: true, usage: { ...run.usage, calls: 80 } };
    const fetchMock = mockApi((url, init) => {
      if (url === root) return response({ ...overview, run_call_limit: 160, runs: [partial] });
      if (url === root + "/runs/review-1") return response(partial);
      if (url.endsWith("/resume") && init?.method === "POST") return response({ ...partial, status: "queued", max_calls: 160, can_extend_budget: false });
      return undefined;
    });
    render(<AdminCatalogReviewPanel />);
    fireEvent.click(await screen.findByRole("button", { name: "提高上限並續跑…" }));
    fireEvent.click(screen.getByRole("button", { name: "確認提高並續跑" }));
    await waitFor(() => expect(fetchMock.mock.calls.some(([url, init]) => String(url).endsWith("/resume?scope=all") && init?.method === "POST")).toBe(true));
    expect(screen.getByRole("link", { name: "設定審核呼叫上限" })).toBeTruthy();
    expect(screen.queryByRole("button", { name: "開始審核現有待審" })).toBeNull();
  });

  it("explains the cumulative cap without suggesting another paid duplicate run", async () => {
    mockApi((url) => url === root + "/runs/review-1" ? response({ ...run, status: "partial", error_code: "catalog_review_call_limit", error_message: "old start a new run advice" }) : undefined);
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    expect(await screen.findByText(/此工作已達累計呼叫上限/)).toBeTruthy();
    expect(screen.queryByText("old start a new run advice")).toBeNull();
  });

  it("keeps mixed history usable without offering new mixed runs", async () => {
    const legacy = { ...run, scope: undefined, status: "partial", can_resume: true };
    const fetchMock = mockApi((url, init) => {
      if (url === root) return response({ ...overview, runs: [legacy] });
      if (url === root + "/runs/review-1") return response(legacy);
      if (url === root + "/runs/review-1/resume" && init?.method === "POST") return response({ ...legacy, scope: "all", status: "queued", can_resume: false });
      return undefined;
    });
    render(<AdminCatalogReviewPanel />);
    await screen.findByRole("button", { name: "繼續未完成工作" }, { timeout: 5_000 });
    expect(screen.queryByRole("button", { name: "開始審核現有待審" })).toBeNull();
    expect(screen.queryByRole("button", { name: /開始尋找/ })).toBeNull();
    expect(within(screen.getByRole("combobox", { name: "選擇審核工作" })).getByRole("option").textContent).toContain("跨領域（舊版混合）");
    fireEvent.click(screen.getByRole("button", { name: "繼續未完成工作" }));
    await waitFor(() => expect(fetchMock.mock.calls.some(([url, init]) => String(url).endsWith("/resume?scope=all") && init?.method === "POST")).toBe(true));
    expect(fetchMock.mock.calls.find(([url, init]) => String(url).endsWith("/resume?scope=all") && init?.method === "POST")![1]!.body).toBeUndefined();
  });

  it("starts foods discovery with only dishes and merchants and a same-scope prior review", async () => {
    const foodRun = { ...run, scope: "foods" };
    const fetchMock = mockApi((url, init) => {
      if (url === root) return response({ ...overview, pending_counts: { hotspot: 0, food: 20, merchant: 49, total: 69 }, runs: [foodRun] });
      if (url === root + "/runs/review-1") return response(foodRun);
      if (url === root + "/runs" && init?.method === "POST") return response({ ...foodRun, status: "queued" });
      return undefined;
    });
    render(<AdminCatalogReviewPanel scope="foods" />);
    await waitFor(() => expect((screen.getByRole("button", { name: "開始尋找 60 筆候選" }) as HTMLButtonElement).disabled).toBe(false));
    expect(screen.getByText("料理 20 筆 · 店家 40 筆；不包含景點。")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "開始尋找 60 筆候選" }));
    await waitFor(() => expect(fetchMock.mock.calls.some(([, init]) => init?.method === "POST")).toBe(true));
    const init = fetchMock.mock.calls.find(([, init]) => init?.method === "POST")![1]!;
    expect(JSON.parse(String(init.body))).toEqual({ mode: "discover_new", scope: "foods", requested_counts: { hotspot: 0, food: 20, merchant: 40 }, max_calls: 80, prior_review_run_id: "review-1" });
    expect(fetchMock.mock.calls.some(([url]) => String(url) === root + "?scope=foods")).toBe(true);
  });

  it("does not reuse a mixed or other-domain review as a discovery prerequisite", async () => {
    mockApi();
    render(<AdminCatalogReviewPanel scope="foods" />);
    await screen.findByText("gemini-review-model", { exact: false });
    expect((screen.getByRole("button", { name: "開始尋找 60 筆候選" }) as HTMLButtonElement).disabled).toBe(true);
  });

  it("names the other active domain and leaves its work outside this workspace", async () => {
    mockApi((url) => url === root ? response({ ...overview, runs: [], can_start_review: false, can_start_discovery: false, active_run: { id: "food-run", scope: "foods", status: "running" } }) : undefined);
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    expect(await screen.findByText(/美食與店家工作正在執行/)).toBeTruthy();
    expect(screen.getByRole("link", { name: "查看執行中工作" }).getAttribute("href")).toBe("/zh-TW/admin/catalog-review");
    expect((screen.getByRole("button", { name: "開始審核現有待審" }) as HTMLButtonElement).disabled).toBe(true);
  });

  it("keeps five-locale domain copy complete with matching substitution parameters", () => {
    expect(Object.keys(ADMIN_REVIEW_COPY).sort()).toEqual(["en", "ja", "ko", "zh-CN", "zh-TW"]);
    for (const copy of Object.values(ADMIN_REVIEW_COPY)) {
      expect(Object.keys(copy).sort()).toEqual(Object.keys(ADMIN_REVIEW_COPY.en).sort());
      expect(Object.keys(copy.scopes).sort()).toEqual(["all", "foods", "hotspots"]);
      for (const key of ["activeElsewhere", "discovery", "startDiscovery"] as const) {
        expect(copy[key].match(/\{[^}]+\}/g)).toEqual(ADMIN_REVIEW_COPY.en[key].match(/\{[^}]+\}/g));
      }
    }
  });

  it("clears selected rows and confirmations when the containing workspace changes scope", async () => {
    mockApi((url) => url.includes("/items?") ? response(listing([candidate("one", "Scope switch row")])) : undefined);
    const view = render(<AdminCatalogReviewPanel scope="hotspots" />);
    fireEvent.click(await screen.findByRole("checkbox", { name: "選取 Scope switch row" }));
    fireEvent.click(screen.getByRole("button", { name: "預覽選取的 1 筆" }));
    expect(screen.getByRole("dialog")).toBeTruthy();
    view.rerender(<AdminCatalogReviewPanel scope="foods" />);
    expect(screen.queryByRole("dialog")).toBeNull();
    await screen.findByRole("button", { name: "開始尋找 60 筆候選" });
    expect((screen.getByRole("button", { name: "預覽選取的 0 筆" }) as HTMLButtonElement).disabled).toBe(true);
  });

  it("discards a pending confirmation when browser history selects another run", async () => {
    const secondRun = { ...run, id: "review-2", version: 8 };
    const fetchMock = mockApi((url) => {
      if (url === root) return response({ ...overview, runs: [run, secondRun] });
      if (url === root + "/runs/review-2") return response(secondRun);
      if (url.includes("/runs/review-1/items?")) return response(listing([candidate("one", "First run candidate")]));
      if (url.includes("/runs/review-2/items?")) return response(listing([candidate("two", "Second run candidate")]));
      return undefined;
    });
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    fireEvent.click(await screen.findByRole("checkbox", { name: "選取 First run candidate" }));
    fireEvent.click(screen.getByRole("button", { name: "預覽選取的 1 筆" }));
    expect(screen.getByRole("dialog")).toBeTruthy();

    await act(async () => {
      window.history.pushState(null, "", "/?run=review-2&page=1&action=approve");
      window.dispatchEvent(new PopStateEvent("popstate"));
    });

    expect(screen.queryByRole("dialog")).toBeNull();
    await screen.findByText("Second run candidate");
    expect(screen.queryByText("First run candidate")).toBeNull();
    expect(fetchMock.mock.calls.filter(([, init]) => init?.method === "POST")).toHaveLength(0);
  });

  it("disables requests using server capabilities and preserves blocking reasons", async () => {
    mockApi((url) => url === root ? response({ ...overview, configured: false, can_start_review: false, can_start_discovery: false, runs: [], blocking_reasons: ["catalog_review_daily_limit_reached"] }) : undefined);
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    expect(await screen.findByText("catalog_review_daily_limit_reached")).toBeTruthy();
    expect((screen.getByRole("button", { name: "開始審核現有待審" }) as HTMLButtonElement).disabled).toBe(true);
    expect((screen.getByRole("button", { name: "開始尋找 40 筆候選" }) as HTMLButtonElement).disabled).toBe(true);
    expect(screen.getByText("Gemini 尚未設定，請先完成服務設定。")).toBeTruthy();
  });

  it("explains a known blocking reason in the current language", async () => {
    mockApi((url) => url === root ? response({ ...overview, can_start_review: false, can_start_discovery: false, blocking_reasons: ["catalog_run_in_progress"] }) : undefined);
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    expect(await screen.findByText("已有目錄審核正在進行，請先查看進度或續跑未完成工作。")).toBeTruthy();
    expect(screen.queryByText("catalog_run_in_progress")).toBeNull();
    expect((screen.getByRole("button", { name: "開始審核現有待審" }) as HTMLButtonElement).disabled).toBe(true);
  });

  it.each([0, 876])("shows thought tokens separately when the server reports %s", async (thoughtTokens) => {
    mockApi((url) => url === root + "/runs/review-1" ? response({ ...run, usage: { ...run.usage, thought_tokens: thoughtTokens } }) : undefined);
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    expect(await screen.findByText(`已呼叫 4 次 · 輸入 123 tokens · 輸出 45 tokens · 思考 ${thoughtTokens} tokens`)).toBeTruthy();
  });

  it("does not invent thought token usage for older run responses", async () => {
    mockApi();
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    await screen.findByText("已呼叫 4 次 · 輸入 123 tokens · 輸出 45 tokens");
    expect(screen.queryByText(/思考 .* tokens/)).toBeNull();
  });

  it.each([
    ["catalog_response_truncated", "Gemini 回應未完整傳回，這筆評估未完成。"],
    ["catalog_response_blocked", "Gemini 安全檢查阻擋了回應，未取得可用評估。"],
    ["catalog_response_empty", "Gemini 未傳回可用的評估內容。"],
    ["catalog_response_invalid", "Gemini 回應格式不符合審核要求。"],
    ["catalog_response_ids_invalid", "Gemini 回應的項目識別碼與這批候選不符。"],
    ["catalog_provider_rate_limited", "Gemini 暫時限制請求頻率，請稍後再試。"],
    ["catalog_provider_timeout", "Gemini 回應逾時，這筆評估未完成。"],
    ["catalog_provider_unavailable", "Gemini 服務暫時無法使用，這筆評估未完成。"],
  ])("explains %s without displaying internal exceptions", async (code, description) => {
    mockApi((url) => url.includes("/items?") ? response(listing([{ ...candidate("one", "Failed assessment"), status: "error", decision: null, reason: "ValueError: internal response details", error_code: code }])) : undefined);
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    expect(await screen.findByText(description)).toBeTruthy();
    expect(screen.queryByText(/ValueError/)).toBeNull();
    expect(screen.queryByText(code)).toBeNull();
    expect((screen.getByRole("checkbox", { name: "選取 Failed assessment" }) as HTMLInputElement).disabled).toBe(true);
  });

  it.each([null, undefined, "unrecognized_internal_error"])("uses a safe fallback for an error row with code %s", async (code) => {
    mockApi((url) => url.includes("/items?") ? response(listing([{ ...candidate("one", "Legacy failure"), status: "error", decision: null, reason: "ValueError: internal response details", error_code: code }])) : undefined);
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    expect(await screen.findByText("這筆評估未完成，未記錄可辨識的原因；尚未套用判斷，請檢查服務狀態後重試。")).toBeTruthy();
    expect(screen.queryByText(/ValueError|unrecognized_internal_error/)).toBeNull();
    expect(screen.queryByText("Gemini 回應格式不符合審核要求。")).toBeNull();
  });

  it("starts a pending review with the fixed counts and call budget", async () => {
    const fetchMock = mockApi((url, init) => {
      if (url === root) return response({ ...overview, can_start_discovery: false, runs: [] });
      if (url === root + "/runs" && init?.method === "POST") return response({ ...run, status: "queued" }, 202);
      return undefined;
    });
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    await waitFor(() => expect((screen.getByRole("button", { name: "開始審核現有待審" }) as HTMLButtonElement).disabled).toBe(false));
    fireEvent.click(screen.getByRole("button", { name: "開始審核現有待審" }));
    await waitFor(() => expect(fetchMock.mock.calls.some(([, init]) => init?.method === "POST")).toBe(true));
    const init = fetchMock.mock.calls.find(([, init]) => init?.method === "POST")![1]!;
    expect(JSON.parse(String(init.body))).toEqual({ mode: "review_pending", scope: "hotspots", requested_counts: { hotspot: 40, food: 0, merchant: 0 }, max_calls: 80 });
    expect((init.headers as Record<string, string>)["Idempotency-Key"]).toMatch(/^[0-9a-f-]{36}$/i);
  });

  it("allows discovery after review completion even when items remain pending", async () => {
    const fetchMock = mockApi((url, init) => url === root + "/runs" && init?.method === "POST" ? response({ ...run, mode: "discover_new", status: "queued" }, 202) : undefined);
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    const start = await screen.findByRole("button", { name: "開始尋找 40 筆候選" });
    await waitFor(() => expect((start as HTMLButtonElement).disabled).toBe(false));
    expect(screen.getByText("僅景點 40 筆；不包含料理或店家。")).toBeTruthy();
    expect(screen.getByText(/新候選先存為待審且不啟用/)).toBeTruthy();
    fireEvent.click(start);
    await waitFor(() => expect(fetchMock.mock.calls.some(([, init]) => init?.method === "POST")).toBe(true));
    const init = fetchMock.mock.calls.find(([, init]) => init?.method === "POST")![1]!;
    expect(JSON.parse(String(init.body))).toEqual({ mode: "discover_new", prior_review_run_id: "review-1", scope: "hotspots", requested_counts: { hotspot: 40, food: 0, merchant: 0 }, max_calls: 80 });
  });

  it("keeps discovery disabled when the server denies it despite a completed review", async () => {
    mockApi((url) => url === root ? response({ ...overview, can_start_discovery: false, blocking_reasons: ["Another run is active."] }) : undefined);
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    expect(await screen.findByText("Another run is active.")).toBeTruthy();
    expect((screen.getByRole("button", { name: "開始尋找 40 筆候選" }) as HTMLButtonElement).disabled).toBe(true);
  });

  it("requires eligible rows and a confirmation, then reports actual per-item outcomes", async () => {
    const first = candidate("one", "Verified shrine");
    const second = candidate("two", "Verified museum");
    const missing = { ...candidate("missing", "Missing Naver"), confidence: 1, gaps: ["Exact Naver identity is missing."] };
    const denied = { ...candidate("denied", "Server denied"), allowed_actions: ["keep_pending"] };
    const records = [first, second, missing, denied];
    const fetchMock = mockApi((url, init) => {
      if (url.includes("/items?")) return response(listing(records));
      if (url.endsWith("/apply") && init?.method === "POST") return response({ run: { ...run, version: 4 }, updated: 1, outcomes: [{ id: "one", action: "approve", status: "applied", reason: "Saved." }, { id: "two", action: "approve", status: "skipped", reason: "candidate_changed" }] });
      return undefined;
    });
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    expect(await screen.findByText("Verified shrine")).toBeTruthy();
    expect(screen.getByText(/Gemini · 模型 gemini-review-model/)).toBeTruthy();
    expect(screen.getAllByText("Official attraction description.")).toHaveLength(4);
    expect((screen.getByRole("checkbox", { name: "選取 Missing Naver" }) as HTMLInputElement).disabled).toBe(true);
    expect((screen.getByRole("checkbox", { name: "選取 Server denied" }) as HTMLInputElement).disabled).toBe(true);
    fireEvent.click(screen.getByRole("button", { name: "選取本頁可操作項目（2）" }));
    fireEvent.click(screen.getByRole("button", { name: "預覽選取的 2 筆" }));
    const dialog = screen.getByRole("dialog", { name: "確認核准 2 筆" });
    expect(within(dialog).getByText("Verified shrine")).toBeTruthy();
    expect(within(dialog).queryByText("Missing Naver")).toBeNull();
    expect(fetchMock.mock.calls.filter(([, init]) => init?.method === "POST")).toHaveLength(0);
    fireEvent.click(within(dialog).getByRole("button", { name: "確認並套用" }));
    expect(await screen.findByText("實際更新 1 筆")).toBeTruthy();
    expect(screen.getByText("候選資料在評估後已變更，請重新審核")).toBeTruthy();
    expect(screen.queryByText("candidate_changed")).toBeNull();
    const init = fetchMock.mock.calls.find(([input]) => String(input).endsWith("/apply?scope=hotspots"))![1]!;
    expect(JSON.parse(String(init.body))).toEqual({ item_ids: ["one", "two"], action: "approve", expected_version: 3 });
  });

  it("localizes known verification gaps while preserving an unknown requirement", async () => {
    const gaps = [
      "missing_source", "missing_five_locale_content", "missing_destination", "missing_meal_type",
      "missing_wikidata_identity", "missing_exact_map_identity", "map_not_independently_verified",
      "missing_durable_coordinates", "coordinates_not_verified", "missing_direct_merchant_source",
      "missing_food_category", "missing_verified_source_evidence", "low_assessment_confidence",
    ];
    mockApi((url) => url.includes("/items?") ? response(listing([{ ...candidate("one", "Incomplete candidate"), gaps: [...gaps, "future_verification_requirement"] }])) : undefined);
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    const requirements = await screen.findByRole("list", { name: "Incomplete candidate 的缺項" });
    expect(within(requirements).getByText("缺少精準地圖身分（韓國須 Naver，其餘須 Google Place ID）")).toBeTruthy();
    expect(within(requirements).getByText("缺少有永久來源佐證的座標")).toBeTruthy();
    expect(within(requirements).getByText("缺少可追溯來源")).toBeTruthy();
    expect(within(requirements).getAllByRole("listitem")).toHaveLength(14);
    for (const code of gaps) expect(within(requirements).queryByText(code)).toBeNull();
    expect(within(requirements).getByText("future_verification_requirement")).toBeTruthy();
    expect((screen.getByRole("checkbox", { name: "選取 Incomplete candidate" }) as HTMLInputElement).disabled).toBe(true);
  });

  it.each(["queued", "running"])("keeps assessed evidence readable but blocks applying while %s", async (status) => {
    const fetchMock = mockApi((url) => {
      if (url === root + "/runs/review-1") return response({ ...run, status, review_complete: false });
      if (url.includes("/items?")) return response(listing([candidate("one", "Assessed during run")]));
      return undefined;
    });
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    await screen.findByText("Assessed during run");
    expect(screen.getByText("Official attraction description.")).toBeTruthy();
    expect(screen.getByText(/工作仍在排隊或執行中/)).toBeTruthy();
    expect((screen.getByRole("checkbox", { name: "選取 Assessed during run" }) as HTMLInputElement).disabled).toBe(true);
    const selectPage = screen.getByRole("button", { name: "選取本頁可操作項目（1）" });
    expect((selectPage as HTMLButtonElement).disabled).toBe(true);
    fireEvent.click(selectPage);
    expect((screen.getByRole("button", { name: "預覽選取的 0 筆" }) as HTMLButtonElement).disabled).toBe(true);
    expect(screen.queryByRole("dialog")).toBeNull();
    expect(fetchMock.mock.calls.filter(([, init]) => init?.method === "POST")).toHaveLength(0);
  });

  it("clears selection on pagination and never selects unseen rows", async () => {
    const fetchMock = mockApi((url) => {
      if (url.includes("/items?page=1")) return response(listing([candidate("one", "First page")], 1, true));
      if (url.includes("/items?page=2")) return response(listing([candidate("two", "Second page")], 2, false));
      return undefined;
    });
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    await screen.findByText("First page");
    fireEvent.click(screen.getByRole("checkbox", { name: "選取 First page" }));
    fireEvent.click(screen.getByRole("button", { name: "下一頁" }));
    await screen.findByText("Second page");
    expect((screen.getByRole("button", { name: "預覽選取的 0 筆" }) as HTMLButtonElement).disabled).toBe(true);
    expect((screen.getByRole("checkbox", { name: "選取 Second page" }) as HTMLInputElement).checked).toBe(false);
    expect(fetchMock.mock.calls.some(([url]) => String(url).endsWith("items?page=2&page_size=30&scope=hotspots"))).toBe(true);
  });

  it("reuses the apply idempotency key after an uncertain network response", async () => {
    let attempts = 0;
    const fetchMock = mockApi((url, init) => {
      if (url.includes("/items?")) return response(listing([candidate("one", "Retry candidate")]));
      if (url.endsWith("/apply") && init?.method === "POST") {
        attempts += 1;
        return attempts === 1 ? Promise.reject(new TypeError("Network interrupted")) : response({ run, updated: 1, outcomes: [] });
      }
      return undefined;
    });
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    await screen.findByText("Retry candidate");
    fireEvent.click(screen.getByRole("checkbox", { name: "選取 Retry candidate" }));
    fireEvent.click(screen.getByRole("button", { name: "預覽選取的 1 筆" }));
    fireEvent.click(screen.getByRole("button", { name: "確認並套用" }));
    await screen.findByText("Network interrupted");
    fireEvent.click(screen.getByRole("button", { name: "確認並套用" }));
    await screen.findByText("實際更新 1 筆");
    const calls = fetchMock.mock.calls.filter(([url]) => String(url).endsWith("/apply?scope=hotspots"));
    expect(calls).toHaveLength(2);
    expect(calls[0][1]!.headers).toEqual(calls[1][1]!.headers);
    expect(calls[0][1]!.body).toBe(calls[1][1]!.body);
  });

  it("refreshes an outdated assessment after 409 without silently replaying approval", async () => {
    let version = 3;
    const fetchMock = mockApi((url, init) => {
      if (url === root + "/runs/review-1") return response({ ...run, version });
      if (url.includes("/items?")) return response(listing([candidate("one", "Changed candidate")]));
      if (url.endsWith("/apply") && init?.method === "POST") { version = 7; return response({ detail: "Assessment version changed." }, 409); }
      return undefined;
    });
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    await screen.findByText("Changed candidate");
    fireEvent.click(screen.getByRole("checkbox", { name: "選取 Changed candidate" }));
    fireEvent.click(screen.getByRole("button", { name: "預覽選取的 1 筆" }));
    fireEvent.click(screen.getByRole("button", { name: "確認並套用" }));
    await screen.findByText("Assessment version changed.");
    expect(screen.queryByRole("dialog")).toBeNull();
    await waitFor(() => expect((screen.getByRole("checkbox", { name: "選取 Changed candidate" }) as HTMLInputElement).disabled).toBe(false));
    expect(fetchMock.mock.calls.filter(([url]) => String(url).endsWith("/apply?scope=hotspots"))).toHaveLength(1);
    fireEvent.click(screen.getByRole("checkbox", { name: "選取 Changed candidate" }));
    fireEvent.click(screen.getByRole("button", { name: "預覽選取的 1 筆" }));
    fireEvent.click(screen.getByRole("button", { name: "確認並套用" }));
    await waitFor(() => expect(fetchMock.mock.calls.filter(([url]) => String(url).endsWith("/apply?scope=hotspots"))).toHaveLength(2));
    const last = fetchMock.mock.calls.filter(([url]) => String(url).endsWith("/apply?scope=hotspots"))[1][1]!;
    expect(JSON.parse(String(last.body)).expected_version).toBe(7);
  });

  it("shows partial work and resumes only when the server allows it", async () => {
    const partial = { ...run, status: "partial", can_resume: true, review_complete: false, error_code: "gemini_daily_budget_exhausted", error_message: "Daily call budget reached." };
    const fetchMock = mockApi((url, init) => {
      if (url === root) return response({ ...overview, runs: [partial] });
      if (url === root + "/runs/review-1") return response(partial);
      if (url.endsWith("/resume") && init?.method === "POST") return response({ ...partial, status: "queued", can_resume: false });
      return undefined;
    });
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    await screen.findByText("Daily call budget reached.");
    expect(screen.getByText("gemini_daily_budget_exhausted")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "繼續未完成工作" }));
    await waitFor(() => expect(fetchMock.mock.calls.some(([url, init]) => String(url).endsWith("/resume?scope=hotspots") && init?.method === "POST")).toBe(true));
  });

  it("keeps 21 missing Gemini assessments incomplete and unavailable for discovery or applying", async () => {
    const partial = { ...run, status: "partial", can_resume: true, review_complete: false, counts: { ...run.counts, total: 307, assessed: 286, failed: 21 } };
    const missing = Array.from({ length: 21 }, (_, index) => ({ ...candidate(`missing-${index}`, `Missing assessment ${index}`), status: "error", decision: null, confidence: 0, reason: "Gemini未回傳這筆候選", evidence: [], allowed_actions: [], error_code: "catalog_response_ids_invalid" }));
    const fetchMock = mockApi((url) => {
      if (url === root) return response({ ...overview, can_start_discovery: false, runs: [partial] });
      if (url === root + "/runs/review-1") return response(partial);
      if (url.includes("/items?")) return response({ ...listing(missing), total: 307, has_more: true });
      return undefined;
    });
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    await screen.findByText("Missing assessment 20");
    expect(screen.getByText("已評估", { selector: "dt" }).parentElement?.textContent).toBe("已評估286");
    expect(screen.getByText("評估失敗", { selector: "dt" }).parentElement?.textContent).toBe("評估失敗21");
    expect(screen.getByText("部分完成")).toBeTruthy();
    expect(screen.queryByText(/這批來源審核已完成/)).toBeNull();
    expect(screen.getAllByText("Gemini 回應的項目識別碼與這批候選不符。")).toHaveLength(21);
    expect(screen.queryByText("Gemini未回傳這筆候選")).toBeNull();
    expect((screen.getByRole("button", { name: "繼續未完成工作" }) as HTMLButtonElement).disabled).toBe(false);
    const discovery = screen.getByRole("button", { name: "開始尋找 40 筆候選" });
    expect((discovery as HTMLButtonElement).disabled).toBe(true);
    fireEvent.click(discovery);
    for (const action of ["approve", "reject", "keep_pending"]) {
      fireEvent.change(screen.getByRole("combobox", { name: "批次動作" }), { target: { value: action } });
      for (const checkbox of screen.getAllByRole("checkbox")) expect((checkbox as HTMLInputElement).disabled).toBe(true);
      expect((screen.getByRole("button", { name: "選取本頁可操作項目（0）" }) as HTMLButtonElement).disabled).toBe(true);
      expect((screen.getByRole("button", { name: "預覽選取的 0 筆" }) as HTMLButtonElement).disabled).toBe(true);
    }
    expect(screen.queryByRole("dialog")).toBeNull();
    expect(fetchMock.mock.calls.filter(([, init]) => init?.method === "POST")).toHaveLength(0);
  });

  it("resumes missing assessments once using the original run instead of creating another batch", async () => {
    let current = { ...run, status: "partial", can_resume: true, review_complete: false, counts: { ...run.counts, total: 307, assessed: 286, failed: 21 } };
    const fetchMock = mockApi((url, init) => {
      if (url === root) return response({ ...overview, can_start_discovery: false, runs: [current] });
      if (url === root + "/runs/review-1") return response(current);
      if (url === root + "/runs/review-1/resume" && init?.method === "POST") {
        current = { ...current, status: "queued", can_resume: false };
        return response(current, 202);
      }
      return undefined;
    });
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    fireEvent.click(await screen.findByRole("button", { name: "繼續未完成工作" }));
    await waitFor(() => expect(screen.queryByRole("button", { name: "繼續未完成工作" })).toBeNull());
    expect((screen.getByRole("combobox", { name: "選擇審核工作" }) as HTMLSelectElement).value).toBe("review-1");
    expect(within(screen.getByRole("combobox", { name: "選擇審核工作" })).getByRole("option").textContent).toContain("排隊中");
    expect((screen.getByRole("button", { name: "開始尋找 40 筆候選" }) as HTMLButtonElement).disabled).toBe(true);
    const writes = fetchMock.mock.calls.filter(([, init]) => init?.method === "POST");
    expect(writes).toHaveLength(1);
    expect(String(writes[0][0])).toBe(root + "/runs/review-1/resume?scope=hotspots");
  });

  it("shows quota codes without a message and distinguishes created candidates from approval suggestions", async () => {
    const partial = { ...run, mode: "discover_new", status: "partial", review_complete: false, error_code: "gemini_daily_budget_exhausted", counts: { ...run.counts, created: 7, approved: 1 } };
    mockApi((url) => url === root + "/runs/review-1" ? response(partial) : undefined);
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    await screen.findByText("gemini_daily_budget_exhausted");
    expect(screen.getByText("部分完成")).toBeTruthy();
    expect(screen.getByText("已建立候選").parentElement?.textContent).toBe("已建立候選7");
    expect(screen.getByText("建議核准").parentElement?.textContent).toBe("建議核准1");
    expect(screen.getByText(/找到候選不等於已核准或已發布/)).toBeTruthy();
    expect(screen.queryByText(/^已發布/)).toBeNull();
    expect(screen.queryByRole("button", { name: "繼續未完成工作" })).toBeNull();
  });

  it("polls without overlap, stops at a terminal state, and refreshes capabilities", async () => {
    vi.useFakeTimers();
    let detailCalls = 0;
    let finishPoll: ((value: Response) => void) | undefined;
    const fetchMock = mockApi((url) => {
      if (url === root + "/runs/review-1") {
        detailCalls += 1;
        return detailCalls === 1 ? response({ ...run, status: "running" }) : new Promise<Response>((resolve) => { finishPoll = resolve; });
      }
      return undefined;
    });
    await act(async () => { render(<AdminCatalogReviewPanel scope="hotspots" />); });
    expect(detailCalls).toBe(1);
    await act(async () => { await vi.advanceTimersByTimeAsync(3_000); });
    expect(detailCalls).toBe(2);
    await act(async () => { await vi.advanceTimersByTimeAsync(9_000); });
    expect(detailCalls).toBe(2);
    await act(async () => { finishPoll!(new Response(JSON.stringify(run))); });
    await act(async () => { await vi.advanceTimersByTimeAsync(12_000); });
    expect(detailCalls).toBe(2);
    expect(fetchMock.mock.calls.filter(([url]) => String(url) === root + "?scope=hotspots")).toHaveLength(2);
  });

  it("updates history from queued through running to a resumable provider circuit stop", async () => {
    vi.useFakeTimers();
    let calls = 0;
    mockApi((url) => {
      if (url === root) return response({ ...overview, runs: [{ ...run, status: "queued" }] });
      if (url === root + "/runs/review-1") {
        calls += 1;
        return response({ ...run, status: calls === 1 ? "queued" : calls === 2 ? "running" : "partial", review_complete: false, can_resume: calls === 3, error_code: calls === 3 ? "catalog_review_provider_circuit_open" : null, error_message: calls === 3 ? "Safe server fallback message" : null });
      }
      return undefined;
    });
    await act(async () => { render(<AdminCatalogReviewPanel scope="hotspots" />); });
    const history = screen.getByRole("combobox", { name: "選擇審核工作" });
    expect(within(history).getByRole("option").textContent).toContain("排隊中");
    await act(async () => { await vi.advanceTimersByTimeAsync(3_000); });
    expect(within(history).getByRole("option").textContent).toContain("執行中");
    expect(within(history).getByRole("option").textContent).not.toContain("排隊中");
    await act(async () => { await vi.advanceTimersByTimeAsync(3_000); });
    expect(within(history).getByRole("option").textContent).toContain("部分完成");
    expect(screen.getByText("提供者連續回應異常，工作已安全停止並保留進度。請檢查服務設定後再續跑。")).toBeTruthy();
    expect(screen.queryByText("Safe server fallback message")).toBeNull();
    expect(screen.getByText("catalog_review_provider_circuit_open")).toBeTruthy();
    expect((screen.getByRole("button", { name: "繼續未完成工作" }) as HTMLButtonElement).disabled).toBe(false);
    await act(async () => { await vi.advanceTimersByTimeAsync(6_000); });
    expect(calls).toBe(3);
  });

  it("preserves a terminal partial result when refreshing overview fails", async () => {
    vi.useFakeTimers();
    let detailCalls = 0;
    let overviewCalls = 0;
    mockApi((url) => {
      if (url === root) {
        overviewCalls += 1;
        return overviewCalls === 1 ? response(overview) : response({ detail: "Overview unavailable." }, 503);
      }
      if (url === root + "/runs/review-1") {
        detailCalls += 1;
        return response({ ...run, status: detailCalls === 1 ? "running" : "partial", review_complete: false, error_code: detailCalls === 1 ? null : "gemini_daily_budget_exhausted" });
      }
      return undefined;
    });
    await act(async () => { render(<AdminCatalogReviewPanel scope="hotspots" />); });
    await act(async () => { await vi.advanceTimersByTimeAsync(3_000); });
    expect(screen.getByText("部分完成")).toBeTruthy();
    expect(screen.getByText("gemini_daily_budget_exhausted")).toBeTruthy();
    expect(screen.getByText("Overview unavailable.")).toBeTruthy();
    expect((screen.getByRole("button", { name: "開始審核現有待審" }) as HTMLButtonElement).disabled).toBe(true);
    expect((screen.getByRole("button", { name: "開始尋找 40 筆候選" }) as HTMLButtonElement).disabled).toBe(true);
    await act(async () => { await vi.advanceTimersByTimeAsync(12_000); });
    expect(detailCalls).toBe(2);
  });

  it("retries a transient polling failure and clears the reconnecting notice", async () => {
    vi.useFakeTimers();
    let detailCalls = 0;
    mockApi((url) => {
      if (url === root + "/runs/review-1") {
        detailCalls += 1;
        if (detailCalls === 2) return Promise.reject(new TypeError("Connection interrupted"));
        return response({ ...run, status: detailCalls === 1 ? "running" : "completed" });
      }
      return undefined;
    });
    await act(async () => { render(<AdminCatalogReviewPanel scope="hotspots" />); });
    await act(async () => { await vi.advanceTimersByTimeAsync(3_000); });
    expect(screen.getByText(/連線暫時中斷/)).toBeTruthy();
    await act(async () => { await vi.advanceTimersByTimeAsync(3_000); });
    expect(screen.queryByText(/連線暫時中斷/)).toBeNull();
    expect(detailCalls).toBe(3);
    await act(async () => { await vi.advanceTimersByTimeAsync(6_000); });
    expect(detailCalls).toBe(3);
  });

  it("aborts the old run poll and ignores its late response after switching history", async () => {
    vi.useFakeTimers();
    let detailCalls = 0;
    let pollSignal: AbortSignal | undefined;
    let finishOldPoll: ((value: Response) => void) | undefined;
    const fetchMock = mockApi((url, init) => {
      if (url === root) return response({ ...overview, runs: [run, { ...run, id: "review-2" }] });
      if (url === root + "/runs/review-1") {
        detailCalls += 1;
        if (detailCalls === 1) return response({ ...run, status: "running" });
        pollSignal = init?.signal as AbortSignal;
        return new Promise<Response>((resolve) => { finishOldPoll = resolve; });
      }
      if (url === root + "/runs/review-2") return response({ ...run, id: "review-2", model: "selected-run-model" });
      return undefined;
    });
    await act(async () => { render(<AdminCatalogReviewPanel scope="hotspots" />); });
    await act(async () => { await vi.advanceTimersByTimeAsync(3_000); });
    await act(async () => { fireEvent.change(screen.getByRole("combobox", { name: "選擇審核工作" }), { target: { value: "review-2" } }); });
    expect(pollSignal?.aborted).toBe(true);
    await act(async () => { finishOldPoll!(new Response(JSON.stringify({ ...run, model: "obsolete-run-model" }))); });
    expect(screen.getByText(/Gemini · 模型 selected-run-model/)).toBeTruthy();
    expect(screen.queryByText(/obsolete-run-model/)).toBeNull();
    expect(fetchMock.mock.calls.filter(([url]) => String(url).includes("/runs/review-1/items?"))).toHaveLength(1);
    await act(async () => { await vi.advanceTimersByTimeAsync(6_000); });
    expect(detailCalls).toBe(2);
  });

  it("aborts an in-flight poll when the page unmounts", async () => {
    vi.useFakeTimers();
    let detailCalls = 0;
    let pollSignal: AbortSignal | undefined;
    mockApi((url, init) => {
      if (url === root + "/runs/review-1") {
        detailCalls += 1;
        if (detailCalls === 1) return response({ ...run, status: "running" });
        pollSignal = init?.signal as AbortSignal;
        return new Promise<Response>(() => undefined);
      }
      return undefined;
    });
    let view: ReturnType<typeof render>;
    await act(async () => { view = render(<AdminCatalogReviewPanel scope="hotspots" />); });
    await act(async () => { await vi.advanceTimersByTimeAsync(3_000); });
    expect(pollSignal?.aborted).toBe(false);
    view!.unmount();
    expect(pollSignal?.aborted).toBe(true);
  });

  it("aborts an in-flight apply on unmount without reloading after a late response", async () => {
    let applySignal: AbortSignal | undefined;
    let finishApply: ((value: Response) => void) | undefined;
    const fetchMock = mockApi((url, init) => {
      if (url.includes("/items?")) return response(listing([candidate("one", "Unmount candidate")]));
      if (url.endsWith("/apply")) {
        applySignal = init?.signal as AbortSignal;
        return new Promise<Response>((resolve) => { finishApply = resolve; });
      }
      return undefined;
    });
    const view = render(<AdminCatalogReviewPanel scope="hotspots" />);
    await screen.findByText("Unmount candidate");
    fireEvent.click(screen.getByRole("checkbox", { name: "選取 Unmount candidate" }));
    fireEvent.click(screen.getByRole("button", { name: "預覽選取的 1 筆" }));
    fireEvent.click(screen.getByRole("button", { name: "確認並套用" }));
    expect(applySignal?.aborted).toBe(false);
    const requestsBeforeUnmount = fetchMock.mock.calls.length;
    view.unmount();
    expect(applySignal?.aborted).toBe(true);
    await act(async () => { finishApply!(new Response(JSON.stringify({ run, outcomes: [], updated: 1 }))); });
    expect(fetchMock.mock.calls).toHaveLength(requestsBeforeUnmount);
  });

  it("shows the merchant enrichment step only in the foods workspace and starts it with the enrich_merchants mode", async () => {
    const foodRun = { ...run, scope: "foods" };
    const fetchMock = mockApi((url, init) => {
      if (url === root) return response({ ...overview, pending_counts: { hotspot: 0, food: 20, merchant: 49, total: 69 }, can_start_enrichment: true, runs: [foodRun] });
      if (url === root + "/runs/review-1") return response(foodRun);
      if (url === root + "/runs" && init?.method === "POST") return response({ ...foodRun, mode: "enrich_merchants", phase: "identify", status: "queued" });
      return undefined;
    });
    render(<AdminCatalogReviewPanel scope="foods" />);
    const start = await screen.findByRole("button", { name: "補齊店家資料" });
    await waitFor(() => expect((start as HTMLButtonElement).disabled).toBe(false));
    expect(screen.getByText("待審店家 49 筆")).toBeTruthy();
    fireEvent.click(start);
    await waitFor(() => expect(fetchMock.mock.calls.some(([, init]) => init?.method === "POST")).toBe(true));
    const init = fetchMock.mock.calls.find(([, init]) => init?.method === "POST")![1]!;
    expect(JSON.parse(String(init.body))).toEqual({ mode: "enrich_merchants", scope: "foods", max_calls: 80 });
  });

  it("keeps enrichment outside the foods workspace and disabled when the server does not allow it", async () => {
    mockApi((url) => url === root ? response({ ...overview, can_start_enrichment: true }) : undefined);
    render(<AdminCatalogReviewPanel scope="hotspots" />);
    await screen.findByText("gemini-review-model", { exact: false });
    expect(screen.queryByRole("button", { name: "補齊店家資料" })).toBeNull();
    cleanup();
    const fetchMock = mockApi((url) => url === root ? response({ ...overview, runs: [{ ...run, scope: "foods" }] }) : undefined);
    render(<AdminCatalogReviewPanel scope="foods" />);
    const start = await screen.findByRole("button", { name: "補齊店家資料" });
    expect((start as HTMLButtonElement).disabled).toBe(true);
    fireEvent.click(start);
    expect(fetchMock.mock.calls.filter(([, init]) => init?.method === "POST")).toHaveLength(0);
  });

  it("renders verified corrections and applies them only through apply_corrections with a confirmation", async () => {
    const enrichRun = {
      ...run, id: "enrich-1", scope: "foods", mode: "enrich_merchants", phase: "enrich_merchants",
      counts: { ...run.counts, total: 2, assessed: 2, approved: 0, needs_review: 2 },
      enrichment: { items_with_corrections: 1, corrections: 2 },
    };
    const site = "https://sushi-dai.example/tsukiji";
    const enriched = {
      ...candidate("one", "Sushi Dai"), kind: "merchant", phase: "enrich_merchants", decision: "needs_review", reason: "找到官網。",
      evidence: [{ url: site, quote: "寿司大 東京都中央区築地5-2-1" }], allowed_actions: ["apply_corrections", "keep_pending"], confidence: 0.8,
      corrections: [
        { field: "address", value: "東京都中央区築地5-2-1", source_url: site, quote: "寿司大 東京都中央区築地5-2-1", kind: "address" },
        { field: "official_website_url", value: site, source_url: "javascript:alert(1)", quote: "寿司大", kind: "merchant_website" },
      ],
      identify: { matched_in_run: true, place_id: "ChIJx", skipped: null },
    };
    const empty = {
      ...candidate("two", "No pages"), kind: "merchant", phase: "enrich_merchants", decision: "needs_review", reason: "搜尋未找到可獨立核對的官網或觀光局頁面。",
      evidence: [], allowed_actions: ["keep_pending"], confidence: 0, corrections: [], identify: { matched_in_run: false, place_id: null, skipped: "kr" },
    };
    const fetchMock = mockApi((url, init) => {
      if (url === root) return response({ ...overview, can_start_enrichment: false, runs: [enrichRun] });
      if (url === root + "/runs/enrich-1") return response(enrichRun);
      if (url.includes("/items?")) return response(listing([enriched, empty]));
      if (url.endsWith("/apply") && init?.method === "POST") return response({ run: { ...enrichRun, version: 4 }, updated: 1, outcomes: [{ id: "one", action: "apply_corrections", status: "applied", reason: "找到官網。", changes: { address: "東京都中央区築地5-2-1", official_website_url: site }, skipped_fields: {} }] });
      return undefined;
    });
    render(<AdminCatalogReviewPanel scope="foods" />);
    expect(await screen.findByText("Sushi Dai")).toBeTruthy();
    const corrections = screen.getByRole("list", { name: "Sushi Dai 的建議補齊" });
    expect(within(corrections).getByText("店家官網 · 官網網址")).toBeTruthy();
    expect(within(corrections).getByText("東京都中央区築地5-2-1")).toBeTruthy();
    expect(within(corrections).getByRole("link", { name: site }).getAttribute("href")).toBe(site);
    expect(within(corrections).getByText("來源網址無法安全開啟")).toBeTruthy();
    expect(screen.getByText("本次已配對 Google 分店身分")).toBeTruthy();
    expect(screen.getAllByText("補齊店家欄位 · 已評估")).toHaveLength(2);
    expect(screen.queryByRole("list", { name: "No pages 的建議補齊" })).toBeNull();
    const select = screen.getByLabelText("批次動作") as HTMLSelectElement;
    expect(Array.from(select.options).map((option) => option.textContent)).toEqual(["套用補齊資料", "保留待審"]);
    expect(select.value).toBe("apply_corrections");
    expect((screen.getByRole("checkbox", { name: "選取 No pages" }) as HTMLInputElement).disabled).toBe(true);
    fireEvent.click(screen.getByRole("button", { name: "選取本頁可操作項目（1）" }));
    fireEvent.click(screen.getByRole("button", { name: "預覽選取的 1 筆" }));
    const dialog = screen.getByRole("dialog", { name: "確認套用補齊資料 1 筆" });
    expect(within(dialog).getByText(/只會填入目前為空的欄位/)).toBeTruthy();
    expect(within(dialog).getByText("地址: 東京都中央区築地5-2-1")).toBeTruthy();
    expect(within(dialog).queryByText("找到官網。")).toBeNull();
    fireEvent.click(within(dialog).getByRole("button", { name: "確認並套用" }));
    expect(await screen.findByText("實際更新 1 筆")).toBeTruthy();
    expect(screen.getByText("已填入：地址, 官網網址")).toBeTruthy();
    const init = fetchMock.mock.calls.find(([input]) => String(input).endsWith("/apply?scope=foods"))![1]!;
    expect(JSON.parse(String(init.body))).toEqual({ item_ids: ["one"], action: "apply_corrections", expected_version: 3 });
  });
});
