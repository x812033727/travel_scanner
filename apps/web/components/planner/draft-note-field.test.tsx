import "@testing-library/jest-dom/vitest";
import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { DraftNoteField } from "./draft-note-field";

afterEach(() => vi.useRealTimers());
const props = { value: "已存備註", placeholder: "備註", label: "當日備註" };
describe("DraftNoteField", () => {
  it("does not save on typing, blur, or time passing; Cancel restores without writing", async () => {
    vi.useFakeTimers();
    const onSave = vi.fn(), onDirtyChange = vi.fn();
    render(<DraftNoteField {...props} onSave={onSave} onDirtyChange={onDirtyChange} />);
    fireEvent.change(screen.getByRole("textbox"), { target: { value: "尚未存的備註" } });
    fireEvent.blur(screen.getByRole("textbox"));
    await act(async () => { await vi.advanceTimersByTimeAsync(5000); });
    expect(onSave).not.toHaveBeenCalled();
    expect(onDirtyChange).toHaveBeenLastCalledWith(true);
    fireEvent.click(screen.getByRole("button", { name: "取消" }));
    expect(screen.getByRole("textbox")).toHaveValue("已存備註");
    expect(onSave).not.toHaveBeenCalled();
    expect(onDirtyChange).toHaveBeenLastCalledWith(false);
  });

  it("preserves a draft on background refresh and failed save, with one explicit retry", async () => {
    const onSave = vi.fn().mockRejectedValueOnce(new Error("failure")).mockResolvedValueOnce(undefined);
    const onDirtyChange = vi.fn();
    const view = render(<DraftNoteField {...props} onSave={onSave} onDirtyChange={onDirtyChange} />);
    fireEvent.change(screen.getByRole("textbox"), { target: { value: "我的草稿" } });
    view.rerender(<DraftNoteField {...props} value="伺服器新備註" onSave={onSave} onDirtyChange={onDirtyChange} />);
    expect(screen.getByRole("textbox")).toHaveValue("我的草稿");
    fireEvent.click(screen.getByRole("button", { name: "儲存" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("內容已保留");
    expect(screen.getByRole("textbox")).toHaveValue("我的草稿");
    expect(onDirtyChange).toHaveBeenLastCalledWith(true);
    fireEvent.click(screen.getByRole("button", { name: "儲存" }));
    await waitFor(() => expect(onDirtyChange).toHaveBeenLastCalledWith(false));
    expect(onSave.mock.calls).toEqual([["我的草稿"], ["我的草稿"]]);
    expect(screen.getByRole("textbox")).toHaveValue("我的草稿");
  });

  it("blocks repeated saves and Cancel until the explicit save settles", async () => {
    let finish!: () => void;
    const onSave = vi.fn(() => new Promise<void>((resolve) => { finish = resolve; }));
    const onBusyChange = vi.fn();
    render(<DraftNoteField {...props} onSave={onSave} onBusyChange={onBusyChange} />);
    fireEvent.change(screen.getByRole("textbox"), { target: { value: "新備註" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存" }));
    fireEvent.click(screen.getByRole("button", { name: "儲存" }));
    expect(onSave).toHaveBeenCalledOnce();
    expect(onBusyChange).toHaveBeenLastCalledWith(true);
    expect(screen.getByRole("button", { name: "取消" })).toBeDisabled();
    expect(screen.getByRole("textbox")).toBeDisabled();
    await act(async () => { finish(); });
    expect(onBusyChange).toHaveBeenLastCalledWith(false);
    expect(screen.getByRole("status")).toHaveTextContent("已儲存");
  });

  it("accepts background updates only while clean", () => {
    const onSave = vi.fn();
    const view = render(<DraftNoteField {...props} onSave={onSave} />);
    view.rerender(<DraftNoteField {...props} value="新版本" onSave={onSave} />);
    expect(screen.getByRole("textbox")).toHaveValue("新版本");
    expect(onSave).not.toHaveBeenCalled();
  });

  it("does not clear another owner's dirty state when an unmounted save completes", async () => {
    let finish!: () => void;
    const onSave = vi.fn(() => new Promise<void>((resolve) => { finish = resolve; }));
    const onDirtyChange = vi.fn();
    const view = render(<DraftNoteField {...props} onSave={onSave} onDirtyChange={onDirtyChange} />);
    fireEvent.change(screen.getByRole("textbox"), { target: { value: "舊日期備註" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存" }));
    view.unmount();
    onDirtyChange.mockClear();
    await act(async () => { finish(); });
    expect(onDirtyChange).not.toHaveBeenCalled();
  });
});
