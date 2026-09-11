import { useEffect, useState } from "react";
import { act, cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { Dialog } from "@/components/community/ui";
import { DiscoveryDetailBoundary, useDiscoveryDetailNavigation } from "./detail-drawer";

const FOOD_ID = "11111111-1111-4111-8111-111111111111";
const MERCHANT_ID = "22222222-2222-4222-8222-222222222222";
const FILTERS = "q=%E5%A3%BD%E5%8F%B8&destination=fukuoka&type=food";
const originalShowModal = Object.getOwnPropertyDescriptor(HTMLDialogElement.prototype, "showModal");
const mock = vi.hoisted(() => ({
  query: "", path: "/explore", back: vi.fn(), replace: vi.fn(),
  ready: new Set<string>(), pending: new Map<string, () => void>(),
  frames: new Map<number, FrameRequestCallback>(), nextFrame: 1,
  childDialog: false, closeChild: vi.fn(),
}));

vi.mock("next/navigation", () => ({ useSearchParams: () => new URLSearchParams(mock.query) }));
vi.mock("@/i18n/navigation", () => ({
  usePathname: () => mock.path,
  useRouter: () => ({ back: mock.back, replace: mock.replace }),
}));
vi.mock("./card", () => ({
  DiscoveryDetails: (props: { kind: string; id: string; returnTo: string }) => <AsyncDetails {...props} />,
}));

function contentQuery(kind: "food" | "merchant", id: string) {
  const params = new URLSearchParams(FILTERS);
  params.set("content", `${kind}:${id}`);
  return params.toString();
}
function detailHref(kind: "food" | "merchant", id: string) {
  return `${mock.path}?${contentQuery(kind, id)}`;
}

// Match the real child's contract: its body/ref is absent until the request resolves.
// Deliberately remount links so restoration cannot use a stale HTMLElement reference.
function AsyncDetails({ kind, id }: { kind: string; id: string; returnTo: string }) {
  const navigation = useDiscoveryDetailNavigation();
  const [ready, setReady] = useState(() => mock.ready.has(id));
  useEffect(() => {
    if (ready) return;
    const resolve = () => setReady(true);
    mock.pending.set(id, resolve);
    return () => { if (mock.pending.get(id) === resolve) mock.pending.delete(id); };
  }, [id, ready]);
  if (!ready) return <p role="status">Loading {kind}</p>;
  return <div data-discovery-detail-body ref={navigation?.restoreDetails}>
    <h2 tabIndex={-1}>{kind === "food" ? "Sushi detail" : "Sakai detail"}</h2>
    {mock.childDialog && <Dialog title="Nested child" onClose={mock.closeChild}><button type="button">Child control</button></Dialog>}
    {kind === "food" && <a href={detailHref("merchant", MERCHANT_ID)}
      data-discovery-detail-target={`merchant:${MERCHANT_ID}`}
      onClick={(event) => {
        event.preventDefault();
        navigation?.remember(event.currentTarget, detailHref("merchant", MERCHANT_ID));
      }}>Sakai merchant</a>}
  </div>;
}
function ListTrigger() {
  const navigation = useDiscoveryDetailNavigation();
  return <>
    <input aria-label="Retained food search" defaultValue="壽司" />
    <button type="button" onClick={(event) => navigation?.remember(event.currentTarget, detailHref("food", FOOD_ID))}>Open sushi</button>
  </>;
}
function Harness() {
  return <DiscoveryDetailBoundary><ListTrigger /></DiscoveryDetailBoundary>;
}
function flushFrames() {
  act(() => {
    const pending = [...mock.frames.values()];
    mock.frames.clear();
    for (const callback of pending) callback(performance.now());
  });
}
function navigate(view: ReturnType<typeof render>, query: string, flush = true) {
  mock.query = query;
  view.rerender(<Harness />);
  if (flush) flushFrames();
}
function closeDrawer() {
  fireEvent.click(within(screen.getByRole("dialog")).getByRole("button", { name: "關閉" }));
}
function openFood(view: ReturnType<typeof render>) {
  fireEvent.click(screen.getByRole("button", { name: "Open sushi" }));
  navigate(view, contentQuery("food", FOOD_ID));
}
function openMerchant(view: ReturnType<typeof render>) {
  fireEvent.click(screen.getByRole("link", { name: "Sakai merchant" }));
  navigate(view, contentQuery("merchant", MERCHANT_ID));
}

beforeEach(() => {
  mock.query = FILTERS; mock.path = "/explore";
  mock.back.mockReset(); mock.replace.mockReset();
  mock.ready.clear(); mock.ready.add(FOOD_ID); mock.ready.add(MERCHANT_ID);
  mock.pending.clear(); mock.frames.clear(); mock.nextFrame = 1;
  mock.childDialog = false; mock.closeChild.mockReset();
  Object.defineProperty(HTMLDialogElement.prototype, "showModal", {
    configurable: true,
    value: function (this: HTMLDialogElement) { this.setAttribute("open", ""); },
  });
  vi.stubGlobal("requestAnimationFrame", (callback: FrameRequestCallback) => {
    const id = mock.nextFrame++; mock.frames.set(id, callback); return id;
  });
  vi.stubGlobal("cancelAnimationFrame", (id: number) => { mock.frames.delete(id); });
});
afterEach(() => {
  cleanup(); flushFrames(); vi.restoreAllMocks(); vi.unstubAllGlobals();
  if (originalShowModal) Object.defineProperty(HTMLDialogElement.prototype, "showModal", originalShowModal);
  else Reflect.deleteProperty(HTMLDialogElement.prototype, "showModal");
});

describe("discovery detail history and focus", () => {
  it("closes a directly opened detail with replace and preserves every list filter", () => {
    mock.path = "/foods";
    mock.query = `${contentQuery("food", FOOD_ID)}&cursor=opaque-value&locale=ja`;
    render(<Harness />); flushFrames();
    closeDrawer();
    expect(mock.replace).toHaveBeenCalledExactlyOnceWith(
      `/foods?${FILTERS}&cursor=opaque-value&locale=ja`, { scroll: false },
    );
    expect(mock.back).not.toHaveBeenCalled();
  });

  it("closes owned list-to-food-to-merchant navigation one history entry at a time", () => {
    const view = render(<Harness />);
    openFood(view); openMerchant(view);
    closeDrawer();
    expect(mock.back).toHaveBeenCalledTimes(1);
    navigate(view, contentQuery("food", FOOD_ID));
    expect(screen.getByRole("heading", { name: "Sushi detail" })).toBeTruthy();
    closeDrawer();
    expect(mock.back).toHaveBeenCalledTimes(2);
    expect(mock.replace).not.toHaveBeenCalled();
    navigate(view, FILTERS);
    expect(screen.queryByRole("dialog")).toBeNull();
  });

  it("consumes a non-cancelable native cancel/close pair and rapid close taps only once per route", () => {
    const view = render(<Harness />);
    openFood(view); openMerchant(view);
    const dialog = screen.getByRole("dialog");
    // CloseWatcher may emit close even though a non-cancelable cancel handler
    // called preventDefault. Both events reach the route owner before it commits.
    fireEvent(dialog, new Event("cancel", { cancelable: false }));
    fireEvent(dialog, new Event("close"));
    closeDrawer(); closeDrawer();
    expect(mock.back).toHaveBeenCalledTimes(1);
    navigate(view, contentQuery("food", FOOD_ID));
    closeDrawer(); closeDrawer();
    expect(mock.back).toHaveBeenCalledTimes(2);
    navigate(view, FILTERS);
    openFood(view);
    closeDrawer(); closeDrawer();
    expect(mock.back).toHaveBeenCalledTimes(3);
    expect(mock.replace).not.toHaveBeenCalled();
  });

  it("deduplicates direct URL replacement until the route changes", () => {
    mock.query = contentQuery("food", FOOD_ID);
    const view = render(<Harness />); flushFrames();
    closeDrawer(); closeDrawer();
    expect(mock.replace).toHaveBeenCalledTimes(1);
    navigate(view, contentQuery("merchant", MERCHANT_ID));
    closeDrawer(); closeDrawer();
    expect(mock.replace).toHaveBeenCalledTimes(2);
    expect(mock.back).not.toHaveBeenCalled();
  });

  it("prevents the keyboard Escape default before native cancel/close while retaining the nested dialog", () => {
    const view = render(<Harness />);
    openFood(view); openMerchant(view);
    const dialog = screen.getByRole("dialog");
    const nativeCancel = vi.fn();
    dialog.addEventListener("cancel", nativeCancel);
    const escape = new KeyboardEvent("keydown", { key: "Escape", bubbles: true, cancelable: true });
    const allowDefault = fireEvent(screen.getByRole("heading", { name: "Sakai detail" }), escape);
    // Model the browser default rather than making jsdom invent CloseWatcher.
    if (allowDefault) {
      fireEvent(dialog, new Event("cancel", { cancelable: false }));
      fireEvent(dialog, new Event("close"));
    }
    expect(allowDefault).toBe(false);
    expect(escape.defaultPrevented).toBe(true);
    expect(nativeCancel).not.toHaveBeenCalled();
    expect(mock.back).toHaveBeenCalledTimes(1);
    expect((dialog as HTMLDialogElement).open).toBe(true);
    navigate(view, contentQuery("food", FOOD_ID));
    expect(screen.getByRole("dialog")).toBe(dialog);
    expect(screen.getByRole("link", { name: "Sakai merchant" })).toBe(document.activeElement);
    fireEvent.keyDown(screen.getByRole("link", { name: "Sakai merchant" }), { key: "Escape" });
    expect(mock.back).toHaveBeenCalledTimes(2);
    navigate(view, FILTERS);
    expect(screen.getByRole("button", { name: "Open sushi" })).toBe(document.activeElement);
  });

  it("leaves consumed, composing and non-Escape keyboard events to their controls", () => {
    const view = render(<Harness />); openFood(view);
    const heading = screen.getByRole("heading", { name: "Sushi detail" });
    const consumed = new KeyboardEvent("keydown", { key: "Escape", bubbles: true, cancelable: true });
    consumed.preventDefault();
    fireEvent(heading, consumed);
    expect(fireEvent.keyDown(heading, { key: "Escape", isComposing: true })).toBe(true);
    expect(fireEvent.keyDown(heading, { key: "Enter" })).toBe(true);
    expect(mock.back).not.toHaveBeenCalled();
    expect(mock.replace).not.toHaveBeenCalled();
  });

  it("does not intercept Escape for a top-layer child dialog", () => {
    mock.childDialog = true;
    const view = render(<Harness />); openFood(view);
    const child = screen.getByRole("dialog", { name: "Nested child" });
    const escape = new KeyboardEvent("keydown", { key: "Escape", bubbles: true, cancelable: true });
    expect(fireEvent(within(child).getByRole("button", { name: "Child control" }), escape)).toBe(true);
    expect(escape.defaultPrevented).toBe(false);
    fireEvent(child, new Event("cancel", { cancelable: true }));
    expect(mock.closeChild).toHaveBeenCalledTimes(1);
    expect(mock.back).not.toHaveBeenCalled();
    expect(mock.replace).not.toHaveBeenCalled();
  });

  it("restores the remounted merchant link and independently scrolling body after async browser back", async () => {
    const view = render(<Harness />);
    openFood(view);
    const oldLink = screen.getByRole("link", { name: "Sakai merchant" });
    const oldBody = oldLink.closest<HTMLElement>("[data-discovery-detail-body]")!;
    oldBody.scrollTop = 684;
    (screen.getByRole("dialog") as HTMLDialogElement).scrollTop = 23;
    oldLink.focus();
    openMerchant(view);
    expect(oldLink.isConnected).toBe(false);
    expect(screen.getByRole("heading", { name: "Sakai detail" })).toBe(document.activeElement);
    mock.ready.delete(FOOD_ID);
    // An actual browser popstate changes the URL without invoking the close button.
    navigate(view, contentQuery("food", FOOD_ID));
    expect(screen.getByRole("status").textContent).toContain("Loading food");
    expect(screen.queryByRole("link", { name: "Sakai merchant" })).toBeNull();
    expect(document.body.style.overflow).toBe("hidden");
    await act(async () => { await Promise.resolve(); mock.pending.get(FOOD_ID)!(); });
    flushFrames();
    const restored = screen.getByRole("link", { name: "Sakai merchant" });
    expect(restored).not.toBe(oldLink);
    expect(document.activeElement).toBe(restored);
    expect(restored.closest<HTMLElement>("[data-discovery-detail-body]")!.scrollTop).toBe(684);
    expect(screen.getByRole("dialog").scrollTop).toBe(23);
    expect(mock.back).not.toHaveBeenCalled();
    expect(mock.replace).not.toHaveBeenCalled();
  });

  it("returns focus to the original list trigger only when the final detail closes", () => {
    document.body.style.overflow = "auto";
    const view = render(<Harness />);
    const trigger = screen.getByRole("button", { name: "Open sushi" });
    const search = screen.getByRole("textbox", { name: "Retained food search" });
    trigger.focus();
    openFood(view); openMerchant(view);
    closeDrawer(); navigate(view, contentQuery("food", FOOD_ID));
    expect(document.activeElement).toBe(screen.getByRole("link", { name: "Sakai merchant" }));
    expect(document.activeElement).not.toBe(trigger);
    expect(document.body.style.overflow).toBe("hidden");
    closeDrawer(); navigate(view, FILTERS);
    expect(document.activeElement).toBe(trigger);
    expect(screen.getByRole("textbox", { name: "Retained food search" })).toBe(search);
    expect((search as HTMLInputElement).value).toBe("壽司");
    expect(document.body.style.overflow).toBe("auto");
    document.body.style.overflow = "";
  });

  it("does not let a delayed frame from an unmounted parent steal child focus", () => {
    const view = render(<Harness />);
    fireEvent.click(screen.getByRole("button", { name: "Open sushi" }));
    navigate(view, contentQuery("food", FOOD_ID), false);
    const obsoleteHeading = screen.getByRole("heading", { name: "Sushi detail" });
    fireEvent.click(screen.getByRole("link", { name: "Sakai merchant" }));
    navigate(view, contentQuery("merchant", MERCHANT_ID), false);
    expect(obsoleteHeading.isConnected).toBe(false);
    flushFrames();
    expect(document.activeElement).toBe(screen.getByRole("heading", { name: "Sakai detail" }));
  });

  it("forgets prior detail ownership when a fresh list journey begins", () => {
    const view = render(<Harness />);
    openFood(view); openMerchant(view);
    navigate(view, FILTERS);
    openFood(view);
    // This old merchant URL was not opened by the new journey's list or detail links.
    navigate(view, contentQuery("merchant", MERCHANT_ID));
    closeDrawer();
    expect(mock.replace).toHaveBeenCalledExactlyOnceWith(`/explore?${FILTERS}`, { scroll: false });
    expect(mock.back).not.toHaveBeenCalled();
  });
});
