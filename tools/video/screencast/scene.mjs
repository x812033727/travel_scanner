// The screencast template: a captured still in a frame, with the cursor, the highlight box, a
// click ripple and an optional zoom drawn on top as CSS animations.
//
// Every state of the scene is one capture (the lines' reveals step through them). In each state
// the cursor glides from where the last state left it to the capture's target, the target gets a
// box, and a target about to be clicked gets a ripple. The renderer freezes the animations frame by
// frame (tools/video/render/browser.mjs, at most MAX_TRANSITION_FRAMES), so a state's entrance is
// a fixed number of frames and the rest of the state holds its still: the same stills-and-
// transitions a slide makes, which assemble already turns into one segment per scene.
import { ORIGIN, SIZE, chrome, escapeHtml, page, richText } from "../templates/templates.mjs";

// Timings in ms. Everything ends by 600 ms, the renderer's 18-frame entrance limit at 30 fps.
export const MOVE_MS = 420;
export const HIGHLIGHT_DELAY_MS = 300;
export const HIGHLIGHT_MS = 240;
export const PRESS_DELAY_MS = 420;
export const PRESS_MS = 180;
export const ZOOM_MS = 540;
export const ENTRANCE_MS = Math.max(MOVE_MS, HIGHLIGHT_DELAY_MS + HIGHLIGHT_MS, PRESS_DELAY_MS + PRESS_MS, ZOOM_MS);
// Where the cursor comes in from when a scene first points at something: the bottom right corner.
export const REST = { x: 92, y: 94 };
// The highlight sits this far (in percent of the screen) outside its target.
const BOX_PAD = 0.5;

const pct = (value) => Math.round(value * 100) / 100;

/** A box in page pixels as percentages of the page. */
export function percentBox(box, viewport) {
  return { x: pct((box.x / viewport.width) * 100), y: pct((box.y / viewport.height) * 100), w: pct((box.w / viewport.width) * 100), h: pct((box.h / viewport.height) * 100) };
}

// The cursor's tip lands centred across the target and a little below its middle, so the arrow
// covers less of the label it points at.
const aim = (box) => ({ x: pct(box.x + box.w / 2), y: pct(box.y + box.h * 0.7) });

/**
 * The frame plan of a screencast scene: for each of its timeline states ({ reveal }), which
 * capture it shows and what moves on top, in percent of the screen. The cursor appears with the
 * first target and stays where the last one left it; the highlight and ripple belong to the state
 * whose capture has the target; zoom punches in on the target (or the centre) and back out at the
 * next capture.
 */
export function screencastPlan(manifest, states) {
  let cursor = null;
  return states.map((state) => {
    const capture = manifest.captures[state.reveal];
    if (!capture) throw new Error(`screencast state reveal ${state.reveal} has no capture (the manifest has ${manifest.captures.length})`);
    const box = capture.target ? percentBox(capture.target, manifest.viewport) : null;
    const from = box ? (cursor ?? REST) : cursor;
    const to = box ? aim(box) : cursor;
    cursor = to;
    const zoom = capture.zoom > 1 ? { scale: capture.zoom, origin: to ?? { x: 50, y: 50 } } : null;
    return {
      capture: state.reveal,
      file: capture.file,
      sha256: capture.sha256,
      cursor: to ? { from, to, moves: from.x !== to.x || from.y !== to.y } : null,
      highlight: box ? { x: pct(box.x - BOX_PAD), y: pct(box.y - BOX_PAD), w: pct(box.w + 2 * BOX_PAD), h: pct(box.h + 2 * BOX_PAD) } : null,
      press: Boolean(box && capture.press),
      zoom,
    };
  });
}

// The screen takes the slide from just under the chapter label: a page is read, not glanced at.
const CSS = [
  ".t-screencast{top:128px}",
  ".t-screencast .sc-frame{flex:1;min-height:0;display:flex;align-items:center;justify-content:center}",
  ".t-screencast .sc-screen{position:relative;height:100%;max-width:100%;aspect-ratio:16/9;border-radius:18px;overflow:hidden;border:2px solid var(--panel-edge);box-shadow:0 30px 80px rgba(0,0,0,.4);background:#fff}",
  ".sc-inner{position:absolute;inset:0}",
  ".sc-inner img{width:100%;height:100%;display:block}",
  ".sc-box{position:absolute;border:5px solid var(--orange);border-radius:10px;box-shadow:0 0 0 9999px rgba(8,24,25,.28),0 0 32px rgba(240,160,75,.6)}",
  ".sc-press{position:absolute;width:4.5%;aspect-ratio:1;border-radius:50%;border:5px solid var(--orange);opacity:0}",
  // The arrow's tip is at (2, 2) of its 24x36 box: shift it back onto the point.
  ".sc-cursor{position:absolute;width:2.4%;transform:translate(-8.3%,-5.6%);filter:drop-shadow(0 3px 6px rgba(0,0,0,.45))}",
  "@keyframes sc-glow{from{opacity:0;transform:scale(1.08)}to{opacity:1;transform:none}}",
  "@keyframes sc-press{from{opacity:.95;transform:translate(-50%,-50%) scale(.3)}to{opacity:0;transform:translate(-50%,-50%) scale(1.4)}}",
].join("");

const CURSOR =
  '<svg class="sc-cursor" viewBox="0 0 24 36" aria-hidden="true"><path d="M2 2 L2 30 L9 23.5 L13.5 34 L18 32 L13.6 21.6 L22.5 21.6 Z" fill="#fff" stroke="#111" stroke-width="2" stroke-linejoin="round"/></svg>';

const at = (point) => `left:${point.x}%;top:${point.y}%`;

/** The page-level CSS of one state: the shared rules plus this state's own moves. */
export function stateCss(plan) {
  const rules = [CSS];
  if (plan.cursor) {
    const { from, to, moves } = plan.cursor;
    rules.push(`.sc-cursor{${at(to)}}`);
    if (moves) {
      rules.push(`@keyframes sc-move{from{${at(from)}}to{${at(to)}}}`);
      rules.push(`.sc-cursor{animation:sc-move ${MOVE_MS}ms cubic-bezier(.3,.6,.2,1) both}`);
    }
  }
  if (plan.highlight) rules.push(`.sc-box{animation:sc-glow ${HIGHLIGHT_MS}ms ${HIGHLIGHT_DELAY_MS}ms ease-out both}`);
  // forwards, not both: before its delay the ripple must stay hidden, not sit at its first keyframe.
  if (plan.press) rules.push(`.sc-press{animation:sc-press ${PRESS_MS}ms ${PRESS_DELAY_MS}ms ease-out forwards}`);
  if (plan.zoom) {
    rules.push(`@keyframes sc-zoom{from{transform:scale(1)}to{transform:scale(${plan.zoom.scale})}}`);
    rules.push(`.sc-inner{transform-origin:${plan.zoom.origin.x}% ${plan.zoom.origin.y}%;animation:sc-zoom ${ZOOM_MS}ms cubic-bezier(.3,.6,.2,1) both}`);
  }
  return rules.join("");
}

/** The image URL of a capture, served from the work directory by the renderer's fake origin. */
export const captureUrl = (file) => `${ORIGIN}/work/${file.split("/").map(encodeURIComponent).join("/")}`;

/**
 * One state of a screencast scene as a complete page. `plan` is one entry of screencastPlan;
 * `state` carries what slideHtml's does: first, chapter, chapterNumber, chapterCount.
 */
export function screencastHtml(scene, plan, state) {
  const data = scene.data;
  const title = data.title ? `<h2 class="heading fit${state.first ? " enter" : ""}" style="--i:0">${richText(data.title)}</h2>` : "";
  const layers = [
    `<img src="${escapeHtml(captureUrl(plan.file))}" alt="">`,
    plan.highlight ? `<div class="sc-box" style="${at(plan.highlight)};width:${plan.highlight.w}%;height:${plan.highlight.h}%"></div>` : "",
    plan.press ? `<div class="sc-press" style="${at(plan.cursor.to)}"></div>` : "",
    plan.cursor ? CURSOR : "",
  ].join("");
  const caption = data.caption ? `<div class="caption-line">${richText(data.caption)}</div>` : "";
  const body = `${chrome(scene, state)}<main class="content t-screencast">${title}<div class="sc-frame"><div class="sc-screen"><div class="sc-inner">${layers}</div></div></div>${caption}</main>`;
  return page(body, SIZE, stateCss(plan));
}
