import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { AdminNewsModelSettings } from "./admin-news-model-settings";
import { AdminNewsWorkspace } from "./admin-news-workspace";
import { adminNewsCopy } from "@/lib/admin-news-copy";
import { newsLocales } from "@/lib/admin-news";
import { siteUrl } from "@/lib/seo";

// The locale the page is read in; a test of the English copy switches it.
const site = vi.hoisted(() => ({ locale: "zh-TW" }));
vi.mock("next-intl", () => ({ useLocale: () => site.locale }));
vi.mock("@/i18n/navigation", () => ({
  Link: ({ href, children, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement> & { href: string }) => <a href={href} {...props}>{children}</a>,
  useRouter: () => ({ replace: vi.fn() }),
}));

type Row = Record<string, unknown> & { id: string; source_title: string };

const summary: Row = {
  id: "00000000-0000-4000-8000-000000000001", vertical: "ai", status: "manual_review",
  source_title: "Official AI API update", canonical_url: "https://example.com/news",
  event_date: "2026-09-23", would_publish: false, human_decision: null, error_code: "news_jev_manual",
  error_detail: "At least one locale was not approved by Jev.", guide_article_id: "00000000-0000-4000-8000-000000000002",
  created_at: "2026-09-23T10:00:00Z", updated_at: "2026-09-23T11:00:00Z",
};
const document = {
  title: "API 更新如何影響一般使用者", description: "已查核的五語新聞。", hero: null,
  blocks: [{ type: "paragraph", text: "這是完整文章內容。" }],
  sources: [{ title: "Official", url: "https://example.com/release", checked_on: "2026-09-23" }],
};
function detailOf(row: Row) {
  return {
    ...row,
    evidence: [{ id: "e1", role: "evidence", is_first_party: true, url: "https://example.com/release", title: "Official release", retrieved_at: "2026-09-23T10:00:00Z", source_date: "2026-09-23", content_hash: "a".repeat(64), excerpt: "Verified evidence excerpt." }],
    assessments: [{ id: "a1", assessment_type: "jev", locale: "en", verdict: "manual", confidence: 0.75, provider: "jev", model: "jev", reasons: ["quota_unavailable"], details: { tier: "confirm" }, created_at: "2026-09-23T11:00:00Z" }],
    runs: [{ id: "r1", stage: "jev", status: "succeeded", attempt: 1, provider: "jev", model: "jev", input_tokens: 20, output_tokens: 0, error_code: null, error_detail: null, metadata: {}, started_at: "2026-09-23T11:00:00Z", finished_at: "2026-09-23T11:00:01Z" }],
    documents: row.guide_article_id ? Object.fromEntries(["zh-TW", "zh-CN", "en", "ja", "ko"].map((locale) => [locale, { ...document, title: `${document.title} ${locale}` }])) : {},
    claim_ledger: [], lint: {}, human_reason: null, human_major_error: false, similar_titles: [] as string[],
    article_slug: null as string | null, article_kind: null as "life" | null,
  };
}
const settings = {
  enabled: false, mode: "shadow", writer_provider: "openai", writer_model: null,
  verifier_provider: "openai", verifier_model: null, editor_provider: "anthropic",
  editor_model: "claude-next", judge_enabled: false, judge_provider: "anthropic", judge_model: null,
  global_concurrency: 2,
  per_vertical_concurrency: 1, min_shadow_days: 14, min_shadow_candidates: 50,
  min_human_agreement: 0.95, jev_act_confidence: 0.9, auto_publish_ai: false,
  auto_publish_tech: false, auto_publish_crypto: false, prompt_version: "news-v1",
  policy_version: "news-policy-v1", updated_at: "2026-09-23T10:00:00Z",
  gates: Object.fromEntries(["ai", "tech", "crypto"].map((vertical) => [vertical, { vertical, days: 0, labelled_candidates: 3, agreements: 2, agreement_rate: 0.6667, serious_false_positives: 0, eligible: false, reasons: ["shadow_days:0/14"] }])),
  model_options: {
    openai: [
      { value: "gpt-6-astra", label: "GPT-6 Astra", description: "Strongest.", status: "stable" },
      { value: "gpt-5.6-terra", label: "GPT-5.6 Terra", description: "Balanced default.", status: "stable" },
    ],
    anthropic: [
      { value: "claude-sonnet-5", label: "Claude Sonnet 5", description: null, status: "stable" },
      { value: "claude-next", label: "Claude Next", description: null, status: "preview" },
    ],
    minimax: [], gemini: [],
  },
  default_models: { openai: "gpt-5.6-terra", anthropic: "claude-sonnet-5", minimax: "MiniMax-M3", gemini: "gemini-3.8-flash" },
};
// The answer of a server from before the review judge: the same settings without its fields.
const settingsBeforeJudge = Object.fromEntries(Object.entries(settings).filter(([key]) => !key.startsWith("judge_")));

// What the stubbed API answers; tests replace rows, details, paging or settings before rendering.
let rows: Row[] = [];
let details: Record<string, ReturnType<typeof detailOf>> = {};
let pages = 1;
let sourceRows: Record<string, unknown>[] = [];
let statsExtra: Record<string, unknown> = {};
let settingsAnswer: Record<string, unknown> = settings;

function serveRows(...next: Row[]) {
  rows = next;
  details = Object.fromEntries(next.map((row) => [row.id, detailOf(row)]));
}

// One verdict of the AI judge, as the detail lists it among the assessments. `extra` carries
// the optional details keys, such as the refusal that turned a publish into a hand-back.
function judgeRow(id: string, verdict: string, stage: string, hold: string, reasons: string[], extra: Record<string, unknown> = {}) {
  return {
    id, assessment_type: "judge", locale: null, verdict, confidence: null, provider: "anthropic", model: "claude-opus-5-5",
    reasons, details: { stage, hold, ...extra }, created_at: "2026-10-06T01:00:00Z",
  };
}
function withAssessments(row: Row, ...assessments: ReturnType<typeof judgeRow>[]) {
  details[row.id] = { ...detailOf(row), assessments: assessments as unknown as ReturnType<typeof detailOf>["assessments"] };
}

beforeEach(() => {
  window.history.replaceState(null, "", "/zh-TW/admin/news?tab=review");
  site.locale = "zh-TW";
  serveRows(summary);
  pages = 1;
  sourceRows = [];
  statsExtra = {};
  settingsAnswer = settings;
  vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    const action = url.match(/\/admin\/news\/candidates\/([0-9a-f-]{36})\/([a-z-]+)$/);
    if (action && init?.method === "POST") {
      const status = action[2] === "reject" ? "rejected" : action[2] === "publish" ? "published" : "discovered";
      return Response.json({ ...details[action[1]], status });
    }
    const one = url.match(/\/admin\/news\/candidates\/([0-9a-f-]{36})$/);
    if (one) return Response.json(details[one[1]]);
    if (url.includes("/admin/news/candidates?")) return Response.json({ candidates: rows, total: rows.length * pages, page: 1, pages });
    if (url.endsWith("/admin/news/sources")) return Response.json(sourceRows);
    if (url.endsWith("/admin/news/settings/models") && init?.method === "PUT") return Response.json({ ...settingsAnswer, ...JSON.parse(String(init.body)) });
    if (url.endsWith("/admin/news/settings")) return Response.json(init?.method === "PUT" ? { ...settingsAnswer, ...JSON.parse(String(init.body)) } : settingsAnswer);
    if (url.endsWith("/admin/news/stats")) return Response.json({ pending_review: 1, failed: 0, published: 3, queue_by_status: { manual_review: 1, needs_redraft: 2, failed: 1 }, pipeline_runs: 4, pipeline_failures: 1, input_tokens: 10, output_tokens: 5, ...statsExtra });
    return Response.json({ detail: "not found" }, { status: 404 });
  }));
});
afterEach(() => vi.unstubAllGlobals());

const posts = () => vi.mocked(fetch).mock.calls.filter(([, init]) => init?.method === "POST").map(([url]) => String(url));
const listCalls = () => vi.mocked(fetch).mock.calls.map(([url]) => String(url)).filter((url) => url.includes("/admin/news/candidates?"));
const actionButtons = () => ["確認發布，翻譯其他語言", "重新翻譯並發布", "五語發布", "重新查核", "不是重複，繼續寫", "用最新來源重新查核", "重新執行", "退件", "回報發布後重大錯誤", "拿回來自己判斷"]
  .filter((name) => screen.queryByRole("button", { name }));

describe("AdminNewsWorkspace", () => {
  it("lists a source that keeps failing on its recent articles first, with a warning", async () => {
    const source = (id: string, name: string, lastStatus: string, lastError: string | null) => ({
      id, name, url: `https://${id}.example/feed`, format: "rss", role: "evidence", vertical: "ai",
      is_first_party: true, enabled: true, scan_interval_minutes: 60, allowed_redirect_hosts: [], config: {},
      etag: null, last_modified: null, last_scanned_at: "2026-09-30T10:00:00Z", next_scan_at: "2026-09-30T11:00:00Z",
      last_status: lastStatus, last_error: lastError, consecutive_failures: 0,
      created_at: "2026-09-01T00:00:00Z", updated_at: "2026-09-30T10:00:00Z",
    });
    sourceRows = [
      source("fine", "Fine source", "partial", "Skipped 1 page(s): https://fine.example/a (ConnectTimeout)"),
      source("stuck", "Stuck source", "stuck", "Failing for more than 6 hours: https://stuck.example/b. Skipped 1 page(s)"),
    ];
    window.history.replaceState(null, "", "/zh-TW/admin/news?tab=sources");
    render(<AdminNewsWorkspace />);
    expect(await screen.findByRole("alert")).toBeTruthy();
    expect(screen.getByText(/1 個來源最近的文章已連續抓不到超過 6 小時/)).toBeTruthy();
    const names = screen.getAllByRole("heading", { level: 3 }).map((heading) => heading.textContent);
    expect(names.indexOf("Stuck source")).toBeLessThan(names.indexOf("Fine source"));
  });

  it("explains a Jev hold in Chinese and publishes it with an audited reason", async () => {
    render(<AdminNewsWorkspace />);
    expect(await screen.findByRole("heading", { name: "AI 每小時自動新聞" })).toBeTruthy();
    fireEvent.click(await screen.findByRole("button", { name: /Official AI API update/ }));
    expect(await screen.findByText(/Official release/)).toBeTruthy();
    expect(screen.getAllByText("待你判斷").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Jev 保留：有語系沒通過").length).toBeGreaterThan(0);
    expect(screen.getByText(/五語草稿已經寫好，但 Jev 對至少一個語系有保留/)).toBeTruthy();
    expect(screen.getByText("AI 和 Jev 的一致率（參考）：你判斷過 3 筆，一致 67%")).toBeTruthy();
    expect(screen.getByText("Jev 終審: 需要人判斷 (需人確認)")).toBeTruthy();
    expect(screen.getByText("Jev 今日額度已用完")).toBeTruthy();
    expect(screen.getAllByRole("button").filter((button) => ["zh-TW", "zh-CN", "en", "ja", "ko"].includes(button.textContent || ""))).toHaveLength(5);
    expect(screen.getByRole("link", { name: /開啟文章編輯器 · zh-TW/ }).getAttribute("href")).toContain(`article=${String(summary.guide_article_id)}`);
    expect(actionButtons()).toEqual(["五語發布", "重新查核", "退件"]);
    expect((screen.getByRole("button", { name: "五語發布" }) as HTMLButtonElement).disabled).toBe(true);
    expect(screen.getByText("先選或填寫原因，按鈕才能按。")).toBeTruthy();

    fireEvent.click(screen.getByRole("button", { name: "內容正確，可以發布" }));
    expect((screen.getByLabelText(/原因（必填/) as HTMLTextAreaElement).value).toBe("內容正確，可以發布");
    fireEvent.click(screen.getByRole("button", { name: "五語發布" }));
    await waitFor(() => expect(fetch).toHaveBeenCalledWith(
      `/api/travel/admin/news/candidates/${summary.id}/publish`,
      expect.objectContaining({ method: "POST" }),
    ));
    expect(await screen.findByText("五個語系都已發布。")).toBeTruthy();
  });

  it("shows what Jev's last call held and still lets the owner publish the saved article", async () => {
    const held = { ...summary, id: "00000000-0000-4000-8000-000000000021", source_title: "A held release", error_code: "news_jev_final_hold", human_decision: "publish" };
    serveRows(held);
    details[held.id] = {
      ...detailOf(held),
      assessments: [
        { id: "f1", assessment_type: "locale_review", locale: "ja", verdict: "pass", confidence: null, provider: "anthropic", model: "claude-opus-5-5", reasons: [], details: { stage: "final_edit", revised: true }, created_at: "2026-09-23T11:00:00Z" },
        { id: "f2", assessment_type: "jev", locale: "ja", verdict: "manual", confidence: 0.8, provider: "jev", model: "jev", reasons: [], details: { tier: "confirm", stage: "final" }, created_at: "2026-09-23T11:01:00Z" },
      ] as unknown as ReturnType<typeof detailOf>["assessments"],
    };
    render(<AdminNewsWorkspace />);
    fireEvent.click(await screen.findByRole("button", { name: /A held release/ }));
    expect((await screen.findAllByText("Jev 最後一關保留")).length).toBeGreaterThan(0);
    expect(screen.getByText(/Jev 最後一關對至少一個語系沒有放行/)).toBeTruthy();
    expect(screen.getByText("翻譯審查・最終修改: 通過")).toBeTruthy();
    expect(screen.getByText("Jev 終審・最後一關: 需要人判斷 (需人確認)")).toBeTruthy();
    expect(actionButtons()).toEqual(["五語發布", "重新查核", "退件"]);
  });

  it("lets auto-publish be switched on in automatic mode without a gate", async () => {
    window.history.replaceState(null, "", "/zh-TW/admin/news?tab=settings");
    render(<AdminNewsWorkspace />);
    const [aiSwitch] = await screen.findAllByRole("checkbox", { name: "自動發布" }) as HTMLInputElement[];
    expect(aiSwitch.disabled).toBe(true);
    expect(screen.getByText(/自動發布不再看這些數字/)).toBeTruthy();
    expect(screen.queryByText("未達標")).toBeNull();
    expect(screen.queryByText("shadow_days:0/14")).toBeNull();
    fireEvent.change(screen.getByLabelText("模式"), { target: { value: "automatic" } });
    expect(aiSwitch.disabled).toBe(false);
  });

  it("offers not-a-duplicate with the closest titles for an uncertain duplicate check", async () => {
    const waiting = { ...summary, id: "00000000-0000-4000-8000-000000000011", source_title: "OpenAI ships a model", error_code: "news_duplicate_uncertain", guide_article_id: null };
    serveRows(waiting);
    details[waiting.id] = { ...detailOf(waiting), similar_titles: ["OpenAI ships a new model", "A weather satellite"] };
    render(<AdminNewsWorkspace />);
    fireEvent.click(await screen.findByRole("button", { name: /OpenAI ships a model/ }));
    expect(await screen.findByText("最像的既有標題")).toBeTruthy();
    expect(screen.getByText("OpenAI ships a new model")).toBeTruthy();
    expect(actionButtons()).toEqual(["不是重複，繼續寫", "退件"]);
    fireEvent.change(screen.getByLabelText(/原因（必填/), { target: { value: "不同的發布" } });
    fireEvent.click(screen.getByRole("button", { name: "不是重複，繼續寫" }));
    await waitFor(() => expect(posts()).toEqual([`/api/travel/admin/news/candidates/${waiting.id}/not-duplicate`]));
    expect(await screen.findByText(/已記下「不是重複」/)).toBeTruthy();
  });

  it("re-checks a story whose sources changed against the current pages", async () => {
    const changed = { ...summary, id: "00000000-0000-4000-8000-000000000031", source_title: "A changed page", error_code: "news_evidence_changed" };
    serveRows(changed);
    render(<AdminNewsWorkspace />);
    fireEvent.click(await screen.findByRole("button", { name: /A changed page/ }));
    expect(await screen.findByText(/來源頁的內容更新了/)).toBeTruthy();
    fireEvent.change(screen.getByLabelText(/原因（必填/), { target: { value: "報導補了新內容" } });
    fireEvent.click(screen.getByRole("button", { name: "用最新來源重新查核" }));
    await waitFor(() => expect(posts()).toEqual([`/api/travel/admin/news/candidates/${changed.id}/refresh-evidence`]));
    expect(await screen.findByText(/已抓取最新來源並排入重新查核/)).toBeTruthy();
  });

  it.each([
    ["published", true],
    ["manual_review", false],
    ["rejected", false],
  ])("links a %s candidate's saved article to its public page: %s", async (status, live) => {
    const slug = "ai-news-api-update-20260923";
    const row = { ...summary, status, error_code: null, error_detail: null, human_decision: null };
    serveRows(row);
    details[row.id] = { ...detailOf(row), article_slug: slug, article_kind: "life" };
    render(<AdminNewsWorkspace />);
    fireEvent.click(await screen.findByRole("button", { name: /Official AI API update/ }));
    await screen.findByText(/Official release/);
    expect(screen.getAllByRole("link", { name: /開啟文章編輯器/ })).toHaveLength(5);
    const links = screen.queryAllByRole("link", { name: /開啟前台文章/ });
    expect(links.map((link) => link.getAttribute("href")))
      .toEqual(live ? newsLocales.map((locale) => `${siteUrl}/${locale}/life/${slug}`) : []);
    for (const link of links) {
      expect(link.getAttribute("target")).toBe("_blank");
      expect(link.getAttribute("rel")).toContain("noopener");
    }
  });

  it.each([
    ["needs_redraft", "news_verification_failed", null, ["重新執行", "退件"]],
    ["failed", "ValidationError", null, ["重新執行", "退件"]],
    ["failed", "news_processing_stale", "00000000-0000-4000-8000-000000000002", ["重新查核", "重新執行", "退件"]],
    ["needs_evidence", "news_evidence_insufficient", null, ["退件"]],
    ["manual_review", "news_evidence_changed", "00000000-0000-4000-8000-000000000002", ["用最新來源重新查核", "退件"]],
    ["manual_review", "news_verification_failed", "00000000-0000-4000-8000-000000000002", ["重新查核", "退件"]],
    ["manual_review", "news_hard_checks_failed", "00000000-0000-4000-8000-000000000002", ["重新查核", "退件"]],
    ["manual_review", "news_hard_checks_failed", null, ["重新執行", "退件"]],
    ["published", null, "00000000-0000-4000-8000-000000000002", ["回報發布後重大錯誤"]],
    ["rejected", null, null, []],
    ["manual_review", "news_zh_draft_ready", null, ["確認發布，翻譯其他語言", "重新執行", "退件"]],
    ["manual_review", "news_ready_to_publish", "00000000-0000-4000-8000-000000000002", ["五語發布", "重新查核", "退件"]],
  ])("shows only the buttons that work for %s / %s", async (status, errorCode, articleId, expected) => {
    const row = { ...summary, status, error_code: errorCode, guide_article_id: articleId, human_decision: null };
    serveRows(row);
    render(<AdminNewsWorkspace />);
    fireEvent.click(await screen.findByRole("button", { name: /Official AI API update/ }));
    await screen.findByText(/Official release/);
    expect(actionButtons().sort()).toEqual([...expected].sort());
  });

  it.each([
    ["manual_review", "news_locale_review_failed", null, ["重新翻譯並發布", "退件"]],
    ["failed", "ValidationError", null, ["重新翻譯並發布", "重新執行", "退件"]],
    ["manual_review", "news_hard_checks_failed", "00000000-0000-4000-8000-000000000002", ["重新翻譯並發布", "重新查核", "退件"]],
    ["manual_review", "news_hard_checks_failed", null, ["重新翻譯並發布", "退件"]],
  ])("offers to translate again once publication is confirmed (%s / %s / %s)", async (status, errorCode, articleId, expected) => {
    serveRows({ ...summary, status, error_code: errorCode, guide_article_id: articleId, human_decision: "publish" });
    render(<AdminNewsWorkspace />);
    fireEvent.click(await screen.findByRole("button", { name: /Official AI API update/ }));
    await screen.findByText(/Official release/);
    expect(actionButtons().sort()).toEqual([...expected].sort());
  });

  it.each([
    ["rejected", "reject", null, ["拿回來自己判斷"]],
    ["duplicate", "duplicate", null, ["拿回來自己判斷"]],
    // A person closed these, so the API would refuse to reopen them.
    ["rejected", "reject", "reject", []],
    ["rejected", "manual", "reject", []],
    ["rejected", null, "reject", []],
    ["duplicate", null, null, []],
    // Handed back, not closed: the hold's own buttons and nothing to take back.
    ["manual_review", "manual", null, ["五語發布", "重新查核", "退件"]],
    ["needs_redraft", "manual", null, ["重新執行", "退件"]],
  ])("offers to take a story back only when the AI judge closed it (%s / judge %s / owner %s)", async (status, judgeDecision, humanDecision, expected) => {
    serveRows({ ...summary, status, judge_decision: judgeDecision, human_decision: humanDecision });
    render(<AdminNewsWorkspace />);
    fireEvent.click(await screen.findByRole("button", { name: /Official AI API update/ }));
    await screen.findByText(/Official release/);
    expect(actionButtons().sort()).toEqual([...expected].sort());
  });

  it("shows the AI judge's verdict and reasons on a story it handed back", async () => {
    const handed = { ...summary, id: "00000000-0000-4000-8000-000000000041", source_title: "A handed-back draft", error_code: "news_zh_draft_ready", guide_article_id: null, judge_decision: "manual" };
    serveRows(handed);
    withAssessments(handed,
      judgeRow("j0", "pass", "duplicate", "news_duplicate_uncertain", ["和列出的報導不是同一件事"]),
      judgeRow("j1", "manual", "zh_draft", "news_zh_draft_ready", ["第二段的數字在來源裡找不到", "標題說得比來源更滿"]),
    );
    render(<AdminNewsWorkspace />);
    fireEvent.click(await screen.findByRole("button", { name: /A handed-back draft/ }));
    const verdict = await screen.findByRole("heading", { name: "AI 代審（claude-opus-5-5）：需要人判斷" });
    expect(within(verdict.parentElement!).getAllByRole("listitem").map((item) => item.textContent))
      .toEqual(["第二段的數字在來源裡找不到", "標題說得比來源更滿"]);
    expect(screen.getAllByRole("heading", { name: /AI 代審（/ })).toHaveLength(1);
    expect(screen.getByText("AI 代審・繁中草稿: 需要人判斷")).toBeTruthy();
    expect(screen.getByText("AI 代審・重複判斷: 通過")).toBeTruthy();
    expect(actionButtons()).toEqual(["確認發布，翻譯其他語言", "重新執行", "退件"]);
  });

  it("shows the AI judge's verdict on a story whose publication was refused because the sources changed", async () => {
    // The judge read Jev's last-call hold and answered publish; the refusal moved the row to
    // the changed-evidence hold, and the verdict keeps the hold it read plus the refusal.
    const moved = { ...summary, id: "00000000-0000-4000-8000-000000000043", source_title: "A story whose sources moved", error_code: "news_evidence_changed", judge_decision: "manual" };
    serveRows(moved);
    withAssessments(moved, judgeRow("j1", "manual", "final", "news_jev_final_hold",
      ["AI 的判斷是發布，但來源內容在查核之後變動了，請先重新查核來源。", "各語言與來源一致"],
      { downgraded_from: "publish", failure: "news_evidence_changed" }));
    render(<AdminNewsWorkspace />);
    fireEvent.click(await screen.findByRole("button", { name: /A story whose sources moved/ }));
    const verdict = await screen.findByRole("heading", { name: "AI 代審（claude-opus-5-5）：需要人判斷" });
    expect(within(verdict.parentElement!).getAllByRole("listitem").map((item) => item.textContent))
      .toEqual(["AI 的判斷是發布，但來源內容在查核之後變動了，請先重新查核來源。", "各語言與來源一致"]);
    expect(screen.getByText(/來源頁的內容更新了/)).toBeTruthy();
    expect(actionButtons()).toEqual(["用最新來源重新查核", "退件"]);
  });

  it.each([
    {
      why: "the story ran again and has not been judged since",
      state: { status: "needs_redraft", error_code: "news_verification_failed", judge_decision: null },
      judged: judgeRow("j1", "revise", "redraft", "news_verification_failed", ["把第三段的推測刪掉"]),
      label: "AI 代審・需重寫: 修改後再審",
    },
    {
      why: "the owner sent it on and it left the hold the verdict answered",
      state: { status: "discovered", error_code: "news_reverify_requested", judge_decision: "manual" },
      judged: judgeRow("j1", "manual", "zh_draft", "news_zh_draft_ready", ["標題說得比來源更滿"]),
      label: "AI 代審・繁中草稿: 需要人判斷",
    },
    {
      why: "the owner's own publish met changed sources on a hold the AI had handed back",
      state: { status: "manual_review", error_code: "news_evidence_changed", judge_decision: "manual" },
      judged: judgeRow("j1", "manual", "final", "news_jev_final_hold", ["日文版第二段和來源不符"]),
      label: "AI 代審・最後一關: 需要人判斷",
    },
  ])("leaves an AI verdict to the assessments table when $why", async ({ state, judged, label }) => {
    const row = { ...summary, ...state, guide_article_id: null };
    serveRows(row);
    withAssessments(row, judged);
    render(<AdminNewsWorkspace />);
    fireEvent.click(await screen.findByRole("button", { name: /Official AI API update/ }));
    expect(await screen.findByText(label)).toBeTruthy();
    expect(screen.queryByRole("heading", { name: /AI 代審（/ })).toBeNull();
  });

  // Each row: status, the judge's decision, the owner's decision, the badge it should carry.
  type BadgeCase = [string, string | null, string | null, string | null];
  const badgeCases: [string, BadgeCase[]][] = [
    ["review", [["manual_review", "manual", null, "AI 交回"], ["manual_review", null, null, null], ["manual_review", "publish", null, null]]],
    ["redraft", [["needs_redraft", "manual", null, "AI 交回"], ["needs_redraft", null, null, null], ["failed", null, null, null]]],
    ["closed", [["rejected", "reject", null, "AI 結案"], ["duplicate", "duplicate", null, "AI 結案"], ["rejected", "manual", "reject", null], ["rejected", null, "reject", null]]],
  ];
  it.each(badgeCases)("marks the rows of the %s list that the AI judge handed back or closed, and no others", async (queue, cases) => {
    window.history.replaceState(null, "", `/zh-TW/admin/news?tab=review&queue=${queue}`);
    serveRows(...cases.map(([status, judgeDecision, humanDecision], index) => ({
      ...summary, id: `00000000-0000-4000-8000-0000000000${50 + index}`, source_title: `Story ${index}`,
      status, judge_decision: judgeDecision, human_decision: humanDecision,
    })));
    render(<AdminNewsWorkspace />);
    await screen.findByRole("button", { name: /Story 0/ });
    const badges = cases.map((_, index) => within(screen.getByRole("button", { name: new RegExp(`Story ${index}`) })).queryByText(/^AI (交回|結案)$/)?.textContent ?? null);
    expect(badges).toEqual(cases.map(([, , , badge]) => badge));
  });

  it("counts the stories the AI judge handed back under the redraft list's hint only", async () => {
    statsExtra = { judge_handed_back: 2 };
    render(<AdminNewsWorkspace />);
    const filters = await screen.findByRole("group", { name: "候選篩選" });
    const redraft = await within(filters).findByRole("button", { name: /需重寫 · 3/ });
    expect(screen.queryByText(/AI 看過後交回給你的/)).toBeNull();
    fireEvent.click(redraft);
    const count = await screen.findByText("其中 2 筆是 AI 看過後交回給你的。");
    expect(count.closest("p")?.textContent).toContain("AI 在寫出五語草稿前就停下了，沒有可以發布的草稿。");
  });

  it.each([undefined, 0])("leaves the count out of the redraft hint when the AI handed nothing back (%s)", async (handedBack) => {
    window.history.replaceState(null, "", "/zh-TW/admin/news?tab=review&queue=redraft");
    statsExtra = { judge_handed_back: handedBack };
    render(<AdminNewsWorkspace />);
    await within(screen.getByRole("group", { name: "候選篩選" })).findByRole("button", { name: /需重寫 · 3/ });
    expect(screen.getByText(/AI 在寫出五語草稿前就停下了，沒有可以發布的草稿/)).toBeTruthy();
    expect(screen.queryByText(/AI 看過後交回給你的/)).toBeNull();
  });

  it("lets the owner take back a story the AI judge closed, with an audited reason", async () => {
    window.history.replaceState(null, "", "/zh-TW/admin/news?tab=review&queue=closed");
    const closed = { ...summary, id: "00000000-0000-4000-8000-000000000061", source_title: "An AI-rejected story", status: "rejected", error_code: "news_zh_draft_ready", guide_article_id: null, judge_decision: "reject" };
    serveRows(closed);
    withAssessments(closed, judgeRow("j1", "reject", "zh_draft", "news_zh_draft_ready", ["只是產品行銷，沒有新的事實"]));
    render(<AdminNewsWorkspace />);
    fireEvent.click(await screen.findByRole("button", { name: /An AI-rejected story/ }));
    expect(await screen.findByText(/這一筆是 AI 結案的，理由在下面/)).toBeTruthy();
    const verdict = screen.getByRole("heading", { name: "AI 代審（claude-opus-5-5）：退件" });
    expect(within(verdict.parentElement!).getAllByRole("listitem").map((item) => item.textContent)).toEqual(["只是產品行銷，沒有新的事實"]);
    expect(actionButtons()).toEqual(["拿回來自己判斷"]);
    const reopen = screen.getByRole("button", { name: "拿回來自己判斷" }) as HTMLButtonElement;
    expect(reopen.disabled).toBe(true);
    fireEvent.change(screen.getByLabelText(/原因（必填/), { target: { value: "這是重要的發布，我自己看" } });
    fireEvent.click(reopen);
    await waitFor(() => expect(posts()).toEqual([`/api/travel/admin/news/candidates/${closed.id}/reopen`]));
    const request = vi.mocked(fetch).mock.calls.find(([, init]) => init?.method === "POST");
    expect(JSON.parse(String(request?.[1]?.body))).toEqual({ reason: "這是重要的發布，我自己看", major_error: false });
    expect(await screen.findByText("已拿回來，AI 不會再判這一筆。")).toBeTruthy();
  });

  it.each([
    ["needs_redraft", "news_verification_failed", null, true],
    ["manual_review", "news_verification_failed", null, false],
    // A rewrite the AI ordered and the writer declined: the AI is done with it and will not
    // be sent this hold, so the note's promise would be false.
    ["needs_redraft", "news_not_eligible", "manual", false],
  ])("explains what the AI judge does with new arrivals on a %s / %s story that has no draft (judge %s): %s", async (status, errorCode, judgeDecision, shown) => {
    serveRows({ ...summary, status, error_code: errorCode, judge_decision: judgeDecision, guide_article_id: null });
    render(<AdminNewsWorkspace />);
    fireEvent.click(await screen.findByRole("button", { name: /Official AI API update/ }));
    expect(await screen.findByText(/AI 在寫出五語草稿前就停下了（原因見上方）/)).toBeTruthy();
    expect(screen.queryAllByText(/「重新執行」是你自己要求整篇重寫/)).toHaveLength(shown ? 1 : 0);
  });

  it("offers the AI judge switch only in automatic mode and saves it with the settings", async () => {
    window.history.replaceState(null, "", "/zh-TW/admin/news?tab=settings");
    render(<AdminNewsWorkspace />);
    const judge = await screen.findByRole("checkbox", { name: "待審查與需重寫交給 AI 判斷" }) as HTMLInputElement;
    expect(judge.disabled).toBe(true);
    expect(judge.checked).toBe(false);
    expect(screen.getByText(/只在自動模式、且該類別開著自動發布時作用/)).toBeTruthy();
    fireEvent.change(screen.getByLabelText("模式"), { target: { value: "automatic" } });
    expect(judge.disabled).toBe(false);
    fireEvent.click(judge);
    expect(judge.checked).toBe(true);
    fireEvent.click(screen.getByRole("button", { name: "儲存設定" }));
    await waitFor(() => expect(fetch).toHaveBeenCalledWith("/api/travel/admin/news/settings", expect.objectContaining({ method: "PUT" })));
    const put = vi.mocked(fetch).mock.calls.find(([, init]) => init?.method === "PUT");
    expect(JSON.parse(String(put?.[1]?.body))).toMatchObject({ mode: "automatic", judge_enabled: true });
  });

  it("leaves the AI judge out of the settings tab when the server's answer has no judge", async () => {
    settingsAnswer = settingsBeforeJudge;
    window.history.replaceState(null, "", "/zh-TW/admin/news?tab=settings");
    render(<AdminNewsWorkspace />);
    expect(await screen.findByText(/統一在「AI 設定 › 各功能模型」選擇/)).toBeTruthy();
    expect(screen.getAllByText(/OpenAI · 預設 · GPT-5\.6 Terra/)).toHaveLength(2);
    expect(screen.getByText(/Anthropic Claude · Claude Next/)).toBeTruthy();
    expect(screen.queryByText("代審模型")).toBeNull();
    expect(screen.getAllByRole("checkbox", { name: "自動發布" })).toHaveLength(3);
    expect(screen.queryByRole("checkbox", { name: "待審查與需重寫交給 AI 判斷" })).toBeNull();
    expect(screen.queryByText(/只在自動模式、且該類別開著自動發布時作用/)).toBeNull();

    fireEvent.click(screen.getByRole("button", { name: "儲存設定" }));
    await waitFor(() => expect(fetch).toHaveBeenCalledWith("/api/travel/admin/news/settings", expect.objectContaining({ method: "PUT" })));
    const put = vi.mocked(fetch).mock.calls.find(([, init]) => init?.method === "PUT");
    // That server refuses a field it does not know, which would fail the whole save.
    expect(JSON.parse(String(put?.[1]?.body))).not.toHaveProperty("judge_enabled");
  });

  it.each([null, "publish"])("re-verifies the saved article after hard checks failed (owner decision: %s)", async (humanDecision) => {
    const articleId = "00000000-0000-4000-8000-000000000042";
    const held = { ...summary, error_code: "news_hard_checks_failed", human_decision: humanDecision, guide_article_id: articleId };
    serveRows(held);
    details[held.id] = { ...detailOf(held), lint: { ja: ["faq_missing"], ko: [] } };
    render(<AdminNewsWorkspace />);
    fireEvent.click(await screen.findByRole("button", { name: /Official AI API update/ }));
    await screen.findByText(/Official release/);
    expect(screen.getByText("文章已儲存但尚未發布。未通過的語系與原因列在下方「硬性檢查」。請到文章編輯器修正，再按「重新查核」，或退件。")).toBeTruthy();
    expect(screen.getByText("faq_missing").closest("article")?.querySelector("h3")?.textContent).toBe("ja");
    expect(screen.getAllByRole("link", { name: /開啟文章編輯器/ }).map((link) => link.getAttribute("href")))
      .toEqual(newsLocales.map((locale) => `/admin/guides?article=${articleId}&lang=${locale}`));
    const verify = screen.getByRole("button", { name: "重新查核" }) as HTMLButtonElement;
    expect(verify.disabled).toBe(true);
    expect(posts()).toEqual([]);
    fireEvent.change(screen.getByLabelText(/原因（必填/), { target: { value: "  已在文章編輯器補齊日文 FAQ  " } });
    expect(verify.disabled).toBe(false);
    fireEvent.click(verify);
    await waitFor(() => expect(posts()).toEqual([`/api/travel/admin/news/candidates/${held.id}/verify`]));
    const request = vi.mocked(fetch).mock.calls.find(([, init]) => init?.method === "POST");
    expect(JSON.parse(String(request?.[1]?.body))).toEqual({ reason: "已在文章編輯器補齊日文 FAQ", major_error: false });
    expect(await screen.findByText(adminNewsCopy("zh-TW").doneVerify)).toBeTruthy();
  });

  it("confirms a Chinese draft and says the translations have started", async () => {
    const draft = { ...summary, error_code: "news_zh_draft_ready", guide_article_id: null, human_decision: null };
    serveRows(draft);
    details[draft.id] = {
      ...detailOf(draft),
      documents: { "zh-TW": { ...document, title: "繁中草稿標題" } },
      assessments: [{ id: "j1", assessment_type: "jev", locale: "zh-TW", verdict: "pass", confidence: 0.93, provider: "jev", model: "jev", reasons: [], details: { tier: "act" }, created_at: "2026-09-25T01:00:00Z" }],
    };
    render(<AdminNewsWorkspace />);
    fireEvent.click(await screen.findByRole("button", { name: /Official AI API update/ }));
    expect(await screen.findByText("繁中草稿標題")).toBeTruthy();
    expect(screen.getAllByText("繁中草稿待確認").length).toBeGreaterThan(0);
    expect(screen.getByText(/繁中草稿已經寫好，也通過查核模型對照原文的查核/)).toBeTruthy();
    expect(screen.getByText("Jev 對這份繁中稿的判斷：可自動處理（信心 0.93）")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "內容正確，可以發布" }));
    fireEvent.click(screen.getByRole("button", { name: "確認發布，翻譯其他語言" }));
    await waitFor(() => expect(posts()).toEqual([`/api/travel/admin/news/candidates/${draft.id}/approve`]));
    expect(await screen.findByText(/已確認發布，正在翻譯另外四語/)).toBeTruthy();
  });

  it("rejects the ticked rows of a list one by one and reports the result", async () => {
    window.history.replaceState(null, "", "/zh-TW/admin/news?tab=review&queue=redraft");
    const first = { ...summary, id: "00000000-0000-4000-8000-000000000021", status: "needs_redraft", error_code: "news_verification_failed", guide_article_id: null, source_title: "First stopped story" };
    const second = { ...first, id: "00000000-0000-4000-8000-000000000022", source_title: "Second stopped story" };
    serveRows(first, second);
    vi.stubGlobal("confirm", vi.fn(() => true));
    render(<AdminNewsWorkspace />);
    expect(await screen.findByText(/AI 在寫出五語草稿前就停下了，沒有可以發布的草稿/)).toBeTruthy();
    expect(listCalls().at(-1)).toContain("status=needs_redraft&status=failed");
    fireEvent.click(screen.getByRole("checkbox", { name: "選取 First stopped story" }));
    fireEvent.click(screen.getByRole("checkbox", { name: "選取 Second stopped story" }));
    expect(screen.getByText("已選 2 筆")).toBeTruthy();
    const reject = screen.getByRole("button", { name: "退件所選" }) as HTMLButtonElement;
    expect(reject.disabled).toBe(true);
    fireEvent.click(screen.getByRole("button", { name: "舊聞，已經過時" }));
    fireEvent.click(reject);
    await waitFor(() => expect(posts()).toEqual([
      `/api/travel/admin/news/candidates/${first.id}/reject`,
      `/api/travel/admin/news/candidates/${second.id}/reject`,
    ]));
    expect(confirm).toHaveBeenCalledWith("確定退件 2 筆？退件後不能復原。");
    expect(await screen.findByText("已退件 2 筆。")).toBeTruthy();
    const bodies = vi.mocked(fetch).mock.calls.filter(([, init]) => init?.method === "POST").map(([, init]) => JSON.parse(String(init?.body)) as { reason: string });
    expect(bodies.map((body) => body.reason)).toEqual(["舊聞，已經過時", "舊聞，已經過時"]);
  });

  it("asks the API only for the statuses of the chosen list and pages through it", async () => {
    pages = 3;
    render(<AdminNewsWorkspace />);
    await screen.findByRole("button", { name: /Official AI API update/ });
    expect(listCalls().at(-1)).toContain("status=manual_review&status=shadow_review");
    expect(listCalls().at(-1)).not.toContain("failed");
    expect(listCalls().at(-1)).toContain("page=1");
    fireEvent.click(screen.getByRole("button", { name: "下一頁" }));
    await waitFor(() => expect(listCalls().at(-1)).toContain("page=2"));
    expect(new URL(window.location.href).searchParams.get("page")).toBe("2");

    const filters = screen.getByRole("group", { name: "候選篩選" });
    fireEvent.click(within(filters).getByRole("button", { name: /缺證據/ }));
    await waitFor(() => expect(listCalls().at(-1)).toContain("status=needs_evidence"));
    expect(listCalls().at(-1)).toContain("page=1");
    expect(screen.getByText(/沒有可以引用的證據頁/)).toBeTruthy();
    const url = new URL(window.location.href);
    expect(url.searchParams.get("queue")).toBe("evidence");
    expect(url.searchParams.get("page")).toBeNull();
    expect(within(filters).getByRole("button", { name: /需重寫 · 3/ })).toBeTruthy();
    fireEvent.click(within(filters).getByRole("button", { name: /已退件/ }));
    await waitFor(() => expect(listCalls().at(-1)).toContain("status=rejected&status=duplicate"));
    expect(screen.queryByRole("checkbox")).toBeNull();
  });

  it("shows the news models read-only, links to AI settings and leaves them out of a save", async () => {
    window.history.replaceState(null, "", "/zh-TW/admin/news?tab=settings");
    render(<AdminNewsWorkspace />);
    expect(await screen.findByText(/統一在「AI 設定 › 各功能模型」選擇/)).toBeTruthy();
    expect(screen.queryByLabelText("模型")).toBeNull();
    expect(screen.getAllByText(/OpenAI · 預設 · GPT-5\.6 Terra/)).toHaveLength(2);
    expect(screen.getByText(/Anthropic Claude · Claude Next/)).toBeTruthy();
    expect(screen.getByText("代審模型").parentElement?.textContent).toBe("代審模型 · Anthropic Claude · 預設 · Claude Sonnet 5");
    expect(screen.getByRole("link", { name: "到 AI 設定修改" }).getAttribute("href")).toBe("/admin/ai-accounts?tab=models&section=news");

    fireEvent.click(screen.getByRole("button", { name: "儲存設定" }));
    await waitFor(() => expect(fetch).toHaveBeenCalledWith("/api/travel/admin/news/settings", expect.objectContaining({ method: "PUT" })));
    const put = vi.mocked(fetch).mock.calls.find(([, init]) => init?.method === "PUT");
    const body = JSON.parse(String(put?.[1]?.body)) as Record<string, unknown>;
    for (const left of ["gates", "updated_at", "model_options", "default_models", "writer_provider", "writer_model", "verifier_provider", "verifier_model", "editor_provider", "editor_model", "judge_provider", "judge_model"]) expect(body).not.toHaveProperty(left);
    // The switch is this page's own setting, unlike the judge's model.
    expect(body.judge_enabled).toBe(false);
  });

  it("picks the writer, checker, final editor and review judge models on the AI settings page", async () => {
    render(<AdminNewsModelSettings />);
    const [writerModel, verifierModel, editorModel, judgeModel] = await screen.findAllByLabelText("模型") as HTMLSelectElement[];
    expect(screen.getAllByLabelText("模型")).toHaveLength(4);
    expect(screen.getByRole("group", { name: "最終修改模型" })).toBeTruthy();
    expect(editorModel.value).toBe("claude-next");
    expect(within(screen.getByRole("group", { name: "代審模型" })).getByText(/建議選和撰稿不同的模型/)).toBeTruthy();
    expect(judgeModel.value).toBe("");
    const labels = (select: HTMLSelectElement) => Array.from(select.options).map((option) => option.text);
    expect(labels(writerModel)).toEqual(["預設 · GPT-5.6 Terra", "GPT-6 Astra", "GPT-5.6 Terra", "自訂…"]);
    expect(screen.getAllByText("Balanced default.")).toHaveLength(2);
    expect(screen.getByText(/換模型不會關掉自動發布/)).toBeTruthy();

    fireEvent.change(writerModel, { target: { value: "gpt-6-astra" } });
    expect(writerModel.value).toBe("gpt-6-astra");
    fireEvent.change(verifierModel, { target: { value: "__custom__" } });
    fireEvent.change(screen.getByLabelText("模型 · 自訂模型 ID"), { target: { value: " gpt-7-preview " } });

    const [writerVendor] = screen.getAllByLabelText("供應商") as HTMLSelectElement[];
    fireEvent.change(writerVendor, { target: { value: "anthropic" } });
    const [writerAfterSwitch] = screen.getAllByLabelText("模型") as HTMLSelectElement[];
    expect(writerAfterSwitch.value).toBe("");
    expect(labels(writerAfterSwitch)).toEqual(["預設 · Claude Sonnet 5", "Claude Sonnet 5", "Claude Next (預覽版)", "自訂…"]);
    fireEvent.change(judgeModel, { target: { value: "claude-next" } });

    fireEvent.click(screen.getByRole("button", { name: "儲存新聞模型" }));
    await waitFor(() => expect(fetch).toHaveBeenCalledWith("/api/travel/admin/news/settings/models", expect.objectContaining({ method: "PUT" })));
    const put = vi.mocked(fetch).mock.calls.find(([, init]) => init?.method === "PUT");
    expect(JSON.parse(String(put?.[1]?.body))).toEqual({ writer_provider: "anthropic", writer_model: null, verifier_provider: "openai", verifier_model: "gpt-7-preview", editor_provider: "anthropic", editor_model: "claude-next", judge_provider: "anthropic", judge_model: "claude-next" });
    expect(await screen.findByText("已儲存。")).toBeTruthy();
  });

  it("picks only the three older roles when the server's answer has no review judge", async () => {
    settingsAnswer = settingsBeforeJudge;
    render(<AdminNewsModelSettings />);
    const [writerModel] = await screen.findAllByLabelText("模型") as HTMLSelectElement[];
    expect(screen.getAllByLabelText("模型")).toHaveLength(3);
    expect(screen.getAllByLabelText("供應商")).toHaveLength(3);
    expect(screen.getByRole("group", { name: "最終修改模型" })).toBeTruthy();
    expect(screen.queryByRole("group", { name: "代審模型" })).toBeNull();
    expect(screen.queryByText(/建議選和撰稿不同的模型/)).toBeNull();
    expect(screen.queryByLabelText("模型 · 自訂模型 ID")).toBeNull();

    fireEvent.change(writerModel, { target: { value: "gpt-6-astra" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存新聞模型" }));
    await waitFor(() => expect(fetch).toHaveBeenCalledWith("/api/travel/admin/news/settings/models", expect.objectContaining({ method: "PUT" })));
    const put = vi.mocked(fetch).mock.calls.find(([, init]) => init?.method === "PUT");
    expect(JSON.parse(String(put?.[1]?.body))).toEqual({ writer_provider: "openai", writer_model: "gpt-6-astra", verifier_provider: "openai", verifier_model: null, editor_provider: "anthropic", editor_model: "claude-next" });
    expect(await screen.findByText("已儲存。")).toBeTruthy();
  });

  it("names a draft approval and a rewrite order in English as calls, not as things that happened", async () => {
    site.locale = "en";
    // The AI approved the draft, and the story then stopped at Jev's last call unpublished.
    const held = { ...summary, error_code: "news_jev_final_hold" };
    serveRows(held);
    withAssessments(held,
      judgeRow("j0", "revise", "redraft", "news_verification_failed", ["把第三段的推測刪掉"]),
      judgeRow("j1", "publish", "zh_draft", "news_zh_draft_ready", ["每個主張都有來源支持"]),
    );
    render(<AdminNewsWorkspace />);
    fireEvent.click(await screen.findByRole("button", { name: /Official AI API update/ }));
    expect(await screen.findByText("AI review・zh-TW draft: publish")).toBeTruthy();
    expect(screen.getByText("AI review・needs redraft: revise and review again")).toBeTruthy();
    expect(screen.getAllByText("Needs your decision").length).toBeGreaterThan(0);
  });

  it("keeps a complete copy catalog in every site locale", () => {
    const flatten = (value: unknown, prefix = ""): Array<[string, unknown]> =>
      value && typeof value === "object" && !Array.isArray(value)
        ? Object.entries(value).flatMap(([key, child]) => flatten(child, `${prefix}${key}.`))
        : Array.isArray(value)
          ? value.map((child, index) => [`${prefix}${index}`, child] as [string, unknown])
          : [[prefix, value]];
    const keys = flatten(adminNewsCopy("en")).map(([key]) => key).sort();
    for (const locale of ["zh-TW", "zh-CN", "ja", "ko"]) {
      const entries = flatten(adminNewsCopy(locale));
      expect(entries.map(([key]) => key).sort()).toEqual(keys);
      expect(entries.every(([, value]) => typeof value === "string" && value.trim())).toBe(true);
      expect(adminNewsCopy(locale).title).not.toBe("AI hourly news");
      expect(adminNewsCopy(locale).statuses.needs_redraft).not.toBe("Needs redraft");
    }
  });
});
