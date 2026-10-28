---
id: 2026-10-28-localize-twelve-ai-foundation-life-guides
title: Localize twelve AI foundation life guides into four languages
status: done
priority: P1
area: api
owner: codex-gpt6-life-ai-foundations-20261028
claimed_at: 2026-10-28T07:12:50Z
created_at: 2026-10-28T07:12:47Z
completed_at: 2026-10-28T08:23:21Z
branch: codex/localize-travel-life-20261028-next
depends_on: []
scope:
  - apps/api/app/guides/content/ai-term-artificial-intelligence.json
  - apps/web/public/guides/ai-term-artificial-intelligence
  - apps/api/app/guides/content/ai-term-machine-learning.json
  - apps/web/public/guides/ai-term-machine-learning
  - apps/api/app/guides/content/ai-term-deep-learning.json
  - apps/web/public/guides/ai-term-deep-learning
  - apps/api/app/guides/content/ai-term-neural-network.json
  - apps/web/public/guides/ai-term-neural-network
  - apps/api/app/guides/content/ai-term-generative-ai.json
  - apps/web/public/guides/ai-term-generative-ai
  - apps/api/app/guides/content/ai-term-transformer.json
  - apps/web/public/guides/ai-term-transformer
  - apps/api/app/guides/content/ai-term-attention-mechanism.json
  - apps/web/public/guides/ai-term-attention-mechanism
  - apps/api/app/guides/content/ai-term-pretraining.json
  - apps/web/public/guides/ai-term-pretraining
  - apps/api/app/guides/content/ai-term-inference.json
  - apps/web/public/guides/ai-term-inference
  - apps/api/app/guides/content/ai-term-model-parameters.json
  - apps/web/public/guides/ai-term-model-parameters
  - apps/api/app/guides/content/ai-term-overfitting.json
  - apps/web/public/guides/ai-term-overfitting
  - apps/api/app/guides/content/ai-term-supervised-fine-tuning.json
  - apps/web/public/guides/ai-term-supervised-fine-tuning
---

# Localize twelve AI foundation life guides into four languages

## Why

The owner requested continued completion of missing travel-information and life
article languages. A fresh public-list census on October 28 identifies 12 intel
articles missing 48 documents and 666 life articles missing 2,664 documents.
These twelve foundational AI life articles are public in Traditional Chinese
and have no repository translations in en, ja, ko or zh-CN. Reuse existing
hash-bound jobs if a matching source is found; otherwise translate the complete
body and text-bearing artwork through the existing localization pipeline.

This is a narrow content child of the existing missing-locale program. The old
coverage document is touched by open PR #1902 and is deliberately not part of
this task's scope. Source corrections, travel-route admission and publication
have separate tasks and evidence.

## Definition of done

- [x] All twelve live sources have fresh source/visibility/version bindings and a source fact review before translation.
- [x] All 48 missing documents and text-bearing images are complete, schema-valid and independently reviewed with exact artifact/document/asset hashes.
- [x] Original repository documents/images and existing live source rows are preserved; any repository-only source-description difference has explicit preservation admission.
- [x] Native bundle assembly/install and replay pass, applicable content checks pass, and a guarded content PR exists.
- [x] A separate release task depends on this task; no authored or rendered document is mislabeled published.

## Steps

- [x] Verify current repository, active scopes, old jobs and fresh public missing-language census.
- [x] Export a bounded repeatable-read production snapshot for exactly these twelve slugs.
- [x] Review source facts, metadata differences and artwork; record any blocking findings separately.
- [x] Pin a scoped baseline and prepare all 48 missing locales.
- [x] Complete the ChatGPT-authenticated native translation run, retaining every attempt and failure.
- [x] Render, independently review each locale and apply only reviewed corrections.
- [x] Assemble/install the native bundle, check source preservation and idempotency, test and open the content/release PR cycle.

## How to verify

Use the unchanged `docs/article-localization/build_baseline.py` and
`tools/article-localization/pipeline.py` with external baseline/work paths and
exact selected slugs/locales. Keep all source snapshots, jobs, attempts, failed
outputs and reviews outside Git. Run official artifact/layout validation,
`GuideDocument`/content-pack checks and native assembly/install guards. Publish
only after a merged/deployed content revision, fresh database guards, backup,
native dry-run/replay and actual public browser acceptance.

## Notes

- Fresh census SHA256: `3053530178e419d65dd6cf38567d5988fe888ec76363db44099e03851bf0daf0`.
  Its sequential public-list observation excludes hidden/expired/draft-only
  articles and is not a repeatable-read whole-database snapshot.
- The selected production snapshot is a fresh repeatable-read read-only export
  from deployed `b78895e5fad1285d68a49a9e059eb318b846e40d`; it is authoritative
  only for these twelve articles. No publication or article mutation occurred.
- The current task claim found no active overlapping task scope. Historical
  research/verification exists, but different staging/source bytes do not inherit
  an old PASS. Current source review and exact-source job reuse remain required.
- Scoped baseline SHA256:
  `3a496f7b1bc9225b64c3d7e7ac439c314ad816c80285a112722e6c5ff19687c8`.
  All twelve source documents exactly match current repository canonical values;
  no repository preservation admission is needed for this cohort. All 48 target
  database locale rows were absent. Source published versions include 2, 8 and 10.
- All twelve full sources and source artwork passed fresh primary-source review.
  A source-citation redirect in `ai-term-inference` is a separate nonblocking
  maintenance task; the same official term search supports the terminology.
  This does not claim every legacy citation URL is directly healthy.
- Initial AI/ML eight documents completed translation, rendering and independent
  native review. One English terminology correction was applied by the root
  coordinator, materialized and rendered without changing any source, attempt or
  visual asset byte. The original finding and exact-diff closure are retained.
  The remaining forty jobs and disjoint independent review partitions continue.
- PR #1906 was merged after all 22 exact-head checks passed as
  `4422b10853e0ead1e647bf17d11f4f0179989fdb`. That receipt merge itself does
  not deploy or publish this new 48-document cohort.
- Native runner uses the existing ChatGPT login, no new paid provider, at most
  three workers, no automatic quota/auth retries, and an external STOP sentinel.
- The overall missing-language program remains open; this task covers 48 target
  documents and does not claim completion of the remaining 2,712 documents.

### Completed local authoring evidence

All 48 documents passed final independent text, glyph and visual review; three
review partitions each sealed 16 native `reviewed_document` PASS results. All
96 final previews were actually viewed. The 144 public SVG/JPG assets are pinned
to their final review manifests. All findings are closed after third-party
application, native materialization, rendering and independent re-review.

- Native bundle manifest SHA256: `c7a96098b4e8483937394e666144194d950f1b94e634d49b2d5f6fa5d13c6de0`.
- Native assembly: 12 articles / 144 public assets. Native installation: 156 files.
- Native replay exit 0; all 192 scoped content/image files retained identical bytes and modification times.
- Independent post-install audit SHA256: `7c5830b17259c667db79f374eb965705a47ce5ec9547df9f100feaf680792183`.
- All twelve zh-TW canonical documents and all 36 original image bytes are unchanged.
  Original reader-facing values and body array ordering are unchanged; the native
  serializer adds schema defaults and sorts the top-level topics taxonomy set
  without changing its members. The initial overly strict raw-order audit was
  retained with the explicit taxonomy-only ruling. No other array exception was made.
- Authoritative jobs, source snapshots, failed attempts, render HOLDs and evidence
  remain outside Git. The unchanged installer requires repository-relative inputs,
  so a locally ignored byte-identical staging mirror was independently admitted;
  it and the ignored durable journals/backups are retained for replay.
- One neural-network Korean call failed with selected-model capacity, with no
  quota/auth/policy error. After an unchanged-model unstarted job succeeded, one
  explicit native reset preserved attempt 1 and completed attempt 2. No automatic
  retries, provider switch or new paid model route was used. The run-level exit 1
  records and all content-invalid outputs remain retained; final native validation
  and all 48 current reviews pass after reviewed corrections.
- Checks: native pipeline 35 passed; artifact/layout 25 passed; localization
  baseline/assemble/install/progress 68 passed; life-pack lint 1,022 entries, exit 0
  with existing warnings; content-pack pytest 9 passed / 5 database integration
  cases skipped locally. CI must supply the real PostgreSQL release-safety gate.
- Translation glyph scan exit 0. Its one JA flag is the exact quoted Chinese
  official term `丟棄正則化`, explicitly attributed to a Traditional Chinese
  glossary; an independent exact-source ruling confirms it is legitimate.
- Separate unclaimed release task: `2026-10-28-release-localized-twelve-ai-foundation-life`.
  This cohort has not been deployed, imported, published or publicly accepted.

| Source slug | Published zh-TW version | Unchanged canonical SHA256 |
| --- | --- | --- |
| ai-term-artificial-intelligence | 10 | `07703e0617326488d72f63f255c089ddba66db016b24d79aca0ba52172ec1cf6` |
| ai-term-attention-mechanism | 2 | `a28ffa4ef31c1fce3ef230096635ea11cf29015151b35fc81887b92670164ade` |
| ai-term-deep-learning | 8 | `09cf22adbfbb39853c0a72534d6d796b9e91a3a2c2c6a30a628ff85c7fbc1761` |
| ai-term-generative-ai | 10 | `a24e2cf6f3e3e5d361d79fe8d14066da2f7328569f60d78a7bce8b2f66ebd508` |
| ai-term-inference | 2 | `c3fb9fa0bb93f59db90e3eaa06a780a12ddb16cb36b7a1c665026dfe37210779` |
| ai-term-machine-learning | 8 | `a9d9857fa2381101eda1d2e04a000dc468efb96ddb33bc7268efbad8af5e0b24` |
| ai-term-model-parameters | 10 | `d81988ad18a6b502971db7be8d7fcb2b04d6670c2309cefb14a16cd6b99613dc` |
| ai-term-neural-network | 2 | `b9ac89cbac4be9d13b9f09f7c302126e5fe2b16b3cf9704371e3440f2a07ceae` |
| ai-term-overfitting | 2 | `3c1c79c9fe076ecf534fb50f3155dcdc92985a8e8a59a3b5759925f623adadfc` |
| ai-term-pretraining | 8 | `6704028caa598aacf1a409b0012c7dbf170229dcd74026fb1d2c65551bf71796` |
| ai-term-supervised-fine-tuning | 8 | `74cb9d2062b3093359dc102ab0d2c7befaa382eda48034336e12fe3aa1113dc6` |
| ai-term-transformer | 10 | `21e988fffe2b5aca82eb54d7f0d254ce8e524f5cc76441df30b0a31e14d3adce` |

| Slug | Locale | Reviewed title | Canonical document SHA256 |
| --- | --- | --- | --- |
| ai-term-artificial-intelligence | en | What Is Artificial Intelligence? | `e70612c13e85da67969971721e43ecaafedc04896cf36c2044bdd2541a572ebe` |
| ai-term-artificial-intelligence | ja | 人工知能（Artificial Intelligence）とは | `45e0e691e83aca5c3da29c0a8d14ad35376789d4e0febb09bc4868d71f4ae3a0` |
| ai-term-artificial-intelligence | ko | 인공지능(Artificial Intelligence)이란 무엇인가 | `ecc9f0e8ae62066f9487fa81cfa838aaffb2b6fb0a79ddbc3deab5b9c84bdd68` |
| ai-term-artificial-intelligence | zh-CN | 人工智能（Artificial Intelligence）是什么 | `53f032dca5250de65763e8af8b73de778352a3a4a7dd810dbbb3dc1045ea0301` |
| ai-term-attention-mechanism | en | What Is Attention? How Models Decide Which Tokens to Refer To | `32913fc4ac2d5f4de0180acf87da19a6d8ed9d435ee061d0d6eeb14bc5058536` |
| ai-term-attention-mechanism | ja | アテンション機構（Attention）とは：モデルは参照する token をどう決めるのか | `cffb5d77d11387b20e07249872d0809ffeb6cf69f808b42a9aa9df48a84cf688` |
| ai-term-attention-mechanism | ko | 어텐션(Attention) 메커니즘이란: 모델은 참고할 토큰을 어떻게 정할까 | `d807eb88e3c1afbd20311fa4377e879dbbaf1eaab8ed30bdf0855e0d01123b89` |
| ai-term-attention-mechanism | zh-CN | 注意力机制（Attention）是什么：模型怎么决定要参考哪些 token | `78d2108cf40d79b01db60595792dedf2334d3cb19f7e31bd0183a5f370a7c55e` |
| ai-term-deep-learning | en | What Is Deep Learning? | `2b6ce529be9d13214c69d43a6f095432a0c7cc342fcb5f0e69602048d6df5774` |
| ai-term-deep-learning | ja | 深層学習（Deep Learning）とは | `097a818a656dcc134cadd74064c0379afd0d65fbcb7d4d6d08765c79886b468e` |
| ai-term-deep-learning | ko | 딥러닝(Deep Learning)이란 | `1c28975b6ccbb22e3efc0f5c25d350d727721f5ec4dc01a49970a28831d62e94` |
| ai-term-deep-learning | zh-CN | 深度学习（Deep Learning）是什么 | `620b05ed17bb5d762028295e65b212954a2f273d69bbd98e8ecfc2be097786d1` |
| ai-term-generative-ai | en | What Is Generative AI? | `fcc262a19623850a2a1f9990320a2a72d01b739f7a44df33902dee3bf5a6bf1d` |
| ai-term-generative-ai | ja | 生成AI（Generative AI）とは | `c5a064bfcd7af562e1a8246b4e74e7c80d2a75a6d3b9a9a52e83e478eaff8240` |
| ai-term-generative-ai | ko | 생성형 AI(Generative AI)란 무엇인가 | `41badfec15fdb4ca49d4a26f1d6b1a9b9983b9b4433211c66989bf1b997c59e8` |
| ai-term-generative-ai | zh-CN | 生成式 AI（Generative AI）是什么 | `edbd73ec19934279ff1025489d767688dfe651ce624a0d22bd7e342c120a43d3` |
| ai-term-inference | en | What Is Inference? The Computation Behind Every Response After Model Training | `71f73ae1b116cc7262bdb9195c1e0e1703678c674f4147444a32f57d0e6ccdd4` |
| ai-term-inference | ja | 推論（Inference）とは：モデルの学習後、回答するたびに行われる計算 | `1f7098c554eaaffad0869c9cc7a18cd2835bd9c0859c64222112f81735a93146` |
| ai-term-inference | ko | 추론(Inference)이란: 모델 학습이 끝난 뒤 매번 응답할 때 수행하는 계산 | `e400909c7ac87d9ba5efed48734f553a123bfb0c5372eaced7dd48acb9ed4722` |
| ai-term-inference | zh-CN | 推论（Inference）是什么：模型训练完成后，每次回答都在做的计算 | `6466a932add0b752e38624b42c4f42cee82534591c1c6bee2a7aa8895d933c57` |
| ai-term-machine-learning | en | What Is Machine Learning? | `69eb72cff1cee797839c1cbc790b47eb62b3502456ad14f89270e7e1d8bb4b73` |
| ai-term-machine-learning | ja | 機械学習（Machine Learning）とは | `99a18105e024f42b3f05c6c9c8393fbf8904cc8e804780493733e3ed397a27b4` |
| ai-term-machine-learning | ko | 머신러닝(Machine Learning)이란 무엇인가 | `b24376622728f825eee5b243e77d3502dd2c90eb3290b57eb782981623e7fbfc` |
| ai-term-machine-learning | zh-CN | 机器学习（Machine Learning）是什么 | `068b5f029bf3cee3539c4fd786941218a8298ada737d54e8a5ec4346f90eb93d` |
| ai-term-model-parameters | en | What Are Model Parameters? | `76145183de83bae06c718f1c4e4416d8ef59afe6140ee52f527c3cb8c1938072` |
| ai-term-model-parameters | ja | モデルパラメータ（Model Parameters）とは | `3461706a81ba11cb83194f9b9a0c3fc900338e5a7b9a5fad503941529d2380bb` |
| ai-term-model-parameters | ko | 모델 매개변수(Model Parameters)란 무엇인가 | `e02b5e98a39b023c8491e25b245bd20c2bbec4b0aa75e7557b7b677924b4656c` |
| ai-term-model-parameters | zh-CN | 模型参数（Model Parameters）是什么 | `3aa651f72b28400fd9441865aeff8b94eec3b7e446c873f0237b877e1c88b2e2` |
| ai-term-neural-network | en | What Is a Neural Network? A Function Built from Layers and Weights That Learns from Data | `27abe697bd7f29dd93fa400332f640fae66e588fa5aaa330b914486a273c75c0` |
| ai-term-neural-network | ja | ニューラルネットワーク（Neural Network）とは：層と重みから成り、データから学習する関数 | `492d1e95079d99bb82969d8eda2103f5ef26f92d33673fc0a9f174d2b8a7c375` |
| ai-term-neural-network | ko | 신경망(Neural Network)이란: 층과 가중치로 이루어져 데이터로 학습하는 함수 | `3aa5c9056b0825241ec2b728fd74be4f721d35423dd41a5e25b27bb3f3d3e90c` |
| ai-term-neural-network | zh-CN | 神经网络（Neural Network）是什么：由层与权重组成、能从数据学习的函数 | `ede7be832b6d7d566b1e0d31a0c9b4b6d8f7d21bbdef941950e8f4f3e70a4650` |
| ai-term-overfitting | en | What Is Overfitting? Acing Past Exam Questions, Failing New Ones | `0dec1a5c0d1eb37e5da7b790aff5d6bb23a2f937b708a44244e2e10115bbf2bc` |
| ai-term-overfitting | ja | 過学習（過適合、Overfitting）とは：過去問は全問正解、新しい問題では誤答 | `5cea377ec66ab48f440e2a34ef1f8c9cd7d0350311dbe6cdcf34981ded5e8eed` |
| ai-term-overfitting | ko | 과적합(과잉 적합, Overfitting)이란: 기출문제는 다 맞히지만 새 문제는 틀린다 | `f11f400f803947add47955c6f62f12d83e17169da03931384c0b93bd447c2f6c` |
| ai-term-overfitting | zh-CN | 过度拟合（过拟合，Overfitting）是什么：历年真题全对，新题却答错 | `bc55f64d5d196e7a2571aa356731b130aceae032cca146f22893a793540c8147` |
| ai-term-pretraining | en | Pretraining: Where a Model's Foundational Abilities Come From | `a14a0565dd205dd3f51b8350f0df5d9aafb0470ab315919c8e2fd92cdb000fca` |
| ai-term-pretraining | ja | 事前学習（Pretraining）：モデルの基礎能力はどこから来るのか | `b5d8629c930e1386e7ca57a814feeb6e7d57e123ad59704be5b63e5c01ac2aa4` |
| ai-term-pretraining | ko | 사전 학습(Pretraining): 모델의 기초 능력은 어디에서 오는가 | `28414e414bc1a427f4e2ee51982e11658bbb3924e4745d7d3b8647175781838a` |
| ai-term-pretraining | zh-CN | 预训练（Pretraining）：模型的基础能力从哪里来 | `d2c3f631a6d54f49363bdc5d6e38d1de860bea3bdd674cf5c1071651b381a246` |
| ai-term-supervised-fine-tuning | en | Supervised Fine-Tuning (SFT): Teaching Models Tasks with Good Examples | `7184bfdcb09c017d3e68e376c6b8e5b75bdf6be32dc3242c40b6c47a7d5b7868` |
| ai-term-supervised-fine-tuning | ja | 教師ありファインチューニング（SFT）：良い例でモデルにタスクの実行を教える | `8a306f163cb5b19bbc82bc05bbb45ca2b4a2d553f4c92481def6dc0086563f69` |
| ai-term-supervised-fine-tuning | ko | 지도 미세 조정(SFT): 좋은 예시로 모델에 작업 수행을 가르치기 | `499ae63e1bd9f8dd78543f8a20d62498aaf9764d8a91b07bbed8838427af225a` |
| ai-term-supervised-fine-tuning | zh-CN | 监督式微调（SFT）：用好示范教模型完成任务 | `ae957b9bbdae8862a10fd45c55c4833ca32269db656e6099de4c9be2c08eb931` |
| ai-term-transformer | en | What Is the Transformer Architecture (Transformer)? | `62eb6c7950415d63a6b91a5b5c879a015736dcb3949b40dbb24698ad1ee21de6` |
| ai-term-transformer | ja | Transformer アーキテクチャ（Transformer）とは | `c3f67339bda928d8eb4d20ba4830e2b7387817e77618d27435b2027c6e2079f0` |
| ai-term-transformer | ko | Transformer 아키텍처(Transformer)란 무엇인가 | `10b08afaac0ba5fb881b79f81c784fadc2c993bf9a51cadc6e8b2cec831c46c9` |
| ai-term-transformer | zh-CN | Transformer 架构（Transformer）是什么 | `108815f960c665d80ab04710afda38c435caae3e84914e95c8044db159cd32cd` |

- Content PR: https://github.com/x812033727/travel_scanner/pull/1911, protected by no-auto-merge. Production remains a separate release task.
