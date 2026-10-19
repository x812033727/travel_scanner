# S08 fresh blind narrative and source check

Checked 2026-10-19. The blind pass read only `script.md` and the 13 questions printed by `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs narrative --slug curio-s08`. Its answers were frozen in `/tmp/curio-s08-fresh-blind.json` (SHA256 `b2925da43bcca10fce428ee60a7ef0506b529edfa44a6689d1479ee4f087f153`) before reading `research.md`, `claims.md`, or the fixed primary transcriptions. Because four answers are **no**, I did **not** invoke `narrative --answers`.

## Files reviewed

| File | SHA256 |
| --- | --- |
| `script.md` | `6f3a8c3fc98793d8b08888fb848762577aad8e6db6196ae4dcfe51fd69aa17a2` |
| `video.json` | `1c918c6c257aff28252247cf576e1e381bd46e052ce353ae8558c051711919ed` |
| `research.md` | `f21289bc2cafb9fc1abcc0e81e5aaa4b5fca2c372f2e65a83f19509707e8085e` |
| `claims.md` | `4b76209bff601cc16289dcbab5606d3667a9278f3fd663a2fc02bb1f230bd8a6` |

## Blind verdict

**9 yes, 4 no.** The exact 13 answers and line evidence are in `/tmp/curio-s08-fresh-blind.json`.

| Criterion | Verdict | Main evidence in `script.md` |
| --- | --- | --- |
| `scene_first` | yes | 9–21: dated scene at 斜谷, army carrying grain, observer at the covered device. |
| `no_spoiler` | **no** | 21 reveals the later finding that the historical text has no drawing (chapter 5, 205–337; especially 273); 29 also says wood ox was already used at 祁山 before the 231 entry at 55. |
| `one_line` | yes | After the preview, 43–203 moves 231 → 232 → 234; 205–397 pursues what the text, then the novel, can establish. |
| `no_toc` | **no** | 47 announces “先回到更早的祁山，看…”, a plan for what to tell next; 385 announces arranging the three annual records into a line. |
| `chapters_link` | **no** | 99 asks why wood ox was “completed” after prior use, but the next chapter's first sentence (105) only reports farming at 黃沙; the relevant entry waits until 109. The question at 379 is followed by a summary and method at 385, rather than a new answer. |
| `open_loops` | yes | Questions or turns recur at 25–41, 67, 99, 137, 163, 203, 241, 277, 305, 341, 359, and 389. |
| `payoffs` | yes | 67 → 75–91; 99 → 109–125; 137 → 143–155; 203 → 209–337; 341 → 347–375; 389 → 393–401. The evidence gap is explicitly given where no historical answer survives. |
| `no_recap` | **no** | 199 says supplies stayed tight; 385 restates that supplies kept chasing the army. The missing diagram/unique form has already been described at 273, 329, and 337 before the broad repeat at 393–397, without an explicit callback. |
| `chapters_are_events` | yes | Headings at 5, 43, 101, 139, 205, 343, and 381 name actions or discoveries. |
| `outro_no_next` | yes | 403–406 invites comments and a subscription only. |
| `opening_hooks` | yes | 25, 33, 37, and 41 leave later supply, walking, tongue operation, and history/fiction questions pending. |
| `one_thread` | yes | 25, 67–99, 137–195, 203–337, and 341–397 all pursue the transport device's practical role and what can be known about it. |
| `no_detour` | yes | The farming scene at 171–195 tests the device's supply role; 347–375 resolves the opening's later-novel question. |

## Independent fixed-text spot-check

I checked the local clone of Ancient-China-Books `sanguozhi` at commit `10a0b1ab3019d8821262f7402366d14fb4aaa102` (`OEBPS/Text/033.htm` and `035.htm`) and `sanguoyanyi` at commit `761813427eb5685c395804493f9fbd7ad8dc7d8d` (`OEBPS/Text/481.html`). These are fixed modern transcriptions, not a manuscript or recovered object; the novel page also interleaves 毛宗崗 commentary. The chronology matches the second `sanguozhi` transcription identified in `research.md` (local SHA256 `1180137e666366039465d794f24ab0d5dd83a70e844e9ec209afdd078c1b15b4`), which is another transcription of the same ancient text.

| Check | Primary text and result |
| --- | --- |
| 231 / 建興九年 | 〈後主傳〉 says “九年春二月，亮復出軍圍祁山，始以木牛運” and “夏六月，亮糧盡退軍.” Script 51–95 accurately pairs use and later shortage without calling wood ox useless. |
| 232 / 建興十年 | The next 〈後主傳〉 entry says “亮休士勸農於黃沙，作流馬木牛畢，教兵講武.” Script 105–137 treats 畢 as completion and leaves invention date, quantity, and revisions open; that boundary is justified by the prior year's wood ox use. |
| 234 / 建興十二年 | 〈後主傳〉 says “十二年春二月，亮由斜谷出，始以流馬運.” 〈諸葛亮傳〉 says he moved to 五丈原, “每患糧不繼,” then “分兵屯田,” with cultivators among 渭濱 residents and people at peace. Script 9–13 and 143–195 follows these entries, without claiming either the flowing horse or farming fed the entire army. |
| Chen Shou versus Pei quote | Chen Shou's main text says “木牛流馬，皆出其意”; Pei's annotation separately introduces “亮集載作木牛流馬法曰.” Script 209–229 keeps the authorship and description layers distinct and does not turn Pei into an eyewitness. |
| Wood ox tongue versus novel operation | The quoted 《諸葛亮集》 text says “舌著於腹” and later “垂者爲牛舌.” It does not say that twisting it stops a device. Chapter 102 of the later novel explicitly has soldiers “將木牛流馬口內舌頭扭轉，牛馬就不能行動,” then twist it back; soldiers cannot drag or lift the stopped devices, and disguised “神兵” deploy smoke. Script 249–253 and 347–375 preserves this distinction. |
| Ancient units and parts | The Pei quote has “特行者數十里，羣行者二十里,” “人行六尺，牛行四步,” and “載一歲糧，日行二十里.” The separate “流馬尺寸之數” has front/rear axle holes, “前後四脚,” and two square sacks, “每枚受米二斛三斗.” Script 261–329 does not convert these into modern mass, speed, wheel count, or a total supply capacity. |
| Mechanical form | The wood ox “一脚四足” and flowing horse “前後四脚” are in different paragraphs. The fixed transcription provides part names and measurements, not a checkable assembly drawing or a complete account of joint motion. Script 273 limits the no-drawing statement to this transcription; 321 and 337–401 appropriately refuse a unique original form. The stronger universal claim that no drawing ever existed is absent. |

**Source verdict:** No material conflict found in these sampled claims. The blockers are narrative: `no_spoiler`, `no_toc`, `chapters_link`, and `no_recap` at the line locations above. No paid media was launched, and no script or video file was edited.
