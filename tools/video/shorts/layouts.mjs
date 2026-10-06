// The look of a Short's cards, one theme for each series of the experiments line and one for the
// highlights (docs/videos/SHORTS.md §風險與對策).
//
// YouTube's monetization policy names content that "looks like it was made from a template" and
// feels repetitive after a few videos. What differs between two Shorts is first of all what they
// say; the themes make sure the three series and the highlights are also told apart at a glance
// on the contact sheet: their own colours, header, kicker, footer, and the way body rows are
// set. The safe area and every measurement of the build are the same for all of them.

const TEAL = {
  background: '#0b2026', text: '#f6f4e8', muted: '#8fc8bd', accent: '#50d2b7', highlight: '#ffb36a',
  glow: '#1f635960', row: '#16353a', rowBorder: '#397b73', caption: '#071a20eb', track: '#244348',
};

export const THEMES = Object.freeze({
  // Everyday questions answered by one real run: the look of the three pilots.
  'lab:daily': { id: 'lab-daily', brand: 'MOKAAIR / AI 真的可以？', kicker: '實測紀錄', footer: '原創實測', rows: 'stack', rule: '114px', glow: 'left:500px;top:-220px;width:850px;height:850px', colors: TEAL },
  // Two results side by side, chosen blind: rows alternate between the two sides.
  'lab:blind': {
    id: 'lab-blind', brand: 'MOKAAIR / AI 真的可以？', kicker: '成品盲選', footer: '盲選實測', rows: 'compare', rule: '220px', glow: 'left:-260px;top:-200px;width:900px;height:900px',
    colors: { background: '#17122b', text: '#f5f1ff', muted: '#b3a6dc', accent: '#a78bfa', highlight: '#f9d65c', glow: '#5b3fb060', row: '#241c45', rowBorder: '#6d55c4', caption: '#0e0a1eeb', track: '#33295c' },
  },
  // A prompt checked line by line: numbered rows.
  'lab:prompts': {
    id: 'lab-prompts', brand: 'MOKAAIR / AI 真的可以？', kicker: '提示驗證', footer: '提示實測', rows: 'numbered', rule: '60px', glow: 'left:420px;top:1100px;width:900px;height:900px',
    colors: { background: '#221a10', text: '#fff7e8', muted: '#d9c19a', accent: '#f0a531', highlight: '#7fe0c3', glow: '#8a5a1460', row: '#33270f', rowBorder: '#a3741c', caption: '#150f07eb', track: '#4a3a1a' },
  },
  // The part of a tutorial most worth keeping, leading back to the full video.
  cut: {
    id: 'cut', brand: 'MOKAAIR / 長片精華', kicker: '一分鐘重點', footer: '完整影片在說明欄', rows: 'stack', rule: '114px', glow: 'left:-300px;top:700px;width:1000px;height:1000px',
    colors: { background: '#0d1b2e', text: '#eef4ff', muted: '#9db4d6', accent: '#5aa9ff', highlight: '#ffd166', glow: '#1f4f8a60', row: '#15294a', rowBorder: '#3a6fb0', caption: '#07111feb', track: '#203a5e' },
  },
  // The Shorts of an illustrated slides video (docs/videos/ILLUSTRATED.md, the tech-story look):
  // deep teal, cream and amber, pointing every card to the long video.
  'cut:illustrated': {
    id: 'cut-illustrated', brand: 'MOKAAIR', kicker: '你以為 · 其實', footer: '完整故事在長片 ▶', rows: 'stack', rule: '114px', glow: 'left:-260px;top:900px;width:960px;height:960px',
    colors: { background: '#0f2f33', text: '#f7f1e3', muted: '#9fc3bd', accent: '#3fbfa8', highlight: '#f2a93b', glow: '#3fbfa833', row: '#173f44', rowBorder: '#3fbfa8', caption: '#08191ceb', track: '#23494e' },
  },
  // An explainer's Shorts (docs/videos/so-thats-why/look.md): the series' cream, ink navy,
  // stamp red and mustard, its name in the header, and every card pointing to the long video.
  'cut:sothatswhy': {
    id: 'cut-sothatswhy', brand: '原來如此事務所', kicker: '原來如此', footer: '完整版在長片 ▶', rows: 'stack', rule: '114px', glow: 'left:520px;top:-240px;width:860px;height:860px',
    colors: { background: '#1f2a44', text: '#f6efe3', muted: '#c9bfae', accent: '#d8452f', highlight: '#e8b64c', glow: '#d8452f33', row: '#2a3656', rowBorder: '#e8b64c', caption: '#141b2eeb', track: '#34405e' },
  },
});

// The entrance of a scene's first card (docs/videos/SHORTS.md §工具端, the same for every theme):
// each element of the content rises 28 px and fades in, the headline first, then the rule, then
// each row a step later, on an ease-out that never overshoots (no bounce). The stagger stops at
// the fifth element so the longest card settles inside the frames build.mjs captures
// (motion.mjs ENTRANCE_FRAMES): 4 × 40 + 240 = 400 ms, twelve frames. The animation is paused in
// the CSS: a card never moves on its own clock; the build seeks it (render/browser.mjs).
export const ENTRANCE = Object.freeze({ rise: 28, duration: 240, stagger: 40, staggerLimit: 4, easing: 'cubic-bezier(0.2, 0.7, 0.2, 1)' });

/** The CSS of the entrance: the `in` elements, each at its `--i` step of the stagger. */
export const entranceCss = () => `@keyframes rise{from{opacity:0;transform:translateY(${ENTRANCE.rise}px)}to{opacity:1;transform:none}}
.in{animation:rise ${ENTRANCE.duration}ms ${ENTRANCE.easing} both;animation-delay:calc(var(--i,0)*${ENTRANCE.stagger}ms);animation-play-state:paused}`;

/** The theme of a script: by series for an experiment, by line otherwise. */
export function themeOf(doc) {
  const line = doc?.schema_version === 1 ? 'lab' : doc?.line;
  return THEMES[`${line}:${doc?.series}`] ?? THEMES[line] ?? THEMES['lab:daily'];
}

/** Every character a theme puts on a card, for the font subset the build embeds. */
export const themeText = () => Object.values(THEMES).map((theme) => `${theme.brand}${theme.kicker}${theme.footer}`).join('');
