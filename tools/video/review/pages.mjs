// The two pages the site owner reviews with, as self-contained HTML files in the work directory:
// review/audio.html to listen to every line and flag the ones read wrong, and review/final.html to
// watch the finished video with its lines alongside. Nothing is loaded from the network, and both
// open straight from disk.
import { characterOf } from "../core/drama.mjs";
import { eachLine, spokenText } from "../core/schema.mjs";
import { formatClock, frameToSeconds } from "../core/timeline.mjs";

export const escapeHtml = (text) => String(text).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[char]);

/** A drama line's text with its speaker in front, 【精衛】 style, so the owner knows whose voice to expect. */
export function labelledText(doc, line) {
  const character = characterOf(doc, line);
  return character ? `【${character.name}】${line.text}` : line.text;
}
// Inside <script>, "</" would end the element early.
const scriptJson = (value) => JSON.stringify(value).replace(/</g, "\\u003c");

const STYLE = `
:root{color-scheme:light dark;--ink:#102a2b;--paper:#f7f1e8;--teal:#0d6b68;--line:#d9d2c5;--muted:#5c6b6b}
@media (prefers-color-scheme:dark){:root{--ink:#f7f1e8;--paper:#102a2b;--teal:#4fc1b5;--line:#2c4a4b;--muted:#a8bcb8}}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.6 system-ui,"Noto Sans TC","Microsoft JhengHei",sans-serif}
main{max-width:60rem;margin:0 auto;padding:1.5rem 1rem 4rem}
h1{font-size:1.5rem;margin:0 0 .5rem}h2{font-size:1.1rem;margin:2rem 0 .5rem;color:var(--teal)}
.hint{color:var(--muted);font-size:.9rem}
ol{list-style:none;padding:0;margin:0}
li{border-top:1px solid var(--line);padding:.75rem 0;display:grid;gap:.4rem}
.say{color:var(--muted);font-size:.85rem}
audio,video{width:100%}
label{display:inline-flex;align-items:center;gap:.4rem;font-weight:600}
input[type=text]{width:100%;padding:.4rem;border:1px solid var(--line);border-radius:.4rem;background:transparent;color:inherit}
button{font:inherit;padding:.6rem 1rem;border-radius:.6rem;border:0;background:var(--teal);color:#fff;font-weight:700;cursor:pointer}
.bar{position:sticky;bottom:0;background:var(--paper);border-top:1px solid var(--line);padding:.75rem 0;display:flex;gap:1rem;align-items:center}
.cue{cursor:pointer;border-radius:.4rem;padding:.3rem .5rem}.cue:hover,.cue.now{background:color-mix(in srgb,var(--teal) 18%,transparent)}
.time{font-variant-numeric:tabular-nums;color:var(--muted);margin-right:.5rem}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(18rem,1fr));gap:1rem}
figure{margin:0}figure img{width:100%;border-radius:.4rem;border:1px solid var(--line)}figcaption{font-size:.9rem;margin-top:.3rem}
`;

const optionKey = (n) => String.fromCharCode(64 + n);

function page(title, body) {
  return `<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escapeHtml(title)}</title><style>${STYLE}</style></head><body><main>${body}</main></body></html>\n`;
}

/** Every line with its audio, a 唸錯 box and a note; exports { slug, speech_hash, flags, notes }. */
export function audioReviewHtml(doc, timeline) {
  const byId = new Map(timeline.lines.map((line) => [line.id, line]));
  const sections = [];
  let current = null;
  for (const { scene, line } of eachLine(doc)) {
    if (current?.id !== scene.id) {
      current = { id: scene.id, title: scene.chapter ?? "", items: [] };
      sections.push(current);
    }
    const placed = byId.get(line.id);
    const time = placed ? formatClock(frameToSeconds(placed.start_frame)) : "";
    const spoken = spokenText(line) !== line.text ? `<span class="say">唸成：${escapeHtml(spokenText(line))}</span>` : "";
    current.items.push(
      `<li data-line="${escapeHtml(line.id)}"><div><span class="time">${time}</span>${escapeHtml(labelledText(doc, line))}</div>${spoken}` +
        `<audio controls preload="none" src="../audio/${encodeURIComponent(line.id)}.wav"></audio>` +
        `<div><label><input type="checkbox" class="flag"> 唸錯</label></div>` +
        `<input type="text" class="note" placeholder="哪個字唸錯、應該怎麼唸（選填）"></li>`,
    );
  }
  const body = [
    `<h1>旁白試聽：${escapeHtml(doc.youtube.title)}</h1>`,
    `<p class="hint">逐句聽一遍，把唸錯的句子打勾，可以寫下哪個字、應該怎麼唸。聽完按「匯出」，把下載的 flags.json 交回，工具只會重做打勾的句子（<code>tts --redo flags.json</code>），唸法會補進發音字典。全部都對，就回覆「旁白可以」。</p>`,
    `<p class="hint">時間軸版本 ${escapeHtml(timeline.speech_hash)}</p>`,
    ...sections.map((section) => `${section.title ? `<h2>${escapeHtml(section.title)}</h2>` : ""}<ol>${section.items.join("")}</ol>`),
    `<div class="bar"><button id="export" type="button">匯出 flags.json</button><span id="count" class="hint"></span></div>`,
    `<script>const meta=${scriptJson({ slug: doc.slug, speech_hash: timeline.speech_hash })};` +
      `const count=()=>{document.getElementById("count").textContent=document.querySelectorAll(".flag:checked").length+" 句標為唸錯"};` +
      `document.addEventListener("change",count);count();` +
      `document.getElementById("export").addEventListener("click",()=>{const flags=[],notes={};` +
      `for(const item of document.querySelectorAll("li[data-line]")){const id=item.dataset.line;` +
      `if(item.querySelector(".flag").checked)flags.push(id);const note=item.querySelector(".note").value.trim();if(note)notes[id]=note}` +
      `const blob=new Blob([JSON.stringify({...meta,flags,notes},null,2)],{type:"application/json"});` +
      `const link=document.createElement("a");link.href=URL.createObjectURL(blob);link.download="flags.json";link.click();URL.revokeObjectURL(link.href)});</script>`,
  ].join("");
  return page(`旁白試聽：${doc.youtube.title}`, body);
}

/** A drama's candidate character sheets with the judge's verdicts, for choosing one per character locally. */
export function lookReviewHtml(doc, manifest) {
  const sections = Object.entries(manifest.characters ?? {}).map(([id, entry]) => {
    const character = doc.characters?.find((each) => each.id === id);
    const cards = (entry.candidates ?? [])
      .map((candidate) => {
        const verdict = candidate.judge ? `judge ${candidate.judge.overall}/10${candidate.judge.problems?.length ? `：${candidate.judge.problems.join("；")}` : ""}` : "not judged";
        return `<figure><img src="../${escapeHtml(candidate.file)}" alt=""><figcaption>${optionKey(candidate.n)}${entry.suggested === candidate.n ? "（建議）" : ""} · ${escapeHtml(verdict)}</figcaption></figure>`;
      })
      .join("");
    return `<h2>${escapeHtml(entry.name)}（${escapeHtml(id)}）</h2><p class="hint">${escapeHtml(character?.appearance ?? "")}</p><div class="grid">${cards}</div>`;
  });
  const body = [
    `<h1>角色設定圖：${escapeHtml(doc.youtube?.title ?? doc.slug)}</h1>`,
    `<p class="hint">每個角色選一張，之後每個鏡頭都以它當參考。在 /admin/videos 決定，或本機執行 <code>node tools/video/cli.mjs look --slug ${escapeHtml(doc.slug)} --choose ${Object.keys(manifest.characters ?? {}).map((id) => `${id}=1`).join(",")}</code> 再 <code>approve --gate look</code>。</p>`,
    `<p class="hint">設定版本 ${escapeHtml(manifest.look_hash ?? "")}</p>`,
    ...sections,
  ].join("");
  return page(`角色設定圖：${doc.youtube?.title ?? doc.slug}`, body);
}

/** The finished video, its chapters, and every line; clicking a line or chapter seeks to it. */
export function finalReviewHtml(doc, timeline, checks) {
  const text = new Map([...eachLine(doc)].map(({ line }) => [line.id, labelledText(doc, line)]));
  const cues = timeline.lines.map((line) => ({ id: line.id, start: frameToSeconds(line.start_frame), end: frameToSeconds(line.end_frame), text: text.get(line.id) ?? "" }));
  const chapters = timeline.chapters.map((chapter) => `<li class="cue" data-start="${frameToSeconds(chapter.start_frame)}"><span class="time">${formatClock(frameToSeconds(chapter.start_frame))}</span>${escapeHtml(chapter.title)}</li>`);
  const lines = cues.map((cue) => `<li class="cue" data-start="${cue.start}" data-end="${cue.end}"><span class="time">${formatClock(cue.start)}</span>${escapeHtml(cue.text)}</li>`);
  const problems = checks?.problems?.length ? `<p class="hint">自動檢查有問題：${checks.problems.map(escapeHtml).join("；")}</p>` : `<p class="hint">自動檢查全部通過：畫格數、影音長度、響度 ${escapeHtml(checks?.metrics?.loudness?.integrated ?? "?")} LUFS、每個場景的抽樣畫面。</p>`;
  const body = [
    `<h1>成片審看：${escapeHtml(doc.youtube.title)}</h1>`,
    problems,
    `<video id="video" controls preload="metadata" src="../final.mp4"></video>`,
    `<p class="hint">從頭看到尾。沒問題就回覆「成片可以」；有問題寫下時間與哪裡不對。點下面的章節或句子會跳到那裡。</p>`,
    `<h2>章節</h2><ol>${chapters.join("")}</ol>`,
    `<h2>每一句</h2><ol id="lines">${lines.join("")}</ol>`,
    `<script>const video=document.getElementById("video");` +
      `document.addEventListener("click",(event)=>{const cue=event.target.closest(".cue");if(!cue)return;video.currentTime=Number(cue.dataset.start)+0.01;video.play()});` +
      `const items=[...document.querySelectorAll("#lines .cue")];` +
      `video.addEventListener("timeupdate",()=>{const t=video.currentTime;for(const item of items){const on=t>=Number(item.dataset.start)&&t<Number(item.dataset.end);` +
      `if(on&&!item.classList.contains("now"))item.scrollIntoView({block:"nearest"});item.classList.toggle("now",on)}});</script>`,
  ].join("");
  return page(`成片審看：${doc.youtube.title}`, body);
}
