import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { VideoToolTokens } from "./video-tool-tokens";

const ENDPOINT = "/api/travel/admin/provider-settings/azure_speech/video-tool-tokens";
const existing = {
  id: "5f0f3b2e-0000-4000-8000-000000000001",
  name: "筆電",
  token_prefix: "mkv_abcdef",
  created_at: "2026-09-24T03:00:00Z",
  last_used_at: null,
  revoked_at: null,
};

function json(value: unknown, status = 200) {
  return Promise.resolve(new Response(JSON.stringify(value), { status, headers: { "Content-Type": "application/json" } }));
}

describe("VideoToolTokens", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("lists tokens by prefix only and shows a new token once", async () => {
    const secret = `mkv_${"z".repeat(43)}`;
    let list = [existing];
    const fetchMock = vi.fn((url: string, init?: RequestInit) => {
      expect(url).toContain(ENDPOINT);
      if (init?.method === "POST") {
        expect(JSON.parse(String(init.body))).toEqual({ name: "工作站" });
        const created = { ...existing, id: "5f0f3b2e-0000-4000-8000-000000000002", name: "工作站", token_prefix: secret.slice(0, 10) };
        list = [created, existing];
        return json({ ...created, token: secret }, 201);
      }
      return json(list);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<VideoToolTokens canManage />);
    expect(await screen.findByText("筆電")).toBeTruthy();
    expect(screen.queryByTestId("new-video-tool-token")).toBeNull();

    fireEvent.change(screen.getByRole("textbox"), { target: { value: "工作站" } });
    fireEvent.submit(screen.getByRole("textbox").closest("form")!);
    expect((await screen.findByTestId("new-video-tool-token")).textContent).toBe(secret);
    await waitFor(() => expect(screen.getByText("工作站")).toBeTruthy());

    fireEvent.click(screen.getByRole("button", { name: /我已經存好了|dismiss/i }));
    expect(screen.queryByTestId("new-video-tool-token")).toBeNull();
    expect(document.body.textContent).not.toContain(secret);
  });

  it("asks for a second click before revoking", async () => {
    const calls: string[] = [];
    vi.stubGlobal("fetch", vi.fn((url: string, init?: RequestInit) => {
      calls.push(`${init?.method ?? "GET"} ${url}`);
      if (init?.method === "DELETE") return json({ ...existing, revoked_at: "2026-09-24T04:00:00Z" });
      return json(calls.some((call) => call.startsWith("DELETE")) ? [{ ...existing, revoked_at: "2026-09-24T04:00:00Z" }] : [existing]);
    }));
    render(<VideoToolTokens canManage />);
    fireEvent.click(await screen.findByRole("button", { name: /撤銷|revoke/i }));
    expect(calls.some((call) => call.startsWith("DELETE"))).toBe(false);
    fireEvent.click(screen.getByRole("button", { name: /確定撤銷|confirm/i }));
    await waitFor(() => expect(calls).toContain(`DELETE ${ENDPOINT}/${existing.id}`));
    expect(await screen.findByText(/已撤銷|revoked/i)).toBeTruthy();
  });

  it("hides the create form and revoke buttons without the manage capability", async () => {
    vi.stubGlobal("fetch", vi.fn(() => json([existing])));
    render(<VideoToolTokens canManage={false} />);
    expect(await screen.findByText("筆電")).toBeTruthy();
    expect(screen.queryByRole("textbox")).toBeNull();
    expect(screen.queryByRole("button", { name: /撤銷|revoke/i })).toBeNull();
  });
});
