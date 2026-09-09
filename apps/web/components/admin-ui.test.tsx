import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { AdminConfirmDialog, AdminStatusPill } from "./admin-ui";

function dialog(open: boolean, onCancel: () => void, busy = false) {
  return <><button type="button">Before dialog</button><AdminConfirmDialog
    open={open}
    title="Sensitive action"
    description="Verify this action"
    confirmationLabel="Confirmation"
    confirmation=""
    expectedConfirmation="CONFIRM"
    password=""
    passwordLabel="Current password"
    busy={busy}
    onConfirmationChange={() => undefined}
    onPasswordChange={() => undefined}
    onCancel={onCancel}
    onConfirm={() => undefined}
  /></>;
}

describe("AdminConfirmDialog", () => {
  it("traps focus, closes with Escape, locks scroll, and restores focus", () => {
    const cancel = vi.fn();
    const view = render(dialog(false, cancel));
    const trigger = screen.getByRole("button", { name: "Before dialog" });
    trigger.focus();
    view.rerender(dialog(true, cancel));

    const password = screen.getByLabelText("Current password");
    expect(document.activeElement).toBe(password);
    expect(document.body.style.overflow).toBe("hidden");
    fireEvent.keyDown(document, { key: "Tab", shiftKey: true });
    expect(document.activeElement).toBe(screen.getByRole("button", { name: "Cancel" }));
    fireEvent.keyDown(document, { key: "Escape" });
    expect(cancel).toHaveBeenCalledTimes(1);

    view.rerender(dialog(false, cancel));
    expect(document.body.style.overflow).toBe("");
    expect(document.activeElement).toBe(trigger);
  });

  it("does not dismiss an in-flight operation with Escape", () => {
    const cancel = vi.fn();
    render(dialog(true, cancel, true));
    fireEvent.keyDown(document, { key: "Escape" });
    expect(cancel).not.toHaveBeenCalled();
  });
});

describe("AdminStatusPill", () => {
  it("keeps multi-word status labels on one line", () => {
    render(<AdminStatusPill status="degraded">部分異常</AdminStatusPill>);
    expect(screen.getByText("部分異常").className).toContain("whitespace-nowrap");
    expect(screen.getByText("部分異常").className).toContain("shrink-0");
  });
});
