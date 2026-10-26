# Doraemon remake R4作者提交包

R4只改d1b082：不再向觀眾掛「月球哪裡有生命餘地」的問題，而以原訪談L32–33記述科學資料參與設定討論、結果腳本仍遇困難。後面的真工作問題仍是原作世界如何接上新舞台，c01用八鍬提議借原作道具及辻村的寫作反應給新答案；沒有補電影情節或科學答案。h04→b08的loop說明改為寫作步驟，所有23個端點不變。d1b082只補原有D15的L33證據，其餘134句與claims列、135個ID、115個scene所有非lines欄位、匿名prompt/camera及三端完整Stage requests/keys均精確保留。

R3 core、SOURCE PASS／verify、native2兩份raw與input/binding/merge、外部round2 manifest及兩份runtime狀態，完整封存在`history/r3`（74檔）；更早R1/R2與所有既有票均不改。舊作者native-state是當時的預審記錄，另外以`native-state-after-review.json`保存事後真實actualcount2。A單票scene_first、B單票no_recap與章名advisory未列本次要求。

重播作者來源與免費檢查：

```bash
python docs/videos/brand-story-remakes-20261025/doraemon/build-candidate.py
node docs/videos/brand-story-remakes-20261025/doraemon/build-image-reuse-plan.mjs
node docs/videos/brand-story-remakes-20261025/doraemon/free-checks-r4.mjs
python docs/videos/brand-story-remakes-20261025/doraemon/freeze-author.py
```

免費runtime在`/workspace/work/brand-story-20261025/doraemon-audit/author-r4/free-runtime`，media另在`author-r4/media`。檢查只複製既有immutable字典的原bytes，不初始化、重建或改字典；正常CLI lint及tts --dry-run使用空ctx.home/env，無憑證讀取或網路。沒有真TTS、音訊、blind payload、模型讀者或批准。

最終3104 native spokenUnits、135行、115 shots、23 loops；免費lint 0 errors、16 soft、0 narrative warnings，完整soft保留。純口播4.5units/s算式689.78秒、native正常間隔估值約14.5分鐘，都不是實聲。薄稿容量風險保持，不宣稱actual FAIL；13分鐘與實聲body720–840秒不變，含cold open及voiced CTA，排新增5秒片頭＋21秒v4片尾，不慢播、不加空白、不重述或切碎填長。繁中試燒+CC、後續八語及乾淨主片保留要求不變。

研究3檔、42下載、213保護項、old9原件與後台snapshot、全部歷史與原runtime、native1/2外部收據、immutable字典1 version/1 event均核SHA不變。源站503與快取仍如實分開。圖中不得出現可識別角色、剪影、招牌道具、真人臉、logo或可讀字；只規劃匿名工作台、空白panel與一般工具。三端same-asset仍false，後續需回收takes1、live cache miss即停、三端judge與裁切後／組片實檔SHA相同。

actualcount保持2，R4未prepare或重抽blind；SOURCE新差分與fresh native3由root另派。當前無verify，R3舊verify只留歷史。念法、實聲、實圖、owner及獨立US$25精確帳戶／全片quote／protected admission均pending。沒有backend、Git、provider、付費或owner操作。
