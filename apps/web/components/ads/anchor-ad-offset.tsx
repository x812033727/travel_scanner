"use client";

import { useEffect } from "react";

export const ANCHOR_BOTTOM_PROPERTY = "--ad-anchor-bottom";
export const ANCHOR_TOP_PROPERTY = "--ad-anchor-top";

/** A fixed unit covering this much of the viewport or more is a vignette, not an anchor. */
const OVERLAY_FRACTION = 0.5;
/** Sub-pixel rounding at the viewport edge. */
const EDGE = 2;

/**
 * How much of the top and bottom edge of the viewport Google's anchor ad covers right now.
 *
 * Read from geometry, not from the tag's own `data-anchor-*` attributes, which are not
 * documented and can change without notice. An anchor is an `ins.adsbygoogle` that is
 * `position: fixed` and touches one edge of the viewport; a collapsed anchor that has slid
 * partly out of view counts only for the part still showing.
 */
export function measureAnchorAds(doc: Document, viewportHeight: number): { top: number; bottom: number } {
  let top = 0;
  let bottom = 0;
  for (const unit of Array.from(doc.querySelectorAll<HTMLElement>("ins.adsbygoogle"))) {
    if (doc.defaultView?.getComputedStyle(unit).position !== "fixed") continue;
    const rect = unit.getBoundingClientRect();
    const visible = Math.min(rect.bottom, viewportHeight) - Math.max(rect.top, 0);
    if (visible <= 0 || visible >= viewportHeight * OVERLAY_FRACTION) continue;
    if (rect.bottom >= viewportHeight - EDGE) bottom = Math.max(bottom, visible);
    else if (rect.top <= EDGE) top = Math.max(top, visible);
  }
  return { top: Math.round(top), bottom: Math.round(bottom) };
}

/**
 * Moves the site's own fixed chrome out from under Google's anchor ad.
 *
 * The anchor sits above everything (z-index 2147483647), so on a phone it would cover the
 * bottom navigation and, at the top, the sticky header. This publishes how much of each edge
 * it covers as two custom properties on `<html>`, and `globals.css` offsets the navigation,
 * the header and the page's bottom padding by them. Both are removed again when the anchor is
 * closed or gone.
 *
 * Mounted by `AdsenseLoader`, so it only ever exists in the isolated advertising document.
 */
export function AnchorAdOffset() {
  useEffect(() => {
    const root = document.documentElement;
    const watched = new Set<Element>();
    let frame = 0;
    const apply = () => {
      frame = 0;
      const { top, bottom } = measureAnchorAds(document, window.innerHeight);
      for (const [property, value] of [[ANCHOR_TOP_PROPERTY, top], [ANCHOR_BOTTOM_PROPERTY, bottom]] as const) {
        if (value > 0) root.style.setProperty(property, `${value}px`);
        else root.style.removeProperty(property);
      }
    };
    const schedule = () => {
      if (!frame) frame = window.requestAnimationFrame(apply);
    };
    // Each unit's own style changes (shown, collapsed, closed) and its slide-in transition.
    const unitObserver = new MutationObserver(schedule);
    const resizeObserver = typeof ResizeObserver === "undefined" ? null : new ResizeObserver(schedule);
    const watch = () => {
      for (const unit of Array.from(document.querySelectorAll("ins.adsbygoogle"))) {
        if (watched.has(unit)) continue;
        watched.add(unit);
        unitObserver.observe(unit, { attributes: true });
        resizeObserver?.observe(unit);
        unit.addEventListener("transitionend", schedule);
      }
      schedule();
    };
    // The tag inserts its overlay units itself, some time after the page has loaded.
    const insertions = new MutationObserver(watch);
    insertions.observe(document.body, { childList: true, subtree: true });
    window.addEventListener("resize", schedule);
    watch();
    return () => {
      insertions.disconnect();
      unitObserver.disconnect();
      resizeObserver?.disconnect();
      for (const unit of watched) unit.removeEventListener("transitionend", schedule);
      window.removeEventListener("resize", schedule);
      if (frame) window.cancelAnimationFrame(frame);
      root.style.removeProperty(ANCHOR_TOP_PROPERTY);
      root.style.removeProperty(ANCHOR_BOTTOM_PROPERTY);
    };
  }, []);
  return null;
}
