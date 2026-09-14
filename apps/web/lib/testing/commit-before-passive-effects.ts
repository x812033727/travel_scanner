import { vi } from "vitest";

/**
 * Stop a test in the gap React leaves between a commit and that commit's `useEffect`s.
 *
 * An update from a resolved promise renders on the default lane, and React 19 flushes passive
 * effects on the spot only for sync-lane commits; everything else waits for a later scheduler
 * task. When the render uses up the scheduler's 5 ms slice -- as the trip editor does on a busy
 * CI runner -- the page shows the new DOM while the effects that belong to it have not run, and
 * `waitFor`/`findBy` can hand control back exactly there. Four full-suite flakes were that gap:
 * a close guard one render behind, an Escape listener not attached yet, focus not yet moved.
 *
 * This makes the gap certain instead of a matter of load: the update runs outside `act` (the
 * way a fetch reaches React), the clock advances on every read so the scheduler always yields
 * after the commit, and control returns at the first macrotask where `committed()` is true.
 */
export async function commitBeforePassiveEffects(update: () => void, committed: () => boolean) {
  const scope = globalThis as { IS_REACT_ACT_ENVIRONMENT?: boolean };
  const actEnvironment = scope.IS_REACT_ACT_ENVIRONMENT;
  scope.IS_REACT_ACT_ENVIRONMENT = false;
  let clock = performance.now();
  const now = vi.spyOn(performance, "now").mockImplementation(() => (clock += 3));
  try {
    update();
    for (let ticks = 0; !committed(); ticks += 1) {
      if (ticks === 50) throw new Error("The update never reached the DOM");
      await new Promise((resolve) => setImmediate(resolve));
    }
  } finally {
    now.mockRestore();
    scope.IS_REACT_ACT_ENVIRONMENT = actEnvironment;
  }
}
