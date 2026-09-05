import { useEffect, useRef } from "react";

// A card's share link ends in #hotspot-<id> or #merchant-<id>. The list arrives
// after the browser has already given up on the fragment, so bring the card into
// view once — and only once — as soon as it exists.
export function useSharedAnchor(ready: boolean) {
  const done = useRef(false);
  useEffect(() => {
    if (!ready || done.current) return;
    const id = window.location.hash.slice(1);
    if (!id) {
      done.current = true;
      return;
    }
    const target = document.getElementById(id);
    if (!target) return;
    done.current = true;
    target.scrollIntoView({ block: "center" });
    target.classList.add("shared-anchor-target");
    window.setTimeout(() => target.classList.remove("shared-anchor-target"), 2400);
  }, [ready]);
}
