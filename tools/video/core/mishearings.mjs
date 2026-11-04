// The words the audio check has misheard on this channel, each with the wording that passed
// (the table in script-writing.md §給 TTS 唸的稿子 also says what each was heard as). The check
// transcribes the synthesized voice and compares it with the script; two tutorials on
// 2026-10-09 had 13 and 19 of 151 lines flagged on their first check, and a line that was only
// recorded again was flagged again. Sent to the slides writer and listener (register.mjs
// HEARD_RULES, whose text is hash-pinned: reordering or editing a pair reruns those stages),
// and warned on by lint before any narration is paid for (mishearingsIn below).
export const MISHEARD_WORDS = [
  ["實跑", "實際跑過"],
  ["行程", "執行中的程式"],
  ["讀檔", "讀取檔案"],
  ["數什麼", "要數什麼"],
  ["擋呼叫的", "負責擋下呼叫的"],
  ["窗格", "畫面上的介面"],
  ["沒人接手", "沒有人替它處理"],
  ["界線", "原則"],
  ["餵假事件", "送假事件進去"],
  ["印出", "顯示的是"],
  ["放行", "讓它通過"],
  ["無介面", "不開畫面的"],
  ["那一欄", "這個欄位"],
  ["沒接的那次", "沒有接上的那一次"],
  ["測試是紅的", "測試沒有通過"],
  ["有檔、沒檔", "有 CLAUDE.md、沒有 CLAUDE.md（說出檔名）"],
  ["有檔案", "有 CLAUDE.md（說出檔名）"],
  ["被叫到", "被呼叫"],
  ["含糊的那一份", "寫得含糊的那一份"],
  ["指到", "對應"],
  ["搬去 hook", "改用 hook 來做"],
  ["本機", "這台機器"],
  ["交辦", "把工作交出去"],
  ["指定前景", "指定不放到背景"],
  ["背景送回來的", "晚一點才送回來的"],
  ["是主對話自己", "是由主對話寫出來的"],
  ["報告檔", "那份報告"],
  ["沒有量", "沒有量到"],
  ["呼叫進來", "有呼叫進來的時候"],
  ["九行", "一共九行"],
  ["唯讀工具", "只能讀取的工具"],
  ["互動式 session", "互動式的畫面"],
  ["握手那一則", "握手的那一則訊息"],
  ["先比禁止", "先比對禁止規則"],
  ["三條禁止", "禁止規則有三條"],
  ["那一次，", "在這一次執行裡，"],
  ["位址", "網址（指的是 URL 時）"],
  ["多一行", "會多出一行"],
  ["執行了。", "被執行了。"],
  ["對上就", "對上了就"],
  ["四項", "那四項"],
  ["同一句要求", "同樣的一句要求"],
  ["同事也要", "你的同事也要"],
  ["怎麼搬？", "怎麼搬過去？"],
  ["帶上旗標", "加上載入外掛的旗標"],
  ["用同一個旗標", "加上同一個旗標"],
  ["這支 hook", "這一支 hook"],
  ["拿一句會用到", "拿一個會用到"],
  ["只載入外掛", "只有載入外掛"],
  ["沒有載入的三次", "沒有載入外掛的那三次"],
  ["拼錯的鍵", "拼錯的欄位"],
  ["不問 Claude", "不用問 Claude"],
  ["那一筆的清單", "那一筆紀錄裡的清單"],
  ["尺取十一", "那把尺取十一"],
  ["比尺大", "比那把尺大"],
  ["在尺以內", "在誤差範圍以內"],
  ["什麼時候進請求", "是什麼時候送進去的"],
  ["第一個請求比基準", "第一個請求的用量比基準"],
  ["影片量到的", "影片實際量到的"],
  ["這些數字怎麼量", "這些數字是怎麼量出來的"],
  ["MCP 那一列", "看 MCP 這一列的時候"],
  ["延後載入一起", "延後載入的機制一起"],
  ["直接載入", "一開始就載入"],
  ["七行就", "一共七行，就"],
  ["交出 subagent", "把工作交給 subagent"],
  ["那支 hook", "同一支 hook"],
  ["只是為了量。", "只是為了量測用的。"],
  ["延後載入，每多", "用延後載入的時候，每多"],
  ["延後多出來的", "延後載入多出來的"],
  ["延後載入的這一次", "用延後載入的這一次"],
  ["延後載入的減預設的", "用延後載入的，減預設的"],
  ["延後的到底是什麼", "被延後的到底是什麼"],
  ["只開八個內建工具的練習專案", "練習專案只開八個內建工具"],
  ["只多六十九", "多出來的是六十九"],
  ["多出來的只有名稱", "多出來的只是名稱而已"],
  ["只接指定的伺服器", "也只連接指定的伺服器"],
  ["沒接伺服器的", "沒有接伺服器的"],
  ["沒接、接上", "沒有接伺服器、接上"],
  ["同一個工具數", "工具數量相同的兩次"],
  ["推回零個", "回推到零個"],
  ["定義合計", "工具定義加起來"],
  ["兩個、十個那兩級", "兩個和十個工具那兩次"],
  ["一開始就載入的那一次", "一開始就全部載入的那一次"],
  ["那一次重跑", "把這一次重新跑"],
  ["卻零個工具", "可是一個工具都沒有"],
];

// Longer phrases that contain a row's words and are fine: the row's own fix, or another word.
// A stretch one of these covers is blanked before the row is looked for.
const UNLESS = {
  // 行程 the row means is a running program; on a travel site it is mostly an itinerary, where
  // 「執行中的程式」 is the wrong advice, and 執行程式 only spans the two words.
  "行程": /執行程|排行程|行程[表單草規]|[天日遊趟份][的]?行程|(?:可用|旅遊|旅行|整份|這份|可驗收的|影響)行程/gu,
  "讀檔": /讀檔案/gu,
  "數什麼": /要數什麼/gu,
  "有檔、沒檔": /有檔案|沒檔案/gu,
  "本機": /日本機|本機場/gu,
  "沒有量": /沒有量到/gu,
  "呼叫進來": /有呼叫進來/gu,
  "九行": /共九行/gu,
  "執行了。": /被執行了。/gu,
  "四項": /那四項|[十百第]四項/gu,
  "同事也要": /的同事也要/gu,
  "延後載入的這一次": /用延後載入的這一次/gu,
  "含糊的那一份": /寫得含糊的那一份/gu,
  "尺取十一": /那把尺取十一/gu,
  "延後的到底是什麼": /被延後的到底是什麼/gu,
};

// Rows whose cell names two phrases, each looked for on its own.
const PHRASES = { "有檔、沒檔": ["有檔", "沒檔"] };

/** The phrases a row is looked for by. */
export function phrasesOf(written) {
  return PHRASES[written] ?? [written];
}

/**
 * The known mishearings a zh narration text contains, once per row: { written, instead, phrase }.
 * Warnings for the writer, never errors (core/lint.mjs): several are ordinary words that read
 * fine in another sentence, and the worker's lint gate must not start refusing old scripts.
 */
export function mishearingsIn(text) {
  const source = String(text ?? "");
  const found = [];
  for (const [written, instead] of MISHEARD_WORDS) {
    const unless = UNLESS[written];
    const visible = unless ? source.replace(unless, (match) => "\u0000".repeat(match.length)) : source;
    const phrase = phrasesOf(written).find((each) => visible.includes(each));
    if (phrase) found.push({ written, instead, phrase });
  }
  return found;
}
