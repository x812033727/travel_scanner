import { fireEvent, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { Dialog } from "./ui";

describe("nested Dialog", () => {
  const original = Object.getOwnPropertyDescriptor(HTMLDialogElement.prototype, "showModal");
  beforeEach(() => {
    Object.defineProperty(HTMLDialogElement.prototype, "showModal", { configurable: true, value: function (this: HTMLDialogElement) { this.open = true; } });
  });
  afterEach(() => {
    if (original) Object.defineProperty(HTMLDialogElement.prototype, "showModal", original);
    else Reflect.deleteProperty(HTMLDialogElement.prototype, "showModal");
  });

  it.each(["cancel", "close"])("%s only closes the active child, preserving the reading drawer", (type) => {
    const closeDetail = vi.fn(); const closeOrganizer = vi.fn();
    render(<Dialog title="Reading detail" onClose={closeDetail}>
      <Dialog title="Organize saved item" onClose={closeOrganizer}>Saved content</Dialog>
    </Dialog>);
    const event = new Event(type, { bubbles: false, cancelable: type === "cancel" });
    fireEvent(screen.getByRole("dialog", { name: "Organize saved item" }), event);
    expect(closeOrganizer).toHaveBeenCalledTimes(1);
    expect(closeDetail).not.toHaveBeenCalled();
    if (type === "cancel") expect(event.defaultPrevented).toBe(true);
  });

  it("still closes the outer drawer on its own Escape cancel event", () => {
    const onClose = vi.fn();
    render(<Dialog title="Reading detail" onClose={onClose}>Content</Dialog>);
    fireEvent(screen.getByRole("dialog", { name: "Reading detail" }), new Event("cancel", { cancelable: true }));
    expect(onClose).toHaveBeenCalledTimes(1);
  });
});
