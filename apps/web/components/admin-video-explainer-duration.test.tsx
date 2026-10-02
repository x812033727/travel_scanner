import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { AdminBootstrap } from "@/lib/admin-operations";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { AdminVideoSeries } from "./admin-video-series";

vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: null, sessionIdentity: null, status: undefined }) }));

function openForm() {
  const posts: Record<string, unknown>[] = [];
  vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith("/drama-requests") && init?.method === "POST") {
      posts.push(JSON.parse(String(init.body)) as Record<string, unknown>);
      return Promise.resolve(Response.json({ series_slug: null }));
    }
    if (url.endsWith("/drama-requests")) return Promise.resolve(Response.json({ requests: [] }));
    if (url.includes("/series?")) return Promise.resolve(Response.json({ series: [] }));
    if (url.includes("/series/binge-quote")) return Promise.resolve(Response.json({ episodes: 40, chapters: 4, episodes_per_chapter: 10, clip_seconds: 0, images: 10, judge_calls: 10, usd: 1, budgets: {}, ok: true }));
    if (url.endsWith("/settings")) return Promise.resolve(Response.json({ detail: "Not in this fixture" }, { status: 503 }));
    return Promise.resolve(Response.json([]));
  }));
  const bootstrap: AdminBootstrap = { admin_roles: [], admin_capabilities: ["content.read", "content.manage"], navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false };
  render(<AdminOperationsProvider bootstrap={bootstrap}><AdminVideoSeries onOpenVideo={() => undefined} /></AdminOperationsProvider>);
  fireEvent.click(screen.getByText("新的漫劇", { selector: "summary" }));
  const form = within(screen.getByRole("form", { name: "新的漫劇" }));
  fireEvent.change(form.getByRole("textbox", { name: "故事前提（必填）" }), { target: { value: "為什麼雷聲比閃電晚？" } });
  return { form, posts };
}

afterEach(() => {
  vi.unstubAllGlobals();
  window.history.replaceState(null, "", "/");
});

describe("explainer duration input", () => {
  it("changes the default and bounds only when crossing the explainer style", () => {
    const { form } = openForm();
    const style = form.getByRole("combobox", { name: "風格" });
    const minutes = form.getByRole("spinbutton") as HTMLInputElement;
    expect([minutes.value, minutes.min, minutes.max]).toEqual(["3", "1", "8"]);
    fireEvent.change(style, { target: { value: "flat-explainer" } });
    expect([minutes.value, minutes.min, minutes.max]).toEqual(["10", "8", "20"]);
    expect(form.getByLabelText("8–20 分鐘")).toBe(minutes);
    fireEvent.change(style, { target: { value: "anime-2d" } });
    expect([minutes.value, minutes.min, minutes.max]).toEqual(["3", "1", "8"]);
    fireEvent.change(minutes, { target: { value: "5" } });
    fireEvent.change(style, { target: { value: "ink-wash" } });
    expect(minutes.value).toBe("5");
  });

  it.each([8, 10, 20])("files an explainer with %i minutes", async (target) => {
    const { form, posts } = openForm();
    fireEvent.change(form.getByRole("combobox", { name: "風格" }), { target: { value: "flat-explainer" } });
    fireEvent.change(form.getByRole("spinbutton"), { target: { value: String(target) } });
    fireEvent.click(form.getByRole("button", { name: "排進製作" }));
    await waitFor(() => expect(posts).toHaveLength(1));
    expect(posts[0]).toMatchObject({ style_preset: "flat-explainer", target_minutes: target });
  });

  it.each([7, 21, 8.5])("refuses an explainer with %s minutes", (target) => {
    const { form, posts } = openForm();
    fireEvent.change(form.getByRole("combobox", { name: "風格" }), { target: { value: "flat-explainer" } });
    fireEvent.change(form.getByRole("spinbutton"), { target: { value: String(target) } });
    expect(form.getByRole("button", { name: "排進製作" })).toHaveProperty("disabled", true);
    expect(posts).toHaveLength(0);
  });

  it("continues to refuse a nine-minute drama", () => {
    const { form } = openForm();
    fireEvent.change(form.getByRole("spinbutton"), { target: { value: "9" } });
    expect(form.getByRole("button", { name: "排進製作" })).toHaveProperty("disabled", true);
  });
});
