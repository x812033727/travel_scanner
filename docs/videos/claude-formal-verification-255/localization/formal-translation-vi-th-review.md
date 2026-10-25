# Formal255 VI / TH translation: three-pass self-review

Current video SHA256: e6e87e77f069a574d6e1d7f47bf2e5be031eb8566bb2edb71defa24ae4c2b99f
Claims SHA256: 527048b6061d21f70e00475cc4790a46b0de6e536a37e8966402194a043fa9c6
Spoken/source worksheet freeze: 232b4495b433041007c039630ec517b7e0b4948c3cd7a5a47da6ecd88cae8a15; speech hash 8028c7320d9cab29.

Completed both105-caption worksheets,7chapters,title/description/tags,and all3 thumbnail fields. No merge, paid calls, backend/git/source changes, or independent review. Layout-only source change e6e87 does not change any of the105 worksheet sources.

Pass1: draft with glossary and source boundaries. Pass2: meaning/native-spoken critique. Pass3: numbers, C/type/negation/scope, source/Latin-term match and character budgets. Critique and fixes are saved below and in the JSON. This self-review is not the independent caption-review gate.

## vi

Title: Nghiên cứu kiểm chứng hình thức của Claude: số 255 nói gì về bảo đảm của chương trình?
Worksheet SHA256: 1641566392931e1e650e40474afc012365a0edd5cea264bf35cd25edcd17330f
Protected fields: resetting ONLY text fields reproduces initial worksheet SHA256 f1c1fb0569eaf65c265ceff435c9b1bc698fb5450a25f72589c61f1f006e9deb exactly.
Completed105lines/7chapters/allmetadata; within max_chars 105/105; unresolved 0.
Read-only native metadata composition: 3062 UTF-8bytes,10credits,7chapters,field-limit errors=[]; exact URL and4source paragraphs retained. This is not a merge or render-fit result.

### Glossary

- AI = AI
- Anthropic = Anthropic
- C = C
- Claude = Claude
- RISC-V = RISC-V
- Rocq = Rocq
- SAT = SAT
- loop = vòng lặp
- formal_verification = kiểm chứng hình thức
- proposition = mệnh đề
- unsigned_integer = số nguyên không dấu
- plain_build = bản thường
- public_release = bản công khai
- termination_proposition = mệnh đề kết thúc

Source-name rendering choices (worksheet glossary itself was not edited):

- Anthropic：Claude形式驗證研究 = Anthropic: nghiên cứu kiểm chứng hình thức của Claude
- Theorem公開proof：README = Theorem: README các proof công khai
- Theorem：證明來源與固定命題 = Theorem: nguồn gốc chứng minh và mệnh đề cố định
- Theorem：實際checker流程 = Theorem: quy trình bộ kiểm thực tế
- Theorem：agreement與halts命題 = Theorem: các mệnh đề agreement và halts
- C11委員會草案：整數提升與無號轉型 = Dự thảo ủy ban C11: nâng kiểu số nguyên và ép kiểu không dấu
- 本片原創C程式與完整結果 = Mã C tự viết và kết quả đầy đủ của video

### Saved critique and applied final fixes

| ID | Draft | Final | Fault / action |
|---|---|---|---|
| c8r2 | Cùng yêu cầu ấy, AI viết chứng minh rồi ai kiểm nhận? | Cùng yêu cầu ấy, AI viết chứng minh rồi ai nghiệm thu? | Natural acceptance-review terminology; preserve who checks AI proof. |
| 4rff | Nghiên cứu đổi yêu cầu kiểm thử thành mệnh đề kiểm được. | Nghiên cứu đổi yêu cầu kiểm thử ra mệnh đề kiểm tra được. | Replace compressed 'kiểm được' with natural verb; retain research attribution. |
| mfag | Nó lớn hơn sức chứa 8; lần này trả về từ chối đúng. | Nó vượt sức chứa 8; lần này trả về kết quả từ chối đúng. | Make returned rejection result grammatical; preserve capacity8 and correct outcome. |
| dfhy | Phiên bản sai chỉ cho qua thêm 255; phiên bản rộng chỉ nhận 0 đến 7. | Bản sai chỉ cho qua thêm 255; bản dùng kiểu rộng chỉ nhận 0 đến 7. | Make widened-type variant natural; preserve extra-only255 and legal0..7. |
| gtuj | Phiên bản sai tìm ra 255; phiên bản rộng không có phản ví dụ ấy. | Bản sai tìm ra 255; bản dùng kiểu rộng không tìm ra phản ví dụ ấy. | Consistent widened-type wording; preserve solver finding vs absent counterexample. |
| unr8 | Cách tìm xem các điều kiện đúng/sai có thể cùng thỏa này gọi là SAT mệnh đề. | Tìm xem các điều kiện đúng/sai có thể đồng thời thỏa mãn: đó là SAT mệnh đề. | Natural propositional satisfaction wording. |
| 6a2b | Hãy thêm điều kiện: đầu vào hợp lệ cũng buộc phải được nhận. | Ghi thêm điều kiện cần kiểm: đầu vào hợp lệ phải được nhận. | Explicitly preserve writing another condition TO CHECK, not merely adding a wish. |
| dkjy | Dòng này chỉ giao phán quyết chấp nhận; chương trình không ghi vào bộ đệm. | Dòng này chỉ đưa kết quả chấp nhận; chương trình không ghi vào bộ đệm dữ liệu. | Replace judicial 'verdict' wording; preserve guard-only/no-buffer-write. Keep DATA-buffer modifier explicitly; do not overstate about incidental I/O buffers. |
| 8ywa | Tôi ghi hai kết quả phiên bản rộng là 0: không nhận sai, không từ chối sai. | Tôi ghi hai kết quả bản dùng kiểu rộng là 0: không nhận sai, không từ chối sai. | Consistent widened-type wording, both zero outcomes retained. |
| xh98 | Dòng xét chấp nhận đã xong; phiếu còn dòng khác đợi kiểm việc trả về. | Dòng chấp nhận đã xong; phiếu còn dòng khác chờ nghiệm thu việc trả về. | Make inspection of the pending return record natural. |
| zg4q | Đối lại với chứng minh chính thức, phải cố định phiên bản chương trình, mệnh đề và mô hình hoạt động. | Đối chiếu phiếu với chứng minh hình thức: cố định phiên bản chương trình, mệnh đề và mô hình vận hành. | Formal proof is 'hình thức', not 'chính thức' meaning official. |
| uqde | Công cụ đối kết quả với mệnh đề cố định, rồi liệt kê các giả định đã dùng. | Công cụ đối chiếu kết quả với mệnh đề cố định, liệt kê các giả định đã dùng. | Natural compare verb; fixed proposition and used assumptions retained. |
| wi26 | Câu hỏi nghiệm thu mở đầu nằm ở việc nhân Rocq và công cụ kiểm mệnh đề, giả định. | Câu hỏi nghiệm thu mở đầu nằm ở việc nhân Rocq và công cụ kiểm tra mệnh đề, giả định. | Use full checking verb. |
| 7ip9 | Phiên bản công khai so hai bản dựng thường và có kiểm lỗi của cùng mã, không phải trước/sau sửa. | Bản công khai so sánh bản thường với bản kiểm lỗi của cùng chương trình, không phải trước/sau sửa. | Natural comparison; retain same program vs before/after distinction. |
| 6x7t | Trong mô hình hệ thống, đầu vào không khiến bản thường vượt hạn mức bộ nhớ. | Ở mô hình hệ thống, đầu vào không làm bản thường vượt mức bộ nhớ đã định. | Restore specified memory-budget qualifier while retaining system/input/plain premise. |
| 4nfp | Chỉ nói bản công khai này; không có nghĩa cả nghiên cứu bỏ qua kết thúc. | Chỉ nói bản công khai này; không có nghĩa cả nghiên cứu không xét kết thúc. | Use non-entailment rather than imputing neglect; retain release-only scope. |
| mj65 | Chạy lại thì đối phiên bản trước, rồi để kết quả dự kiến và thực tế cùng một dòng. | Chạy lại: trước hết kiểm phiên bản, rồi đặt kết quả dự kiến và thực tế cùng dòng. | Make first check version unambiguous, not previous-version reading. |
| edry | Như vậy không lấy mã đã sửa so với đáp án của mã cũ khác. | Tránh lấy mã đã sửa so với đáp án của một mã cũ khác. | Natural version-mismatch warning; preserve another old program. |
| rsx8 | Phiếu đã tách chấp nhận và trả về; chứng minh trong nghiên cứu Claude kiểm cùng yêu cầu sao? | Phiếu đã tách chấp nhận và trả về; chứng minh trong nghiên cứu Claude kiểm cùng loại yêu cầu sao? | Retain SAME KIND of requirement, not an identical local predicate. |
| 3u2q | Cả hai đều đối chiếu C chạy thật; chưa chạy bộ kiểm Rocq của nghiên cứu. | Cả hai đều đối chiếu với C chạy thật; chưa chạy bộ kiểm Rocq của nghiên cứu. | Restore natural comparison preposition; preserve no official Rocq run. |
| cawx | Nhân Rocq kiểm tra chứng minh khi biên dịch. | Nhân Rocq kiểm tra chứng minh do AI khi biên dịch. | Final named-term check caught omitted AI authorship; restored AI provenance within50chars. |
| zgkb | Phiếu thêm mô hình giải, viết cùng đầu vào thành 8 bit đúng hoặc sai. | Phiếu thêm mô hình để giải, viết cùng đầu vào thành 8 bit đúng hoặc sai. | Natural mathematical model-to-solve wording; preserve same8-bit input. |

### Remaining budget conflicts

None. All105VI lines are within the worksheet max_chars; actual dub/window fit remains unmeasured.

### Metadata critique

- Preserved audience conjunction rather than broadening to OR.
- Kept original self-written C and original SVG ownership explicit; no product-operation image claim.
- Restored formal-verification qualifier in thumbnail tag rather than shortening away its type.
- Kept title under100chars,7 chapter names about30chars, stressed255 and newline in thumbnail.

### Numeric / logical boundaries checked

- 2026-10-25 local demo date /10-22 official study publication distinct; clause date first.
- 0..255 input;8byte capacity+1byte terminator;0..7 accepted iff others rejected;bit vsbyte preserved.
- int256 then uint8 narrowing0; unsigned8/16 and complete widening/cast changes retained.
- sole extra255;256 input comparisons;deny-all symbolic not compiledC;0falseaccept/8falsereject.
- loop independent,0.25sec observation only;fixedinput256-step cycle vs actual fixed C returning256 /n+1.
- 239entry/123library official report vs60entry/25library publicrelease;onlythisrelease lacks halts proof.
- Rocq compile/kernel AI-proof attribution, wrapper fixed proposition/used assumptions, allowlist maintained.
- plain specified memory budget;finite observable records same allowed set;no entire-app certificate/no vendorRocq rerun.

## th

Title: งานวิจัยการทวนสอบเชิงรูปนัยของ Claude: ใช้ 255 เข้าใจสิ่งที่โปรแกรมรับประกัน
Worksheet SHA256: bb3a489d2305de9bf9d923d7492e6fde5ba54d89eac51c0e89b380d5f0f8c01e
Protected fields: resetting ONLY text fields reproduces initial worksheet SHA256 faa2744eaf91abd2f827f2b71124c6258fcadd8259cea5d70113d3dceda143b2 exactly.
Completed105lines/7chapters/allmetadata; within max_chars 97/105; unresolved 8.
Read-only native metadata composition: 4157 UTF-8bytes,10credits,7chapters,field-limit errors=[]; exact URL and4source paragraphs retained. This is not a merge or render-fit result.

### Glossary

- AI = AI
- Anthropic = Anthropic
- C = C
- Claude = Claude
- RISC-V = RISC-V
- Rocq = Rocq
- SAT = SAT
- loop = ลูป
- formal_verification = การทวนสอบเชิงรูปนัย
- proposition = ประพจน์
- unsigned_integer = จำนวนเต็มไร้เครื่องหมาย
- plain_build = รุ่นปกติ
- public_release = ฉบับสาธารณะ
- termination_proposition = ประพจน์การสิ้นสุด

Source-name rendering choices (worksheet glossary itself was not edited):

- Anthropic：Claude形式驗證研究 = Anthropic: งานวิจัยทวนสอบเชิงรูปนัยของ Claude
- Theorem公開proof：README = Theorem: README บทพิสูจน์ที่เผยแพร่
- Theorem：證明來源與固定命題 = Theorem: ที่มาบทพิสูจน์และประพจน์ที่กำหนด
- Theorem：實際checker流程 = Theorem: ขั้นตอนตัวตรวจจริง
- Theorem：agreement與halts命題 = Theorem: ประพจน์ agreement และ halts
- C11委員會草案：整數提升與無號轉型 = ร่างคณะกรรมการ C11: การยกระดับจำนวนเต็มและแปลงชนิดไร้เครื่องหมาย
- 本片原創C程式與完整結果 = โค้ด C ที่เขียนเองและผลครบของวิดีโอ

### Saved critique and applied final fixes

| ID | Draft | Final | Fault / action |
|---|---|---|---|
| 4rff | งานวิจัยแปลงเงื่อนไขทดสอบเป็นประพจน์ที่ตรวจได้ | งานวิจัยแปลงเกณฑ์ทดสอบเป็นประพจน์ตรวจได้ | Shorten via equivalent test-criteria phrase, keeping research/checkable proposition. |
| zfmi | ฉบับผิดแปลงความยาวรวมกลับเป็นจำนวนเต็มไร้เครื่องหมาย 8 บิต | ฉบับผิดแปลงผลรวมเป็นจำนวนเต็มไร้เครื่องหมาย 8 บิต | Total length is established; retain wrong-version unsigned8 cast without using unexplained C abbreviation. |
| uqde | เครื่องมือเทียบผลกับประพจน์ที่ตรึงไว้ แล้วแจกแจงสมมติฐานที่ใช้ | เครื่องมือเทียบผลกับประพจน์ที่กำหนด แล้วระบุสมมติฐานที่ใช้ | Natural shorter verbs; specified fixed proposition and used assumptions retained. |
| wi26 | คำถามตรวจรับตอนต้น อยู่ที่เคอร์เนล Rocq กับเครื่องมือตรวจประพจน์และสมมติฐาน | คำถามตรวจรับแรก อยู่ที่เคอร์เนล Rocq กับเครื่องมือตรวจประพจน์และสมมติฐาน | Equivalent opening-question wording; retain kernel/tool/proposition/assumptions. |
| u2xw | ฉันใช้โปรแกรมนับอีกตัวที่อิสระกรอกช่องคืนค่า อินพุตคือขีดจำกัดนับ | ฉันกรอกช่องคืนค่าด้วยโปรแกรมนับอิสระอีกตัว อินพุตคือขีดจำกัดการนับ | Natural independent-counter wording; retain first person, return field and input limit even if over budget. |
| 4nfp | นี่เฉพาะฉบับสาธารณะ ไม่ได้หมายความว่างานวิจัยทั้งหมดไม่จัดการการสิ้นสุด | นี่เฉพาะฉบับสาธารณะ ไม่ได้แปลว่างานวิจัยทั้งหมดไม่พิจารณาการสิ้นสุด | Natural research 'address/consider termination', not manage termination; preserve non-entailment/scope. |
| rsx8 | บันทึกแยกรับกับคืนค่าแล้ว งานวิจัย Claude ก็พิสูจน์ข้อกำหนดเดียวกันไหม? | บันทึกแยกรับกับคืนค่าแล้ว งานวิจัย Claude ก็พิสูจน์ข้อกำหนดแบบเดียวกันไหม? | Retain same KIND of requirement in the rhetorical comparison. |
| 3u2q | ทั้งสองเทียบกับ C รันจริง แต่ไม่ได้รันตัวตรวจ Rocq ในข่าว | ทั้งคู่เทียบกับผลรัน C จริง แต่ไม่ได้รันตัวตรวจ Rocq ในข่าว | Natural actual-execution-results comparison; preserve no official checker execution. |
| cawx | เคอร์เนล Rocq ตรวจบทพิสูจน์ตอนคอมไพล์ | เคอร์เนล Rocq ตรวจบทพิสูจน์ที่ AI เขียนขณะคอมไพล์ | Final named-term check caught omitted AI authorship; restore full AI-written proof clause even over36char budget. |
| 936d | budget-only | คำนวณให้คงค่าครบ แล้วเก็บผลรวมด้วยจำนวนเต็มไร้เครื่องหมาย 16 บิต | Over provisional character budget. Preserve full meaning; unresolved for coordinator, not silently passed. |
| u2xw | budget-only | ฉันกรอกช่องคืนค่าด้วยโปรแกรมนับอิสระอีกตัว อินพุตคือขีดจำกัดการนับ | Over provisional character budget. Preserve full meaning; unresolved for coordinator, not silently passed. |
| cawx | budget-only | เคอร์เนล Rocq ตรวจบทพิสูจน์ที่ AI เขียนขณะคอมไพล์ | Over provisional character budget. Preserve full meaning; unresolved for coordinator, not silently passed. |
| 7ip9 | budget-only | ฉบับสาธารณะเทียบรุ่นปกติกับรุ่นตรวจข้อผิดพลาดของโปรแกรมเดียวกัน ไม่ใช่ก่อนหลังแก้ | Over provisional character budget. Preserve full meaning; unresolved for coordinator, not silently passed. |
| 6x7t | budget-only | ในโมเดลระบบ อินพุตต้องไม่ทำให้รุ่นปกติเกินงบหน่วยความจำที่ระบุ | Over provisional character budget. Preserve full meaning; unresolved for coordinator, not silently passed. |
| 5u3j | budget-only | ตรงตามเงื่อนไขนี้ ทั้งสองรุ่นจะไม่เกิดข้อผิดพลาดที่ระบุ | Over provisional character budget. Preserve full meaning; unresolved for coordinator, not silently passed. |
| cnnu | budget-only | บันทึกพฤติกรรมที่มีความยาวจำกัด อาจมีข้อความที่โปรแกรมส่งออกแล้ว | Over provisional character budget. Preserve full meaning; unresolved for coordinator, not silently passed. |
| 4nfp | budget-only | นี่เฉพาะฉบับสาธารณะ ไม่ได้แปลว่างานวิจัยทั้งหมดไม่พิจารณาการสิ้นสุด | Over provisional character budget. Preserve full meaning; unresolved for coordinator, not silently passed. |

### Remaining budget conflicts

Full faithful Thai text is retained. These8lines are NOT declared budget-ready; independent review or actual native whole-window fit must resolve them. No premise, negation, scope, AI authorship or numeric value was removed to force the count.

| ID | chars/max | over | text |
|---|---|---|---|
| 936d | 64/63 | +1 | คำนวณให้คงค่าครบ แล้วเก็บผลรวมด้วยจำนวนเต็มไร้เครื่องหมาย 16 บิต |
| u2xw | 66/58 | +8 | ฉันกรอกช่องคืนค่าด้วยโปรแกรมนับอิสระอีกตัว อินพุตคือขีดจำกัดการนับ |
| cawx | 49/36 | +13 | เคอร์เนล Rocq ตรวจบทพิสูจน์ที่ AI เขียนขณะคอมไพล์ |
| 7ip9 | 81/74 | +7 | ฉบับสาธารณะเทียบรุ่นปกติกับรุ่นตรวจข้อผิดพลาดของโปรแกรมเดียวกัน ไม่ใช่ก่อนหลังแก้ |
| 6x7t | 62/54 | +8 | ในโมเดลระบบ อินพุตต้องไม่ทำให้รุ่นปกติเกินงบหน่วยความจำที่ระบุ |
| 5u3j | 55/44 | +11 | ตรงตามเงื่อนไขนี้ ทั้งสองรุ่นจะไม่เกิดข้อผิดพลาดที่ระบุ |
| cnnu | 64/52 | +12 | บันทึกพฤติกรรมที่มีความยาวจำกัด อาจมีข้อความที่โปรแกรมส่งออกแล้ว |
| 4nfp | 67/57 | +10 | นี่เฉพาะฉบับสาธารณะ ไม่ได้แปลว่างานวิจัยทั้งหมดไม่พิจารณาการสิ้นสุด |

### Metadata critique

- Preserved audience conjunction rather than broadening to OR.
- Kept original self-written C and original SVG ownership explicit; no product-operation image claim.
- Restored formal-verification qualifier in thumbnail tag rather than shortening away its type.
- Kept title under100chars,7 chapter names about30chars, stressed255 and newline in thumbnail.

### Numeric / logical boundaries checked

- 2026-10-25 local demo date /10-22 official study publication distinct; clause date first.
- 0..255 input;8byte capacity+1byte terminator;0..7 accepted iff others rejected;bit vsbyte preserved.
- int256 then uint8 narrowing0; unsigned8/16 and complete widening/cast changes retained.
- sole extra255;256 input comparisons;deny-all symbolic not compiledC;0falseaccept/8falsereject.
- loop independent,0.25sec observation only;fixedinput256-step cycle vs actual fixed C returning256 /n+1.
- 239entry/123library official report vs60entry/25library publicrelease;onlythisrelease lacks halts proof.
- Rocq compile/kernel AI-proof attribution, wrapper fixed proposition/used assumptions, allowlist maintained.
- plain specified memory budget;finite observable records same allowed set;no entire-app certificate/no vendorRocq rerun.

## Handoff

VI: complete,0budget conflicts,await independent review. TH: complete,8provisional line-budget conflicts preserved in full,await independent review and fit. Neither locale has been merged or synthesized by this translator. No thumbnail render fit or audio quality is claimed.
