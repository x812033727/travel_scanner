import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import * as intl from "next-intl";
import { StrictMode, useState, type CSSProperties } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { plannerOverlayCopy } from "./planner/overlay-copy";
import { PlannerOverlay } from "./planner-overlay";
import { useModalSheet } from "@/lib/modal-sheet";

function LegacyChild() {
  const [open, setOpen] = useState(false);
  const ref = useModalSheet<HTMLDivElement>(open, () => setOpen(false));
  return <><button onClick={() => setOpen(true)}>Open hotel service</button>{open && <div ref={ref} role="dialog" aria-modal="true" aria-label="Legacy hotel service">
    <button aria-label="Close hotel service" onClick={() => setOpen(false)}>Close</button><button>Last hotel action</button>
  </div>}</>;
}

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
  afterEach(() => vi.restoreAllMocks());
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

  it("uses unique dialog descriptions and lets only the top layer handle Escape", async () => {
    const firstClose = vi.fn();
    const secondClose = vi.fn();
    render(<><PlannerOverlay open title="第一層" description="第一層說明" onClose={firstClose}>First</PlannerOverlay><PlannerOverlay open title="第二層" description="第二層說明" onClose={secondClose}>Second</PlannerOverlay></>);
    await nextFrame();
    const dialogs = [...document.querySelectorAll<HTMLElement>("[role='dialog']")];
    expect(new Set(dialogs.map((dialog) => dialog.getAttribute("aria-labelledby"))).size).toBe(2);
    expect(new Set(dialogs.map((dialog) => dialog.getAttribute("aria-describedby"))).size).toBe(2);
    for (const dialog of dialogs) {
      expect(document.getElementById(dialog.getAttribute("aria-labelledby")!)?.textContent).toContain("層");
    }
    expect(screen.queryByRole("dialog", { name: "第一層" })).toBeNull();
    expect(dialogs[0].parentElement?.inert).toBe(true);
    fireEvent.keyDown(document, { key: "Escape" });
    expect(secondClose).toHaveBeenCalledOnce();
    expect(firstClose).not.toHaveBeenCalled();
  });

  it("lets a nested legacy service sheet own Escape and Tab without closing tools or losing scroll lock", async () => {
    const close = vi.fn();
    const previousOverflow = document.body.style.overflow;
    const { unmount } = render(<PlannerOverlay open title="Tools" onClose={close}><LegacyChild /></PlannerOverlay>);
    await nextFrame();
    const opener = screen.getByRole("button", { name: "Open hotel service" });
    opener.focus(); fireEvent.click(opener);
    await nextFrame();
    const childClose = screen.getByRole("button", { name: "Close hotel service" });
    expect(document.activeElement).toBe(childClose);
    const last = screen.getByRole("button", { name: "Last hotel action" });
    last.focus(); fireEvent.keyDown(last, { key: "Tab" });
    expect(document.activeElement).toBe(childClose);
    fireEvent.keyDown(childClose, { key: "Escape" });
    expect(screen.queryByRole("dialog", { name: "Legacy hotel service" })).toBeNull();
    expect(screen.getByRole("dialog", { name: "Tools" })).toBeTruthy();
    expect(close).not.toHaveBeenCalled();
    expect(document.activeElement).toBe(opener);
    expect(document.body.style.overflow).toBe("hidden");
    fireEvent.keyDown(opener, { key: "Escape" });
    expect(close).toHaveBeenCalledOnce();
    unmount();
    expect(document.body.style.overflow).toBe(previousOverflow);
  });

  it("restores body styles and scroll after out-of-order unmounts, including Strict Mode", async () => {
    const oldStyle = document.body.getAttribute("style");
    document.body.style.overflow = "scroll";
    document.body.style.position = "relative";
    document.body.style.top = "7px";
    document.body.style.paddingRight = "9px";
    const startingStyle = document.body.getAttribute("style");
    let y = 420;
    vi.spyOn(window, "scrollY", "get").mockImplementation(() => y);
    const scroll = vi.spyOn(window, "scrollTo").mockImplementation(() => undefined);
    const { rerender, unmount } = render(<StrictMode><PlannerOverlay open title="A" onClose={() => undefined}>A</PlannerOverlay><PlannerOverlay open title="B" onClose={() => undefined}>B</PlannerOverlay></StrictMode>);
    await nextFrame();
    expect(document.body.style.overflow).toBe("hidden");
    expect(document.body.style.top).toBe("-420px");
    rerender(<StrictMode><PlannerOverlay open={false} title="A" onClose={() => undefined}>A</PlannerOverlay><PlannerOverlay open title="B" onClose={() => undefined}>B</PlannerOverlay></StrictMode>);
    expect(document.body.style.overflow).toBe("hidden");
    y = 0;
    unmount();
    expect(document.body.getAttribute("style")).toBe(startingStyle);
    expect(scroll).toHaveBeenCalledWith({ left: 0, top: 420, behavior: "instant" });
    if (oldStyle === null) document.body.removeAttribute("style");
    else document.body.setAttribute("style", oldStyle);
  });

  it("traps focus without including hidden or collapsed advanced controls", async () => {
    render(<PlannerOverlay open title="Focus" onClose={() => undefined}><button hidden>Hidden</button><details><summary>Advanced</summary><input aria-label="Hidden advanced input" /></details><button>Last action</button></PlannerOverlay>);
    await nextFrame();
    const close = screen.getByRole("button", { name: "關閉" });
    const last = screen.getByRole("button", { name: "Last action" });
    close.focus();
    fireEvent.keyDown(close, { key: "Tab", shiftKey: true });
    expect(document.activeElement).toBe(last);
    fireEvent.keyDown(last, { key: "Tab" });
    expect(document.activeElement).toBe(close);
  });

  it("honors expansion defaults on reopen and separates back from close", () => {
    const close = vi.fn();
    const back = vi.fn();
    const { rerender } = render(<PlannerOverlay open title="Route" expandable onBack={back} onClose={close}>Route</PlannerOverlay>);
    fireEvent.click(screen.getByRole("button", { name: "展開面板" }));
    expect(screen.getByRole("button", { name: "縮小面板" }).getAttribute("aria-expanded")).toBe("true");
    fireEvent.click(screen.getByRole("button", { name: "返回上一層" }));
    expect(back).toHaveBeenCalledOnce();
    expect(close).not.toHaveBeenCalled();
    rerender(<PlannerOverlay open={false} title="Route" expandable onClose={close}>Route</PlannerOverlay>);
    rerender(<PlannerOverlay open title="Route" expandable onClose={close}>Route</PlannerOverlay>);
    expect(screen.getByRole("button", { name: "展開面板" }).getAttribute("aria-expanded")).toBe("false");
  });

  it("ignores composing Escape and panel clicks but closes on the backdrop", async () => {
    const close = vi.fn();
    render(<PlannerOverlay open title="Route" onClose={close}>Content</PlannerOverlay>);
    await nextFrame();
    fireEvent.keyDown(document, { key: "Escape", isComposing: true });
    fireEvent.mouseDown(screen.getByRole("dialog", { name: "Route" }));
    expect(close).not.toHaveBeenCalled();
    fireEvent.mouseDown(screen.getByRole("dialog", { name: "Route" }).parentElement!);
    expect(close).toHaveBeenCalledOnce();
  });

  it("carries only planner theme variables into the portal and follows live theme changes", async () => {
    const close = vi.fn();
    const { rerender } = render(<main data-planner-theme="ocean" style={{ "--teal": "#27658a", "--unrelated": "do-not-copy" } as CSSProperties}><PlannerOverlay open title="Theme" onClose={close}>Themed content</PlannerOverlay></main>);
    const layer = screen.getByRole("dialog", { name: "Theme" }).parentElement!;
    expect(layer.parentElement).toBe(document.body);
    expect(layer.dataset.plannerTheme).toBe("ocean");
    expect(layer.style.getPropertyValue("--teal")).toBe("#27658a");
    expect(layer.style.getPropertyValue("--unrelated")).toBe("");
    rerender(<main data-planner-theme="sunset" style={{ "--teal": "#a94f38" } as CSSProperties}><PlannerOverlay open title="Theme" onClose={close}>Themed content</PlannerOverlay></main>);
    await waitFor(() => expect(layer.dataset.plannerTheme).toBe("sunset"));
    expect(layer.style.getPropertyValue("--teal")).toBe("#a94f38");
    expect(close).not.toHaveBeenCalled();
  });

  it.each(["en", "ja", "ko", "zh-TW", "zh-CN"])("localizes all overlay controls for %s", (locale) => {
    vi.spyOn(intl, "useLocale").mockReturnValue(locale);
    const copy = plannerOverlayCopy(locale);
    render(<PlannerOverlay open title="Trip" onClose={() => undefined} onBack={() => undefined} expandable>Content</PlannerOverlay>);
    expect(screen.getByRole("button", { name: copy.close })).toBeTruthy();
    expect(screen.getByRole("button", { name: copy.back })).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: copy.expand }));
    expect(screen.getByRole("button", { name: copy.collapse })).toBeTruthy();
  });
});
