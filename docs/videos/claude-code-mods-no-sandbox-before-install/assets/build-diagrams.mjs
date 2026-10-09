// Source-owned teaching diagrams. These are explanatory drawings, never captured product UI.
import { mkdirSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
const output = fileURLToPath(new URL('./', import.meta.url));
mkdirSync(output, { recursive: true });
const escape = (s) => s.replaceAll('&', '&amp;').replaceAll('<', '&lt;');
const text = (x,y,s,size=30,color='#edf5f1',weight=500) => `<text x="${x}" y="${y}" fill="${color}" font-size="${size}" font-weight="${weight}">${escape(s)}</text>`;
const shell = (body) => `<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#e9b779"/></marker></defs><rect width="1600" height="900" rx="28" fill="#102b2a"/><g font-family="Noto Sans TC, Microsoft JhengHei, sans-serif">${body}</g></svg>`;
const line = (d,quiet=false) => `<path d="${d}" fill="none" stroke="${quiet?'#7e9e96':'#e9b779'}" stroke-width="5" ${quiet?'stroke-dasharray="10 10"':''} marker-end="url(#arrow)"/>`;
const node = (x,y,w,h,label,sub,active) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="20" fill="${active?'#674f35':'#1c3c39'}" stroke="${active?'#e9b779':'#53746b'}" stroke-width="${active?4:2}"/>${text(x+22,y+48,label,32,'#fff',700)}${text(x+22,y+91,sub,24,'#d0ded8')}`;
for (const stage of ['all','model','hook','ui']) {
  const on = (key) => stage==='all'||stage===key;
  const body = text(60,76,'同一個計數器，沿著同一條流程看',44,'#fff',700)
    +text(60,125,'本片案例的簡化流程｜Mod 觀察事件，然後讓原本工作繼續',28,'#adc5bd')
    +`<rect x="480" y="195" width="1060" height="540" rx="28" fill="#173330" stroke="#63847a" stroke-width="2"/>`
    +text(510,249,'Claude Code：協調工具執行與介面',32,'#c8e1d7',700)
    +node(55,310,330,135,'Claude 模型','提出工具需求',on('model'))
    +node(515,310,285,135,'工具呼叫事件','tool.call',on('hook'))
    +node(865,310,280,135,'計數器 Mod','記一筆，再 next(e)',on('hook'))
    +node(1210,310,295,135,'工具繼續執行','例如：讀取檔案',false)
    +line('M 390 377 L 507 377')+line('M 807 377 L 857 377')+line('M 1152 377 L 1202 377')
    +line('M 1005 450 L 1005 550')+text(1030,510,'更新畫面',25,'#e9b779')
    +node(835,560,650,125,'同一個 Claude Code 畫面','工具呼叫次數：0 → 1（示意）',on('ui'))
    +line('M 1355 450 L 1355 480 L 345 480 L 345 451',true)
    +text(455,525,'工具結果交回模型，繼續原本的任務',26,'#adc5bd')
    +text(60,806,'這裡數的是呼叫事件；不是完成任務數，也不是花費。',32,'#e9b779',700)
    +text(60,857,'依官方 first-mod 範例繪製的機制圖；不是實測畫面。',25,'#adc5bd');
  writeFileSync(`${output}${stage==='all'?'mod-flow':`mod-flow-${stage}`}.svg`,shell(body));
}
const beforeAfter = text(65,84,'它用了幾次工具？直接顯示次數',45,'#fff',700)
  +text(65,135,'同一個案例：在工作狀態旁加入工具呼叫計數',29,'#adc5bd')
  +`<rect x="65" y="205" width="680" height="475" rx="28" fill="#1c3c39" stroke="#53746b" stroke-width="2"/><rect x="855" y="205" width="680" height="475" rx="28" fill="#243d36" stroke="#e9b779" stroke-width="4"/>`
  +text(103,267,'原本',35,'#adc5bd',700)+text(895,267,'加上計數器 Mod',35,'#e9b779',700)
  +text(105,385,'工作進行中',49,'#fff',700)+text(895,385,'工作進行中',49,'#fff',700)
  +text(105,448,'讀取檔案 → 執行下一步',32,'#adc5bd')+text(895,448,'讀取檔案 → 執行下一步',32,'#adc5bd')
  +text(895,555,'工具呼叫',32,'#d0ded8')+text(1150,584,'2',118,'#e9b779',700)+text(1250,565,'次',36,'#e9b779')
  +text(105,602,'同一個模型、同一個任務',31,'#adc5bd')+text(895,635,'多了一個你看得見的數字',31,'#e9b779')
  +line('M 775 430 L 825 430')
  +text(65,770,'它數的是工具呼叫，不是「完成兩件工作」。',34,'#fff',700)
  +text(65,836,'示意計數｜依官方 first-mod 範例繪製；不是 Claude Code 實測介面。',28,'#adc5bd');
writeFileSync(`${output}counter-before-after.svg`,shell(beforeAfter));
console.log('Wrote five explicitly labelled teaching diagrams.');
