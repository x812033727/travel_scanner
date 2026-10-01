import { fireEvent, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { AdminBootstrap } from "@/lib/admin-operations";
import { adminOperationsCopy } from "@/lib/admin-operations-copy";
import { useModalSheet } from "@/lib/modal-sheet";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { AdminShell } from "./admin-shell";

vi.mock("./language-switcher", () => ({ LanguageSwitcher: () => null }));

const copy = adminOperationsCopy("zh-TW");
const bootstrap: AdminBootstrap = {
  admin_roles: ["owner"],
  admin_capabilities: ["admin.access", "dashboard.read", "content.read"],
  navigation: [
    { key: "dashboard", href: "/admin", group: "overview" },
    { key: "hotspots", href: "/admin/hotspots", group: "content" },
  ],
  pending_counts: {},
  system_status: {},
  environment: "test",
  can_deploy: false,
  can_manage_database: false,
};

function AdditionalSheet({ open, onClose }: { open: boolean; onClose: () => void }) {
  const ref = useModalSheet<HTMLDivElement>(open, onClose);
  return open ? <div ref={ref} role="dialog" aria-label="Additional sheet">
    <button onClick={onClose}>Close additional sheet</button>
  </div> : null;
}

function Harness({ topOpen = false, onTopClose = () => {}, showShell = true }) {
  return <AdminOperationsProvider bootstrap={bootstrap}>
    {showShell && <AdminShell><button>Original keyboard focus</button></AdminShell>}
    <AdditionalSheet open={topOpen} onClose={onTopClose} />
  </AdminOperationsProvider>;
}

function openCommand() {
  const trigger = screen.getByRole("button", { name: copy.command });
  trigger.focus();
  fireEvent.click(trigger);
  return { trigger, dialog: screen.getByRole("dialog", { name: copy.command }) };
}

describe("AdminShell command dialog", () => {
  afterEach(() => { window.localStorage.clear(); document.body.style.overflow = ""; });

  it("focuses search, traps Tab and closes from document Escape with focus restored", () => {
    render(<Harness />);
    const { trigger, dialog } = openCommand();
    const input = within(dialog).getByRole("textbox");
    expect(document.activeElement).toBe(input);
    const links = within(dialog).getAllByRole("link");
    const last = links.at(-1)!;
    last.focus();
    fireEvent.keyDown(document, { key: "Tab" });
    expect(document.activeElement).toBe(input);
    fireEvent.keyDown(document, { key: "Tab", shiftKey: true });
    expect(document.activeElement).toBe(last);
    expect(document.body.style.overflow).toBe("hidden");
    fireEvent.keyDown(document, { key: "Escape" });
    expect(screen.queryByRole("dialog")).toBeNull();
    expect(document.activeElement).toBe(trigger);
    expect(document.body.style.overflow).toBe("");
  });

  it("returns to the actual keyboard opener after Ctrl+K", () => {
    render(<Harness />);
    const opener = screen.getByRole("button", { name: "Original keyboard focus" });
    opener.focus();
    fireEvent.keyDown(window, { key: "k", ctrlKey: true });
    expect(document.activeElement).toBe(within(screen.getByRole("dialog")).getByRole("textbox"));
    fireEvent.keyDown(document, { key: "Escape" });
    expect(document.activeElement).toBe(opener);
  });

  it("leaves Escape to an active IME or a handler that already consumed it", () => {
    render(<Harness />);
    openCommand();
    fireEvent.keyDown(document, { key: "Escape", isComposing: true });
    expect(screen.getByRole("dialog", { name: copy.command })).toBeTruthy();
    const handled = new KeyboardEvent("keydown", { key: "Escape", cancelable: true });
    handled.preventDefault();
    fireEvent(document, handled);
    expect(screen.getByRole("dialog", { name: copy.command })).toBeTruthy();
  });

  it("lets only the top sheet handle Tab and Escape, retaining the lower scroll lock", () => {
    const closeTop = vi.fn();
    const view = render(<Harness onTopClose={closeTop} />);
    const { dialog } = openCommand();
    const input = within(dialog).getByRole("textbox");
    view.rerender(<Harness topOpen onTopClose={closeTop} />);
    const topButton = screen.getByRole("button", { name: "Close additional sheet" });
    fireEvent.keyDown(document, { key: "Tab" });
    expect(document.activeElement).toBe(topButton);
    fireEvent.keyDown(document, { key: "Escape" });
    expect(closeTop).toHaveBeenCalledOnce();
    expect(screen.getByRole("dialog", { name: copy.command })).toBe(dialog);
    view.rerender(<Harness onTopClose={closeTop} />);
    expect(document.activeElement).toBe(input);
    expect(document.body.style.overflow).toBe("hidden");
    fireEvent.keyDown(document, { key: "Escape" });
    expect(document.body.style.overflow).toBe("");
  });

  it("keeps an independent sheet locked when the command shell unmounts first", () => {
    document.body.style.overflow = "clip";
    const view = render(<Harness />);
    openCommand();
    view.rerender(<Harness topOpen />);
    view.rerender(<Harness topOpen showShell={false} />);
    expect(document.body.style.overflow).toBe("hidden");
    view.rerender(<Harness showShell={false} />);
    expect(document.body.style.overflow).toBe("clip");
  });
});
