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
const OUT=path.dirname(fileURLToPath(import.meta.url)),REPO=path.resolve(OUT,'../../../..');
const SLUG='story-everyday-zippo-c20-remake-20261025',RUNTIME='/workspace/work/brand-story-20261025/c20-submission-root',AUDIT='/workspace/work/brand-story-20261025/c20-audit',MEDIA=path.join(AUDIT,'media');
const sha=x=>createHash('sha256').update(x).digest('hex'),fileSha=p=>sha(fs.readFileSync(p)),read=p=>JSON.parse(fs.readFileSync(p,'utf8')),write=(p,x)=>fs.writeFileSync(path.join(OUT,p),JSON.stringify(x,null,2)+'\n');
const PROTECTED={'research-original.md':'bd325631384e70272d074326b8b0bc5fa10c01adc2210276fe591a3a54765be2','research-original.claims.json':'4763b1808d0ad7d21a42256f7584c3c78352bb33eb10f91027c9aa6be7a8517c','original-preservation.json':'4932a5ed91683a1dc56b717fb292ca1d74ed61d13b7c40064bb0a029e0cb96bf'};
for(const[f,h]of Object.entries(PROTECTED))assert.equal(fileSha(path.join(OUT,f)),h,'protected research '+f);
const research=read(path.join(OUT,'research-original.claims.json')),pres=read(path.join(OUT,'original-preservation.json'));
const protectedOld=[];for(const section of[pres,pres.additional_related_legacy_tree])for(const f of section.files){const source=path.join(section.source_root,f.path),snapshot=path.join(section.external_readonly_snapshot??section.snapshot_root,f.path);assert.equal(fileSha(source),f.sha256,source);assert.equal(fileSha(snapshot),f.sha256,snapshot);protectedOld.push({source,snapshot,sha256:f.sha256});}assert.equal(protectedOld.length,68);
const rawManifestFile=path.join(AUDIT,'source-cache-manifest.json'),rawManifest=read(rawManifestFile);for(const f of rawManifest.files)assert.equal(fileSha(path.join(rawManifest.cache_root,f.relative_path)),f.sha256,'raw '+f.relative_path);
const voicePath=path.join(REPO,'docs/videos/brand-story-remakes-20261025/c06/video.json'),voice=structuredClone(read(voicePath).voice);
const rows=[
  {
    "id": "c20r1h01",
    "chapter": "粉紅色小盒，磨輪停住了",
    "text": "你會把用了約三、四年的禮物寄去修，讓廠商決定換掉哪一部分嗎？",
    "research_claim_refs": [
      "J01",
      "J02"
    ],
    "claim_class": "viewer_question",
    "visual": "gift"
  },
  {
    "id": "c20r1h02",
    "chapter": "粉紅色小盒，磨輪停住了",
    "text": "二〇二四年，日本，一位使用者發現，粉紅色打火機的開合變鬆了。",
    "research_claim_refs": [
      "J03",
      "J09"
    ],
    "claim_class": "attributed",
    "visual": "inspect"
  },
  {
    "id": "c20r1h03",
    "chapter": "粉紅色小盒，磨輪停住了",
    "text": "他說，裡面一片彈簧裂了；也許因此，連打火的磨輪都不轉。",
    "research_claim_refs": [
      "J03",
      "J04"
    ],
    "claim_class": "attributed",
    "visual": "insert"
  },
  {
    "id": "c20r1h04",
    "chapter": "粉紅色小盒，磨輪停住了",
    "text": "小盒點不著了，我好奇的是，他會先找哪一種修法？",
    "research_claim_refs": [
      "J05",
      "J06"
    ],
    "claim_class": "reaction_question",
    "visual": "inspect"
  },
  {
    "id": "c20r1h05",
    "chapter": "粉紅色小盒，磨輪停住了",
    "text": "封口前，一張修理表上，有什麼比故障位置還不能填錯？",
    "research_claim_refs": [
      "J13"
    ],
    "claim_class": "question",
    "visual": "form"
  },
  {
    "id": "c20r1h06",
    "chapter": "粉紅色小盒，磨輪停住了",
    "text": "等到回件，包裹裡會只有換上的機件嗎？",
    "research_claim_refs": [
      "J17",
      "J18"
    ],
    "claim_class": "question",
    "visual": "sealed"
  },
  {
    "id": "c20r1h07",
    "chapter": "粉紅色小盒，磨輪停住了",
    "text": "今天跟著 Zippo 這只粉紅殼，走一趟四十七天的送修。",
    "research_claim_refs": [
      "J09",
      "J15"
    ],
    "claim_class": "editorial_promise",
    "visual": "gift"
  },
  {
    "id": "c20r1h08",
    "chapter": "粉紅色小盒，磨輪停住了",
    "text": "免費修，最後讓什麼換了新，又讓什麼留了下來？",
    "research_claim_refs": [
      "J18",
      "J22"
    ],
    "claim_class": "question",
    "visual": "sealed"
  },
  {
    "id": "c20r1o01",
    "chapter": "先找零件，才找到那句保證",
    "text": "他先上網找零件，想看看，能不能在家把這只小盒修好。",
    "research_claim_refs": [
      "J06"
    ],
    "claim_class": "attributed",
    "visual": "search"
  },
  {
    "id": "c20r1o02",
    "chapter": "先找零件，才找到那句保證",
    "text": "這不是一只剛拿到手的新品；使用期間，他曾換火石，也換過裡面的填料。",
    "research_claim_refs": [
      "J02"
    ],
    "claim_class": "attributed",
    "visual": "supplies"
  },
  {
    "id": "c20r1o03",
    "chapter": "先找零件，才找到那句保證",
    "text": "可是保養用過的辦法，這次還能直接接著用嗎？",
    "research_claim_refs": [
      "J03",
      "J04",
      "O02"
    ],
    "claim_class": "question",
    "visual": "inspect"
  },
  {
    "id": "c20r1o04",
    "chapter": "先找零件，才找到那句保證",
    "text": "他發現的裂片叫凸輪彈簧，是這次備忘錄記下的故障部位。",
    "research_claim_refs": [
      "J03"
    ],
    "claim_class": "attributed",
    "visual": "insert"
  },
  {
    "id": "c20r1o05",
    "chapter": "先找零件，才找到那句保證",
    "text": "而磨輪轉不動，讓他連點火的動作，都沒辦法做下去。",
    "research_claim_refs": [
      "J04",
      "J05"
    ],
    "claim_class": "editorial_link",
    "visual": "wheel"
  },
  {
    "id": "c20r1o06",
    "chapter": "先找零件，才找到那句保證",
    "text": "我覺得這個差別很關鍵：有時候補的是消耗掉的東西，有時候是機件停住。",
    "research_claim_refs": [
      "O01",
      "O02",
      "J04"
    ],
    "claim_class": "reaction",
    "visual": "supplies"
  },
  {
    "id": "c20r1o07",
    "chapter": "先找零件，才找到那句保證",
    "text": "你若只聽到「不會亮」，很容易把這些情況，全當成同一種壞。",
    "research_claim_refs": [
      "O01",
      "O02",
      "O03"
    ],
    "claim_class": "viewer_conditional",
    "visual": "wheel"
  },
  {
    "id": "c20r1o08",
    "chapter": "先找零件，才找到那句保證",
    "text": "美國現在的排障頁，甚至先問最基本的一件事：裡面有燃料嗎？",
    "research_claim_refs": [
      "O01"
    ],
    "claim_class": "attributed",
    "visual": "fuel"
  },
  {
    "id": "c20r1o09",
    "chapter": "先找零件，才找到那句保證",
    "text": "傳統液體燃料款出廠時，不先裝好油；沒燃料，並不能證明機械壞了。",
    "research_claim_refs": [
      "O01"
    ],
    "claim_class": "fact",
    "visual": "fuel"
  },
  {
    "id": "c20r1o10",
    "chapter": "先找零件，才找到那句保證",
    "text": "另一種情況是磨輪轉得很空，卻打不出火花；官方會請你檢查火石。",
    "research_claim_refs": [
      "O02"
    ],
    "claim_class": "attributed",
    "visual": "wheel"
  },
  {
    "id": "c20r1o11",
    "chapter": "先找零件，才找到那句保證",
    "text": "火石會隨使用磨耗，燈芯積碳，也有自己的保養方式。",
    "research_claim_refs": [
      "O02",
      "O06"
    ],
    "claim_class": "fact",
    "visual": "supplies"
  },
  {
    "id": "c20r1o12",
    "chapter": "先找零件，才找到那句保證",
    "text": "但這位作者遇到的，不是前面那種「磨輪空轉」；他的輪子根本不動。",
    "research_claim_refs": [
      "J04",
      "O02"
    ],
    "claim_class": "editorial_link",
    "visual": "wheel"
  },
  {
    "id": "c20r1o13",
    "chapter": "先找零件，才找到那句保證",
    "text": "所以這裡只分清症狀，不替他把官網上的每個排障步驟都做一遍。",
    "research_claim_refs": [
      "J04",
      "O03"
    ],
    "claim_class": "editorial_boundary",
    "visual": "inspect"
  },
  {
    "id": "c20r1o14",
    "chapter": "先找零件，才找到那句保證",
    "text": "他在網路上找到了能用的替換零件嗎？",
    "research_claim_refs": [
      "J06"
    ],
    "claim_class": "question",
    "visual": "search"
  },
  {
    "id": "c20r1o15",
    "chapter": "先找零件，才找到那句保證",
    "text": "問題卡在尺寸：他用的不是一般大小，找零件這條路，看來走不通。",
    "research_claim_refs": [
      "J06"
    ],
    "claim_class": "attributed",
    "visual": "search"
  },
  {
    "id": "c20r1o16",
    "chapter": "先找零件，才找到那句保證",
    "text": "他沒有寫下買到零件、拆開修成功，而是決定把打火機送出去。",
    "research_claim_refs": [
      "J06"
    ],
    "claim_class": "attributed",
    "visual": "parcel"
  },
  {
    "id": "c20r1o17",
    "chapter": "先找零件，才找到那句保證",
    "text": "到這時，他才注意到，這個品牌原來有永久保證。",
    "research_claim_refs": [
      "J07"
    ],
    "claim_class": "attributed",
    "visual": "form"
  },
  {
    "id": "c20r1o18",
    "chapter": "先找零件，才找到那句保證",
    "text": "我讀到這裡的反應是：原來那句很有名的承諾，使用者也可能用了幾年才想起來查。",
    "research_claim_refs": [
      "J02",
      "J07"
    ],
    "claim_class": "reaction",
    "visual": "form"
  },
  {
    "id": "c20r1o19",
    "chapter": "先找零件，才找到那句保證",
    "text": "你熟悉自己的東西，不一定也熟悉，廠商會怎麼接手它。",
    "research_claim_refs": [
      "J07"
    ],
    "claim_class": "viewer_reaction",
    "visual": "gift"
  },
  {
    "id": "c20r1o20",
    "chapter": "先找零件，才找到那句保證",
    "text": "那如果這只禮物早就沒有盒子，連收據都找不到，還要不要寄？",
    "research_claim_refs": [
      "J08"
    ],
    "claim_class": "question",
    "visual": "emptybox"
  },
  {
    "id": "c20r1i01",
    "chapter": "沒有盒與收據，還是把舊物送回去",
    "text": "沒有盒子和收據，正是他開始查維修費用時，擺在面前的情況。",
    "research_claim_refs": [
      "J08"
    ],
    "claim_class": "attributed",
    "visual": "emptybox"
  },
  {
    "id": "c20r1i02",
    "chapter": "沒有盒與收據，還是把舊物送回去",
    "text": "他說，若修起來要花不少錢，就連重新買一只，也會放進考量。",
    "research_claim_refs": [
      "J08"
    ],
    "claim_class": "attributed",
    "visual": "choice"
  },
  {
    "id": "c20r1i03",
    "chapter": "沒有盒與收據，還是把舊物送回去",
    "text": "所以在找到保證之前，他並沒有先認定，修理一定比買新划算。",
    "research_claim_refs": [
      "J08"
    ],
    "claim_class": "editorial_link",
    "visual": "choice"
  },
  {
    "id": "c20r1i04",
    "chapter": "沒有盒與收據，還是把舊物送回去",
    "text": "你遇到一件有感情的禮物，最後作決定時，會只比兩張價錢嗎？",
    "research_claim_refs": [
      "J01",
      "J08"
    ],
    "claim_class": "viewer_question",
    "visual": "gift"
  },
  {
    "id": "c20r1i05",
    "chapter": "沒有盒與收據，還是把舊物送回去",
    "text": "他查到的說法，是正品有免費終身保證；查修費的問題，於是轉成怎麼寄回去。",
    "research_claim_refs": [
      "J07",
      "J08"
    ],
    "claim_class": "attributed",
    "visual": "form"
  },
  {
    "id": "c20r1i06",
    "chapter": "沒有盒與收據，還是把舊物送回去",
    "text": "能確定的是，找過維修資訊之後，他選了寄修，沒有就此換掉整只。",
    "research_claim_refs": [
      "J07",
      "J14"
    ],
    "claim_class": "attributed",
    "visual": "parcel"
  },
  {
    "id": "c20r1i07",
    "chapter": "沒有盒與收據，還是把舊物送回去",
    "text": "而這句「能用，否則免費修」，究竟接住的是什麼？",
    "research_claim_refs": [
      "O07"
    ],
    "claim_class": "question",
    "visual": "case"
  },
  {
    "id": "c20r1i08",
    "chapter": "沒有盒與收據，還是把舊物送回去",
    "text": "在美國當代的保證裡，傳統防風口袋打火機，承諾的是繼續工作的功能。",
    "research_claim_refs": [
      "O07"
    ],
    "claim_class": "attributed",
    "visual": "case"
  },
  {
    "id": "c20r1i09",
    "chapter": "沒有盒與收據，還是把舊物送回去",
    "text": "例如蓋子和盒身之間的鉸鏈脫離，美國官方就明說，會免費修理。",
    "research_claim_refs": [
      "O08"
    ],
    "claim_class": "attributed",
    "visual": "hinge"
  },
  {
    "id": "c20r1i10",
    "chapter": "沒有盒與收據，還是把舊物送回去",
    "text": "但若你送去的只是塗裝磨掉，同一句終身承諾，會把它翻新嗎？",
    "research_claim_refs": [
      "O09"
    ],
    "claim_class": "question",
    "visual": "case"
  },
  {
    "id": "c20r1i11",
    "chapter": "沒有盒與收據，還是把舊物送回去",
    "text": "美國保證不涵蓋塗裝與裝飾；我在這裡，才把功能和外觀分開看。",
    "research_claim_refs": [
      "O09"
    ],
    "claim_class": "reaction",
    "visual": "choice"
  },
  {
    "id": "c20r1i12",
    "chapter": "沒有盒與收據，還是把舊物送回去",
    "text": "那新買不久就遇到外觀問題，難道也一概沒人處理嗎？",
    "research_claim_refs": [
      "O10"
    ],
    "claim_class": "question",
    "visual": "case"
  },
  {
    "id": "c20r1i13",
    "chapter": "沒有盒與收據，還是把舊物送回去",
    "text": "新買不到一年就有外觀問題，美國頁面請使用者聯絡客服，討論可能選項。",
    "research_claim_refs": [
      "O10"
    ],
    "claim_class": "attributed",
    "visual": "form"
  },
  {
    "id": "c20r1i14",
    "chapter": "沒有盒與收據，還是把舊物送回去",
    "text": "這不是每個外觀問題都能免費翻新，更不能拿來替日本這次送修下保證。",
    "research_claim_refs": [
      "O10",
      "J08"
    ],
    "claim_class": "editorial_boundary",
    "visual": "form"
  },
  {
    "id": "c20r1i15",
    "chapter": "沒有盒與收據，還是把舊物送回去",
    "text": "這位作者最後寄去的，還是自己的粉紅色小盒；不過，他得先把它分開。",
    "research_claim_refs": [
      "J09",
      "J11"
    ],
    "claim_class": "attributed",
    "visual": "case"
  },
  {
    "id": "c20r1i16",
    "chapter": "沒有盒與收據，還是把舊物送回去",
    "text": "一只看起來完整的打火機，為什麼寄之前，會變成可以拆開的兩部分？",
    "research_claim_refs": [
      "J11",
      "O04"
    ],
    "claim_class": "question",
    "visual": "case"
  },
  {
    "id": "c20r1i17",
    "chapter": "沒有盒與收據，還是把舊物送回去",
    "text": "因為外面的翻蓋殼，和裡面負責燃料、火石、燈芯的內膽，本來就能分離。",
    "research_claim_refs": [
      "J11",
      "O04",
      "O05",
      "O06"
    ],
    "claim_class": "fact",
    "visual": "separate"
  },
  {
    "id": "c20r1i18",
    "chapter": "沒有盒與收據，還是把舊物送回去",
    "text": "把內膽拔出，底下還有毛氈墊，掀開才接觸到燃料室的填料。",
    "research_claim_refs": [
      "O04"
    ],
    "claim_class": "fact",
    "visual": "pad"
  },
  {
    "id": "c20r1i19",
    "chapter": "沒有盒與收據，還是把舊物送回去",
    "text": "你在外面看到的粉紅殼，沒有把所有工作機件，都固定成同一片金屬。",
    "research_claim_refs": [
      "O04",
      "J20"
    ],
    "claim_class": "editorial_link",
    "visual": "separate"
  },
  {
    "id": "c20r1i20",
    "chapter": "沒有盒與收據，還是把舊物送回去",
    "text": "但能拆出來，也就表示他能買到任意一組內膽，直接換進去嗎？",
    "research_claim_refs": [
      "J06"
    ],
    "claim_class": "question",
    "visual": "insert"
  },
  {
    "id": "c20r1i21",
    "chapter": "沒有盒與收據，還是把舊物送回去",
    "text": "他前面已經卡在尺寸；可分開，不等於眼前就有自己找得到的合用零件。",
    "research_claim_refs": [
      "J06",
      "O04"
    ],
    "claim_class": "editorial_link",
    "visual": "insert"
  },
  {
    "id": "c20r1i22",
    "chapter": "沒有盒與收據，還是把舊物送回去",
    "text": "我反而能理解，他為什麼在這裡把零件搜尋停下，轉向廠商的維修入口。",
    "research_claim_refs": [
      "J06",
      "J07"
    ],
    "claim_class": "reaction",
    "visual": "parcel"
  },
  {
    "id": "c20r1e01",
    "chapter": "把內膽拔出，讓包裹準備好出門",
    "text": "轉向廠商之後，寄件前先遇到的，卻不是誰來焊那片金屬，而是裡面的油。",
    "research_claim_refs": [
      "J11",
      "J12"
    ],
    "claim_class": "editorial_link",
    "visual": "separate"
  },
  {
    "id": "c20r1e02",
    "chapter": "把內膽拔出，讓包裹準備好出門",
    "text": "他在備忘錄整理了當時官網的要求：把內膽拔出，讓油完全蒸發。",
    "research_claim_refs": [
      "J12"
    ],
    "claim_class": "attributed",
    "visual": "dry"
  },
  {
    "id": "c20r1e03",
    "chapter": "把內膽拔出，讓包裹準備好出門",
    "text": "他記的乾燥時間是一整天；這是他二〇二四年那次準備寄件時的說明。",
    "research_claim_refs": [
      "J12"
    ],
    "claim_class": "attributed",
    "visual": "dry"
  },
  {
    "id": "c20r1e04",
    "chapter": "把內膽拔出，讓包裹準備好出門",
    "text": "為什麼不能直接把平常放在口袋裡的樣子，連油一起包走？",
    "research_claim_refs": [
      "J12"
    ],
    "claim_class": "question",
    "visual": "parcel"
  },
  {
    "id": "c20r1e05",
    "chapter": "把內膽拔出，讓包裹準備好出門",
    "text": "因為他讀到的寄修準備，要求處理的不是外表擦乾，而是內膽裡剩下的燃料。",
    "research_claim_refs": [
      "J12"
    ],
    "claim_class": "editorial_link",
    "visual": "dry"
  },
  {
    "id": "c20r1e06",
    "chapter": "把內膽拔出，讓包裹準備好出門",
    "text": "你若要照做，這一段不能當今天跨國寄件的通用規則；不同地方的程序會不同。",
    "research_claim_refs": [
      "J12",
      "U06"
    ],
    "claim_class": "viewer_conditional",
    "visual": "parcel"
  },
  {
    "id": "c20r1e07",
    "chapter": "把內膽拔出，讓包裹準備好出門",
    "text": "我在這裡最在意的，是油還藏在裡面；外面看起來乾，不是同一回事。",
    "research_claim_refs": [
      "J12",
      "O04"
    ],
    "claim_class": "reaction",
    "visual": "pad"
  },
  {
    "id": "c20r1e08",
    "chapter": "把內膽拔出，讓包裹準備好出門",
    "text": "油處理完，這兩個分開的部分，難道就能直接丟進袋子？",
    "research_claim_refs": [
      "J10",
      "J11"
    ],
    "claim_class": "question",
    "visual": "wrap"
  },
  {
    "id": "c20r1e09",
    "chapter": "把內膽拔出，讓包裹準備好出門",
    "text": "他列出的材料，有緩衝材、紙膠帶，以及家裡原有的夾鏈袋。",
    "research_claim_refs": [
      "J10"
    ],
    "claim_class": "attributed",
    "visual": "wrap"
  },
  {
    "id": "c20r1e10",
    "chapter": "把內膽拔出，讓包裹準備好出門",
    "text": "分開的兩部分，各自包起來，再收進袋子，是他文中整理的包法。",
    "research_claim_refs": [
      "J11"
    ],
    "claim_class": "attributed",
    "visual": "wrap"
  },
  {
    "id": "c20r1e11",
    "chapter": "把內膽拔出，讓包裹準備好出門",
    "text": "這是為了讓小物件寄得出去，那原來的禮盒，要不要也一起放？",
    "research_claim_refs": [
      "J08",
      "J10"
    ],
    "claim_class": "question",
    "visual": "emptybox"
  },
  {
    "id": "c20r1e12",
    "chapter": "把內膽拔出，讓包裹準備好出門",
    "text": "他引述當時官網說明，盒子之類的附屬品不要同封；保留寄修本體和必要資料。",
    "research_claim_refs": [
      "J12",
      "J13"
    ],
    "claim_class": "attributed",
    "visual": "parcel"
  },
  {
    "id": "c20r1e13",
    "chapter": "把內膽拔出，讓包裹準備好出門",
    "text": "這回他本來也沒有原盒，準備的重點，就落在小盒、內膽和修理表。",
    "research_claim_refs": [
      "J08",
      "J10",
      "J13"
    ],
    "claim_class": "editorial_link",
    "visual": "form"
  },
  {
    "id": "c20r1e14",
    "chapter": "把內膽拔出，讓包裹準備好出門",
    "text": "開頭那張修理表，除了描述故障，最不能填錯的是返還地址。",
    "research_claim_refs": [
      "J13"
    ],
    "claim_class": "attributed",
    "visual": "form"
  },
  {
    "id": "c20r1e15",
    "chapter": "把內膽拔出，讓包裹準備好出門",
    "text": "作者特別提醒，封口前要檢查；地址漏了，或寫錯了，回件就會出問題。",
    "research_claim_refs": [
      "J13"
    ],
    "claim_class": "attributed",
    "visual": "form"
  },
  {
    "id": "c20r1e16",
    "chapter": "把內膽拔出，讓包裹準備好出門",
    "text": "不知道那片彈簧的名字，這張表又要怎麼說清楚？",
    "research_claim_refs": [
      "J13"
    ],
    "claim_class": "question",
    "visual": "form"
  },
  {
    "id": "c20r1e17",
    "chapter": "把內膽拔出，讓包裹準備好出門",
    "text": "他的建議是，知道故障處就說清楚；不清楚，也可以寫下困擾。",
    "research_claim_refs": [
      "J13"
    ],
    "claim_class": "attributed",
    "visual": "form"
  },
  {
    "id": "c20r1e18",
    "chapter": "把內膽拔出，讓包裹準備好出門",
    "text": "這不表示我們看過他填完的表，或知道他最後畫了哪一個故障位置。",
    "research_claim_refs": [
      "J13"
    ],
    "claim_class": "editorial_boundary",
    "visual": "form"
  },
  {
    "id": "c20r1e19",
    "chapter": "把內膽拔出，讓包裹準備好出門",
    "text": "我喜歡這個順序：小盒在講哪裡不能工作，表格則替它留下回來的路。",
    "research_claim_refs": [
      "J13"
    ],
    "claim_class": "reaction",
    "visual": "parcel"
  },
  {
    "id": "c20r1e20",
    "chapter": "把內膽拔出，讓包裹準備好出門",
    "text": "材料齊了，這位作者用哪一種方式，把它寄出去？",
    "research_claim_refs": [
      "J10"
    ],
    "claim_class": "question",
    "visual": "mailer"
  },
  {
    "id": "c20r1e21",
    "chapter": "把內膽拔出，讓包裹準備好出門",
    "text": "他實際列出的寄件材料，還包括日本郵便的追蹤型郵件袋。",
    "research_claim_refs": [
      "J10"
    ],
    "claim_class": "attributed",
    "visual": "mailer"
  },
  {
    "id": "c20r1e22",
    "chapter": "把內膽拔出，讓包裹準備好出門",
    "text": "他說，自己不熟郵件怎麼被處理，也不想為了確認送達，一直打聽。",
    "research_claim_refs": [
      "J10",
      "J21"
    ],
    "claim_class": "attributed",
    "visual": "tracking"
  },
  {
    "id": "c20r1e23",
    "chapter": "把內膽拔出，讓包裹準備好出門",
    "text": "所以能追到包裹去了哪裡，對他來說，是選這種寄法的一個好處。",
    "research_claim_refs": [
      "J10",
      "J21"
    ],
    "claim_class": "attributed",
    "visual": "tracking"
  },
  {
    "id": "c20r1e24",
    "chapter": "把內膽拔出，讓包裹準備好出門",
    "text": "封好袋子之後，粉紅色禮物終於離開手邊；接下來，是等待一筆送達紀錄。",
    "research_claim_refs": [
      "J14",
      "J21"
    ],
    "claim_class": "editorial_link",
    "visual": "sealed"
  },
  {
    "id": "c20r1t01",
    "chapter": "郵件送達了，等的卻不是同一個時鐘",
    "text": "九月一日，他把包裹寄出；兩天後，追蹤頁面出現送達紀錄。",
    "research_claim_refs": [
      "J14",
      "J21"
    ],
    "claim_class": "attributed",
    "visual": "tracking"
  },
  {
    "id": "c20r1t02",
    "chapter": "郵件送達了，等的卻不是同一個時鐘",
    "text": "截圖顯示的是郵件已送到目的地，還不是工人已經拆開、開始修的證據。",
    "research_claim_refs": [
      "J21"
    ],
    "claim_class": "editorial_boundary",
    "visual": "tracking"
  },
  {
    "id": "c20r1t03",
    "chapter": "郵件送達了，等的卻不是同一個時鐘",
    "text": "你若也寄過珍惜的小物，看到送達時，可能才剛放下第一個擔心。",
    "research_claim_refs": [
      "J21"
    ],
    "claim_class": "viewer_conditional",
    "visual": "tracking"
  },
  {
    "id": "c20r1t04",
    "chapter": "郵件送達了，等的卻不是同一個時鐘",
    "text": "但到站之後，要等多久，才真的回到自己手裡？",
    "research_claim_refs": [
      "J15"
    ],
    "claim_class": "question",
    "visual": "sealed"
  },
  {
    "id": "c20r1t05",
    "chapter": "郵件送達了，等的卻不是同一個時鐘",
    "text": "這位作者說，寄之前查到的別人經驗，從一週到幾個月都有。",
    "research_claim_refs": [
      "J15"
    ],
    "claim_class": "attributed",
    "visual": "waiting"
  },
  {
    "id": "c20r1t06",
    "chapter": "郵件送達了，等的卻不是同一個時鐘",
    "text": "那些不同說法，沒有變成他這只小盒的交件日期。",
    "research_claim_refs": [
      "J15"
    ],
    "claim_class": "editorial_link",
    "visual": "waiting"
  },
  {
    "id": "c20r1t07",
    "chapter": "郵件送達了，等的卻不是同一個時鐘",
    "text": "他沒有這只打火機，就會每天覺得不方便嗎？",
    "research_claim_refs": [
      "J16"
    ],
    "claim_class": "question",
    "visual": "waiting"
  },
  {
    "id": "c20r1t08",
    "chapter": "郵件送達了，等的卻不是同一個時鐘",
    "text": "他說並不困擾，甚至想，只要年底前回來就好；沒有趕著要用。",
    "research_claim_refs": [
      "J16"
    ],
    "claim_class": "attributed",
    "visual": "waiting"
  },
  {
    "id": "c20r1t09",
    "chapter": "郵件送達了，等的卻不是同一個時鐘",
    "text": "我在這裡鬆一口氣，是因為他自己說不急，不必替這段等待加上焦慮。",
    "research_claim_refs": [
      "J16"
    ],
    "claim_class": "reaction",
    "visual": "waiting"
  },
  {
    "id": "c20r1t10",
    "chapter": "郵件送達了，等的卻不是同一個時鐘",
    "text": "而他等到的回件，是十月十八日早上。",
    "research_claim_refs": [
      "J14",
      "J15"
    ],
    "claim_class": "attributed",
    "visual": "sealed"
  },
  {
    "id": "c20r1t11",
    "chapter": "郵件送達了，等的卻不是同一個時鐘",
    "text": "回到開頭那趟四十七天的送修，能算出工人真正修了幾小時嗎？",
    "research_claim_refs": [
      "J15"
    ],
    "claim_class": "question",
    "visual": "sealed"
  },
  {
    "id": "c20r1t12",
    "chapter": "郵件送達了，等的卻不是同一個時鐘",
    "text": "算不出；那是從投寄到回到手上的旅程，不是連續維修的工時。",
    "research_claim_refs": [
      "J15"
    ],
    "claim_class": "editorial_boundary",
    "visual": "bench"
  },
  {
    "id": "c20r1t13",
    "chapter": "郵件送達了，等的卻不是同一個時鐘",
    "text": "你能從郵件日期算出旅程長度，卻不能因此算出，真正修理花了幾個小時。",
    "research_claim_refs": [
      "J15",
      "J21"
    ],
    "claim_class": "viewer_conditional",
    "visual": "tracking"
  },
  {
    "id": "c20r1t14",
    "chapter": "郵件送達了，等的卻不是同一個時鐘",
    "text": "包裹回到手邊，作者卻先有一個關於內膽的預期。",
    "research_claim_refs": [
      "J17"
    ],
    "claim_class": "attributed",
    "visual": "sealed"
  },
  {
    "id": "c20r1t15",
    "chapter": "郵件送達了，等的卻不是同一個時鐘",
    "text": "他理解到的處理方式，不是把原內膽裡的小零件逐一修復，而是換一組。",
    "research_claim_refs": [
      "J17",
      "J18"
    ],
    "claim_class": "attributed",
    "visual": "insert"
  },
  {
    "id": "c20r1t16",
    "chapter": "郵件送達了，等的卻不是同一個時鐘",
    "text": "既然換新的，那原來壞掉的這組，還會不會留給他？",
    "research_claim_refs": [
      "J17"
    ],
    "claim_class": "question",
    "visual": "sealed"
  },
  {
    "id": "c20r1t17",
    "chapter": "郵件送達了，等的卻不是同一個時鐘",
    "text": "作者原先以為，舊的應該不會回來；這就是他開包裹時的落差來源。",
    "research_claim_refs": [
      "J17"
    ],
    "claim_class": "attributed",
    "visual": "sealed"
  },
  {
    "id": "c20r1t18",
    "chapter": "郵件送達了，等的卻不是同一個時鐘",
    "text": "所以現在最值得看的一幕，不在我們沒見過的工廠裡，而在回件拆開之後。",
    "research_claim_refs": [
      "J18",
      "J22"
    ],
    "claim_class": "editorial_link",
    "visual": "sealed"
  },
  {
    "id": "c20r1n01",
    "chapter": "包裹裡，新舊內膽都在",
    "text": "開頭那個回件包裹打開後，他寫下的結果是：新舊兩組內膽，都在裡面。",
    "research_claim_refs": [
      "J18"
    ],
    "claim_class": "attributed",
    "visual": "sealed"
  },
  {
    "id": "c20r1n02",
    "chapter": "包裹裡，新舊內膽都在",
    "text": "作者附的照片，左邊是打開的粉紅殼，裡面裝著一組內膽。",
    "research_claim_refs": [
      "J22"
    ],
    "claim_class": "attributed",
    "visual": "returned"
  },
  {
    "id": "c20r1n03",
    "chapter": "包裹裡，新舊內膽都在",
    "text": "右邊還有另一組，表面磨損比較明顯，放在氣泡材料上。",
    "research_claim_refs": [
      "J22"
    ],
    "claim_class": "fact",
    "visual": "oldinsert"
  },
  {
    "id": "c20r1n04",
    "chapter": "包裹裡，新舊內膽都在",
    "text": "我最意外的不是「換新」這兩個字，而是舊的那組，也沒有在這次寄修後消失。",
    "research_claim_refs": [
      "J17",
      "J18"
    ],
    "claim_class": "reaction",
    "visual": "returned"
  },
  {
    "id": "c20r1n05",
    "chapter": "包裹裡，新舊內膽都在",
    "text": "他還寫，連自己寄去的東西都回來了，圖說也提到緩衝材和紙膠帶。",
    "research_claim_refs": [
      "J19"
    ],
    "claim_class": "attributed",
    "visual": "wrappingreturn"
  },
  {
    "id": "c20r1n06",
    "chapter": "包裹裡，新舊內膽都在",
    "text": "那是不是只要送修，你就能把原殼、原內膽，還有每片零件全留下？",
    "research_claim_refs": [
      "J18",
      "U03",
      "U04"
    ],
    "claim_class": "viewer_question",
    "visual": "returned"
  },
  {
    "id": "c20r1n07",
    "chapter": "包裹裡，新舊內膽都在",
    "text": "這一次的回件，回答不了每一次送修；不同地方，對舊件有不同的處理條件。",
    "research_claim_refs": [
      "J18",
      "U04"
    ],
    "claim_class": "editorial_link",
    "visual": "form"
  },
  {
    "id": "c20r1n08",
    "chapter": "包裹裡，新舊內膽都在",
    "text": "像英國二〇二六年版修理表，就明寫內膽不逐件修，正常做法是整組更換。",
    "research_claim_refs": [
      "U03"
    ],
    "claim_class": "attributed",
    "visual": "insert"
  },
  {
    "id": "c20r1n09",
    "chapter": "包裹裡，新舊內膽都在",
    "text": "如果想拿回原來的內膽，要在特別說明欄提出要求；它不會自動寄回。",
    "research_claim_refs": [
      "U04"
    ],
    "claim_class": "attributed",
    "visual": "form"
  },
  {
    "id": "c20r1n10",
    "chapter": "包裹裡，新舊內膽都在",
    "text": "這份表上，還能提出哪些跟外殼有關的要求？",
    "research_claim_refs": [
      "U08"
    ],
    "claim_class": "question",
    "visual": "form"
  },
  {
    "id": "c20r1n11",
    "chapter": "包裹裡，新舊內膽都在",
    "text": "你甚至可以勾「不要修鉸鏈」；「有紀念意義」也有另外的欄位。",
    "research_claim_refs": [
      "U08"
    ],
    "claim_class": "viewer_conditional",
    "visual": "form"
  },
  {
    "id": "c20r1n12",
    "chapter": "包裹裡，新舊內膽都在",
    "text": "可是我們能因此說，日本這位作者，當年也提出了同樣要求嗎？",
    "research_claim_refs": [
      "J13",
      "J18",
      "U04"
    ],
    "claim_class": "question",
    "visual": "returned"
  },
  {
    "id": "c20r1n13",
    "chapter": "包裹裡，新舊內膽都在",
    "text": "不能；他沒有公開填妥的修理表，也沒有交代，廠方為什麼把舊內膽一起退回。",
    "research_claim_refs": [
      "J13",
      "J18"
    ],
    "claim_class": "editorial_boundary",
    "visual": "form"
  },
  {
    "id": "c20r1n14",
    "chapter": "包裹裡，新舊內膽都在",
    "text": "英國的條件，是英國的條件；不能倒過來，替這次日本回件填上一個原因。",
    "research_claim_refs": [
      "J18",
      "U04"
    ],
    "claim_class": "editorial_boundary",
    "visual": "returned"
  },
  {
    "id": "c20r1n15",
    "chapter": "包裹裡，新舊內膽都在",
    "text": "我覺得，到這裡停住，反而保住了這個小故事真正特別的地方：他確實拿回了兩組。",
    "research_claim_refs": [
      "J18"
    ],
    "claim_class": "reaction",
    "visual": "returned"
  },
  {
    "id": "c20r1n16",
    "chapter": "包裹裡，新舊內膽都在",
    "text": "那組看起來比較乾淨的內膽，就能當成成功點火的證明嗎？",
    "research_claim_refs": [
      "J22"
    ],
    "claim_class": "question",
    "visual": "oldinsert"
  },
  {
    "id": "c20r1n17",
    "chapter": "包裹裡，新舊內膽都在",
    "text": "這份回件紀錄沒有火焰，也沒有記下換新後的燃燒表現。",
    "research_claim_refs": [
      "J22"
    ],
    "claim_class": "editorial_boundary",
    "visual": "returned"
  },
  {
    "id": "c20r1n18",
    "chapter": "包裹裡，新舊內膽都在",
    "text": "我們看到的是回來的物件；「能用，否則免費修」，則仍是廠商的功能承諾。",
    "research_claim_refs": [
      "J22",
      "O07"
    ],
    "claim_class": "editorial_link",
    "visual": "case"
  },
  {
    "id": "c20r1n19",
    "chapter": "包裹裡，新舊內膽都在",
    "text": "開頭那只粉紅殼，這次沒有把「換新」變成「舊件消失」；這是回件留下的答案。",
    "research_claim_refs": [
      "J18",
      "O07"
    ],
    "claim_class": "editorial_answer",
    "visual": "returned"
  },
  {
    "id": "c20r1n20",
    "chapter": "包裹裡，新舊內膽都在",
    "text": "如果是你的禮物，你會留著換下來的內膽，還是只要手裡那只繼續陪你？",
    "research_claim_refs": [],
    "claim_class": "cta",
    "visual": "gift"
  },
  {
    "id": "c20r1n21",
    "chapter": "包裹裡，新舊內膽都在",
    "text": "想繼續看日用品一句承諾，怎麼變成具體的選擇，歡迎訂閱品牌故事。",
    "research_claim_refs": [],
    "claim_class": "cta",
    "visual": "gift"
  }
];
const visual={
gift:'An anonymous adult holding a small plain pink hinged metal case above a wooden tabletop, thoughtful expression, warm indoor light.',
inspect:'An anonymous adult examining a small plain pink hinged metal case on a wooden tabletop, puzzled expression, gentle window light.',
insert:'A worn plain silver lighter insert on a wooden tabletop, a tiny curved metal strip visible near its upper rim, soft side light.',
wheel:'Close view of the small serrated wheel on a plain silver lighter insert resting on a wooden tabletop, muted indoor light.',
search:'An anonymous adult looking at an unmarked component tray beside a plain pink hinged metal case, uncertain expression, soft desk light.',
supplies:'An anonymous adult studying a small flint and a short pale wick beside a plain silver insert on a work surface, gentle side light.',
fuel:'A plain silver insert resting upright beside a closed unmarked metal fuel can on a wooden surface, mild window light.',
parcel:'An anonymous adult preparing an empty padded mailer beside a plain pink hinged metal case, focused expression, soft window light.',
form:'An anonymous adult pausing with a pencil over a face-down unmarked sheet beside a closed plain pink hinged metal case and an empty padded mailer, soft window light.',
emptybox:'An anonymous adult looking at an empty plain cardboard tray beside a small plain pink hinged metal case, thoughtful expression, soft room light.',
choice:'An anonymous adult considering a closed plain pink hinged metal case on a small table, thoughtful expression, warm room light.',
case:'A closed plain pink hinged metal case resting at the center of a simple wooden tabletop, soft side light.',
hinge:'A close view of a simple hinge joining the lid and body of a plain pink metal case, mild side light.',
separate:'An anonymous adult holding a plain silver lighter insert above an open plain pink metal case on a wooden tabletop, gentle window light.',
pad:'A close view of a pale felt pad at the base of a plain silver lighter insert resting on a clean table, soft side light.',
dry:'A plain silver lighter insert resting separately from an open plain pink metal case on a clear wooden tabletop beside a window, muted daylight.',
wrap:'An anonymous adult wrapping a plain silver insert in cushioning beside a separately wrapped plain pink metal case, mild desk light.',
mailer:'An anonymous adult holding an empty plain gray mailing pouch beside a small cushioned object on a tabletop, soft indoor light.',
tracking:'An anonymous adult checking a device showing only abstract nonlinguistic marks beside a sealed plain gray mailer, gentle room light.',
waiting:'An anonymous adult seated beside an empty space on a small wooden tabletop, relaxed expression, mild window light.',
sealed:'An anonymous adult resting one hand beside a closed opaque plain gray padded mailer on a wooden table, anticipatory expression, soft window light.',
bench:'An empty simple maintenance workbench with an unmarked tool tray and a closed plain gray padded mailer, gentle side light.',
returned:'An open plain pink hinged metal case holding a plain silver lighter insert on cushioning, another worn plain silver insert nearby, soft window light.',
oldinsert:'A worn plain silver lighter insert resting on clear cushioning beside the edge of an open plain pink metal case, gentle side light.',
wrappingreturn:'An anonymous adult setting plain cushioning and a short strip of pale tape beside an open plain pink metal case on a wooden table, soft indoor light.'
};
const seen=new Map();let globalShotIndex=0;for(const r of rows){assert(visual[r.visual],r.visual);const n=seen.get(r.visual)??0;seen.set(r.visual,n+1);const framing=['Medium shot','Close-up','Medium close-up','Wide shot'];r.prompt=framing[n%4]+' of '+visual[r.visual];r.camera=['push in','pan left','pull out','pan right'][globalShotIndex++%4];}
const promptOverrides={
  "c20r1o09": "Close-up of a plain silver lighter insert base with its felt pad visible beside a closed unmarked fuel can, mild side light.",
  "c20r1o15": "Medium shot of a narrow plain pink hinged metal case beside a wider plain dark green hinged metal case on a table, soft indoor light.",
  "c20r1o18": "Close-up of a plain pink metal case resting on a folded neutral cloth, gentle side light.",
  "c20r1o20": "Medium shot of an anonymous adult considering a small plain pink hinged metal case held in one hand, soft room light.",
  "c20r1i03": "Close-up of a plain pink hinged metal case beside an unmarked component tray, gentle light from the left.",
  "c20r1i07": "Medium shot of an anonymous adult examining an open plain pink metal case, thoughtful expression, soft window light.",
  "c20r1i14": "Close-up of a simple hinge along a plain pink metal lid, muted side light.",
  "c20r1i16": "Medium close-up of an anonymous adult holding an open plain pink metal case above a wooden table, soft room light.",
  "c20r1i20": "Medium shot of an anonymous adult looking at several unmarked metal components in a small tray, uncertain expression, soft desk light.",
  "c20r1i21": "Close-up of a narrow plain pink metal case beside the edge of a wider plain dark green metal case, gentle window light.",
  "c20r1e03": "Close-up of the base of a plain silver insert standing alone on a clear wooden surface near a window, muted daylight.",
  "c20r1e09": "Close-up of clear cushioning, a short strip of pale tape and an empty transparent pouch arranged on a clean tabletop, soft overhead light.",
  "c20r1e10": "Medium shot of anonymous hands placing two separately cushioned small metal objects into a transparent pouch, gentle side light.",
  "c20r1e13": "Close-up of an unmarked sheet resting beside a transparent pouch containing two cushioned shapes, soft window light.",
  "c20r1e15": "Medium shot of anonymous hands inspecting the back of an unmarked sheet before an open gray mailer on a desk, soft indoor light.",
  "c20r1e16": "Close-up of a plain silver lighter insert on a wooden surface with an unmarked pencil nearby, muted side light.",
  "c20r1e18": "Medium shot of a closed plain pink hinged metal case resting alone on a neutral cloth, soft room light.",
  "c20r1e19": "Close-up of anonymous hands placing an unmarked folded sheet beside a small cushioned pink object, gentle desk light.",
  "c20r1e21": "Close-up of a plain gray mailing pouch on a clear wooden surface with the small cushioned object beside it, mild overhead light.",
  "c20r1e23": "Medium shot of an anonymous adult holding a device showing only abstract nonlinguistic marks, no mailer in view, soft room light.",
  "c20r1t02": "Close-up of a closed opaque gray padded mailer on a simple tabletop beside an empty unmarked tool tray, muted side light.",
  "c20r1t03": "Medium close-up of anonymous hands holding a device with a few abstract nonlinguistic marks above a clear tabletop, gentle window light.",
  "c20r1t05": "Wide shot of a closed opaque gray mailer on a wooden desk beside a stack of unmarked sheets, soft side light.",
  "c20r1t07": "Close-up of an empty spot on a small wooden tabletop beside a simple chair, soft window light.",
  "c20r1t09": "Medium shot of an anonymous adult sitting comfortably beside an uncluttered table, relaxed shoulders, warm indoor light.",
  "c20r1t11": "Close-up of a closed opaque gray mailer beside an unmarked wristwatch face without symbols, muted desk light.",
  "c20r1t16": "Medium shot of an anonymous adult looking at a closed opaque gray padded mailer from across a simple table, soft window light.",
  "c20r1t17": "Close-up of a worn plain silver insert on a neutral tabletop, mild side light, no parcel or other object in view.",
  "c20r1t18": "Close-up of an unopened opaque plain gray padded mailer at the center of a clean table, gentle overhead light.",
  "c20r1n10": "Close-up of an anonymous hand holding an unmarked pencil above a face-down plain sheet beside a metal hinge, soft side light.",
  "c20r1n11": "Medium shot of an anonymous adult examining an open plain pink hinged metal case beside a folded unmarked sheet, soft window light.",
  "c20r1n15": "Close-up of two plain silver inserts resting separately on clear cushioning, one visibly more worn, muted window light."
};for(const r of rows)if(promptOverrides[r.id])r.prompt=promptOverrides[r.id];
const pairDefs=[['c20r1h05','c20r1e14','return-address-before-sealing'],['c20r1h06','c20r1n01','closed-return-parcel']];for(const[a,b]of pairDefs){const setup=rows.find(r=>r.id===a),payoff=rows.find(r=>r.id===b);setup.prompt=payoff.prompt;setup.camera=payoff.camera;}
const loopDefs=[['h04','o01','先找零件是否能自己修'],['h05','e14','封口前修理表上的返還地址'],['h06','n01','返還包裹是否只有換新的機件'],['h08','n19','換新是否讓舊內膽消失'],['o03','o04','曾做保養和這次裂彈簧的差別'],['o14','o15','零件搜尋卡在非regular尺寸'],['o20','i06','沒有盒收據最後仍選寄修'],['i07','i08','功能保證實際接住哪個要求'],['i10','i11','功能保證不含外觀翻新'],['i12','i13','未滿一年外觀問題可聯絡客服談選項'],['i16','i17','外殼與內膽可分離'],['e04','e05','油藏在內膽而非只擦外表'],['e08','e10','分開用緩衝材包再收袋'],['e16','e17','不確定故障名稱也可描述困擾'],['e11','e12','包裹不附盒子等配件'],['e20','e21','作者採用能追蹤的郵件袋'],['t04','t10','等到10月18日早上回件'],['t07','t08','作者不急用只期待年底前回'],['t11','t12','投寄到手日期不是維修工時'],['t16','n01','舊內膽也在這次包裹中'],['n06','n09','地域條件不同並非每次自動退舊'],['n12','n13','個案未公開完成表故未知退舊原因'],['n10','n11','UK表另有不修hinge與紀念性選項'],['n16','n17','回件照片不等於燃燒測試']];
const loops=loopDefs.map(([a,b,what])=>({setup:'c20r1'+a,payoff:'c20r1'+b,what}));
const title='Zippo免費修，47天後包裹多一組？｜品牌故事';
const scenes=[];let chapter='';for(const r of rows.slice(0,-3)){const s={id:r.id,template:'shot',data:{prompt:r.prompt,visual:'still',camera:r.camera},lines:[{id:r.id,text:r.text,emotion:'對一位觀眾自然說書，四到五字每秒的聊天速度；實際觀察、作者推測與當代地域條款讀清楚'}]};if(r.chapter!==chapter){chapter=r.chapter;s.chapter=chapter;}scenes.push(s);}
scenes.push({id:'c20r1outro',template:'outro',data:{title:'換新，也留下舊內膽',cta:'你會保留換下的舊機件嗎？'},lines:rows.slice(-3).map(r=>({id:r.id,text:r.text,emotion:'對一位觀眾溫暖收束，自然邀請'}))});
const usedIds=new Set(rows.flatMap(r=>r.research_claim_refs).flatMap(id=>{const c=research.claims.find(c=>c.id===id);assert(c,id);return[c.evidence.source_id,...(c.supporting_caption_evidence?[c.supporting_caption_evidence.source_id]:[])];}));
const sources=research.sources.filter(s=>usedIds.has(s.id));
const description='一只用了約三到四年的粉紅色液體燃料打火機，磨輪不轉、無法點火後，被寄回維修。沿著日本作者ゆきいるか2024年的公開備忘錄及其原物照片，追到新舊內膽返還的結果。47日是2024-09-01投寄到10-18回件的單次紀錄，不是保證時限。沒有返還後成功點火、完整作業單、填妥表格或廠方退舊理由；英國2026條件與美國當代功能／外觀範圍只作明示地域對照，不倒推日本2024。匿名概念插圖，不重建真實長相、商標或可讀表單。\n\n原始來源（下載／親讀2026-10-26；歷史與現行分開）：\n'+sources.map(s=>s.publisher+'：'+s.research_use+'\n'+s.url).join('\n');
const doc={schema_version:1,slug:SLUG,format:'drama',category:'story',narration_locale:'zh-TW',target_minutes:[12,14],voice,subtitles:{burn_in:true},look:{preset:'cute-mystery'},characters:[],music:{prompt:'light, curious, a little mysterious, no vocals',gain_db:-20,duck_db:-10},loops,youtube:{category_id:27,made_for_kids:false,default_language:'zh-TW',title,description,tags:['Zippo','之寶','打火機','維修','品牌故事','日用品的意外轉身'],video_id:null},thumbnail:{template:'thumb',data:{layout:'d',headline:'免費修多一組',sub:'47天後打開包裹',brand:'ZIPPO',tag:'品牌故事',shot:'c20r1h02'}},sources:sources.map(s=>({title:s.publisher+' '+s.id,url:s.url,checked_on:'2026-10-26'})),assets:[],scenes};
const validation=validateVideo(doc);assert.equal(validation.errors?.length??0,0,JSON.stringify(validation.errors));write('video.json',doc);write('narration-only.json',rows.map(({chapter,id,text})=>({chapter,id,text})));
const script=['# '+title,'','C20 R1作者稿，HOLD。ID／章名不讀；13分鐘是原目標，字量容量風險如實保留，沒有用紙面字量冒充實聲。待另一位來源／配鏡QA與全新讀者；沒有SOURCE PASS、敘事批准或owner批准。',''];chapter='';for(const r of rows){if(r.chapter!==chapter){chapter=r.chapter;script.push('## '+chapter,'');}script.push('### '+r.id,'',r.text,'');}fs.writeFileSync(path.join(OUT,'script.md'),script.join('\n'));
const anchorRegistry={};for(const c of research.claims){anchorRegistry[c.id+'-Q1']={id:c.id+'-Q1',research_claim_id:c.id,...c.evidence};if(c.supporting_caption_evidence)anchorRegistry[c.id+'-CAPTION']={id:c.id+'-CAPTION',research_claim_id:c.id,...c.supporting_caption_evidence};}
const jp=research.sources.find(s=>s.id==='JP_NOTE'),jpText=fs.readFileSync(jp.text_path,'utf8'),normalize=x=>x.replace(/\s+/g,' ').trim();
const extraQuotes={J08:'新しく買うのも視野にいれつつ修理料金調べた',J10:'届いたかどうかで問い合わせるのも億劫だったので',J12:'箱などの付属品は同封しないよう',J13:'ご返却先住所を未記入、または間違えると帰ってこない',J15:'1週間や3か月、半年',J07:'純正品であれば無料生涯保障'};
for(const[id,q]of Object.entries(extraQuotes)){assert(normalize(jpText).includes(normalize(q)),q);anchorRegistry[id+'-EXTRA']={id:id+'-EXTRA',research_claim_id:id,source_id:'JP_NOTE',raw_path:jp.raw_path,raw_sha256:jp.raw_sha256,quote:q,locator:{text_path:jp.text_path,text_sha256:jp.text_sha256,normalized_whitespace:true,normalized_text_character_offset:normalize(jpText).indexOf(normalize(q))},role:'Additional short exact anchor from the same personally read primary account; does not edit frozen research.'};}
const classes={attributed:'作者／公司有歸屬敘述',fact:'原件支持的限定事實',question:'旁白疑問',viewer_question:'對觀眾提問',reaction_question:'旁白反應與疑問',reaction:'旁白意見／反應',viewer_conditional:'對觀眾的明示條件／假設',viewer_reaction:'對觀眾反應',editorial_link:'編輯連接',editorial_boundary:'來源範圍界線',editorial_promise:'本集命名承諾',editorial_answer:'片尾回呼答案',cta:'觀眾邀請'};
const authored=rows.map((r,i)=>{const facts=r.research_claim_refs.map(id=>research.claims.find(c=>c.id===id));const anchors=Object.values(anchorRegistry).filter(a=>r.research_claim_refs.includes(a.research_claim_id));return{id:r.id,scene_id:i>=rows.length-3?'c20r1outro':r.id,claim:r.text,claim_class:classes[r.claim_class],claim_kind:r.claim_class,research_claim_ids:r.research_claim_refs,source_ids:[...new Set(anchors.map(a=>a.source_id))],quote_ids:anchors.map(a=>a.id),source_evidence:anchors,limits:facts.map(c=>c.forbidden_inferences_zh),visual_prompt:i>=rows.length-3?'Native outro typography; no generated image':r.prompt,visual_scope:'Anonymous explanatory concept; plain pink hinged case, unmarked insert and parcel only. No named face, logo, readable letters, copyrighted decorative graphic, flame, successful ignition, unobserved factory operation or filled personal form.',independent_source_review:'PENDING_OTHER_REVIEWER',independent_visual_review:'PENDING_OTHER_REVIEWER'};});
for(const[a,b,asset]of pairDefs)for(const id of[a,b])authored.find(r=>r.id===id).planned_same_image={plan:'image-reuse-plan.json',asset_plan_id:asset,source_scene_id:b,reuse_scene_id:a,actual_file_sha256:null,status:'PLAN_ONLY'};
write('claims.json',{schema_version:1,status:'PENDING_INDEPENDENT_SOURCE_AND_VISUAL_QA',candidate_revision:'c20-r1',author:'/root/c20_primary_research',video_slug:SLUG,frozen_research_sha256:PROTECTED,source_registry:Object.fromEntries(research.sources.map(s=>[s.id,s])),anchor_registry:anchorRegistry,rows:authored,source_pass_claimed:false,approvals_created:0});
const cm=['# C20 R1 逐句來源與書面配鏡','','作者綁定，不是獨立SOURCE PASS。原研究63claims／raw及68舊檔保持原SHA。每句寫清歸屬、反應、假設、來源邊界；原圖只作研究參照。','','| ID | 旁白 | 分類 | 原文錨點 |','| --- | --- | --- | --- |'];for(const c of authored)cm.push(`| ${c.id} | ${c.claim} | ${c.claim_class} | ${c.quote_ids.join('、')} |`);cm.push('','## 原件界線','','日本個案2024只見返還新舊內膽；未明證成功點火、維修作業、填妥表格、Sentimental、要求退舊或廠方原因。JP_NOTE操作建議不冒本人實際每一步，更不冒現行日本條款；當前官方maintenance未讀到實質條款。US功能／finish與UK2026insert更換／comments要求各守地域與時間。未將Joseph/Jetta/Gatsby案例拼同物。','');fs.writeFileSync(path.join(OUT,'claims.md'),cm.join('\n'));
const series={kind:'story',slug:'brand-story-remakes-20261025',episode:20,chapter:1,title,logline:'日本2024粉紅色液體燃料打火機點不著，寄修後新舊內膽同回；跟同一物件看換與留的界線。',names:['Zippo','之寶','ゆきいるか'],characters:[],visual_tier:'stills',compilation:false,target_minutes:13,image_model:'image-01',look:{preset:'cute-mystery'},candidate_revision:'c20-r1',status:'hold_pending_independent_source_and_fresh_readers'};write('series.json',series);
const whole=rows.reduce((n,r)=>n+spokenUnits(r.text),0),opening=rows.filter(r=>r.chapter===rows[0].chapter).reduce((n,r)=>n+spokenUnits(r.text),0),cta=rows.slice(-2).reduce((n,r)=>n+spokenUnits(r.text),0);assert(rows.every(r=>spokenUnits(r.text)<=40));
const brief=['# C20 R1｜寄出粉紅殼，回來新舊內膽','','狀態：HOLD_PENDING_INDEPENDENT_SOURCE_AND_FRESH_READERS。作者交接，不是來源自核或owner批准。新slug '+SLUG+'，不重綁舊episode，不沿用舊批准。','','## 問題','','免費修，最後讓什麼換了新，又讓什麼留了下來？','','## 一句答案','','在日本作者這一次回件裡，粉紅殼與新舊內膽一起返還；沒有回件後燃燒測試或退舊理由的證據。','','## 站主觀點','','跟同一只真實物件的抉擇、投寄與回件推故事；不為湊長度添年表、WWII、產量或其他維修案例。','','## 單一主線與開場','','ゆきいるか2024日本粉紅case：收到禮物用了約3–4年→cam spring裂／作者不確定因果的wheel不轉／不能點火→網購找不到非regular尺寸零件→查保證→無盒收據仍寄修→分離內膽讓油蒸發／包裝／表格返還地址→9/1寄9/3送達→10/18回件→先以為舊件不回，結果新舊inside unit都在。沒有自創觀眾、工人診斷或廠內連續工序。頭兩句以你及約3–4年進場；六句內有真案動作與原圖相關場景。最多兩事件預告：修理表h05→e14，回件封袋h06→n01；h07點名Zippo與47日，h08中央問題。兩組均用中性前置圖，沒有先畫出地址／新舊內膽結果。','','## 字量與實聲風險','','全篇 '+whole+' native spokenUnits（coldopen '+opening+'，有聲CTA '+cta+'），含冷開場與有聲CTA，只排另外加入的5秒／21秒頻道bookends。目標仍13分鐘／約3500，不降低目標；現稿差'+(3500-whole)+'units，保留MATERIAL_CAPACITY_RISK，不以字量宣稱13min-ready。4–5 units/s算術約'+(whole/5).toFixed(1)+'–'+(whole/4).toFixed(1)+'秒，只是算術；actual_narration_seconds與actual_final_seconds均null。研究容量2290–3440已有風險，作者沒有用第二案例、保養清單或重述填到假門檻。','','## 畫面與聲音','','匿名英文prompt、image-01、stills、唯一look {preset:cute-mystery}。正文相關shot100%，無連續卡；無品牌／真人／logo／可讀表單／版權裝飾圖，不畫火焰或未見廠內修理。只取C06完整voice物件，沒有借C06字典或批准；新project正常initializeStoryLexicon。原生same-image完整輸入key、payoff first takes1、唯讀cache guard／缺cache停、兩端judge與裁切後實檔SHA待驗，詳image-reuse-plan.json；actualfalse。','','## 來源與地域','','JP2024乾燥一天／郵件袋均屬當事人當時敘述，不當現行寄件教學；US現在功能/外觀條款獨立，UK2026更換/退舊要求不倒推日本。沒有完成表、勾選、退舊要求、工單、郵資或功能測試，舊件回來的原因未知。','','## 待辦','','別位來源與書面配鏡QA、全新原生雙讀者、精確owner核稿／企劃、正式branding只讀preflight、製片入場、真TTS與時長／聲音檢查、實圖／同圖／成片QA均待完成。作者不寫verify-1，不自PASS，不拉production pin；provider／paid／backend／Git均0。',''];fs.writeFileSync(path.join(OUT,'brief.md'),brief.join('\n'));
const coreFiles=['video.json','script.md','narration-only.json','claims.json'],coreHashes=Object.fromEntries(coreFiles.map(f=>[f,fileSha(path.join(OUT,f))]));
const plan={
  "schema_version": 1,
  "revision": "c19-r2",
  "status": "WRITTEN_REUSE_PLAN_PENDING_GENERATION_AND_REAL_FILE_SHA_VERIFICATION",
  "not_a_video_schema_extension": true,
  "not_a_keyframes_manifest": true,
  "no_assets_generated": true,
  "actual_same_asset_verified": false,
  "candidate_binding": {
    "core_four_sha256": {
      "video.json": "ee3ecc0b38fa986ea69c3f8f6d29fb3ce770b5f031ba3ea8f2c903f3218ea493",
      "script.md": "5831b821fb7a0c118a7c123ad4b8c7c05c0702aad04f2fdfd676c20ce209bbcc",
      "narration-only.json": "bf1299053e51efdbb40f2dd5b8396f6532e72b07aa40f9879962f469d6f89586",
      "claims.json": "728d4c243d0c07bc560814cef019ba2882ef2aba770f599375e57c29c0dce9e3"
    },
    "claims_md_sha256": "b61d2ebae9dbcade1c4321d39d55c6a08bc06b9c1fd2eeacf40b1e17e1453c9c",
    "brief_sha256": "0135b4b158f913bcc194e82add785800930e9040390a5388710996bf0f19d144",
    "series_sha256": "5b0dd1c9e5193fd61180ccaefb5c8d02f32853fad2eec2ae9b8bb2f7960f9cde"
  },
  "rule": {
    "file": ".agents/skills/youtube-video/references/script-writing.md",
    "sha256": "bbb1fe37e8ae9458a961324d6a13e512eab6c5d07493954338ecc2bf2c1f0392",
    "quote": "每一個預告句用回收它的那一章的畫面（同一張圖）"
  },
  "code_readback": {
    "files_sha256": {
      "tools/video/media/keyframes.mjs": "c9e80d93d91d349699446f04edc56906edf552d5225d3c25c2795c7459cef6a6",
      "tools/video/media/stages.mjs": "94c3608376402477dc98d4664316df7723128bd25b4e6da7bc8c889ee3a517df",
      "tools/video/media/cache.mjs": "df1eb83a26e4cbe756047a4f9d920cfac048ad9b93e6729d657bdd45da6c288d",
      "tools/video/media/prompt-budget.mjs": "f7010c3a252336b6fd7ea0c8615a628005645e4364e89242698bc9f6e7e80404",
      "tools/video/core/drama.mjs": "0877885c11f51b794b64ee1d3a76a8b0193d239127f84e26856d6506a9b4bee1",
      "tools/video/media/trim.mjs": "37e3b9fd6b9c30cb058447588232e769357b628b3d6bff69db905e37e238ad1b"
    },
    "still_alias_field_available": false,
    "clip_source_field_not_applicable": "Still data.source is unsupported; no alias or custom video schema field was invented.",
    "native_supported_route": "Official keyframes --shot with the ordinary exact-request cache, independently judged at both endpoints.",
    "cache_identity": "The pure local Stage.imageKey was called with declared model/version/size and full request inputs. Scene ID and output target do not enter the native key.",
    "camera_matters": "Camera is part of composed prompt and must be identical.",
    "guard_is_read_only": "Use readCache plus existsSync and SHA of actual bytes. Never use cached() as a read-only guard: it can delete an invalid entry and write cache.json."
  },
  "pairs": [
    {
      "asset_plan_id": "branch-tissue-packet",
      "role": "PLANNED_ONE_IDENTICAL_IMAGE_NOT_AN_ACTUAL_ASSET",
      "source_scene_id": "c19r1a18",
      "source_line_id": "c19r1a18",
      "reuse_scene_id": "c19r1h05",
      "reuse_line_id": "c19r1h05",
      "narration_setup_text": "銀行分行裡的一包面紙，會怎麼把客人帶向超商？",
      "narration_payoff_text": "開頭那包面紙，就是合作金融機構製作、在自家分行發送的宣傳物。",
      "source_prompt_sha256": "be0e11a00850b0742b6ca775cc37691b165a5373bff1fa208224680e9d2e37fd",
      "reuse_prompt_sha256": "be0e11a00850b0742b6ca775cc37691b165a5373bff1fa208224680e9d2e37fd",
      "prompt_exact_match": true,
      "source_camera": "push in",
      "reuse_camera": "push in",
      "composed_prompt_sha256": "278737e97de32f36c15505a69bf89df04bfdcbd787fc2305a22374e6141dcfe0",
      "no_result_drawn_in_teaser": "A worker holds a closed blank packet before distribution; no recipient, completed handoff, promotional wording or usage-growth result is shown.",
      "native_same_input_key_rehearsal": {
        "pure_local_functions_only": true,
        "input_tuple": {
          "provider": "minimax",
          "model": "image-01",
          "prompt": "Medium close-up at a plain bank branch counter, an anonymous employee holding a small unmarked tissue packet beside a blank folded poster, mild overhead light.. Style: cute Taiwanese YouTube explainer cartoon: chibi characters with big round heads, large expressive eyes and exaggerated comic expressions, thick clean dark outlines, flat colours with soft cel shading, a limited palette of deep navy night, parchment yellow, muted teal and one warning-red accent, subtle paper grain, simple clear backgrounds, one subject in the centre third, playful and friendly, 16:9. Camera: push in",
          "negative": "",
          "width": 1920,
          "height": 1080,
          "seed": 1,
          "references": []
        },
        "aspect": "16:9",
        "requested_size": null,
        "nominal_image_size": "1K",
        "image_selection_version": 1,
        "seed_offset": 0,
        "takes": 1,
        "correction_list": [],
        "prompt_budget_chars": 1500,
        "base_key": "4297efec8b809bb9",
        "native_stage_key": "405c4c491292b652",
        "parameters_are_declared_plan_not_backend_readback": true,
        "no_provider_call": true
      },
      "actual_source_file": null,
      "actual_source_sha256": null,
      "actual_reused_file": null,
      "actual_reused_sha256": null,
      "actual_same_asset_verified": false,
      "actual_same_file_sha_verified": false
    },
    {
      "asset_plan_id": "cash-management-container",
      "role": "PLANNED_ONE_IDENTICAL_IMAGE_NOT_AN_ACTUAL_ASSET",
      "source_scene_id": "c19r1n10",
      "source_line_id": "c19r1n10",
      "reuse_scene_id": "c19r1h06",
      "reuse_line_id": "c19r1h06",
      "narration_setup_text": "而機器裡的鈔票，真的是裝得越多越好嗎？",
      "narration_payoff_text": "回到開頭那個問題：多放現金，能少補幾次，卻會讓資金成本上升。",
      "source_prompt_sha256": "fbd5d420f9b8f5bccdd3ccff57b65e2054c4ab20eb3f497a665dfe9f1e072c8d",
      "reuse_prompt_sha256": "fbd5d420f9b8f5bccdd3ccff57b65e2054c4ab20eb3f497a665dfe9f1e072c8d",
      "prompt_exact_match": true,
      "source_camera": "pan right",
      "reuse_camera": "pan right",
      "composed_prompt_sha256": "62b1bdb317375d97cbc58887663c291fa5c17db46f961209beafd18730005cea",
      "no_result_drawn_in_teaser": "An analyst holds a blank clipboard beside a closed container; no cash quantity, replenishment trip, funding-cost comparison or immediate cash recycling is shown.",
      "native_same_input_key_rehearsal": {
        "pure_local_functions_only": true,
        "input_tuple": {
          "provider": "minimax",
          "model": "image-01",
          "prompt": "Medium shot in a plain cash management office, an anonymous analyst reviewing a blank clipboard beside a single closed unmarked metal container, muted window light on the object.. Style: cute Taiwanese YouTube explainer cartoon: chibi characters with big round heads, large expressive eyes and exaggerated comic expressions, thick clean dark outlines, flat colours with soft cel shading, a limited palette of deep navy night, parchment yellow, muted teal and one warning-red accent, subtle paper grain, simple clear backgrounds, one subject in the centre third, playful and friendly, 16:9. Camera: pan right",
          "negative": "",
          "width": 1920,
          "height": 1080,
          "seed": 1,
          "references": []
        },
        "aspect": "16:9",
        "requested_size": null,
        "nominal_image_size": "1K",
        "image_selection_version": 1,
        "seed_offset": 0,
        "takes": 1,
        "correction_list": [],
        "prompt_budget_chars": 1500,
        "base_key": "b8849c7e3426afaf",
        "native_stage_key": "ae36141f34ff04cc",
        "parameters_are_declared_plan_not_backend_readback": true,
        "no_provider_call": true
      },
      "actual_source_file": null,
      "actual_source_sha256": null,
      "actual_reused_file": null,
      "actual_reused_sha256": null,
      "actual_same_asset_verified": false,
      "actual_same_file_sha_verified": false
    }
  ],
  "production_handoff": {
    "preconditions": [
      "Current exact independent source/visual and fresh-reader reviews, owner approvals, actual production admission and all-in quote are still pending. This plan executes nothing.",
      "Read actual provider/model/version/prompt limit/size/negative/references/seed/fixes before admission and recompute each native key from that readback; planned example values are not a live cache receipt.",
      "Same immutable project/workdir, exact request, default seed offset 0 and takes1 at both endpoints."
    ],
    "official_command_recipe_only": [
      {
        "purpose": "PAYOFF FIRST only after normal production admission",
        "argv": [
          "node",
          "docs/videos/brand-story-remakes-20261025/runtime-cli.mjs",
          "/workspace/work/brand-story-20261025/c19-submission-root",
          "keyframes",
          "--slug",
          "story-everyday-seven-bank-c19-remake-20261025",
          "--workdir",
          "/workspace/work/brand-story-20261025/media",
          "--shot",
          "c19r1a18",
          "--takes",
          "1"
        ]
      },
      {
        "purpose": "MANDATORY READ-ONLY LIVE CACHE GUARD BEFORE THE SECOND COMMAND",
        "required_checks": [
          "Read keyframes/manifest.json shots[c19r1a18]; require passed judge, needs_review false, seed1, one take, no fixes, key equal to live-recomputed native Stage.imageKey.",
          "Hash the actual selected file bytes; match selected.sha256. Trimmed selected file may differ from the original cache file.",
          "Read media/cache.json using readCache(workdir); require entries[live-key] exists, provider/model equal the live request, actual file exists, actual bytes SHA equal entry.sha256.",
          "Any missing/mismatching file, key, model, selection or SHA: STOP. Do not issue teaser command, clear cache, submit another purchase or hand-edit a manifest."
        ]
      },
      {
        "purpose": "TEASER only after the real cache guard succeeds; exact cache hit prevents duplicate image purchase",
        "argv": [
          "node",
          "docs/videos/brand-story-remakes-20261025/runtime-cli.mjs",
          "/workspace/work/brand-story-20261025/c19-submission-root",
          "keyframes",
          "--slug",
          "story-everyday-seven-bank-c19-remake-20261025",
          "--workdir",
          "/workspace/work/brand-story-20261025/media",
          "--shot",
          "c19r1h05",
          "--takes",
          "1"
        ]
      },
      {
        "purpose": "PAYOFF FIRST only after normal production admission",
        "argv": [
          "node",
          "docs/videos/brand-story-remakes-20261025/runtime-cli.mjs",
          "/workspace/work/brand-story-20261025/c19-submission-root",
          "keyframes",
          "--slug",
          "story-everyday-seven-bank-c19-remake-20261025",
          "--workdir",
          "/workspace/work/brand-story-20261025/media",
          "--shot",
          "c19r1n10",
          "--takes",
          "1"
        ]
      },
      {
        "purpose": "MANDATORY READ-ONLY LIVE CACHE GUARD BEFORE THE SECOND COMMAND",
        "required_checks": [
          "Read keyframes/manifest.json shots[c19r1n10]; require passed judge, needs_review false, seed1, one take, no fixes, key equal to live-recomputed native Stage.imageKey.",
          "Hash the actual selected file bytes; match selected.sha256. Trimmed selected file may differ from the original cache file.",
          "Read media/cache.json using readCache(workdir); require entries[live-key] exists, provider/model equal the live request, actual file exists, actual bytes SHA equal entry.sha256.",
          "Any missing/mismatching file, key, model, selection or SHA: STOP. Do not issue teaser command, clear cache, submit another purchase or hand-edit a manifest."
        ]
      },
      {
        "purpose": "TEASER only after the real cache guard succeeds; exact cache hit prevents duplicate image purchase",
        "argv": [
          "node",
          "docs/videos/brand-story-remakes-20261025/runtime-cli.mjs",
          "/workspace/work/brand-story-20261025/c19-submission-root",
          "keyframes",
          "--slug",
          "story-everyday-seven-bank-c19-remake-20261025",
          "--workdir",
          "/workspace/work/brand-story-20261025/media",
          "--shot",
          "c19r1h06",
          "--takes",
          "1"
        ]
      }
    ],
    "on_any_failure_or_changed_request": "Stop the pair. No separate reroll, force, accept-best bypass, independent look-alike purchase or hand-written manifest. Correct both endpoints together, repeat normal bound source/visual review and admission.",
    "actual_verification_required": [
      "Both endpoints must pass their own ordinary official judge verdict.",
      "After the official commands, read manifest shots for the pair, require identical selected file reference and SHA, then hash the actual bytes.",
      "If trimming occurs, require identical final trimmed selected file and SHA at both endpoints; matching original-generated hashes alone is insufficient.",
      "Hash original cache bytes and final selected bytes separately; do not assume original and trimmed SHA are equal.",
      "Read final assembly inputs and require the same selected file at teaser and payoff. Preserve normal job/cache/ledger receipts."
    ],
    "executed": false
  },
  "provider_calls": 0,
  "paid_calls": 0
};
plan.revision='c20-r1';plan.candidate_binding={core_four_sha256:coreHashes,claims_md_sha256:fileSha(path.join(OUT,'claims.md')),brief_sha256:fileSha(path.join(OUT,'brief.md')),series_sha256:fileSha(path.join(OUT,'series.json'))};plan.rule.sha256=fileSha(path.join(REPO,plan.rule.file));for(const f of Object.keys(plan.code_readback.files_sha256))plan.code_readback.files_sha256[f]=fileSha(path.join(REPO,f));
plan.pairs=pairDefs.map(([a,b,asset])=>{const setup=scenes.find(s=>s.id===a),payoff=scenes.find(s=>s.id===b);assert.equal(setup.data.prompt,payoff.data.prompt);assert.equal(setup.data.camera,payoff.data.camera);const prompt=shotPrompt(setup,resolveLook(doc.look),[],1500);assert.equal(prompt,shotPrompt(payoff,resolveLook(doc.look),[],1500));const tuple={provider:'minimax',model:'image-01',prompt,negative:'',width:1920,height:1080,seed:1,references:[]},opts={prompt,negative:'',references:[],seed:1,size:null},ctx={status:{image:{provider:'minimax',model:'image-01'}},format:null,imageVersion:imageSelectionVersion(series)},key=Stage.prototype.imageKey.call(ctx,opts);assert.equal(key,Stage.prototype.imageKey.call(ctx,{...opts,prompt:shotPrompt(payoff,resolveLook(doc.look),[],1500)}));return{asset_plan_id:asset,role:'PLANNED_ONE_IDENTICAL_IMAGE_NOT_AN_ACTUAL_ASSET',source_scene_id:b,source_line_id:b,reuse_scene_id:a,reuse_line_id:a,narration_setup_text:setup.lines[0].text,narration_payoff_text:payoff.lines[0].text,source_prompt_sha256:sha(payoff.data.prompt),reuse_prompt_sha256:sha(setup.data.prompt),prompt_exact_match:true,source_camera:payoff.data.camera,reuse_camera:setup.data.camera,composed_prompt_sha256:sha(prompt),no_result_drawn_in_teaser:asset==='return-address-before-sealing'?'Adult pauses over a face-down unmarked sheet before sealing; no filled address, checkbox, request or completed form is shown.':'Closed opaque mailer before opening; no pink case, contents, replacement unit, returned original, flame or successful repair is shown.',native_same_input_key_rehearsal:{pure_local_functions_only:true,input_tuple:tuple,aspect:'16:9',requested_size:null,nominal_image_size:'1K',image_selection_version:imageSelectionVersion(series),seed_offset:0,takes:1,correction_list:[],prompt_budget_chars:1500,base_key:keyframeKey(tuple),native_stage_key:key,parameters_are_declared_plan_not_backend_readback:true,no_provider_call:true},actual_source_file:null,actual_source_sha256:null,actual_reused_file:null,actual_reused_sha256:null,actual_same_asset_verified:false,actual_same_file_sha_verified:false};});
plan.production_handoff.official_command_recipe_only=plan.pairs.flatMap(p=>[{purpose:'PAYOFF FIRST only after normal production admission',argv:['node','docs/videos/brand-story-remakes-20261025/runtime-cli.mjs',RUNTIME,'keyframes','--slug',SLUG,'--workdir',MEDIA,'--shot',p.source_scene_id,'--takes','1']},{purpose:'MANDATORY READ-ONLY LIVE CACHE GUARD BEFORE TEASER',required_checks:['Read actual keyframes/manifest.json source shot '+p.source_scene_id+'; require ordinary passed judge, needs_review false, one take, seed1, no fixes and live-recomputed exact Stage.imageKey.','Hash selected bytes against selected.sha256; separately readCache(workdir) and require the live-key entry, actual file, provider/model and entry SHA all match.','Any missing or changed entry/file/key/SHA/selection: STOP without teaser command, cache clearing, another purchase, forced selection or handwritten manifest.']},{purpose:'TEASER only after real cache guard succeeds, then ordinary independent endpoint judge',argv:['node','docs/videos/brand-story-remakes-20261025/runtime-cli.mjs',RUNTIME,'keyframes','--slug',SLUG,'--workdir',MEDIA,'--shot',p.reuse_scene_id,'--takes','1']}]);write('image-reuse-plan.json',plan);
const producer=['# C20 R1 製作交接','','作者recipe，沒有provider／paid／backend／Git寫入。新project runtime '+RUNTIME+'；隔離media根 '+MEDIA+'，只建立原生不可變字典，沒有音訊或影像。video無series重綁定。','','## 正常初始化與免費預檢','','用本批prepare-runtime.mjs只選c20；新字典由shared dictionary snapshot和本集names正常初始化，不拷別集字典／approval。voice完整物件源C06，未改共享檔。原生screenplay與作者附來源稿分開。category story；13min原目標，約3500容量有風險，actual seconds null。','','## 同圖','','兩組h05→e14、h06→n01同完整prompt／camera／look／model／seed／size／version，計畫key已純本地重算。正常入場後先payoff --takes1，再讀實際manifest與readCache的真檔SHA；缺或錯即停，不能讓teaser另買一張。兩端各自judge，裁切後selected檔與真SHA仍須相同；組片前讀實際輸入。actual_same_asset_verified=false，所有實檔欄null。不得用cached()當唯讀守衛。','','## 其餘','','繁中燒錄＋CC；5秒片頭在coldopen後、21秒v4片尾在有聲CTA後。正式PR1860 branding的全域required readback由root另作，不拉production pin、不用候選冒充正式。全部媒體仍未生成。獨立來源與新讀者另派，作者不寫verify或批准。68舊檔／readonly snapshots、研究3原件、source-cache159檔SHA全部保護。',''];fs.writeFileSync(path.join(OUT,'producer.md'),producer.join('\n'));
write('protected-inputs-r1.json',{schema_version:1,role:'AUTHOR_INPUT_PROTECTION_NOT_SOURCE_QA',at_utc:new Date().toISOString(),research_three_sha256:PROTECTED,legacy_files:protectedOld,legacy_count:protectedOld.length,raw_manifest_path:rawManifestFile,raw_manifest_sha256:fileSha(rawManifestFile),raw_file_count:rawManifest.files.length,raw_all_match:true,legacy_and_snapshots_all_match:true});
write('author-notes.json',{schema_version:1,status:'HOLD_PENDING_INDEPENDENT_SOURCE_VISUAL_AND_FRESH_READERS',candidate_revision:'c20-r1',author:'/root/c20_primary_research',counts:{lines:rows.length,scenes:scenes.length,shots:scenes.filter(s=>s.template==='shot').length,cards:0,outro:1,chapters:6,loops:loops.length},native_units:{whole_narration_spoken_units:whole,coldopen:opening,voiced_CTA:cta,rough_planning_target:3500,delta_to_rough_target:whole-3500,actual_narration_seconds:null,actual_final_seconds:null,actual_duration_verified:false,planning_arithmetic_at_4_to_5_units_per_second:[whole/5,whole/4],planning_is_not_actual_time:true,official_duration_scope:'Whole unwrapped narration including coldopen and voiced CTA; only separately added channel bookends excluded.',capacity_status:'MATERIAL_CAPACITY_RISK_NOT_13MIN_READY'},voice_source:{path:voicePath,file_sha256:fileSha(voicePath),voice_object_sha256:sha(JSON.stringify(voice)),exact_copy:true,other_episode_dictionary_copied:false},source_research_sha256:PROTECTED,protected_old_file_count:68,raw_preserved_file_count:rawManifest.files.length,protected_old_and_snapshot_unchanged:true,source_pass_claimed:false,narrative_pass_claimed:false,owner_approval_created:false,actual_media_generated:false,actual_same_image_verified:false,provider_calls:0,paid_calls:0,backend_mutations:0,git_mutations:0,runtime_root:RUNTIME,media_base:MEDIA,image_reuse_plan_sha256:fileSha(path.join(OUT,'image-reuse-plan.json')),independent_source_review:'PENDING_OTHER_REVIEWER',independent_narrative_review:'PENDING_FRESH_READERS'});
console.log(JSON.stringify({core_four_sha256:coreHashes,whole_units:whole,coldopen:opening,CTA:cta,lines:rows.length,scenes:scenes.length,shots:scenes.filter(s=>s.template==='shot').length,reuse_plan_sha256:fileSha(path.join(OUT,'image-reuse-plan.json'))},null,2));
