type HistoryHandler = (event: PopStateEvent) => void;
type NavigationHistoryBridge = { handlers: HistoryHandler[] };

declare global {
  interface Window {
    __mokaairNavigationHistory?: NavigationHistoryBridge;
  }
}

// Static, nonce-protected head bootstrap: install an ordinary bubble listener before
// the router hydrates. It does nothing until a draft subscribes, and never changes
// the router's listeners, history state, or event methods.
export const NAVIGATION_HISTORY_BOOTSTRAP_SCRIPT = `(function(){if(window.__mokaairNavigationHistory)return;var b={handlers:[]};window.__mokaairNavigationHistory=b;window.addEventListener("popstate",function mokaairHistoryBridge(e){var h=b.handlers[b.handlers.length-1];if(h)h(e)})})()`;

export function subscribeNavigationHistory(handler: HistoryHandler): () => void {
  let bridge = window.__mokaairNavigationHistory;
  if (!bridge) {
    // Standalone component hosts may not render LocaleLayout. The application uses
    // the earlier head bootstrap; this fallback does not promise router precedence.
    bridge = { handlers: [] };
    window.__mokaairNavigationHistory = bridge;
    const handlers = bridge.handlers;
    window.addEventListener("popstate", function mokaairHistoryBridge(event) {
      handlers.at(-1)?.(event);
    });
  }
  const handlers = bridge.handlers;
  handlers.push(handler);
  return () => {
    const index = handlers.indexOf(handler);
    if (index >= 0) handlers.splice(index, 1);
  };
}
