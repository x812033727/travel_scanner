import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { VideoProductionState } from "./admin-video-production-state";
import { type ProjectSummary, PublishPill, publishState } from "./admin-video-review-card";

const project: ProjectSummary = {
  slug: "imported-final", title: "Imported final", stage: "final", pending: 0,
  last_synced_at: "2026-10-05T00:00:00Z", youtube_video_id: null,
  checklist: [{ key: "final_video_approved", label: "Final approved", done: true }],
  locales_decided_at: "2026-10-05T00:00:00Z", locales: { en: { metadata: true, captions: true, dub: false } },
  languages: { en: { metadata: { state: "ready" }, captions: { state: "working" } } },
  ready_to_upload: false, worker_state: "not_adopted",
};

describe("video production evidence", () => {
  it("explains unadopted work separately from incomplete language results", () => {
    render(<PublishPill project={project} />);
    expect(screen.getByText("語言尚未完成")).toBeTruthy();
    expect(screen.getByText("主工人未接手")).toBeTruthy();
    expect(screen.getByText(/請從原製作流程及已核准素材接續/)).toBeTruthy();
    expect(publishState(project)).toBe("making");
  });

  it("does not describe persisted registration as a running process", () => {
    render(<VideoProductionState state="registered" />);
    expect(screen.getByText("主工人已有登記")).toBeTruthy();
    expect(screen.getByText(/這不代表行程正在執行/)).toBeTruthy();
  });

  it("keeps a recorded worker completion separate from later language choices", () => {
    render(<PublishPill project={{ ...project, worker_state: "done" }} />);
    expect(screen.getByText("語言尚未完成")).toBeTruthy();
    expect(screen.getByText("主工人已記錄完成")).toBeTruthy();
    expect(screen.getByText(/後來勾選的語言是否就緒/)).toBeTruthy();
  });

  it.each([
    { ...project, locales: {}, languages: {}, youtube_video_id: "dQw4w9WgXcQ" },
    { ...project, ready_to_upload: true },
    { ...project, shorts_line: "lab" as const },
    { ...project, format: "shorts" as const },
    { ...project, dropped_at: "2026-10-05T00:00:00Z" },
  ])("does not report a handoff gap once no production work remains or another route owns it", (complete) => {
    render(<PublishPill project={complete} />);
    expect(screen.queryByText("主工人未接手")).toBeNull();
  });

  it("still shows unfinished added languages for a video already on YouTube", () => {
    render(<PublishPill project={{ ...project, youtube_video_id: "dQw4w9WgXcQ" }} />);
    expect(screen.getByText("已上架")).toBeTruthy();
    expect(screen.getByText("主工人未接手")).toBeTruthy();
  });

  it("does not invent handoff evidence for older APIs", () => {
    const { container } = render(<VideoProductionState state={undefined} />);
    expect(container.textContent).toBe("");
  });
});
