# 第 1 集接手狀態（2026-11-07 06:54 UTC，Colab 帳號 A 收尾）

- 草稿 28 鏡：out/（c19 剪成 73 格、c26 39 格在 trimmed/；h3.sh cuts 已跑）
- 精修完成（1312×736）：st2/refined/ c01 c01b c02 c03 c04 c05 c06 c07 c08（c01b c02 c03 c05 c08 之後會被重拍版取代）
- c23 重拍草稿：retake/out/c23.mp4（站著，已選用）
- 重拍（retake3，審片後 10 鏡改寫正文）：完成 c01b-r1 c02-r1 c03-r1；c05 起未完成（Colab kernel 兩次卡住逾時）
  還要拍：c05 c08 c12(兩個) c15 c16 c17 c18(兩個) c22 → retake3/retake3.json 去掉已完成的三筆，cd retake3 再跑
- 還要精修：不用重拍的 c09 c10 c11 c13 c14 c19 c20 c21 c23 c24 c25 c26 c27（st2/st2-part*.json --only），
  與挑好的重拍（post/st2.py --st1 retake3/st1-all.json 的子集 --drafts retake3/trimmed --take …）
- 換帳號後：bootstrap 重新取 Colab 憑證；H3_PROFILE=hero bootstrap.sh patch；一律 cd 到 manifest 所在資料夾再 batch
- 後製：e001-post/（audio 19 句、music 兩首、edit 表在 repo post/edit-e001.json；音效庫 post/sfx.sh 重建）
