// Flat line icons a card may carry: one simple object beside a word, a step or a point, the way
// the reference channel's slides put a small drawing next to every idea (docs/videos/PAPER.md).
//
// Each is a 24x24 stroke drawing in the current text colour, so it takes the card's palette on
// either ground and holds no text for the font check to cover. A card asks for one by name
// (`icon: "folder"`); templates.mjs draws it and carries ICON_CSS in the page only then, so no
// card without an icon changes a byte. This file imports nothing.

const STROKE = 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"';

export const ICONS = {
  folder: '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
  file: '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/>',
  document: '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
  checklist: '<path d="M10 6h11M10 12h11M10 18h11"/><path d="M3 6l1.5 1.5L7 5M3 12l1.5 1.5L7 11M3 18l1.5 1.5L7 17"/>',
  terminal: '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 9l3 3-3 3M13 15h4"/>',
  clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
  person: '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
  warning: '<path d="M12 3l10 18H2z"/><path d="M12 10v4M12 17.5v.5"/>',
  book: '<path d="M4 4h6a2 2 0 0 1 2 2v14a2 2 0 0 0-2-2H4zM20 4h-6a2 2 0 0 0-2 2v14a2 2 0 0 1 2-2h6z"/>',
  gear: '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/>',
  search: '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
  chat: '<path d="M4 5h16v11H9l-5 4z"/>',
  globe: '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
  lock: '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
  lightning: '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
  arrow: '<path d="M4 12h16M13 5l7 7-7 7"/>',
};

export const ICON_NAMES = Object.keys(ICONS);
export const isIconName = (value) => typeof value === "string" && Object.hasOwn(ICONS, value);

/** The icon's markup, sized by the font size where it is drawn (ICON_CSS). */
export function icon(name) {
  if (!isIconName(name)) throw new Error(`unknown icon ${name}`);
  return `<svg class="icon" viewBox="0 0 24 24" ${STROKE} aria-hidden="true">${ICONS[name]}</svg>`;
}

// Where each card puts its icon. In the page only when a card draws one, like TERMINAL_CSS.
export const ICON_CSS =
  ".icon{display:inline-block;width:1em;height:1em;vertical-align:-.12em;flex:none}" +
  ".t-big .ic{font-size:150px;line-height:1;color:var(--teal)}" +
  ".t-bullets .n.ic{background:transparent;color:var(--teal);font-size:68px}" +
  ".t-steps .step .ic{margin-top:14px;font-size:72px;line-height:1;color:var(--teal)}" +
  ".card h3 .icon{margin-right:.3em;vertical-align:-.1em;font-size:.95em}";
