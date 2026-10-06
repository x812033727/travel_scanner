import { cleanup, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { ReviewCard, type Review, type ReviewFile } from "./admin-video-review-card";

// The owner's decision of 2026-10-06: an illustrated video whose pictures still fail the judge after
// two prompt fixes keeps the best take of each and goes on (tools/video/media/keyframes.mjs
// --accept-best). Its storyboard marks those shots accepted, and its cut is sent for the owner's own
// review with the pictures listed (tools/video/review/sync.mjs). These pin down what the two cards
// show of that, and that a payload of any other shape shows nothing and never breaks the card.
const sha = (char: string) => char.repeat(64);
const image = (role: string, char: string): ReviewFile => ({ role, sha256: sha(char), size: 100, content_type: "image/png" });
const review = (gate: Review["gate"], payload: Review["payload"], files: ReviewFile[] = []): Review => ({
  id: "5332abba-80a5-4400-895d-954b4ec4328f", gate, content_sha256: sha("b"), summary: "Synthetic review",
  payload, files, status: "pending", choice: null, note: null, decided_at: null, created_at: "2026-10-06T08:40:31Z",
});
const show = (value: Review) => render(<ReviewCard slug="ai-ranking" review={value} canManage onDecided={vi.fn()} />);
const texts = (elements: Iterable<Element>) => [...elements].map((element) => element.textContent);

const REASON = "有 2 張插圖未通過 judge（desk、race），需站主審看成片；機械品管僅供參考。";
const REPORT = { ok: false, final_sha256: sha("b"), items: [
  { id: "assemble", ok: true, detail: "1800 frames", warnings: ["desk: kept with the judge's remarks after the prompt fixes"] },
  { id: "pace", ok: false, detail: "slide 4 stays 21 s" },
] };
const final = (payload: Review["payload"]) => review("final", { checks: { ok: true, problems: [] }, ...payload }, [{ role: "preview", sha256: sha("c"), size: 10, content_type: "video/mp4" }]);

afterEach(cleanup);

describe("a final cut sent for the owner's own review", () => {
  it("says why, lists the quality check for reference only, and lists every kept picture with what the judge said", () => {
    show(final({
      manual_review: true, manual_review_reason: REASON, manual_review_qa: REPORT,
      accepted_pictures: [{ id: "desk", problems: ["awkward: the hand → a hand resting flat", "details: no cup"] }, { id: "race", problems: [] }],
    }));
    const card = screen.getByRole("article", { name: "成片" });
    const notice = within(card).getByRole("region", { name: "這支成片要由你審看，不會自動核准" });
    expect(notice.textContent).toContain(REASON);

    // The same list a cut approved from payload.qa shows, failed items first, with the mark.
    const report = within(card).getByLabelText("自動品管");
    expect(report.textContent).toContain("僅供參考");
    expect(report.textContent).toContain("1 項沒過");
    const items = texts(report.querySelectorAll(":scope > ul > li"));
    expect(items[0]).toContain("節奏 · slide 4 stays 21 s");
    expect(items[1]).toContain("合成 · 1800 frames");
    expect(items[1]).toContain("注意：desk: kept with the judge's remarks after the prompt fixes");
    expect(within(card).getAllByLabelText("自動品管")).toHaveLength(1);

    const kept = within(card).getByRole("region", { name: "保留的插圖（2 張）" });
    expect(texts(within(kept).getAllByRole("listitem"))).toEqual([
      "desk · awkward: the hand → a hand resting flat；details: no cup",
      "race · judge 沒有留下意見",
    ]);
    // The decision is the owner's: nothing about the kept pictures holds the button back.
    expect(within(card).getByRole("button", { name: "核准" })).toHaveProperty("disabled", false);
  });

  it("lists eighty kept pictures, each with its own remarks", () => {
    const pictures = Array.from({ length: 80 }, (_, index) => ({ id: `shot-${index + 1}`, problems: [`generated: glossy ${index + 1}`] }));
    show(final({ manual_review: true, manual_review_reason: "有 80 張插圖未通過 judge（shot-1、shot-2、shot-3、shot-4、shot-5 等，另 75 張），需站主審看成片；機械品管僅供參考。", accepted_pictures: pictures }));
    const kept = screen.getByRole("region", { name: "保留的插圖（80 張）" });
    const rows = texts(within(kept).getAllByRole("listitem"));
    expect(rows).toHaveLength(80);
    expect(rows[0]).toBe("shot-1 · generated: glossy 1");
    expect(rows[79]).toBe("shot-80 · generated: glossy 80");
  });

  it("shows a renewal's reason too, and the notice alone when the cut gives no reason", () => {
    const { unmount } = show(final({ manual_review: true, manual_review_reason: "  片尾換了新版\n請再看一次銜接  " }));
    expect(screen.getByRole("region", { name: "這支成片要由你審看，不會自動核准" }).textContent).toBe("這支成片要由你審看，不會自動核准片尾換了新版\n請再看一次銜接");
    unmount();
    show(final({ manual_review: true }));
    expect(screen.getByRole("region", { name: "這支成片要由你審看，不會自動核准" }).textContent).toBe("這支成片要由你審看，不會自動核准");
    expect(screen.queryByLabelText("自動品管")).toBeNull();
    expect(screen.queryByRole("region", { name: /^保留的插圖/ })).toBeNull();
  });

  it("leaves a cut approved from its own report as it was: no notice, no mark, no kept pictures", () => {
    show(final({ qa: REPORT }));
    const card = screen.getByRole("article", { name: "成片" });
    expect(within(card).queryByRole("region", { name: "這支成片要由你審看，不會自動核准" })).toBeNull();
    expect(within(card).queryByRole("region", { name: /^保留的插圖/ })).toBeNull();
    const report = within(card).getByLabelText("自動品管");
    expect(report.textContent).toContain("1 項沒過");
    expect(report.textContent).not.toContain("僅供參考");
  });

  it("shows the report an approval reads once, unmarked, when a payload carries both", () => {
    show(final({ manual_review: true, manual_review_reason: REASON, qa: REPORT, manual_review_qa: { ok: true, items: [{ id: "render", ok: true }] } }));
    const reports = screen.getAllByLabelText("自動品管");
    expect(reports).toHaveLength(1);
    expect(reports[0].textContent).toContain("節奏");
    expect(reports[0].textContent).not.toContain("僅供參考");
  });

  it.each([
    ["manual_review that is not true", { manual_review: "true", manual_review_reason: REASON }],
    ["manual_review as a number", { manual_review: 1, manual_review_reason: REASON }],
    ["a reason with no manual review", { manual_review_reason: REASON }],
  ])("shows no notice for %s", (_label, payload) => {
    show(final(payload));
    expect(screen.queryByRole("region", { name: "這支成片要由你審看，不會自動核准" })).toBeNull();
    expect(screen.getByRole("article", { name: "成片" }).textContent).not.toContain(REASON);
  });

  it.each([
    ["a number", 42], ["a list", ["x"]], ["an object", { text: "x" }], ["null", null], ["blank text", "   "],
  ])("shows the notice without a reason when the reason is %s", (_label, reason) => {
    show(final({ manual_review: true, manual_review_reason: reason }));
    expect(screen.getByRole("region", { name: "這支成片要由你審看，不會自動核准" }).textContent).toBe("這支成片要由你審看，不會自動核准");
  });

  it.each([
    ["text", "passed"], ["a number", 7], ["null", null], ["a list", [{ id: "pace", ok: true }]],
    ["items that are not a list", { items: "pace" }], ["items with nothing that names a check", { items: [null, 3, "pace", { ok: true }, []] }],
  ])("shows no quality check when manual_review_qa is %s", (_label, report) => {
    show(final({ manual_review: true, manual_review_reason: "Renewed branding", manual_review_qa: report }));
    expect(screen.queryByLabelText("自動品管")).toBeNull();
    expect(screen.getByRole("article", { name: "成片" }).textContent).not.toContain("僅供參考");
    expect(screen.getByRole("region", { name: "這支成片要由你審看，不會自動核准" }).textContent).toContain("Renewed branding");
  });

  it.each([
    ["text", "desk"], ["a number", 3], ["null", null], ["an object", { id: "desk", problems: ["x"] }], ["an empty list", []],
    ["entries that name no picture", [null, 3, "desk", ["desk"], { problems: ["no id"] }, { id: {}, problems: ["x"] }, { id: "" }]],
  ])("shows no kept pictures when accepted_pictures is %s", (_label, pictures) => {
    show(final({ manual_review: true, manual_review_reason: REASON, accepted_pictures: pictures }));
    expect(screen.queryByRole("region", { name: /^保留的插圖/ })).toBeNull();
    expect(screen.getByRole("region", { name: "這支成片要由你審看，不會自動核准" })).toBeTruthy();
  });

  it("keeps what it can read of a half-broken list: the entries with an id, and of their remarks the text", () => {
    show(final({ accepted_pictures: [null, { id: "desk", problems: "not a list" }, { problems: ["no id"] }, { id: 7, problems: [null, { a: 1 }, "blurred", 5, ""] }, { id: "desk" }] }));
    const kept = screen.getByRole("region", { name: "保留的插圖（3 張）" });
    expect(texts(within(kept).getAllByRole("listitem"))).toEqual(["desk · judge 沒有留下意見", "7 · blurred；5", "desk · judge 沒有留下意見"]);
  });
});

describe("a storyboard with pictures kept with the judge's remarks", () => {
  const shots = [
    { id: "opening", prompt: "A quiet street", file_role: "shot_01", needs_review: false, judge: { overall: 8, problems: [] } },
    { id: "desk", prompt: "A kitchen table", file_role: "shot_02", needs_review: false, accepted: true, judge: { overall: 5, problems: ["awkward: the hand"] } },
    { id: "clock", prompt: "A train platform", file_role: "shot_03", needs_review: true, judge: { overall: 6, problems: ["details: no clock"] } },
  ];
  const files = [image("shot_01", "1"), image("shot_02", "2"), image("shot_03", "3")];
  // A shot's row starts with its number and id; no id here begins another.
  const row = (id: string) => {
    const found = screen.getAllByRole("listitem").find((item) => new RegExp(`^\\d+\\. ${id}`).test(item.textContent ?? ""));
    if (!found) throw new Error(`no row for ${id}`);
    return found;
  };

  it("marks the shots payload.accepted names as kept, with their score and problems, apart from a shot still waiting for a prompt fix", () => {
    show(review("storyboard", { shots, judge: { overall: 6, problems: ["details: no clock"] }, accepted: [{ id: "desk", overall: 5, problems: ["awkward: the hand → a hand resting flat"] }] }, files));
    const card = screen.getByRole("article", { name: "分鏡" });
    expect(card.textContent).toContain("1 鏡保留：judge 沒過，成片時由你審看");

    const desk = row("desk");
    expect(desk.textContent).toContain("保留");
    expect(desk.textContent).toContain("提示詞修完仍沒通過 judge，保留最好的一張；成片時由你審看");
    // The list's remarks, which carry the judge's fix, not the shot's shorter verdict.
    expect(desk.textContent).toContain("judge 5/10：awkward: the hand → a hand resting flat");
    expect(desk.textContent).not.toContain("沒有一次通過 judge");
    expect(desk.className).toContain("border-sky-600");
    expect(within(desk).getByRole("img", { name: "desk" })).toBeTruthy();

    const clock = row("clock");
    expect(clock.textContent).toContain("沒有一次通過 judge，提示詞要修");
    expect(clock.textContent).toContain("judge 6/10：details: no clock");
    expect(clock.textContent).not.toContain("保留");
    expect(clock.className).toContain("border-amber-600");

    const opening = row("opening");
    expect(opening.textContent).not.toContain("保留");
    expect(opening.textContent).not.toContain("沒有一次通過 judge");
    expect(opening.className).not.toMatch(/border-(sky|amber)-600/);
  });

  it("counts a board whose every shot was kept, which has no lowest score of its own", () => {
    const every = shots.map((shot) => ({ ...shot, needs_review: false, accepted: true, judge: { overall: 4, problems: ["x"] } }));
    show(review("storyboard", { shots: every, judge: { overall: null, problems: [] }, accepted: every.map((shot) => ({ id: shot.id, overall: 4, problems: ["generated: glossy"] })) }, files));
    const card = screen.getByRole("article", { name: "分鏡" });
    expect(card.textContent).toContain("3 鏡保留：judge 沒過，成片時由你審看");
    for (const shot of every) expect(row(shot.id).textContent).toContain("judge 4/10：generated: glossy");
  });

  it("reads a shot's own accepted flag and verdict when the list is missing or says less", () => {
    const { unmount } = show(review("storyboard", { shots }, files));
    expect(row("desk").textContent).toContain("保留");
    expect(row("desk").textContent).toContain("judge 5/10：awkward: the hand");
    expect(screen.getByRole("article", { name: "分鏡" }).textContent).toContain("1 鏡保留");
    unmount();
    // Named with neither score nor remarks: the shot's verdict stands in. Named with no verdict anywhere: said so.
    show(review("storyboard", { shots: [...shots, { id: "door", prompt: "A hallway", file_role: null }], accepted: [{ id: "desk" }, { id: "door", overall: "low", problems: [null] }] }, files));
    expect(row("desk").textContent).toContain("judge 5/10：awkward: the hand");
    expect(row("door").textContent).toContain("保留");
    expect(row("door").textContent).toContain("judge 沒有留下意見");
    expect(screen.getByRole("article", { name: "分鏡" }).textContent).toContain("2 鏡保留");
  });

  it("never calls a shot kept while it still waits for a prompt fix, whatever the list says", () => {
    show(review("storyboard", { shots, accepted: [{ id: "clock", overall: 6, problems: ["details: no clock"] }] }, files));
    expect(row("clock").textContent).toContain("沒有一次通過 judge，提示詞要修");
    expect(row("clock").textContent).not.toContain("保留");
    // The desk still says so itself.
    expect(screen.getByRole("article", { name: "分鏡" }).textContent).toContain("1 鏡保留");
  });

  it.each([
    ["text", "desk"], ["a number", 2], ["null", null], ["an object", { id: "opening" }],
    ["entries that name no shot of the board", [null, 4, "opening", { overall: 5 }, { id: "gone", overall: 5, problems: ["x"] }, { id: {} }]],
  ])("marks nothing kept when payload.accepted is %s", (_label, accepted) => {
    const plain = shots.map((shot) => ({ ...shot, accepted: undefined }));
    show(review("storyboard", { shots: plain, judge: { overall: 5, problems: [] }, accepted }, files));
    const card = screen.getByRole("article", { name: "分鏡" });
    expect(card.textContent).not.toContain("保留");
    expect(screen.getAllByRole("listitem")).toHaveLength(3);
    expect(row("clock").textContent).toContain("沒有一次通過 judge，提示詞要修");
    expect(row("desk").textContent).toContain("judge 5/10：awkward: the hand");
  });

  it("leaves a storyboard from before kept pictures as it was", () => {
    show(review("storyboard", { shots: [{ id: "one", prompt: "Synthetic shot", file_role: "shot_01", needs_review: true, judge: { overall: 5, problems: ["no bird"] } }], judge: { overall: 5, problems: ["no bird"] } }, [files[0]]));
    const card = screen.getByRole("article", { name: "分鏡" });
    expect(card.textContent).toContain("judge 5/10：no bird");
    expect(card.textContent).toContain("沒有一次通過 judge，提示詞要修");
    expect(card.textContent).not.toContain("保留");
  });
});
