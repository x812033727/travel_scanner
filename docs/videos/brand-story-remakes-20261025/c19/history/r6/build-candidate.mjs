import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {spokenUnits,estimateTimeline} from '../../../../tools/video/core/timeline.mjs';
import {validateVideo} from '../../../../tools/video/core/schema.mjs';
import {resolveLook,keyframeKey} from '../../../../tools/video/core/drama.mjs';
import {shotPrompt} from '../../../../tools/video/media/keyframes.mjs';
import {Stage,imageSelectionVersion} from '../../../../tools/video/media/stages.mjs';
const OUT=path.dirname(fileURLToPath(import.meta.url)), REPO=path.resolve(OUT,'../../../..');
const SLUG='story-everyday-seven-bank-c19-remake-20261025',RUNTIME='/workspace/work/brand-story-20261025/c19-submission-root',MEDIA='/workspace/work/brand-story-20261025/media';
const sha=x=>createHash('sha256').update(x).digest('hex'),fileSha=p=>sha(fs.readFileSync(p)),read=p=>JSON.parse(fs.readFileSync(p,'utf8')),write=(p,x)=>fs.writeFileSync(path.join(OUT,p),JSON.stringify(x,null,2)+'\n');
const PROTECTED={'research-original.md':'2f75f4bb90a470616f461ea17aac864a8f1e58ce46f3d15808be98ac8b01d8d3','research-original.claims.json':'5864de9d0780140a4c3378ce07fe1185ad2ff7befb646892df24f0c699f7b2cc','original-preservation.json':'2624d569571d9430774dcec55a67e24018dbf9d7b57c5d7219a8539cb599b4ad'};
for(const[f,h]of Object.entries(PROTECTED))assert.equal(fileSha(path.join(OUT,f)),h,f);
const research=read(path.join(OUT,'research-original.claims.json')),pres=read(path.join(OUT,'original-preservation.json'));
const r1state=read(path.join(OUT,'history/r1/review-state.json'));for(const f of r1state.files)assert.equal(fileSha(path.join(OUT,'history/r1',f.path)),f.sha256,'R1 archive '+f.path);
const r2state=read(path.join(OUT,'history/r2/review-state.json'));for(const f of r2state.files)assert.equal(fileSha(path.join(OUT,'history/r2',f.path)),f.sha256,'R2 archive '+f.path);assert(!fs.existsSync(path.join(OUT,'verify-1.md')),'R2 verification must remain archived, not current for R3');
const r3state=read(path.join(OUT,'history/r3/review-state.json'));for(const f of r3state.files)assert.equal(fileSha(path.join(OUT,'history/r3',f.path)),f.sha256,'R3 archive '+f.path);assert(!fs.existsSync(path.join(OUT,'verify-1.md')),'R3 verification remains archived, not current for R4');
const r4state=read(path.join(OUT,'history/r4/review-state.json'));for(const f of r4state.files)assert.equal(fileSha(path.join(OUT,'history/r4',f.path)),f.sha256,'R4 archive '+f.path);assert(!fs.existsSync(path.join(OUT,'verify-1.md')),'R4 verification remains archived, not current for R5');
const r5state=read(path.join(OUT,'history/r5/review-state.json'));for(const f of r5state.files)assert.equal(fileSha(path.join(OUT,'history/r5',f.path)),f.sha256,'R5 archive '+f.path);assert(!fs.existsSync(path.join(OUT,'verify-1.md')),'R5 verification remains archived, not current for R6');





for(const x of pres.files){assert.equal(fileSha(path.join(pres.legacy_directory,x.path)),x.sha256,x.path);assert.equal(fileSha(path.join(pres.snapshot_directory,x.path)),x.sha256,'snapshot '+x.path);}
const voicePath=path.join(REPO,'docs/videos/brand-story-remakes-20261025/c06/video.json'),voice=structuredClone(read(voicePath).voice);
const rows=[
  {
    "id": "c19r1h01",
    "chapter": "金融廳裡，先拿到一份文件",
    "text": "你想在超商用別家銀行的卡領錢，背後這張網，從六十六台機器起步。",
    "research_claim_refs": [
      "R05",
      "R10"
    ],
    "claim_class": "hypothetical",
    "visual": "viewer",
    "prompt": "Medium shot beside an unbranded terminal in a plain shop, an anonymous adult holding a blank card while facing the viewer, soft light from a side window.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r1h02",
    "chapter": "金融廳裡，先拿到一份文件",
    "text": "二〇〇一年四月六日，金融廳裡，一位西裝人士在桌旁拿著文件。",
    "research_claim_refs": [
      "R04"
    ],
    "claim_class": "fact",
    "visual": "license",
    "prompt": "Medium shot inside a plain government office, one anonymous suited adult holding an unmarked document beside a small table, soft light from a side window.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1h03",
    "chapter": "金融廳裡，先拿到一份文件",
    "text": "圖說寫的是取得預備牌照；銀行卻還沒有成立。",
    "research_claim_refs": [
      "R04"
    ],
    "claim_class": "attributed",
    "visual": "license",
    "prompt": "Medium close-up inside a plain government office, one anonymous suited adult extending an unmarked document above a small table, mild overhead light.",
    "camera": "pull out",
    "note": ""
  },
  {
    "id": "c19r1h04",
    "chapter": "金融廳裡，先拿到一份文件",
    "text": "我先卡住了：這份文件，離你能插卡還有多遠？",
    "research_claim_refs": [
      "R04",
      "R05"
    ],
    "claim_class": "reaction_question",
    "visual": "license",
    "prompt": "Wide shot at a plain office table, an anonymous administrator opening an unmarked document folder, gentle light from the left.",
    "camera": "pan right",
    "note": ""
  },
  {
    "id": "c19r1h05",
    "chapter": "金融廳裡，先拿到一份文件",
    "text": "銀行分行裡的一包面紙，會怎麼把客人帶向超商？",
    "research_claim_refs": [
      "R15"
    ],
    "claim_class": "question",
    "visual": "packet",
    "prompt": "Medium close-up at a plain bank branch counter, an anonymous employee holding a small unmarked tissue packet beside a blank folded poster, mild overhead light.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r1h06",
    "chapter": "金融廳裡，先拿到一份文件",
    "text": "而機器裡的鈔票，真的是裝得越多越好嗎？",
    "research_claim_refs": [
      "R27"
    ],
    "claim_class": "question",
    "visual": "cash",
    "prompt": "Medium shot in a plain cash management office, an anonymous analyst reviewing a blank clipboard beside a single closed unmarked metal container, muted window light on the object.",
    "camera": "pan right",
    "note": ""
  },
  {
    "id": "c19r1h07",
    "chapter": "金融廳裡，先拿到一份文件",
    "text": "跟著七銀行，追一個店角的提款入口，如何接到別家銀行的卡。",
    "research_claim_refs": [
      "R05",
      "R10"
    ],
    "claim_class": "editorial_link",
    "visual": "viewer",
    "prompt": "Medium close-up beside an unbranded terminal in a plain shop, an anonymous adult holding a blank card while facing the viewer, mild overhead light.",
    "camera": "pull out",
    "note": ""
  },
  {
    "id": "c19r1h08",
    "chapter": "金融廳裡，先拿到一份文件",
    "text": "等銀行辦好了，機器就能接待每一張卡嗎？",
    "research_claim_refs": [
      "R10",
      "R19"
    ],
    "claim_class": "question",
    "visual": "bankcard",
    "prompt": "Medium shot at a plain service counter, an anonymous adult examining a blank bank card beside an unbranded terminal, soft light from a side window.",
    "camera": "pan right",
    "note": ""
  },
  {
    "id": "c19r1o01",
    "chapter": "預備牌照之後，機器才開門",
    "text": "拿到預備牌照，還不是拿到一台能用的機器；四天後，IY銀行才成立。",
    "research_claim_refs": [
      "R04",
      "R05"
    ],
    "claim_class": "fact",
    "visual": "license",
    "prompt": "Close-up at a plain office table, an anonymous administrator opening an unmarked document folder, soft interior light from the right.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r1o02",
    "chapter": "預備牌照之後，機器才開門",
    "text": "四月二十五日，它再取得銀行營業牌照；五月七日，開始受理普通預金開戶。",
    "research_claim_refs": [
      "R04",
      "R05"
    ],
    "claim_class": "fact",
    "visual": "accounts",
    "prompt": "Medium shot at a simple office table, an anonymous accountant examining an open unmarked ledger with abstract nonlinguistic lines, soft light from a side window.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1o03",
    "chapter": "預備牌照之後，機器才開門",
    "text": "銀行先開門，店裡的機器也同一天啟用嗎？",
    "research_claim_refs": [
      "R05"
    ],
    "claim_class": "question",
    "visual": "hardware",
    "prompt": "Medium shot in a plain equipment workshop, an anonymous technician examining a closed unmarked terminal housing beside a blank clipboard, soft light from a side window.",
    "camera": "pull out",
    "note": ""
  },
  {
    "id": "c19r1o04",
    "chapter": "預備牌照之後，機器才開門",
    "text": "又過了八天，本店舉行ATM啟用儀式；照片裡的人站在紅緞帶前，身後就是機器。",
    "research_claim_refs": [
      "R05",
      "R06"
    ],
    "claim_class": "fact",
    "visual": "launch",
    "prompt": "Medium shot inside a plain bank lobby, an anonymous suited adult standing beside a ribbon barrier with an unbranded automated teller terminal behind, soft light from a side window.",
    "camera": "pan right",
    "note": ""
  },
  {
    "id": "c19r1o05",
    "chapter": "預備牌照之後，機器才開門",
    "text": "開頭的六十六台，五月十五日在東京二十三區的五十九個地點，開始運作。",
    "research_claim_refs": [
      "R05"
    ],
    "claim_class": "fact",
    "visual": "install",
    "prompt": "Medium shot inside a plain neighborhood shop, an anonymous technician positioning a closed unbranded terminal beside a shelf, soft light from a side window.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r1o06",
    "chapter": "預備牌照之後，機器才開門",
    "text": "我在這裡才看見，領牌照和放機器，是同一個計畫裡前後相接的工作。",
    "research_claim_refs": [
      "R04",
      "R05"
    ],
    "claim_class": "reaction",
    "visual": "hardware",
    "prompt": "Medium close-up in a plain equipment workshop, an anonymous technician examining a closed unmarked terminal housing beside a blank clipboard, mild overhead light.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1o07",
    "chapter": "預備牌照之後，機器才開門",
    "text": "公司首次揭露誌給的起點，是顧客的要求；顧客原本還想在店裡辦什麼？",
    "research_claim_refs": [
      "R02"
    ],
    "claim_class": "attributed_question",
    "visual": "bankcard",
    "prompt": "Medium close-up at a plain service counter, an anonymous adult examining a blank bank card beside an unbranded terminal, mild overhead light.",
    "camera": "pull out",
    "note": ""
  },
  {
    "id": "c19r1o08",
    "chapter": "預備牌照之後，機器才開門",
    "text": "集團原本代收水電等公共費用；顧客接著希望，存提款、匯款也能在店裡辦。",
    "research_claim_refs": [
      "R01",
      "R02"
    ],
    "claim_class": "attributed",
    "visual": "counter",
    "prompt": "Medium shot inside a plain convenience store, an anonymous adult cashier holding a blank bill beside a small barcode scanner, soft light from a side window.",
    "camera": "pan right",
    "note": ""
  },
  {
    "id": "c19r1o09",
    "chapter": "預備牌照之後，機器才開門",
    "text": "你能在購物的地方繳費，卻不等於能用自己的卡提款；那要再接上金融機構。",
    "research_claim_refs": [
      "R01",
      "R10"
    ],
    "claim_class": "editorial_link",
    "visual": "bankcard",
    "prompt": "Wide shot at a plain service counter, an anonymous adult examining a blank bank card beside an unbranded terminal, gentle light from the left.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r1o10",
    "chapter": "預備牌照之後，機器才開門",
    "text": "不過，一九九九年其他超商就已有銀行合作；這個集團不是超商ATM的首創者。",
    "research_claim_refs": [
      "R03"
    ],
    "claim_class": "fact",
    "visual": "install",
    "prompt": "Medium close-up inside a plain neighborhood shop, an anonymous technician positioning a closed unbranded terminal beside a shelf, mild overhead light.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1o11",
    "chapter": "預備牌照之後，機器才開門",
    "text": "光是店裡多一台機器，還說不清銀行的工作；它要接待誰的客人？",
    "research_claim_refs": [
      "R10"
    ],
    "claim_class": "question",
    "visual": "viewer",
    "prompt": "Wide shot beside an unbranded terminal in a plain shop, an anonymous adult holding a blank card while facing the viewer, gentle light from the left.",
    "camera": "pull out",
    "note": ""
  },
  {
    "id": "c19r1o12",
    "chapter": "預備牌照之後，機器才開門",
    "text": "公司把自家存戶的金融服務，和供合作金融機構使用的ATM網路，放在同一張業務圖。",
    "research_claim_refs": [
      "R10"
    ],
    "claim_class": "attributed",
    "visual": "accounts",
    "prompt": "Medium close-up at a simple office table, an anonymous accountant examining an open unmarked ledger with abstract nonlinguistic lines, mild overhead light.",
    "camera": "pan right",
    "note": ""
  },
  {
    "id": "c19r1o14",
    "chapter": "預備牌照之後，機器才開門",
    "text": "你手上的卡若來自別家銀行，店裡就得有一條路，把那張卡接回原來的機構。",
    "research_claim_refs": [
      "R08",
      "R10"
    ],
    "claim_class": "hypothetical",
    "visual": "link",
    "prompt": "Medium shot in a simple equipment room, an anonymous engineer connecting a plain cable to a closed communication cabinet, soft light from a side window.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1o15",
    "chapter": "預備牌照之後，機器才開門",
    "text": "這條路，要從實際合作開始；啟用那天，哪家銀行也跟著接進來？",
    "research_claim_refs": [
      "R07"
    ],
    "claim_class": "question",
    "visual": "link",
    "prompt": "Medium close-up in a simple equipment room, an anonymous engineer connecting a plain cable to a closed communication cabinet, mild overhead light.",
    "camera": "pull out",
    "note": ""
  },
  {
    "id": "c19r1a01",
    "chapter": "別家銀行的客人走進店裡",
    "text": "先把合作接起來，再讓顧客知道；啟用當天的年表，就並列三和銀行合作。",
    "research_claim_refs": [
      "R07"
    ],
    "claim_class": "attributed",
    "visual": "link",
    "prompt": "Wide shot in a simple equipment room, an anonymous engineer connecting a plain cable to a closed communication cabinet, gentle light from the left.",
    "camera": "pan right",
    "note": ""
  },
  {
    "id": "c19r1a02",
    "chapter": "別家銀行的客人走進店裡",
    "text": "六月，這張網向東京以外延伸；與靜岡銀行合作時，也開始在靜岡縣服務。",
    "research_claim_refs": [
      "R07"
    ],
    "claim_class": "fact",
    "visual": "map",
    "prompt": "Medium shot at a planning office, an anonymous planner placing a plain marker onto an unlabelled outline map board, soft light from a side window.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r1a03",
    "chapter": "別家銀行的客人走進店裡",
    "text": "設點與合作往前走，新的卡片功能卻不是同一天全部打開。",
    "research_claim_refs": [
      "R08"
    ],
    "claim_class": "editorial_link",
    "visual": "bankcard",
    "prompt": "Close-up at a plain service counter, an anonymous adult examining a blank bank card beside an unbranded terminal, soft interior light from the right.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r2a30",
    "chapter": "別家銀行的客人走進店裡",
    "text": "六月十一日，銀行也把系統接上全銀網；匯款服務的啟用，還要等下一步。",
    "research_claim_refs": [
      "R08"
    ],
    "claim_class": "fact",
    "visual": "link",
    "prompt": "Close-up inside a plain bank equipment room, an anonymous engineer attaching a plain cable to a closed communication cabinet, soft interior light from the right.",
    "camera": "pan right",
    "note": ""
  },
  {
    "id": "c19r1a04",
    "chapter": "別家銀行的客人走進店裡",
    "text": "六月十三日，都市銀行卡也能在這裡提款；那匯款，是不是同一天開始？",
    "research_claim_refs": [
      "R08"
    ],
    "claim_class": "question",
    "visual": "link",
    "prompt": "Medium shot in a simple equipment room, an anonymous engineer connecting a plain cable to a closed communication cabinet, muted window light on the object.",
    "camera": "pull out",
    "note": ""
  },
  {
    "id": "c19r1a05",
    "chapter": "別家銀行的客人走進店裡",
    "text": "匯款服務又到六月十八日才開始。",
    "research_claim_refs": [
      "R08"
    ],
    "claim_class": "fact",
    "visual": "accounts",
    "prompt": "Wide shot at a simple office table, an anonymous accountant examining an open unmarked ledger with abstract nonlinguistic lines, gentle light from the left.",
    "camera": "pan right",
    "note": "R6僅保留新匯款啟用日期；刪除a03已說的功能分日開放概括。"
  },
  {
    "id": "c19r1a06",
    "chapter": "別家銀行的客人走進店裡",
    "text": "到七月十三日，機器已經超過一千台；找得到入口的地點，隨著設置擴大。",
    "research_claim_refs": [
      "R09"
    ],
    "claim_class": "fact",
    "visual": "install",
    "prompt": "Wide shot inside a plain neighborhood shop, an anonymous technician positioning a closed unbranded terminal beside a shelf, gentle light from the left.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r1a07",
    "chapter": "別家銀行的客人走進店裡",
    "text": "設點擴大，店裡接觸的現金也不只提款；店家一天收下的營業款，能不能存進去？",
    "research_claim_refs": [
      "R11"
    ],
    "claim_class": "question",
    "visual": "salesdeposit",
    "prompt": "Medium shot inside a plain shop after trading hours, an anonymous adult proprietor holding a sealed plain cash envelope beside a closed unbranded deposit terminal, soft light from a side window.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1a25",
    "chapter": "別家銀行的客人走進店裡",
    "text": "同年十二月，銀行開始替Seven-Eleven店舖辦理營業款入金，先接住店舖的需要。",
    "research_claim_refs": [
      "R11"
    ],
    "claim_class": "fact",
    "visual": "salesdeposit",
    "prompt": "Medium close-up inside a plain shop after trading hours, an anonymous adult proprietor holding a sealed plain cash envelope beside a closed unbranded deposit terminal, mild overhead light.",
    "camera": "pan right",
    "note": ""
  },
  {
    "id": "c19r1a27",
    "chapter": "別家銀行的客人走進店裡",
    "text": "機器接了店家的存款，其他人帶銀行卡來，還是得知道，自己能在這裡做什麼。",
    "research_claim_refs": [
      "R10",
      "R11",
      "R19"
    ],
    "claim_class": "editorial_link",
    "visual": "bankcard",
    "prompt": "Medium shot at a plain service counter, an anonymous adult examining a blank bank card beside an unbranded terminal, muted window light on the object.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1a10",
    "chapter": "別家銀行的客人走進店裡",
    "text": "更麻煩的是，接通了資料，不等於客人知道，自己手裡那張卡能在這裡用。",
    "research_claim_refs": [
      "R14",
      "R15",
      "R19"
    ],
    "claim_class": "editorial_link",
    "visual": "poster",
    "prompt": "Medium shot inside a plain shop entrance, an anonymous employee lifting a blank poster toward a bare notice board, soft light from a side window.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r1a11",
    "chapter": "別家銀行的客人走進店裡",
    "text": "二〇〇二年揭露誌寫，ATM設點會揭示合作銀行的招牌，讓顧客辨認。",
    "research_claim_refs": [
      "R14"
    ],
    "claim_class": "attributed",
    "visual": "poster",
    "prompt": "Medium close-up inside a plain shop entrance, an anonymous employee lifting a blank poster toward a bare notice board, mild overhead light.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r2a31",
    "chapter": "別家銀行的客人走進店裡",
    "text": "當時公司把ATM列為合作銀行的共同出張所；那螢幕，要照哪家銀行的規格？",
    "research_claim_refs": [
      "R14"
    ],
    "claim_class": "attributed_question",
    "visual": "bankcard",
    "prompt": "Medium close-up inside a plain bank branch lobby, an anonymous employee holding a blank bank card beside a closed automated terminal, soft light from a side window.",
    "camera": "pull out",
    "note": ""
  },
  {
    "id": "c19r2a32",
    "chapter": "別家銀行的客人走進店裡",
    "text": "它還把這種合作寫成業務外包；另一家銀行，不必把自己的機器一起搬進店裡。",
    "research_claim_refs": [
      "R14"
    ],
    "claim_class": "attributed",
    "visual": "install",
    "prompt": "Close-up inside a plain shop, an anonymous employee examining one closed unbranded automated terminal beside a shelf, soft interior light from the right.",
    "camera": "pan right",
    "note": ""
  },
  {
    "id": "c19r1a12",
    "chapter": "別家銀行的客人走進店裡",
    "text": "如果你拿的是適用合作卡，機器的畫面，就按那家合作銀行的規格顯示。",
    "research_claim_refs": [
      "R14",
      "R19"
    ],
    "claim_class": "hypothetical",
    "visual": "display",
    "prompt": "Medium shot beside an unbranded automated teller terminal, an anonymous adult pointing toward a blank screen with simple nonfunctional shapes, soft light from a side window.",
    "camera": "pull out",
    "note": "R3僅把被刪a13的適用合作卡/你移到a12；畫面規格只說一次，服務差異仍由原a14保留。"
  },
  {
    "id": "c19r1a14",
    "chapter": "別家銀行的客人走進店裡",
    "text": "各家可辦業務、時段和費用不同；那麼，最後印出的收據，也得跟著卡片換嗎？",
    "research_claim_refs": [
      "R14",
      "R19"
    ],
    "claim_class": "question",
    "visual": "receipt",
    "prompt": "Medium shot at a plain bank counter, an anonymous employee examining a blank receipt strip beside a blank bank card, soft light from a side window.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r1a15",
    "chapter": "別家銀行的客人走進店裡",
    "text": "我原先只注意提款口，沒想到，連最後印出的收據，也按合作銀行的規格顯示。",
    "research_claim_refs": [
      "R14"
    ],
    "claim_class": "reaction",
    "visual": "receipt",
    "prompt": "Medium close-up at a plain bank counter, an anonymous employee examining a blank receipt strip beside a blank bank card, mild overhead light.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1a16",
    "chapter": "別家銀行的客人走進店裡",
    "text": "但收據要操作之後才看得到；客人還沒靠近機器前，誰先把消息送給他？",
    "research_claim_refs": [
      "R14",
      "R15"
    ],
    "claim_class": "question",
    "visual": "brochure",
    "prompt": "Medium shot beside a plain shop shelf, an anonymous adult opening a blank folded leaflet beside a closed unbranded terminal, soft light from a side window.",
    "camera": "pull out",
    "note": ""
  },
  {
    "id": "c19r1a17",
    "chapter": "別家銀行的客人走進店裡",
    "text": "店內先擺服務冊子、貼海報，銀行也和零售集團一起推廣ATM的用途。",
    "research_claim_refs": [
      "R15"
    ],
    "claim_class": "fact",
    "visual": "brochure",
    "prompt": "Medium close-up beside a plain shop shelf, an anonymous adult opening a blank folded leaflet beside a closed unbranded terminal, mild overhead light.",
    "camera": "pan right",
    "note": ""
  },
  {
    "id": "c19r1a18",
    "chapter": "別家銀行的客人走進店裡",
    "text": "開頭那包面紙，就是合作金融機構製作、在自家分行發送的宣傳物。",
    "research_claim_refs": [
      "R15"
    ],
    "claim_class": "fact",
    "visual": "packet",
    "prompt": "Medium close-up at a plain bank branch counter, an anonymous employee holding a small unmarked tissue packet beside a blank folded poster, mild overhead light.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r1a19",
    "chapter": "別家銀行的客人走進店裡",
    "text": "同一份報告還記下，合作方製作海報，在分行張貼，幫忙推動機器的使用。",
    "research_claim_refs": [
      "R15"
    ],
    "claim_class": "attributed",
    "visual": "branchposter",
    "prompt": "Medium shot inside a plain bank branch lobby, an anonymous employee lifting a blank poster toward a bare notice board, soft light from a side window.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1a20",
    "chapter": "別家銀行的客人走進店裡",
    "text": "那麼，公司報告裡，不同批次新設機器的使用次數，成長有什麼差別？",
    "research_claim_refs": [
      "R15",
      "R16"
    ],
    "claim_class": "question",
    "visual": "branchposter",
    "prompt": "Medium close-up at a plain bank branch entrance, an anonymous visitor looking at a blank poster on a simple notice board, mild overhead light.",
    "camera": "pull out",
    "note": "R6改問公司報告記錄的不同設置批次使用次數成長；a22/a33分別給2002年2月與開業初期2001年6月機器群。沒有詢問或宣稱宣傳的獨立因果效果。"
  },
  {
    "id": "c19r1a21",
    "chapter": "別家銀行的客人走進店裡",
    "text": "公司把廣告後認知提高、合作機構增加，和不同批次機器的使用成長，放在一起比較。",
    "research_claim_refs": [
      "R16"
    ],
    "claim_class": "attributed",
    "visual": "accounts",
    "prompt": "Close-up at a simple office table, an anonymous accountant examining an open unmarked ledger with abstract nonlinguistic lines, soft interior light from the right.",
    "camera": "pan right",
    "note": ""
  },
  {
    "id": "c19r1a22",
    "chapter": "別家銀行的客人走進店裡",
    "text": "它比較不同時期新設的機器，說二〇〇二年二月那批，使用次數成長更明顯。",
    "research_claim_refs": [
      "R16"
    ],
    "claim_class": "attributed",
    "visual": "accounts",
    "prompt": "Medium shot at a simple office table, an anonymous accountant examining an open unmarked ledger with abstract nonlinguistic lines, muted window light on the object.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r2a33",
    "chapter": "別家銀行的客人走進店裡",
    "text": "拿來相比的，是開業初期六月設下的機器；公司看到的是不同批次的使用成長。",
    "research_claim_refs": [
      "R16"
    ],
    "claim_class": "attributed",
    "visual": "accounts",
    "prompt": "Medium close-up at a plain planning desk, an anonymous analyst comparing two blank folders beside a simple calendar with abstract nonlinguistic marks, soft light.",
    "camera": "pull out",
    "note": ""
  },
  {
    "id": "c19r1a23",
    "chapter": "別家銀行的客人走進店裡",
    "text": "至於哪種卡能存、哪種卡只提款，服務表另外分列，仍得看自己那家銀行。",
    "research_claim_refs": [
      "R19"
    ],
    "claim_class": "fact",
    "visual": "receipt",
    "prompt": "Wide shot at a plain bank counter, an anonymous employee examining a blank receipt strip beside a blank bank card, gentle light from the left.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1a28",
    "chapter": "別家銀行的客人走進店裡",
    "text": "服務往店裡集中，顧客真遇到不懂的步驟，總不能只問機殼；該找誰？",
    "research_claim_refs": [
      "R13"
    ],
    "claim_class": "question",
    "visual": "phone",
    "prompt": "Medium shot beside an unbranded terminal in a plain shop, an anonymous customer holding a simple attached telephone handset, soft light from a side window.",
    "camera": "pull out",
    "note": ""
  },
  {
    "id": "c19r1e01",
    "chapter": "入口變多，仍有人沒有用",
    "text": "機殼旁就接了一條求助的路；二〇〇二年報告，已記下ATM附設電話。",
    "research_claim_refs": [
      "R13"
    ],
    "claim_class": "attributed",
    "visual": "phone",
    "prompt": "Medium close-up beside an unbranded terminal in a plain shop, an anonymous customer holding a simple attached telephone handset, mild overhead light.",
    "camera": "pan right",
    "note": ""
  },
  {
    "id": "c19r1e02",
    "chapter": "入口變多，仍有人沒有用",
    "text": "使用者拿起話筒，詢問會送到監視中心，由那裡回應操作中的疑問。",
    "research_claim_refs": [
      "R13"
    ],
    "claim_class": "fact",
    "visual": "phone",
    "prompt": "Wide shot beside an unbranded terminal in a plain shop, an anonymous customer holding a simple attached telephone handset, gentle light from the left.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r1e03",
    "chapter": "入口變多，仍有人沒有用",
    "text": "你要問的不是貨架商品，接手的人也得能處理這台機器的服務。",
    "research_claim_refs": [
      "R13"
    ],
    "claim_class": "editorial_link",
    "visual": "callcenter",
    "prompt": "Medium shot in a plain support office, an anonymous headset operator looking toward a blank monitor with abstract status shapes, soft light from a side window.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1e04",
    "chapter": "入口變多，仍有人沒有用",
    "text": "機器旁的電話接到中心，那麼入出金的資料、警備與監視，又各走各的嗎？",
    "research_claim_refs": [
      "R12",
      "R13"
    ],
    "claim_class": "question",
    "visual": "system",
    "prompt": "Medium shot inside a simple operations room, an anonymous operator examining a row of closed equipment cabinets, soft light from a side window.",
    "camera": "pull out",
    "note": ""
  },
  {
    "id": "c19r1e05",
    "chapter": "入口變多，仍有人沒有用",
    "text": "公司把這四種工作接成統一管理的網路，全天監看，並把設備與線路做成雙重配置。",
    "research_claim_refs": [
      "R12",
      "R13"
    ],
    "claim_class": "attributed",
    "visual": "system",
    "prompt": "Medium close-up inside a simple operations room, an anonymous operator examining a row of closed equipment cabinets, mild overhead light.",
    "camera": "pan right",
    "note": ""
  },
  {
    "id": "c19r2e30",
    "chapter": "入口變多，仍有人沒有用",
    "text": "銀行還另設備援中心，為突發狀況預作準備；店裡一台機器，連線之外也有支援。",
    "research_claim_refs": [
      "R12"
    ],
    "claim_class": "attributed",
    "visual": "system",
    "prompt": "Wide shot inside a plain backup equipment room, an anonymous engineer inspecting a row of closed communication cabinets, gentle light from the left.",
    "camera": "pull out",
    "note": ""
  },
  {
    "id": "c19r1e06",
    "chapter": "入口變多，仍有人沒有用",
    "text": "我在這裡開始看懂，一台機器要有人持續接手；服務一多，現鈔又該怎麼顧？",
    "research_claim_refs": [
      "R11",
      "R12",
      "R13",
      "R26"
    ],
    "claim_class": "reaction_question",
    "visual": "callcenter",
    "prompt": "Medium close-up in a plain support office, an anonymous headset operator looking toward a blank monitor with abstract status shapes, mild overhead light.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r1a26",
    "chapter": "入口變多，仍有人沒有用",
    "text": "機器接待的也不只個人；二〇〇三財年，營業款入金開始走向一般企業。",
    "research_claim_refs": [
      "R11"
    ],
    "claim_class": "fact",
    "visual": "salesdeposit",
    "prompt": "Wide shot inside a plain shop after trading hours, an anonymous adult proprietor holding a sealed plain cash envelope beside a closed unbranded deposit terminal, gentle light from the left.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r2e31",
    "chapter": "入口變多，仍有人沒有用",
    "text": "商家把錢存進來、個人把錢提出去，現金的兩端，往後都得被這張網照顧。",
    "research_claim_refs": [
      "R11",
      "R26",
      "R28"
    ],
    "claim_class": "editorial_link",
    "visual": "cash",
    "prompt": "Medium close-up in a plain cash management office, an anonymous analyst reviewing a blank clipboard beside a single closed unmarked metal container, mild overhead light.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1e07",
    "chapter": "入口變多，仍有人沒有用",
    "text": "機器越設越多，銀行後來又從鈔票處理這一端，改了什麼？",
    "research_claim_refs": [
      "R17"
    ],
    "claim_class": "question",
    "visual": "hardware",
    "prompt": "Wide shot in a plain equipment workshop, an anonymous technician examining a closed unmarked terminal housing beside a blank clipboard, gentle light from the left.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1e08",
    "chapter": "入口變多，仍有人沒有用",
    "text": "二〇〇五年四月，設置台數超過一萬；七月，第二代ATM開始導入。",
    "research_claim_refs": [
      "R17"
    ],
    "claim_class": "fact",
    "visual": "hardware",
    "prompt": "Close-up in a plain equipment workshop, an anonymous technician examining a closed unmarked terminal housing beside a blank clipboard, soft interior light from the right.",
    "camera": "pull out",
    "note": ""
  },
  {
    "id": "c19r1e09",
    "chapter": "入口變多，仍有人沒有用",
    "text": "公司後來回顧，二代把紙幣處理做得更快、容量更大，改善操作與現金運送效率。",
    "research_claim_refs": [
      "R17"
    ],
    "claim_class": "attributed",
    "visual": "hardware",
    "prompt": "Medium shot in a plain equipment workshop, an anonymous technician examining a closed unmarked terminal housing beside a blank clipboard, muted window light on the object.",
    "camera": "pan right",
    "note": ""
  },
  {
    "id": "c19r1e11",
    "chapter": "入口變多，仍有人沒有用",
    "text": "同年十月，IY銀行改名七銀行；公司說，新名字要讓人更容易想到店內服務。",
    "research_claim_refs": [
      "R18"
    ],
    "claim_class": "attributed",
    "visual": "poster",
    "prompt": "Wide shot inside a plain shop entrance, an anonymous employee lifting a blank poster toward a bare notice board, gentle light from the left.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1e12",
    "chapter": "入口變多，仍有人沒有用",
    "text": "你可能會想，機器、招牌和宣傳都增加，大家總該知道自己的卡能不能用了吧？",
    "research_claim_refs": [
      "R14",
      "R15",
      "R20"
    ],
    "claim_class": "reaction_question",
    "visual": "viewer",
    "prompt": "Medium shot beside an unbranded terminal in a plain shop, an anonymous adult holding a blank card while facing the viewer, muted window light on the object.",
    "camera": "pull out",
    "note": ""
  },
  {
    "id": "c19r1e13",
    "chapter": "入口變多，仍有人沒有用",
    "text": "可是二〇〇九年十一月的一次萬人調查，讓這件事又出現一個缺口。",
    "research_claim_refs": [
      "R20"
    ],
    "claim_class": "attributed",
    "visual": "survey",
    "prompt": "Medium shot inside a plain convenience store, an anonymous adult holding an unmarked survey sheet beside a shelf, soft light from a side window.",
    "camera": "pan right",
    "note": ""
  },
  {
    "id": "c19r1e14",
    "chapter": "入口變多，仍有人沒有用",
    "text": "二〇一〇年報說，有些店客沒有使用，是誤以為自己的卡不能用，或一定要付費。",
    "research_claim_refs": [
      "R20"
    ],
    "claim_class": "attributed",
    "visual": "survey",
    "prompt": "Medium close-up inside a plain convenience store, an anonymous adult holding an unmarked survey sheet beside a shelf, mild overhead light.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r1e15",
    "chapter": "入口變多，仍有人沒有用",
    "text": "他們誤會的是手裡的卡，或螢幕上的費用；銀行又打算怎麼補上這個缺口？",
    "research_claim_refs": [
      "R20"
    ],
    "claim_class": "question",
    "visual": "survey",
    "prompt": "Wide shot inside a plain convenience store, an anonymous adult holding an unmarked survey sheet beside a shelf, gentle light from the left.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1e16",
    "chapter": "入口變多，仍有人沒有用",
    "text": "卡片接上了，人卻可能停在前面，根本沒有把它拿出來的打算。",
    "research_claim_refs": [
      "R20"
    ],
    "claim_class": "editorial_link",
    "visual": "bankcard",
    "prompt": "Wide shot at a plain service counter, an anonymous adult examining a blank bank card beside an unbranded terminal, mild overhead light.",
    "camera": "pull out",
    "note": ""
  },
  {
    "id": "c19r1e17",
    "chapter": "入口變多，仍有人沒有用",
    "text": "銀行因此在報告裡提出，把店內資訊擺得更醒目，並和合作機構一起告知。",
    "research_claim_refs": [
      "R20"
    ],
    "claim_class": "attributed",
    "visual": "poster",
    "prompt": "Close-up inside a plain shop entrance, an anonymous employee lifting a blank poster toward a bare notice board, soft interior light from the right.",
    "camera": "pan right",
    "note": ""
  },
  {
    "id": "c19r1e18",
    "chapter": "入口變多，仍有人沒有用",
    "text": "這也讓我追到另一個問題：有些人以為要付費，代表每次提款真的都要付嗎？",
    "research_claim_refs": [
      "R20",
      "R21"
    ],
    "claim_class": "reaction_question",
    "visual": "fees",
    "prompt": "Medium shot at a simple banking desk, an anonymous employee placing a blank bank card beside two plain closed folders, soft light from a side window.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r1e19",
    "chapter": "入口變多，仍有人沒有用",
    "text": "如果顧客看見的是免手續費，替他接銀行、照顧機器的那筆帳，又落在哪裡？",
    "research_claim_refs": [
      "R21",
      "R22"
    ],
    "claim_class": "question",
    "visual": "fees",
    "prompt": "Medium close-up at a simple banking desk, an anonymous employee placing a blank bank card beside two plain closed folders, mild overhead light.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1t01",
    "chapter": "螢幕上的免費，沒有結清網路的帳",
    "text": "那筆帳得分開看；二〇一〇年報的模型，把顧客費用交給帳戶所屬銀行決定。",
    "research_claim_refs": [
      "R21"
    ],
    "claim_class": "attributed",
    "visual": "fees",
    "prompt": "Wide shot at a simple banking desk, an anonymous employee placing a blank bank card beside two plain closed folders, gentle light from the left.",
    "camera": "pull out",
    "note": ""
  },
  {
    "id": "c19r1t03",
    "chapter": "螢幕上的免費，沒有結清網路的帳",
    "text": "它可以按自己的策略，替顧客定價或給優惠；那機器經營者，又向誰收費？",
    "research_claim_refs": [
      "R21"
    ],
    "claim_class": "question",
    "visual": "accounts",
    "prompt": "Wide shot at a simple office table, an anonymous accountant examining an open unmarked ledger with abstract nonlinguistic lines, mild overhead light.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r1t04",
    "chapter": "螢幕上的免費，沒有結清網路的帳",
    "text": "七銀行收的，則是合作金融機構付給它的ATM使用費，兩個方向不能混成一筆。",
    "research_claim_refs": [
      "R21"
    ],
    "claim_class": "fact",
    "visual": "fees",
    "prompt": "Close-up at a simple banking desk, an anonymous employee placing a blank bank card beside two plain closed folders, soft interior light from the right.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1t05",
    "chapter": "螢幕上的免費，沒有結清網路的帳",
    "text": "顧客看到免費，不能直接推成機器經營者沒有收入；但也不能反過來猜每筆收多少。",
    "research_claim_refs": [
      "R21"
    ],
    "claim_class": "editorial_link",
    "visual": "display",
    "prompt": "Wide shot beside an unbranded automated teller terminal, an anonymous adult pointing toward a blank screen with simple nonfunctional shapes, gentle light from the left.",
    "camera": "pull out",
    "note": ""
  },
  {
    "id": "c19r1t06",
    "chapter": "螢幕上的免費，沒有結清網路的帳",
    "text": "我覺得有意思的，是合作銀行也成了客戶：它一邊照顧存戶，一邊購買這張網。",
    "research_claim_refs": [
      "R10",
      "R21"
    ],
    "claim_class": "reaction",
    "visual": "accounts",
    "prompt": "Close-up at a simple office table, an anonymous accountant examining an open unmarked ledger with abstract nonlinguistic lines, gentle light from the left.",
    "camera": "pan right",
    "note": ""
  },
  {
    "id": "c19r1t07",
    "chapter": "螢幕上的免費，沒有結清網路的帳",
    "text": "報告把借用網路，和自己建一整套ATM來比較；合作方為什麼願意買？",
    "research_claim_refs": [
      "R22"
    ],
    "claim_class": "question",
    "visual": "map",
    "prompt": "Medium close-up at a planning office, an anonymous planner placing a plain marker onto an unlabelled outline map board, mild overhead light.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r1t08",
    "chapter": "螢幕上的免費，沒有結清網路的帳",
    "text": "合作方可以把服務伸到這些設點，減少自有機器的維護與資金負擔。",
    "research_claim_refs": [
      "R22"
    ],
    "claim_class": "fact",
    "visual": "maintain",
    "prompt": "Medium shot inside a plain shop, an anonymous maintenance worker holding a blank checklist beside a closed unbranded terminal, soft light from a side window.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1t10",
    "chapter": "螢幕上的免費，沒有結清網路的帳",
    "text": "這樣的合作，當時接進了多少家金融機構？",
    "research_claim_refs": [
      "R23"
    ],
    "claim_class": "question",
    "visual": "viewer",
    "prompt": "Medium close-up beside an unbranded terminal in a plain shop, an anonymous adult holding a blank card while facing the viewer, soft light from a side window.",
    "camera": "pan right",
    "note": "R4只保留尚未回答的合作機構數問題；刪去重述t08的入口/維運減負前半句。"
  },
  {
    "id": "c19r1t11",
    "chapter": "螢幕上的免費，沒有結清網路的帳",
    "text": "當時的模型圖，已列出五百五十五家合作金融機構，並不只是銀行一家類型。",
    "research_claim_refs": [
      "R23"
    ],
    "claim_class": "attributed",
    "visual": "map",
    "prompt": "Wide shot at a planning office, an anonymous planner placing a plain marker onto an unlabelled outline map board, gentle light from the left.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r1t12",
    "chapter": "螢幕上的免費，沒有結清網路的帳",
    "text": "它們帶著不同的卡、服務和定價進來，機器經營者承接的，也是一組組不同需求。",
    "research_claim_refs": [
      "R19",
      "R21",
      "R23"
    ],
    "claim_class": "editorial_link",
    "visual": "bankcard",
    "prompt": "Medium shot at a plain service counter, an anonymous adult examining a blank bank card beside an unbranded terminal, soft interior light from the right.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1t13",
    "chapter": "螢幕上的免費，沒有結清網路的帳",
    "text": "年報有一欄可以看；同一年度的帳上，這門工作究竟留下了多少收入？",
    "research_claim_refs": [
      "R30"
    ],
    "claim_class": "question",
    "visual": "accounts",
    "prompt": "Medium close-up at a simple office table, an anonymous accountant examining an open unmarked ledger with abstract nonlinguistic lines, muted window light on the object.",
    "camera": "pull out",
    "note": ""
  },
  {
    "id": "c19r1t14",
    "chapter": "螢幕上的免費，沒有結清網路的帳",
    "text": "截至二〇一〇年三月底的一年，ATM相關手續費收入，約八百五十三億日圓。",
    "research_claim_refs": [
      "R30"
    ],
    "claim_class": "fact",
    "visual": "accounts",
    "prompt": "Wide shot at a simple office table, an anonymous accountant examining an open unmarked ledger with abstract nonlinguistic lines, soft light from a side window.",
    "camera": "pan right",
    "note": ""
  },
  {
    "id": "c19r1t15",
    "chapter": "螢幕上的免費，沒有結清網路的帳",
    "text": "那是整張網一整年的收入，還沒把設點、資金與營運的各種支出扣完。",
    "research_claim_refs": [
      "R27",
      "R30"
    ],
    "claim_class": "editorial_link",
    "visual": "accounts",
    "prompt": "Close-up at a simple office table, an anonymous accountant examining an open unmarked ledger with abstract nonlinguistic lines, mild overhead light.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r1t16",
    "chapter": "螢幕上的免費，沒有結清網路的帳",
    "text": "所以不能拿這個總數，替某次提款開收據，更不能直接說一台機器賺多少。",
    "research_claim_refs": [
      "R30"
    ],
    "claim_class": "editorial_link",
    "visual": "receipt",
    "prompt": "Close-up at a plain bank counter, an anonymous employee examining a blank receipt strip beside a blank bank card, soft interior light from the right.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1t17",
    "chapter": "螢幕上的免費，沒有結清網路的帳",
    "text": "收入來自合作，支出卻不只買機器；別人想把這張網當備援，出問題又由誰接手？",
    "research_claim_refs": [
      "R22",
      "R25",
      "R26",
      "R27",
      "R30"
    ],
    "claim_class": "question",
    "visual": "maintain",
    "prompt": "Medium close-up inside a plain shop, an anonymous maintenance worker holding a blank checklist beside a closed unbranded terminal, mild overhead light.",
    "camera": "pull out",
    "note": ""
  },
  {
    "id": "c19r1t18",
    "chapter": "螢幕上的免費，沒有結清網路的帳",
    "text": "報告甚至把這張網，列為合作方原有ATM網路的備援選擇。",
    "research_claim_refs": [
      "R22"
    ],
    "claim_class": "attributed",
    "visual": "relay",
    "prompt": "Medium shot inside a simple data room, an anonymous network engineer standing between two closed equipment cabinets connected by a plain cable, soft light from a side window.",
    "camera": "pan right",
    "note": ""
  },
  {
    "id": "c19r1t19",
    "chapter": "螢幕上的免費，沒有結清網路的帳",
    "text": "要讓別人願意依靠，經營者不只得接得通，還得安排接通之後誰一直照看。",
    "research_claim_refs": [
      "R24",
      "R25"
    ],
    "claim_class": "editorial_link",
    "visual": "callcenter",
    "prompt": "Wide shot in a plain support office, an anonymous headset operator looking toward a blank monitor with abstract status shapes, gentle light from the left.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r1t20",
    "chapter": "螢幕上的免費，沒有結清網路的帳",
    "text": "你把卡插進店裡的機器，交易訊息走遠了；留在眼前的鈔票，又該怎麼顧？",
    "research_claim_refs": [
      "R24",
      "R27"
    ],
    "claim_class": "question",
    "visual": "bankcard",
    "prompt": "Medium close-up at a plain service counter, an anonymous adult examining a blank bank card beside an unbranded terminal, muted window light on the object.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1n01",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "訊息先接到中繼；二〇一〇年報，記的是橫濱與大阪兩套系統。",
    "research_claim_refs": [
      "R24"
    ],
    "claim_class": "attributed",
    "visual": "relay",
    "prompt": "Medium close-up inside a simple data room, an anonymous network engineer standing between two closed equipment cabinets connected by a plain cable, mild overhead light.",
    "camera": "pull out",
    "note": ""
  },
  {
    "id": "c19r1n02",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "ATM和合作金融機構透過它們處理交易，兩邊平常都在運作。",
    "research_claim_refs": [
      "R24"
    ],
    "claim_class": "fact",
    "visual": "link",
    "prompt": "Medium close-up in a simple equipment room, an anonymous engineer connecting a plain cable to a closed communication cabinet, soft light from a side window.",
    "camera": "pan right",
    "note": ""
  },
  {
    "id": "c19r1n03",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "公司說，一邊停了，另一邊有能力接全部交易；可是，機器的狀況又由誰來看？",
    "research_claim_refs": [
      "R24",
      "R25"
    ],
    "claim_class": "attributed_question",
    "visual": "relay",
    "prompt": "Wide shot inside a simple data room, an anonymous network engineer standing between two closed equipment cabinets connected by a plain cable, gentle light from the left.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r1n04",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "同份年報記載，支援中心位於東京與大阪，全天待命。",
    "research_claim_refs": [
      "R25"
    ],
    "claim_class": "fact",
    "visual": "callcenter",
    "prompt": "Close-up in a plain support office, an anonymous headset operator looking toward a blank monitor with abstract status shapes, soft interior light from the right.",
    "camera": "pan left",
    "note": "R5僅保留該年報列明的東京/大阪地點與全天待命資訊；刪除e02已述接客人詢問功能，不把報告發表日期當建造或首次啟用日期。"
  },
  {
    "id": "c19r1n05",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "你聽到兩組城市，是因為中繼交易與支援現場，本來就是不同的工作。",
    "research_claim_refs": [
      "R24",
      "R25"
    ],
    "claim_class": "editorial_link",
    "visual": "system",
    "prompt": "Close-up inside a simple operations room, an anonymous operator examining a row of closed equipment cabinets, soft interior light from the right.",
    "camera": "pull out",
    "note": ""
  },
  {
    "id": "c19r1n06",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "機器出了問題，中心先用遠端方式處理，必要時再協調警備或維修公司。",
    "research_claim_refs": [
      "R25"
    ],
    "claim_class": "fact",
    "visual": "callcenter",
    "prompt": "Medium shot in a plain support office, an anonymous headset operator looking toward a blank monitor with abstract status shapes, muted window light on the object.",
    "camera": "pan right",
    "note": ""
  },
  {
    "id": "c19r1n07",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "我原先只想到壞了再修，卻漏了另一種暫停：維護服務本身，會不會占用機器？",
    "research_claim_refs": [
      "R26"
    ],
    "claim_class": "reaction_question",
    "visual": "maintain",
    "prompt": "Wide shot inside a plain shop, an anonymous maintenance worker holding a blank checklist beside a closed unbranded terminal, gentle light from the left.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r1n08",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "但它確實列出，缺鈔、故障、定期檢查，甚至裝鈔補鈔，都可能讓服務暫停。",
    "research_claim_refs": [
      "R26"
    ],
    "claim_class": "fact",
    "visual": "maintain",
    "prompt": "Close-up inside a plain shop, an anonymous maintenance worker holding a blank checklist beside a closed unbranded terminal, soft interior light from the right.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1n09",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "那麼，乾脆一次裝很多鈔票，不就好了？",
    "research_claim_refs": [
      "R26",
      "R27"
    ],
    "claim_class": "question",
    "visual": "cash",
    "prompt": "Close-up in a plain cash management office, an anonymous analyst reviewing a blank clipboard beside a single closed unmarked metal container, soft interior light from the right.",
    "camera": "pull out",
    "note": "R6只留下增加裝鈔量的新問題；刪去n08已說裝鈔補鈔可能暫停服務的重述。"
  },
  {
    "id": "c19r1n10",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "回到開頭那個問題：多放現金，能少補幾次，卻會讓資金成本上升。",
    "research_claim_refs": [
      "R27"
    ],
    "claim_class": "fact",
    "visual": "cash",
    "prompt": "Medium shot in a plain cash management office, an anonymous analyst reviewing a blank clipboard beside a single closed unmarked metal container, muted window light on the object.",
    "camera": "pan right",
    "note": ""
  },
  {
    "id": "c19r1n11",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "少放一些，補鈔頻率又增加，相關的外包成本也跟著往上走。",
    "research_claim_refs": [
      "R27"
    ],
    "claim_class": "fact",
    "visual": "cash",
    "prompt": "Medium close-up in a plain cash management office, an anonymous analyst reviewing a blank clipboard beside a single closed unmarked metal container, soft light from a side window.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r1n12",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "你需要的是來的時候有鈔可領；營運者卻得處理兩種成本，不斷做取捨。",
    "research_claim_refs": [
      "R27"
    ],
    "claim_class": "editorial_link",
    "visual": "viewer",
    "prompt": "Wide shot beside an unbranded terminal in a plain shop, an anonymous adult holding a blank card while facing the viewer, mild overhead light.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1n13",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "所以報告記下，銀行會逐台分析使用趨勢，照每台機器被使用的方式管理。",
    "research_claim_refs": [
      "R26"
    ],
    "claim_class": "attributed",
    "visual": "system",
    "prompt": "Medium shot inside a simple operations room, an anonymous operator examining a row of closed equipment cabinets, muted window light on the object.",
    "camera": "pull out",
    "note": ""
  },
  {
    "id": "c19r1n14",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "逐台分析了使用趨勢，還有沒有別的現金入口，能跟提款需求一起管理？",
    "research_claim_refs": [
      "R26",
      "R28"
    ],
    "claim_class": "question",
    "visual": "cash",
    "prompt": "Wide shot in a plain cash management office, an anonymous analyst reviewing a blank clipboard beside a single closed unmarked metal container, mild overhead light.",
    "camera": "pan right",
    "note": ""
  },
  {
    "id": "c19r1n15",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "我原本盯著補進去多少，報告卻又把目光拉到附近店家：它們也有錢要存。",
    "research_claim_refs": [
      "R28"
    ],
    "claim_class": "reaction",
    "visual": "salesdeposit",
    "prompt": "Close-up inside a plain shop after trading hours, an anonymous adult proprietor holding a sealed plain cash envelope beside a closed unbranded deposit terminal, soft interior light from the right.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r1n16",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "前面開始的營業款入金，到這時就跟整張網的現金管理接在一起。",
    "research_claim_refs": [
      "R11",
      "R28"
    ],
    "claim_class": "editorial_link",
    "visual": "salesdeposit",
    "prompt": "Medium shot inside a plain shop after trading hours, an anonymous adult proprietor holding a sealed plain cash envelope beside a closed unbranded deposit terminal, muted window light on the object.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1n17",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "七銀行說，它讓附近超商與其他企業把營業款存進ATM，改善現金管理效率。",
    "research_claim_refs": [
      "R28"
    ],
    "claim_class": "attributed",
    "visual": "salesdeposit",
    "prompt": "Medium close-up inside a plain shop after trading hours, an anonymous adult proprietor holding a sealed plain cash envelope beside a closed unbranded deposit terminal, soft light from a side window.",
    "camera": "pull out",
    "note": ""
  },
  {
    "id": "c19r1n18",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "這裡講的是整體管理辦法，沒有說某家店存進去的那張紙鈔，立刻就交給下一位客人。",
    "research_claim_refs": [
      "R28"
    ],
    "claim_class": "editorial_link",
    "visual": "salesdeposit",
    "prompt": "Wide shot inside a plain shop after trading hours, an anonymous adult proprietor holding a sealed plain cash envelope beside a closed unbranded deposit terminal, mild overhead light.",
    "camera": "pan right",
    "note": ""
  },
  {
    "id": "c19r1n19",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "當時報告把每台每月補鈔頻率記為約一點七次；這就代表每個點都完全一樣嗎？",
    "research_claim_refs": [
      "R29"
    ],
    "claim_class": "attributed_question",
    "visual": "cash",
    "prompt": "Close-up in a plain cash management office, an anonymous analyst reviewing a blank clipboard beside a single closed unmarked metal container, gentle light from the left.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r1n20",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "這是當年網路平均的營運數字；不同機器的使用趨勢，仍然要分別照看。",
    "research_claim_refs": [
      "R26",
      "R29"
    ],
    "claim_class": "fact",
    "visual": "system",
    "prompt": "Medium close-up inside a simple operations room, an anonymous operator examining a row of closed equipment cabinets, soft light from a side window.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1n22",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "這張網走到二〇一〇年，機器、合作方與管理方式，也跟著服務範圍繼續調整。",
    "research_claim_refs": [
      "R05",
      "R24",
      "R25",
      "R28"
    ],
    "claim_class": "editorial_link",
    "visual": "install",
    "prompt": "Medium shot inside a plain neighborhood shop, an anonymous technician positioning a closed unbranded terminal beside a shelf, muted window light on the object.",
    "camera": "pan right",
    "note": ""
  },
  {
    "id": "c19r1n23",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "這張網已經接上，那你手裡任何一張卡，現在走過去都能提款嗎？",
    "research_claim_refs": [
      "R19",
      "R26"
    ],
    "claim_class": "question",
    "visual": "bankcard",
    "prompt": "Wide shot at a plain service counter, an anonymous adult examining a blank bank card beside an unbranded terminal, soft light from a side window.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r1n24",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "仍得確認卡種與時段、銀行核准，還要機器正常有鈔，不能只看店裡有沒有機器。",
    "research_claim_refs": [
      "R19",
      "R26"
    ],
    "claim_class": "hypothetical",
    "visual": "viewer",
    "prompt": "Medium shot beside an unbranded terminal in a plain shop, an anonymous adult holding a blank card while facing the viewer, soft interior light from the right.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1n25",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "回到開頭，店角那台機器，怎麼替別家銀行的客人辦事？",
    "research_claim_refs": [
      "R05",
      "R10",
      "R25",
      "R28"
    ],
    "claim_class": "question",
    "visual": "launch",
    "prompt": "Medium close-up in a plain bank lobby, an anonymous employee standing beside an unbranded automated teller terminal at a small opening ceremony, mild overhead light.",
    "camera": "pull out",
    "note": ""
  },
  {
    "id": "c19r1n27",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "我的答案是：零售集團設立銀行，再把合作、辨認、支援和現鈔管理，接成同一張網。",
    "research_claim_refs": [
      "R04",
      "R10",
      "R14",
      "R25",
      "R28"
    ],
    "claim_class": "reaction",
    "visual": "viewer",
    "prompt": "Medium close-up beside an unbranded terminal in a plain shop, an anonymous adult holding a blank card while facing the viewer, soft interior light.",
    "camera": "push in",
    "note": ""
  },
  {
    "id": "c19r1ct1",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "留言告訴我，你用過哪一種店內服務，是後來才發現，背後還接著別家公司？",
    "research_claim_refs": [],
    "claim_class": "cta",
    "visual": "viewer",
    "prompt": "Medium close-up beside an unbranded terminal in a plain shop, an anonymous adult holding a blank card while facing the viewer, soft interior light.",
    "camera": "pan left",
    "note": ""
  },
  {
    "id": "c19r1ct2",
    "chapter": "訊息接回銀行，現鈔留在機器裡",
    "text": "想繼續拆開日用品背後，那些替你接住麻煩的生意，歡迎訂閱品牌故事。",
    "research_claim_refs": [],
    "claim_class": "cta",
    "visual": "viewer",
    "prompt": "Medium close-up beside an unbranded terminal in a plain shop, an anonymous adult holding a blank card while facing the viewer, soft interior light.",
    "camera": "pull out",
    "note": ""
  }
];
// R6 three necessary line edits: all prompts/cameras are copied byte-for-byte from frozen R5; no restyling or new history.
const pairDefs=[['c19r1h05','c19r1a18','branch-tissue-packet'],['c19r1h06','c19r1n10','cash-management-container']];
for(const[a,b]of pairDefs){const setup=rows.find(r=>r.id===a),payoff=rows.find(r=>r.id===b);setup.prompt=payoff.prompt;setup.camera=payoff.camera;}
const classMap={fact:'事實',attributed:'歸屬',question:'旁白疑問',reaction:'反應',reaction_question:'反應＋旁白疑問',attributed_question:'歸屬＋旁白疑問',editorial_link:'編輯連接',hypothetical:'假設／條件',cta:'對觀眾邀請'};
const loopsData=[['h04','o05','預備牌照後歷經成立取牌開業才到ATM啟用'],['h05','a18','分行面紙參與合作機構在分行推廣'],['h06','n10','多放現金會增加資金成本'],['h08','n24','機器仍受卡種時段核准正常有鈔條件限制'],['o03','o04','銀行開門後八天才啟用機器'],['o07','o08','公司所述顧客需求延伸出收銀代收之外的現金入口'],['o11','o12','自家存戶與合作機構客戶兩種業務'],['o15','a01','首日三和銀行合作'],['a04','a05','他行出金與匯款開始日不同'],['a07','a25','2001年底店舖營業款入金'],['a10','a11','設點揭示合作銀行以利辨認'],['a14','a15','收據依合作銀行規格'],['a16','a17','使用前由店內冊子和海報告知'],['a20','a22','公司比較較後新設機器的使用成長'],['a28','e01','ATM附設電話接到監視中心'],['e04','e05','四機能接成統一網路'],['e06','n13','持續接手之後現鈔管理依逐台使用趨勢'],['e07','e09','二代提高紙幣容量與處理速度'],['e12','e14','2009調查仍有認知缺口'],['e15','e17','公司提出強化店內與合作告知'],['e18','t01','顧客費由帳戶銀行定價'],['e19','t04','合作機構付網路使用費'],['t03','t04','經營者向合作金融機構收費'],['t07','t08','相較自有機器的代營運效益'],['t10','t11','2010模型列555家合作機構'],['t13','t14','指定年度ATM相關費收入'],['t17','n06','營運者遠端處理與必要協調'],['t20','n13','逐台使用分析處理現金管理'],['n03','n04','年報列支援中心在東京大阪全天待命'],['n07','n08','維護本身也會占用服務時間'],['n09','n10','更多現金提高資金成本'],['n12','n13','逐台分析使用方式'],['n14','n17','營業款存入納入現金管理'],['n19','n20','補鈔頻率是平均不是每點固定'],['n23','n24','卡種和時段等使用條件'],['n25','n27','回收入口背後的合作與維運問題']];
const loops=loopsData.map(([a,b,what])=>({setup:'c19r1'+a,payoff:'c19r1'+b,what}));
const title='七銀行憑什麼讓他行卡進超商？從66台起步｜品牌故事';
const sources=research.sources.filter(s=>s.id!=='S4');
const scenes=[];let current='';
for(const r of rows){if(r.id.endsWith('ct1')||r.id.endsWith('ct2')||r.id.endsWith('n27'))continue;const s={id:r.id,template:'shot',data:{prompt:r.prompt,visual:'still',camera:r.camera},lines:[{id:r.id,text:r.text,emotion:'對一位觀眾自然說書，來源歸屬與年份讀清楚，問句帶好奇，句間不拖'}]};if(r.chapter!==current){current=r.chapter;s.chapter=current;}scenes.push(s);}
scenes.push({id:'c19r1outro',template:'outro',data:{title:'店角的入口，接著整張網',cta:'分享你後來才看懂的店內服務'},lines:rows.slice(-3).map(r=>({id:r.id,text:r.text,emotion:'對一位觀眾溫暖收束，自然邀請'}))});
const doc={schema_version:1,slug:SLUG,format:'drama',category:'story',narration_locale:'zh-TW',target_minutes:[12,14],voice,subtitles:{burn_in:true},look:{preset:'cute-mystery'},characters:[],music:{prompt:'light, curious, a little mysterious, no vocals',gain_db:-20,duck_db:-10},loops,youtube:{category_id:27,made_for_kids:false,default_language:'zh-TW',title,description:'零售集團為顧客的ATM要求，為何成立一家銀行？從2001年金融廳預備牌照文件場面與東京首批66台機器，沿著他行卡接入、合作銀行畫面與收據、分行宣傳，再到遠端支援和現鈔管理，看七銀行如何經營一個店內入口。創立日期依公司近同期揭露與沿革，不冒稱獨立監管原件；2002、2005、2009調查與2010營運各守自己的年代。匿名概念插圖，不重建特定顧客或紙鈔交易。\n\n原發行者資料（公開原件下載2026-10-25，重讀2026-10-26）\n'+sources.map(s=>s.title+'\n'+s.effective_url).join('\n'),tags:['七銀行','Seven Bank','ATM','便利商店','品牌故事','日用品的意外轉身'],video_id:null},thumbnail:{template:'thumb',data:{layout:'d',headline:'超商先開銀行',sub:'66台接起他行卡',brand:'SEVEN BANK',tag:'品牌故事',shot:'c19r1h02'}},sources:sources.map(s=>({title:s.title,url:s.effective_url,checked_on:'2026-10-26'})),assets:[],scenes};
const validation=validateVideo(doc);assert.equal(validation.errors?.length??0,0,JSON.stringify(validation.errors));write('video.json',doc);write('narration-only.json',rows.map(({chapter,id,text})=>({chapter,id,text})));
const script=['# '+title,'','C19 R6作者稿，HOLD。ID和章名不讀入旁白；全文3222 native spokenUnits，目標13分鐘只是規劃。尚未生成或量測音檔，待獨立逐來源/配鏡及新讀者；沒有SOURCE、敘事、owner或媒體批准。兩個開場預告各自單景單句，規劃與a18/n10回收端共用中性前置圖；真檔SHA仍待製作後驗證。',''];current='';for(const r of rows){if(r.chapter!==current){current=r.chapter;script.push('## '+current,'');}script.push('### '+r.id,'',r.text,'');}fs.writeFileSync(path.join(OUT,'script.md'),script.join('\n'));
const anchorRegistry={};for(const c of research.claims)for(const[eidx,e]of c.evidence.entries()){const id=c.id+'-Q'+(eidx+1);anchorRegistry[id]={id,research_claim_id:c.id,...e,quote_sha256:sha(e.original_quote)};}
anchorRegistry['R04-PHOTO1']={id:'R04-PHOTO1',research_claim_id:'R04',source_id:'S6',url:research.sources.find(s=>s.id==='S6').effective_url,raw_sha256:research.sources.find(s=>s.id==='S6').raw_sha256,locator:'PDF6／印4 左側照片與圖說；圖說事件2001-04-06，發表2002-07',original_quote:'4 月 6 日 予備免許取得（金融庁にて）',quote_sha256:sha('4 月 6 日 予備免許取得（金融庁にて）'),visual_readback:{rendered_page_path:'/workspace/work/brand-story-20261025/c19-audit/S6-page6-r2.png',rendered_page_sha256:fileSha('/workspace/work/brand-story-20261025/c19-audit/S6-page6-r2.png'),read_by_author:true,observed:'One suited person at the table holds a document toward two suited people opposite. Recipient identity, readable text, completed receipt and psychology are not established.',source_image_is_research_only:true}};
anchorRegistry['R06-Q1'].visual_readback={same_raw_pdf_sha256:research.sources.find(s=>s.id==='S6').raw_sha256,locator:'PDF6／印4 右側5月15日本店啟用照片',observed:'Four suited people stand at a red ribbon barrier with automated teller terminals behind; no card transaction, cash dispense, countdown or speech is shown.',source_image_is_research_only:true};
anchorRegistry['R14-Q4']={id:'R14-Q4',research_claim_id:'R14',source_id:'S6',url:research.sources.find(s=>s.id==='S6').effective_url,raw_sha256:research.sources.find(s=>s.id==='S6').raw_sha256,locator:'PDF14／印12 ATMの代替／効果的な活用',original_quote:'業務のアウトソーシングによる効率的な事業展開へ',quote_sha256:sha('業務のアウトソーシングによる効率的な事業展開へ'),scope:'Company explanation of ATM operation outsourcing; no individual negotiation or savings amount established.'};
const claims=rows.map(r=>{const facts=r.research_claim_refs.map(id=>research.claims.find(c=>c.id===id));assert(facts.every(Boolean));const anchors=Object.keys(anchorRegistry).filter(k=>r.research_claim_refs.includes(anchorRegistry[k].research_claim_id));return{id:r.id,scene_id:(r.id.startsWith('c19r1ct')||r.id.endsWith('n27'))?'c19r1outro':r.id,claim:r.text,claim_class:classMap[r.claim_class],claim_kind:r.claim_class,source_ids:[...new Set(anchors.map(a=>anchorRegistry[a].source_id))],research_claim_ids:r.research_claim_refs,quote_ids:anchors,source_evidence:anchors.map(a=>anchorRegistry[a]),limits:[...new Set(facts.flatMap(c=>c.forbidden_inferences))],author_context:r.note||'逐句分類為研究原件支持、編輯連接、旁白疑問/反應或明示假設；不把匿名示意當真實交易。',visual_prompt:scenes.find(s=>s.id===r.id)?.data.prompt??'Native outro typography only; no newly generated image.',visual_scope:'Anonymous concept only; blank signs/cards/receipts and nonfunctional shapes. No logo, named likeness or usable interface.',independent_source_review:'PENDING_OTHER_REVIEWER',independent_visual_review:'PENDING_OTHER_REVIEWER'};});
for(const[a,b,asset]of pairDefs)for(const id of[a,b])claims.find(c=>c.id===id).planned_same_image={plan:'image-reuse-plan.json',asset_plan_id:asset,source_scene_id:b,reuse_scene_id:a,actual_file_sha256:null,status:'PLAN_ONLY'};
write('claims.json',{schema_version:1,status:'PENDING_INDEPENDENT_SOURCE_AND_VISUAL_QA',candidate_revision:'c19-r6',author:'/root/c19_primary_research',video_slug:SLUG,frozen_research_sha256:PROTECTED,source_registry:Object.fromEntries(sources.map(s=>[s.id,s])),anchor_registry:anchorRegistry,rows:claims,source_pass_claimed:false,approvals_created:0});
const cm=['# C19 R6 逐句來源與書面配鏡','','作者綁定，不是獨立SOURCE PASS。每句連到R01–R31及各自Q原文錨點；原件SHA與發表/事件日期保持研究分級。照片僅研究參照，全部圖為匿名概念示意。','','| ID | 旁白 | 分類 | 原文錨點 |','| --- | --- | --- | --- |'];for(const c of claims)cm.push(`| ${c.id} | ${c.claim} | ${c.claim_class} | ${c.quote_ids.join('、')} |`);cm.push('','## 原語引文錨點','');for(const[id,a]of Object.entries(anchorRegistry))cm.push('### '+id,'',`${a.source_id}；${a.locator}；raw SHA ${a.raw_sha256}。`,'','> '+a.original_quote,'');cm.push('','## 寫作界線','','S3雙頁定位為PDF14–15/印12–13合作模型、PDF20/印18中繼、PDF21/印19支援與補鈔、PDF55/印53收入費用；S8入金分界PDF26/印24。S5/S7已cp932嚴格解碼。2009-11調查不當1987原問卷；2001牌照屬公司近同期+live沿革，沒有FSA獨立原件。2001的66台不是59台或59家超商，2005一萬、2010合作555/收入約853億日圓/平均每月1.7各守時點與層級。存入不推同紙鈔立即提款，備援不推實際事故成功，沒有現金車路線或店員接觸內機。','');fs.writeFileSync(path.join(OUT,'claims.md'),cm.join('\n'));
const series={kind:'story',slug:'brand-story-remakes-20261025',episode:19,chapter:1,title,logline:'店內一個ATM入口，如何經由合作卡辨認、分行宣傳、遠端支援與現鈔管理接成服務網。',names:['Seven Bank','IY','ATM','Seven-Eleven','七銀行','IY銀行','三和銀行','靜岡銀行'],characters:[],visual_tier:'stills',compilation:false,target_minutes:13,image_model:'image-01',look:{preset:'cute-mystery'},candidate_revision:'c19-r6',status:'hold_pending_independent_source_and_fresh_readers'};write('series.json',series);
const whole=rows.reduce((n,r)=>n+spokenUnits(r.text),0),opening=rows.filter(r=>r.chapter===rows[0].chapter).reduce((n,r)=>n+spokenUnits(r.text),0),cta=rows.slice(-2).reduce((n,r)=>n+spokenUnits(r.text),0);assert(whole>=3200&&whole<=3500); // Deleted factual paraphrases are not replaced with padding to satisfy the former planning range.
assert(rows.every(r=>spokenUnits(r.text)<=40));
const brief=['# C19 R6｜零售集團把一個入口接成網','','狀態：HOLD_PENDING_INDEPENDENT_SOURCE_AND_FRESH_READERS。新slug '+SLUG+'；video無series重綁定。來源研究由同一作者重用，後續SOURCE必須另派，沒有自核批准。','','## 問題','', '店角這台機器，怎麼才能替別家銀行的客人辦事？','', '## 一句答案','', '零售集團設立銀行，再以合作卡接入、辨認介面、持續支援與現鈔管理，把店角入口接成一張網。','', '## 站主觀點','', '由機器背後新增的工作與結果推故事，來源不足不加虛構人物或百科清單。','', '## 單線與觀眾利害','','你拿別家銀行的卡在超商提款，店角的機器必須接到自己的銀行，還要讓你辨認、有人處理與正常有鈔。主角是2001起步的ATM合作網，並非一台實體機器跨九年，也不是晚餐虛構顧客。開場第一句給觀眾用他行卡提款的利害及66台規模，第二句直接進入2001-04-06金融廳有人持文件面對兩人的原件場面；不把統計當現場。第三句停在預備牌照後銀行尚未成立；正文立即接四天後成立。最多兩事件預告，分行面紙→現鈔庫存，按正文a18→n10順序回收，h07給題目規模承諾，h08為核心問題。','','## 推進方式','','金融廳預備牌照場面→四天後成立/正式取牌/開業→首批機器啟用及合作卡接入→2001-12店舖入金→2002辨認規格與分行推廣/電話監控→2003一般企業入金→2005二代/改名→2009認知缺口→2010費用/中繼/支援/現鈔管理。需求背景縮在機器啟用後的三句歸屬說明，不另開1987年表；2001/2003入金不再倒回插敘。每章開頭接前一個問題，每章有你與我反應，不以法規名詞或新服務產品清單補長。','','## 紙面容量與尚未量測','','全文 '+whole+' native spokenUnits（coldopen '+opening+'，有聲CTA '+cta+'）；目標13分鐘、約3500全篇單位為規劃。以4–5 units/s純算術約'+(whole/5).toFixed(1)+'–'+(whole/4).toFixed(1)+'秒；不是TTS或成片時長。官方實聲口徑含coldopen及有聲CTA，只排另外加入的頻道bookends。actual_seconds=null、actual_duration_verified=false。沒有放慢、長停頓、純recap或重複數字補時。','','## 同圖與畫面規格','','英文匿名人物/場景、無品牌人名logo可讀字；不畫真實可操作UI、ATM廠牌、現金車路線或鈔票匣路由。look唯一{preset:cute-mystery}，image-01、stills；112 shot+1 native outro，正文插圖100%、無連續卡。開場h05/a18共用分行員工持中性面紙包、h06/n10共用現鈔管理者與關閉容器；same prompt+camera只是計畫，實圖尚未存在。完整原生Stage.imageKey純本地重算與正式payoff first/真cache guard/兩端judge/裁切後SHA待驗在image-reuse-plan.json。','','## 原件邊界','','S3/S8採修正後PDF/印刷雙頁；S5/S7 cp932。牌照為公司近同期+live沿革，不冒稱監管獨立證實。2009-11調查不冒1987；66台/59點、一萬/555/853億/1.7次各守年度/範圍。顧客費與網費分開，雙relay能力不演成事故成功，店家存入不推同紙鈔立即出款。','','## 待辦','','獨立逐句來源與書面配鏡、新旁白盲讀、精確站主稿件/企劃核准、真製作入場與整片報價、正常TTS及聲音品質/時長、實圖/同圖/成片都待完成。未生成付費素材，backend/Git/paid均0。',''];fs.writeFileSync(path.join(OUT,'brief.md'),brief.join('\n'));
const coreFiles=['video.json','script.md','narration-only.json','claims.json'];const coreHashes=Object.fromEntries(coreFiles.map(f=>[f,fileSha(path.join(OUT,f))]));
const codeFiles=['tools/video/media/keyframes.mjs','tools/video/media/stages.mjs','tools/video/media/cache.mjs','tools/video/media/prompt-budget.mjs','tools/video/core/drama.mjs','tools/video/media/trim.mjs'];
const pairs=pairDefs.map(([setup,payoff,asset])=>{const a=scenes.find(s=>s.id===setup),b=scenes.find(s=>s.id===payoff);assert.equal(a.data.prompt,b.data.prompt);assert.equal(a.data.camera,b.data.camera);const prompt=shotPrompt(a,resolveLook(doc.look),[],1500);assert.equal(prompt,shotPrompt(b,resolveLook(doc.look),[],1500));const tuple={provider:'minimax',model:'image-01',prompt,negative:'',width:1920,height:1080,seed:1,references:[]},options={prompt,negative:'',references:[],seed:1,size:null},ctx={status:{image:{provider:'minimax',model:'image-01'}},format:null,imageVersion:imageSelectionVersion(series)},key=Stage.prototype.imageKey.call(ctx,options);assert.equal(key,Stage.prototype.imageKey.call(ctx,{...options,prompt:shotPrompt(b,resolveLook(doc.look),[],1500)}));return{asset_plan_id:asset,role:'PLANNED_ONE_IDENTICAL_IMAGE_NOT_AN_ACTUAL_ASSET',source_scene_id:payoff,source_line_id:payoff,reuse_scene_id:setup,reuse_line_id:setup,narration_setup_text:a.lines[0].text,narration_payoff_text:b.lines[0].text,source_prompt_sha256:sha(b.data.prompt),reuse_prompt_sha256:sha(a.data.prompt),prompt_exact_match:true,source_camera:b.data.camera,reuse_camera:a.data.camera,composed_prompt_sha256:sha(prompt),no_result_drawn_in_teaser:asset==='branch-tissue-packet'?'A worker holds a closed blank packet before distribution; no recipient, completed handoff, promotional wording or usage-growth result is shown.':'An analyst holds a blank clipboard beside a closed container; no cash quantity, replenishment trip, funding-cost comparison or immediate cash recycling is shown.',native_same_input_key_rehearsal:{pure_local_functions_only:true,input_tuple:tuple,aspect:'16:9',requested_size:null,nominal_image_size:'1K',image_selection_version:imageSelectionVersion(series),seed_offset:0,takes:1,correction_list:[],prompt_budget_chars:1500,base_key:keyframeKey(tuple),native_stage_key:key,parameters_are_declared_plan_not_backend_readback:true,no_provider_call:true},actual_source_file:null,actual_source_sha256:null,actual_reused_file:null,actual_reused_sha256:null,actual_same_asset_verified:false,actual_same_file_sha_verified:false};});
const plan={schema_version:1,revision:'c19-r6',status:'WRITTEN_REUSE_PLAN_PENDING_GENERATION_AND_REAL_FILE_SHA_VERIFICATION',not_a_video_schema_extension:true,not_a_keyframes_manifest:true,no_assets_generated:true,actual_same_asset_verified:false,candidate_binding:{core_four_sha256:coreHashes,claims_md_sha256:fileSha(path.join(OUT,'claims.md')),brief_sha256:fileSha(path.join(OUT,'brief.md')),series_sha256:fileSha(path.join(OUT,'series.json'))},rule:{file:'.agents/skills/youtube-video/references/script-writing.md',sha256:fileSha(path.join(REPO,'.agents/skills/youtube-video/references/script-writing.md')),quote:'每一個預告句用回收它的那一章的畫面（同一張圖）'},code_readback:{files_sha256:Object.fromEntries(codeFiles.map(f=>[f,fileSha(path.join(REPO,f))])),still_alias_field_available:false,clip_source_field_not_applicable:'Still data.source is unsupported; no alias or custom video schema field was invented.',native_supported_route:'Official keyframes --shot with the ordinary exact-request cache, independently judged at both endpoints.',cache_identity:'The pure local Stage.imageKey was called with declared model/version/size and full request inputs. Scene ID and output target do not enter the native key.',camera_matters:'Camera is part of composed prompt and must be identical.',guard_is_read_only:'Use readCache plus existsSync and SHA of actual bytes. Never use cached() as a read-only guard: it can delete an invalid entry and write cache.json.'},pairs,production_handoff:{preconditions:['Current exact independent source/visual and fresh-reader reviews, owner approvals, actual production admission and all-in quote are still pending. This plan executes nothing.','Read actual provider/model/version/prompt limit/size/negative/references/seed/fixes before admission and recompute each native key from that readback; planned example values are not a live cache receipt.','Same immutable project/workdir, exact request, default seed offset 0 and takes1 at both endpoints.'],official_command_recipe_only:pairs.flatMap(p=>[{purpose:'PAYOFF FIRST only after normal production admission',argv:['node','docs/videos/brand-story-remakes-20261025/runtime-cli.mjs',RUNTIME,'keyframes','--slug',SLUG,'--workdir',MEDIA,'--shot',p.source_scene_id,'--takes','1']},{purpose:'MANDATORY READ-ONLY LIVE CACHE GUARD BEFORE THE SECOND COMMAND',required_checks:['Read keyframes/manifest.json shots['+p.source_scene_id+']; require passed judge, needs_review false, seed1, one take, no fixes, key equal to live-recomputed native Stage.imageKey.','Hash the actual selected file bytes; match selected.sha256. Trimmed selected file may differ from the original cache file.','Read media/cache.json using readCache(workdir); require entries[live-key] exists, provider/model equal the live request, actual file exists, actual bytes SHA equal entry.sha256.','Any missing/mismatching file, key, model, selection or SHA: STOP. Do not issue teaser command, clear cache, submit another purchase or hand-edit a manifest.']},{purpose:'TEASER only after the real cache guard succeeds; exact cache hit prevents duplicate image purchase',argv:['node','docs/videos/brand-story-remakes-20261025/runtime-cli.mjs',RUNTIME,'keyframes','--slug',SLUG,'--workdir',MEDIA,'--shot',p.reuse_scene_id,'--takes','1']}]),on_any_failure_or_changed_request:'Stop the pair. No separate reroll, force, accept-best bypass, independent look-alike purchase or hand-written manifest. Correct both endpoints together, repeat normal bound source/visual review and admission.',actual_verification_required:['Both endpoints must pass their own ordinary official judge verdict.','After the official commands, read manifest shots for the pair, require identical selected file reference and SHA, then hash the actual bytes.','If trimming occurs, require identical final trimmed selected file and SHA at both endpoints; matching original-generated hashes alone is insufficient.','Hash original cache bytes and final selected bytes separately; do not assume original and trimmed SHA are equal.','Read final assembly inputs and require the same selected file at teaser and payoff. Preserve normal job/cache/ledger receipts.'],executed:false},provider_calls:0,paid_calls:0};write('image-reuse-plan.json',plan);
const producer=['# C19 R6 製作交接','','本檔僅recipe；paid/provider/backend/Git均0。video無series欄，context的series.json僅供普通不可變字典及企劃使用。正常prepare-runtime.mjs c19初始化到'+RUNTIME+'，media base '+MEDIA+'；只跑免費lint，不跑聲音/圖片/審圖/組片。','','## 中文','','voice整個物件逐字採C06 Sulafat設定（沒有複製別集字典）；本集字典透過initializeStoryLexicon建立不可變snapshot。13分鐘目標，全文3222 native units，尚無實聲，不能把字量當通過。繁中燒錄+CC；5秒頻道片頭在coldopen後，21秒正式v4片尾在有聲CTA後。所有媒體尚未辨識/讀回。','','## 兩組同圖','','h05→a18、h06→n10按正文順序。image-reuse-plan.json載完整計畫輸入與兩端本地Stage.imageKey相等。正常入場後先payoff --takes 1；實際第一take通過並仍被選中後，第二命令之前，讀真manifest選圖與真media/cache.json、重算live request key，兩個實體檔各自SHA均須吻合。cache缺或錯立即停止，不能讓teaser命令另外買圖。不要用會刪錯cache的cached()當唯讀guard。','','兩端各走正常judge；完成後讀官方manifest，確認相同selected路徑與真bytes SHA，裁切後仍要相同最終derived檔。不能拿原圖SHA當裁切後SHA。組片前再核對實際輸入。actual_same_asset_verified保持false，實檔欄null，直到以上真查完。','','## 其他保護','','只改c19新版文件；old66檔、外部唯讀快照及研究三檔原SHA均保護。沒有FSA原件；不增加首創、每卡可用、逐筆網費、單機淨利、災難切換成功、紙鈔直接再出款、運鈔路線或店員接內機。獨立source/native另派，作者不寫verify或任何批准。',''];fs.writeFileSync(path.join(OUT,'producer.md'),producer.join('\n'));
write('author-notes.json',{schema_version:1,status:'HOLD_PENDING_INDEPENDENT_SOURCE_VISUAL_AND_FRESH_READERS',candidate_revision:'c19-r6',author:'/root/c19_primary_research',counts:{lines:rows.length,scenes:scenes.length,shots:scenes.filter(s=>s.template==='shot').length,cards:0,outro:1,chapters:6,loops:loops.length},native_units:{whole_narration_spoken_units:whole,coldopen:opening,voiced_CTA:cta,rough_planning_target:3500,delta_to_rough_target:whole-3500,actual_narration_seconds:null,actual_final_seconds:null,actual_duration_verified:false,planning_arithmetic_at_4_to_5_units_per_second:[whole/5,whole/4],planning_is_not_actual_time:true,official_duration_scope:'Whole unwrapped narration including coldopen and voiced CTA; excludes separately added channel bookends.'},voice_source:{path:voicePath,file_sha256:fileSha(voicePath),voice_object_sha256:sha(JSON.stringify(voice)),exact_copy:true,other_episode_dictionary_copied:false},source_research_sha256:PROTECTED,protected_old_file_count:pres.file_count,protected_old_and_snapshot_unchanged:true,source_pass_claimed:false,narrative_pass_claimed:false,owner_approval_created:false,actual_media_generated:false,actual_same_image_verified:false,provider_calls:0,paid_calls:0,backend_mutations:0,git_mutations:0,runtime_root:RUNTIME,image_reuse_plan_sha256:fileSha(path.join(OUT,'image-reuse-plan.json')),independent_source_review:'PENDING_OTHER_REVIEWER',independent_narrative_review:'PENDING_FRESH_READERS'});
console.log(JSON.stringify({core_four_sha256:coreHashes,whole_units:whole,coldopen:opening,CTA:cta,lines:rows.length,scenes:scenes.length,shots:scenes.filter(s=>s.template==='shot').length,unique_composed_shot_requests:new Set(scenes.filter(s=>s.template==='shot').map(s=>shotPrompt(s,resolveLook(doc.look),[],1500))).size,reuse_plan_sha256:fileSha(path.join(OUT,'image-reuse-plan.json'))},null,2));
