# Vietnamese independent review

| id or field | problem | current | suggested |
| --- | --- | --- | --- |
| 9e738a | Meaning: 不好解釋 means hard to explain; câu hỏi khó only says difficult. Restore that distinction, the strongest preference, the animation and comment request within 64 codepoints. | Bạn muốn làm hoạt hình câu hỏi khó nào nhất? Hãy bình luận. | Muốn làm hoạt hình về vấn đề khó giải thích nào nhất? Bình luận. |
| aa0639 | Cue order: source and SRT put not generating another nice image before actually fixing the typo; the translation reverses those clauses. | Bạn cần sửa được lỗi chữ thật sự, chứ không phải thử vận may lấy hình đẹp khác. | Bạn không cần thử vận may lấy hình đẹp khác, mà cần sửa được lỗi chữ thật sự. |
| 75368c | Cue order: source says explain the reason then stop, while the translation says stop then explain. Preserve the source instruction sequence. | Nhập điều kiện không hỗ trợ thì phải dừng và nêu lý do, không âm thầm vẽ thành bài khác. | Nhập điều kiện không hỗ trợ thì phải nêu lý do rồi dừng, không âm thầm vẽ thành bài khác. |
| 1de727 | Readability and precision: thu nhỏ xem trước bằng màn hình điện thoại is an awkward fragment and omits the specified width; restore the preview noun and phone-width check. | Thu nhỏ xem trước bằng màn hình điện thoại; xem tiêu đề đọc được, trọng tâm rõ không. | Thu bản xem trước về độ rộng điện thoại; xem tiêu đề đọc được, trọng tâm rõ không. |
| thumbnail:tag | Thumbnail: source AI 教學動畫 includes the teaching purpose; Hoạt hình AI omits it. Restore teaching in a short tag. | Hoạt hình AI | Hoạt hình AI để dạy học |

Verdict: ready after the five fixes.

Fixes by kind: meaning 1; facts 0; glossary 0; cue order 2; readability 1; budget 0; metadata 0; thumbnail 1.

Independently read all 101 final captions, all eight chapters, title, description, tags and all three thumbnail fields against the zh-TW script, slide data, claims, lexicon, six worksheet cue boundaries and all 107 timed SRT cues. The translator critique was not consulted. All original captions fit their hard max_chars by actual Unicode codepoints, and every proposed line correction also fits. Title: 55/90 characters. No Han, kana or Hangul appears in Vietnamese fields. Product names, date, URL, dice assumptions, ordered outcomes, six/five result counts, highlighted-cell updates, zh-TW-only practice language, silent MP4, designed rather than measured SRT timing and the Claude Motion disclaimer were checked.

Source-only observation, excluded from locale correction counts: claims.md c10 says the stills-only option was not evidenced and narration should ask AI to add it, but current video.json/SRT line 005752 still instructs using it. The Vietnamese follows the current source.
