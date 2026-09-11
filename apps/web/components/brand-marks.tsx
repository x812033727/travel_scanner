/**
 * Official identity marks for the third-party sign-in buttons.
 *
 * These are the providers' own logos, not decoration we are free to restyle: each
 * brand's sign-in guidelines fix the artwork, its colours and the clear space
 * around it. They are inline SVG rather than files in `public/` so a button keeps
 * its mark when the page is still loading, scales with the reader's text size,
 * and costs no extra request; `currentColor` is used only where the guidelines
 * actually allow the mark to take the button's foreground colour.
 *
 * Every mark is `aria-hidden`: the visible label beside it already names the
 * provider, so exposing the logo to a screen reader would only say it twice.
 */

type MarkProps = { className?: string };

const base = "h-5 w-5 shrink-0";

/**
 * Google's four-colour "G". Google's branding guidelines require this exact
 * artwork in its own colours — it may not be recoloured, outlined or redrawn,
 * which is why it does not follow the button's text colour.
 */
export function GoogleMark({ className }: MarkProps) {
  return (
    <svg className={`${base} ${className ?? ""}`} viewBox="0 0 48 48" aria-hidden="true" focusable="false">
      <path fill="#4285F4" d="M45.12 24.5c0-1.56-.14-3.06-.4-4.5H24v8.51h11.84c-.51 2.75-2.06 5.08-4.39 6.64v5.52h7.11c4.16-3.83 6.56-9.47 6.56-16.17z" />
      <path fill="#34A853" d="M24 46c5.94 0 10.92-1.97 14.56-5.33l-7.11-5.52c-1.97 1.32-4.49 2.1-7.45 2.1-5.73 0-10.58-3.87-12.31-9.07H4.34v5.7C7.96 41.07 15.4 46 24 46z" />
      <path fill="#FBBC05" d="M11.69 28.18c-.44-1.32-.69-2.73-.69-4.18s.25-2.86.69-4.18v-5.7H4.34C2.85 17.09 2 20.45 2 24s.85 6.91 2.34 9.88l7.35-5.7z" />
      <path fill="#EA4335" d="M24 10.75c3.23 0 6.13 1.11 8.41 3.29l6.31-6.31C34.91 4.18 29.93 2 24 2 15.4 2 7.96 6.93 4.34 14.12l7.35 5.7c1.73-5.2 6.58-9.07 12.31-9.07z" />
    </svg>
  );
}

/**
 * The LINE logo. LINE's guidelines fix the mark and the button green (#06C755);
 * on that green button the mark is the white knockout, so it takes the button's
 * own foreground colour rather than carrying a hard-coded white.
 */
export function LineMark({ className }: MarkProps) {
  return (
    <svg className={`${base} ${className ?? ""}`} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false">
      <path d="M24 10.17C24 4.83 18.62.49 12 .49S0 4.83 0 10.17c0 4.78 4.26 8.79 10.02 9.55.39.08.92.26 1.06.59.12.3.08.77.04 1.08l-.17 1.02c-.05.3-.24 1.18 1.05.64 1.29-.54 6.91-4.07 9.43-6.97C23.17 14.19 24 12.29 24 10.17zM7.75 13.1a.23.23 0 0 1-.23.23H4.16a.23.23 0 0 1-.23-.23V7.87c0-.13.1-.23.23-.23h.84c.13 0 .23.1.23.23v4.16h2.29c.13 0 .23.1.23.23v.84zm2.02 0a.23.23 0 0 1-.23.23h-.84a.23.23 0 0 1-.23-.23V7.87c0-.13.1-.23.23-.23h.84c.13 0 .23.1.23.23v5.23zm5.79 0a.23.23 0 0 1-.23.23h-.85a.22.22 0 0 1-.06-.01l-.01-.01h-.01l-.01-.01h-.01l-.01-.01-.01-.01-.01-.01a.23.23 0 0 1-.04-.04l-2.39-3.23v3.1a.23.23 0 0 1-.23.23h-.84a.23.23 0 0 1-.23-.23V7.87c0-.13.1-.23.23-.23h.87l.02.01h.01l.02.01.01.01h.01l.01.02h.01l.01.02.01.01.01.02 2.4 3.23V7.87c0-.13.1-.23.23-.23h.84c.13 0 .23.1.23.23v5.23zm4.64-4.39a.23.23 0 0 1-.23.23h-2.29v.88h2.29c.13 0 .23.11.23.23v.85a.23.23 0 0 1-.23.23h-2.29v.88h2.29c.13 0 .23.1.23.23v.84a.23.23 0 0 1-.23.23h-3.36a.23.23 0 0 1-.23-.23V7.87c0-.13.1-.23.23-.23h3.36c.13 0 .23.1.23.23v.84z" />
    </svg>
  );
}

/**
 * The Apple logo. Sign in with Apple's guidelines allow the mark in white on the
 * black button, so it follows the button's foreground colour. Drawing it rather
 * than typing the  character also keeps it legible on platforms with no Apple
 * font installed, where the character renders as a missing glyph.
 */
export function AppleMark({ className }: MarkProps) {
  return (
    <svg className={`${base} ${className ?? ""}`} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false">
      <path d="M17.05 12.54c-.03-2.73 2.23-4.04 2.33-4.1-1.27-1.86-3.25-2.11-3.95-2.14-1.68-.17-3.28 .99-4.13 .99-.85 0-2.16-.97-3.55-.94-1.83.03-3.51 1.06-4.45 2.7-1.9 3.29-.48 8.17 1.36 10.84.9 1.31 1.98 2.78 3.39 2.72 1.36-.05 1.88-.88 3.53-.88 1.65 0 2.11.88 3.55.85 1.47-.02 2.4-1.33 3.3-2.64 1.04-1.51 1.47-2.98 1.49-3.06-.03-.01-2.86-1.1-2.89-4.34zM14.4 4.51c.75-.91 1.25-2.17 1.11-3.43-1.08.04-2.38.72-3.15 1.62-.69.8-1.3 2.08-1.14 3.31 1.2.09 2.43-.61 3.18-1.5z" />
    </svg>
  );
}
