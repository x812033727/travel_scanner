import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { type SlidesRequest, SlidesRequests } from "./admin-video-slides-requests";
import type { AdminBootstrap } from "@/lib/admin-operations";

function bootstrap(capabilities: string[]): AdminBootstrap {
  return { admin_roles: [], admin_capabilities: capabilities, navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false };
}
const READER = ["content.read"];
const MANAGER = ["content.read", "content.manage"];

const base: SlidesRequest = {
  id: "6f1d2c3b-4a59-4e6f-8a7b-9c0d1e2f3a4b", source_guide: "ai-freelance-getting-started", title: "AI 接案入門", url: "https://mokaair.com/zh-TW/life/ai-freelance-getting-started",
  note: null, status: "queued", slug: null, created_by_user_id: null, created_at: "2026-10-05T01:00:00Z", started_at: null, finished_at: null, cancelled_at: null,
};
const started: SlidesRequest = {
  ...base, id: "7a2e3d4c-5b6a-4f70-8b8c-0d1e2f3a4b5c", source_guide: "ai-trading-bot-claims", title: null, url: "https://mokaair.com/zh-TW/life/ai-trading-bot-claims",
  note: "只講制度，不推薦個股", status: "started", slug: "slides-7a2e3d4c", started_at: "2026-10-05T02:00:00Z",
};

type Call = { url: string; method: string; body: unknown };
/** A fetch stub for the requests route: `answer` gives the list (or a problem) at call time; a POST or DELETE goes to `write`. */
function stubFetch(answer: () => Response, write: (call: Call) => Response = () => Response.json(base, { status: 201 })) {
  const calls: Call[] = [];
  vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    const call = { url: String(input), method: init?.method ?? "GET", body: init?.body ? JSON.parse(String(init.body)) : undefined };
    calls.push(call);
    return Promise.resolve(call.method === "GET" ? answer() : write(call));
  }));
  return calls;
}
const listed = (requests: unknown) => () => Response.json({ requests });
const show = (capabilities: string[], onOpen = vi.fn()) =>
  render(<AdminOperationsProvider bootstrap={bootstrap(capabilities)}><SlidesRequests onOpen={onOpen} /></AdminOperationsProvider>);

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
  vi.useRealTimers();
});

describe("SlidesRequests", () => {
  it("shows a reader the queue with each article and its state, but no form and no withdraw button", async () => {
    const calls = stubFetch(listed([base, started]));
    show(READER);
    const queue = await screen.findByRole("region", { name: "指定文章的影片" });
    expect(calls[0].url).toBe("/api/travel/admin/video-automation/slides-requests");
    // A sibling of the tutorials tab's h2 groups, right under the page's h1.
    expect(within(queue).getByRole("heading", { name: "指定文章的影片" }).tagName).toBe("H2");
    const rows = within(queue).getAllByRole("listitem");
    expect(rows).toHaveLength(2);
    expect(rows[0].textContent).toContain("排隊中");
    expect(rows[0].textContent).toContain("AI 接案入門");
    // A request filed before its title was known reads as its slug.
    expect(rows[1].textContent).toContain("製作中");
    expect(within(rows[1]).getAllByText(/ai-trading-bot-claims/).length).toBeGreaterThan(0);
    expect(rows[1].textContent).toContain("只講制度，不推薦個股");
    const link = within(rows[0]).getByRole("link", { name: "看文章" });
    expect(link.getAttribute("href")).toBe(base.url);
    expect(link.getAttribute("target")).toBe("_blank");
    expect(screen.queryByText("用站上文章做一支教學影片")).toBeNull();
    expect(screen.queryByRole("button", { name: "取消" })).toBeNull();
  });

  it("shows a reader nothing at all while nothing was asked for", async () => {
    const calls = stubFetch(listed([]));
    const { container } = show(READER);
    await waitFor(() => expect(calls).toHaveLength(1));
    expect(container.innerHTML).toBe("");
  });

  it("says done once the video is on YouTube and dropped once it was dropped, and keeps a finished one only for a week", async () => {
    vi.useFakeTimers({ toFake: ["Date"] });
    vi.setSystemTime(new Date("2026-10-20T00:00:00Z"));
    const old = { ...started, created_at: "2026-10-01T00:00:00Z" };
    stubFetch(listed([
      { ...base, id: "a", source_guide: "queued-long-ago", title: "很久以前排的", created_at: "2026-09-01T00:00:00Z" },
      { ...old, id: "b", source_guide: "started-long-ago", title: "很久以前開始的" },
      { ...old, id: "c", source_guide: "done-this-week", title: "這週完成的", status: "done", created_at: "2026-10-14T00:00:00Z" },
      { ...old, id: "d", source_guide: "dropped-this-week", title: "這週放棄的", status: "dropped", created_at: "2026-10-13T00:01:00Z" },
      { ...old, id: "e", source_guide: "done-long-ago", title: "很久以前完成的", status: "done" },
      { ...old, id: "f", source_guide: "cancelled-long-ago", title: "很久以前取消的", status: "cancelled", created_at: "2026-10-12T23:59:00Z" },
    ]));
    show(READER);
    const queue = await screen.findByRole("region", { name: "指定文章的影片" });
    const rows = within(queue).getAllByRole("listitem").map((row) => row.textContent ?? "");
    expect(rows).toHaveLength(4);
    expect(rows[0]).toContain("很久以前排的");
    expect(rows[1]).toContain("很久以前開始的");
    expect(rows[2]).toContain("完成");
    expect(rows[3]).toContain("已放棄");
    expect(queue.textContent).not.toContain("很久以前完成的");
    expect(queue.textContent).not.toContain("很久以前取消的");
  });

  it("lets a manager file a request only for a well-formed slug, posting the trimmed slug and note and reading the queue again", async () => {
    let requests: SlidesRequest[] = [];
    const calls = stubFetch(() => Response.json({ requests }), (call) => {
      const body = call.body as { source_guide: string; note?: string };
      requests = [{ ...base, source_guide: body.source_guide, note: body.note ?? null }];
      return Response.json(requests[0], { status: 201 });
    });
    show(MANAGER);
    fireEvent.click(await screen.findByText("用站上文章做一支教學影片", { selector: "summary" }));
    const form = screen.getByRole("form", { name: "用站上文章做一支教學影片" });
    const submit = within(form).getByRole("button", { name: "排進製作" });
    const article = within(form).getByRole("textbox", { name: "站上文章（slug）" });
    expect(submit).toHaveProperty("disabled", true);
    fireEvent.change(article, { target: { value: "Not A Slug" } });
    expect(submit).toHaveProperty("disabled", true);
    expect(article.getAttribute("aria-invalid")).toBe("true");
    fireEvent.change(article, { target: { value: "  ai-freelance-getting-started " } });
    expect(submit).toHaveProperty("disabled", false);
    fireEvent.change(within(form).getByRole("textbox", { name: "給企劃的備註（選填）" }), { target: { value: "  結尾加免責說明  " } });
    fireEvent.click(submit);
    await waitFor(() => expect(calls.some((call) => call.method === "POST")).toBe(true));
    const post = calls.find((call) => call.method === "POST");
    expect(post?.url).toBe("/api/travel/admin/video-automation/slides-requests");
    expect(post?.body).toEqual({ source_guide: "ai-freelance-getting-started", note: "結尾加免責說明" });
    const queue = await screen.findByRole("region", { name: "指定文章的影片" });
    expect(queue.textContent).toContain("結尾加免責說明");
    expect(calls.filter((call) => call.method === "GET").length).toBeGreaterThanOrEqual(2);
    expect((article as HTMLInputElement).value).toBe("");
  });

  it("leaves the note out when it is blank and shows the server's reason when it refuses", async () => {
    const calls = stubFetch(listed([]), () => Response.json(
      { title: "Conflict", status: 409, code: "video_slides_request_article_used", detail: "這篇文章已經有影片了" }, { status: 409 },
    ));
    show(MANAGER);
    fireEvent.click(await screen.findByText("用站上文章做一支教學影片", { selector: "summary" }));
    fireEvent.change(screen.getByRole("textbox", { name: "站上文章（slug）" }), { target: { value: "ai-concept-stocks-explained" } });
    fireEvent.change(screen.getByRole("textbox", { name: "給企劃的備註（選填）" }), { target: { value: "   " } });
    fireEvent.click(screen.getByRole("button", { name: "排進製作" }));
    expect((await screen.findByRole("alert")).textContent).toBe("沒有排進：這篇文章已經有影片了");
    expect(calls.find((call) => call.method === "POST")?.body).toEqual({ source_guide: "ai-concept-stocks-explained" });
    // A refused request keeps what the owner typed.
    expect((screen.getByRole("textbox", { name: "站上文章（slug）" }) as HTMLInputElement).value).toBe("ai-concept-stocks-explained");
  });

  it("withdraws a queued request after a confirmation, and offers no withdraw on a started one", async () => {
    let requests: SlidesRequest[] = [base, started];
    const calls = stubFetch(() => Response.json({ requests }), (call) => {
      requests = requests.map((request) => (call.url.endsWith(request.id) ? { ...request, status: "cancelled", cancelled_at: "2026-10-05T03:00:00Z" } : request));
      return Response.json(requests[0]);
    });
    const confirm = vi.spyOn(window, "confirm").mockReturnValueOnce(false).mockReturnValueOnce(true);
    show(MANAGER);
    const queue = await screen.findByRole("region", { name: "指定文章的影片" });
    const [queuedRow, startedRow] = within(queue).getAllByRole("listitem");
    expect(within(startedRow).queryByRole("button", { name: "取消" })).toBeNull();
    fireEvent.click(within(queuedRow).getByRole("button", { name: "取消" }));
    expect(confirm).toHaveBeenCalledWith("取消這個請求？工人就不會做它。");
    expect(calls.some((call) => call.method === "DELETE")).toBe(false);
    fireEvent.click(within(queuedRow).getByRole("button", { name: "取消" }));
    await waitFor(() => expect(calls.some((call) => call.method === "DELETE")).toBe(true));
    expect(calls.find((call) => call.method === "DELETE")?.url).toBe(`/api/travel/admin/video-automation/slides-requests/${base.id}`);
    await waitFor(() => expect(within(screen.getByRole("region", { name: "指定文章的影片" })).getAllByRole("listitem")[0].textContent).toContain("已取消"));
  });

  it("opens a started request's video", async () => {
    stubFetch(listed([started]));
    const onOpen = vi.fn();
    show(READER, onOpen);
    fireEvent.click(await screen.findByRole("button", { name: "打開 slides-7a2e3d4c" }));
    expect(onOpen).toHaveBeenCalledWith("slides-7a2e3d4c");
  });

  it("shows nothing on an API without the route, even to a manager", async () => {
    const calls = stubFetch(() => Response.json({ title: "Not Found", status: 404, detail: "Not Found" }, { status: 404 }));
    const { container } = show(MANAGER);
    await waitFor(() => expect(calls).toHaveLength(1));
    await Promise.resolve();
    expect(container.innerHTML).toBe("");
  });

  it("reads an answer that is not the list as an empty queue", async () => {
    for (const answer of [[], { slug: "ai-model-choice", reviews: [] }, { requests: "nope" }, { requests: [null, 3, { id: "x" }] }]) {
      const calls = stubFetch(() => Response.json(answer));
      const { unmount } = show(MANAGER);
      expect(await screen.findByText("用站上文章做一支教學影片", { selector: "summary" })).toBeTruthy();
      expect(calls).toHaveLength(1);
      expect(screen.queryByRole("region", { name: "指定文章的影片" })).toBeNull();
      unmount();
      vi.unstubAllGlobals();
    }
  });

  it("quotes a setting in the form's help only by the label the settings tab gives it", async () => {
    const catalogs = await Promise.all([
      import("@/messages/zh-TW/admin.json"), import("@/messages/zh-CN/admin.json"),
      import("@/messages/en/admin.json"), import("@/messages/ja/admin.json"), import("@/messages/ko/admin.json"),
    ]);
    for (const { default: copy } of catalogs) {
      const quoted = [...copy.videoReviews.slidesRequests.help.matchAll(/[「“"]([^」”"]+)[」”"]/g)].map((match) => match[1]);
      for (const phrase of quoted) expect(Object.values(copy.videoSettings.fields)).toContain(phrase);
    }
    // The Chinese texts name the waiting-drafts cap outright; the others paraphrase it.
    const [zhTW, zhCN] = catalogs.map((catalog) => catalog.default);
    expect(zhTW.videoReviews.slidesRequests.help).toContain(`「${zhTW.videoSettings.fields.max_waiting_drafts}」`);
    expect(zhCN.videoReviews.slidesRequests.help).toContain(`“${zhCN.videoSettings.fields.max_waiting_drafts}”`);
  });
});
