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
const SLUG='story-everyday-zippo-c20-remake-20261025',RUNTIME='/workspace/work/brand-story-20261025/c20-audit/author-r8/runtime',AUDIT='/workspace/work/brand-story-20261025/c20-audit',MEDIA=path.join(AUDIT,'author-r8/media');
const sha=x=>createHash('sha256').update(x).digest('hex'),fileSha=p=>sha(fs.readFileSync(p)),read=p=>JSON.parse(fs.readFileSync(p,'utf8')),write=(p,x)=>fs.writeFileSync(path.join(OUT,p),JSON.stringify(x,null,2)+'\n');
const PROTECTED={'research-original.md':'bd325631384e70272d074326b8b0bc5fa10c01adc2210276fe591a3a54765be2','research-original.claims.json':'4763b1808d0ad7d21a42256f7584c3c78352bb33eb10f91027c9aa6be7a8517c','original-preservation.json':'4932a5ed91683a1dc56b717fb292ca1d74ed61d13b7c40064bb0a029e0cb96bf'};
for(const[f,h]of Object.entries(PROTECTED))assert.equal(fileSha(path.join(OUT,f)),h,'protected research '+f);
const research=read(path.join(OUT,'research-original.claims.json')),pres=read(path.join(OUT,'original-preservation.json'));
const supplement={
  "schema_version": 1,
  "revision": "c20-r3",
  "role": "AUTHOR_REOPENED_PRIMARY_ANCHORS_NOT_SOURCE_REVIEW",
  "at_utc": "2026-10-26T04:20:28.342819+00:00",
  "original_research_three_unchanged": true,
  "original_raw159_unchanged": true,
  "new_raw_downloads": 0,
  "claims": [
    {
      "id": "E01",
      "scope_zh": "帶環舊物為一次深夜或清早拍賣標得；表面有船圖、盾與刻字，仍有不少顏色。",
      "evidence": {
        "source_id": "DF_CASE",
        "raw_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.html",
        "raw_sha256": "6f623a6bbcb0c94cafa9fac32c7992cd5224ae78fd9885b3403e4ea57a18ebac",
        "quote": "one of those late night or early morning Ebay bids",
        "locator": {
          "text_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.txt",
          "text_sha256": "6ac84a07c099b3f5ede3b11718a6070f23edc23a0cbcf37bf68991e0e5844cd5",
          "start_line": 26,
          "end_line": 26,
          "normalized_whitespace": true,
          "normalized_text_character_offset": 878
        }
      },
      "source_class": "named first-person customer report",
      "applicable_region": "United States, historical reported experience",
      "publisher_date": "published 2022-04-06; modified 2022-04-08",
      "event_date_or_period": "March–April 2022 repairs",
      "allowed_attribution": "作者喬瑟夫的2022親歷自述；不是廠內連續工序或獨立實測。",
      "forbidden_inferences_zh": "不補拍賣日期、金額、船員身分、戰場經歷或收藏價值。",
      "status": "AUTHOR_ADDITIONAL_PRIMARY_ANCHOR_PENDING_INDEPENDENT_QA"
    },
    {
      "id": "E02",
      "scope_zh": "作者說鉸鏈鬆、蓋子晃，擔心照用途攜帶會增損甚至遺失部分。",
      "evidence": {
        "source_id": "DF_CASE",
        "raw_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.html",
        "raw_sha256": "6f623a6bbcb0c94cafa9fac32c7992cd5224ae78fd9885b3403e4ea57a18ebac",
        "quote": "the way the lid flopped around",
        "locator": {
          "text_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.txt",
          "text_sha256": "6ac84a07c099b3f5ede3b11718a6070f23edc23a0cbcf37bf68991e0e5844cd5",
          "start_line": 27,
          "end_line": 27,
          "normalized_whitespace": true,
          "normalized_text_character_offset": 1326
        }
      },
      "source_class": "named first-person customer report",
      "applicable_region": "United States, historical reported experience",
      "publisher_date": "published 2022-04-06; modified 2022-04-08",
      "event_date_or_period": "March–April 2022 repairs",
      "allowed_attribution": "作者喬瑟夫的2022親歷自述；不是廠內連續工序或獨立實測。",
      "forbidden_inferences_zh": "屬作者顧慮，沒有實際遺失；不能推原先無法點火。",
      "status": "AUTHOR_ADDITIONAL_PRIMARY_ANCHOR_PENDING_INDEPENDENT_QA"
    },
    {
      "id": "E03",
      "scope_zh": "作者之前未送修，說自己看過的舊修件鉸鏈歪、痕跡難看；這是他的顧慮。",
      "evidence": {
        "source_id": "DF_CASE",
        "raw_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.html",
        "raw_sha256": "6f623a6bbcb0c94cafa9fac32c7992cd5224ae78fd9885b3403e4ea57a18ebac",
        "quote": "I had a negative opinion",
        "locator": {
          "text_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.txt",
          "text_sha256": "6ac84a07c099b3f5ede3b11718a6070f23edc23a0cbcf37bf68991e0e5844cd5",
          "start_line": 28,
          "end_line": 28,
          "normalized_whitespace": true,
          "normalized_text_character_offset": 1775
        }
      },
      "source_class": "named first-person customer report",
      "applicable_region": "United States, historical reported experience",
      "publisher_date": "published 2022-04-06; modified 2022-04-08",
      "event_date_or_period": "March–April 2022 repairs",
      "allowed_attribution": "作者喬瑟夫的2022親歷自述；不是廠內連續工序或獨立實測。",
      "forbidden_inferences_zh": "不是全部repair clinic工藝結論，不編無出處心理或廠內操作。",
      "status": "AUTHOR_ADDITIONAL_PRIMARY_ANCHOR_PENDING_INDEPENDENT_QA"
    },
    {
      "id": "E04",
      "scope_zh": "作者在社群放待修舊物圖片想交換，別人問為何不寄回修；按其回顧歸屬。",
      "evidence": {
        "source_id": "DF_CASE",
        "raw_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.html",
        "raw_sha256": "6f623a6bbcb0c94cafa9fac32c7992cd5224ae78fd9885b3403e4ea57a18ebac",
        "quote": "I was interested in trading",
        "locator": {
          "text_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.txt",
          "text_sha256": "6ac84a07c099b3f5ede3b11718a6070f23edc23a0cbcf37bf68991e0e5844cd5",
          "start_line": 28,
          "end_line": 28,
          "normalized_whitespace": true,
          "normalized_text_character_offset": 1571
        }
      },
      "source_class": "named first-person customer report",
      "applicable_region": "United States, historical reported experience",
      "publisher_date": "published 2022-04-06; modified 2022-04-08",
      "event_date_or_period": "March–April 2022 repairs",
      "allowed_attribution": "作者喬瑟夫的2022親歷自述；不是廠內連續工序或獨立實測。",
      "forbidden_inferences_zh": "沒有原社群截圖，不能逐字重演對話、身份或斷言這是唯一原因。",
      "status": "AUTHOR_ADDITIONAL_PRIMARY_ANCHOR_PENDING_INDEPENDENT_QA"
    },
    {
      "id": "E05",
      "scope_zh": "作者先email詢問特殊款能否修回原樣，等不到回信就決定寄；原文自述不耐。",
      "evidence": {
        "source_id": "DF_CASE",
        "raw_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.html",
        "raw_sha256": "6f623a6bbcb0c94cafa9fac32c7992cd5224ae78fd9885b3403e4ea57a18ebac",
        "quote": "I got bored of waiting for a response",
        "locator": {
          "text_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.txt",
          "text_sha256": "6ac84a07c099b3f5ede3b11718a6070f23edc23a0cbcf37bf68991e0e5844cd5",
          "start_line": 50,
          "end_line": 50,
          "normalized_whitespace": true,
          "normalized_text_character_offset": 7186
        }
      },
      "source_class": "named first-person customer report",
      "applicable_region": "United States, historical reported experience",
      "publisher_date": "published 2022-04-06; modified 2022-04-08",
      "event_date_or_period": "March–April 2022 repairs",
      "allowed_attribution": "作者喬瑟夫的2022親歷自述；不是廠內連續工序或獨立實測。",
      "forbidden_inferences_zh": "不編精確等了幾天、廠方故意拖延或此前已承諾特殊修法。",
      "status": "AUTHOR_ADDITIONAL_PRIMARY_ANCHOR_PENDING_INDEPENDENT_QA"
    },
    {
      "id": "E06",
      "scope_zh": "作者同次寄兩只；另篇記收件email說收到兩只。",
      "evidence": {
        "source_id": "DF_PRE_REPAIR",
        "raw_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_PRE_REPAIR.html",
        "raw_sha256": "59d3ffe8516ba1ff468c507718dbc4dde04a2f3d307dc9cf384e9ae71dcbd722",
        "quote": "received two lighters for repair",
        "locator": {
          "text_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_PRE_REPAIR.decoded.txt",
          "text_sha256": "61de0bee875121a7ef95cca07a7371e2d571c38a981fa43e0362d07e66d34eda",
          "start_line": 32,
          "end_line": 32,
          "normalized_whitespace": true,
          "normalized_text_character_offset": 2652
        }
      },
      "source_class": "same first-person author follow-up chronology",
      "applicable_region": "United States, historical reported experience",
      "publisher_date": "published 2022-04-04; modified 2022-04-05",
      "event_date_or_period": "March 2022 dispatch/receipt/return notice",
      "allowed_attribution": "作者喬瑟夫的2022親歷自述；不是廠內連續工序或獨立實測。",
      "forbidden_inferences_zh": "兩只是同一Joe包裹，不是JP粉紅case；不要把另外一只普通款的修法移到帶環款。",
      "status": "AUTHOR_ADDITIONAL_PRIMARY_ANCHOR_PENDING_INDEPENDENT_QA"
    },
    {
      "id": "E07",
      "scope_zh": "作者說當時表建議堅固盒或緩衝袋、1–2只一包，自己仔細保護後照表地址寄出。",
      "evidence": {
        "source_id": "DF_CASE",
        "raw_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.html",
        "raw_sha256": "6f623a6bbcb0c94cafa9fac32c7992cd5224ae78fd9885b3403e4ea57a18ebac",
        "quote": "sturdy box or padded mailer",
        "locator": {
          "text_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.txt",
          "text_sha256": "6ac84a07c099b3f5ede3b11718a6070f23edc23a0cbcf37bf68991e0e5844cd5",
          "start_line": 34,
          "end_line": 34,
          "normalized_whitespace": true,
          "normalized_text_character_offset": 2876
        }
      },
      "source_class": "named first-person customer report",
      "applicable_region": "United States, historical reported experience",
      "publisher_date": "published 2022-04-06; modified 2022-04-08",
      "event_date_or_period": "March–April 2022 repairs",
      "allowed_attribution": "作者喬瑟夫的2022親歷自述；不是廠內連續工序或獨立實測。",
      "forbidden_inferences_zh": "是作者轉述當時原表，非本次取得的2022官方PDF或當今全球寄件指示。",
      "status": "AUTHOR_ADDITIONAL_PRIMARY_ANCHOR_PENDING_INDEPENDENT_QA"
    },
    {
      "id": "E08",
      "scope_zh": "作者說有收藏者記得不同地址，他照表寄，回件時看到PO Box回郵地址。",
      "evidence": {
        "source_id": "DF_CASE",
        "raw_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.html",
        "raw_sha256": "6f623a6bbcb0c94cafa9fac32c7992cd5224ae78fd9885b3403e4ea57a18ebac",
        "quote": "the address provided worked fine",
        "locator": {
          "text_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.txt",
          "text_sha256": "6ac84a07c099b3f5ede3b11718a6070f23edc23a0cbcf37bf68991e0e5844cd5",
          "start_line": 35,
          "end_line": 35,
          "normalized_whitespace": true,
          "normalized_text_character_offset": 3431
        }
      },
      "source_class": "named first-person customer report",
      "applicable_region": "United States, historical reported experience",
      "publisher_date": "published 2022-04-06; modified 2022-04-08",
      "event_date_or_period": "March–April 2022 repairs",
      "allowed_attribution": "作者喬瑟夫的2022親歷自述；不是廠內連續工序或獨立實測。",
      "forbidden_inferences_zh": "不把當時地址或PO Box推現行寄送地；不加收件追蹤號。",
      "status": "AUTHOR_ADDITIONAL_PRIMARY_ANCHOR_PENDING_INDEPENDENT_QA"
    },
    {
      "id": "E09",
      "scope_zh": "作者記2022三月首週寄、十八日收件通知、二十九日出件通知。",
      "evidence": {
        "source_id": "DF_PRE_REPAIR",
        "raw_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_PRE_REPAIR.html",
        "raw_sha256": "59d3ffe8516ba1ff468c507718dbc4dde04a2f3d307dc9cf384e9ae71dcbd722",
        "quote": "March 29",
        "locator": {
          "text_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_PRE_REPAIR.decoded.txt",
          "text_sha256": "61de0bee875121a7ef95cca07a7371e2d571c38a981fa43e0362d07e66d34eda",
          "start_line": 32,
          "end_line": 32,
          "normalized_whitespace": true,
          "normalized_text_character_offset": 2728
        }
      },
      "source_class": "same first-person author follow-up chronology",
      "applicable_region": "United States, historical reported experience",
      "publisher_date": "published 2022-04-04; modified 2022-04-05",
      "event_date_or_period": "March 2022 dispatch/receipt/return notice",
      "allowed_attribution": "作者喬瑟夫的2022親歷自述；不是廠內連續工序或獨立實測。",
      "forbidden_inferences_zh": "本人對email的描述，未取得email原件；不是JP2024日期或實修工時。",
      "status": "AUTHOR_ADDITIONAL_PRIMARY_ANCHOR_PENDING_INDEPENDENT_QA"
    },
    {
      "id": "E10",
      "scope_zh": "較早詢問的答覆在出件通知之後到，內容泛稱能修，沒有具體說帶環鉸鏈。",
      "evidence": {
        "source_id": "DF_PRE_REPAIR",
        "raw_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_PRE_REPAIR.html",
        "raw_sha256": "59d3ffe8516ba1ff468c507718dbc4dde04a2f3d307dc9cf384e9ae71dcbd722",
        "quote": "it never mentioned the lossproof hinge specifically",
        "locator": {
          "text_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_PRE_REPAIR.decoded.txt",
          "text_sha256": "61de0bee875121a7ef95cca07a7371e2d571c38a981fa43e0362d07e66d34eda",
          "start_line": 33,
          "end_line": 33,
          "normalized_whitespace": true,
          "normalized_text_character_offset": 3040
        }
      },
      "source_class": "same first-person author follow-up chronology",
      "applicable_region": "United States, historical reported experience",
      "publisher_date": "published 2022-04-04; modified 2022-04-05",
      "event_date_or_period": "March 2022 dispatch/receipt/return notice",
      "allowed_attribution": "作者喬瑟夫的2022親歷自述；不是廠內連續工序或獨立實測。",
      "forbidden_inferences_zh": "不能斷言廠方保證精確特殊修法，不能編實際對話或回信文字。",
      "status": "AUTHOR_ADDITIONAL_PRIMARY_ANCHOR_PENDING_INDEPENDENT_QA"
    },
    {
      "id": "E11",
      "scope_zh": "Camden款補繩、鉸鏈緊，看來換彎成環的pin，作者看不見新焊痕。",
      "evidence": {
        "source_id": "DF_CASE",
        "raw_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.html",
        "raw_sha256": "6f623a6bbcb0c94cafa9fac32c7992cd5224ae78fd9885b3403e4ea57a18ebac",
        "quote": "There are no new weld marks or scars",
        "locator": {
          "text_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.txt",
          "text_sha256": "6ac84a07c099b3f5ede3b11718a6070f23edc23a0cbcf37bf68991e0e5844cd5",
          "start_line": 43,
          "end_line": 43,
          "normalized_whitespace": true,
          "normalized_text_character_offset": 5539
        }
      },
      "source_class": "named first-person customer report",
      "applicable_region": "United States, historical reported experience",
      "publisher_date": "published 2022-04-06; modified 2022-04-08",
      "event_date_or_period": "March–April 2022 repairs",
      "allowed_attribution": "作者喬瑟夫的2022親歷自述；不是廠內連續工序或獨立實測。",
      "forbidden_inferences_zh": "保留appears；不畫新焊接、不把另外普通款換hinge結果套此款，不補點火成功。",
      "status": "AUTHOR_ADDITIONAL_PRIMARY_ANCHOR_PENDING_INDEPENDENT_QA"
    },
    {
      "id": "E12",
      "scope_zh": "作者對回程兩只同放緩衝袋有顧慮，但明說到貨完好；擔心原有顏色。",
      "evidence": {
        "source_id": "DF_CASE",
        "raw_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.html",
        "raw_sha256": "6f623a6bbcb0c94cafa9fac32c7992cd5224ae78fd9885b3403e4ea57a18ebac",
        "quote": "the lighters arrived fine",
        "locator": {
          "text_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.txt",
          "text_sha256": "6ac84a07c099b3f5ede3b11718a6070f23edc23a0cbcf37bf68991e0e5844cd5",
          "start_line": 48,
          "end_line": 48,
          "normalized_whitespace": true,
          "normalized_text_character_offset": 6369
        }
      },
      "source_class": "named first-person customer report",
      "applicable_region": "United States, historical reported experience",
      "publisher_date": "published 2022-04-06; modified 2022-04-08",
      "event_date_or_period": "March–April 2022 repairs",
      "allowed_attribution": "作者喬瑟夫的2022親歷自述；不是廠內連續工序或獨立實測。",
      "forbidden_inferences_zh": "不指控這次新增碰損／掉漆，不把作者品牌負評當普遍事實。",
      "status": "AUTHOR_ADDITIONAL_PRIMARY_ANCHOR_PENDING_INDEPENDENT_QA"
    },
    {
      "id": "E13",
      "scope_zh": "作者表示未來分開一只一包寄，以保護finish。",
      "evidence": {
        "source_id": "DF_CASE",
        "raw_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.html",
        "raw_sha256": "6f623a6bbcb0c94cafa9fac32c7992cd5224ae78fd9885b3403e4ea57a18ebac",
        "quote": "I will only send lighters in individually in the future",
        "locator": {
          "text_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.txt",
          "text_sha256": "6ac84a07c099b3f5ede3b11718a6070f23edc23a0cbcf37bf68991e0e5844cd5",
          "start_line": 49,
          "end_line": 49,
          "normalized_whitespace": true,
          "normalized_text_character_offset": 6875
        }
      },
      "source_class": "named first-person customer report",
      "applicable_region": "United States, historical reported experience",
      "publisher_date": "published 2022-04-06; modified 2022-04-08",
      "event_date_or_period": "March–April 2022 repairs",
      "allowed_attribution": "作者喬瑟夫的2022親歷自述；不是廠內連續工序或獨立實測。",
      "forbidden_inferences_zh": "這是未來意向，不是已發生的第二次寄件或廠商全球新規則。",
      "status": "AUTHOR_ADDITIONAL_PRIMARY_ANCHOR_PENDING_INDEPENDENT_QA"
    },
    {
      "id": "E14",
      "scope_zh": "同包另一普通鍍鉻舊物，作者要求接蓋、裝新內膽。",
      "evidence": {
        "source_id": "DF_CASE",
        "raw_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.html",
        "raw_sha256": "6f623a6bbcb0c94cafa9fac32c7992cd5224ae78fd9885b3403e4ea57a18ebac",
        "quote": "I requested the lid be re-attached and a new insert installed",
        "locator": {
          "text_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.txt",
          "text_sha256": "6ac84a07c099b3f5ede3b11718a6070f23edc23a0cbcf37bf68991e0e5844cd5",
          "start_line": 38,
          "end_line": 38,
          "normalized_whitespace": true,
          "normalized_text_character_offset": 4106
        }
      },
      "source_class": "named first-person customer report",
      "applicable_region": "United States, historical reported experience",
      "publisher_date": "published 2022-04-06; modified 2022-04-08",
      "event_date_or_period": "March–April 2022 repairs",
      "allowed_attribution": "作者喬瑟夫的2022親歷自述；不是廠內連續工序或獨立實測。",
      "forbidden_inferences_zh": "這是請求，不把新內膽確已安裝寫成結果；不移到帶環Camden或日本粉紅款。",
      "status": "AUTHOR_ADDITIONAL_PRIMARY_ANCHOR_PENDING_INDEPENDENT_QA"
    },
    {
      "id": "E15",
      "scope_zh": "作者說想試保證近一年；知有承諾與實際寄件之間有遲疑。",
      "evidence": {
        "source_id": "DF_CASE",
        "raw_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.html",
        "raw_sha256": "6f623a6bbcb0c94cafa9fac32c7992cd5224ae78fd9885b3403e4ea57a18ebac",
        "quote": "I had been eager for almost a yr now",
        "locator": {
          "text_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.txt",
          "text_sha256": "6ac84a07c099b3f5ede3b11718a6070f23edc23a0cbcf37bf68991e0e5844cd5",
          "start_line": 27,
          "end_line": 27,
          "normalized_whitespace": true,
          "normalized_text_character_offset": 1389
        }
      },
      "source_class": "named first-person customer report",
      "applicable_region": "United States, historical reported experience",
      "publisher_date": "published 2022-04-06; modified 2022-04-08",
      "event_date_or_period": "March–April 2022 repairs",
      "allowed_attribution": "作者喬瑟夫的2022親歷自述；不是廠內連續工序或獨立實測。",
      "forbidden_inferences_zh": "不自行倒算第一次知道保證日，不把其個人顧慮當創辦人心理。",
      "status": "AUTHOR_ADDITIONAL_PRIMARY_ANCHOR_PENDING_INDEPENDENT_QA"
    },
    {
      "id": "E16",
      "scope_zh": "原照片左方帶船圖刻字那只後的表格，Hinge pin欄可見勾選。",
      "evidence": {
        "source_id": "DF_FORM_PHOTO",
        "raw_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_ORIGINAL_PHOTO.html",
        "raw_sha256": "5d7c44365f958fafe241ebe05d4adb8c47531dacc5ad83b018730ec9ceab03e7",
        "quote": "Hinge pin",
        "locator": {
          "kind": "human visual reread",
          "position": "left-hand form behind the vessel-decorated engraved case; Hinge pin checkbox tick; Will not light/work unchecked"
        }
      },
      "source_class": "author photograph",
      "applicable_region": "United States",
      "publisher_date": "linked in 2022-04-06 article",
      "event_date_or_period": "2022 dispatch photograph",
      "allowed_attribution": "作者喬瑟夫的2022親歷自述；不是廠內連續工序或獨立實測。",
      "forbidden_inferences_zh": "只讀可見欄，不推全部遮住的手寫內容，不能稱Will not light/work被勾或已進廠診斷。",
      "status": "AUTHOR_ADDITIONAL_PRIMARY_ANCHOR_PENDING_INDEPENDENT_QA"
    },
    {
      "id": "E17",
      "scope_zh": "同包另一普通款作者說換上的hinge接得乾淨，觀感如新產品接點，磨痕仍在。",
      "evidence": {
        "source_id": "DF_CASE",
        "raw_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.html",
        "raw_sha256": "6f623a6bbcb0c94cafa9fac32c7992cd5224ae78fd9885b3403e4ea57a18ebac",
        "quote": "how cleanly the replacement hinge was attached",
        "locator": {
          "text_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.txt",
          "text_sha256": "6ac84a07c099b3f5ede3b11718a6070f23edc23a0cbcf37bf68991e0e5844cd5",
          "start_line": 42,
          "end_line": 42,
          "normalized_whitespace": true,
          "normalized_text_character_offset": 4939
        }
      },
      "source_class": "named first-person customer report",
      "applicable_region": "United States, historical reported experience",
      "publisher_date": "published 2022-04-06; modified 2022-04-08",
      "event_date_or_period": "March–April 2022 repairs",
      "allowed_attribution": "作者喬瑟夫的2022親歷自述；不是廠內連續工序或獨立實測。",
      "forbidden_inferences_zh": "僅使用者觀察；不描繪實際新焊接工序、不等於獨立強度試驗，也不證new insert請求已實現。",
      "status": "AUTHOR_ADDITIONAL_PRIMARY_ANCHOR_PENDING_INDEPENDENT_QA"
    },
    {
      "id": "E18",
      "scope_zh": "作者說用產品結構圖查故障部位名字，列於連結。",
      "evidence": {
        "source_id": "JP_NOTE",
        "raw_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/patent-subtask/repair-case/snow-dolphin-jp.html",
        "raw_sha256": "11820f397cc4b37b30d763b862704668a26ae9aac7cc5963da202c7215c09ca4",
        "quote": "故障個所の名称を調べるときに使いました",
        "locator": {
          "text_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/patent-subtask/repair-case/snow-dolphin-jp.txt",
          "text_sha256": "7f6c3b6c3d982dd06fa42552cf9ecb042b745c63a393ae7bbe75370a53857828",
          "start_line": 70,
          "end_line": 70,
          "normalized_whitespace": true,
          "normalized_text_character_offset": 1754
        }
      },
      "source_class": "first-person contemporary account with author photographs",
      "applicable_region": "Japan; author says Tokyo–Osaka",
      "publisher_date": "2024-10-18 23:51 (page display; timezone not independently established)",
      "event_date_or_period": "2024-09-01 to 2024-10-18",
      "allowed_attribution": "日本作者2024親歷與說明；不當現行官方原條款。",
      "forbidden_inferences_zh": "只證作者用過／連結，未取得當時官方圖原件，不畫全型號BOM、不當實修成功。",
      "status": "AUTHOR_ADDITIONAL_PRIMARY_ANCHOR_PENDING_INDEPENDENT_QA"
    },
    {
      "id": "E19",
      "scope_zh": "作者說郵件袋本身也回來，並說寄的物件都回來；原圖說緩衝材、膠帶、新舊內膽。",
      "evidence": {
        "source_id": "JP_NOTE",
        "raw_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/patent-subtask/repair-case/snow-dolphin-jp.html",
        "raw_sha256": "11820f397cc4b37b30d763b862704668a26ae9aac7cc5963da202c7215c09ca4",
        "quote": "レターパックごと戻ってきた",
        "locator": {
          "text_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/patent-subtask/repair-case/snow-dolphin-jp.txt",
          "text_sha256": "7f6c3b6c3d982dd06fa42552cf9ecb042b745c63a393ae7bbe75370a53857828",
          "start_line": 63,
          "end_line": 63,
          "normalized_whitespace": true,
          "normalized_text_character_offset": 1640
        }
      },
      "source_class": "first-person contemporary account with author photographs",
      "applicable_region": "Japan; author says Tokyo–Osaka",
      "publisher_date": "2024-10-18 23:51 (page display; timezone not independently established)",
      "event_date_or_period": "2024-09-01 to 2024-10-18",
      "allowed_attribution": "日本作者2024親歷與說明；不當現行官方原條款。",
      "forbidden_inferences_zh": "只限此次本人敘述，不保證全球退原包材或原件，不據此聲稱carrier空運規定。",
      "status": "AUTHOR_ADDITIONAL_PRIMARY_ANCHOR_PENDING_INDEPENDENT_QA"
    },
    {
      "id": "E20",
      "scope_zh": "另一普通款來自一小批舊物，Joseph記不清取得細節；僅本人回顧。",
      "evidence": {
        "source_id": "DF_CASE",
        "raw_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.html",
        "raw_sha256": "6f623a6bbcb0c94cafa9fac32c7992cd5224ae78fd9885b3403e4ea57a18ebac",
        "quote": "I don’t even remember how I acquired it other than it was in a small lot.",
        "locator": {
          "text_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.txt",
          "text_sha256": "6ac84a07c099b3f5ede3b11718a6070f23edc23a0cbcf37bf68991e0e5844cd5",
          "start_line": 31,
          "end_line": 31,
          "normalized_whitespace": true,
          "normalized_text_character_offset": 2117
        }
      },
      "source_class": "named first-person customer report",
      "applicable_region": "United States, historical reported experience",
      "publisher_date": "published 2022-04-06; modified 2022-04-08",
      "event_date_or_period": "March–April 2022",
      "allowed_attribution": "作者歷史親歷自述/備忘錄，非連續工序或獨立性能試驗。",
      "forbidden_inferences_zh": "不補拍賣價格、日期、來源人物；不要把其來歷移到帶環款。",
      "status": "AUTHOR_ADDITIONAL_PRIMARY_ANCHOR_PENDING_INDEPENDENT_QA"
    },
    {
      "id": "E21",
      "scope_zh": "Joseph不指望普通款外觀吸睛，仍希望繼續用；與帶環款在意塗裝是不同的要求。",
      "evidence": {
        "source_id": "DF_CASE",
        "raw_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.html",
        "raw_sha256": "6f623a6bbcb0c94cafa9fac32c7992cd5224ae78fd9885b3403e4ea57a18ebac",
        "quote": "wasn’t ever really going to catch anyone’s attention for its aesthetic beauty but I had great hope for its continued usefulness.",
        "locator": {
          "text_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/DF_CASE.txt",
          "text_sha256": "6ac84a07c099b3f5ede3b11718a6070f23edc23a0cbcf37bf68991e0e5844cd5",
          "start_line": 38,
          "end_line": 38,
          "normalized_whitespace": true,
          "normalized_text_character_offset": 3977
        }
      },
      "source_class": "named first-person customer report",
      "applicable_region": "United States, historical reported experience",
      "publisher_date": "published 2022-04-06; modified 2022-04-08",
      "event_date_or_period": "March–April 2022",
      "allowed_attribution": "作者歷史親歷自述/備忘錄，非連續工序或獨立性能試驗。",
      "forbidden_inferences_zh": "是送修前的希望，不證要求的新內膽已裝上或完成點火測試。",
      "status": "AUTHOR_ADDITIONAL_PRIMARY_ANCHOR_PENDING_INDEPENDENT_QA"
    },
    {
      "id": "E22",
      "scope_zh": "日本作者備忘錄列本體、內膽、修理表為一併送出的內容，不是單寄裂掉彈簧。",
      "evidence": {
        "source_id": "JP_NOTE",
        "raw_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/patent-subtask/repair-case/snow-dolphin-jp.html",
        "raw_sha256": "11820f397cc4b37b30d763b862704668a26ae9aac7cc5963da202c7215c09ca4",
        "quote": "本体-インサイド・ユニット-修理シートをレターパックに入れたら封をして送る",
        "locator": {
          "text_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/patent-subtask/repair-case/snow-dolphin-jp.txt",
          "text_sha256": "7f6c3b6c3d982dd06fa42552cf9ecb042b745c63a393ae7bbe75370a53857828",
          "start_line": 61,
          "end_line": 61,
          "normalized_whitespace": true,
          "normalized_text_character_offset": 1540
        }
      },
      "source_class": "first-person contemporary account with author photographs",
      "applicable_region": "Japan; author says Tokyo–Osaka",
      "publisher_date": "2024-10-18 23:51 (page display; timezone not independently established)",
      "event_date_or_period": "2024-09-01 to 2024-10-18",
      "allowed_attribution": "作者歷史親歷自述/備忘錄，非連續工序或獨立性能試驗。",
      "forbidden_inferences_zh": "只歸屬其歷史備忘錄，不證填妥表內容/勾選/退舊要求，非當今全球寄件教程。",
      "status": "AUTHOR_ADDITIONAL_PRIMARY_ANCHOR_PENDING_INDEPENDENT_QA"
    },
    {
      "id": "E23",
      "scope_zh": "日本作者說將已分離的殼與內膽裝在同一夾鏈袋，避免在郵件袋內晃動；非教學步驟。",
      "evidence": {
        "source_id": "JP_NOTE",
        "raw_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/patent-subtask/repair-case/snow-dolphin-jp.html",
        "raw_sha256": "11820f397cc4b37b30d763b862704668a26ae9aac7cc5963da202c7215c09ca4",
        "quote": "分離してポリ袋にまとめて入れた",
        "locator": {
          "text_path": "/workspace/work/brand-story-20261025/c20-audit/source-cache/patent-subtask/repair-case/snow-dolphin-jp.txt",
          "text_sha256": "7f6c3b6c3d982dd06fa42552cf9ecb042b745c63a393ae7bbe75370a53857828",
          "start_line": 47,
          "end_line": 47,
          "normalized_whitespace": true,
          "normalized_text_character_offset": 1161
        }
      },
      "source_class": "first-person contemporary account with author photographs",
      "applicable_region": "Japan, 2024 author account",
      "publisher_date": "2024-10-18 23:51 (page display; timezone not independently established)",
      "event_date_or_period": "2024-09-01 shipment",
      "allowed_attribution": "只歸屬作者這次包裹的親歷自述，不是當今官方寄件指示。",
      "forbidden_inferences_zh": "不補已填表內容/工廠開包流程/成功測試，不當全球寄件教學。",
      "status": "AUTHOR_ADDITIONAL_PRIMARY_ANCHOR_PENDING_INDEPENDENT_QA"
    }
  ],
  "r2_claims_inherited_with_original_evidence": 19
};research.claims.push(...supplement.claims);
const archivedR7=read(path.join(OUT,'history/r7/archive-manifest.json'));for(const f of archivedR7.files)assert.equal(fileSha(path.join(OUT,'history/r7',f.path)),f.sha256,'R7 archive '+f.path);
const archivedR6=read(path.join(OUT,'history/r6/archive-manifest.json'));for(const f of archivedR6.files)assert.equal(fileSha(path.join(OUT,'history/r6',f.path)),f.sha256,'R6 archive '+f.path);
const archivedR5=read(path.join(OUT,'history/r5/archive-manifest.json'));for(const f of archivedR5.files)assert.equal(fileSha(path.join(OUT,'history/r5',f.path)),f.sha256,'R5 archive '+f.path);
const archivedR4=read(path.join(OUT,'history/r4/archive-manifest.json'));for(const f of archivedR4.files)assert.equal(fileSha(path.join(OUT,'history/r4',f.path)),f.sha256,'R4 archive '+f.path);
const archivedR3=read(path.join(OUT,'history/r3/archive-manifest.json'));for(const f of archivedR3.files)assert.equal(fileSha(path.join(OUT,'history/r3',f.path)),f.sha256,'R3 archive '+f.path);
const archivedR2=read(path.join(OUT,'history/r2/archive-manifest.json'));for(const f of archivedR2.files)assert.equal(fileSha(path.join(OUT,'history/r2',f.path)),f.sha256,'R2 archive '+f.path);
const archivedR1=read(path.join(OUT,'history/r1/review-state.json'));for(const f of archivedR1.files)assert.equal(fileSha(path.join(OUT,'history/r1',f.path)),f.sha256,'R1 archive '+f.path);
const protectedOld=[];for(const section of[pres,pres.additional_related_legacy_tree])for(const f of section.files){const source=path.join(section.source_root,f.path),snapshot=path.join(section.external_readonly_snapshot??section.snapshot_root,f.path);assert.equal(fileSha(source),f.sha256,source);assert.equal(fileSha(snapshot),f.sha256,snapshot);protectedOld.push({source,snapshot,sha256:f.sha256});}assert.equal(protectedOld.length,68);
const rawManifestFile=path.join(AUDIT,'source-cache-manifest.json'),rawManifest=read(rawManifestFile);for(const f of rawManifest.files)assert.equal(fileSha(path.join(rawManifest.cache_root,f.relative_path)),f.sha256,'raw '+f.relative_path);
const voicePath=path.join(REPO,'docs/videos/brand-story-remakes-20261025/c06/video.json'),voice=structuredClone(read(voicePath).voice);
const rows=[
  {
    "id": "c20r3h01",
    "chapter": "帶繫繩環的舊盒，準備寄回去",
    "text": "你若像這位收藏者，一次寄修兩只舊物，想留的痕跡，會被免費修掉嗎？",
    "research_claim_refs": [
      "E06",
      "D05",
      "O09"
    ],
    "claim_class": "viewer_question",
    "visual": "twocases"
  },
  {
    "id": "c20r3h02",
    "chapter": "帶繫繩環的舊盒，準備寄回去",
    "text": "二〇二二年，美國，收藏者喬瑟夫準備寄出一只舊 Zippo。",
    "research_claim_refs": [
      "D01",
      "E01"
    ],
    "claim_class": "attributed",
    "visual": "joeinspect"
  },
  {
    "id": "c20r3h03",
    "chapter": "帶繫繩環的舊盒，準備寄回去",
    "text": "盒蓋晃得厲害，鉸鏈旁邊，還有一個原本能接繫繩的小環。",
    "research_claim_refs": [
      "E02",
      "D02"
    ],
    "claim_class": "attributed",
    "visual": "loop"
  },
  {
    "id": "c20r3h04",
    "chapter": "帶繫繩環的舊盒，準備寄回去",
    "text": "他想修緊那裡，卻又怕，外殼添上難看的修補痕跡。",
    "research_claim_refs": [
      "E03"
    ],
    "claim_class": "attributed",
    "visual": "joeinspect"
  },
  {
    "id": "c20r3h05",
    "chapter": "帶繫繩環的舊盒，準備寄回去",
    "text": "等回件到了，小環旁邊，會不會多出新的焊痕？",
    "research_claim_refs": [
      "D04"
    ],
    "claim_class": "question",
    "visual": "loopinspect"
  },
  {
    "id": "c20r3h06",
    "chapter": "帶繫繩環的舊盒，準備寄回去",
    "text": "兩年後，日本另一只粉紅小盒寄出，原來的內膽，還會回來嗎？",
    "research_claim_refs": [
      "J09",
      "J17"
    ],
    "claim_class": "question",
    "visual": "sealed"
  },
  {
    "id": "c20r3h07",
    "chapter": "帶繫繩環的舊盒，準備寄回去",
    "text": "今天沿著 Zippo 兩次真實送修，看終身承諾怎麼處理新機件與舊物。",
    "research_claim_refs": [
      "D01",
      "J01",
      "O07"
    ],
    "claim_class": "editorial_promise",
    "visual": "twoparcels"
  },
  {
    "id": "c20r3h08",
    "chapter": "帶繫繩環的舊盒，準備寄回去",
    "text": "我想問的是，它到底保證修好什麼，又替你留下什麼？",
    "research_claim_refs": [
      "O07",
      "O09",
      "D05",
      "J18"
    ],
    "claim_class": "reaction_question",
    "visual": "twoparcels"
  },
  {
    "id": "c20r3o01",
    "chapter": "想修鬆蓋，卻遲遲沒寄的舊盒",
    "text": "面對開頭那個鬆蓋，喬瑟夫早就想試試免費修，但這個念頭，擱了將近一年。",
    "research_claim_refs": [
      "E02",
      "E15"
    ],
    "claim_class": "attributed",
    "visual": "joethink"
  },
  {
    "id": "c20r3o02",
    "chapter": "想修鬆蓋，卻遲遲沒寄的舊盒",
    "text": "這句能用、否則免費修的承諾，公司後來回顧一九三三年首款時，也把它寫進去。",
    "research_claim_refs": [
      "H02",
      "H03",
      "O07"
    ],
    "claim_class": "attributed",
    "visual": "brass"
  },
  {
    "id": "c20r3o03",
    "chapter": "想修鬆蓋，卻遲遲沒寄的舊盒",
    "text": "落到他手上，問題變成：把這只舊盒送走，換回來的，會是什麼樣子？",
    "research_claim_refs": [
      "E03",
      "E05"
    ],
    "claim_class": "editorial_link",
    "visual": "joeinspect"
  },
  {
    "id": "c20r3o04",
    "chapter": "想修鬆蓋，卻遲遲沒寄的舊盒",
    "text": "我在意的，是那個「修」字，最後會落在哪一個零件上。",
    "research_claim_refs": [
      "O07",
      "D02"
    ],
    "claim_class": "reaction",
    "visual": "loop"
  },
  {
    "id": "c20r3o05",
    "chapter": "想修鬆蓋，卻遲遲沒寄的舊盒",
    "text": "你若想把某些舊東西留下，免費二字，還沒有替你選完。",
    "research_claim_refs": [
      "D02",
      "D05"
    ],
    "claim_class": "viewer_conditional",
    "visual": "brass"
  },
  {
    "id": "c20r3o06",
    "chapter": "想修鬆蓋，卻遲遲沒寄的舊盒",
    "text": "那位美國收藏者標到的舊盒，究竟還留下哪些特徵？",
    "research_claim_refs": [
      "E01"
    ],
    "claim_class": "question",
    "visual": "joeinspect"
  },
  {
    "id": "c20r3o07",
    "chapter": "想修鬆蓋，卻遲遲沒寄的舊盒",
    "text": "他說，這是一次深夜或清早，在拍賣網站標到的舊物。",
    "research_claim_refs": [
      "E01"
    ],
    "claim_class": "attributed",
    "visual": "acquisition"
  },
  {
    "id": "c20r3o08",
    "chapter": "想修鬆蓋，卻遲遲沒寄的舊盒",
    "text": "整只已經磨損，盒上還有船隻與盾牌圖樣，也留著刻字。",
    "research_claim_refs": [
      "E01"
    ],
    "claim_class": "attributed",
    "visual": "brass"
  },
  {
    "id": "c20r3o09",
    "chapter": "想修鬆蓋，卻遲遲沒寄的舊盒",
    "text": "那些圖案還保有不少顏色，讓這只舊殼，不只是任意一個金屬盒。",
    "research_claim_refs": [
      "E01"
    ],
    "claim_class": "editorial_link",
    "visual": "brass"
  },
  {
    "id": "c20r3o10",
    "chapter": "想修鬆蓋，卻遲遲沒寄的舊盒",
    "text": "帶著這樣的小環與鬆蓋，這只舊物，還適合直接帶在身上用嗎？",
    "research_claim_refs": [
      "E02"
    ],
    "claim_class": "question",
    "visual": "loop"
  },
  {
    "id": "c20r3o11",
    "chapter": "想修鬆蓋，卻遲遲沒寄的舊盒",
    "text": "開頭那個亂晃的蓋子，讓他擔心，繼續照原本用途帶著走，反而會更傷。",
    "research_claim_refs": [
      "E02"
    ],
    "claim_class": "attributed",
    "visual": "joeinspect"
  },
  {
    "id": "c20r3o13",
    "chapter": "想修鬆蓋，卻遲遲沒寄的舊盒",
    "text": "他甚至怕，有一部分可能會掉走；這是他對繼續使用的顧慮，不是已經弄丟。",
    "research_claim_refs": [
      "E02"
    ],
    "claim_class": "attributed",
    "visual": "loop"
  },
  {
    "id": "c20r3o14",
    "chapter": "想修鬆蓋，卻遲遲沒寄的舊盒",
    "text": "但知道廠商說免費修，他就立刻寄回去了嗎？",
    "research_claim_refs": [
      "E03"
    ],
    "claim_class": "question",
    "visual": "joethink"
  },
  {
    "id": "c20r3o15",
    "chapter": "想修鬆蓋，卻遲遲沒寄的舊盒",
    "text": "他在回顧裡說，自己曾看過一些修過的舊件，鉸鏈歪斜，旁邊留著不好看的痕跡。",
    "research_claim_refs": [
      "E03"
    ],
    "claim_class": "attributed",
    "visual": "repairconcern"
  },
  {
    "id": "c20r3o17",
    "chapter": "想修鬆蓋，卻遲遲沒寄的舊盒",
    "text": "當他把一批待修舊物的照片，放進社群想找人交換時，有人問他，為什麼不寄回去？",
    "research_claim_refs": [
      "E04"
    ],
    "claim_class": "attributed",
    "visual": "photoqueue"
  },
  {
    "id": "c20r3o18",
    "chapter": "想修鬆蓋，卻遲遲沒寄的舊盒",
    "text": "這個提醒，卻沒有先替他回答，這種帶環的鉸鏈，現在還能不能照原樣處理。",
    "research_claim_refs": [
      "E04",
      "E05"
    ],
    "claim_class": "editorial_link",
    "visual": "loop"
  },
  {
    "id": "c20r3o19",
    "chapter": "想修鬆蓋，卻遲遲沒寄的舊盒",
    "text": "他先寄了一封電子郵件，問的就是，這只特殊款還能不能恢復原來的樣子。",
    "research_claim_refs": [
      "E05"
    ],
    "claim_class": "attributed",
    "visual": "email"
  },
  {
    "id": "c20r3o20",
    "chapter": "想修鬆蓋，卻遲遲沒寄的舊盒",
    "text": "你若要把有刻字的舊物交出去，大概也會想，先得到一個說得夠具體的答覆。",
    "research_claim_refs": [
      "E01",
      "E05"
    ],
    "claim_class": "viewer_conditional",
    "visual": "joethink"
  },
  {
    "id": "c20r3o21",
    "chapter": "想修鬆蓋，卻遲遲沒寄的舊盒",
    "text": "那麼，這封信寄出後，他真的等到完整回覆，才把打火機裝箱嗎？",
    "research_claim_refs": [
      "E05"
    ],
    "claim_class": "question",
    "visual": "email"
  },
  {
    "id": "c20r3i01",
    "chapter": "回信還沒來，包裹先出門",
    "text": "他等得不耐，最後沒有繼續等回信，就決定把打火機寄出去。",
    "research_claim_refs": [
      "E05"
    ],
    "claim_class": "attributed",
    "visual": "joepack"
  },
  {
    "id": "c20r3i02",
    "chapter": "回信還沒來，包裹先出門",
    "text": "真正交給修理端時，他有沒有把要求寫得更具體？",
    "research_claim_refs": [
      "D02"
    ],
    "claim_class": "question",
    "visual": "joerequest"
  },
  {
    "id": "c20r3i03",
    "chapter": "回信還沒來，包裹先出門",
    "text": "在送修表上，他要求修好鉸鏈和小環；如果可以，也補上已經缺掉的繫繩。",
    "research_claim_refs": [
      "D02"
    ],
    "claim_class": "attributed",
    "visual": "joerequest"
  },
  {
    "id": "c20r3i04",
    "chapter": "回信還沒來，包裹先出門",
    "text": "他當時讀到的說明，按產品有不同的包裝和寄法，自己只關心口袋打火機。",
    "research_claim_refs": [
      "E07"
    ],
    "claim_class": "attributed",
    "visual": "joerequest"
  },
  {
    "id": "c20r3i05",
    "chapter": "回信還沒來，包裹先出門",
    "text": "開頭同包的另一只普通鍍鉻款，他要求接回上蓋，並裝上一組新的內膽。",
    "research_claim_refs": [
      "E14"
    ],
    "claim_class": "attributed",
    "visual": "plainchrome"
  },
  {
    "id": "c20r3i09",
    "chapter": "回信還沒來，包裹先出門",
    "text": "這只普通款，他連怎麼取得都記不清，只記得，來自一小批舊物。",
    "research_claim_refs": [
      "E20"
    ],
    "claim_class": "attributed",
    "visual": "plainchrome"
  },
  {
    "id": "c20r3i25",
    "chapter": "回信還沒來，包裹先出門",
    "text": "他不指望那只舊款靠外表吸引人，卻說，很希望它能繼續派上用場。",
    "research_claim_refs": [
      "E21"
    ],
    "claim_class": "attributed",
    "visual": "plainchrome"
  },
  {
    "id": "c20r3i06",
    "chapter": "回信還沒來，包裹先出門",
    "text": "剛剛那只帶環的舊盒，在他公開的照片裡，對應的修理表勾的是哪一欄？",
    "research_claim_refs": [
      "E16"
    ],
    "claim_class": "question",
    "visual": "joerequest"
  },
  {
    "id": "c20r3i07",
    "chapter": "回信還沒來，包裹先出門",
    "text": "你能看見，後方那張表的鉸鏈插銷欄，打了一個勾。",
    "research_claim_refs": [
      "E16"
    ],
    "claim_class": "viewer_reaction",
    "visual": "twocushioned"
  },
  {
    "id": "c20r3i08",
    "chapter": "回信還沒來，包裹先出門",
    "text": "我覺得抉擇就在那個「如果可以」：繫繩，是他提出的希望，還不是已經拿到的結果。",
    "research_claim_refs": [
      "D02"
    ],
    "claim_class": "reaction",
    "visual": "loop"
  },
  {
    "id": "c20r3i10",
    "chapter": "回信還沒來，包裹先出門",
    "text": "那包舊物，是隨便丟進信封，就直接寄出嗎？",
    "research_claim_refs": [
      "E07"
    ],
    "claim_class": "question",
    "visual": "joepack"
  },
  {
    "id": "c20r3i11",
    "chapter": "回信還沒來，包裹先出門",
    "text": "他當時讀到的表格，建議用堅固的盒子，或有緩衝的郵寄袋。",
    "research_claim_refs": [
      "E07"
    ],
    "claim_class": "attributed",
    "visual": "mailer"
  },
  {
    "id": "c20r3i12",
    "chapter": "回信還沒來，包裹先出門",
    "text": "表格還提醒，多件寄修，難以追蹤或避免損傷，建議一包放一到兩只。",
    "research_claim_refs": [
      "E07"
    ],
    "claim_class": "attributed",
    "visual": "twocushioned"
  },
  {
    "id": "c20r3i13",
    "chapter": "回信還沒來，包裹先出門",
    "text": "他說，三月第一週，自己仔細做好保護，再照這份表格裡的地址，把包裹送走。",
    "research_claim_refs": [
      "E07",
      "E09"
    ],
    "claim_class": "attributed",
    "visual": "joepack"
  },
  {
    "id": "c20r3i14",
    "chapter": "回信還沒來，包裹先出門",
    "text": "表格地址和一些收藏者記得的不一樣，這次包裹，到底到了沒有？",
    "research_claim_refs": [
      "E08"
    ],
    "claim_class": "question",
    "visual": "address"
  },
  {
    "id": "c20r3i15",
    "chapter": "回信還沒來，包裹先出門",
    "text": "三月十八日，一封電子郵件，帶來了收件消息。",
    "research_claim_refs": [
      "E09"
    ],
    "claim_class": "attributed",
    "visual": "joeship"
  },
  {
    "id": "c20r3i16",
    "chapter": "回信還沒來，包裹先出門",
    "text": "他在日記裡記下，通知收到了兩只，數量跟自己同一包寄出的相符。",
    "research_claim_refs": [
      "E09",
      "E06"
    ],
    "claim_class": "attributed",
    "visual": "email"
  },
  {
    "id": "c20r3i17",
    "chapter": "回信還沒來，包裹先出門",
    "text": "他原本沒有預期，廠商還會主動寄來，收件與出件的通知。",
    "research_claim_refs": [
      "E09"
    ],
    "claim_class": "attributed",
    "visual": "twocushioned"
  },
  {
    "id": "c20r3i18",
    "chapter": "回信還沒來，包裹先出門",
    "text": "收到之後，那封原本詢問特殊鉸鏈的信，就有答案了嗎？",
    "research_claim_refs": [
      "E10"
    ],
    "claim_class": "question",
    "visual": "email"
  },
  {
    "id": "c20r3i19",
    "chapter": "回信還沒來，包裹先出門",
    "text": "還沒有；他先等到的是三月二十九日，另一封通知，說包裹已經寄回。",
    "research_claim_refs": [
      "E09",
      "E10"
    ],
    "claim_class": "attributed",
    "visual": "joeship"
  },
  {
    "id": "c20r3i20",
    "chapter": "回信還沒來，包裹先出門",
    "text": "一直到這份出件通知之後，他才收到先前那封詢問的回覆。",
    "research_claim_refs": [
      "E10"
    ],
    "claim_class": "attributed",
    "visual": "email"
  },
  {
    "id": "c20r3i21",
    "chapter": "回信還沒來，包裹先出門",
    "text": "但那封信，只是一般性地表示能修，沒有特別回答帶環鉸鏈該怎麼處理。",
    "research_claim_refs": [
      "E10"
    ],
    "claim_class": "attributed",
    "visual": "joerequest"
  },
  {
    "id": "c20r3i22",
    "chapter": "回信還沒來，包裹先出門",
    "text": "我這時會更想打開包裹，直接看看，這次他到底拿回了什麼。",
    "research_claim_refs": [
      "D04",
      "E10"
    ],
    "claim_class": "reaction",
    "visual": "sealedbrass"
  },
  {
    "id": "c20r3i23",
    "chapter": "回信還沒來，包裹先出門",
    "text": "你若是他，這時最想確認的，應該也是那個自己特別提出過要求的小環。",
    "research_claim_refs": [
      "D02",
      "D04"
    ],
    "claim_class": "viewer_conditional",
    "visual": "loopinspect"
  },
  {
    "id": "c20r3i24",
    "chapter": "回信還沒來，包裹先出門",
    "text": "那只他原本怕添上焊痕的舊殼，最後真的多了一道傷嗎？",
    "research_claim_refs": [
      "D04"
    ],
    "claim_class": "question",
    "visual": "loopinspect"
  },
  {
    "id": "c20r3e01",
    "chapter": "蓋子收緊，舊磨痕仍在",
    "text": "開頭那個小環旁邊，喬瑟夫回件後看，沒有看到新的焊痕或疤。",
    "research_claim_refs": [
      "D04",
      "E11"
    ],
    "claim_class": "attributed",
    "visual": "loopinspect"
  },
  {
    "id": "c20r3e02",
    "chapter": "蓋子收緊，舊磨痕仍在",
    "text": "他說，缺掉的繫繩補上了，原本鬆動的鉸鏈，也收緊了。",
    "research_claim_refs": [
      "D04",
      "E11"
    ],
    "claim_class": "attributed",
    "visual": "lanyard"
  },
  {
    "id": "c20r3e03",
    "chapter": "蓋子收緊，舊磨痕仍在",
    "text": "小環是怎麼留下來的？他的觀察是，看來只換了那根彎成環的插銷。",
    "research_claim_refs": [
      "D04",
      "E11"
    ],
    "claim_class": "attributed_question",
    "visual": "loop"
  },
  {
    "id": "c20r3e04",
    "chapter": "蓋子收緊，舊磨痕仍在",
    "text": "他用的是「看來」，這是拆包後的觀察，不是廠內逐步怎麼修的紀錄。",
    "research_claim_refs": [
      "D04"
    ],
    "claim_class": "editorial_boundary",
    "visual": "loop"
  },
  {
    "id": "c20r3e05",
    "chapter": "蓋子收緊，舊磨痕仍在",
    "text": "同包裡那只要接回上蓋的普通舊款，回來時，又有什麼不同？",
    "research_claim_refs": [
      "E14",
      "E17"
    ],
    "claim_class": "question",
    "visual": "plainchrome"
  },
  {
    "id": "c20r3e08",
    "chapter": "蓋子收緊，舊磨痕仍在",
    "text": "喬瑟夫說，這只換上的鉸鏈，接點看起來，像他近期見過的新打火機一樣整齊。",
    "research_claim_refs": [
      "E17"
    ],
    "claim_class": "attributed",
    "visual": "twocases"
  },
  {
    "id": "c20r3e09",
    "chapter": "蓋子收緊，舊磨痕仍在",
    "text": "而這只外殼上，原先的表面磨損，也跟著回來了。",
    "research_claim_refs": [
      "D05"
    ],
    "claim_class": "attributed",
    "visual": "brass"
  },
  {
    "id": "c20r3e10",
    "chapter": "蓋子收緊，舊磨痕仍在",
    "text": "你若以為免費修，就是把它的外觀全部變新，這次的回件，給的是另一種結果。",
    "research_claim_refs": [
      "D05"
    ],
    "claim_class": "viewer_conditional",
    "visual": "brass"
  },
  {
    "id": "c20r3e11",
    "chapter": "蓋子收緊，舊磨痕仍在",
    "text": "不過包裹裡的擺法，反而讓他又擔心起，殼上留下的顏色。",
    "research_claim_refs": [
      "E12"
    ],
    "claim_class": "editorial_link",
    "visual": "returnbag"
  },
  {
    "id": "c20r3e12",
    "chapter": "蓋子收緊，舊磨痕仍在",
    "text": "他覺得，兩只舊物像是直接放進氣泡信封，回程時可能互相碰撞。",
    "research_claim_refs": [
      "E12"
    ],
    "claim_class": "attributed",
    "visual": "returnbag"
  },
  {
    "id": "c20r3e13",
    "chapter": "蓋子收緊，舊磨痕仍在",
    "text": "這次真的撞壞，或掉了他想留的漆嗎？",
    "research_claim_refs": [
      "E12"
    ],
    "claim_class": "question",
    "visual": "brass"
  },
  {
    "id": "c20r3e14",
    "chapter": "蓋子收緊，舊磨痕仍在",
    "text": "他隨即補充，這次送達完好，並不是在抱怨已經發生的損傷。",
    "research_claim_refs": [
      "E12"
    ],
    "claim_class": "attributed",
    "visual": "twocases"
  },
  {
    "id": "c20r3e15",
    "chapter": "蓋子收緊，舊磨痕仍在",
    "text": "只是其中一只還有他不想失去的顏色，這也正是寄出時，他仔細包裝的原因。",
    "research_claim_refs": [
      "E12"
    ],
    "claim_class": "attributed",
    "visual": "brass"
  },
  {
    "id": "c20r3e16",
    "chapter": "蓋子收緊，舊磨痕仍在",
    "text": "我覺得這個擔心很實在：修好連接處，還不等於替他決定，怎麼保護表面。",
    "research_claim_refs": [
      "D04",
      "E12"
    ],
    "claim_class": "reaction",
    "visual": "returnbag"
  },
  {
    "id": "c20r3e17",
    "chapter": "蓋子收緊，舊磨痕仍在",
    "text": "他要怎麼避免，下次再讓兩只舊物，在回程碰在一起？",
    "research_claim_refs": [
      "E13"
    ],
    "claim_class": "question",
    "visual": "singleparcel"
  },
  {
    "id": "c20r3e18",
    "chapter": "蓋子收緊，舊磨痕仍在",
    "text": "他說，未來一次只寄一只，讓舊塗裝少一點互相碰撞的機會。",
    "research_claim_refs": [
      "E13"
    ],
    "claim_class": "attributed",
    "visual": "singleparcel"
  },
  {
    "id": "c20r3e19",
    "chapter": "蓋子收緊，舊磨痕仍在",
    "text": "這只帶環舊物修理的，是連著盒蓋的結構；而負責點火的內膽，還有另一層。",
    "research_claim_refs": [
      "D04",
      "O04"
    ],
    "claim_class": "editorial_link",
    "visual": "separatebrass"
  },
  {
    "id": "c20r3e20",
    "chapter": "蓋子收緊，舊磨痕仍在",
    "text": "傳統款把內膽抽出時，上蓋與鉸鏈仍跟著外殼，點火機件則留在抽出的內套裡。",
    "research_claim_refs": [
      "O04",
      "P04"
    ],
    "claim_class": "fact",
    "visual": "separatebrass"
  },
  {
    "id": "c20r3e21",
    "chapter": "蓋子收緊，舊磨痕仍在",
    "text": "同一個「修」字，可以落在外殼的連接，也可以碰到內部整組機件。",
    "research_claim_refs": [
      "O04",
      "D04",
      "U03"
    ],
    "claim_class": "editorial_link",
    "visual": "insert"
  },
  {
    "id": "c20r3e22",
    "chapter": "蓋子收緊，舊磨痕仍在",
    "text": "但如果壞的是內膽，廠商會修原來那組，還是乾脆換一組新的？",
    "research_claim_refs": [
      "J17",
      "U03"
    ],
    "claim_class": "question",
    "visual": "insert"
  },
  {
    "id": "c20r3t01",
    "chapter": "粉紅色禮物，輪子也停住了",
    "text": "兩年後在日本，開頭預告的那只粉紅小盒，因內部機件問題，進了寄修包裹。",
    "research_claim_refs": [
      "J09",
      "J03",
      "J14"
    ],
    "claim_class": "attributed",
    "visual": "gift"
  },
  {
    "id": "c20r3t02",
    "chapter": "粉紅色禮物，輪子也停住了",
    "text": "這是收到的禮物，他估計已用約三到四年，期間曾換火石，也換過裡面的填料。",
    "research_claim_refs": [
      "J01",
      "J02"
    ],
    "claim_class": "attributed",
    "visual": "supplies"
  },
  {
    "id": "c20r3t04",
    "chapter": "粉紅色禮物，輪子也停住了",
    "text": "開合太鬆之後，他在裡面，看見了什麼問題？",
    "research_claim_refs": [
      "J03"
    ],
    "claim_class": "question",
    "visual": "wheel"
  },
  {
    "id": "c20r3t05",
    "chapter": "粉紅色禮物，輪子也停住了",
    "text": "他看到凸輪彈簧裂了，也說曾用產品結構圖，查故障部位的名字。",
    "research_claim_refs": [
      "J03",
      "E18"
    ],
    "claim_class": "attributed",
    "visual": "components"
  },
  {
    "id": "c20r3t06",
    "chapter": "粉紅色禮物，輪子也停住了",
    "text": "他說，也許因此，磨輪也轉不動了，已經沒辦法點火。",
    "research_claim_refs": [
      "J04",
      "J05"
    ],
    "claim_class": "attributed",
    "visual": "search"
  },
  {
    "id": "c20r3t07",
    "chapter": "粉紅色禮物，輪子也停住了",
    "text": "這一次，使用者會直接寄回廠商，還是先找零件，想辦法自己修？",
    "research_claim_refs": [
      "J06"
    ],
    "claim_class": "question",
    "visual": "search"
  },
  {
    "id": "c20r3t08",
    "chapter": "粉紅色禮物，輪子也停住了",
    "text": "他先往網路找，覺得零件若能備齊，在家修，也許不是完全辦不到。",
    "research_claim_refs": [
      "J06"
    ],
    "claim_class": "attributed",
    "visual": "search"
  },
  {
    "id": "c20r3t09",
    "chapter": "粉紅色禮物，輪子也停住了",
    "text": "但因為自己這只不是一般大小，替換零件的搜尋，最後看來走不通。",
    "research_claim_refs": [
      "J06"
    ],
    "claim_class": "attributed",
    "visual": "separate"
  },
  {
    "id": "c20r3t10",
    "chapter": "粉紅色禮物，輪子也停住了",
    "text": "廠商那裡，還有能接手的入口嗎？",
    "research_claim_refs": [
      "J07"
    ],
    "claim_class": "question",
    "visual": "form"
  },
  {
    "id": "c20r3t11",
    "chapter": "粉紅色禮物，輪子也停住了",
    "text": "他當時也沒有原盒與收據，查維修費時，想過若太貴，就乾脆買新。",
    "research_claim_refs": [
      "J08"
    ],
    "claim_class": "attributed",
    "visual": "pinkinspect"
  },
  {
    "id": "c20r3t12",
    "chapter": "粉紅色禮物，輪子也停住了",
    "text": "他查到正品有免費終身保證；我這才看到，選擇裡多了送回廠商這條路。",
    "research_claim_refs": [
      "J07",
      "J14"
    ],
    "claim_class": "reaction",
    "visual": "emptybox"
  },
  {
    "id": "c20r3t13",
    "chapter": "粉紅色禮物，輪子也停住了",
    "text": "查到保證後，他選的，仍是把這份禮物寄出去，沒有就此換掉整只。",
    "research_claim_refs": [
      "J07",
      "J14"
    ],
    "claim_class": "attributed",
    "visual": "parcel"
  },
  {
    "id": "c20r3t14",
    "chapter": "粉紅色禮物，輪子也停住了",
    "text": "他當時交出去的，會只有那個小零件嗎？",
    "research_claim_refs": [
      "J03",
      "J11"
    ],
    "claim_class": "question",
    "visual": "components"
  },
  {
    "id": "c20r3t15",
    "chapter": "粉紅色禮物，輪子也停住了",
    "text": "他在備忘錄列的送修內容，是外殼、內膽與修理表。",
    "research_claim_refs": [
      "E22"
    ],
    "claim_class": "attributed",
    "visual": "separate"
  },
  {
    "id": "c20r3t16",
    "chapter": "粉紅色禮物，輪子也停住了",
    "text": "他把外殼與內膽分開包好，放在同一個袋子，讓這份禮物的兩部分，一起離開手邊。",
    "research_claim_refs": [
      "J11",
      "E23"
    ],
    "claim_class": "attributed",
    "visual": "wrap"
  },
  {
    "id": "c20r3t17",
    "chapter": "粉紅色禮物，輪子也停住了",
    "text": "你若想留下用慣的機件，這時要等的，還不只是粉紅外殼能不能回來。",
    "research_claim_refs": [
      "J11",
      "J17"
    ],
    "claim_class": "viewer_reaction",
    "visual": "oldinsert"
  },
  {
    "id": "c20r3t27",
    "chapter": "粉紅色禮物，輪子也停住了",
    "text": "整趟往返四十七天後，他收到寄回的包裹。",
    "research_claim_refs": [
      "J14",
      "J15"
    ],
    "claim_class": "attributed",
    "visual": "sealed"
  },
  {
    "id": "c20r3t30",
    "chapter": "粉紅色禮物，輪子也停住了",
    "text": "他以為廠商既然整組換新，卸下來的舊內膽，應該就不會再寄回。",
    "research_claim_refs": [
      "J17"
    ],
    "claim_class": "attributed",
    "visual": "oldinsert"
  },
  {
    "id": "c20r3t31",
    "chapter": "粉紅色禮物，輪子也停住了",
    "text": "那開頭預告的粉紅小盒回來時，包裹裡，真的少了原來那組嗎？",
    "research_claim_refs": [
      "J17",
      "J18"
    ],
    "claim_class": "question",
    "visual": "sealed"
  },
  {
    "id": "c20r3n01",
    "chapter": "原來的內膽，也一起回來",
    "text": "開頭那個粉紅小盒的回件拆開後，他寫下的結果是，新舊兩組內膽都在裡面。",
    "research_claim_refs": [
      "J18"
    ],
    "claim_class": "attributed",
    "visual": "sealed"
  },
  {
    "id": "c20r3n02",
    "chapter": "原來的內膽，也一起回來",
    "text": "作者照片的左邊，是打開的粉紅殼，裡面裝著一組內膽。",
    "research_claim_refs": [
      "J22"
    ],
    "claim_class": "attributed",
    "visual": "returned"
  },
  {
    "id": "c20r3n03",
    "chapter": "原來的內膽，也一起回來",
    "text": "右邊還有另一組，表面磨損比較明顯，放在氣泡材料上。",
    "research_claim_refs": [
      "J22"
    ],
    "claim_class": "fact",
    "visual": "oldinsert"
  },
  {
    "id": "c20r3n04",
    "chapter": "原來的內膽，也一起回來",
    "text": "跟著內膽返還的，只有這些金屬嗎？",
    "research_claim_refs": [
      "J19",
      "E19"
    ],
    "claim_class": "question",
    "visual": "wrappingreturn"
  },
  {
    "id": "c20r3n05",
    "chapter": "原來的內膽，也一起回來",
    "text": "作者還寫，寄去的東西全回來了，圖說列出緩衝材、紙膠帶，郵件袋也跟著回到手邊。",
    "research_claim_refs": [
      "J19",
      "E19"
    ],
    "claim_class": "attributed",
    "visual": "wrappingreturn"
  },
  {
    "id": "c20r3n07",
    "chapter": "原來的內膽，也一起回來",
    "text": "我會把旁邊那組收好，因為換下來的，也可能正是你想留下的東西。",
    "research_claim_refs": [
      "J18"
    ],
    "claim_class": "reaction",
    "visual": "returned"
  },
  {
    "id": "c20r3n08",
    "chapter": "原來的內膽，也一起回來",
    "text": "這回原內膽一起回來，是不是因為他事先在送修表上，特別要求了？",
    "research_claim_refs": [
      "J13",
      "J18"
    ],
    "claim_class": "question",
    "visual": "form"
  },
  {
    "id": "c20r3n09",
    "chapter": "原來的內膽，也一起回來",
    "text": "他沒有公開填妥的表格，也沒有交代退舊的理由，不能替他補上一個申請。",
    "research_claim_refs": [
      "J13",
      "J18"
    ],
    "claim_class": "editorial_boundary",
    "visual": "form"
  },
  {
    "id": "c20r3n10",
    "chapter": "原來的內膽，也一起回來",
    "text": "那今天想把舊內膽拿回來，還能只靠這次個案的結果，不另外問嗎？",
    "research_claim_refs": [
      "U03",
      "U04"
    ],
    "claim_class": "question",
    "visual": "oldinsert"
  },
  {
    "id": "c20r3n11",
    "chapter": "原來的內膽，也一起回來",
    "text": "英國二〇二六年版修理表，寫的是內膽通常換新；想拿回舊的，得在說明欄要求。",
    "research_claim_refs": [
      "U03",
      "U04"
    ],
    "claim_class": "attributed",
    "visual": "form"
  },
  {
    "id": "c20r3n12",
    "chapter": "原來的內膽，也一起回來",
    "text": "這份英國的條件，讓你看到，想修好與想拿回原件，可以是兩個要說清楚的要求。",
    "research_claim_refs": [
      "U04"
    ],
    "claim_class": "viewer_conditional",
    "visual": "form"
  },
  {
    "id": "c20r3n13",
    "chapter": "原來的內膽，也一起回來",
    "text": "美國現在的條款，還承諾連塗裝與裝飾，都一起翻新嗎？",
    "research_claim_refs": [
      "O09"
    ],
    "claim_class": "question",
    "visual": "brass"
  },
  {
    "id": "c20r3n14",
    "chapter": "原來的內膽，也一起回來",
    "text": "美國明列，塗裝與裝飾不在終身保證內；功能修好，並不承諾外觀翻新。",
    "research_claim_refs": [
      "O07",
      "O09"
    ],
    "claim_class": "attributed",
    "visual": "case"
  },
  {
    "id": "c20r3n15",
    "chapter": "原來的內膽，也一起回來",
    "text": "這位日本作者也沒有記錄回件後的燃燒表現，照片裡沒有火焰。",
    "research_claim_refs": [
      "J22"
    ],
    "claim_class": "editorial_boundary",
    "visual": "returned"
  },
  {
    "id": "c20r3n16",
    "chapter": "原來的內膽，也一起回來",
    "text": "回到開頭，Zippo承諾的是恢復工作；要留下哪些舊東西，還有使用者自己那一份選擇。",
    "research_claim_refs": [
      "O07",
      "O09",
      "D02",
      "E13",
      "J18",
      "U04"
    ],
    "claim_class": "editorial_answer",
    "visual": "twoparcels"
  },
  {
    "id": "c20r3n17",
    "chapter": "原來的內膽，也一起回來",
    "text": "如果是你的舊物，你會特別要求留下哪一部分，還是只想讓它繼續陪你？",
    "research_claim_refs": [],
    "claim_class": "cta",
    "visual": "gift"
  },
  {
    "id": "c20r3n18",
    "chapter": "原來的內膽，也一起回來",
    "text": "想繼續看日用品一句承諾，怎麼變成具體的選擇，歡迎訂閱品牌故事。",
    "research_claim_refs": [],
    "claim_class": "cta",
    "visual": "gift"
  }
];
const visual={
  "brass": "A worn plain warm brass hinged metal case resting on a wooden tabletop, gentle side light.",
  "joeinspect": "An anonymous adult collector examining a worn plain warm brass hinged metal case, concerned expression, soft window light.",
  "loop": "A simple loose hinge and a small loop at the side of a worn unmarked warm brass metal case, mild side light.",
  "loopinspect": "An anonymous adult holding a closed plain warm brass metal case with a small side loop above a wooden table, inspecting it before any work, soft window light.",
  "joethink": "An anonymous adult collector considering an unmarked warm brass metal case on a clear wooden desk, thoughtful expression, gentle indoor light.",
  "earlycase": "A plain unmarked rectangular hinged metal pocket case on a simple old wooden counter, soft room light.",
  "acquisition": "An anonymous adult collector setting a worn unmarked warm brass hinged case beside a plain parcel on a desk, mild overhead light.",
  "repairconcern": "A close view of a generic uneven metal hinge beside an unmarked metal panel in a conceptual component tray, muted side light.",
  "photoqueue": "An anonymous adult collector looking at a device showing only abstract shapes beside several closed plain metal cases, soft desk light.",
  "email": "An anonymous adult reading a device with abstract nonlinguistic blocks beside a closed plain gray mailer, gentle room light.",
  "joepack": "An anonymous adult carefully wrapping a worn plain brass metal case in cushioning before an open gray mailer, soft side light.",
  "joerequest": "An anonymous adult pausing with a pencil over an unmarked sheet beside a closed plain brass case with a small side loop, soft window light.",
  "plainchrome": "A worn plain silvery hinged metal case resting on cushioning beside a closed unmarked gray mailing pouch, muted daylight.",
  "chromehinge": "An anonymous adult collector examining a simple hinge at the edge of a worn unmarked silvery metal lid, gentle side light.",
  "twocushioned": "Two separately cushioned small plain metal cases resting beside an open gray mailing pouch, mild room light.",
  "mailer": "An anonymous adult holding an empty plain gray mailing pouch beside cushioning on a tabletop, soft indoor light.",
  "address": "An anonymous hand holding the back of an unmarked sheet beside an open gray mailing pouch, gentle desk light.",
  "joeship": "An anonymous adult holding a sealed plain gray parcel beside a clear table, mild side light.",
  "sealedbrass": "A closed opaque gray padded mailer resting on an empty wooden tabletop, soft overhead light.",
  "lanyard": "A worn unmarked warm brass hinged case with a simple cord loosely beside its small side loop, gentle window light.",
  "returnbag": "Two closed unmarked metal cases lying apart beside an open plain padded gray mailer on a table, soft side light.",
  "twocases": "A plain warm brass hinged case with a small side loop beside a worn plain silvery hinged case on cushioning, mild indoor light.",
  "singleparcel": "One closed plain padded mailer resting beside a single cushioned metal object on a wooden desk, soft side light.",
  "separatebrass": "An anonymous adult lifting a plain silver insert above an open unmarked brass metal case, gentle room light.",
  "insert": "A plain silver open-top lighter insert resting on an unmarked work surface, mild side light.",
  "gift": "An anonymous adult holding a small plain pink hinged metal case above a wooden tabletop, thoughtful expression, warm indoor light.",
  "supplies": "A small flint and pale wick beside a plain silver insert on a clear work surface, gentle side light.",
  "pinkinspect": "An anonymous adult examining a plain pink hinged metal case on a wooden tabletop, puzzled expression, gentle window light.",
  "wheel": "The small serrated wheel on a plain silver lighter insert resting on a wooden tabletop, muted indoor light.",
  "components": "An anonymous adult looking at an unmarked component tray beside a plain silver insert, focused expression, soft side light.",
  "search": "An anonymous adult considering a narrow plain pink metal case beside a wider plain dark green hinged case on a table, gentle room light.",
  "separate": "An anonymous adult holding a plain silver lighter insert above an open plain pink metal case on a wooden tabletop, gentle window light.",
  "form": "An anonymous adult looking at an unmarked sheet beside a closed plain pink metal case, soft indoor light.",
  "emptybox": "An empty plain cardboard tray beside a small closed plain pink hinged metal case, muted window light.",
  "parcel": "A transparent pouch containing small cushioned shapes beside an open plain gray mailer and an unmarked sheet, soft side light.",
  "dry": "A plain silver lighter insert resting separately from an open plain pink metal case on a clear wooden tabletop near a window, muted daylight.",
  "wrap": "An anonymous adult wrapping a plain silver insert in cushioning beside a separately wrapped plain pink metal case, mild desk light.",
  "tracking": "An anonymous adult checking a device showing only abstract nonlinguistic marks beside a sealed gray mailer, gentle room light.",
  "sealed": "An anonymous adult resting one hand beside a closed opaque plain gray padded mailer on a wooden table, anticipatory expression, soft window light.",
  "waiting": "An anonymous adult sitting comfortably beside an uncluttered table, relaxed shoulders, warm indoor light.",
  "oldinsert": "A worn plain silver insert resting separately on clear cushioning, gentle side light.",
  "returned": "An open plain pink hinged metal case holding one plain silver insert on cushioning with another worn silver insert nearby, soft window light.",
  "wrappingreturn": "Clear cushioning, a short strip of pale tape and a closed opaque gray mailing pouch on a wooden tabletop, soft indoor light.",
  "case": "A closed plain pink hinged metal case resting beside a worn unmarked warm brass case on a neutral cloth, mild side light.",
  "twoparcels": "Two distinct closed opaque plain gray mailing pouches placed apart on a wooden desk, soft room light."
};
const seen=new Map();let globalShotIndex=0;for(const r of rows){assert(visual[r.visual],r.visual);const n=seen.get(r.visual)??0;seen.set(r.visual,n+1);const framing=['Medium shot','Close-up','Medium close-up','Wide shot'];r.prompt=framing[n%4]+' of '+visual[r.visual];r.camera=['push in','pan left','pull out','pan right'][globalShotIndex++%4];}
const promptOverrides={
  "c20r3i09": "Wide shot of an anonymous adult beside a shallow tray containing a few unmarked metal objects on a clear desk, mild room light.",
  "c20r3i25": "Medium close-up of an anonymous hand holding an open plain silvery chrome case above an uncluttered tabletop, gentle window light.",
  "c20r3t29": "Medium shot of an anonymous adult considering a small closed opaque gray parcel on a table, subdued window light.",
  "c20r3t30": "Close-up of a single worn plain silver insert beside a closed unmarked cardboard tray, soft room light.",
  "c20r3e03": "Close-up of a simple hinge and small side loop on a plain unmarked warm brass metal case, neutral inspection view, soft side light.",
  "c20r3e04": "Medium close-up of an anonymous hand holding a plain warm brass metal case by its hinge and small side loop for inspection, gentle window light.",
  "c20r3e09": "Close-up of a worn plain silvery chrome hinged metal case resting on cushioning, mild side light.",
  "c20r3h08": "Medium shot of an anonymous adult considering two closed opaque gray parcels placed apart on a clear wooden desk, gentle indoor light.",
  "c20r3o03": "Close-up of an anonymous hand holding a closed plain brass pocket case above an empty wooden counter, soft side light.",
  "c20r3t15": "Close-up of a plain silver insert beside a closed pink hinged metal case and the back of an unmarked sheet, soft indoor light.",
  "c20r3o09": "Close-up of a worn edge of a plain brass lid beside a small metal loop, muted side light.",
  "c20r3i03": "Close-up of an unmarked pencil beside the back of a plain sheet with a closed brass case partly visible, gentle desk light.",
  "c20r3i04": "Medium shot of a small loop and hinge on a closed plain brass case resting by a folded unmarked request sheet, soft indoor light.",
  "c20r3i24": "Close-up of an unopened opaque gray padded mailer on a clear tabletop, soft overhead light.",
  "c20r3e07": "Close-up of a plain silver hinge and the worn edge of a silvery metal lid on neutral cushioning, soft side light.",
  "c20r3e10": "Medium shot of an anonymous adult considering a worn brass case and a plain silvery case placed apart on a clear table, soft room light.",
  "c20r3e12": "Close-up of two closed plain metal cases lying apart on clear cushioning, no outer mailer in view, muted daylight.",
  "c20r3e18": "Medium shot of an anonymous adult placing one small cushioned metal object beside one empty gray mailer, soft window light.",
  "c20r3e20": "Close-up of a silver open-top insert resting separately from an open plain brass outer case on a neutral work surface, soft side light.",
  "c20r3e22": "Medium shot of an anonymous adult holding a plain silver insert above an empty wooden tabletop, thoughtful expression, mild indoor light.",
  "c20r3t06": "Close-up of a serrated wheel at the top of a plain silver insert on a clear surface, muted side light.",
  "c20r3t07": "Medium shot of an anonymous adult considering a small closed plain pink metal case in one hand, gentle room light.",
  "c20r3t17": "Close-up of two separately cushioned small metal objects inside a transparent pouch, soft overhead light.",
  "c20r3t20": "Close-up of anonymous hands holding a small device above a clear table, three abstract nonlinguistic dots visible on its screen, soft window light.",
  "c20r3t21": "Medium shot of a sealed plain gray padded mailer beside clear cushioning on a wooden desk, mild side light.",
  "c20r3t22": "Close-up of an empty plain cardboard tray at the edge of a wooden table beside a small closed pink case, muted daylight.",
  "c20r3t31": "Close-up of a worn plain silver insert resting alone on a neutral surface, gentle side light.",
  "c20r3n05": "Close-up of a short strip of pale tape on flattened clear cushioning beside an opaque gray mailer, mild indoor light.",
  "c20r3n09": "Medium shot of an anonymous adult holding the back of an unmarked sheet beside a closed pink case, soft room light.",
  "c20r3n12": "Close-up of a closed plain pink hinged case resting near two separate silver inserts on cushioning, soft window light."
};for(const r of rows)if(promptOverrides[r.id])r.prompt=promptOverrides[r.id];
const r7Visuals=new Map(read(path.join(OUT,'history/r7/video.json')).scenes.filter(s=>s.template==='shot').map(s=>[s.id,s.data]));for(const r of rows.slice(0,-3)){const original=r7Visuals.get(r.id);assert(original,'R7 retained visual '+r.id);r.prompt=original.prompt;r.camera=original.camera;}
const pairDefs=[['c20r3h05','c20r3e01','loop-inspection-before-result'],['c20r3h06','c20r3n01','pink-return-parcel-before-opening']];for(const[a,b]of pairDefs){const setup=rows.find(r=>r.id===a),payoff=rows.find(r=>r.id===b);setup.prompt=payoff.prompt;setup.camera=payoff.camera;}
const loopDefs=[["c20r3o03", "c20r3e01", "舊盒送出後回件未見新焊痕"], ["c20r3h05", "c20r3e01", "帶環case無新焊痕"], ["c20r3h06", "c20r3n01", "日本新舊內膽同返"], ["c20r3h08", "c20r3n16", "功能承諾與保留選擇"], ["c20r3o06", "c20r3o08", "舊殼圖樣刻字仍在"], ["c20r3o10", "c20r3o11", "作者擔心繼續攜帶增損"], ["c20r3o14", "c20r3o15", "先前所見舊修件令他遲疑"], ["c20r3o21", "c20r3i01", "未等詢問回信便寄"], ["c20r3i02", "c20r3i03", "明寫特殊hinge與loop請求"], ["c20r3i06", "c20r3i07", "原照片勾hinge pin"], ["c20r3i10", "c20r3i11", "當時表建議堅固盒或緩衝袋"], ["c20r3i14", "c20r3i15", "收到18日到件通知"], ["c20r3i18", "c20r3i19", "先等到29日出件通知"], ["c20r3i24", "c20r3e01", "原環旁未見新焊痕"], ["c20r3e05", "c20r3e08", "Joseph觀察普通款replacement hinge接點如近期新物"], ["c20r3e13", "c20r3e14", "到貨完好未報新增損傷"], ["c20r3e17", "c20r3e18", "下次分開一只寄"], ["c20r3t04", "c20r3t05", "作者看見cam spring裂"], ["c20r3t07", "c20r3t09", "非regular尺寸令零件搜尋卡住"], ["c20r3t10", "c20r3t12", "查到免費終身保證入口"], ["c20r3t14", "c20r3t15", "備忘錄列外殼內膽與修理表一同送出"], ["c20r3t31", "c20r3n01", "原內膽也在包裹裡"], ["c20r3n04", "c20r3n05", "包材郵件袋也回來"], ["c20r3n08", "c20r3n09", "未公開表或退舊理由"], ["c20r3n10", "c20r3n11", "UK表需提出退舊要求"], ["c20r3n13", "c20r3n14", "US功能保證排除外觀翻新"]];const loops=loopDefs.map(([setup,payoff,what])=>({setup,payoff,what}));
const title='Zippo終身免費修，2次送修留下什麼？｜品牌故事';
const scenes=[];let chapter='';for(const r of rows.slice(0,-3)){const s={id:r.id,template:'shot',data:{prompt:r.prompt,visual:'still',camera:r.camera},lines:[{id:r.id,text:r.text,emotion:'對一位觀眾自然說書，四到五字每秒的聊天速度；實際觀察、作者推測與當代地域條款讀清楚'}]};if(r.chapter!==chapter){chapter=r.chapter;s.chapter=chapter;}scenes.push(s);}
scenes.push({id:'c20r3outro',template:'outro',data:{title:'換新，也留下舊內膽',cta:'你會保留換下的舊機件嗎？'},lines:rows.slice(-3).map(r=>({id:r.id,text:r.text,emotion:'對一位觀眾溫暖收束，自然邀請'}))});
const usedIds=new Set(rows.flatMap(r=>r.research_claim_refs).flatMap(id=>{const c=research.claims.find(c=>c.id===id);assert(c,id);return[c.evidence.source_id,...(c.supporting_caption_evidence?[c.supporting_caption_evidence.source_id]:[])];}));
const sources=research.sources.filter(s=>usedIds.has(s.id));
const description='同一句終身功能承諾，怎麼落在不同的舊物上？從2022美國收藏者Joseph遲遲未寄的鬆蓋舊物，追同包兩只修件。1933首款/保證只歸屬公司後來回憶。帶環Camden款補繩、看來換pin且無新焊痕；同包普通款換hinge。其後是2024日本ゆきいるか粉紅禮物不能點火、寄修後新舊內膽同返。兩次送修、不同人國家與物件，沒有同serial延續、互相啟發或修法移用。47日只日本單次旅程，不是實修工時或現行時限。JP未公開完成表/勾選/退舊要求或原因、未記回件後成功燃燒；US不補原先不能點火或廠內新焊接工序。UK2026退舊條件只按地域短說；US當代finish exclusion不擴成全球所有產品。\n\n原始來源（下載親讀2026-10-26，歷史與現行分開）\n'+sources.map(s=>s.publisher+'：'+s.research_use+'\n'+s.url).join('\n');
const doc={schema_version:1,slug:SLUG,format:'drama',category:'story',narration_locale:'zh-TW',target_minutes:[12,14],voice,subtitles:{burn_in:true},look:{preset:'cute-mystery'},characters:[],music:{prompt:'light, curious, a little mysterious, no vocals',gain_db:-20,duck_db:-10},loops,youtube:{category_id:27,made_for_kids:false,default_language:'zh-TW',title,description,tags:['Zippo','之寶','打火機','維修','品牌故事','日用品的意外轉身'],video_id:null},thumbnail:{template:'thumb',data:{layout:'d',headline:'免費修換掉誰',sub:'兩次回件看原件',brand:'ZIPPO',tag:'品牌故事',shot:'c20r3h02'}},sources:sources.map(s=>({title:s.publisher+' '+s.id,url:s.url,checked_on:'2026-10-26'})),assets:[],scenes};
const validation=validateVideo(doc);assert.equal(validation.errors?.length??0,0,JSON.stringify(validation.errors));write('video.json',doc);write('narration-only.json',rows.map(({chapter,id,text})=>({chapter,id,text})));
const script=['# '+title,'','C20 R8作者稿，HOLD。ID／章名不讀；13分鐘是原目標，字量容量風險如實保留，沒有用紙面字量冒充實聲。待另一位來源／配鏡QA與全新讀者；沒有SOURCE PASS、敘事批准或owner批准。',''];chapter='';for(const r of rows){if(r.chapter!==chapter){chapter=r.chapter;script.push('## '+chapter,'');}script.push('### '+r.id,'',r.text,'');}fs.writeFileSync(path.join(OUT,'script.md'),script.join('\n'));
const anchorRegistry={};for(const c of research.claims){anchorRegistry[c.id+'-Q1']={id:c.id+'-Q1',research_claim_id:c.id,...c.evidence};if(c.supporting_caption_evidence)anchorRegistry[c.id+'-CAPTION']={id:c.id+'-CAPTION',research_claim_id:c.id,...c.supporting_caption_evidence};}
const jp=research.sources.find(s=>s.id==='JP_NOTE'),jpText=fs.readFileSync(jp.text_path,'utf8'),normalize=x=>x.replace(/\s+/g,' ').trim();
const extraQuotes={J06:'部品さえ揃えば家でも直せそう',J08:'新しく買うのも視野にいれつつ修理料金調べた',J10:'届いたかどうかで問い合わせるのも億劫だったので',J12:'箱などの付属品は同封しないよう',J13:'ご返却先住所を未記入、または間違えると帰ってこない',J15:'1週間や3か月、半年',J07:'純正品であれば無料生涯保障'};
for(const[id,q]of Object.entries(extraQuotes)){assert(normalize(jpText).includes(normalize(q)),q);anchorRegistry[id+'-EXTRA']={id:id+'-EXTRA',research_claim_id:id,source_id:'JP_NOTE',raw_path:jp.raw_path,raw_sha256:jp.raw_sha256,quote:q,locator:{text_path:jp.text_path,text_sha256:jp.text_sha256,normalized_whitespace:true,normalized_text_character_offset:normalize(jpText).indexOf(normalize(q))},role:'Additional short exact anchor from the same personally read primary account; does not edit frozen research.'};}
const dfPre=research.sources.find(s=>s.id==='DF_PRE_REPAIR'),dfText=fs.readFileSync(dfPre.text_path,'utf8'),dfQuote='I wasn’t expecting to be notified';assert(normalize(dfText).includes(normalize(dfQuote)));anchorRegistry['E09-EXTRA']={id:'E09-EXTRA',research_claim_id:'E09',source_id:'DF_PRE_REPAIR',raw_path:dfPre.raw_path,raw_sha256:dfPre.raw_sha256,quote:dfQuote,locator:{text_path:dfPre.text_path,text_sha256:dfPre.text_sha256,normalized_whitespace:true,normalized_text_character_offset:normalize(dfText).indexOf(normalize(dfQuote))}};
const df=research.sources.find(s=>s.id==='DF_CASE'),dfCaseText=fs.readFileSync(df.text_path,'utf8'),productQuote='varying instructions on shipping and packaging depending on the product';assert(normalize(dfCaseText).includes(normalize(productQuote)));anchorRegistry['E07-EXTRA']={id:'E07-EXTRA',research_claim_id:'E07',source_id:'DF_CASE',raw_path:df.raw_path,raw_sha256:df.raw_sha256,quote:productQuote,locator:{text_path:df.text_path,text_sha256:df.text_sha256,normalized_whitespace:true,normalized_text_character_offset:normalize(dfCaseText).indexOf(normalize(productQuote))}};
const classes={attributed_question:'作者歸屬與旁白提問',attributed:'作者／公司有歸屬敘述',fact:'原件支持的限定事實',question:'旁白疑問',viewer_question:'對觀眾提問',reaction_question:'旁白反應與疑問',reaction:'旁白意見／反應',viewer_conditional:'對觀眾的明示條件／假設',viewer_reaction:'對觀眾反應',editorial_link:'編輯連接',editorial_boundary:'來源範圍界線',editorial_promise:'本集命名承諾',editorial_answer:'片尾回呼答案',cta:'觀眾邀請'};
const authored=rows.map((r,i)=>{const facts=r.research_claim_refs.map(id=>research.claims.find(c=>c.id===id));const anchors=Object.values(anchorRegistry).filter(a=>r.research_claim_refs.includes(a.research_claim_id));return{id:r.id,scene_id:i>=rows.length-3?'c20r3outro':r.id,claim:r.text,claim_class:classes[r.claim_class],claim_kind:r.claim_class,research_claim_ids:r.research_claim_refs,source_ids:[...new Set(anchors.map(a=>a.source_id))],quote_ids:anchors.map(a=>a.id),source_evidence:anchors,limits:facts.map(c=>c.forbidden_inferences_zh),visual_prompt:i>=rows.length-3?'Native outro typography; no generated image':r.prompt,visual_scope:'Anonymous explanatory concepts: US loop case, its separate plain chrome companion, and a later Japanese pink case are distinct objects. No named face, logo, readable letters, copied vessel/shield/engraving, flame, successful ignition or unobserved factory welding; Joe photo checkbox is attributed, JP completed form is unobserved.',independent_source_review:'PENDING_OTHER_REVIEWER',independent_visual_review:'PENDING_OTHER_REVIEWER'};});
for(const[a,b,asset]of pairDefs)for(const id of[a,b])authored.find(r=>r.id===id).planned_same_image={plan:'image-reuse-plan.json',asset_plan_id:asset,source_scene_id:b,reuse_scene_id:a,actual_file_sha256:null,status:'PLAN_ONLY'};
write('claims.json',{schema_version:1,status:'PENDING_INDEPENDENT_SOURCE_AND_VISUAL_QA',candidate_revision:'c20-r8',author:'/root/c20_primary_research',video_slug:SLUG,frozen_research_sha256:PROTECTED,source_registry:Object.fromEntries(research.sources.map(s=>[s.id,s])),anchor_registry:anchorRegistry,rows:authored,source_pass_claimed:false,approvals_created:0});
const cm=['# C20 R8 逐句來源與書面配鏡','','作者綁定，不是獨立SOURCE PASS。原研究63claims加作者23原文錨點；原raw159及68舊檔保持原SHA。每句寫清歸屬、反應、假設、來源邊界；原圖只作研究參照。','','| ID | 旁白 | 分類 | 原文錨點 |','| --- | --- | --- | --- |'];for(const c of authored)cm.push(`| ${c.id} | ${c.claim} | ${c.claim_class} | ${c.quote_ids.join('、')} |`);cm.push('','## 原件界線','','R8承諾為功能保證與舊物保存。1933僅公司後來回憶；2022 Joseph同包兩只各有requests/results，帶環款補繩看來換pin且無新焊痕，普通款另換hinge；2024日本粉紅case才是不能點火/換內膽/新舊同回。兩人國家物件與年月分開；沒有廠內連續工序、新焊接、跨例同serial、JP成功燃燒/填妥表格/要求退舊原因。UK2026末尾短界線不倒推JP。R1至R7來源/視覺/native verdict均封存，不套新稿。','');fs.writeFileSync(path.join(OUT,'claims.md'),cm.join('\n'));
const series={kind:'story',slug:'brand-story-remakes-20261025',episode:20,chapter:1,title,logline:'從2022美國鬆蓋待修與舊殼保留，追鉸鏈修件與2024日本內膽換新回件，看免費修與留下原件的不同選擇。',names:['Zippo','之寶','Joseph','喬瑟夫','ゆきいるか'],characters:[],visual_tier:'stills',compilation:false,target_minutes:13,image_model:'image-01',look:{preset:'cute-mystery'},candidate_revision:'c20-r8',status:'hold_pending_independent_source_and_fresh_readers'};write('series.json',series);
const whole=rows.reduce((n,r)=>n+spokenUnits(r.text),0),opening=rows.filter(r=>r.chapter===rows[0].chapter).reduce((n,r)=>n+spokenUnits(r.text),0),cta=rows.slice(-2).reduce((n,r)=>n+spokenUnits(r.text),0);assert(rows.every(r=>spokenUnits(r.text)<=40));
const brief=['# C20 R8｜同一句保證，兩次送修的換與留','','狀態：HOLD_PENDING_INDEPENDENT_SOURCE_AND_NATIVE8。R1全套已封存；R2來源文字PASS/書面HOLD、actualnative2共享三HOLD與A單讀者one_line/no_detour均封存history/r2，原文/輸入/binding/core/freeze/plan及保護檔原SHA保留。R3來源/書面PASS、verify、actualnative3共享no_recap HOLD（A i06/B t10）及raw/input/binding/payload/core/freeze/plan已完整history/r3封存，actualcount3。R4來源/書面PASS、verify、actualnative4共享no_detour HOLD（A t03/B t28）與B單讀者t14 no_recap、raw/input/binding/payload/core/freeze/plan已完整history/r4封存，actualcount4。R5來源/書面PASS、verify、actualnative5兩位共同指o16 no_recap HOLD及raw/input/binding/payload/core/freeze/plan/原runtime hash manifest完整封存history/r5，actualcount5，原round-5不改不重抽。R6來源/書面PASS、verify、actualnative6共同e06/e08 no_recap HOLD與B單讀者payoffs及raw/input/binding/payload/core/freeze/plan/原runtime與round6 hash manifest完整封存history/r6，actualcount6，原round-6不改不重抽。R7來源/書面PASS、verify、actualnative7兩票no_recap（A h06/t01、B t01/t02）及raw/input/binding/payload/core/freeze/plan/原runtime與round7 hash manifest完整封存history/r7，actualcount7，原round-7不改不重抽。current無舊verify；R8不沿用批准。新slug '+SLUG+'，category story、不重綁舊episode。','','## 問題','','Zippo終身保證到底修什麼，哪些舊東西會留下？','','## 一句答案','','承諾接住工作功能；2022美國Joseph帶環舊物修緊/補繩/看來換pin且舊finish仍在，同包普通款另換hinge；2024日本粉紅禮物則換inside unit並返還新舊兩組。保存哪些舊物與怎麼提出需求，仍有不同人的選擇及地域條件，不承諾全球保留每片原件。','','## 站主觀點','','同一因果難題是免費修功能如何碰上保留舊物，從2022美國舊盒遲遲未寄的難題→具體要求與回件→2024日本新內部故障→當代邊界往前；1933只一句公司後來回憶，嵌在當下功能承諾內。不是把同類商品列例，不虛構兩人承襲、同一serial或相互影響。','','## 實質改寫','','原日本單案承諾拓寬為兩次送修的功能/保存抉擇。增加Joseph真實零件與寄件行動：舊物來源與刻字/顏色、過去舊修件顧慮、社群交換回顧、先email未等回、不同物件的明確要求、原照片hinge-pin勾選、表格寄件/地址、三月收件出件email與較晚泛答、帶環款看來換pin/補繩/無新焊痕、同包另一只換hinge、回程包裝擔憂但未報新增損傷、未來分寄選擇。再交日本新的內部機件難題，不能把普通款換hinge說成Camden新焊或JP經歷。','','R8唯一旁白變更是t01，明確點名接回h06開場同一日本粉紅小盒的寄修事件，並撤掉t01的禮物稱呼；t02原句不改，收到禮物/估用3–4年/火石與填料仍只在這裡交代。兩年後、日本、內部機件問題及寄修動作等原事實不變，不冒用美國物件或另一位作者。其他107句、26 loops、h06與t01的完整prompt/camera、全部存留配鏡與兩組imageKey沿R7不動。原runtime只讀，免費檢查用author-r8內同集副本及原immutable三檔，不準備native8盲讀輸入。JP表格事件預告撤，當事人未公開完成表，不演勾選或要求退舊。UK僅末尾一段條件，不再開售後百科；美國新購一年客服全刪。','','## 開場與同圖','','第一句對你提出保存利害與同包兩只的來源數量，第二句接2022真準備動作，前六句進Joseph真行動與原物相關場面；最多兩預告，h05帶環檢視→e01、h06日本粉紅回件→n01；h07點名Zippo與兩次實修，h08中央問題。兩組共用中性前置圖，完整prompt/camera/look/model/size/version/seed原生Stage.imageKey一致；先payoff takes1/真cache guard/缺cache停/兩端judge/裁切後同檔SHA及assembly待驗，actualfalse。','','## 字量與媒體','','whole '+whole+' native units（coldopen '+opening+'、有聲CTA '+cta+'）；13分鐘、正文720–840秒自然語速與約3300–3500仍是規劃目標，低於3300約'+Math.max(0,3300-whole)+'、與3500差'+(3500-whole)+'，容量風險如實保留。4–5 units/s算術 '+(whole/5).toFixed(1)+'–'+(whole/4).toFixed(1)+'秒，不是音檔實測。官方時長口徑含coldopen及有聲CTA，僅排另外5秒/21秒頻道bookends。未量實聲，不把lint估秒當PASS。','','## 來源／畫面／字典','','原研究三檔/68舊檔/readonly snapshots/raw159未改；作者原文錨點author-primary-anchors-r3.json綁同raw，並非SOURCE PASS。企業1933是後來回憶，非同期原卡或創辦心理；Joseph照片與自述不是連續工序，US未補先前不能點火/焊接；JP未補成功點火/完成表/退舊原因。英文匿名prompt無品牌人名logo可讀字，不照抄船徽/刻字/版權裝飾，不畫焊接與火焰。正文shot100%。C06整個voice物件同源；既有本集不可變字典原head/version沿用，沒有重建或借別集。','','## 待辦','','另一位R8來源/配鏡QA與actualnative8 pending；owner/branding read-only preflight/製片入場/實聲/實圖/成片全待完成。沒有verify、自PASS、owner、Git/backend或付費。',''];fs.writeFileSync(path.join(OUT,'brief.md'),brief.join('\n'));
const coreFiles=['video.json','script.md','narration-only.json','claims.json'],coreHashes=Object.fromEntries(coreFiles.map(f=>[f,fileSha(path.join(OUT,f))]));
const plan={
  "schema_version": 1,
  "revision": "c20-r3",
  "status": "WRITTEN_REUSE_PLAN_PENDING_GENERATION_AND_REAL_FILE_SHA_VERIFICATION",
  "not_a_video_schema_extension": true,
  "not_a_keyframes_manifest": true,
  "no_assets_generated": true,
  "actual_same_asset_verified": false,
  "candidate_binding": {
    "core_four_sha256": {
      "video.json": "1590484bcebbd45dc29bcf4fe555895d7d39d56f216623a6f60980b9e9be0170",
      "script.md": "5ed7d81b2ba7455d64970dc407f4155e03fdb53cc4c31b2ed8fd6c77d453d2ad",
      "narration-only.json": "0fbbdf635e1668889917e021cbe4b0d601ba931577779c928b81e6bc8b0efbf7",
      "claims.json": "6170d489e93e97bb36f49b340e012924160576f04cbca4b3c3910fd9dcb1913b"
    },
    "claims_md_sha256": "9debb863e546ef5f9c614a1c861da58c51e1caf966be1216f65a574f7a0dce5c",
    "brief_sha256": "7f2fce54d15ebdd6bcf702cf6a66cb758212e4e4742a5bb0b01fcaf476299dff",
    "series_sha256": "7133d6fe8a4d9ecac064140e0da47a5d4a3054fd485513ab81986df841b9c604"
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
      "asset_plan_id": "loop-inspection-before-result",
      "role": "PLANNED_ONE_IDENTICAL_IMAGE_NOT_AN_ACTUAL_ASSET",
      "source_scene_id": "c20r3e01",
      "source_line_id": "c20r3e01",
      "reuse_scene_id": "c20r3h05",
      "reuse_line_id": "c20r3h05",
      "narration_setup_text": "等回件到了，小環旁邊，會不會多出新的焊痕？",
      "narration_payoff_text": "開頭那個小環旁邊，喬瑟夫回件後看，沒有看到新的焊痕或疤。",
      "source_prompt_sha256": "533b285b252bad703653a68b4c04f574131ad69feb5facba9a9b15c4755d7a3b",
      "reuse_prompt_sha256": "533b285b252bad703653a68b4c04f574131ad69feb5facba9a9b15c4755d7a3b",
      "prompt_exact_match": true,
      "source_camera": "pan left",
      "reuse_camera": "pan left",
      "composed_prompt_sha256": "f6aa701ac9dd7c2edd06474c99b4ea9b00457e616c5a7995e106ecd10d61989c",
      "no_result_drawn_in_teaser": "Anonymous owner holds a closed plain brass case with side loop for inspection before a result; no new weld, repaired pin, completed repair, replacement part, readable engraving or finish outcome is drawn.",
      "native_same_input_key_rehearsal": {
        "pure_local_functions_only": true,
        "input_tuple": {
          "provider": "minimax",
          "model": "image-01",
          "prompt": "Wide shot of An anonymous adult holding a closed plain warm brass metal case with a small side loop above a wooden table, inspecting it before any work, soft window light.. Style: cute Taiwanese YouTube explainer cartoon: chibi characters with big round heads, large expressive eyes and exaggerated comic expressions, thick clean dark outlines, flat colours with soft cel shading, a limited palette of deep navy night, parchment yellow, muted teal and one warning-red accent, subtle paper grain, simple clear backgrounds, one subject in the centre third, playful and friendly, 16:9. Camera: pan left",
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
        "base_key": "14da6fdbee2275d6",
        "native_stage_key": "10628c6d991ddf8d",
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
      "asset_plan_id": "pink-return-parcel-before-opening",
      "role": "PLANNED_ONE_IDENTICAL_IMAGE_NOT_AN_ACTUAL_ASSET",
      "source_scene_id": "c20r3n01",
      "source_line_id": "c20r3n01",
      "reuse_scene_id": "c20r3h06",
      "reuse_line_id": "c20r3h06",
      "narration_setup_text": "兩年後，日本另一只粉紅小盒寄出，原來的內膽，還會回來嗎？",
      "narration_payoff_text": "開頭那個粉紅小盒的回件拆開後，他寫下的結果是，新舊兩組內膽都在裡面。",
      "source_prompt_sha256": "d552889fedb669b7303ac68362ce72c9dfeadc148579c0964173ac953a7f3c33",
      "reuse_prompt_sha256": "d552889fedb669b7303ac68362ce72c9dfeadc148579c0964173ac953a7f3c33",
      "prompt_exact_match": true,
      "source_camera": "pull out",
      "reuse_camera": "pull out",
      "composed_prompt_sha256": "672a05de19ae06af4371ff86389ce15ecf09c7a4c086a3dda4b8fcaf1f540a66",
      "no_result_drawn_in_teaser": "Closed opaque mailer before opening; no pink case, contents, replacement unit, returned original, flame or successful repair is shown.",
      "native_same_input_key_rehearsal": {
        "pure_local_functions_only": true,
        "input_tuple": {
          "provider": "minimax",
          "model": "image-01",
          "prompt": "Medium shot of An anonymous adult resting one hand beside a closed opaque plain gray padded mailer on a wooden table, anticipatory expression, soft window light.. Style: cute Taiwanese YouTube explainer cartoon: chibi characters with big round heads, large expressive eyes and exaggerated comic expressions, thick clean dark outlines, flat colours with soft cel shading, a limited palette of deep navy night, parchment yellow, muted teal and one warning-red accent, subtle paper grain, simple clear backgrounds, one subject in the centre third, playful and friendly, 16:9. Camera: pull out",
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
        "base_key": "405fd645b4ec7dca",
        "native_stage_key": "bf1ad24b43c37ae3",
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
          "/workspace/work/brand-story-20261025/c20-submission-root",
          "keyframes",
          "--slug",
          "story-everyday-zippo-c20-remake-20261025",
          "--workdir",
          "/workspace/work/brand-story-20261025/c20-audit/media",
          "--shot",
          "c20r3e01",
          "--takes",
          "1"
        ]
      },
      {
        "purpose": "MANDATORY READ-ONLY LIVE CACHE GUARD BEFORE TEASER",
        "required_checks": [
          "Read actual keyframes/manifest.json source shot c20r3e01; require ordinary passed judge, needs_review false, one take, seed1, no fixes and live-recomputed exact Stage.imageKey.",
          "Hash selected bytes against selected.sha256; separately readCache(workdir) and require the live-key entry, actual file, provider/model and entry SHA all match.",
          "Any missing or changed entry/file/key/SHA/selection: STOP without teaser command, cache clearing, another purchase, forced selection or handwritten manifest."
        ]
      },
      {
        "purpose": "TEASER only after real cache guard succeeds, then ordinary independent endpoint judge",
        "argv": [
          "node",
          "docs/videos/brand-story-remakes-20261025/runtime-cli.mjs",
          "/workspace/work/brand-story-20261025/c20-submission-root",
          "keyframes",
          "--slug",
          "story-everyday-zippo-c20-remake-20261025",
          "--workdir",
          "/workspace/work/brand-story-20261025/c20-audit/media",
          "--shot",
          "c20r3h05",
          "--takes",
          "1"
        ]
      },
      {
        "purpose": "PAYOFF FIRST only after normal production admission",
        "argv": [
          "node",
          "docs/videos/brand-story-remakes-20261025/runtime-cli.mjs",
          "/workspace/work/brand-story-20261025/c20-submission-root",
          "keyframes",
          "--slug",
          "story-everyday-zippo-c20-remake-20261025",
          "--workdir",
          "/workspace/work/brand-story-20261025/c20-audit/media",
          "--shot",
          "c20r3n01",
          "--takes",
          "1"
        ]
      },
      {
        "purpose": "MANDATORY READ-ONLY LIVE CACHE GUARD BEFORE TEASER",
        "required_checks": [
          "Read actual keyframes/manifest.json source shot c20r3n01; require ordinary passed judge, needs_review false, one take, seed1, no fixes and live-recomputed exact Stage.imageKey.",
          "Hash selected bytes against selected.sha256; separately readCache(workdir) and require the live-key entry, actual file, provider/model and entry SHA all match.",
          "Any missing or changed entry/file/key/SHA/selection: STOP without teaser command, cache clearing, another purchase, forced selection or handwritten manifest."
        ]
      },
      {
        "purpose": "TEASER only after real cache guard succeeds, then ordinary independent endpoint judge",
        "argv": [
          "node",
          "docs/videos/brand-story-remakes-20261025/runtime-cli.mjs",
          "/workspace/work/brand-story-20261025/c20-submission-root",
          "keyframes",
          "--slug",
          "story-everyday-zippo-c20-remake-20261025",
          "--workdir",
          "/workspace/work/brand-story-20261025/c20-audit/media",
          "--shot",
          "c20r3h06",
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
plan.revision='c20-r8';plan.candidate_binding={core_four_sha256:coreHashes,claims_md_sha256:fileSha(path.join(OUT,'claims.md')),brief_sha256:fileSha(path.join(OUT,'brief.md')),series_sha256:fileSha(path.join(OUT,'series.json'))};plan.rule.sha256=fileSha(path.join(REPO,plan.rule.file));for(const f of Object.keys(plan.code_readback.files_sha256))plan.code_readback.files_sha256[f]=fileSha(path.join(REPO,f));
plan.pairs=pairDefs.map(([a,b,asset])=>{const setup=scenes.find(s=>s.id===a),payoff=scenes.find(s=>s.id===b);assert.equal(setup.data.prompt,payoff.data.prompt);assert.equal(setup.data.camera,payoff.data.camera);const prompt=shotPrompt(setup,resolveLook(doc.look),[],1500);assert.equal(prompt,shotPrompt(payoff,resolveLook(doc.look),[],1500));const tuple={provider:'minimax',model:'image-01',prompt,negative:'',width:1920,height:1080,seed:1,references:[]},opts={prompt,negative:'',references:[],seed:1,size:null},ctx={status:{image:{provider:'minimax',model:'image-01'}},format:null,imageVersion:imageSelectionVersion(series)},key=Stage.prototype.imageKey.call(ctx,opts);assert.equal(key,Stage.prototype.imageKey.call(ctx,{...opts,prompt:shotPrompt(payoff,resolveLook(doc.look),[],1500)}));return{asset_plan_id:asset,role:'PLANNED_ONE_IDENTICAL_IMAGE_NOT_AN_ACTUAL_ASSET',source_scene_id:b,source_line_id:b,reuse_scene_id:a,reuse_line_id:a,narration_setup_text:setup.lines[0].text,narration_payoff_text:payoff.lines[0].text,source_prompt_sha256:sha(payoff.data.prompt),reuse_prompt_sha256:sha(setup.data.prompt),prompt_exact_match:true,source_camera:payoff.data.camera,reuse_camera:setup.data.camera,composed_prompt_sha256:sha(prompt),no_result_drawn_in_teaser:asset==='loop-inspection-before-result'?'Anonymous owner holds a closed plain brass case with side loop for inspection before a result; no new weld, repaired pin, completed repair, replacement part, readable engraving or finish outcome is drawn.':'Closed opaque mailer before opening; no pink case, contents, replacement unit, returned original, flame or successful repair is shown.',native_same_input_key_rehearsal:{pure_local_functions_only:true,input_tuple:tuple,aspect:'16:9',requested_size:null,nominal_image_size:'1K',image_selection_version:imageSelectionVersion(series),seed_offset:0,takes:1,correction_list:[],prompt_budget_chars:1500,base_key:keyframeKey(tuple),native_stage_key:key,parameters_are_declared_plan_not_backend_readback:true,no_provider_call:true},actual_source_file:null,actual_source_sha256:null,actual_reused_file:null,actual_reused_sha256:null,actual_same_asset_verified:false,actual_same_file_sha_verified:false};});
plan.production_handoff.official_command_recipe_only=plan.pairs.flatMap(p=>[{purpose:'PAYOFF FIRST only after normal production admission',argv:['node','docs/videos/brand-story-remakes-20261025/runtime-cli.mjs',RUNTIME,'keyframes','--slug',SLUG,'--workdir',MEDIA,'--shot',p.source_scene_id,'--takes','1']},{purpose:'MANDATORY READ-ONLY LIVE CACHE GUARD BEFORE TEASER',required_checks:['Read actual keyframes/manifest.json source shot '+p.source_scene_id+'; require ordinary passed judge, needs_review false, one take, seed1, no fixes and live-recomputed exact Stage.imageKey.','Hash selected bytes against selected.sha256; separately readCache(workdir) and require the live-key entry, actual file, provider/model and entry SHA all match.','Any missing or changed entry/file/key/SHA/selection: STOP without teaser command, cache clearing, another purchase, forced selection or handwritten manifest.']},{purpose:'TEASER only after real cache guard succeeds, then ordinary independent endpoint judge',argv:['node','docs/videos/brand-story-remakes-20261025/runtime-cli.mjs',RUNTIME,'keyframes','--slug',SLUG,'--workdir',MEDIA,'--shot',p.reuse_scene_id,'--takes','1']}]);write('image-reuse-plan.json',plan);
const producer=['# C20 R8 製作交接','','作者recipe，provider/paid/backend/Git均0。runtime '+RUNTIME+'，media '+MEDIA+'。延用本集既有不可變lexicon，嚴禁重建字典或借別集批准；voice只沿C06完整正常object。','','兩次送修按時間前進；美國同包兩件各自requests/results不可互換，帶環殼沒有新焊痕只作者觀察pin，普通款另換hinge，不畫廠內焊接。日本另一只粉紅case，不補完成表/退舊要求/原因或成功燃燒。兩組h05→e01、h06→n01完整key相同；正式入場後payoff takes1→唯讀live cache/key/檔SHA守衛→才允許teaser，兩端judge/trim後真同檔及assembly驗收前actualfalse。','','繁中燒錄+CC；5秒片頭在coldopen後，21秒v4片尾在有聲CTA後。正式PR1860 branding required由root另作只讀preflight，不拉production pin。R8來源QA/native8/owner/製片均pending。',''];fs.writeFileSync(path.join(OUT,'producer.md'),producer.join('\n'));
write('protected-inputs-r8.json',{schema_version:1,role:'AUTHOR_INPUT_PROTECTION_NOT_SOURCE_QA',at_utc:new Date().toISOString(),research_three_sha256:PROTECTED,legacy_files:protectedOld,legacy_count:protectedOld.length,raw_manifest_path:rawManifestFile,raw_manifest_sha256:fileSha(rawManifestFile),raw_file_count:rawManifest.files.length,raw_all_match:true,legacy_and_snapshots_all_match:true});
write('author-notes.json',{schema_version:1,status:'HOLD_PENDING_INDEPENDENT_SOURCE_VISUAL_AND_FRESH_READERS',candidate_revision:'c20-r8',author:'/root/c20_primary_research',counts:{lines:rows.length,scenes:scenes.length,shots:scenes.filter(s=>s.template==='shot').length,cards:0,outro:1,chapters:6,loops:loops.length},native_units:{whole_narration_spoken_units:whole,coldopen:opening,voiced_CTA:cta,rough_planning_target:3500,delta_to_rough_target:whole-3500,actual_narration_seconds:null,actual_final_seconds:null,actual_duration_verified:false,planning_arithmetic_at_4_to_5_units_per_second:[whole/5,whole/4],planning_is_not_actual_time:true,official_duration_scope:'Whole unwrapped narration including coldopen and voiced CTA; only separately added channel bookends excluded.',capacity_status:'MATERIAL_CAPACITY_RISK_BELOW_3300_TO_3500_NOT_ACTUAL_DURATION_PASS'},voice_source:{path:voicePath,file_sha256:fileSha(voicePath),voice_object_sha256:sha(JSON.stringify(voice)),exact_copy:true,other_episode_dictionary_copied:false},source_research_sha256:PROTECTED,protected_old_file_count:68,raw_preserved_file_count:rawManifest.files.length,protected_old_and_snapshot_unchanged:true,source_pass_claimed:false,narrative_pass_claimed:false,owner_approval_created:false,actual_media_generated:false,actual_same_image_verified:false,provider_calls:0,paid_calls:0,backend_mutations:0,git_mutations:0,runtime_root:RUNTIME,media_base:MEDIA,image_reuse_plan_sha256:fileSha(path.join(OUT,'image-reuse-plan.json')),independent_source_review:'PENDING_OTHER_REVIEWER',independent_narrative_review:'PENDING_FRESH_READERS'});
console.log(JSON.stringify({core_four_sha256:coreHashes,whole_units:whole,coldopen:opening,CTA:cta,lines:rows.length,scenes:scenes.length,shots:scenes.filter(s=>s.template==='shot').length,reuse_plan_sha256:fileSha(path.join(OUT,'image-reuse-plan.json'))},null,2));
