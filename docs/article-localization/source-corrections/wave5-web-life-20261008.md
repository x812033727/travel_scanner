# Source corrections for twelve design and performance articles

Four published Traditional Chinese life articles contained five article links
that sent ordinary HTML markup or URL parameters to unrelated AI glossary
articles. Replace precisely those `ArticleInline` objects with `TextInline`
objects containing the same visible words before authoring the missing locales.
All remaining document nodes, article metadata, citations, original dates and
original media retain their original values.

| Article | Document pointer | Preserved word | Original unrelated target |
| --- | --- | --- | --- |
| lazy-loading-images | /blocks/9/inlines/1 | 標記 | ai-term-token |
| open-graph-sharing | /blocks/1/inlines/1 | 標記 | ai-term-token |
| open-graph-sharing | /blocks/3/inlines/1 | 參數 | ai-term-model-parameters |
| ui-ux-learning | /blocks/16/inlines/1 | 標記 | ai-term-token |
| amp-website-decision | /blocks/3/inlines/1 | 標記 | ai-term-token |

The first six source audit proposed the Lazy Loading and Open Graph corrections;
the second six source audit proposed the UI/UX and AMP corrections. Root applied
the external candidates. Each audit's author independently reviewed the other
audit's corrected sources, including their complete bodies, primary citations,
native diagrams and original hero images. No correction author approved their
own proposal. The other eight selected sources passed their original independent
source audits without changes.

Source review took place on 2026-10-07 UTC (2026-10-08 in Taipei). Original citation
`checked_on` dates remain unchanged and are not presented as those reviewers'
historical visit dates. AMP's original Site Scan DNS failure is retained; the
reviewer separately read the indexed official primary body. This supports the
source claim and does not establish current origin availability.

| Article | Original normalized document SHA256 | Corrected normalized document SHA256 | Independent formal review SHA256 |
| --- | --- | --- | --- |
| lazy-loading-images | e0cb879c815acb62b04985be6ca1525606f7184a8815875d1abce46efce76335 | 2dda1061b6dd39fdfd06fe12b257d82ac92bfea46ded62ac0bddba6bb68bbde4 | 54229b57ad6a7bea42b2f26126fb68f7aeaf327d7f48327ba0900a5dcc283f7b |
| open-graph-sharing | db4f28219ece2b1db0cc1fb932830c2e7689c628d894ee41176d6df36d2c9e21 | 8df97903caaae96f1792f04a3947d4a043991347ad5768051db0a110c5bc936f | 8995381fc73a92ec34cd41a52d6473154d04b7487dc6f6af24856fa0119bd812 |
| ui-ux-learning | 978d15c8a8170fc433861b6cd031a73ec665928357d0afaa00e7455b0310270a | b01fb3630f90549698f89d9eac791dcc011b91e6b0e38069f0c9d8c1a6469411 | a24edf34bc61f080751a3e6b6ce85c9be0253e22a3802a998cc41e2bfa01f509 |
| amp-website-decision | 832702dfda328e301140bda475ca702c9481ae75149e6e7f8a8f727b9a7c8974 | 7369c58003df56cc169d35efb05523c392cace876dddc1247daa5dfe250bbd40 | b18d828eb81270f10351f4d320860fb8a92188164a2602e118ebbeb9d702fb27 |

The two genuine evidence files are bound by
`4edebacb8714f1f52c5f27e498cdfe3b914411abc66090f00bf5a4a4630807dc`
(Lazy Loading and Open Graph) and
`c461827ba68c51925ab1397707b4b22b282f0c399b405cefc6e3c35c6fe48832`
(UI/UX and AMP). The unchanged official source correction verifier accepted all
four exact formal reviews before Root copied the four candidate packs. Formal
receipts contain private database identity/version guards and remain external.

Actual source admission and unchanged official preparation completed with exit 0
for twelve articles and 48 fresh locale jobs. The admission receipt SHA256 is
`ea3738ed9ae3a98dc49c888e2050a1d73435210c8201c464aaea00b0ecd6e19d`.
The original baseline remains byte-identical at
`1c5ac31f7a4e3d2973867f12677888b0adef9f259a732d2b4b0ceef0c74054de`;
the separately derived baseline is
`dd2ba60408ee287992c0b8179f163ed08c8bda24125a7766d4e94da4f8aa8d03`.
Only desired source documents/hashes, the four source-locale documents and their
pack byte hashes changed in that derived baseline. A full restoration comparison
preserved every original database guard, metadata/asset record and unselected row.
All 36 original selected media files remain byte-identical.

Source correction approval and local job preparation do not approve translated
documents or their visuals. Independent locale review, official bundle assembly
and installation, scoped checks and CI remain separate gates. Production release
requires a fresh snapshot, original source/locale version checks, dry-run, backup,
durable publication and actual five-language public page verification.
