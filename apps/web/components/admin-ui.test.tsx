import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { AdminConfirmDialog, AdminDetailDrawer, AdminStatusPill } from "./admin-ui";

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

describe("AdminDetailDrawer under a confirmation", () => {
  function layers(drawerOpen: boolean, confirmOpen: boolean, onClose: () => void, onCancel: () => void) {
    return <>
      <AdminDetailDrawer open={drawerOpen} title="Member" onClose={onClose} closeLabel="Close drawer">
        <button type="button">Suspend member</button>
      </AdminDetailDrawer>
      <AdminConfirmDialog
        open={confirmOpen}
        title="Sensitive action"
        description="Verify this action"
        confirmationLabel="Confirmation"
        confirmation=""
        expectedConfirmation="CONFIRM"
        password=""
        passwordLabel="Current password"
        onConfirmationChange={() => undefined}
        onPasswordChange={() => undefined}
        onCancel={onCancel}
        onConfirm={() => undefined}
      />
    </>;
  }

  it("keeps Escape, Tab and the scroll lock on the layer that is on top", () => {
    const close = vi.fn();
    const cancel = vi.fn();
    const view = render(layers(true, false, close, cancel));
    view.rerender(layers(true, true, close, cancel));

    // Two independent document-level handlers used to both answer one Escape, so
    // confirming a suspension also threw away the member record behind it.
    fireEvent.keyDown(document, { key: "Escape" });
    expect(cancel).toHaveBeenCalledTimes(1);
    expect(close).not.toHaveBeenCalled();

    // The drawer's own button is still in the document; Tab must not offer it.
    const password = screen.getByLabelText("Current password");
    password.focus();
    fireEvent.keyDown(document, { key: "Tab", shiftKey: true });
    expect(document.activeElement).toBe(screen.getByRole("button", { name: "Cancel" }));

    // Closing the layer underneath must not unlock a page that is still covered.
    view.rerender(layers(false, true, close, cancel));
    expect(document.body.style.overflow).toBe("hidden");
    view.rerender(layers(false, false, close, cancel));
    expect(document.body.style.overflow).toBe("");
  });
});
