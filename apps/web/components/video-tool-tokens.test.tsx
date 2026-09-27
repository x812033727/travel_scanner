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

    fireEvent.change(screen.getByLabelText("名稱"), { target: { value: "工作站" } });
    fireEvent.submit(screen.getByLabelText("名稱").closest("form")!);
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

describe("VideoToolTokens pairing", () => {
  const pending = {
    user_code: "BCDF-GHJK",
    client_name: "工作室筆電",
    client_ip: "203.0.113.9",
    created_at: "2026-09-24T05:00:00Z",
    expires_at: "2026-09-24T05:10:00Z",
    status: "pending",
  };

  afterEach(() => {
    vi.unstubAllGlobals();
    window.history.replaceState(null, "", "/");
  });

  it("opens the pairing from the link login prints, and allows it only on a click", async () => {
    window.history.replaceState(null, "", "/zh-TW/admin/settings?provider=azure_speech&video_pairing=BCDFGHJK");
    const calls: string[] = [];
    vi.stubGlobal("fetch", vi.fn((url: string, init?: RequestInit) => {
      calls.push(`${init?.method ?? "GET"} ${url}`);
      if (url.endsWith("/pairings/BCDFGHJK")) return json(pending);
      if (url.endsWith("/pairings/BCDFGHJK/approve")) return json({ ...pending, status: "approved" });
      return json([existing]);
    }));
    render(<VideoToolTokens canManage />);
    const card = await screen.findByTestId("video-tool-pairing");
    expect(card.textContent).toContain("BCDF-GHJK");
    expect(card.textContent).toContain("工作室筆電");
    expect(card.textContent).toContain("203.0.113.9");
    expect((screen.getByLabelText("驗證碼") as HTMLInputElement).value).toBe("BCDFGHJK");
    expect(screen.getByText(/只允許你自己剛剛在終端機上看到的驗證碼/)).toBeTruthy();
    expect(calls.some((call) => call.startsWith("POST"))).toBe(false);

    fireEvent.click(screen.getByRole("button", { name: "允許" }));
    expect(await screen.findByText(/已允許/)).toBeTruthy();
    expect(calls).toContain(`POST ${ENDPOINT}/pairings/BCDFGHJK/approve`);
    expect(screen.queryByRole("button", { name: "允許" })).toBeNull();
  });

  it("looks up a typed code and can deny it", async () => {
    const calls: string[] = [];
    vi.stubGlobal("fetch", vi.fn((url: string, init?: RequestInit) => {
      calls.push(`${init?.method ?? "GET"} ${url}`);
      if (url.endsWith("/pairings/BCDFGHJK")) return json(pending);
      if (url.endsWith("/pairings/BCDFGHJK/deny")) return json({ ...pending, status: "denied" });
      return json([existing]);
    }));
    render(<VideoToolTokens canManage />);
    await screen.findByText("筆電");
    fireEvent.change(screen.getByLabelText("驗證碼"), { target: { value: "bcdf-ghjk" } });
    fireEvent.click(screen.getByRole("button", { name: "查詢" }));
    await screen.findByTestId("video-tool-pairing");
    fireEvent.click(screen.getByRole("button", { name: "拒絕" }));
    expect(await screen.findByText(/已拒絕/)).toBeTruthy();
    expect(calls).toContain(`POST ${ENDPOINT}/pairings/BCDFGHJK/deny`);
    expect(calls.some((call) => call.endsWith("/approve"))).toBe(false);
  });

  it("explains a malformed code without asking the server, and shows the server's refusal", async () => {
    const fetchMock = vi.fn((url: string) => {
      if (url.includes("/pairings/")) return json({ title: "請求未完成", status: 404, code: "video_pairing_not_found", detail: "找不到這組驗證碼" }, 404);
      return json([existing]);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<VideoToolTokens canManage />);
    await screen.findByText("筆電");
    fireEvent.change(screen.getByLabelText("驗證碼"), { target: { value: "ABC" } });
    fireEvent.click(screen.getByRole("button", { name: "查詢" }));
    expect((await screen.findByRole("alert")).textContent).toContain("8 個英文字母");
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/pairings/"))).toBe(false);

    fireEvent.change(screen.getByLabelText("驗證碼"), { target: { value: "BCDF-GHJK" } });
    fireEvent.click(screen.getByRole("button", { name: "查詢" }));
    await waitFor(() => expect(screen.getByRole("alert").textContent).toContain("找不到這組驗證碼"));
    expect(screen.queryByTestId("video-tool-pairing")).toBeNull();
  });

  it("offers no pairing to an admin who cannot manage settings, even from the link", async () => {
    window.history.replaceState(null, "", "/zh-TW/admin/settings?video_pairing=BCDFGHJK");
    const fetchMock = vi.fn<(url: string) => Promise<Response>>(() => json([existing]));
    vi.stubGlobal("fetch", fetchMock);
    render(<VideoToolTokens canManage={false} />);
    await screen.findByText("筆電");
    expect(screen.queryByLabelText("驗證碼")).toBeNull();
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes("/pairings/"))).toBe(false);
  });
});
