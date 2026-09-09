import { act, cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { DiscoveryPreferenceEditor } from "./preferences";

const mock = vi.hoisted(() => ({ api: vi.fn(), guard: vi.fn() }));
vi.mock("@/lib/navigation-guard", () => ({ useNavigationGuard: mock.guard }));
vi.mock("@/lib/api", async (original) => ({ ...await original<object>(), api: mock.api }));
vi.mock("@/lib/discovery", async (original) => ({ ...await original<object>(), useDiscoveryResource: (path: string) => ({ data: path === "/discovery/preferences" ? { version: 1, destinations: [], topics: [], include_saved: true, include_following: true } : { destinations: [], topics: [] }, reload: vi.fn() }) }));
beforeEach(() => {
  mock.api.mockReset(); mock.guard.mockReset();
  vi.spyOn(window, "confirm").mockReturnValue(false);
  Object.defineProperty(HTMLDialogElement.prototype, "showModal", { configurable: true, value: function (this: HTMLDialogElement) { this.open = true; } });
});
afterEach(() => { cleanup(); vi.restoreAllMocks(); });

describe("interest draft closure", () => {
  it.each(["button", "Escape", "backdrop"])("keeps changes after cancelling %s and closes only after explicit discard", (method) => {
    const close = vi.fn(); render(<DiscoveryPreferenceEditor onClose={close} onSaved={vi.fn()} />);
    const saved = screen.getByRole("checkbox", { name: "參考我的收藏" }); fireEvent.click(saved);
    const dialog = screen.getByRole("dialog");
    const dismiss = () => {
      if (method === "button") fireEvent.click(screen.getByRole("button", { name: "關閉" }));
      else if (method === "Escape") fireEvent(dialog, new Event("cancel", { cancelable: true }));
      else { vi.spyOn(dialog, "getBoundingClientRect").mockReturnValue({ left: 20, top: 20, right: 200, bottom: 200 } as DOMRect); fireEvent(dialog, new MouseEvent("pointerdown", { bubbles: true, clientX: 1, clientY: 1 })); fireEvent.click(dialog, { clientX: 1, clientY: 1 }); }
    };
    dismiss(); expect(close).not.toHaveBeenCalled(); expect((saved as HTMLInputElement).checked).toBe(false); expect(mock.api).not.toHaveBeenCalled();
    vi.mocked(window.confirm).mockReturnValue(true); dismiss(); expect(close).toHaveBeenCalledOnce(); expect(mock.api).not.toHaveBeenCalled();
  });

  it("does not close an in-flight save and keeps the draft when it fails", async () => {
    let reject: (reason: Error) => void = () => {};
    mock.api.mockImplementation(() => new Promise((_resolve, fail) => { reject = fail; }));
    const close = vi.fn(); render(<DiscoveryPreferenceEditor onClose={close} onSaved={vi.fn()} />);
    fireEvent.click(screen.getByRole("checkbox", { name: "參考我的收藏" })); fireEvent.click(screen.getByRole("button", { name: "儲存興趣" }));
    fireEvent.click(screen.getByRole("button", { name: "關閉" })); expect(close).not.toHaveBeenCalled(); expect(window.confirm).not.toHaveBeenCalled();
    await act(async () => reject(new Error("fixture unavailable")));
    expect(screen.getByRole("alert")).toBeTruthy(); expect((screen.getByRole("checkbox", { name: "參考我的收藏" }) as HTMLInputElement).checked).toBe(false);
  });
});
