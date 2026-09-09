import { runInNewContext } from "node:vm";
import { describe, expect, it, vi } from "vitest";
import { NAVIGATION_HISTORY_BOOTSTRAP_SCRIPT, subscribeNavigationHistory } from "./navigation-history";

describe("prepaint navigation history bridge", () => {
  it("installs exactly one ordinary bubble listener and is inert without subscribers", () => {
    const addEventListener = vi.fn();
    const host: Pick<Window, "__mokaairNavigationHistory"> & { addEventListener: typeof addEventListener } = { addEventListener };
    runInNewContext(NAVIGATION_HISTORY_BOOTSTRAP_SCRIPT, { window: host });
    runInNewContext(NAVIGATION_HISTORY_BOOTSTRAP_SCRIPT, { window: host });
    expect(addEventListener).toHaveBeenCalledOnce();
    const [type, listener, options] = addEventListener.mock.calls[0];
    expect(type).toBe("popstate");
    expect(options).toBeUndefined();
    expect(listener.name).toBe("mokaairHistoryBridge");
    const event = new PopStateEvent("popstate");
    const stop = vi.spyOn(event, "stopImmediatePropagation");
    listener(event);
    expect(stop).not.toHaveBeenCalled();
  });

  it("dispatches only to the top subscriber and restores the previous one on unsubscribe", () => {
    window.eval(NAVIGATION_HISTORY_BOOTSTRAP_SCRIPT);
    const first = vi.fn(); const second = vi.fn();
    const offFirst = subscribeNavigationHistory(first);
    const offSecond = subscribeNavigationHistory(second);
    try {
      const event = new PopStateEvent("popstate");
      window.dispatchEvent(event);
      expect(first).not.toHaveBeenCalled();
      expect(second).toHaveBeenCalledExactlyOnceWith(event);
      offSecond(); offSecond();
      window.dispatchEvent(event);
      expect(first).toHaveBeenCalledExactlyOnceWith(event);
      expect(second).toHaveBeenCalledOnce();
      offFirst();
      window.dispatchEvent(event);
      expect(first).toHaveBeenCalledOnce();
    } finally { offSecond(); offFirst(); }
  });
});
