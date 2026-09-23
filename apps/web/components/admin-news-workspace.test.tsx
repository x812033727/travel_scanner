import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { AdminNewsWorkspace } from "./admin-news-workspace";
import { adminNewsCopy } from "@/lib/admin-news-copy";

vi.mock("next-intl", () => ({ useLocale: () => "zh-TW" }));
vi.mock("@/i18n/navigation", () => ({
  Link: ({ href, children, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement> & { href: string }) => <a href={href} {...props}>{children}</a>,
  useRouter: () => ({ replace: vi.fn() }),
}));

const summary = {
  id: "00000000-0000-4000-8000-000000000001", vertical: "ai", status: "manual_review",
  source_title: "Official AI API update", canonical_url: "https://example.com/news",
  event_date: "2026-09-23", would_publish: false, human_decision: null, error_code: "news_jev_manual",
  error_detail: "English locale requested confirmation.", guide_article_id: "00000000-0000-4000-8000-000000000002",
  created_at: "2026-09-23T10:00:00Z", updated_at: "2026-09-23T11:00:00Z",
};
const document = {
  title: "API 更新如何影響一般使用者", description: "已查核的五語新聞。", hero: null,
  blocks: [{ type: "paragraph", text: "這是完整文章內容。" }],
  sources: [{ title: "Official", url: "https://example.com/release", checked_on: "2026-09-23" }],
};
const detail = {
  ...summary,
  evidence: [{ id: "e1", role: "evidence", is_first_party: true, url: "https://example.com/release", title: "Official release", retrieved_at: "2026-09-23T10:00:00Z", source_date: "2026-09-23", content_hash: "a".repeat(64), excerpt: "Verified evidence excerpt." }],
  assessments: [{ id: "a1", assessment_type: "jev", locale: "en", verdict: "manual", confidence: 0.75, provider: "jev", model: "jev", reasons: [], details: { tier: "confirm" }, created_at: "2026-09-23T11:00:00Z" }],
  runs: [{ id: "r1", stage: "jev", status: "succeeded", attempt: 1, provider: "jev", model: "jev", input_tokens: 20, output_tokens: 0, error_code: null, error_detail: null, metadata: {}, started_at: "2026-09-23T11:00:00Z", finished_at: "2026-09-23T11:00:01Z" }],
  documents: Object.fromEntries(["zh-TW", "zh-CN", "en", "ja", "ko"].map((locale) => [locale, { ...document, title: `${document.title} ${locale}` }])),
  claim_ledger: [], lint: {}, human_reason: null, human_major_error: false,
};
const settings = {
  enabled: false, mode: "shadow", writer_provider: "openai", writer_model: null,
  verifier_provider: "openai", verifier_model: null, global_concurrency: 2,
  per_vertical_concurrency: 1, min_shadow_days: 14, min_shadow_candidates: 50,
  min_human_agreement: 0.95, jev_act_confidence: 0.9, auto_publish_ai: false,
  auto_publish_tech: false, auto_publish_crypto: false, prompt_version: "news-v1",
  policy_version: "news-policy-v1", updated_at: "2026-09-23T10:00:00Z",
  gates: Object.fromEntries(["ai", "tech", "crypto"].map((vertical) => [vertical, { vertical, days: 0, labelled_candidates: 0, agreements: 0, agreement_rate: 0, serious_false_positives: 0, eligible: false, reasons: ["shadow_days:0/14"] }])),
};

beforeEach(() => {
  window.history.replaceState(null, "", "/zh-TW/admin/news?tab=review");
  vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith(`/admin/news/candidates/${summary.id}`)) return Response.json(detail);
    if (url.includes(`/admin/news/candidates/${summary.id}/publish`) && init?.method === "POST") {
      return Response.json({ ...detail, status: "published", human_decision: "publish" });
    }
    if (url.includes("/admin/news/candidates?")) return Response.json({ candidates: [summary], total: 1, page: 1, pages: 1 });
    if (url.endsWith("/admin/news/sources")) return Response.json([]);
    if (url.endsWith("/admin/news/settings")) return Response.json(settings);
    if (url.endsWith("/admin/news/stats")) return Response.json({ pending_review: 1, failed: 0, published: 3, queue_by_status: { manual_review: 1 } });
    return Response.json({ detail: "not found" }, { status: 404 });
  }));
});
afterEach(() => vi.unstubAllGlobals());

describe("AdminNewsWorkspace", () => {
  it("shows the review badge data, five locales, evidence and audited publish action", async () => {
    render(<AdminNewsWorkspace />);
    expect(await screen.findByRole("heading", { name: "AI 每小時自動新聞" })).toBeTruthy();
    fireEvent.click(await screen.findByRole("button", { name: /Official AI API update/ }));
    expect(await screen.findByText(/Official release/)).toBeTruthy();
    expect(screen.getAllByRole("button").filter((button) => ["zh-TW", "zh-CN", "en", "ja", "ko"].includes(button.textContent || ""))).toHaveLength(5);
    expect(screen.getByRole("link", { name: /開啟文章編輯器 · zh-TW/ }).getAttribute("href")).toContain(`article=${summary.guide_article_id}`);
    fireEvent.change(screen.getByLabelText("必填原因"), { target: { value: "人工確認來源與五語完整" } });
    fireEvent.click(screen.getByRole("button", { name: "五語發布" }));
    await waitFor(() => expect(fetch).toHaveBeenCalledWith(
      `/api/travel/admin/news/candidates/${summary.id}/publish`,
      expect.objectContaining({ method: "POST" }),
    ));
  });

  it("keeps a complete local copy catalog in every site locale", () => {
    const keys = Object.keys(adminNewsCopy("en")).sort();
    for (const locale of ["zh-TW", "zh-CN", "ja", "ko"]) {
      const copy = adminNewsCopy(locale);
      expect(Object.keys(copy).sort()).toEqual(keys);
      expect(Object.values(copy).every((value) => value.trim())).toBe(true);
      expect(copy.nav).not.toBe("AI News");
    }
  });
});
