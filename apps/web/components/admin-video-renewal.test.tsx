import { createHash, webcrypto } from "node:crypto";
import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminVideoRenewal, renewalCandidate } from "./admin-video-renewal";
import type { Project, Review } from "./admin-video-review-card";

const oldSha = "a".repeat(64), newSha = "b".repeat(64), brand = "c".repeat(64);
const oldId = "11111111-1111-4111-8111-111111111111", newId = "22222222-2222-4222-8222-222222222222";
const old: Review = { id: oldId, gate: "final", content_sha256: oldSha, status: "approved", subject: null, summary: "Original", files: [], payload: {}, created_at: "2026-10-01T00:00:00Z", decided_at: "2026-10-01T01:00:00Z", choice: null, note: null };
const project: Project = { slug: "video-one", title: "Video one", stage: "on YouTube", checklist: [{ key: "on_youtube", label: "Next", done: false }], youtube_video_id: null, last_synced_at: "2026-10-01T00:00:00Z", pending: 0, format: "slides", reviews: [old] };
const candidate = () => ({ schema_version: 1, kind: "long-final-renewal", slug: project.slug, site: window.location.origin, source: { final_review_id: oldId, final_sha256: oldSha, body_sha256: "d".repeat(64) }, candidate: { final_sha256: newSha, branding_hash: brand, final_bytes: 20 }, review: { gate: "final", content_sha256: newSha, summary: "New cut with CC reminder", payload: { manual_review: true, branding_hash: brand, duration_seconds: 38 }, files: [{ role: "final", sha256: newSha, size: 20, content_type: "video/mp4" }, { role: "preview", sha256: "e".repeat(64), size: 7, content_type: "video/mp4" }] } });
const state = { version: "f".repeat(64), final_review_id: oldId, final_sha256: oldSha };
const replacement = () => ({ ...old, ...candidate().review, id: newId, status: "pending" as const });
async function select(value = candidate()) {
  fireEvent.change(screen.getByLabelText("候選收據（.json）"), { target: { files: [new File([JSON.stringify(value)], "renewal-candidate.json", { type: "application/json" })] } });
  await screen.findByText("New cut with CC reminder");
  await waitFor(() => expect(screen.getByRole("button", { name: "核對目前審核" })).toHaveProperty("disabled", false));
}
afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks(); });

describe("owner final renewal", () => {
  it("does not offer mutation to readers, Shorts or videos with upload activity", () => {
    const { rerender } = render(<AdminVideoRenewal project={project} canManage={false} onSubmitted={vi.fn()} />);
    expect(screen.queryByRole("region")).toBeNull();
    for (const changed of [{ format: "shorts" as const }, { youtube_video_id: "abcdefghijk" }, { youtube_publish_at: "2026-10-02T00:00:00Z" }, { youtube_removed_at: "2026-10-01T00:00:00Z" }]) {
      rerender(<AdminVideoRenewal project={{ ...project, ...changed }} canManage onSubmitted={vi.fn()} />);
      expect(screen.queryByRole("region")).toBeNull();
    }
  });

  it("selects locally, reads fresh versions, then verifies persisted manual pending", async () => {
    const submitted = vi.fn();
    const fetchMock = vi.fn((url: string, init?: RequestInit) => Promise.resolve(Response.json(
      init?.method === "POST" ? replacement() : url.endsWith("final-renewal") ? state : { ...project, reviews: [replacement(), { ...old, status: "superseded" }] },
    )));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminVideoRenewal project={project} canManage onSubmitted={submitted} />);
    await select();
    expect(fetchMock).not.toHaveBeenCalled();
    expect(screen.getByText("新版片長：38.0 秒")).toBeTruthy();
    const button = screen.getByRole("button", { name: "送出新版，交由我審看" });
    expect(button).toHaveProperty("disabled", true);
    fireEvent.change(screen.getByLabelText("換版原因"), { target: { value: "CC reminder introduction" } });
    fireEvent.click(screen.getByRole("button", { name: "核對目前審核" }));
    await screen.findByText("原成片符合。目前版本會在送出前再次核對。");
    fireEvent.click(button);
    await screen.findByText("新版已送出，等待人工審看。先前決策與附件保留在歷史記錄。");
    expect(fetchMock.mock.calls.map(([, init]) => init?.method ?? "GET")).toEqual(["GET", "GET", "POST", "GET"]);
    const payload = JSON.parse(String(fetchMock.mock.calls[2][1]?.body));
    expect(payload.expected_version).toBe(state.version);
    expect(payload.expected_final_review_id).toBe(oldId);
    expect(payload.expected_final_sha256).toBe(oldSha);
    expect(payload.review.content_sha256).toBe(newSha);
    expect(submitted).toHaveBeenCalledTimes(1);
  });

  it("preserves the receipt and reason when the version changes before submit, sending no POST", async () => {
    let count = 0;
    const fetchMock = vi.fn(() => Promise.resolve(Response.json({ ...state, version: count++ ? "9".repeat(64) : state.version })));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminVideoRenewal project={project} canManage onSubmitted={vi.fn()} />);
    await select();
    fireEvent.change(screen.getByLabelText("換版原因"), { target: { value: "Keep my reason" } });
    fireEvent.click(screen.getByRole("button", { name: "核對目前審核" }));
    await screen.findByText("原成片符合。目前版本會在送出前再次核對。");
    fireEvent.click(screen.getByRole("button", { name: "送出新版，交由我審看" }));
    await screen.findByRole("alert");
    expect(fetchMock).toHaveBeenCalledTimes(2);
    expect(screen.getByLabelText("換版原因")).toHaveProperty("value", "Keep my reason");
    expect(screen.getByRole("button", { name: "送出新版，交由我審看" })).toHaveProperty("disabled", true);
  });

  it("does not call a 201 without read-back proof completed, and never retries an ambiguous POST", async () => {
    const submitted = vi.fn();
    const fetchMock = vi.fn((url: string, init?: RequestInit) => Promise.resolve(Response.json(init?.method === "POST" ? replacement() : url.endsWith("final-renewal") ? state : project)));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminVideoRenewal project={project} canManage onSubmitted={submitted} />);
    await select();
    fireEvent.change(screen.getByLabelText("換版原因"), { target: { value: "New intro" } });
    fireEvent.click(screen.getByRole("button", { name: "核對目前審核" }));
    await screen.findByText("原成片符合。目前版本會在送出前再次核對。");
    fireEvent.click(screen.getByRole("button", { name: "送出新版，交由我審看" }));
    expect((await screen.findByRole("alert")).textContent).toContain("送出結果尚未確認");
    expect(fetchMock.mock.calls.filter(([, init]) => init?.method === "POST")).toHaveLength(1);
    expect(submitted).not.toHaveBeenCalled();
    expect(screen.getByRole("button", { name: "送出新版，交由我審看" })).toHaveProperty("disabled", true);
  });

  it("refuses foreign-site/slug, reused hashes, duplicate roles and forged server history", () => {
    const valid = candidate();
    expect(renewalCandidate(valid, project.slug, window.location.origin)).not.toBeNull();
    for (const changed of [
      { ...valid, site: "https://other.example" }, { ...valid, slug: "another" },
      { ...valid, source: { ...valid.source, final_sha256: newSha } },
      { ...valid, review: { ...valid.review, files: [...valid.review.files, valid.review.files[0]] } },
      { ...valid, review: { ...valid.review, payload: { ...valid.review.payload, _final_renewal: {} } } },
    ]) expect(renewalCandidate(changed, project.slug, window.location.origin)).toBeNull();
  });

  it("rejects an unrelated local preview without ever uploading the file", async () => {
    const fetchMock = vi.fn(); vi.stubGlobal("fetch", fetchMock);
    render(<AdminVideoRenewal project={project} canManage onSubmitted={vi.fn()} />);
    await select();
    fireEvent.change(screen.getByLabelText("可選取本機 preview.mp4（須與收據一致）"), { target: { files: [new File(["wrong"], "preview.mp4", { type: "video/mp4" })] } });
    expect((await screen.findByRole("alert")).textContent).toContain("預覽檔與收據不符");
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("plays only matching preview bytes locally and revokes the object URL on unmount", async () => {
    const fetchMock = vi.fn(); vi.stubGlobal("fetch", fetchMock);
    const create = vi.fn(() => "blob:verified-preview"), revoke = vi.fn();
    vi.stubGlobal("URL", { createObjectURL: create, revokeObjectURL: revoke });
    vi.stubGlobal("crypto", { subtle: { digest: (algorithm: string, bytes: ArrayBuffer) => webcrypto.subtle.digest(algorithm, new Uint8Array(bytes)) } });
    const receipt = candidate(); receipt.review.files[1].sha256 = createHash("sha256").update("preview").digest("hex");
    const view = render(<AdminVideoRenewal project={project} canManage onSubmitted={vi.fn()} />);
    await select(receipt);
    fireEvent.change(screen.getByLabelText("可選取本機 preview.mp4（須與收據一致）"), { target: { files: [new File(["preview"], "preview.mp4", { type: "video/mp4" })] } });
    await waitFor(() => expect(create).toHaveBeenCalledTimes(1));
    expect(view.container.querySelector("video")?.getAttribute("src")).toBe("blob:verified-preview");
    view.unmount();
    expect(revoke).toHaveBeenCalledWith("blob:verified-preview");
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("does not allocate a preview URL when hashing completes after the owner navigates away", async () => {
    let finish!: (bytes: ArrayBuffer) => void;
    const digest = vi.fn(() => new Promise<ArrayBuffer>((resolve) => { finish = resolve; }));
    const create = vi.fn(), revoke = vi.fn();
    vi.stubGlobal("crypto", { subtle: { digest } });
    vi.stubGlobal("URL", { createObjectURL: create, revokeObjectURL: revoke });
    const view = render(<AdminVideoRenewal project={project} canManage onSubmitted={vi.fn()} />);
    await select();
    fireEvent.change(screen.getByLabelText("可選取本機 preview.mp4（須與收據一致）"), { target: { files: [new File(["preview"], "preview.mp4", { type: "video/mp4" })] } });
    await waitFor(() => expect(digest).toHaveBeenCalledTimes(1));
    view.unmount();
    await act(async () => { finish(new Uint8Array(32).fill(238).buffer); });
    expect(create).not.toHaveBeenCalled();
    expect(revoke).not.toHaveBeenCalled();
  });
});
