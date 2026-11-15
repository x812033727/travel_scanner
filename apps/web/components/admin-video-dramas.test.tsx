import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { DramaDocument, DramaEpisodeDetail, DramaIndex } from "./admin-video-dramas";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { AdminVideoReviews } from "./admin-video-reviews";
import { api } from "@/lib/api";
import { videoDramasCopy } from "@/lib/video-dramas-copy";

vi.mock("@/lib/api", () => ({ api: vi.fn() }));
vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: null, sessionIdentity: null, status: undefined }) }));
const copy = videoDramasCopy("zh-TW");
const index: DramaIndex = { schema_version: 1, status: "AUTHORED_TEXT_NOT_PRODUCTION_STATE", series: [
  { key: "tai-nainai", name: "恁祖媽今年18", content_sha256: "a".repeat(64), counts: { episodes: 2, brief: 2, script: 2, storyboard: 0, review: 0 },
    episodes: [
      { slug: "tai-nainai-e001", number: 1, variant: null, title: "燈下閉眼｜恁祖媽今年18 第1集", target_minutes: [2, 3.5], docs: [{ kind: "brief", bytes: 10 }, { kind: "script", bytes: 20 }] },
      { slug: "tai-nainai-e002", number: 2, variant: null, title: "祠堂點燈｜恁祖媽今年18 第2集", target_minutes: 3, docs: [{ kind: "brief", bytes: 10 }, { kind: "script", bytes: 20 }] },
    ],
    documents: [{ id: "series-plans-top40-tai-nainai-outline", path: "docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/outline.md", title: "第一季大綱", bytes: 30 }] },
  { key: "zhong-tian-qu-qi", name: "種田娶妻打天下", content_sha256: "b".repeat(64), counts: { episodes: 1, brief: 0, script: 1, storyboard: 1, review: 0 },
    episodes: [{ slug: "zhong-tian-qu-qi-e001-r2", number: 1, variant: "r2", title: "官差踹門｜種田娶妻打天下 第1集", target_minutes: null, docs: [{ kind: "script", bytes: 20 }, { kind: "storyboard", bytes: 20 }] }],
    documents: [] },
] };
const episode: DramaEpisodeDetail = { series: "tai-nainai", slug: "tai-nainai-e001", title: "燈下閉眼", docs: [{ kind: "brief", markdown: "簡介：月棠替長明燈添油" }, { kind: "script", markdown: "第一場：祠堂，夜" }] };
const document: DramaDocument = { series: "tai-nainai", id: "series-plans-top40-tai-nainai-outline", path: "x.md", title: "第一季大綱", markdown: "大綱正文" };
const provider = { admin_roles: [], admin_capabilities: ["content.read"], navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false };
const renderAt = (url: string) => {
  window.history.replaceState(null, "", url);
  return render(<AdminOperationsProvider bootstrap={provider}><AdminVideoReviews /></AdminOperationsProvider>);
};
afterEach(() => {
  vi.mocked(api).mockReset();
  window.history.replaceState(null, "", "/");
});
function respond() {
  vi.mocked(api).mockImplementation(async (path) => {
    const value = String(path);
    if (value === "/admin/video-dramas") return index;
    if (value.includes("/episodes/")) return episode;
    if (value.includes("/documents/")) return document;
    throw new Error(`unexpected ${value}`);
  });
}

describe("AI drama scripts in video admin", () => {
  it("lists episodes, opens the script first and switches to the brief, read-only", async () => {
    respond();
    renderAt("/zh-TW/admin/videos?tab=scripts");
    expect(await screen.findByRole("heading", { name: "燈下閉眼｜恁祖媽今年18 第1集" })).toBeTruthy();
    expect(screen.getByRole("tab", { name: copy.tab }).getAttribute("aria-selected")).toBe("true");
    expect(screen.getByText("共 2 集：劇本 2、簡介 2、分鏡 0、審稿 0")).toBeTruthy();
    fireEvent.click(screen.getAllByText(copy.open)[0]);
    expect(await screen.findByText("第一場：祠堂，夜")).toBeTruthy();
    fireEvent.click(screen.getByRole("tab", { name: copy.docs.brief }));
    expect(screen.getByText("簡介：月棠替長明燈添油")).toBeTruthy();
    expect(vi.mocked(api).mock.calls.every(([, options]) => !options?.method || options.method === "GET")).toBe(true);
  });

  it("filters episodes, switches series and shows series documents", async () => {
    respond();
    renderAt("/zh-TW/admin/videos?tab=scripts&script_q=祠堂");
    expect(await screen.findByRole("heading", { name: "祠堂點燈｜恁祖媽今年18 第2集" })).toBeTruthy();
    expect(screen.queryByRole("heading", { name: "燈下閉眼｜恁祖媽今年18 第1集" })).toBeNull();
    fireEvent.change(screen.getByRole("combobox", { name: copy.seriesLabel }), { target: { value: "zhong-tian-qu-qi" } });
    expect(await screen.findByText("改寫版")).toBeTruthy();
    fireEvent.change(screen.getByRole("combobox", { name: copy.seriesLabel }), { target: { value: "tai-nainai" } });
    fireEvent.change(screen.getByRole("combobox", { name: copy.viewLabel }), { target: { value: "documents" } });
    await waitFor(() => expect(new URL(window.location.href).searchParams.get("script_view")).toBe("documents"));
    fireEvent.click(await screen.findByText(copy.open));
    expect(await screen.findByText("大綱正文")).toBeTruthy();
  });
});
