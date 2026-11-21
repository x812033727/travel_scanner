#!/usr/bin/env node
/**
 * Shorts 零台詞短劇前檢、Google Flow 轉寫與盲評彙整工具
 * （對應 docs/videos/shorts-drama/{WRITING,REVIEW,PRODUCTION-ROUTES}.md）
 *
 * 用法：
 *   node docs/videos/shorts-drama/preflight.mjs check <spec-or-plan.json> [--engine h3|flow|veo] [--json] [--strict]
 *   node docs/videos/shorts-drama/preflight.mjs export-flow <spec.json> [--out flow-prompts.md]
 *   node docs/videos/shorts-drama/preflight.mjs score-blind <judge1.json> <judge2.json> [judge3.json ...] [--threshold 70] [--json]
 */
import { readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { parseArgs } from 'node:util';

export const HARD_DURATION = Object.freeze({ min: 9.0, max: 20.0 });
export const GOLDEN_DURATION = Object.freeze({ min: 11.0, max: 16.0 });
export const MAX_MOTION_SECONDS = 3.5;
export const TAIL_SFX_MARGIN_SECONDS = 0.45;

// 對齊 docs/videos/SHORTS.md 與 tools/video/shorts/build.mjs 的 1080×1920 安全區：
// x: 78–902 (0.072–0.835), y: 180–1380 (0.094–0.719)
export const SAFE_ZONE = Object.freeze({
  minX: 78 / 1080,
  maxX: 902 / 1080,
  minY: 180 / 1920,
  maxY: 1380 / 1920,
});

export const RUBRIC_MAX = Object.freeze({
  hook: 15,
  premise: 10,
  laughs: 20,
  escalation: 10,
  surprise: 15,
  character: 10,
  payoff: 10,
  share: 10,
});

export const SERIES_DIRS = Object.freeze({
  'wangjia-couple': '汪家夫妻',
  'raccoon-mischief': '闖禍小浣熊',
  'influencer-piglet': '網美小豬',
  'shechu-hell': '社畜地獄',
});

export const FLOW_AUDIO_GUARDRAIL =
  'Silent film visual comedy: zero spoken dialogue, no voices, no gibberish speech, no background music; only subtle natural foley sounds.';

export const SAFE_ZONE_FRAMING_NOTE =
  'Keep key face, furry paws, and punchline props framed inside the middle-upper 9:16 safe area, clear of the bottom quarter and right edge.';

const CALLS_TO_ACTION = [
  /(?:按|點|給)(?:個|我個|我一個|一個|一下)?讚/u,
  /小鈴鐺/u,
  /點(?:擊|下|一下|個)?連結/u,
  /(?:記得|別忘了?|請|快|歡迎|幫我|按|點|來)訂閱|訂閱(?:頻道|我們|我|本頻道|一下|起來|加|並|＋|\+)/u,
  /(?:記得|別忘了?|請|快|歡迎|幫我|來)追蹤|追蹤(?:我們|我|頻道|本頻道|一下|起來)/u,
  /\b(?:subscribe|like\s+and\s+subscribe|ring\s+the\s+bell|link\s+in\s+bio)\b/i,
];

const POSITIVE_HUMAN_LIMB_RE = /\b(?<!no\s)(?<!without\s)human\s+(?:hand|hands|finger|fingers|arm|arms)\b/i;
const HOLDING_PROP_RE = /\b(?<!camera\s)(?:holding|holds|grasping|grabbing|clutches|clutching)\b(?!\s+(?:a\s+static|still|steady|frozen|perfectly\s+still))/i;
const ANIMAL_PAW_RE = /\b(?:paw|paws|hoof|hooves|claw|claws|trotter|trotters)\b/i;
const OFFSCREEN_REACH_RE = /\b(?:hand|arm|paw)\s+reaches?\s+in\b|\breaches?\s+in\s+from\s+(?:the\s+)?(?:edge|off-?screen|side)\b/i;
const DISGUISE_CUE_RE = /\b(?:pretend(?:s|ing)?|disguis(?:e|ed|ing)|swaddled|inside\s+a\s+[\w\s]*vase|hanging\s+from\s+(?:the\s+)?ceiling\s+hook|empty\s+tv\s+frame|picture\s+frame|as\s+a\s+(?:clock|lamp|vase|chandelier|statue|baby))\b/i;
const SELF_ANCHOR_RE = /\b(?:himself|herself)\b/i;
const NEGATIVE_PEOPLE_RE = /\bno\s+(?:people|humans|person|persons|passersby|pedestrians|crowd)\b/i;
const CROWD_PRONE_ENV_RE = /\b(?:office|street(?!\s*(?:lamp|light))|alley|parking\s+lot|cafe|coffee\s+shop|restaurant|subway|mall|supermarket)\b/i;
const ENCLOSED_BG_RE = /\b(?:solid|plain\s+\w*\s*wall|blank\s+wall|empty\s+room|no\s+cubicles|brick\s+wall|wooden\s+fence|high\s+wall|closed\s+room|empty\s+rooftop|empty\s+parking)\b/i;
const FORBIDDEN_PRINT_RE = /\b(?:magazine\s+cover|watermark|brand\s+logo)\b/i;
const TEXT_PRONE_PROP_RE = /\b(?:laptop|smartphone|phone\s+screen|monitor|computer\s+screen|wall\s+clock|clock\s+face|bar\s+chart|chart|book|newspaper|snack\s+bag|cereal\s+box)\b/i;
const UNBRANDED_GUARD_RE = /\b(?:unbranded|plain|blank|no\s+text|no\s+logos?|no\s+numbers|logo-?free|wordless)\b/i;
const CLOSED_MOUTH_RE = /\b(?:lips\s+remain\s+closed|mouth\s+stays?\s+closed|mouth\s+closed|lips\s+closed|closed\s+mouth|silent\s+closed\s+mouth)\b/i;
const AMBIGUOUS_SMILE_RE = /\b(?:rueful|wry\s+smile|smirk(?:s|ing)?)\b/i;
const CAMERA_ENDING_RE = /\b(?:static\s+shot|locked\s+(?:shot|camera|frame)|pushes?\s+in|pulls?\s+(?:back|out)|pans?\s+(?:left|right)|tilts?\s+(?:up|down)|zooms?\s+(?:in|out)|camera\s+holds)\b/i;
const AI_DISCLOSURE_RE = /(?:AI|人工智慧|合成|生成|synthetic)/i;

export function detectSeries(slug = '') {
  const value = String(slug || '').toLowerCase();
  for (const key of Object.keys(SERIES_DIRS)) {
    if (value.startsWith(`${key}-`) || value === key) return key;
  }
  return null;
}

export function detectMode(doc) {
  const shots = Array.isArray(doc?.shots) ? doc.shots : [];
  if (shots.some((s) => typeof s?.ff === 'string' && s.ff.trim().length > 0)) return 'spec';
  if (typeof doc?.music === 'string' || shots.some((s) => typeof s?.clip === 'string' && /\.(?:mp4|mov|mkv)$/i.test(s.clip))) {
    return 'plan';
  }
  return 'spec';
}

function normalizeSfxList(raw) {
  if (!Array.isArray(raw)) return [];
  const list = [];
  for (const entry of raw) {
    if (Array.isArray(entry)) {
      list.push({ name: String(entry[0] ?? ''), at: Number(entry[1]), gain_db: entry[2] ?? 0 });
    } else if (entry && typeof entry === 'object') {
      list.push({
        name: String(entry.file ?? entry.name ?? ''),
        at: Number(entry.at),
        gain_db: entry.gain_db ?? 0,
      });
    }
  }
  return list;
}

function issue(severity, code, shotId, message, fix) {
  return { severity, code, shot: shotId ?? null, message, fix };
}

/**
 * 執行零台詞 Shorts 分鏡規格（<slug>.json）或剪接表（edit/plan.json）前檢。
 */
export function preflightShort(doc, { engine = 'h3', mode: forcedMode = null } = {}) {
  const issues = [];
  if (!doc || typeof doc !== 'object' || Array.isArray(doc)) {
    return {
      ok: false,
      mode: 'unknown',
      series: null,
      engine,
      summary: { shots: 0, totalDuration: 0, errors: 1, warnings: 0 },
      issues: [issue('error', 'invalid_json', null, '輸入必須是 JSON 物件', '確認檔案為有效的 <slug>.json 或 edit/plan.json')],
    };
  }

  const mode = forcedMode || detectMode(doc);
  const series = detectSeries(doc.slug);
  const shots = Array.isArray(doc.shots) ? doc.shots : [];

  if (!shots.length) {
    issues.push(issue('error', 'missing_shots', null, 'shots 陣列是空的', '至少需要 4–7 鏡（黃金五拍結構）'));
  }

  let totalDuration = 0;
  let hasMusicOff = false;
  const shotIds = new Set();
  const intros = doc.intros && typeof doc.intros === 'object' ? doc.intros : {};

  for (let i = 0; i < shots.length; i += 1) {
    const shot = shots[i] || {};
    const shotId = shot.id || `shot_${String(i + 1).padStart(2, '0')}`;
    if (shot.id) {
      if (shotIds.has(shot.id)) {
        issues.push(issue('error', 'duplicate_shot_id', shotId, `鏡號重複：${shot.id}`, '每鏡需有唯一 id'));
      }
      shotIds.add(shot.id);
    }

    const dur = Number(shot.dur);
    const hold = Number(shot.hold ?? 0);
    const inSec = Number(shot.in ?? 0);
    if (!Number.isFinite(dur) || dur <= 0) {
      issues.push(issue('error', 'invalid_dur', shotId, `dur 無效（${shot.dur}）`, '填入正數秒數（建議 0.6–3.0 秒）'));
    } else {
      totalDuration += dur;
      if (hold < 0 || hold > dur) {
        issues.push(issue('error', 'invalid_hold', shotId, `hold (${hold}s) 超出 dur (${dur}s)`, 'hold 必須介於 0 與 dur 之間'));
      }
      const motionDur = dur - (Number.isFinite(hold) ? Math.max(0, hold) : 0);
      const isStill = Boolean(shot.still) || (typeof shot.clip === 'string' && /-still\.mp4$/i.test(shot.clip));
      if (!isStill && motionDur > MAX_MOTION_SECONDS) {
        issues.push(
          issue(
            'error',
            'shot_too_long',
            shotId,
            `動態段長度 ${motionDur.toFixed(2)}s 超過 ${MAX_MOTION_SECONDS}s 上限`,
            '5 秒 H3／8 秒 Veo 片段後半容易變形或自行換景；拆成兩鏡、剪短 dur，或加上 hold 定格／still 靜圖慢推',
          ),
        );
      }

      // 第 1 鏡鉤子節奏檢查
      if (i === 0) {
        if (series === 'influencer-piglet' && dur > 1.5) {
          issues.push(
            issue(
              'error',
              'piglet_hook_too_long',
              shotId,
              `《網美小豬》第 1 鏡唯美照 dur=${dur}s 超過 1.5s`,
              '唯美照必須壓在 1.0–1.2s（0.9s 快門聲）立刻拉遠揭曉假景，否則觀眾直接滑走',
            ),
          );
        } else if (dur > 2.5) {
          issues.push(
            issue(
              'warn',
              'hook_too_long',
              shotId,
              `第 1 鏡（鉤子）dur=${dur}s 偏長，建議壓在 0.8–1.5s`,
              '第一格直接從出事／衝突瞬間開始，避免前 1.2 秒太慢造成高滑走率',
            ),
          );
        }
      }
    }

    if (Number.isFinite(inSec) && inSec < 0) {
      issues.push(issue('error', 'invalid_in', shotId, `in (${inSec}s) 不可小於 0`, '預設設為 0.2–0.3s 避開啟動抖動'));
    }

    if (shot.music_off) hasMusicOff = true;

    // 音效落點檢查（杜絕收尾音效被切斷）
    const sfxList = normalizeSfxList(shot.sfx);
    for (const sfx of sfxList) {
      if (!Number.isFinite(sfx.at) || sfx.at < 0) {
        issues.push(issue('error', 'invalid_sfx_at', shotId, `音效 ${sfx.name || '(未命名)'} 時間點無效（${sfx.at}）`, '填入 ≥ 0 的秒數'));
      } else if (Number.isFinite(dur) && sfx.at >= dur) {
        issues.push(
          issue(
            'error',
            'sfx_outside_shot',
            shotId,
            `音效 ${sfx.name || '(未命名)'} 排在 ${sfx.at}s，但該鏡 dur 僅 ${dur}s，成片會直接被切掉`,
            `把 at 往前移到 ≤ ${(Math.max(0, dur - 0.5)).toFixed(2)}s，或加 hold 延長畫面`,
          ),
        );
      } else if (i === shots.length - 1 && Number.isFinite(dur) && dur - sfx.at < TAIL_SFX_MARGIN_SECONDS) {
        issues.push(
          issue(
            'warn',
            'tail_sfx_tight',
            shotId,
            `最後一鏡音效 ${sfx.name || '(未命名)'} 在 ${sfx.at}s，距離鏡尾僅 ${(dur - sfx.at).toFixed(2)}s`,
            '收尾重音建議比鏡尾早至少 0.45–0.5s，或搭配 hold: 0.6–0.9 讓音效完整響完',
          ),
        );
      }
    }

    // 9:16 Safe-Zone 焦點檢查（push + anchor）
    if (Array.isArray(shot.anchor) && shot.anchor.length === 2) {
      const [ax, ay] = shot.anchor.map(Number);
      if (Number.isFinite(ax) && Number.isFinite(ay)) {
        if (ax < SAFE_ZONE.minX || ax > SAFE_ZONE.maxX || ay < SAFE_ZONE.minY || ay > SAFE_ZONE.maxY) {
          issues.push(
            issue(
              'warn',
              'anchor_outside_safe_zone',
              shotId,
              `推近焦點 anchor=[${ax}, ${ay}] 超出 9:16 Shorts 介面安全區（x: 0.07–0.84, y: 0.09–0.72）`,
              '右側會被按讚／留言／分享按鈕遮擋，底部 28% 會被標題區遮擋；調整構圖或 anchor 進安全區內',
            ),
          );
        }
      }
    }

    // 鑰匙聲反應鏡過長檢查（《闖禍小浣熊》實戰教訓）
    if (
      series === 'raccoon-mischief' &&
      Number.isFinite(dur) &&
      dur > 1.2 &&
      (sfxList.some((s) => /keys?/i.test(s.name)) || /key/i.test(shotId))
    ) {
      issues.push(
        issue(
          'warn',
          'raccoon_key_reaction_slow',
          shotId,
          `《闖禍小浣熊》鑰匙聲反應鏡 dur=${dur}s 超過 1.2s`,
          '2026-11-04 雙人笑點審核實證：鑰匙聲呆臉反應超過 1 秒就會冷掉，建議壓在 0.6–0.8s',
        ),
      );
    }

    // 以下為 spec 模式的 Prompt 與角色檢查
    if (mode === 'spec') {
      const chars = Array.isArray(shot.chars) ? shot.chars : [];
      if (chars.length > 1 && !shot.allow_multi_char) {
        issues.push(
          issue(
            'error',
            'multi_char_frame',
            shotId,
            `違反單人框鐵律：chars 同時包含 ${chars.join(', ')}`,
            '拆成正反打單人鏡，或確認為必要遠景／對稱鏡後加上 allow_multi_char: true',
          ),
        );
      }

      if (series === 'influencer-piglet' && chars.length > 1) {
        issues.push(
          issue(
            'error',
            'piglet_no_two_shot',
            shotId,
            `《網美小豬》鐵律禁止粉粉與水豚同框（chars: ${chars.join(', ')}）`,
            '小豬與水豚必須拆開單人鏡或由遠景＋成品照角落破綻交代，絕不可同框',
          ),
        );
      }

      if (Object.keys(intros).length > 0) {
        for (const ch of chars) {
          if (!Object.hasOwn(intros, ch)) {
            issues.push(
              issue('error', 'unknown_char', shotId, `角色 "${ch}" 未定義在 intros 裡`, `在 intros 補上 "${ch}" 的系列定妝錨點`),
            );
          }
        }
      }

      const ff = typeof shot.ff === 'string' ? shot.ff : '';
      const clip = typeof shot.clip === 'string' ? shot.clip : '';
      const combined = `${ff}\n${clip}`;

      if (!ff.trim()) {
        issues.push(issue('error', 'missing_ff', shotId, '缺少首格英文提示詞 ff', '補上英文首格描述（景別＋封閉背景＋角色造型與表情）'));
      }
      if (!clip.trim() && !shot.still) {
        issues.push(issue('error', 'missing_clip', shotId, '缺少片段英文提示詞 clip', '補上單一明確動作軌跡與收尾運鏡句，或標記 still: true'));
      }

      // 畫外伸手＋同框主角（高風險分身／多手）
      if (chars.length >= 1 && OFFSCREEN_REACH_RE.test(combined)) {
        issues.push(
          issue(
            'error',
            'offscreen_hand_with_subject',
            shotId,
            '同框已有主角又寫「畫外伸手進入」（reaches in），極易長出分身或多一隻懸空手',
            '改拆成獨立的純道具特寫鏡（chars: []）或改用正反打鏡頭',
          ),
        );
      }

      // 陷阱 1：人手／手指
      if (POSITIVE_HUMAN_LIMB_RE.test(combined)) {
        issues.push(
          issue(
            'error',
            'human_limb_prompt',
            shotId,
            'Prompt 正面提及人類手／手指／手臂（human hand/finger/arm）',
            '零台詞動物世界嚴禁人類肢體；改寫為 two furry front paws, no human fingers',
          ),
        );
      }
      if (chars.length > 0 && HOLDING_PROP_RE.test(combined) && !ANIMAL_PAW_RE.test(combined)) {
        issues.push(
          issue(
            'warn',
            'holding_without_paws',
            shotId,
            '出現 holding/grasping 拿道具但未明寫 furry paws',
            '盡量改放桌上／胸口，若必拿請明寫 two furry front paws, no human fingers',
          ),
        );
      }

      // 陷阱 2：偽裝／結果造型漏寫 himself/herself
      if (chars.length > 0 && DISGUISE_CUE_RE.test(ff) && !SELF_ANCHOR_RE.test(ff)) {
        issues.push(
          issue(
            'warn',
            'disguise_missing_self_anchor',
            shotId,
            '首格涉及偽裝或特殊造型，但未寫 himself / herself',
            '明寫 "<角色> the <動物> himself/herself is..."，避免 AI 把真物件畫在角色旁邊',
          ),
        );
      }

      // 陷阱 3：背景路人（否定句 no people 或開放場所缺封閉牆面）
      if (NEGATIVE_PEOPLE_RE.test(ff)) {
        issues.push(
          issue(
            'warn',
            'negative_people_prompt',
            shotId,
            'ff 使用否定句 "no people / no humans"，生圖模型常忽略否定詞反而畫出人',
            '改為正面封閉背景描述：directly behind him/her is a solid plain wall, empty room',
          ),
        );
      }
      if (CROWD_PRONE_ENV_RE.test(ff) && !ENCLOSED_BG_RE.test(ff)) {
        issues.push(
          issue(
            'warn',
            'open_background_risk',
            shotId,
            '場景（辦公室／街道／停車場／咖啡廳等）未寫明封閉實牆或空場景，容易冒出人類路人',
            '加上 solid plain wall directly behind, no cubicles, empty room 或高牆／圍欄',
          ),
        );
      }

      // 陷阱 4：假字、Logo、浮水印
      if (FORBIDDEN_PRINT_RE.test(combined)) {
        issues.push(
          issue(
            'error',
            'forbidden_print_keyword',
            shotId,
            '出現高風險文字／Logo 詞（magazine cover / watermark / brand logo）',
            '刪除該詞，改用純視覺燈光與構圖描述並加 plain, unbranded, no text, no logos',
          ),
        );
      }
      if (TEXT_PRONE_PROP_RE.test(ff) && !UNBRANDED_GUARD_RE.test(ff)) {
        issues.push(
          issue(
            'warn',
            'prop_missing_unbranded_guard',
            shotId,
            '首格出現筆電／手機／時鐘／書籍／圖表／包裝袋等易長亂碼道具，卻未加 unbranded/plain/no text 防護',
            '加上 plain, unbranded, blank, no logos, no text, no numbers',
          ),
        );
      }

      // 陷阱 5：H3 首格錨點與運鏡結尾
      if (clip.trim() && !shot.still) {
        if (engine === 'h3' && !/<Picture\s*1>/i.test(clip)) {
          issues.push(
            issue(
              'warn',
              'h3_missing_picture1',
              shotId,
              'H3 模式的 clip 未帶 <Picture 1> 錨點',
              '開頭寫 "The <動物> shown in <Picture 1> ..." 鎖定首格外觀',
            ),
          );
        }
        if (engine !== 'h3' && /<Picture\s*1>/i.test(clip)) {
          issues.push(
            issue(
              'warn',
              'flow_has_picture1_token',
              shotId,
              `${engine.toUpperCase()} 模式的 clip 殘留 H3 專用標記 <Picture 1>`,
              '改用 export-flow 轉成自然英文主體描寫，避免 Veo 誤讀角括號標記',
            ),
          );
        }
        if (!CAMERA_ENDING_RE.test(clip)) {
          issues.push(
            issue(
              'warn',
              'clip_missing_camera_sentence',
              shotId,
              'clip 結尾缺少明確運鏡句',
              '句尾加上 "The camera holds a static shot." 或明確慢推／拉遠句',
            ),
          );
        }
      }

      // 陷阱 6：露臉角色閉嘴與禁用模糊笑詞
      if (chars.length > 0 && clip.trim() && !shot.still && !CLOSED_MOUTH_RE.test(clip)) {
        issues.push(
          issue(
            'warn',
            'missing_closed_mouth_guard',
            shotId,
            '有主角露臉的動態鏡，clip 未加閉嘴防護句（易被模型畫成開口笑或像在講話）',
            '加上 "His/Her lips remain closed."（嚴肅／慌張鏡再補 "No smile at any moment."）',
          ),
        );
      }
      if (AMBIGUOUS_SMILE_RE.test(combined)) {
        issues.push(
          issue(
            'warn',
            'ambiguous_smile_word',
            shotId,
            '使用模糊情緒詞（rueful / wry smile / smirk），模型常畫成開心大笑',
            '改寫為具體五官部位：ears flattened back, brows pulled down, eyes wide, lips pressed tightly closed',
          ),
        );
      }
    }
  }

  // 全集片長檢查
  if (shots.length > 0) {
    if (totalDuration < HARD_DURATION.min || totalDuration > HARD_DURATION.max) {
      issues.push(
        issue(
          'error',
          'total_duration_out_of_range',
          null,
          `全集總長 ${totalDuration.toFixed(2)}s 超出硬範圍 ${HARD_DURATION.min}–${HARD_DURATION.max}s`,
          '調整各鏡 dur（目標黃金區間 11–16s），砍短拖沓反應鏡或補定格 hold',
        ),
      );
    } else if (totalDuration < GOLDEN_DURATION.min || totalDuration > GOLDEN_DURATION.max) {
      issues.push(
        issue(
          'warn',
          'total_duration_outside_golden',
          null,
          `全集總長 ${totalDuration.toFixed(2)}s 在硬範圍內，但超出黃金區間 ${GOLDEN_DURATION.min}–${GOLDEN_DURATION.max}s`,
          '11–16s 最容易衝出 >100% 重播留存，可檢視是否能再精簡反應鏡',
        ),
      );
    }

    if (shots.length < 4 || shots.length > 9) {
      issues.push(
        issue('warn', 'shot_count_unusual', null, `全集共 ${shots.length} 鏡，建議落在 5–7 鏡（黃金五拍）`, '確認是否缺少升級／反轉拍或過度切碎'),
      );
    }

    if (!hasMusicOff) {
      issues.push(
        issue(
          'warn',
          'missing_music_off',
          null,
          '全集沒有任何一鏡設定 music_off: true（抽掉背景音樂的喜劇留白）',
          '建議在轉折凝視鏡或結尾定格鏡加上 "music_off": true 強化笑點力道',
        ),
      );
    }

    const lastShot = shots.at(-1);
    if (lastShot && Number(lastShot.hold ?? 0) < 0.4 && !lastShot.seamless_loop) {
      issues.push(
        issue(
          'warn',
          'missing_ending_hold',
          lastShot.id || `shot_${shots.length}`,
          '最後一鏡沒有設定 hold ≥ 0.4s（也未標記 seamless_loop: true）',
          '建議加 "hold": 0.6–0.9 停在最強反應格讓觀眾看懂笑點，或刻意設計無縫迴圈並標記 seamless_loop: true',
        ),
      );
    }
  }

  // spec 模式：縮圖與中繼資料檢查
  if (mode === 'spec') {
    if (!doc.thumb) {
      issues.push(issue('error', 'missing_thumb', null, '缺少縮圖指定鏡 thumb', '指定最誇張或反轉前最強表情的 shot id 作為 thumb'));
    } else if (shotIds.size > 0 && !shotIds.has(doc.thumb)) {
      issues.push(issue('error', 'invalid_thumb', null, `thumb="${doc.thumb}" 不存在於 shots 鏡號清單中`, '改為有效的 shot.id'));
    }

    if (typeof doc.title === 'string') {
      const titleLen = [...doc.title.trim()].length;
      if (!titleLen || titleLen > 100 || /[<>]/.test(doc.title)) {
        issues.push(issue('error', 'invalid_title', null, `title 格式不符（長度 ${titleLen}，不可含 < > 且需 1–100 字元）`, '修正為 1–100 字元的純情境鉤子標題'));
      }
      for (const re of CALLS_TO_ACTION) {
        const hit = re.exec(doc.title);
        if (hit) {
          issues.push(issue('error', 'title_has_cta', null, `title 含有禁止的呼籲互動詞「${hit[0]}」`, '拿掉按讚／訂閱／小鈴鐺等字眼'));
        }
      }
    }

    if (typeof doc.description === 'string' && !AI_DISCLOSURE_RE.test(doc.description)) {
      issues.push(
        issue('warn', 'description_missing_ai_disclosure', null, 'description 未見 AI 生成揭露說明', '補上「本片畫面、配樂由 AI 生成。」（上架亦須設 synthetic_media: true）'),
      );
    }

    if (Array.isArray(doc.tags) && doc.tags.length > 15) {
      issues.push(issue('error', 'too_many_tags', null, `tags 有 ${doc.tags.length} 個，超過上限 15 個`, '精簡至 5–15 個核心關鍵字'));
    }
  }

  const errors = issues.filter((item) => item.severity === 'error').length;
  const warnings = issues.filter((item) => item.severity === 'warn').length;
  return {
    ok: errors === 0,
    mode,
    series,
    engine,
    summary: {
      shots: shots.length,
      totalDuration: Number(totalDuration.toFixed(2)),
      errors,
      warnings,
    },
    issues,
  };
}

/**
 * 將 H3 格式的 clip 提示詞轉寫為 Google Flow (Veo 3.1 Frames-to-Video) 提示詞。
 */
export function rewriteClipForFlow(clip = '') {
  const cleaned = String(clip)
    .replace(/\bshown\s+in\s*<Picture\s*\d+>/gi, 'from the starting frame')
    .replace(/\bin\s*<Picture\s*\d+>/gi, 'in the starting frame')
    .replace(/<Picture\s*\d+>/gi, 'the starting frame')
    .replace(/\s+/g, ' ')
    .trim();
  const base = cleaned.endsWith('.') ? cleaned : `${cleaned}.`;
  return `${base} ${FLOW_AUDIO_GUARDRAIL}`;
}

/**
 * 將 <slug>.json 轉出成可直接貼進 Google Flow (Veo 3.1 Portrait 9:16) 的 Markdown 交接單。
 */
export function exportFlowPromptSheet(doc) {
  const slug = doc.slug || 'untitled-short';
  const series = detectSeries(slug);
  const seriesName = series ? SERIES_DIRS[series] : '<系列名稱>';
  const shots = Array.isArray(doc.shots) ? doc.shots : [];
  const total = shots.reduce((acc, s) => acc + (Number(s.dur) || 0), 0);

  const lines = [
    `# Google Flow（Veo 3.1）製作提示詞單：${slug}`,
    '',
    `- **標題**：${doc.title || '（未填）'}`,
    `- **目標總長**：${total.toFixed(1)}s（${shots.length} 鏡）｜**畫幅**：Portrait 9:16（\`1080×1920\`）`,
    `- **縮圖建議鏡**：\`${doc.thumb || '（未指定）'}\``,
    `- **雲端交接資料夾**：`,
    `  - 上傳首格（Frames）：\`AI/備份/Shorts/${seriesName}/${slug}/flow-inputs/\``,
    `  - 下載成片（Clips）：\`AI/備份/Shorts/${seriesName}/${slug}/flow-clips/\`（檔名請存成 \`<鏡號>.mp4\`）`,
    '- **Flow 操作設定**：建立新專案 → 選 **Frames to Video**（上傳對應首格）→ 比例選 **Portrait (9:16)** → 模型選 **Veo 3.1 Fast**（重點表情可升 Quality）。',
    '- **音訊提醒**：每段 Flow Prompt 已強制加入無台詞防護句；進 `edit.py` 組裝時預設 `-an` 靜音軌，再統一鋪系列 BGM、`music_off` 留白與物理音效。',
    '',
    '---',
    '',
  ];

  for (let i = 0; i < shots.length; i += 1) {
    const s = shots[i];
    const id = s.id || `s${String(i + 1).padStart(2, '0')}`;
    const sfxText = normalizeSfxList(s.sfx)
      .map((x) => `${x.name}@${x.at}s`)
      .join(', ') || '無';
    const flags = [
      `剪輯目標：in=${s.in ?? 0.2}s, dur=${s.dur}s`,
      s.hold ? `hold=${s.hold}s` : null,
      s.music_off ? 'music_off=True' : null,
      s.still ? '靜圖慢推（免進 Flow 生片）' : null,
      `音效：${sfxText}`,
    ]
      .filter(Boolean)
      .join(' ｜ ');

    lines.push(`## ${i + 1}. \`${id}\`${s.chapter ? `（${s.chapter}）` : ''}`);
    lines.push(`- **機位**：${s.camera || 'Locked'} ｜ **角色**：${(s.chars || []).join(', ') || '無（純道具）'}`);
    lines.push(`- **後製參數**：${flags}`);
    lines.push(`- **首格圖檔**：\`flow-inputs/${id}.png\`（${SAFE_ZONE_FRAMING_NOTE}）`);
    lines.push('');
    lines.push('**首格提示詞（Image / First Frame）：**');
    lines.push('```text');
    lines.push(`${(s.ff || '').trim()} ${SAFE_ZONE_FRAMING_NOTE}`.trim());
    lines.push('```');
    lines.push('');
    if (!s.still) {
      lines.push(`**Flow 動態提示詞（輸出存為 \`flow-clips/${id}.mp4\`）：**`);
      lines.push('```text');
      lines.push(rewriteClipForFlow(s.clip || ''));
      lines.push('```');
      lines.push('');
    }
  }

  return `${lines.join('\n')}\n`;
}

function median(values) {
  const sorted = [...values].sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 === 1 ? sorted[mid] : Number(((sorted[mid - 1] + sorted[mid]) / 2).toFixed(2));
}

/**
 * 彙整階段一三位獨立評審的盲評 JSON，核對八軸加總、計算中位數與滑走陷阱並排序開拍優先序。
 */
export function aggregateBlindReviews(reviews, { threshold = 70 } = {}) {
  if (!Array.isArray(reviews) || reviews.length < 2) {
    throw new Error('至少需要 2 份獨立評審盲評 JSON（標準為 3 位評審）');
  }

  const validationErrors = [];
  const byWork = new Map();

  for (const rev of reviews) {
    const judge = String(rev?.judge || 'unknown');
    const works = Array.isArray(rev?.works) ? rev.works : [];
    for (const entry of works) {
      const work = String(entry?.work || '');
      if (!work) continue;
      const scores = entry.scores || {};
      let sum = 0;
      for (const [axis, max] of Object.entries(RUBRIC_MAX)) {
        const val = Number(scores[axis]);
        if (!Number.isFinite(val) || val < 0 || val > max) {
          validationErrors.push(`${judge} / 作品 ${work}：軸 ${axis}=${scores[axis]} 超出 0–${max}`);
        } else {
          sum += val;
        }
      }
      if (Number(entry.total) !== sum) {
        validationErrors.push(`${judge} / 作品 ${work}：回報 total=${entry.total} 與八軸加總 ${sum} 不符（改採加總值 ${sum}）`);
      }

      if (!byWork.has(work)) {
        byWork.set(work, { work, judgeScores: {}, totals: [], scrollAways: [], fixes: [] });
      }
      const bucket = byWork.get(work);
      bucket.judgeScores[judge] = sum;
      bucket.totals.push(sum);
      if (entry.would_scroll_away_at) {
        bucket.scrollAways.push({ judge, shot: String(entry.would_scroll_away_at) });
      }
      if (Array.isArray(entry.fixes)) {
        for (const fix of entry.fixes) bucket.fixes.push(`[${judge}] ${fix}`);
      }
    }
  }

  const results = [...byWork.values()].map((item) => {
    const med = median(item.totals);
    const min = Math.min(...item.totals);
    const max = Math.max(...item.totals);

    // 同一鏡被 >= 2 位評審標記滑走 → 強制退修
    const shotScrollCounts = new Map();
    for (const s of item.scrollAways) {
      shotScrollCounts.set(s.shot, (shotScrollCounts.get(s.shot) || 0) + 1);
    }
    const scrollTraps = [...shotScrollCounts.entries()]
      .filter(([, count]) => count >= 2)
      .map(([shot, count]) => `${shot} (${count}位滑走)`);

    const passed = med >= threshold && scrollTraps.length === 0;
    const reason = !passed
      ? [med < threshold ? `中位數 ${med} < ${threshold}` : null, scrollTraps.length ? `滑走陷阱：${scrollTraps.join(', ')}` : null]
          .filter(Boolean)
          .join('；')
      : '過關，可進入階段二技術審稿';

    return {
      work: item.work,
      median: med,
      min,
      max,
      judgeScores: item.judgeScores,
      scrollAways: item.scrollAways,
      scrollTraps,
      passed,
      reason,
      fixes: item.fixes,
    };
  });

  // 排序：過關優先 → 中位數高到低 → 最低分高到低
  results.sort((a, b) => Number(b.passed) - Number(a.passed) || b.median - a.median || b.min - a.min);

  return {
    threshold,
    judges: reviews.map((r) => String(r?.judge || 'unknown')),
    validationErrors,
    results,
  };
}

function formatCheckText(report, filePath) {
  const lines = [
    `[${report.ok ? 'PASS' : 'FAIL'}] ${filePath}`,
    `  模式: ${report.mode} | 系列: ${report.series ?? '未登記／通用'} | 引擎: ${report.engine} | 鏡數: ${report.summary.shots} | 總長: ${report.summary.totalDuration}s | 錯誤: ${report.summary.errors} | 警告: ${report.summary.warnings}`,
  ];
  for (const item of report.issues) {
    const tag = item.severity === 'error' ? 'ERROR' : 'WARN ';
    const where = item.shot ? `[${item.shot}] ` : '[全集] ';
    lines.push(`  ${tag} (${item.code}) ${where}${item.message}`);
    lines.push(`        → 建議：${item.fix}`);
  }
  return lines.join('\n');
}

function formatBlindMarkdown(agg) {
  const lines = [
    `# 階段一盲評彙整表（開拍門檻：中位數 ≥ ${agg.threshold}，且無 ≥ 2 位同鏡滑走）`,
    '',
    '| 排序 | 作品 | 中位數 | 最低／最高 | 各評審分數 | 滑走標記 | 判定 |',
    '| --- | --- | --- | --- | --- | --- | --- |',
  ];
  agg.results.forEach((r, idx) => {
    const perJudge = Object.entries(r.judgeScores)
      .map(([j, s]) => `${j}: ${s}`)
      .join(' / ');
    const scrolls = r.scrollAways.length ? r.scrollAways.map((s) => `${s.judge}@${s.shot}`).join(', ') : '無';
    lines.push(`| ${idx + 1} | ${r.work} | **${r.median}** | ${r.min} / ${r.max} | ${perJudge} | ${scrolls} | ${r.passed ? '✅ ' : '❌ '}${r.reason} |`);
  });
  if (agg.validationErrors.length) {
    lines.push('', '## 格式／加總核對提醒');
    for (const e of agg.validationErrors) lines.push(`- ${e}`);
  }
  return lines.join('\n');
}

export function main(argv = process.argv.slice(2)) {
  const cmd = argv[0];
  if (!cmd || cmd === '--help' || cmd === '-h' || cmd === 'help') {
    console.log(
      [
        'Shorts 零台詞短劇前檢、Google Flow 轉寫與盲評彙整工具',
        '  check <spec-or-plan.json> [--engine h3|flow|veo] [--json] [--strict]',
        '  export-flow <spec.json> [--out flow-prompts.md]',
        '  score-blind <judge1.json> <judge2.json> [judge3.json ...] [--threshold 70] [--json]',
      ].join('\n'),
    );
    return 0;
  }

  const { values, positionals } = parseArgs({
    args: argv.slice(1),
    allowPositionals: true,
    options: {
      engine: { type: 'string', default: 'h3' },
      mode: { type: 'string' },
      json: { type: 'boolean', default: false },
      strict: { type: 'boolean', default: false },
      out: { type: 'string' },
      threshold: { type: 'string', default: '70' },
    },
  });

  if (cmd === 'check') {
    if (!positionals.length) throw new Error('請指定至少一個 <spec-or-plan.json> 檔案');
    let failed = false;
    const reports = [];
    for (const file of positionals) {
      const doc = JSON.parse(readFileSync(path.resolve(file), 'utf8'));
      const report = preflightShort(doc, { engine: values.engine, mode: values.mode });
      reports.push({ file, ...report });
      if (!report.ok || (values.strict && report.summary.warnings > 0)) failed = true;
      if (!values.json) console.log(formatCheckText(report, file));
    }
    if (values.json) console.log(JSON.stringify(reports.length === 1 ? reports[0] : reports, null, 2));
    return failed ? 1 : 0;
  }

  if (cmd === 'export-flow') {
    if (!positionals[0]) throw new Error('請指定 <spec.json>');
    const doc = JSON.parse(readFileSync(path.resolve(positionals[0]), 'utf8'));
    const report = preflightShort(doc, { engine: 'flow', mode: 'spec' });
    if (!report.ok) {
      console.error(formatCheckText(report, positionals[0]));
      if (values.strict) return 1;
    }
    const md = exportFlowPromptSheet(doc);
    if (values.out) {
      writeFileSync(path.resolve(values.out), md, 'utf8');
      console.log(`已輸出 Google Flow 提示詞單至 ${values.out}`);
    } else {
      console.log(md);
    }
    return 0;
  }

  if (cmd === 'score-blind') {
    if (positionals.length < 2) throw new Error('請提供至少 2 份盲評 JSON 檔案');
    const reviews = positionals.map((f) => JSON.parse(readFileSync(path.resolve(f), 'utf8')));
    const agg = aggregateBlindReviews(reviews, { threshold: Number(values.threshold) });
    if (values.json) console.log(JSON.stringify(agg, null, 2));
    else console.log(formatBlindMarkdown(agg));
    return agg.results.some((r) => r.passed) ? 0 : 1;
  }

  throw new Error(`未知子指令：${cmd}`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  try {
    process.exitCode = main();
  } catch (err) {
    console.error(err?.message || String(err));
    process.exitCode = 1;
  }
}
