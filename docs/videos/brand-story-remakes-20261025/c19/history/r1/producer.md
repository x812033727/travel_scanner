# C19 R1 製作交接

本檔僅recipe；paid/provider/backend/Git均0。video無series欄，context的series.json僅供普通不可變字典及企劃使用。正常prepare-runtime.mjs c19初始化到/workspace/work/brand-story-20261025/c19-submission-root，media base /workspace/work/brand-story-20261025/media；只跑免費lint，不跑聲音/圖片/審圖/組片。

## 中文

voice整個物件逐字採C06 Sulafat設定（沒有複製別集字典）；本集字典透過initializeStoryLexicon建立不可變snapshot。13分鐘目標，全文約3500 native units，尚無實聲，不能把字量當通過。繁中燒錄+CC；5秒頻道片頭在coldopen後，21秒正式v4片尾在有聲CTA後。所有媒體尚未辨識/讀回。

## 兩組同圖

h05→a18、h06→n10按正文順序。image-reuse-plan.json載完整計畫輸入與兩端本地Stage.imageKey相等。正常入場後先payoff --takes 1；實際第一take通過並仍被選中後，第二命令之前，讀真manifest選圖與真media/cache.json、重算live request key，兩個實體檔各自SHA均須吻合。cache缺或錯立即停止，不能讓teaser命令另外買圖。不要用會刪錯cache的cached()當唯讀guard。

兩端各走正常judge；完成後讀官方manifest，確認相同selected路徑與真bytes SHA，裁切後仍要相同最終derived檔。不能拿原圖SHA當裁切後SHA。組片前再核對實際輸入。actual_same_asset_verified保持false，實檔欄null，直到以上真查完。

## 其他保護

只改c19新版文件；old66檔、外部唯讀快照及研究三檔原SHA均保護。沒有FSA原件；不增加首創、每卡可用、逐筆網費、單機淨利、災難切換成功、紙鈔直接再出款、運鈔路線或店員接內機。獨立source/native另派，作者不寫verify或任何批准。
