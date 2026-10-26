# Independent ES / PT / ID review

Source `e6e87e77f069a574d6e1d7f47bf2e5be031eb8566bb2edb71defa24ae4c2b99f`; claims `527048b6061d21f70e00475cc4790a46b0de6e536a37e8966402194a043fa9c6`. Independently read 315 current captions, 21 chapters, all metadata and nine thumbnail words. Three rounds covered source meaning, natural spoken text, and static character budgets. No actual dub fit was tested.

## Required fixes

| Locale / ID | Reason | Proposed |
|---|---|---|
| id / kfft | “mengubahnya”紧接Batas，通常回指上限；源句要求没有其他执行者修改计数器，这项假设支撑后面的确定性循环。必须点名penghitung。 | Batas tetap; penghitung tidak diubah pihak lain. |
| id / z9dp | 须禁止错误输入通过，而不是把错误输入排除出输入域；加lolos保留一方向接受条件，仍问全拒绝是否足够。 | Catatan cuma larang input salah lolos; tolak semua cukup? |
| id / 7ip9 | “versi biasa dan pemeriksa galat”容易变成一般版与错误检查器两种对象；须明确是同一程序的一般版和带错误检查的版本，保留不是修正前后的对比。 | Rilis publik: program sama, versi normal dan versi cek galat; bukan sebelum dan sesudah perbaikan. |
| es / wi26 | 原句四项名词串接，没有自然表达检查主体与对象；补revisan明确Rocq核心和工具检查命题、假设，保留开场回收。 | La duda inicial: núcleo Rocq y herramientas revisan proposición y supuestos. |
| es / description | Reserve 1 terminator byte within capacity 8; scope the missing halts proof to this release only. | Full old/proposed text, preserving paragraphs and URL, is in JSON. |
| pt / description | Reserve 1 terminator byte within capacity 8; scope the missing halts proof to this release only. | Full old/proposed text, preserving paragraphs and URL, is in JSON. |
| id / description | Reserve 1 terminator byte within capacity 8; scope the missing halts proof to this release only. | Full old/proposed text, preserving paragraphs and URL, is in JSON. |

## Static budget review

| Locale | Initial excesses | Fitting candidates | Unresolved | Snapshot SHA |
|---|---:|---:|---:|---|
| es | 27 | 15 | 12 | `864df775ca153d3b7e3876d31bf466e503e252c1e4be21a937cad0c40d2e9a3c` |
| pt | 38 | 23 | 15 | `7039ecdf73435aee76a45411456addb261e5601add0f9cd10e946f80d08d4ab6` |
| id | 28 | 25 | 3 | `496ec40177f66f52554f8f89ab85694ed675404dfce1946e75426a78422432ad` |

### es

| ID | Old / max | Candidate / max | Result | Candidate |
|---|---:|---:|---|---|
| z9dp | 65 / 59 | 58 / 59 | fits statically | Registro: solo no aceptar inválidos. ¿Rechazar todo basta? |
| bpnn | 70 / 64 | 59 / 64 | fits statically | Falta el retorno: ¿el otro programa contador de veras sale? |
| c8r2 | 61 / 57 | 56 / 57 | fits statically | AI crea la prueba del mismo requisito. ¿Quién la revisa? |
| qwaw | 91 / 74 | 83 / 74 | unresolved | Este registro aclara dudas de verificación del estudio de Claude del 22 de octubre. |
| 4rff | 72 / 43 | 63 / 43 | unresolved | Los requisitos de prueba se vuelven proposiciones comprobables. |
| 936d | 91 / 68 | 68 / 68 | fits statically | Calcula sin truncar; guarda el total en entero sin signo de 16 bits. |
| s57e | 88 / 75 | 74 / 75 | fits statically | Si reduces a 8 bits y guardas en una variable más ancha, 0 sigue siendo 0. |
| yavq | 65 / 63 | 63 / 63 | fits statically | Cambia toda la línea: cálculo y conversión al guardar el total. |
| 2zma | 75 / 72 | 71 / 72 | fits statically | Es pequeño: puede probarse entero; el solucionador no añade respuestas. |
| 4bqi | 76 / 72 | 67 / 72 | fits statically | Si el registro solo veta inválidos, ¿vale entregar rechazando todo? |
| w9b4 | 61 / 53 | 53 / 53 | fits statically | Registro unilateral inicial: ya exige aceptar válidos |
| dkjy | 78 / 68 | 66 / 68 | fits statically | Fila: decisión de aceptar; el código no escribe en búfer de datos. |
| u2xw | 76 / 62 | 74 / 62 | unresolved | Uso otro programa contador independiente para el retorno; entra el límite. |
| rsx8 | 86 / 82 | 80 / 82 | fits statically | Separé aceptación y retorno. ¿Las pruebas del estudio de Claude cubren lo mismo? |
| zg4q | 88 / 84 | 95 / 84 | unresolved | Al cotejar registro y prueba formal, fija versión del programa, proposición y modelo operativo. |
| cawx | 65 / 38 | 58 / 38 | unresolved | Al compilar, el núcleo Rocq revisa pruebas creadas por AI. |
| uqde | 89 / 62 | 75 / 62 | unresolved | La herramienta coteja resultado y proposición fija; lista supuestos usados. |
| 5fga | 76 / 58 | 68 / 58 | unresolved | Los supuestos usados deben pasar la auditoría de la lista permitida. |
| 7ip9 | 100 / 79 | 103 / 79 | unresolved | La pública compara el mismo programa normal y con control de errores, no antes y después de corregirlo. |
| 6x7t | 110 / 57 | 105 / 57 | unresolved | En el modelo del sistema, la entrada debe mantener la versión normal en el presupuesto de memoria fijado. |
| 5u3j | 56 / 47 | 46 / 47 | fits statically | Con esa premisa, ambas evitan errores fijados. |
| i2pt | 79 / 74 | 71 / 74 | fits statically | Anota versión; separa el total del estudio y la versión pública actual. |
| 3u2q | 87 / 66 | 65 / 66 | fits statically | Ambos con C ejecutado de contraste; no corrí el verificador Rocq. |
| ucn4 | 90 / 71 | 70 / 71 | fits statically | Mis resultados solo son de 2 casos locales; no certifican toda la app. |
| edry | 72 / 50 | 55 / 50 | unresolved | No cotejes código corregido y respuestas de otro viejo. |
| mhjn | 40 / 28 | 36 / 28 | unresolved | Fija criterios claros de aceptación. |
| 22tu | 62 / 58 | 60 / 58 | unresolved | Suscríbete: entendamos estudios de AI con resultados reales. |

### pt

| ID | Old / max | Candidate / max | Result | Candidate |
|---|---:|---:|---|---|
| bpnn | 67 / 57 | 56 / 57 | fits statically | Falta anotar retorno: outro programa contador sai mesmo? |
| c8r2 | 55 / 50 | 49 / 50 | fits statically | A AI cria prova do mesmo requisito. Quem confere? |
| qwaw | 82 / 66 | 80 / 66 | unresolved | O registro responde dúvidas de verificação do estudo de Claude de 22 de outubro. |
| 4rff | 68 / 39 | 51 / 39 | unresolved | Requisitos de teste viram proposições verificáveis. |
| fzz5 | 49 / 48 | 44 / 48 | fits statically | Cabem 8 bytes; reserve 1 byte ao terminador. |
| 936d | 86 / 60 | 60 / 60 | fits statically | Cálculo completo; total salvo: inteiro de 16 bits sem sinal. |
| yavq | 58 / 56 | 56 / 56 | fits statically | Mude a linha toda: cálculo e conversão ao salvar o total |
| mfag | 44 / 42 | 44 / 42 | unresolved | Supera a capacidade 8: rejeita corretamente. |
| zgkb | 79 / 69 | 65 / 69 | fits statically | Registro um modelo de solução: mesma entrada em 8 bits booleanos. |
| gtuj | 51 / 50 | 50 / 50 | fits statically | Acha 255 na errada; na ampliada não acha tal caso. |
| 2zma | 80 / 64 | 64 / 64 | fits statically | Faixa pequena: dá para testar tudo; solver não dá nova resposta. |
| 4bqi | 72 / 64 | 64 / 64 | fits statically | Se o registro só veta inválidos, posso entregar rejeitando tudo? |
| 7d4v | 53 / 52 | 45 / 52 | fits statically | Se só veta inválidos, cumpre rejeitando tudo. |
| w9b4 | 56 / 47 | 57 / 47 | unresolved | Registro inicial unilateral: agora exige aceitar válidas. |
| dkjy | 80 / 61 | 56 / 61 | fits statically | Decisão de aceitar; código não grava no buffer de dados. |
| u2xw | 72 / 55 | 72 / 55 | unresolved | Uso outro programa contador independente para o retorno; entra o limite. |
| kq36 | 66 / 59 | 59 / 59 | fits statically | Grafo de controle inteiro: ciclo 256 passos; modelo não sai |
| qjaw | 73 / 60 | 60 / 60 | fits statically | Timeout é o observado; ciclo no grafo de controle é a razão. |
| p8te | 61 / 55 | 55 / 55 | fits statically | Contador e conversão: use inteiros de 16 bits sem sinal |
| ey22 | 80 / 74 | 69 / 74 | fits statically | Retorno registrado: para toda entrada, sai e retorna o limite mais 1. |
| rsx8 | 79 / 73 | 71 / 73 | fits statically | Separei aceitação e retorno. Provas do estudo de Claude checam o mesmo? |
| zg4q | 89 / 75 | 93 / 75 | unresolved | Ao ligar o registro à prova formal, fixe versão do programa, proposição e modelo operacional. |
| cawx | 59 / 34 | 56 / 34 | unresolved | Ao compilar, o núcleo Rocq checa provas criadas pela AI. |
| uqde | 83 / 55 | 72 / 55 | unresolved | A ferramenta coteja resultado e proposição fixa; lista hipóteses usadas. |
| 5fga | 72 / 52 | 65 / 52 | unresolved | As hipóteses usadas devem passar na auditoria da lista permitida. |
| wi26 | 99 / 70 | 66 / 70 | fits statically | Dúvida inicial: núcleo Rocq e ferramentas checam tese e hipóteses. |
| 7ip9 | 110 / 70 | 101 / 70 | unresolved | A pública compara o mesmo programa normal e com verificação de erros, não antes e depois da correção. |
| 6x7t | 104 / 51 | 91 / 51 | unresolved | No modelo do sistema, a entrada deve manter a versão normal no orçamento de memória fixado. |
| 5u3j | 52 / 42 | 40 / 42 | fits statically | Sob a premissa, ambas evitam erros-alvo. |
| cnnu | 60 / 50 | 45 / 50 | fits statically | Traços finitos podem conter texto já emitido. |
| cr5k | 58 / 57 | 57 / 57 | fits statically | Informe oficial: 123 bibliotecas e 239 pontos de entrada. |
| 3u2q | 82 / 59 | 63 / 59 | unresolved | Confrontei ambos com C executado; não rodei o verificador Rocq. |
| ucn4 | 84 / 63 | 62 / 63 | fits statically | Meus resultados: só 2 casos locais; não certificam todo o app. |
| bt2j | 80 / 69 | 66 / 69 | fits statically | Separo correções do total e do contador: declaração e atualização. |
| mj65 | 65 / 61 | 59 / 61 | fits statically | Ao repetir, confira versão; esperado e real na mesma linha. |
| edry | 72 / 45 | 56 / 45 | unresolved | Não coteje código corrigido e respostas de outro antigo. |
| mhjn | 40 / 25 | 32 / 25 | unresolved | Fixe critérios claros de aceite. |
| 22tu | 65 / 52 | 60 / 52 | unresolved | Inscreva-se: entendamos pesquisa de AI com resultados reais. |

### id

| ID | Old / max | Candidate / max | Result | Candidate |
|---|---:|---:|---|---|
| bpnn | 65 / 64 | 62 / 64 | fits statically | Return belum dicatat. Benarkah program penghitung lain keluar? |
| 4rff | 58 / 43 | 42 / 43 | fits statically | Syarat uji jadi proposisi yang bisa dicek. |
| 5iky | 60 / 59 | 58 / 59 | fits statically | Penjumlahan dipromosikan ke int, tak langsung menjadi nol. |
| zfmi | 64 / 53 | 53 / 53 | fits statically | Versi salah: ubah total ke integer 8 bit tanpa tanda. |
| dfhy | 78 / 76 | 73 / 76 | fits statically | Tambahan yang diterima versi salah cuma 255; versi lebar cuma 0 sampai 7. |
| 4bqi | 76 / 72 | 72 / 72 | fits statically | Jika catatan cuma larang input salah lolos, bisa serahkan penolak semua? |
| xfvp | 63 / 62 | 61 / 62 | fits statically | Aturan satu arah: tolak semua mencegah input tidak sah lolos. |
| cabc | 52 / 50 | 44 / 50 | fits statically | Panjang 0 sampai 7 pun tidak ada yang lolos. |
| 7d4v | 87 / 59 | 59 / 59 | fits statically | Larang input salah lolos saja: program cukup menolak semua. |
| w9b4 | 58 / 53 | 53 / 53 | fits statically | Catatan awal satu arah kini: input sah wajib diterima |
| dkjy | 77 / 68 | 67 / 68 | fits statically | Baris ini: keputusan penerimaan; kode tidak menulis ke buffer data. |
| 8ywa | 64 / 63 | 62 / 63 | fits statically | Saya catat dua nol: versi lebar tak salah terima maupun tolak. |
| v9sd | 67 / 62 | 60 / 62 | fits statically | Penghitung tak melebihi batas: tambah 1; jika tidak, keluar. |
| riuf | 60 / 58 | 56 / 58 | fits statically | Jumlah kenaikan dan return harus sebesar batas tambah 1. |
| ihny | 75 / 74 | 68 / 74 | fits statically | Waktu habis saja tidak membuktikan program tak akan pernah berakhir. |
| ey22 | 87 / 83 | 81 / 83 | fits statically | Kolom return terisi: tiap input, program keluar dan mengembalikan batas tambah 1. |
| cawx | 54 / 38 | 48 / 38 | unresolved | Saat kompilasi, kernel Rocq cek bukti buatan AI. |
| uqde | 73 / 62 | 62 / 62 | fits statically | Alat cocokkan hasil ke proposisi tetap, catat asumsi terpakai. |
| 5fga | 61 / 58 | 51 / 58 | fits statically | Asumsi terpakai juga harus lolos audit daftar izin. |
| 7ip9 | 119 / 79 | 98 / 79 | unresolved | Rilis publik: program sama, versi normal dan versi cek galat; bukan sebelum dan sesudah perbaikan. |
| 6x7t | 104 / 57 | 88 / 57 | unresolved | Di model sistem, input harus menjaga versi normal dalam anggaran memori yang ditetapkan. |
| 5u3j | 62 / 47 | 41 / 47 | fits statically | Dengan itu, keduanya bebas galat sasaran. |
| te3s | 65 / 61 | 60 / 61 | fits statically | Catat metode uji juga agar beda hasil yang diserahkan jelas. |
| 3u2q | 93 / 66 | 64 / 66 | fits statically | Keduanya dicek via eksekusi C; saya tak jalankan pemeriksa Rocq. |
| bt2j | 94 / 77 | 77 / 77 | fits statically | Catatan memisahkan revisi total panjang, deklarasi, dan pembaruan penghitung. |
| mj65 | 89 / 68 | 66 / 68 | fits statically | Saat ulang, cek versi dulu; ekspektasi dan hasil nyata satu baris. |
| edry | 67 / 50 | 47 / 50 | fits statically | Jangan cocokkan revisi ke hasil kode lama lain. |
| mhjn | 37 / 28 | 27 / 28 | fits statically | Perjelas syarat penerimaan. |

## Scope checks

- 0..255 domain; 8-byte capacity with 1 terminator byte inside it; acceptance iff 0..7.
- 255+1 is int 256 after promotion, then unsigned 8-bit narrowing stores 0; bits differ from bytes.
- Wide calculation/casts and total storage both preserve the full value; widening after narrowing cannot recover 256.
- Only widened guard has no counterexample in both SAT directions; reject-all is symbolic, not another compiled C run.
- Guard only decides Boolean acceptance; no buffer write.
- Counter is independent, fixed limit, no other counter writer; 0.25-second timeout alone is not proof; finite 256-step cycle gives the reason.
- Counter declaration and update cast are both fixed to unsigned 16-bit; every input exits and returns limit+1.
- Rocq kernel checks AI-written proofs at compilation, tool checks fixed statement and lists used assumptions, then allowlist audit.
- Public proof compares normal and error-checked builds of same program; premise concerns normal-build specified memory budget in system model. Both exclude specified errors and have equal allowed observable finite-trace sets.
- No halts proof conclusion applies only to this public release. Study 123 libraries/239 entries vs public 60 entries/25 libraries retained.
- Local actual C comparisons are not Rocq reproduction or certification of the entire application.
- Product names, dates, full pinned URL and original-SVG provenance preserved; no invented Chinese pronunciations.

Fitting candidates are reviewer proposals, not applied translations or proof of actual audio fit. Unresolved rows retain all source constraints in the proposed full wording. No max_chars was edited. Contextual pronouns and ordinary full-word equivalents are used; no word fragments or Chinese pronunciation substitutions.

All edits remain proposals. No worksheet, source, media, merge state, paid service, backend or git operation changed. Author self-review was consulted after the independent read and was not treated as proof.
