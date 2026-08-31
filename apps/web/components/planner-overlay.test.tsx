import { act, fireEvent, render, screen } from "@testing-library/react";
import { useState } from "react";
import { describe, expect, it } from "vitest";
import { PlannerOverlay } from "./planner-overlay";

function Harness() {
  const [open, setOpen] = useState(false);
  const [value, setValue] = useState("");

  return <>
    <button type="button" onClick={() => setOpen(true)}>開啟編輯</button>
    <PlannerOverlay open={open} onClose={() => setOpen(false)} title="編輯安排">
      <label>安排名稱<input value={value} onChange={(event) => setValue(event.target.value)} /></label>
    </PlannerOverlay>
  </>;
}

async function nextFrame() {
  await act(async () => {
    await new Promise<void>((resolve) => requestAnimationFrame(() => resolve()));
  });
}

// The project does not install @testing-library/user-event. This minimal driver
// dispatches the same per-character keyboard/input sequence needed by this focus regression.
const userEvent = {
  async type(input: HTMLInputElement, text: string) {
    input.focus();
    let value = input.value;
    for (const character of text) {
      fireEvent.keyDown(input, { key: character });
      value += character;
      fireEvent.input(input, { target: { value } });
      fireEvent.keyUp(input, { key: character });
      await nextFrame();
      expect(document.activeElement).toBe(input);
    }
  },
};

describe("PlannerOverlay", () => {
  it("keeps the active input focused while a controlled parent re-renders", async () => {
    render(<Harness />);
    fireEvent.click(screen.getByRole("button", { name: "開啟編輯" }));
    await nextFrame();

    const input = screen.getByLabelText("安排名稱") as HTMLInputElement;
    await userEvent.type(input, "淺草寺與雷門");

    expect(input.value).toBe("淺草寺與雷門");
    expect(document.activeElement).toBe(input);
  });

  it("closes with Escape and restores focus to the trigger", async () => {
    render(<Harness />);
    const trigger = screen.getByRole("button", { name: "開啟編輯" });
    trigger.focus();
    fireEvent.click(trigger);
    await nextFrame();

    expect(screen.getByRole("dialog", { name: "編輯安排" })).toBeTruthy();
    fireEvent.keyDown(document, { key: "Escape" });

    expect(screen.queryByRole("dialog", { name: "編輯安排" })).toBeNull();
    expect(document.activeElement).toBe(trigger);
  });
});
