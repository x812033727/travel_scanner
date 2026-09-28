// 《三針》的來源拆成七個檔案寫（setting、四篇、包裝），這裡組成 build.mjs 讀的那一個物件。
import head from "./setting.mjs";
import c1 from "./chapter-1.mjs";
import c2 from "./chapter-2.mjs";
import c3 from "./chapter-3.mjs";
import c4 from "./chapter-4.mjs";
import tail from "./packaging.mjs";

export default { ...head, chapters: [c1, c2, c3, c4], ...tail };
