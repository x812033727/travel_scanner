# C03 pt / id translation preparation

Status: final native worksheets filled for metadata and captions only. No merge, timed SRT, dub, voice, media generation, backend call, approval update, runtime language state, date change, or source hash write.

Counts: pt 143 caption entries, 6 chapter names, title, description, tags and 3 thumbnail fields; id the same. All requested text fields are populated. Only text fields changed; all ids, scenes, sources, todo flags, parts, glossary and boundaries remain unchanged.

Titles:
- pt (65 characters): Moleskine vende cadernos vazios: por que valia quase 500 milhões?
- id (63 characters): Moleskine menjual buku kosong: kenapa nilainya hampir 500 juta?

Glossary:
- Moleskine -> Moleskine in both locales.
- Modo -> Modo&Modo in company references in both locales; the supplied glossary fragment stays untouched.
- D / Ieteren -> D’Ieteren in company references in both locales; supplied glossary fragments stay untouched.
- DIeteren-Moleskine -> DIeteren-Moleskine inside the unchanged source URL in both locales.
- Code -> Code inside the unchanged official title Code of Ethics in both locales.
- Chatwin -> Chatwin in both locales.
- The Songlines -> O Rastro dos Cantos (Brazilian book title) in pt; The Songlines in id.
- market capitalization -> valor de mercado (pt); kapitalisasi pasar / nilai pasar (id; technical noun / ordinary wording).
- equity valuation -> avaliação do capital acionário (pt); valuasi ekuitas (id).
- revenue -> receita (pt); pendapatan (id).
- operating result -> resultado operacional (pt); hasil operasional (id).
- consignment -> consignação (pt); konsinyasi (id).
- brand intangible asset impairment -> perda por redução ao valor recuperável do ativo intangível da marca (pt); penurunan nilai aset takberwujud merek (id).
- inventory replenishment -> reposição de estoque (pt); pengisian stok (id).
- wholesale / direct retail -> atacado / varejo próprio (pt); grosir / ritel yang dikelola sendiri (id).

Source names, preserving each official English title where supplied:
- 1. pt: Prospecto de abertura de capital da Moleskine na Itália, 2013; id: Prospektus penawaran saham perdana Moleskine di Italia, 2013
- 2. pt: Moleskine, Our Heritage; id: Moleskine, Our Heritage
- 3. pt: Moleskine, Code of Ethics; id: Moleskine, Code of Ethics
- 4. pt: Apresentação da D’Ieteren a investidores, 2017; id: Presentasi investor D’Ieteren, 2017
- 5. pt: Anúncio da bolsa italiana sobre a estreia de 2013; id: Pengumuman pencatatan bursa Italia, 2013
- 6. pt: Anúncio de aquisição da D’Ieteren, 2016; id: Pengumuman akuisisi D’Ieteren, 2016
- 7. pt: Anúncio da D’Ieteren sobre a conclusão da aquisição, 2017; id: Pengumuman penyelesaian akuisisi D’Ieteren, 2017
- 8. pt: D’Ieteren 2017 Activity Report — Moleskine; id: D’Ieteren 2017 Activity Report — Moleskine
- 9. pt: D’Ieteren 2017 Annual Report; id: D’Ieteren 2017 Annual Report
- 10. pt: D’Ieteren 2025 Full-Year Results; id: D’Ieteren 2025 Full-Year Results
- 11. pt: D’Ieteren 2026 Half-Year Results; id: D’Ieteren 2026 Half-Year Results

Three passes:
1. Draft: translated every requested entry using current scene data, supplied glossary, and cue boundaries.
2. Critique: checked each clause against source order; checked all numbers, dates, euro amounts, corporate attribution, narrator's first person, target register, proper names, scripts, metadata limits and chapter/thumbnail lengths.
3. Final: applied all corrections below; worksheet contains the final text alone.

Critique findings and applied fixes:
- pt r3i032 | Draft asserted audience reach; restore the prospectus's suitability claim. | por isso seriam adequadas ao público que a empresa buscava. Escolher a estante já é contar uma história.
- pt r309021 | Avoid making the name itself the seller. | O mesmo nome podia seguir nas vendas de agendas, artigos de escrita e acessórios de viagem.
- pt r3e101 | Make the gradual requirement explicit. | A empresa passou, aos poucos, a exigir desses distribuidores dados mensais das vendas às lojas,
- pt r313012 | Make agreement signing explicit. | anunciou a assinatura de um acordo para comprar 41% da Moleskine e planejou adquirir as ações restantes.
- pt r3t021 | Make equity valuation distinct from market capitalization and revenue. | O acordo fixou 2,40 euros por ação; avaliou todo o capital acionário em cerca de 506 milhões de euros.
- pt r315021 | Restore the not-yet qualification. | Mochilas, canetas inteligentes e outros acessórios já existiam, mas ainda não tiraram o papel da liderança.
- pt r316011 | Restore the new-platform detail. | As vendas online caíram no ano da migração para uma nova plataforma. Além de investir na experiência de compra, que operações eram necessárias?
- pt r3n012 | Make continuing inventory management explicit. | O relatório financeiro é mais específico: alguns grandes clientes nos Estados Unidos seguiam cautelosos ao gerir o estoque.
- pt r3n041 | Restore financial forecasts and explicit discounting. | Projeções financeiras para os próximos 5 anos descontam os fluxos de caixa futuros a valor presente para testar o valor contábil.
- pt r318051 | Restore the equal-amount cash distinction. | É um recálculo contábil do ativo da marca; não é gasto extra de igual valor naquele ano, nem tantos cadernos devolvidos.
- pt r319011 | Use natural, complete retail-performance wording. | No período mais recente, o primeiro semestre de 2026, o grupo relatou recuperação do atacado nos Estados Unidos e bom desempenho do varejo.
- pt r319021 | Make year-on-year half-year comparison explicit. | As vendas foram de cerca de 52,2 milhões de euros, 2,2% acima do mesmo semestre do ano anterior.
- pt r3n061 | Clarify comparison period. | Comparamos o mesmo semestre de cada ano, não com o ano inteiro anterior. A receita voltou; o resultado operacional acompanhou?
- pt r319041 | Make prior-year comparison explicit. | O resultado operacional foi de 700 mil euros, ligeiramente abaixo do mesmo período do ano anterior.
- pt r320041 | Restore real-world tests. | Para entender pelos objetos do dia a dia como um nome vira negócio e quais desafios reais enfrenta, inscreva-se.
- pt description | Draft strengthened association with old notebooks into a blanket use claim | Restored association and the explicit distinction from the modern brand.
- id r3h011 | Remove casual slang and retain kamu. | Kamu mungkin hanya ingin buku catatan; perusahaan buku hitam kecil ini masuk bursa dengan nilai pasar hampir 500 juta euro.
- id r3h031 | Use everyday Indonesian without slang. | Saya sempat heran: tanpa cerita tercetak, apa yang membuat buku ini menarik untuk kamu?
- id r302021 | Use neutral everyday tidak. | Menurut cerita di situs itu, buku hitam kecil yang biasa dipakainya tidak lagi tersedia:
- id r302031 | State the missing complete factory record explicitly. | Saya rasa kita perlu berhenti sejenak: ini kisah penulis yang diceritakan ulang merek; kita tidak punya arsip lengkap pabrik saat itu.
- id r309021 | Avoid making the name itself the seller. | Nama yang sama bisa terus dipakai untuk menjual agenda, alat tulis, dan aksesori perjalanan.
- id r3e031 | Remove casual slang. | Kamu hanya membawa satu buku dari toko, tetapi di sisi lain jumlah produksi harus diputuskan lebih awal.
- id r313012 | Make signing and subsequent plan explicit. | mengumumkan penandatanganan perjanjian membeli 41% saham Moleskine, lalu berencana membeli sisanya.
- id r3t042 | Restore the direct-evidence qualification. | lalu terhubung ke alat digital; ini arah produk, tidak langsung berarti transformasi berhasil.
- id r316011 | Restore new-platform detail. | Penjualan online turun pada tahun perpindahan ke platform baru. Selain investasi pengalaman belanja, pekerjaan operasional apa yang perlu dilakukan?
- id r3n041 | Restore financial forecasts and natural carrying-value test. | Proyeksi keuangan 5 tahun mendatang mendiskontokan arus kas masa depan ke nilai kini untuk menguji apakah nilai buku bisa dipertahankan.
- id r318051 | Restore equal cash amount. | Jadi, ini perhitungan ulang nilai buku aset merek, bukan tambahan kas keluar sebesar itu pada tahun itu atau buku sebanyak itu dikembalikan.

Checks:
- 143/143 lines and 6/6 chapters filled per locale; 11 source URLs retained exactly per description.
- Titles under 100 characters; chapter names all under 30 characters; tag strings under 500 characters.
- No channel/series name in titles or tags. Thumbnail labels are localized to describe the source's label.
- No Chinese characters, kana or Hangul in any translated text; company/product names stay in Latin letters.
- pt uses você; id uses kamu, saya for narrator's first person, and standard everyday words without slang.
- Financial separation preserved: 2013 listing market capitalization 487.6m euro; 2016 equity valuation 506m euro at 2.40 euro/share; revenue, operating results, impairment and financing effects remain distinct.
- 2025 is the fiscal/reporting year, not the publication year. 1997-11-26 remains the first trademark application date.
- Production-to-launch average of 3–6 months remains an interval, not manufacturing duration; 79 stores remains end-2016; 2013 contract arrangements remain historically scoped.
- Attributed corporate claims remain attributed; the text does not turn positioning into proof of why every customer bought.
- Approximate 80-character caption target: pt mean 89 characters, 91 lines over 80, longest 166 (r319031); id mean 90, 94 over 80, longest 156 (r319031). No max_chars budgets exist in these metadata+CC sheets. Long atomic source entries retain their financial qualifiers and multiple clauses; later caption tooling may split cues. No timing or audio fit is claimed.

Uncertainties: no unresolved semantic or terminology uncertainty identified. Final caption cue readability and thumbnail fit await the authorized later media/timing stage. Parent will perform independent review and serialize merges.
