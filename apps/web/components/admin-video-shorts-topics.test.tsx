import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { fitted, PART_BYTES, sha256Hex, type Topic } from "./admin-video-shorts-data";
import { frontOrder, ShortsTopics } from "./admin-video-shorts-topics";

// The canvas the browser shrinks a photo on is not in jsdom: the test hands back a file of its own size.
const shrunk = vi.hoisted(() => ({ size: 10 }));
vi.mock("@/components/admin-video-shorts-data", async (importOriginal) => ({
  ...(await importOriginal<typeof import("./admin-video-shorts-data")>()),
  shrinkImage: vi.fn(async () => ({ blob: new Blob([new Uint8Array(shrunk.size)], { type: "image/jpeg" }), filename: "landmark-near.jpg" })),
}));

const topic = (slug: string, fields: Partial<Topic> = {}): Topic => ({
  slug, line: "lab", series: "blind", title: slug, hook: null, status: "ready", brief: {}, source_slug: null, origin: "campaign", release_order: null,
  assets_needed: [], assets: [], waiting_for: [], paid: false, project_slug: null, started_at: null, finished_at: null, note: null,
  created_at: "2026-10-01T00:00:00Z", updated_at: "2026-10-01T00:00:00Z", ...fields,
});
const protocol = { setup: "三張發票", input: "照片與題目", condition_a: "直接問", condition_b: "先列步驟", runs: "各一次", scoring: "對總額", failure_path: "重試一次" };
const receipt = topic("shorts-receipt-total", {
  title: "AI 算發票總額", hook: "三張發票，AI 算對幾張", release_order: 1,
  brief: { test_protocol: protocol, truth_check: ["總額 1,234 元"], acceptance: ["兩組都跑完"] },
});
const location = topic("shorts-taiwan-location", {
  title: "AI 認景點", status: "needs_assets", release_order: 4,
  assets_needed: [{ key: "landmarks", label: "三張景點照片", count: 3 }],
  waiting_for: ["缺素材：三張景點照片（還差 3 個）", "受測模型要看圖：要接一個有金鑰的視覺模型"],
});
const idea = topic("idea-20261001-abc123", { title: "AI 會不會數錢", status: "idea", origin: "owner", waiting_for: ["測試規格缺 setup"] });
const cut = topic("travel-guide-cut-1", { line: "cut", title: "東京交通（精華 1）", origin: "auto", source_slug: "travel-guide", series: "travel-guide" });
const dropped = topic("shorts-old", { title: "舊題目", status: "dropped" });

type Call = { url: string; method: string; body: unknown; headers: Record<string, string> };

function stubFetch(items: Topic[], write?: (call: Call) => unknown) {
  const calls: Call[] = [];
  vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const body = init?.body;
    const call = { url: String(input), method: init?.method ?? "GET", body: typeof body === "string" ? body : body, headers: (init?.headers ?? {}) as Record<string, string> };
    calls.push(call);
    if (call.method === "GET") return Response.json({ items });
    const answer = write?.(call);
    if (answer instanceof Response) return answer;
    return Response.json(answer ?? {});
  }));
  return calls;
}

const path = (call: Call) => call.url.replace(/^.*\/api\/travel/, "");
const writes = (calls: Call[]) => calls.filter((call) => call.method !== "GET");
const json = (call: Call) => JSON.parse(String(call.body));

afterEach(() => vi.unstubAllGlobals());

describe("where moving a topic to the front puts it", () => {
  it("goes one before the first of its line, and moves the others back when nothing is left below", () => {
    const one = topic("one", { release_order: 3 });
    const two = topic("two", { release_order: 5 });
    const other = topic("other-line", { line: "cut", release_order: 0 });
    expect(frontOrder(two, [one, two, other])).toEqual({ order: 2, shift: [] });
    expect(frontOrder(one, [one, two, other])).toEqual({ order: 3, shift: [] });
    expect(frontOrder(one, [one, other])).toEqual({ order: 3, shift: [] });
    expect(frontOrder(topic("loose"), [topic("loose"), other])).toEqual({ order: 0, shift: [] });
    const zero = topic("zero", { release_order: 0 });
    const gone = topic("gone", { release_order: 0, status: "made" });
    expect(frontOrder(two, [zero, two, gone])).toEqual({ order: 0, shift: [zero] });
  });
});

describe("the photo as it goes up", () => {
  it("keeps its long edge at 2,048 px at most, never enlarged", () => {
    expect(fitted(4032, 3024)).toEqual({ width: 2048, height: 1536 });
    expect(fitted(3000, 6000)).toEqual({ width: 1024, height: 2048 });
    expect(fitted(800, 600)).toEqual({ width: 800, height: 600 });
  });

  it("is named by its SHA-256", async () => {
    expect(await sha256Hex(new Blob(["abc"]))).toBe("ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad");
  });
});

describe("ShortsTopics", () => {
  it("groups the topics by line, says why one cannot be made yet, and opens the whole spec", async () => {
    stubFetch([receipt, location, idea, cut]);
    render(<ShortsTopics canManage />);
    const lab = await screen.findByRole("region", { name: "實測" });
    const cuts = screen.getByRole("region", { name: "長片精華" });
    expect(screen.queryByRole("region", { name: "漫劇直式短篇" })).toBeNull();
    for (const title of ["AI 算發票總額", "AI 認景點", "AI 會不會數錢"]) expect(within(lab).getByRole("listitem", { name: title })).toBeTruthy();
    expect(within(lab).queryByRole("listitem", { name: "東京交通（精華 1）" })).toBeNull();
    expect(within(cuts).getByRole("listitem", { name: "東京交通（精華 1）" })).toBeTruthy();
    expect(cuts.textContent).toContain("自動");

    const card = within(lab).getByRole("listitem", { name: "AI 認景點" });
    expect(card.textContent).toContain("缺素材");
    expect(card.textContent).toContain("還不能做，因為：");
    expect(card.textContent).toContain("受測模型要看圖");
    expect(within(lab).getByRole("listitem", { name: "AI 會不會數錢" }).textContent).toContain("站主");

    const first = within(lab).getByRole("listitem", { name: "AI 算發票總額" });
    expect(first.textContent).toContain("可以做");
    expect(first.textContent).toContain("企劃");
    expect(first.textContent).toContain("三張發票，AI 算對幾張");
    expect(within(first).queryByLabelText("AI 算發票總額 的規格")).toBeNull();
    fireEvent.click(within(first).getByRole("button", { name: "看完整規格" }));
    const spec = within(first).getByLabelText("AI 算發票總額 的規格");
    expect(spec.textContent).toContain("先列步驟");
    expect(spec.textContent).toContain("總額 1,234 元");
    expect(spec.textContent).toContain("兩組都跑完");
    expect(within(first).getByRole("button", { name: "收起規格" }).getAttribute("aria-expanded")).toBe("true");
  });

  it("gives a topic up after asking, takes a dropped one back, and moves one to the front of its line", async () => {
    // The server's library: a change is what the next read returns.
    const library = [receipt, location, dropped];
    const calls = stubFetch(library, (call) => {
      const sent = json(call);
      const index = library.findIndex((each) => each.slug === path(call).split("/").pop());
      library[index] = { ...library[index], ...(sent.dropped === true ? { status: "dropped" } : sent.dropped === false ? { status: "idea" } : sent) };
      return library[index];
    });
    const confirm = vi.spyOn(window, "confirm").mockReturnValueOnce(false).mockReturnValue(true);
    render(<ShortsTopics canManage />);
    const card = await screen.findByRole("listitem", { name: "AI 認景點" });
    fireEvent.click(within(card).getByRole("button", { name: "放棄這題" }));
    expect(writes(calls)).toHaveLength(0);
    fireEvent.click(within(card).getByRole("button", { name: "放棄這題" }));
    await waitFor(() => expect(writes(calls)).toHaveLength(1));
    expect(writes(calls)[0]).toMatchObject({ method: "PATCH" });
    expect(path(writes(calls)[0])).toBe("/admin/video-shorts/topics/shorts-taiwan-location");
    expect(json(writes(calls)[0])).toEqual({ dropped: true });
    expect(confirm).toHaveBeenLastCalledWith("放棄「AI 認景點」？之後還可以取回。");

    fireEvent.click(within(screen.getByRole("listitem", { name: "舊題目" })).getByRole("button", { name: "取回這題" }));
    await waitFor(() => expect(writes(calls)).toHaveLength(2));
    expect(json(writes(calls)[1])).toEqual({ dropped: false });

    // The dropped topic came back as an idea; the location topic is dropped now, so the receipt
    // (release order 1) and the restored one are left: moving the restored one up puts it at 0.
    const restored = await screen.findByRole("listitem", { name: "舊題目" });
    await waitFor(() => expect(within(restored).getByRole("button", { name: "排到最前面" })).toBeTruthy());
    fireEvent.click(within(restored).getByRole("button", { name: "排到最前面" }));
    await waitFor(() => expect(writes(calls)).toHaveLength(3));
    expect(path(writes(calls)[2])).toBe("/admin/video-shorts/topics/shorts-old");
    expect(json(writes(calls)[2])).toEqual({ release_order: 0 });
    confirm.mockRestore();
  });

  it("keeps an idea in a sentence and its line", async () => {
    const calls = stubFetch([], () => idea);
    render(<ShortsTopics canManage />);
    expect(await screen.findByText("題庫還是空的")).toBeTruthy();
    const form = screen.getByRole("form", { name: "新增想法" });
    const submit = within(form).getByRole("button", { name: "存成想法" });
    expect(submit).toHaveProperty("disabled", true);
    fireEvent.change(within(form).getByLabelText("想法"), { target: { value: "  AI 會不會數錢  " } });
    fireEvent.change(within(form).getByLabelText("內容線"), { target: { value: "cut" } });
    fireEvent.click(submit);
    await waitFor(() => expect(writes(calls)).toHaveLength(1));
    expect(writes(calls)[0]).toMatchObject({ method: "POST" });
    expect(path(writes(calls)[0])).toBe("/admin/video-shorts/topics");
    expect(json(writes(calls)[0])).toEqual({ title: "AI 會不會數錢", line: "cut" });
    expect((await within(form).findByRole("status")).textContent).toContain("企劃模型下一輪會把它補成完整的規格");
    expect((within(form).getByLabelText("想法") as HTMLTextAreaElement).value).toBe("");
  });

  it("sends campaign.json as it is and says how many it took and skipped", async () => {
    const calls = stubFetch([], () => ({ created: 3, updated: 0, skipped: 12, items: [] }));
    render(<ShortsTopics canManage />);
    const input = await screen.findByLabelText("campaign.json 檔案");
    fireEvent.change(input, { target: { files: [new File(["not json"], "campaign.json", { type: "application/json" })] } });
    expect((await screen.findByRole("alert")).textContent).toBe("這個檔案不是 JSON，請選 campaign.json。");
    expect(writes(calls)).toHaveLength(0);

    const campaign = JSON.stringify({ campaign_id: "ai-shorts-001", topics: [{ slug: "shorts-receipt-total", topic_zh: "AI 算發票總額" }] });
    fireEvent.change(input, { target: { files: [new File([campaign], "campaign.json", { type: "application/json" })] } });
    await waitFor(() => expect(writes(calls)).toHaveLength(1));
    expect(path(writes(calls)[0])).toBe("/admin/video-shorts/topics/import");
    expect(writes(calls)[0].body).toBe(campaign);
    expect((await screen.findByRole("status")).textContent).toBe("匯入了 3 題，略過 12 題（已經在題庫裡）。");
  });

  it("takes a photo only with its author, the day it was taken and its terms, in parts of 4 MiB", async () => {
    shrunk.size = PART_BYTES + 10;
    const ready = { ...location, status: "ready", waiting_for: [], assets: [{ id: "a1", need: "landmarks", sha256: "f".repeat(64), filename: "landmark-near.jpg", content_type: "image/jpeg", size: PART_BYTES + 10, author: "站主", taken_on: "2026-09-30", rights_note: "自己拍的", created_at: "2026-10-01T00:00:00Z", download_path: "x" }] };
    const calls = stubFetch([location], (call) => (new URL(call.url, "http://x").searchParams.get("part") === "1" ? { received: [0, 1], complete: true, asset: ready.assets[0], topic: ready } : { received: [0], complete: false, asset: null, topic: null }));
    render(<ShortsTopics canManage />);
    const box = await screen.findByRole("region", { name: "三張景點照片" });
    expect(box.textContent).toContain("0／3");
    const upload = within(box).getByRole("button", { name: "上傳" });
    fireEvent.change(within(box).getByLabelText("照片（PNG、JPEG 或 WebP）"), { target: { files: [new File(["x"], "IMG_0001.HEIC.jpg", { type: "image/jpeg" })] } });
    fireEvent.change(within(box).getByLabelText("拍攝者（或作者）"), { target: { value: "站主" } });
    fireEvent.change(within(box).getByLabelText("授權說明（誰拍的、可以怎麼用）"), { target: { value: "自己拍的" } });
    expect(upload).toHaveProperty("disabled", true);
    fireEvent.change(within(box).getByLabelText("拍攝日期"), { target: { value: "2026-09-30" } });
    expect(upload).toHaveProperty("disabled", false);
    fireEvent.click(upload);
    await waitFor(() => expect(writes(calls)).toHaveLength(2));
    const [first, second] = writes(calls).map((call) => new URL(call.url, "http://x"));
    expect(first.pathname).toBe("/api/travel/admin/video-shorts/topics/shorts-taiwan-location/assets");
    expect(Object.fromEntries(first.searchParams)).toMatchObject({
      part: "0", parts: "2", size: String(PART_BYTES + 10), need: "landmarks", filename: "landmark-near.jpg",
      author: "站主", rights_note: "自己拍的", taken_on: "2026-09-30",
    });
    expect(first.searchParams.get("sha256")).toMatch(/^[0-9a-f]{64}$/);
    expect(second.searchParams.get("part")).toBe("1");
    expect(second.searchParams.get("sha256")).toBe(first.searchParams.get("sha256"));
    expect((writes(calls)[0].body as Blob).size).toBe(PART_BYTES);
    expect((writes(calls)[1].body as Blob).size).toBe(10);
    expect(writes(calls)[0].headers["Content-Type"]).toBe("application/octet-stream");
    // The topic comes back as the server settled it: the file is in, and nothing is said to be missing.
    const card = screen.getByRole("listitem", { name: "AI 認景點" });
    await waitFor(() => expect(card.textContent).toContain("可以做"));
    expect(card.textContent).not.toContain("還不能做");
    expect(box.textContent).toContain("1／3");
    expect(box.textContent).toContain("拍攝者 站主");
    expect(within(box).getByRole("status").textContent).toBe("上傳好了。");
    shrunk.size = 10;
  });

  it("says what the server said when it refuses a part", async () => {
    const calls = stubFetch([location], () => Response.json({ code: "video_shorts_asset_type", detail: "素材只收 PNG、JPEG 或 WebP 圖片" }, { status: 415 }));
    render(<ShortsTopics canManage />);
    const box = await screen.findByRole("region", { name: "三張景點照片" });
    fireEvent.change(within(box).getByLabelText("照片（PNG、JPEG 或 WebP）"), { target: { files: [new File(["x"], "a.jpg", { type: "image/jpeg" })] } });
    fireEvent.change(within(box).getByLabelText("拍攝者（或作者）"), { target: { value: "站主" } });
    fireEvent.change(within(box).getByLabelText("拍攝日期"), { target: { value: "2026-09-30" } });
    fireEvent.change(within(box).getByLabelText("授權說明（誰拍的、可以怎麼用）"), { target: { value: "自己拍的" } });
    fireEvent.click(within(box).getByRole("button", { name: "上傳" }));
    expect((await within(box).findByRole("alert")).textContent).toBe("沒有上傳：素材只收 PNG、JPEG 或 WebP 圖片");
    expect(writes(calls)).toHaveLength(1);
  });

  it("gives a reader the topics and their specs but no way to change them", async () => {
    const calls = stubFetch([receipt, location, dropped]);
    render(<ShortsTopics canManage={false} />);
    const lab = await screen.findByRole("region", { name: "實測" });
    expect(screen.queryByRole("form", { name: "新增想法" })).toBeNull();
    expect(screen.queryByLabelText("campaign.json 檔案")).toBeNull();
    expect(within(lab).queryByRole("button", { name: "放棄這題" })).toBeNull();
    expect(within(lab).queryByRole("button", { name: "排到最前面" })).toBeNull();
    expect(within(lab).queryByRole("button", { name: "取回這題" })).toBeNull();
    expect(within(lab).queryByRole("button", { name: "上傳" })).toBeNull();
    expect(screen.getByRole("region", { name: "三張景點照片" })).toBeTruthy();
    expect(within(lab).getAllByRole("button", { name: "看完整規格" })).toHaveLength(3);
    expect(writes(calls)).toHaveLength(0);
  });
});
