import "@testing-library/jest-dom/vitest";
import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { useState } from "react";
import { describe, expect, it, vi } from "vitest";
import { PlannerToolSections } from "./tool-sections";

function Settings() {
  const [text, setText] = useState("");
  return <input aria-label="偏好草稿" value={text} onChange={(event) => setText(event.target.value)} />;
}
describe("PlannerToolSections", () => {
  it("vetoes Back without unmounting unsaved fields, then resumes the exact action after confirmation", async () => {
    let deferred: (() => void) | undefined;
    let dirty = false;
    const guard = vi.fn((proceed: () => void) => { if (!dirty) return true; deferred = proceed; return false; });
    render(<PlannerToolSections locale="zh-TW" preparation={<p>準備</p>} settings={<Settings />} sharing={<p>分享</p>} beforeSectionChange={guard} />);
    const menu = screen.getByRole("button", { name: /旅程設定/ });
    fireEvent.click(menu);
    fireEvent.change(screen.getByLabelText("偏好草稿"), { target: { value: "還在編輯" } }); dirty = true;
    fireEvent.click(screen.getByRole("button", { name: /返回/ }));
    expect(screen.getByLabelText("偏好草稿")).toHaveValue("還在編輯");
    expect(deferred).toBeTypeOf("function");
    await act(async () => { deferred?.(); });
    expect(screen.queryByLabelText("偏好草稿")).not.toBeInTheDocument();
    await waitFor(() => expect(screen.getByRole("button", { name: /旅程設定/ })).toHaveFocus());
    expect(guard).toHaveBeenCalledTimes(2);
  });

  it("does not call the exit guard or navigate while busy", () => {
    const guard = vi.fn(() => true);
    render(<PlannerToolSections locale="zh-TW" preparation={<p>準備</p>} settings={<Settings />} sharing={<p>分享</p>} disabled beforeSectionChange={guard} />);
    fireEvent.click(screen.getByRole("button", { name: /旅程設定/ }));
    expect(guard).not.toHaveBeenCalled();
    expect(screen.queryByLabelText("偏好草稿")).not.toBeInTheDocument();
  });
});
