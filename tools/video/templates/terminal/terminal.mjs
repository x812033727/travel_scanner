// The `terminal` slide: a command typed at a prompt, then what the tool printed, for tutorials
// on terminal tools such as Claude Code or Codex.
//
// The output is evidence, not illustration: it is copied from a real run, and the scene carries
// the date of that run (`ran_on`) and the version of the tool that printed it (`tool_version`),
// both drawn under the window, so the fact checker can repeat the run and the viewer knows how old
// it is. The prompt is a bare "$" or ">": a user or host name never reaches a slide, and a home
// folder, a user@host prompt or an email address in the command or the output is refused.
//
// Motion is frozen like every other entrance (tools/video/render/browser.mjs seeks the page's
// animations to fixed 1/30 s steps): in the scene's first state the command is typed one
// character per frame, squeezed to fit the renderer's transition window when it is long, and the
// output that state shows comes in the frame after the last key. Each later reveal prints its
// part one line per frame. This file imports nothing from templates.mjs, which imports it.

export const TERMINAL_PROMPTS = ["$", ">"];
// A terminal's classic width, and what fits the window at the slide's type size.
export const TERMINAL_COLUMNS = 80;
export const TERMINAL_OUTPUT_LINES = 8;
export const TERMINAL_PARTS = 6;
// Up to this many rows (the command's included) of this many columns, the type is a third larger.
const LARGE_ROWS = 6;
const LARGE_COLUMNS = 60;

const FRAME = 1000 / 30;
// The renderer keeps 18 transition frames (MAX_TRANSITION_FRAMES), frame 0 being before any
// key; the command is fully typed by the last of them.
const TYPING_WINDOW = 17 * FRAME;

const isText = (value) => typeof value === "string" && value.trim().length > 0;
const escape = (text) => String(text).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[char]);
const ms = (value) => `${Number(value.toFixed(3))}ms`;

/** Columns a line takes in a terminal: East Asian wide characters take two. */
export function columns(text) {
  let total = 0;
  for (const char of text) {
    const code = char.codePointAt(0);
    const wide =
      (code >= 0x1100 && code <= 0x115f) || (code >= 0x2e80 && code <= 0xa4cf) || (code >= 0xac00 && code <= 0xd7a3) || (code >= 0xf900 && code <= 0xfaff) ||
      (code >= 0xfe30 && code <= 0xfe4f) || (code >= 0xff00 && code <= 0xff60) || (code >= 0xffe0 && code <= 0xffe6) || code >= 0x20000;
    total += wide ? 2 : 1;
  }
  return total;
}

// What would put a person on screen. ~ stands for a home folder; Shared and Public are not a user.
const PERSONAL = [
  [/(?:\/home\/|\/Users\/|[A-Za-z]:[\\/]Users[\\/])(?!(?:Shared|Public)\b)[^\s\\/"'`]+/i, "a home folder with a user name in it (write ~ instead)"],
  [/[\w.-]+@[\w.-]+:\s*[~/]/, "a user@host prompt"],
  [/[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.[a-z]{2,}\b/i, "an email address"],
];

function personal(text) {
  return PERSONAL.find(([pattern]) => pattern.test(text))?.[1] ?? null;
}

function isDate(value) {
  if (typeof value !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const date = new Date(`${value}T00:00:00Z`);
  return !Number.isNaN(date.getTime()) && date.toISOString().slice(0, 10) === value;
}

const outputLines = (output) => output.flatMap((part) => part.split("\n"));

export const TERMINAL_SPEC = {
  check: (data) => {
    const output = Array.isArray(data.output) && data.output.length >= 1 && data.output.length <= TERMINAL_PARTS && data.output.every(isText) ? data.output : null;
    const lines = output ? outputLines(output) : [];
    const command = isText(data.command) ? data.command : null;
    const commandShows = command && personal(command);
    const outputShows = output && personal(output.join("\n"));
    return [
      data.title !== undefined && !isText(data.title) && "title must be text",
      data.prompt !== undefined && !TERMINAL_PROMPTS.includes(data.prompt) && `prompt must be ${TERMINAL_PROMPTS.map((each) => `"${each}"`).join(" or ")}: a user or host name never goes on a slide`,
      !command && "command is required: the command as it was typed",
      command && (command.includes("\n") || command.includes("\t") || columns(command) > TERMINAL_COLUMNS - 2) && `command must be one line of at most ${TERMINAL_COLUMNS - 2} columns, without tabs`,
      !output && `output must be 1 to ${TERMINAL_PARTS} parts of text, copied from the real run (a part may hold several lines; each reveal shows the next part)`,
      output && lines.length > TERMINAL_OUTPUT_LINES && `output has ${lines.length} lines; at most ${TERMINAL_OUTPUT_LINES} fit, so show the part that matters`,
      output && lines.some((line) => columns(line) > TERMINAL_COLUMNS) && `an output line is longer than ${TERMINAL_COLUMNS} columns; break it where the terminal would, or cut it`,
      output && lines.some((line) => line.includes("\t")) && "output has a tab; expand it to spaces so the columns line up as they did",
      !isDate(data.ran_on) && "ran_on is required: the date (YYYY-MM-DD) the command was really run, so the output can be checked",
      !(isText(data.tool_version) && /\d/.test(data.tool_version) && !data.tool_version.includes("\n") && columns(data.tool_version) <= 40) &&
        "tool_version is required: the version of the tool that printed the output, as it reports it (for example 2.1.285 (Claude Code)), one line of at most 40 columns",
      commandShows && `the command shows ${commandShows}`,
      outputShows && `the output shows ${outputShows}`,
    ];
  },
  capacity: (data) => data.output.length,
};

/**
 * The slide's body. `state` is the template context: `first` and `visible(count)` from
 * templates.mjs; `heading` is the title's markup, made there.
 */
export function terminalBody(data, state, heading = "") {
  const prompt = data.prompt ?? "$";
  const show = state.visible(data.output.length);
  const parts = data.output.map((part, index) => ({ ...show(index), lines: part.split("\n") }));
  const chars = [...data.command];
  const step = Math.min(FRAME, TYPING_WINDOW / chars.length);
  // The output this state brings in starts the frame after the last key, or at once.
  const start = state.first ? chars.length * step + FRAME : 0;
  const command = state.first ? chars.map((char, index) => `<span class="k" style="animation-delay:${ms(index * step)}">${escape(char)}</span>`).join("") : escape(data.command);

  const printedBefore = parts.some((part) => part.shown && !part.entering);
  const printingNow = parts.some((part) => part.entering);
  // The caret waits after the command until the command has printed something.
  const caret = printedBefore ? "" : printingNow ? `<span class="caret gone" style="animation-delay:${ms(start)}"></span>` : '<span class="caret"></span>';

  let printed = 0;
  const rows = parts.flatMap((part) =>
    part.lines.map((line) => {
      const text = escape(line) || " ";
      if (!part.shown) return `<div class="row out" data-hidden>${text}</div>`;
      if (!part.entering) return `<div class="row out">${text}</div>`;
      return `<div class="row out print" style="animation-delay:${ms(start + printed++ * FRAME)}">${text}</div>`;
    }),
  );
  // A short session is set larger, to read on a phone; the limits keep it inside the slide.
  const lines = outputLines(data.output);
  const large = lines.length + 1 <= LARGE_ROWS && columns(`${prompt} ${data.command}`) <= LARGE_COLUMNS && lines.every((line) => columns(line) <= LARGE_COLUMNS);
  return [
    heading,
    '<div class="stage"><div class="term">',
    '<div class="bar"><i></i><i></i><i></i></div>',
    `<div class="screen${large ? " large" : ""}"><div class="row"><span class="ps">${escape(prompt)}</span> <span class="cmd">${command}</span>${caret}</div>${rows.join("")}</div>`,
    "</div>",
    `<div class="ran">Ran on ${escape(data.ran_on)} · ${escape(data.tool_version)}</div>`,
    "</div>",
  ].join("");
}

// Carried in the terminal slide's own <style> rather than the theme, so that adding the template
// changed no other video's frame keys (the keys hash the theme).
export const TERMINAL_CSS =
  ".t-terminal .stage{flex:1;min-height:0;display:flex;flex-direction:column;justify-content:center}" +
  ".t-terminal .term{background:var(--code-ground);border:2px solid var(--panel-edge);border-radius:24px}" +
  ".t-terminal .bar{display:flex;align-items:center;gap:12px;height:56px;padding:0 28px;border-bottom:2px solid var(--panel-edge)}" +
  ".t-terminal .bar i{width:16px;height:16px;border-radius:50%;background:rgba(247,241,232,.2)}" +
  ".t-terminal .screen{padding:26px 40px 30px;font-family:var(--mono);font-size:30px;line-height:1.45}" +
  ".t-terminal .screen.large{font-size:40px}" +
  ".t-terminal .row{white-space:pre;min-height:1.45em}" +
  ".t-terminal .ps{color:var(--teal);font-weight:700}" +
  ".t-terminal .cmd{color:var(--paper);font-weight:600}" +
  ".t-terminal .out{color:#d3dfdb}" +
  ".t-terminal .caret{display:inline-block;width:.6em;height:1.15em;margin-left:2px;vertical-align:-.22em;background:var(--orange)}" +
  ".t-terminal .ran{margin-top:22px;font-family:var(--mono);font-size:24px;color:var(--faint)}" +
  ".t-terminal .k{animation:term-key 1ms steps(1,end) both}" +
  ".t-terminal .print{animation:term-show 1ms steps(1,end) both}" +
  ".t-terminal .caret.gone{animation:term-gone 1ms steps(1,end) both}" +
  "@keyframes term-key{from{font-size:0}to{font-size:1em}}" +
  "@keyframes term-show{from{visibility:hidden}to{visibility:visible}}" +
  "@keyframes term-gone{from{visibility:visible}to{visibility:hidden}}";
