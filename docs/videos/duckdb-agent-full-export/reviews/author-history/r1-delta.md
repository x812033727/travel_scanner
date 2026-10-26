# 第五片R1精確差異

初稿source `cf4bb2ae8cb8496503ac55308b5fe91d7b8071c1b2117272f4a9808ce733fd0e` → R1 `fc5c2b2dce69763905273e049f32290f613354cc8d068532e67086dcfd2a3da2`。
claims `4768284319dc295bf5cfb3d80bdc709ef9a88c67d6df9f798266f1faa86620ff` → `02bcb6bc2bb7b540b2d5030f37e15fc54334d3f4063c15678e662f455f484dd7`。完整逐line、scene順序、卡片data、全部五欄claim前後值在r1-delta.json，不省略最後「場景」欄。

敘事：68→66景，121→114句。新增景：json-stream-question, copy-limit-question, run-followup, run-readback, source-predicate-check, new-requirement-consequence, run-variant, variant-members-question, different-deliveries。移除景：one-running-task, voice-the-rule, strict-greater, preview-versus-file, upgrade-question, pick-the-tool, agent-mode-fit, lts-is-a-promise, storage-condition, format-is-not-correctness, author-demo-scope。章數仍6，keep-the-rule無新chapter，歸第六章。

claims：23→21項，移除未使用c21（LTS）與c22（格式相容）；其官方事實不被推翻，原source／舊claims／官方來源完整保留。c20縮成這次選用新目錄的方法，c17移除過時「未登記」描述；現有範圍與證據欄完整保留，公開重跑另補證據。其餘行的場景引用依實際R1自動重算且逐一核對。

外部asset新增／修改／刪除均0；沒有render。原生卡片data的每一項變化及新增卡完整列在JSON。舊demo/、runlogs/、sources/逐bytes不動；root封存75檔與第五原始demo93檔均不動。

公開命令是另外一項已執行的路徑正規化：./duckdb、-no-init、兩mode、:memory:，從public-run/實際執行9條命令後才更新5張命令卡。兩張preview卡只有shell續行，其餘3卡原樣一行；全命令比對收據通過。新ZIP是duckdb-public-fixtures.zip，舊duckdb-followup-fixtures.zip保持歷史bytes。runtime symlink不跟隨、不打包。詳細收據與全量oracle在public-command-proof.json、public-run/。
