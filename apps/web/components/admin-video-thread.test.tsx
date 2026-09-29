import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { DiscussionThread, docSubject, scriptSubject, threadPath } from "./admin-video-thread";

type Line = { id: string; subject: string; author: string; body_md: string; refers_to: string | null; answered_at: string | null; created_at: string; created_by_user_id: string | null };
const lines: Line[] = [
  { id: "m1", subject: "script:1", author: "owner", body_md: "開場的鐘聲太早。", refers_to: "1a2b3c4d5e6f", answered_at: "2026-09-27T05:10:00Z", created_at: "2026-09-27T05:00:00Z", created_by_user_id: "u1" },
  { id: "m2", subject: "script:1", author: "writer", body_md: "把鐘聲移到沈瀾開口之後了。", refers_to: "6f5e4d3c2b1a", answered_at: "2026-09-27T05:10:00Z", created_at: "2026-09-27T05:10:00Z", created_by_user_id: null },
];

type Call = { url: string; method: string; body?: unknown };
function stubFetch(refusal?: { status: number; code: string; detail: string }) {
  const calls: Call[] = [];
  let thread = [...lines];
  vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    const method = init?.method ?? "GET";
    const body = init?.body ? JSON.parse(String(init.body)) as { subject: string; body: string } : undefined;
    calls.push({ url, method, body });
    if (method === "POST") {
      if (refusal) return Promise.resolve(Response.json({ type: "about:blank", title: "Conflict", status: refusal.status, code: refusal.code, detail: refusal.detail }, { status: refusal.status }));
      const line: Line = { id: "m3", subject: body?.subject ?? "", author: "owner", body_md: body?.body ?? "", refers_to: "6f5e4d3c2b1a", answered_at: null, created_at: "2026-09-27T05:20:00Z", created_by_user_id: "u1" };
      thread = [...thread, line];
      return Promise.resolve(Response.json(line, { status: 201 }));
    }
    return Promise.resolve(Response.json({ messages: thread }));
  }));
  return calls;
}

afterEach(() => vi.unstubAllGlobals());

describe("DiscussionThread", () => {
  it("names the API's subjects and path", () => {
    expect(docSubject("setting", 0)).toBe("setting");
    expect(docSubject("bible", 0)).toBe("bible");
    expect(docSubject("chapter", 3)).toBe("chapter:3");
    expect(scriptSubject(12)).toBe("script:12");
    expect(threadPath("wenjian", "chapter:3")).toBe("/admin/video-automation/series/wenjian/messages?subject=chapter%3A3");
  });

  it("shows every line with its author, its version and its time, and posts the owner's line to the same subject", async () => {
    const calls = stubFetch();
    const onMessagesLoaded = vi.fn();
    render(<DiscussionThread seriesSlug="wenjian" subject="script:1" canManage onMessagesLoaded={onMessagesLoaded} />);
    const thread = await screen.findByRole("region", { name: "討論" });
    await waitFor(() => expect(thread.textContent).toContain("開場的鐘聲太早。"));
    expect(onMessagesLoaded).toHaveBeenCalledWith(lines);
    expect(calls[0].url).toBe("/api/travel/admin/video-automation/series/wenjian/messages?subject=script%3A1");
    expect(thread.textContent).toContain("站主");
    expect(thread.textContent).toContain("撰稿");
    expect(thread.textContent).toContain("對劇本 1a2b3c4d5e6f");
    expect(thread.textContent).toContain("對劇本 6f5e4d3c2b1a");
    expect(thread.textContent).toContain("把鐘聲移到沈瀾開口之後了。");
    expect(screen.queryByText("等模型回覆")).toBeNull();

    const send = screen.getByRole("button", { name: "送出" });
    expect(send).toHaveProperty("disabled", true);
    fireEvent.change(screen.getByRole("textbox", { name: "給模型的話" }), { target: { value: "  多給我兩個開場。  " } });
    expect(send).toHaveProperty("disabled", false);
    fireEvent.click(send);
    await waitFor(() => expect(calls.some((call) => call.method === "POST")).toBe(true));
    const post = calls.find((call) => call.method === "POST");
    expect(post?.url).toBe("/api/travel/admin/video-automation/series/wenjian/messages");
    expect(post?.body).toEqual({ subject: "script:1", body: "多給我兩個開場。" });
    await waitFor(() => expect(thread.textContent).toContain("多給我兩個開場。"));
    expect(screen.getAllByText("等模型回覆")).toHaveLength(2);
    expect((screen.getByRole("textbox", { name: "給模型的話" }) as HTMLTextAreaElement).value).toBe("");
  });

  it("says the thread waits when the parent already knows, and shows the API's reason when a line is refused", async () => {
    stubFetch({ status: 409, code: "video_drama_script_approved", detail: "劇本已經核准，這條討論串只留紀錄" });
    const onPosted = vi.fn();
    render(<DiscussionThread seriesSlug="wenjian" subject="script:1" canManage waiting onPosted={onPosted} />);
    const thread = await screen.findByRole("region", { name: "討論" });
    expect(screen.getByText("等模型回覆")).toBeTruthy();
    await waitFor(() => expect(thread.textContent).toContain("開場的鐘聲太早。"));
    fireEvent.change(screen.getByRole("textbox", { name: "給模型的話" }), { target: { value: "再改一次" } });
    fireEvent.click(screen.getByRole("button", { name: "送出" }));
    expect((await screen.findByRole("alert")).textContent).toBe("沒有送出：劇本已經核准，這條討論串只留紀錄");
    expect(onPosted).not.toHaveBeenCalled();
    expect((screen.getByRole("textbox", { name: "給模型的話" }) as HTMLTextAreaElement).value).toBe("再改一次");
  });

  it("keeps the owner's line from the server's answer when the thread cannot be read back after posting", async () => {
    let posted = false;
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      if (init?.method === "POST") {
        posted = true;
        const body = JSON.parse(String(init.body)) as { subject: string; body: string };
        return Promise.resolve(Response.json({ id: "m3", subject: body.subject, author: "owner", body_md: body.body, refers_to: "6f5e4d3c2b1a", answered_at: null, created_at: "2026-09-27T05:20:00Z", created_by_user_id: "u1" }, { status: 201 }));
      }
      if (posted) return Promise.resolve(Response.json({ type: "about:blank", title: "Internal Server Error", status: 500, detail: "database away" }, { status: 500 }));
      return Promise.resolve(Response.json({ messages: lines }));
    }));
    render(<DiscussionThread seriesSlug="wenjian" subject="script:1" canManage />);
    const thread = await screen.findByRole("region", { name: "討論" });
    await waitFor(() => expect(thread.textContent).toContain("開場的鐘聲太早。"));
    fireEvent.change(screen.getByRole("textbox", { name: "給模型的話" }), { target: { value: "結尾再加一句旁白" } });
    fireEvent.click(screen.getByRole("button", { name: "送出" }));
    // The 201 body is appended after the lines already read; the failed re-read is not an error.
    await waitFor(() => expect(thread.textContent).toContain("結尾再加一句旁白"));
    expect(thread.textContent).toContain("開場的鐘聲太早。");
    expect(thread.textContent).toContain("把鐘聲移到沈瀾開口之後了。");
    expect(screen.getAllByText("等模型回覆")).toHaveLength(2);
    expect((screen.getByRole("textbox", { name: "給模型的話" }) as HTMLTextAreaElement).value).toBe("");
    expect(screen.queryByRole("alert")).toBeNull();
  });

  it("keeps an approved thread as a record, hides the input from a reader, and shows nothing for an empty closed thread", async () => {
    stubFetch();
    const closed = render(<DiscussionThread seriesSlug="wenjian" subject="script:1" canManage readOnly />);
    const record = await screen.findByRole("region", { name: "討論" });
    await waitFor(() => expect(record.textContent).toContain("開場的鐘聲太早。"));
    expect(record.textContent).toContain("只留紀錄");
    expect(screen.queryByRole("textbox")).toBeNull();
    closed.unmount();

    const reader = render(<DiscussionThread seriesSlug="wenjian" subject="script:1" canManage={false} />);
    await waitFor(() => expect(screen.getByRole("region", { name: "討論" }).textContent).toContain("開場的鐘聲太早。"));
    expect(screen.queryByRole("textbox")).toBeNull();
    expect(screen.queryByText("只留紀錄")).toBeNull();
    reader.unmount();

    vi.stubGlobal("fetch", vi.fn(() => Promise.resolve(Response.json({ messages: [] }))));
    const { container } = render(<DiscussionThread seriesSlug="wenjian" subject="bible" canManage readOnly />);
    await waitFor(() => expect(fetch).toHaveBeenCalled());
    expect(container.textContent).toBe("");
  });
});
