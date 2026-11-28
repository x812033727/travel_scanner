# C03 Korean / Spanish translation audit

Scope: preparatory metadata + CC translations only. No audio, timing, timed SRT, merge, locale-completion claim, backend write, approval change, source hash or date change.

Final worksheets: `ko.todo.json` and `es.todo.json` each contain 143 translated lines, 6 chapters, title, description, tags and 3 thumbnail words. Draft → critique → final completed for each locale. Read-only structural comparison confirmed that every non-`text` value and key, including id/scene/source/todo/parts/glossary/boundaries, remains identical to the original worksheet context.

## Titles and checks

- ko: “Moleskine은 빈 노트를 팔아 어떻게 5억 유로 가까운 기업이 됐을까?” — 42 characters; 합니다체; chapter maximum 21 characters; tags 31 characters.
- es: “Moleskine vende libretas vacías: ¿por qué valía casi 500 millones de euros?” — 75 characters; neutral Latin-American tú; chapter maximum 29 characters; tags 80 characters; no CJK script in translated text.
- Titles and tags omit channel/series names. All source URLs, the 2026-10-25 source-access date, numbers, euro amounts and fiscal periods were retained.
- Reviewed distinctions: 2013 market capitalization (€487.6 million) versus 2016 total-equity valuation (€506 million); €2.40 per share; 2015 revenue €128 million; 2016 year-end 79 stores; 2017 paper share 81%; 2025 revenue €117.8 million / −3.7%, brand-intangible impairment €107.4 million; 2026 H1 revenue €52.2 million / +2.2%, operating result €700,000.
- Reviewed qualifications: first trademark filing on 1997-11-26; historical notebook type versus modern brand; average 3–6 months from production to launch; arrangements scoped to the 2013 prospectus; company statements and narrator opinions remain attributed; no inferred individual buyer motive.

## Glossary

| Source term | ko | es |
| --- | --- | --- |
| Moleskine / Modo&Modo / D’Ieteren | Exact Latin spelling | Exact Latin spelling |
| 招股書 | 투자설명서 | prospecto |
| 筆記本 | 노트 | libreta |
| 市值 | 시가총액 / 시총 | capitalización bursátil |
| 股權估值 | 지분 평가액 | valor de todas las acciones |
| 營收 | 매출 | ingresos |
| 營業結果 | 영업손익 | resultado operativo |
| 調整後營業結果 | 조정 영업손익 | resultado operativo ajustado |
| 營業利潤 | 영업이익 | utilidad operativa |
| 調整後集團應占稅前虧損 | 조정된 그룹 귀속 세전손실 | pérdida ajustada antes de impuestos atribuible al grupo |
| 品牌無形資產減損 | 브랜드 무형자산 손상차손 | deterioro del activo intangible de la marca |
| 股東貸款本金減免 | 주주에게 빌린 자금의 원금 일부 면제 | condonación de parte del principal de préstamos de accionistas |
| 寄售 | 위탁판매 | consignación |
| 批發銷售據點 | 도매 판매 거점 | puntos de venta mayorista |
| 直營店 | 직영점 | tiendas propias |
| 歌之版圖 | 송라인 | Los trazos de la canción |

Dictionary fragments `Code`, `D`, `DIeteren-Moleskine`, `Ieteren`, `Modo` remain intact within the complete official source title/company name/URL; they were not separately transliterated.

Source headings translated descriptively:
- Moleskine 2013 年義大利上市招股書 → ko “Moleskine 2013년 이탈리아 상장 투자설명서”; es “Moleskine 2013 — Prospecto de salida a bolsa en Italia”.
- D’Ieteren 2017 年投資人簡報 → ko “D’Ieteren 2017년 투자자 설명 자료”; es “D’Ieteren 2017 — Presentación a inversionistas”.
- 義大利交易所 2013 年上市公告 → ko “이탈리아 거래소 2013년 상장 공고”; es “Bolsa Italiana 2013 — Anuncio de salida a bolsa”.
- D’Ieteren 2016 年收購公告 → ko “D’Ieteren 2016년 인수 공고”; es “D’Ieteren 2016 — Anuncio de adquisición”.
- D’Ieteren 2017 年完成收購公告 → ko “D’Ieteren 2017년 인수 완료 공고”; es “D’Ieteren 2017 — Anuncio de finalización de la adquisición”.
- Official English headings retained exactly in both descriptions: “Moleskine, Our Heritage”; “Moleskine, Code of Ethics”; “D’Ieteren 2017 Activity Report — Moleskine”; “D’Ieteren 2017 Annual Report”; “D’Ieteren 2025 Full-Year Results”; “D’Ieteren 2026 Half-Year Results”.

## Critique applied in final

Korean:
- r302031 ｜ draft sounded dismissive of the retold story ｜ used neutral attribution and retained the absence of a complete factory archive.
- r305031 ｜ publisher term varied ｜ normalized to 출판사.
- r3i011 ｜ draft compressed the ordinary book being written for the viewer ｜ restored 여러분을 위해.
- r306021 ｜ bookstore setting implicit ｜ made 서점 explicit.
- r307021 ｜ awkward retrospective phrasing ｜ used 후일의 투자자 설명 자료.
- r3e071 ｜ “still” responsibility implicit ｜ restored 여전히.
- r313012 ｜ announced agreement could obscure signing ｜ explicitly used 인수 계약 체결.
- r315051 ｜ expansion beyond third-party stores unclear ｜ clarified 다른 업체 매장.
- r3n012 ｜ awkward attribution ｜ clarified 재무보고서에 나온 이유.
- r3n022 ｜ 실적 too broad for operating result ｜ changed to 조정 영업손익.
- r3n031 ｜ operating pressure phrasing awkward ｜ used 운영 부담이 커진 뒤.
- r3n061 ｜ operating-result metric inconsistent ｜ changed to 영업손익.
- r319041 ｜ operating-result metric inconsistent ｜ changed to 영업손익.
- r319031 ｜ shareholder-loan direction ambiguous ｜ explicitly stated funds borrowed from shareholders and partial principal forgiveness.
- r319051 ｜ “still” and return to the opening question weak ｜ explicitly retained both.
- r320011 ｜ operating-result metric inconsistent ｜ changed to 영업손익.
- r320013 ｜ draft omitted worthiness ｜ restored 받아들일 가치가 있는지.

Spanish draft critique:
- description ｜ historical use too definite ｜ restored association with the old notebook type and distinction from the modern brand.
- r3e131 ｜ possible spillover sounded certain ｜ restored podría.
- r314021 ｜ ownership scope insufficiently explicit ｜ retained all shares, including treasury shares.
- r3n022 / r319031 ｜ financial wording needed precision ｜ retained adjusted metrics, operating leverage, attributable pretax loss and partial loan-principal forgiveness.
- r3n041 / r318051 ｜ accounting wording needed clarity ｜ retained five-year forecasts and book-value recalculation.
- chapters / thumbnail / multiple lines ｜ overly long wording ｜ shortened without dropping clauses.

Spanish pair-review critique:
- r3h011 ｜ listing market-cap metric implicit ｜ explicitly retained capitalización bursátil.
- r307031 ｜ outlets rendered as actors ｜ changed to puntos de reventa.
- r3e112 ｜ “not today's contracts” overasserted the source ｜ changed to no pueden tomarse como.
- r313012 ｜ signing implicit ｜ changed to anunció la firma de un acuerdo.
- r3t042 ｜ grammar did not connect to que crearas ｜ changed to y luego conectaras.
- r316011 ｜ al migrar could imply causation ｜ explicitly stated sales fell in the year of the platform migration.
- r3n041 ｜ financial qualifier on forecasts missing ｜ restored financieras.
- r3n072 ｜ subject agreement awkward ｜ used pero eso no sustituye.
- r320013 ｜ worthiness missing ｜ restored si vale la pena.
- r320031 ｜ first-choice sequence weak ｜ restored primero and testing how well it writes.

## Remaining limitations

No unresolved semantic term or factual uncertainty was identified in these translations. Readability remains for later caption-cue QA: ko has 91 entries over the approximate 40-character guidance (maximum 72); es has 73 over the approximate 80-character guidance (maximum 177, r319031). These are intact multi-clause entries with required names, attribution and financial distinctions. No hard max_chars, narration duration or caption timing exists in these preparation sheets, so they must not be presented as timing-validated captions or completed locales. Root will serialize merges after independent review.
