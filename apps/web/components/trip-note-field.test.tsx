import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { TripNoteField } from "./trip-note-field";

afterEach(() => vi.useRealTimers());

function field(onSave: (next: string) => Promise<void>, value = "") {
  return (
    <TripNoteField label="旅程備註" placeholder="例如：護照 12 月到期" value={value} onSave={onSave} />
  );
}

describe("trip note field", () => {
  it("saves on blur without waiting for the debounce", async () => {
    const onSave = vi.fn(async () => undefined);
    render(field(onSave));

    const box = screen.getByLabelText("旅程備註");
    fireEvent.change(box, { target: { value: "護照 12 月到期" } });
    expect(onSave).not.toHaveBeenCalled();
    fireEvent.blur(box);

    await waitFor(() => expect(onSave).toHaveBeenCalledWith("護照 12 月到期"));
    expect(await screen.findByText("備註已儲存")).toBeTruthy();
  });

  it("keeps what was typed when the save fails", async () => {
    const onSave = vi.fn(async () => {
      throw new Error("offline");
    });
    render(field(onSave));

    const box = screen.getByLabelText("旅程備註") as HTMLTextAreaElement;
    fireEvent.change(box, { target: { value: "這天要先訂位" } });
    fireEvent.blur(box);

    expect(await screen.findByRole("alert")).toBeTruthy();
    // Losing a note the traveller typed is worse than any other failure here.
    expect(box.value).toBe("這天要先訂位");
  });

  it("does not save again when nothing changed", async () => {
    const onSave = vi.fn(async () => undefined);
    render(field(onSave, "已經寫好的備註"));

    fireEvent.blur(screen.getByLabelText("旅程備註"));

    await new Promise((resolve) => setTimeout(resolve, 20));
    expect(onSave).not.toHaveBeenCalled();
  });

  it("ignores a server value while the box has unsaved text", async () => {
    const onSave = vi.fn(async () => undefined);
    const { rerender } = render(field(onSave, "原本的"));

    const box = screen.getByLabelText("旅程備註") as HTMLTextAreaElement;
    fireEvent.change(box, { target: { value: "正在打字" } });
    // A background trip refresh arrives mid-sentence.
    rerender(field(onSave, "伺服器版本"));

    expect(box.value).toBe("正在打字");
  });
});
