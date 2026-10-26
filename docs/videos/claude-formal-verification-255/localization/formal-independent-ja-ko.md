# Formal255 JA / KO: independent caption and metadata review

Reviewed all105caption/source pairs per locale,7chapters,title,full description,tags and all3thumbnail fields. This reviewer did not translate JA/KO. Read the author self-report but did not treat it as proof. No worksheet/merge/source/media/paid/git action.

Source SHA256: e6e87e77f069a574d6e1d7f47bf2e5be031eb8566bb2edb71defa24ae4c2b99f
Claims SHA256: 527048b6061d21f70e00475cc4790a46b0de6e536a37e8966402194a043fa9c6
Speech hash: 8028c7320d9cab29

Three passes: semantic/factual scope; naturalness/terminology; static budgets and read-only native metadata checks.

**Verdict: fixes required; actual current worksheets are not declared ready for dubbing.** Main shared semantic fix: AI writing a candidate proof is not the same claim as AI having already proved the requirement. Explicit +1 steps should also be retained in the0/7examples.

## ja

Input worksheet SHA256: 8196e242410ad889165878f77a4e620ce5d7f779769ce9556b7fc2027506b64b
All105/7chapters/allmetadata read. Current budget overs: 1. Remaining after offered candidates: 1 (cawx).
Read-only composed description: 3107UTF-8bytes,10credits,7chapters,field-limit errors=[]. No merge performed.

| ID | Kind | Current | Proposed | Chars / max | Reason / status |
|---|---|---|---|---|---|
| bpnn | meaning | 記録には戻り値も必要です。別の計数プログラムは終了しますか？ | 記録の戻り欄も埋めます。別の計数プログラムは本当に終了しますか？ | 32/37 | 原文要填的是返回行為/欄位，不只返回值。現譯戻り値把紀錄縮成值；改回戻り欄並保留另一支計數程式是否真的退出。 Candidate fits static guidance. |
| c8r2 | meaning | 同じ要件をAIが証明した後、誰が検収しますか？ | 同じ要件の証明をAIが書いた後、誰が検収しますか？ | 25/33 | AI寫出待驗收證明，不等於要件已被AI成功證明。保留同一要件、AI作者、之後誰驗收，避免先宣稱證明成立。 Candidate fits static guidance. |
| cgit | numeric_step | 入力0では1回加算し、1を返す想定です。 | 入力0は1を1回足し、1を返す想定です。 | 20/25 | 原句明說輸入0、加1一次、預期返回1。1回加算只保留次數，補回每次增量1；不是修改原規則。 Candidate fits static guidance. |
| y326 | numeric_step | 入力7では8回加算し、8を返す想定です。 | 入力7は1を8回足し、8を返す想定です。 | 20/29 | 原句明說輸入7、加1八次、預期返回8。補回每次增量1，保留8次和返回8。 Candidate fits static guidance. |
| zg4q | glossary | 記録と正式な証明を照合するには、コードの版、命題、動作モデルを固定します。 | 記録と形式的な証明を照合するには、コードの版、命題、動作モデルを固定します。 | 38/49 | 此處是formal proof。正式な偏正式/官方身分，形式的な對齊形式驗證語境；程式版、命題、模型全部保留。 Candidate fits static guidance. |
| chapter:fix-proof-object | metadata_glossary | 記録を正式な証明の条件と照合 | 記録を形式的な証明の条件と照合 | 15/about30 | 章名同樣採形式的な証明，與標題形式検証及zg4q一致。 Candidate fits static guidance. |
| cawx | budget | Rocqカーネルはコンパイル時にAIの証明を検査します。 | Rocqカーネルはコンパイル時にAIの証明を検査します。 | 28/22 | 現句28/22，完整保留Rocq/kernel/compile/AI證明/檢查。沒有找到在22字內同時自然ですます且保留全部條件的可靠候選；保全文，靜態預算未解。 UNRESOLVED; full meaning retained. Optional explicit-authorship full line: Rocqカーネルはコンパイル時にAI作の証明を検査します。 (29chars); not a budget solution. |

Every original over-budget ID has either a faithful candidate or an explicit unresolved row. Proposed text is not applied.

## ko

Input worksheet SHA256: cfb509d14a94c35fbbc4c7942be416a89abb77bb8d562b8f4f27615eadc3a13c
All105/7chapters/allmetadata read. Current budget overs: 8. Remaining after offered candidates: 4 (wunt, cawx, 6x7t, 4nfp).
Read-only composed description: 3063UTF-8bytes,10credits,7chapters,field-limit errors=[]. No merge performed.

| ID | Kind | Current | Proposed | Chars / max | Reason / status |
|---|---|---|---|---|---|
| zfgp | naturalness | 2026년 10월 25일, 제 프로그램은 용량이 8바이트인데 길이 255를 허용합니다? | 2026년 10월 25일, 제 프로그램은 용량이 8바이트인데 길이 255를 허용합니까? | 48/53 | 保留完整日期、我的程式、容量8byte、長度255及驚訝問句；허용합니다?是陳述尾加問號，改正式自然疑問尾허용합니까。 Candidate fits static guidance. |
| c8r2 | meaning | 같은 요구를 AI가 증명한 뒤, 누가 검수할까요? | 같은 요구로 AI가 쓴 증명, 누가 검수합니까? | 26/28 | 把AI가 증명한 뒤已證明改為AI가 쓴 증명寫出的證明；保留同一要求、AI作者、驗收者，不先宣稱候選已成立。 Candidate fits static guidance. |
| 84hx | meaning_clarity | 두 사례로 사이의 다른 오류도 배제할까요? | 두 사례만으로 중간 오류도 없다고 알까요? | 23/26 | 保留只看兩筆的限制與是否足以知道中間沒有錯的提問。現句두 사례로...배제할까요容易像建議排除錯誤，且少了只的限制。 Candidate fits static guidance. |
| s57e | type_clarity | 먼저 8비트로 줄여 큰 변수에 저장해도, 0은 여전히 0입니다. | 먼저 8비트로 줄여 넓은 형에 저장해도, 0은 여전히 0입니다. | 35/37 | 큰 변수容易理解為數值很大；改넓은 형明指加寬型別。先縮8bit、再存入較寬型別、0仍為0的順序全保留。 Candidate fits static guidance. |
| cgit | numeric_step_budget | 입력 0은 한 번 더해 1 반환을 기대합니다. | 0은 1씩 1회 더해 1 반환 예상입니다 | 22/22 | 補明每次+1、1次、預期返回1。0作本段已定義輸入值的主題，並非刪除輸入條件；保留예상。完整합니다體，無句末句號，22/22。 Candidate fits static guidance. |
| y326 | numeric_step | 입력 7은 8회 더해 8 반환을 예상합니다. | 입력7은 1씩 8번 더해 8 반환 예상입니다. | 25/25 | 保留輸入7、每次+1、8次、預期返回8，25/25；原句只寫8次加算未明說增量1。 Candidate fits static guidance. |
| zg4q | glossary | 기록을 정식 증명과 대조할 땐 코드 버전, 명제, 실행 모델을 고정합니다. | 기록을 형식적 증명과 대조할 땐 코드 버전, 명제, 실행 모델을 고정합니다. | 42/42 | 用형식적 증명對齊formal proof，不是정식的正式身分；完整保留版號/命題/模型，42/42。 Candidate fits static guidance. |
| chapter:fix-proof-object | metadata_glossary | 기록을 정식 증명 조건과 맞추다 | 기록을 형식적 증명 조건과 맞추다 | 18/about30 | 章名與標題형식 검증及zg4q的formal術語一致。 Candidate fits static guidance. |
| zfmi | budget | 오류판은 총길이를 8비트 무부호 정수로 되돌립니다. | 오류판은 합계를 8비트 무부호 정수로 돌립니다. | 26/26 | 합계承接前文總長，保留錯版、轉回8bit無號整數。只縮總長的同義稱呼與動詞，26/26。 Candidate fits static guidance. |
| wunt | budget | 처음 고른 작은 값 0,1,2,3,4는 다섯 개 모두 예상대로였습니다. | 처음 고른 작은 0,1,2,3,4 다섯 값은 다 예상대로입니다. | 35/25 | 保留最初選取、五個小值、0/1/2/3/4、全符合預期；35/25仍超10，不能靠刪列舉、五個、小值或初選資訊硬塞。 UNRESOLVED; full meaning retained. |
| cawx | budget | Rocq 커널은 컴파일할 때 AI의 증명을 검사합니다. | Rocq 커널은 컴파일할 때 AI의 증명을 검사합니다. | 30/19 | 現句30/19。保留Rocq/kernel/編譯時/AI證明/檢查，未找到19字內自然且完整候選；保留全文，不用刪AI或編譯條件換取字數。 UNRESOLVED; full meaning retained. Optional explicit-authorship full line: 컴파일 시 Rocq 커널이 AI가 쓴 증명을 검사합니다. (31chars); not a budget solution. |
| 7ip9 | budget | 공개판은 같은 코드의 일반판과 오류 검사판을 비교하며, 방금의 수정 전후는 아닙니다. | 공개판은 같은 코드의 일반·오류 검사판 비교이며 수정 전후는 아닙니다. | 39/39 | 保留公開版、同一程式、一般與錯誤檢查兩建置、不是修正前後；39/39。只省同段已明白的剛才回呼，沒有把兩建置說成兩份相同binary。 Candidate fits static guidance. |
| 6x7t | budget | 모델상 일반판이 지정 메모리 예산 내인 입력이 전제입니다. | 모델상 일반판이 지정 메모리 한도를 지킬 입력만 봅니다. | 31/28 | 完整保留模型、一般版、指定記憶體預算及限制於讓一般版不超預算的輸入；31/28仍超3。不得縮成輸入大小本身低於記憶體上限。 UNRESOLVED; full meaning retained. |
| 4nfp | budget | 이 공개판의 얘기지 연구 전체가 종료를 안 다뤘다는 뜻은 아닙니다. | 이 공개판 한정이지 연구 전체가 종료를 안 다뤘단 뜻은 아닙니다. | 36/30 | 保留這份公開版限定、不代表、整個研究、沒處理終止；36/30仍超6。未改成研究整體缺少終止證明或完全沒終止工作。 UNRESOLVED; full meaning retained. |
| 3u2q | budget | 둘 다 실제 C 실행과 대조, Rocq 검사기는 미실행입니다. | 둘 다 실제 C 실행과 대조, Rocq 검사는 안 했습니다. | 33/33 | 保留兩者、實際C執行對照及沒執行Rocq檢查；33/33。檢查而非檢查器的同義表達不新增供應商執行。 Candidate fits static guidance. |

Every original over-budget ID has either a faithful candidate or an explicit unresolved row. Proposed text is not applied.

## Remaining source and metadata checks

- Input0..255,8byte capacity with1byte terminator within8,0..7iff and other8..255 rejection retained.
- int promotion256 then uint8 narrowing0;8bit vs8byte;16bit full expression and counter/update cast retained.
- Reject-all symbolic only, not a separate compiledC;widened-guard two-direction solver findings preserved, no second SAT study claimed.
- Independent counter not downstream of fixedguard;0.25sec observation vs256-step model cycle;all repaired inputs returnn+1.
- Official compile/kernel then wrapper/fixedtype/PrintAssumptions thenallowlist not replaced by modelself-claim.
- Plain build specified-memory premise,finite observable-record set equality,release-only nohalts and no studywide inference retained.
- Official123libraries239entries vs public60entries25libraries remain correctly attributed;no fabricated Claude toy experiment/full-app certificate.
- All metadata URLs/4paragraph blocks/originalSVG provenance/thumb numbers retained; no additional price/view/date claim.

Rejected shortcut: A28char phrase meaning input itself lies inside a memory limit is not offered: it may lose the premise about plain BUILD runtime memory usage.31chars full candidate remains unresolved.

## Limits / handoff

- Current words are not modified. Candidates need coordinator adoption and later independent/native checks as appropriate.
- No actual dub, pronunciation, audio hash,rendered thumbnail or whole-window fit has been reviewed here.
- Static fits do not guarantee speech fit; current source105 and old individual actualaudio checked earlier remain separate gates.
- The reviewer read all105 per locale; this is not a re-run of vendor proofs or paid translations.

JA retains1budget blocker. KO can reduce8original budget blockers to4with the offered full-meaning candidates; keep wunt/cawx/6x7t/4nfp full if no better faithful wording is found. Neither these counts nor this review certify a paid dub/M4A.
