"""Normalize reviewed editorial spellings without changing program identifiers."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[3]
replacements={
 '交给':'交給','测试':'測試','条件':'條件','独立':'獨立','因为':'因為','下载':'下載',
 '相邻':'相鄰','没有':'沒有','证据':'證據','差异':'差異','目录':'目錄','重写':'重寫',
 '记录':'紀錄','处理':'處理','来源':'來源','路径':'路徑','实际':'實際','询問':'詢問',
 '暂時':'暫時','写入':'寫入','查阅':'查閱','文档':'文件','足够':'足夠','恢复':'恢復',
 '约':'約','分开':'分開','一个':'一個','脚本':'腳本','保留原始輸出而不是只记':'保留原始輸出而不是只記',
 '校验':'驗證','输出':'輸出','输入':'輸入','错误':'錯誤','执行':'執行','验证':'驗證',
 '阅读':'閱讀','已经':'已經','单一':'單一','失败':'失敗','误判':'誤判','确认':'確認',
 '请求':'請求','标准':'標準','并且':'並且','停止条件':'停止條件','补上':'補上',
 '启動':'啟動','名称':'名稱','状态':'狀態','删除':'刪除','响应':'回應','简单':'簡單',
 '重复':'重複','与':'與','后续':'後續','规则':'規則','依据':'依據','发现':'發現','无法':'無法',
 '证据':'證據','条':'條','为了':'為了','任务':'任務','写进':'寫進','触':'觸','计時':'計時',
 '检查':'檢查','説明':'說明',
}
for number in range(61,97):
 path=ROOT/f'docs/claude-code-series/lessons/{number}.md'
 if not path.exists():continue
 text=path.read_text(encoding='utf-8').replace('](/tutorials/claude-code/','](https://mokaair.com/tutorials/claude-code/')
 parts=re.split(r'(```.*?```)',text,flags=re.S)
 for index,part in enumerate(parts):
  if part.startswith('```'):continue
  for before,after in replacements.items():part=part.replace(before,after)
  parts[index]=part
 text=''.join(parts)
 path.write_text(text,encoding='utf-8')
