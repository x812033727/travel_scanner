import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminDeploymentsPanel } from "./admin-deployments-panel";

const sha = "b".repeat(40);
const run = { id: "run-1", requested_by_email: "deploy@example.com", status: "queued", stage: "queued", target_sha: sha, created_at: "2026-09-01T00:00:00Z", updated_at: "2026-09-01T00:00:00Z", events: [] };
const overview = { enabled: true, agent_connected: true, deployed_sha: "a".repeat(40), target_sha: sha, target_commit_subject: "Add deployment center", update_available: true, ci_status: "success", ci_url: "https://github.com/x812033727/travel_scanner/actions/runs/1", commits: [{ sha, subject: "Add deployment center" }], checks: [{ name: "docker", status: "ok", detail: "可用" }] };

function response(value: unknown, status = 200) {
  return Promise.resolve(new Response(JSON.stringify(value), { status, headers: { "Content-Type": "application/json" } }));
}

afterEach(() => vi.unstubAllGlobals());

describe("AdminDeploymentsPanel", () => {
  it("labels the release guard check and shows why the agent refuses", async () => {
    const held = { ...overview, checks: [{ name: "release_guard", status: "failed", detail: "codex-release 正在發布 cccccccccccc" }] };
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL) => {
      const url = String(input);
      if (url.endsWith("/admin/deployments/overview")) return response(held);
      if (url.includes("/admin/deployments?")) return response({ items: [] });
      throw new Error(`unexpected ${url}`);
    }));
    render(<AdminDeploymentsPanel />);
    expect(await screen.findByText("其他發布")).toBeTruthy();
    expect(screen.getByText("codex-release 正在發布 cccccccccccc")).toBeTruthy();
    expect(screen.queryByText("release_guard")).toBeNull();
  });

  it("shows the green target and requires password plus exact SHA confirmation", async () => {
    const fetchMock = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.endsWith("/admin/deployments/overview")) return response(overview);
      if (url.includes("/admin/deployments?")) return response({ items: [] });
      if (url.endsWith("/admin/deployments") && init?.method === "POST") return response(run, 202);
      throw new Error(`unexpected ${url}`);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminDeploymentsPanel />);
    const deploy = await screen.findByRole("button", { name: "部署最新版本" });
    expect(screen.getAllByText("bbbbbbb").length).toBeGreaterThan(0);
    fireEvent.click(deploy);
    const submit = screen.getByRole("button", { name: "確認並開始部署" });
    expect((submit as HTMLButtonElement).disabled).toBe(true);
    fireEvent.change(screen.getByLabelText("目前密碼"), { target: { value: "correct password" } });
    fireEvent.change(screen.getByLabelText(/輸入 DEPLOY/), { target: { value: "DEPLOY bbbbbbb" } });
    expect((submit as HTMLButtonElement).disabled).toBe(false);
    fireEvent.click(submit);
    await waitFor(() => expect(fetchMock).toHaveBeenCalledWith(
      "/api/travel/admin/deployments",
      expect.objectContaining({ method: "POST", headers: expect.objectContaining({ "Idempotency-Key": expect.stringMatching(/^deploy-/) }) }),
    ));
    const post = fetchMock.mock.calls.find(([, init]) => init?.method === "POST");
    expect(JSON.parse(String(post?.[1]?.body))).toEqual({ expected_target_sha: sha, password: "correct password", confirmation: "DEPLOY bbbbbbb" });
  });

  it("explains why deploy is disabled", async () => {
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL) => String(input).includes("overview") ? response({ ...overview, update_available: false, target_sha: overview.deployed_sha }) : response({ items: [] })));
    render(<AdminDeploymentsPanel />);
    expect(await screen.findByText("目前已是最新綠燈版本")).toBeTruthy();
    expect((screen.getByRole("button", { name: "部署最新版本" }) as HTMLButtonElement).disabled).toBe(true);
  });
  const live = "a".repeat(40);
  const host = { reported_at: "2026-11-16T01:00:00Z", responding: true, dry_run: false, deploy_windows: ["04:30-06:00"], auto_deploys_today: 1, last_decision: { action: "wait", gate: "schedule", reason: "outside the deploy window" }, last_deploy: { sha: live, verify: "PASS" }, last_missed_window: { window: "04:30-06:00", gate: "ci", reason: "CI red", sha } };
  const hostOverview = { ...overview, executor: "host_timer", ci_status: "unknown", checks: [{ name: "host_timer", status: "ok", detail: "主機自動部署排程器正常回報" }], host };

  it("shows the host timer and deploys latest with an unknown CI result", async () => {
    const fetchMock = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.endsWith("/admin/deployments/overview")) return response(hostOverview);
      if (url.includes("/admin/deployments?")) return response({ items: [] });
      if (url.endsWith("/admin/deployments") && init?.method === "POST") return response(run, 202);
      throw new Error(`unexpected ${url}`);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminDeploymentsPanel />);
    const deploy = await screen.findByRole("button", { name: "部署最新版本" });
    expect(screen.getByRole("region", { name: "主機自動部署排程器" })).toBeTruthy();
    expect(screen.getByText("主機部署排程器")).toBeTruthy();
    expect(screen.getByText("04:30-06:00")).toBeTruthy();
    expect(screen.getByText("aaaaaaa・驗證 PASS")).toBeTruthy();
    expect(screen.getByText("04:30-06:00：bbbbbbb 卡在 ci：CI red")).toBeTruthy();
    expect((deploy as HTMLButtonElement).disabled).toBe(false);
    fireEvent.click(deploy);
    expect(screen.getByText(/部署腳本只在 migration 有變動時備份/)).toBeTruthy();
    fireEvent.click(screen.getByLabelText(/有付費影片工作在執行時先不要部署/));
    fireEvent.change(screen.getByLabelText("目前密碼"), { target: { value: "pw" } });
    fireEvent.change(screen.getByLabelText(/輸入 DEPLOY/), { target: { value: "DEPLOY bbbbbbb" } });
    fireEvent.click(screen.getByRole("button", { name: "確認並開始部署" }));
    await waitFor(() => expect(fetchMock.mock.calls.some(([, init]) => init?.method === "POST")).toBe(true));
    const post = fetchMock.mock.calls.find(([, init]) => init?.method === "POST");
    expect(JSON.parse(String(post?.[1]?.body))).toEqual({ expected_target_sha: sha, password: "pw", confirmation: "DEPLOY bbbbbbb", mode: "latest", wait_for_paid_work: false });
  });

  it("rebuilds the live commit", async () => {
    const fetchMock = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.endsWith("/admin/deployments/overview")) return response({ ...hostOverview, target_sha: live, update_available: false });
      if (url.includes("/admin/deployments?")) return response({ items: [] });
      if (init?.method === "POST") return response({ ...run, target_sha: live }, 202);
      throw new Error(`unexpected ${url}`);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminDeploymentsPanel />);
    const rebuild = await screen.findByRole("button", { name: "重建目前版本" });
    expect((screen.getByRole("button", { name: "部署最新版本" }) as HTMLButtonElement).disabled).toBe(true);
    fireEvent.click(rebuild);
    expect(screen.getByRole("dialog", { name: "確認重建 aaaaaaa" })).toBeTruthy();
    fireEvent.change(screen.getByLabelText("目前密碼"), { target: { value: "pw" } });
    fireEvent.change(screen.getByLabelText(/輸入 DEPLOY/), { target: { value: "DEPLOY aaaaaaa" } });
    fireEvent.click(screen.getByRole("button", { name: "確認並開始部署" }));
    await waitFor(() => expect(fetchMock.mock.calls.some(([, init]) => init?.method === "POST")).toBe(true));
    const post = fetchMock.mock.calls.find(([, init]) => init?.method === "POST");
    expect(JSON.parse(String(post?.[1]?.body))).toMatchObject({ expected_target_sha: live, mode: "rebuild", wait_for_paid_work: true });
  });

  it("blocks both buttons while automatic deploys are paused or the timer is silent", async () => {
    const paused = { ...hostOverview, host: { ...host, paused_reason: "deploy of bbbbbbbbbbbb exited 1" } };
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL) => String(input).includes("overview") ? response(paused) : response({ items: [] })));
    const { unmount } = render(<AdminDeploymentsPanel />);
    expect(await screen.findByText(/上一次自動部署失敗、已暫停/)).toBeTruthy();
    expect(screen.getByRole("alert").textContent).toContain("exited 1");
    expect((screen.getByRole("button", { name: "部署最新版本" }) as HTMLButtonElement).disabled).toBe(true);
    expect((screen.getByRole("button", { name: "重建目前版本" }) as HTMLButtonElement).disabled).toBe(true);
    unmount();
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL) => String(input).includes("overview") ? response({ ...hostOverview, agent_connected: false }) : response({ items: [] })));
    render(<AdminDeploymentsPanel />);
    expect(await screen.findByText("主機部署排程器超過 15 分鐘沒有回報")).toBeTruthy();
  });

  it("closes the confirmation with Escape from anywhere and traps Tab inside it", async () => {
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL) =>
      String(input).endsWith("/admin/deployments/overview") ? response(overview) : response({ items: [] })));
    render(<AdminDeploymentsPanel />);
    const deploy = await screen.findByRole("button", { name: "部署最新版本" });
    deploy.focus();
    fireEvent.click(deploy);

    const confirm = screen.getByRole("dialog", { name: /部署/ });
    expect(document.activeElement).toBe(screen.getByLabelText("目前密碼"));
    expect(document.body.style.overflow).toBe("hidden");

    // Tab must not walk out into the deployment history behind the scrim.
    const close = screen.getByRole("button", { name: "關閉部署確認" });
    close.focus();
    fireEvent.keyDown(close, { key: "Tab", shiftKey: true });
    expect(confirm.contains(document.activeElement)).toBe(true);

    // Escape was bound to the form, so it did nothing whenever focus was not inside it —
    // which is where focus lands after a click on the scrim.
    document.body.focus();
    fireEvent.keyDown(document.body, { key: "Escape" });
    await waitFor(() => expect(screen.queryByRole("dialog", { name: /部署/ })).toBeNull());
    expect(document.body.style.overflow).toBe("");
    expect(document.activeElement).toBe(deploy);
  });
});
