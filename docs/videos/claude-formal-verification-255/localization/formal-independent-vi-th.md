# Independent VI / TH caption review

Reviewed all current 105 lines, 7 chapters and all metadata/thumbnail fields in each locale. Reviewer did not translate VI or TH. Semantic, native spoken and static-budget passes are complete. Findings are proposals only; neither worksheet was changed. No actual audio, TTS, ASR, paid work, merge, backend, git, source, claim, media or cache operation was performed.

Source SHA256: `e6e87e77f069a574d6e1d7f47bf2e5be031eb8566bb2edb71defa24ae4c2b99f`
Claims SHA256: `527048b6061d21f70e00475cc4790a46b0de6e536a37e8966402194a043fa9c6`
Speech reference: `8028c7320d9cab29` (coordinator/author reference; not regenerated).

No metadata correction is required: title/chapter/tag limits, complete source-package URL, paragraph structure, all thumbnail fields, stressed **255** and its newline match the requirements. Actual thumbnail rendering and dubbing fit were not assessed.

| Locale | Worksheet SHA256 | Current within budget | Required findings | Optional suggestions | Unresolved after candidates |
| --- | --- | ---: | ---: | ---: | ---: |
| vi | `1641566392931e1e650e40474afc012365a0edd5cea264bf35cd25edcd17330f` | 105/105 | 5 | 2 | 0 |
| th | `bb3a489d2305de9bf9d923d7492e6fde5ba54d89eac51c0e89b380d5f0f8c01e` | 97/105 | 11 | 0 | 3 |

Thai has five full-meaning candidates within the existing budgets: 936d, u2xw, 7ip9, 5u3j and 4nfp. Three remain unresolved: cawx, 6x7t and cnnu. The complete wording is retained in those candidates. This is a static character assessment, not an actual audio FAIL or PASS.

## VI findings

### cawx

Source: Rocq核心在編譯時，檢查AI寫出的證明。

Old (50/50): Nhân Rocq kiểm tra chứng minh do AI khi biên dịch.

Proposed (48/50): Khi biên dịch, nhân Rocq xét chứng minh AI viết.

Reason: The relative clause 'do AI' is grammatically unfinished. Name AI's writing explicitly, and attach the compile-time clause to the Rocq kernel's examination of that proof. The selected wording retains kernel, Rocq, AI authorship and compile time.

Static status: candidate_within_budget. No change applied.

Alternative (52/50): Nhân Rocq kiểm tra chứng minh AI viết khi biên dịch.; over static budget.

### 6x7t

Source: 在系統模型內，輸入須讓一般版不超過指定記憶體預算。

Old (73/75): Ở mô hình hệ thống, đầu vào không làm bản thường vượt mức bộ nhớ đã định.

Proposed (71/75): Mô hình hệ thống: đầu vào phải giữ bản thường trong mức bộ nhớ đã định.

Reason: Make the memory restriction explicitly a requirement on the admitted input, rather than a bare assertion that input never exceeds memory. Retain the system model, ordinary build and specified memory allowance. 'phai' restores the premise's must-condition.

Static status: candidate_within_budget. No change applied.

### ey22

Source: 紀錄的返回欄有結果了：每個輸入都離開，並返回上限加一。

Old (72/108): Ô trả về đã có kết quả: mọi đầu vào đều thoát và trả về giới hạn cộng 1.

Proposed (83/108): Ô trả về có kết quả: với mọi đầu vào, chương trình thoát và trả về giới hạn cộng 1.

Reason: An input does not itself exit or return a value. State that for every input the program exits and returns limit plus 1, while retaining the result in the return column.

Static status: candidate_within_budget. No change applied.

### 2yfh

Source: 這次的錯在轉型儲存，不能把兩種八當成同一件事。

Old (58/83): Lỗi ở ép kiểu lúc lưu; đừng coi hai số 8 là cùng một việc.

Proposed (55/83): Lỗi ở ép kiểu khi lưu; không thể đánh đồng hai số 8 ấy.

Reason: 'Hai so 8 la cung mot viec' is an unnatural literal rendering of treating two eights as the same thing. Use the ordinary Vietnamese verb for conflating them; keep the conversion-at-storage location and the two eights.

Static status: candidate_within_budget. No change applied.

### 5u3j

Source: 符合這個前提，兩版都不會出現指定錯誤。

Old (52/61): Đủ tiền đề ấy, cả hai bản không gặp lỗi đã chỉ định.

Proposed (54/61): Thỏa tiền đề ấy, cả hai bản không gặp lỗi đã chỉ định.

Reason: 'Du tien de' is an unnatural way to say that this premise is satisfied. Use 'thoa tien de'; retain the conditional, both builds, negation and only the designated errors.

Static status: candidate_within_budget. No change applied.

### 84hx (optional)

Source: 但只看這兩筆，怎麼確認中間沒有別的錯？

Old (58/70): Nhưng chỉ xem hai dòng này, sao biết ở giữa không còn lỗi?

Proposed (61/70): Nhưng chỉ xem hai kết quả này, sao biết ở giữa không còn lỗi?

Reason: 'Hai dong' can be understood as two record rows, but is also easy to confuse with two code lines just discussed. Naming the two results directly is clearer; this is not a claimed factual contradiction.

Static status: candidate_within_budget. No change applied.

### zgkb (optional)

Source: 這份紀錄另加一個求解模型，把同一輸入寫成八個真假位元。

Old (72/101): Phiếu thêm mô hình để giải, viết cùng đầu vào thành 8 bit đúng hoặc sai.

Proposed (73/101): Phiếu thêm mô hình giải: cùng đầu vào được biểu diễn bằng 8 bit đúng/sai.

Reason: The original meaning is recoverable. 'Bieu dien' makes the mathematical encoding of the same input in eight true/false bits more natural than 'viet cung dau vao thanh'. No model strength or checker is added.

Static status: candidate_within_budget. No change applied.

Verdict: ready_after_required_wording_fixes; actual_audio_not_assessed.


## TH findings

### cawx

Source: Rocq核心在編譯時，檢查AI寫出的證明。

Old (49/36): เคอร์เนล Rocq ตรวจบทพิสูจน์ที่ AI เขียนขณะคอมไพล์

Proposed (50/36): ขณะคอมไพล์ เคอร์เนล Rocq ตรวจบทพิสูจน์ที่ AI เขียน

Reason: At the end of the current relative clause, 'while compiling' can modify AI writing the proof. Put compile time first so the kernel performs the check during compilation. Keep the full kernel term, Rocq, proof and AI-written authorship. The clear candidate remains over 36 and is unresolved.

Static status: unresolved_keep_full_meaning. No change applied.

Alternative (45/36): ขณะคอมไพล์ แกน Rocq ตรวจบทพิสูจน์ที่ AI เขียน; over static budget.

### 936d

Source: 讓計算保留完整值，再用十六位元無號整數儲存總長。

Old (64/63): คำนวณให้คงค่าครบ แล้วเก็บผลรวมด้วยจำนวนเต็มไร้เครื่องหมาย 16 บิต

Proposed (62/63): คำนวณให้คงค่าครบ แล้วเก็บผลรวมในจำนวนเต็มไร้เครื่องหมาย 16 บิต

Reason: Replace only the storage preposition with 'in'. Preserve complete calculation value, stored total, integer, unsignedness and 16 bits.

Static status: candidate_within_budget. No change applied.

### u2xw

Source: 我用另一支獨立計數程式填返回欄；輸入是計數上限。

Old (66/58): ฉันกรอกช่องคืนค่าด้วยโปรแกรมนับอิสระอีกตัว อินพุตคือขีดจำกัดการนับ

Proposed (55/58): ฉันใช้โปรแกรมนับอิสระอีกตัวกรอกค่าคืน อินพุตคือขีดจำกัด

Reason: Fill the return value in the already named return field, using another independent counting program. State explicitly that its input is the limit. 'Counting' is already carried by the program, so the limit remains its counting limit; no downstream relation to the guard is introduced.

Static status: candidate_within_budget. No change applied.

Alternative (53/58): ฉันใช้โปรแกรมนับอิสระอีกตัวกรอกช่องคืนค่า รับขีดจำกัด; within static budget.

Alternative (59/58): ฉันใช้โปรแกรมนับอิสระอีกตัวกรอกช่องคืนค่า รับขีดจำกัดการนับ; over static budget.

### 7ip9

Source: 公開版比較同一程式的一般版與錯誤檢查版，並非剛才的修正前後。

Old (81/74): ฉบับสาธารณะเทียบรุ่นปกติกับรุ่นตรวจข้อผิดพลาดของโปรแกรมเดียวกัน ไม่ใช่ก่อนหลังแก้

Proposed (73/74): ฉบับสาธารณะเทียบโปรแกรมเดียวกันแบบปกติกับตรวจข้อผิดพลาด ไม่ใช่ก่อนหลังแก้

Reason: Move 'same program' before the ordinary/error-checking forms and avoid repeating 'version'. Retain public release, the same program, both forms and the explicit not-before/after-repair distinction.

Static status: candidate_within_budget. No change applied.

### 6x7t

Source: 在系統模型內，輸入須讓一般版不超過指定記憶體預算。

Old (62/54): ในโมเดลระบบ อินพุตต้องไม่ทำให้รุ่นปกติเกินงบหน่วยความจำที่ระบุ

Proposed (60/54): ในโมเดลระบบ อินพุตต้องให้รุ่นปกติไม่เกินงบหน่วยความจำที่ระบุ

Reason: The current meaning is correct. The shorter candidate still preserves system model, input must-condition, ordinary build, non-exceedance and specified memory budget. It remains over 54; no faithful natural in-budget version is offered.

Static status: unresolved_keep_full_meaning. No change applied.

### 5u3j

Source: 符合這個前提，兩版都不會出現指定錯誤。

Old (55/44): ตรงตามเงื่อนไขนี้ ทั้งสองรุ่นจะไม่เกิดข้อผิดพลาดที่ระบุ

Proposed (42/44): ถ้าตรงเกณฑ์นี้ ทั้งคู่ไร้ข้อผิดพลาดที่ระบุ

Reason: Use an explicit if-condition and 'both' referring to the two builds. Keep the absence of the designated errors, rather than promising absence of every possible error.

Static status: candidate_within_budget. No change applied.

### cnnu

Source: 有限的行為紀錄，可以包含程式已經輸出的文字。

Old (64/52): บันทึกพฤติกรรมที่มีความยาวจำกัด อาจมีข้อความที่โปรแกรมส่งออกแล้ว

Proposed (58/52): บันทึกพฤติกรรมความยาวจำกัดอาจมีข้อความที่โปรแกรมส่งออกแล้ว

Reason: Keep finite length of the behavioral record, possibility, text, the program as emitter and already-produced output. The clear shorter noun phrase remains over 52. A finite number of records or short records would change the claim and is not proposed.

Static status: unresolved_keep_full_meaning. No change applied.

### 4nfp

Source: 這說的是這份公開版本，不代表整個研究都沒處理終止。

Old (67/57): นี่เฉพาะฉบับสาธารณะ ไม่ได้แปลว่างานวิจัยทั้งหมดไม่พิจารณาการสิ้นสุด

Proposed (51/57): ข้อสรุปนี้ใช้เฉพาะฉบับสาธารณะนี้ ไม่ใช่ทั้งงานวิจัย

Reason: 'This conclusion' explicitly refers to the immediately preceding termination-proof statement. Restrict that conclusion to this public release and exclude the entire research from its scope. This preserves the source's anaphoric limitation without repeating the termination noun and does not assert that the wider research proved termination.

Static status: candidate_within_budget. No change applied.

### mvnc

Source: 紀錄已找到反例，哪一行能把完整總長留下？

Old (51/58): บันทึกพบกรณีโต้แย้งแล้ว แถวไหนเก็บความยาวรวมได้ครบ?

Proposed (54/58): บันทึกพบกรณีโต้แย้งแล้ว บรรทัดไหนเก็บความยาวรวมได้ครบ?

Reason: Use the Thai term for a line of code, not a table row: this question points to the line that preserves the total. Keep the found counterexample and complete total.

Static status: candidate_within_budget. No change applied.

### yavq

Source: 修正版這一整行，計算和存放總長的轉型都要一起改。

Old (53/59): ต้องแก้ทั้งแถว ทั้งการคำนวณและการแปลงชนิดที่เก็บผลรวม

Proposed (56/59): ต้องแก้ทั้งบรรทัด ทั้งการคำนวณและการแปลงชนิดที่เก็บผลรวม

Reason: This is the entire code line, not a record-table row. Retain both calculation and the conversion used to store the total as changes to that line.

Static status: candidate_within_budget. No change applied.

### ey22

Source: 紀錄的返回欄有結果了：每個輸入都離開，並返回上限加一。

Old (54/78): ช่องคืนค่าได้ผลแล้ว ทุกอินพุตออกและคืนค่าขีดจำกัดบวก 1

Proposed (62/78): ช่องคืนค่าได้ผลแล้ว ทุกอินพุต โปรแกรมออกและคืนค่าขีดจำกัดบวก 1

Reason: Make the program the subject that exits and returns the bound plus 1 for every input, rather than saying that the inputs exit. Retain the completed return-column result and the universal input scope.

Static status: candidate_within_budget. No change applied.

Verdict: wording_fixes_required; static_budget_pending.

## Boundary checks

local arithmetic: No numeric/type error found. Both retain 255 + 1 -> promoted ordinary integer 256 -> unsigned 8-bit narrowing 0; 8 bits and 8 bytes remain distinct.
guard contract and repair: Input 0..255, capacity 8 bytes, extra terminator byte, accept exactly 0..7, complete calculation/storage fix, no data-buffer write, both false-accept/false-reject directions retained.
local model scope: SAT remains propositional; two no-counterexample queries concern widened guard; deny-all comparison remains symbolic; loop uses complete finite control graph; local C comparison does not become Rocq reproduction or whole-app certification.
independent loop: Other independent counter, fixed limit, no other actor writing counter, 256-step cycle, timeout alone insufficient, counter declaration/update conversion repaired, all-input exit and n+1 value retained. Return-subject phrasing should be clarified as listed.
public proof attribution and order: AI authorship and compilation-stage checking need listed cawx wording fixes. The following fixed-proposition/used-assumptions and allowlist-audit sequence is retained in both.
agreement premise and behavior: Normal/error-checking builds of same program, not local before/after repair; ordinary-build memory allowance under system model; only designated errors excluded under premise; finite observable allowed-record sets equal. VI must-condition should be explicit as listed.
research vs release: Official research 123 libraries/239 entry points remains distinct from public 60/25. Lack of halts proof stays confined to this public release, with no extrapolation to the whole research. Thai scope-preserving short candidate uses explicit this-conclusion reference.

Raw Unicode character counts include Thai combining marks. No max_chars or source fields were changed. Full 105-line coverage, hashes, all proposals and alternate counts are in the JSON.
