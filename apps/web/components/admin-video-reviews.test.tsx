import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { AdminVideoReviews } from "./admin-video-reviews";
import type { AdminBootstrap } from "@/lib/admin-operations";

vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: null, sessionIdentity: null, status: undefined }) }));

function bootstrap(capabilities: string[]): AdminBootstrap {
  return { admin_roles: [], admin_capabilities: capabilities, navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false };
}

const summary = {
  slug: "ai-model-choice", title: "AI 模型怎麼挑", stage: "final", youtube_video_id: null,
  last_synced_at: "2026-09-25T05:00:00Z", pending: 2,
  checklist: [{ key: "brief", label: "企劃", done: true }, { key: "final", label: "成片", done: false }],
};
const outline = {
  id: "11111111-1111-4111-8111-111111111111", gate: "outline", content_sha256: "a".repeat(64), summary: "三個大綱",
  payload: { brief: "# 企劃", options: [{ key: "A", title: "判斷方法框架" }, { key: "B", title: "從情境開始" }] },
  files: [], status: "pending", choice: null, note: null, decided_at: null, created_at: "2026-09-25T05:00:00Z",
};
const final = {
  id: "22222222-2222-4222-8222-222222222222", gate: "final", content_sha256: "b".repeat(64), summary: "成片 10:00",
  payload: { checks: { ok: true, problems: [] }, chapters: [{ time: "0:00", title: "開場" }] },
  files: [{ role: "preview", sha256: "c".repeat(64), size: 10, content_type: "video/mp4" }],
  status: "pending", choice: null, note: null, decided_at: null, created_at: "2026-09-25T05:00:00Z",
};

function stubFetch() {
  const posts: Array<{ url: string; body: unknown }> = [];
  const fetchMock = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (init?.method === "POST") {
      posts.push({ url, body: JSON.parse(String(init.body)) });
      return Promise.resolve(Response.json({ ...outline, status: "approved" }));
    }
    const body = url.endsWith("/admin/videos") ? [summary] : { ...summary, reviews: [outline, final] };
    return Promise.resolve(Response.json(body));
  });
  vi.stubGlobal("fetch", fetchMock);
  return posts;
}

afterEach(() => {
  vi.unstubAllGlobals();
  window.history.replaceState(null, "", "/");
});

describe("AdminVideoReviews", () => {
  it("lists videos, opens one, and approves an outline only once an option is chosen", async () => {
    const posts = stubFetch();
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    fireEvent.click(await screen.findByRole("button", { name: /AI 模型怎麼挑/ }));
    const approve = await screen.findByRole("button", { name: "用這個大綱" });
    expect(approve).toHaveProperty("disabled", true);
    fireEvent.click(screen.getByRole("radio", { name: /選項 B/ }));
    expect(approve).toHaveProperty("disabled", false);
    fireEvent.click(approve);
    await waitFor(() => expect(posts).toHaveLength(1));
    expect(posts[0].url).toContain(`/admin/videos/ai-model-choice/reviews/${outline.id}/decision`);
    expect(posts[0].body).toEqual({ decision: "approve", choice: "B" });
    expect(window.location.search).toContain("video=ai-model-choice");
  });

  it("plays the preview through the admin file route and needs a reason to send a cut back", async () => {
    stubFetch();
    window.history.replaceState(null, "", "/?video=ai-model-choice");
    const { container } = render(<AdminOperationsProvider bootstrap={bootstrap(["content.read", "content.manage"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const card = await screen.findByRole("article", { name: "成片" });
    expect(container.querySelector("video")?.getAttribute("src")).toBe(`/api/admin-video-files/ai-model-choice/${"c".repeat(64)}`);
    const sendBack = card.querySelector("button:last-of-type") as HTMLButtonElement;
    expect(sendBack.textContent).toBe("退回");
    expect(sendBack.disabled).toBe(true);
    fireEvent.change(card.querySelector("textarea") as HTMLTextAreaElement, { target: { value: "片頭太長" } });
    expect(sendBack.disabled).toBe(false);
  });

  it("lets a reader look but not decide", async () => {
    stubFetch();
    window.history.replaceState(null, "", "/?video=ai-model-choice");
    render(<AdminOperationsProvider bootstrap={bootstrap(["content.read"])}><AdminVideoReviews /></AdminOperationsProvider>);
    const approve = await screen.findByRole("button", { name: "核准" });
    expect(approve).toHaveProperty("disabled", true);
  });
});
