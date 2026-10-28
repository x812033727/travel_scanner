#!/usr/bin/env python3
"""Rehearse the exact public-kit commands in an isolated scratch directory.
No installation/download. The validated existing CLI is symlinked, never bundled.
"""
from pathlib import Path
from datetime import datetime,timezone
import csv,hashlib,json,shutil,subprocess,zipfile
BASE=Path(__file__).resolve().parent
PUB=BASE/'public-run'
BINARY=BASE.parent/'fifth-demo/bin/duckdb'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def record(p):return {'bytes':p.stat().st_size,'sha256':sha(p)}
def main():
 for n in ['demo/input','demo/output','runlogs']:(PUB/n).mkdir(parents=True,exist_ok=True)
 for p in sorted((BASE/'demo').glob('*.sql')):shutil.copyfile(p,PUB/'demo'/p.name)
 shutil.copyfile(BASE/'demo/input/parcels.csv',PUB/'demo/input/parcels.csv')
 shutil.copyfile(BASE/'LICENSE-ORIGINAL.txt',PUB/'LICENSE-ORIGINAL.txt')
 link=PUB/'duckdb'
 if link.is_symlink():assert link.resolve()==BINARY.resolve()
 else:assert not link.exists();link.symlink_to(BINARY)
 runs=[]
 cmds=[('version',['./duckdb','--version']),('human-preview',['./duckdb','-no-init','-no-agent',':memory:','-f','demo/preview.sql']),('agent-preview',['./duckdb','-no-init','-agent',':memory:','-f','demo/preview.sql']),('human-typo',['./duckdb','-no-init','-no-agent',':memory:','-f','demo/typo.sql']),('agent-typo',['./duckdb','-no-init','-agent',':memory:','-f','demo/typo.sql']),('agent-followup',['./duckdb','-no-init','-agent',':memory:','-f','demo/followup.sql']),('human-followup',['./duckdb','-no-init','-no-agent',':memory:','-f','demo/followup.sql']),('readback',['./duckdb','-no-init','-no-agent',':memory:','-f','demo/readback.sql']),('variant',['./duckdb','-no-init','-agent',':memory:','-f','demo/variant.sql'])]
 for name,argv in cmds:
  r=subprocess.run(argv,cwd=PUB,capture_output=True,timeout=15)
  out=PUB/'runlogs'/f'{name}.stdout.txt';err=PUB/'runlogs'/f'{name}.stderr.txt'
  out.write_bytes(r.stdout);err.write_bytes(r.stderr)
  rec={'name':name,'argv':argv,'shell_command':' '.join(argv),'cwd':str(PUB),'observed_at_utc':datetime.now(timezone.utc).isoformat(),'exit_code':r.returncode,'stdout':record(out),'stderr':record(err)}
  if name.endswith('followup'):rec['export_after_this_mode']=record(PUB/'demo/output/late-followup.csv')
  (PUB/'runlogs'/f'{name}.command.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n');runs.append(rec)
  assert r.returncode==(1 if 'typo' in name else 0),(name,r.stderr)
 assert 'v2.0.0 (Cyanoptera) d54cbbe3df' in (PUB/'runlogs/version.stdout.txt').read_text()
 assert '1200 rows (40 shown) 5 columns' in ' '.join((PUB/'runlogs/human-preview.stdout.txt').read_text().split())
 assert '| … 1160 rows omitted … |' in (PUB/'runlogs/agent-preview.stdout.txt').read_text()
 stderr=(PUB/'runlogs/agent-typo.stderr.txt').read_text();parts=stderr.splitlines()
 assert len(parts)==2 and parts[0].startswith('duckdb agent mode on')
 obj=json.loads(parts[1]);assert obj['error_subtype']=='COLUMN_NOT_FOUND' and obj['name']=='actual_day' and '"actual_days"' in obj['exception_message']
 try:json.loads(stderr)
 except json.JSONDecodeError:pass
 else:raise AssertionError('mixed stderr unexpectedly parsed as one JSON object')
 def rows(n):
  with (PUB/n).open(newline='') as f:return list(csv.DictReader(f))
 source=rows('demo/input/parcels.csv');mainrows=rows('demo/output/late-followup.csv');variant=rows('demo/output/due-or-late.csv')
 def expected(inclusive):
  result=[]
  for r in source:
   if r['status']!='delivered':continue
   a,p=int(r['actual_days']),int(r['promised_days'])
   if not (a>=p if inclusive else a>p):continue
   result.append({'parcel_id':r['parcel_id'],'route':r['route'],'promised_days':str(p),'actual_days':str(a),'days_late':str(a-p)})
  return sorted(result,key=lambda r:r['parcel_id'])
 assert len(source)==1200 and mainrows==expected(False) and len(mainrows)==480
 assert variant==expected(True) and len(variant)==720
 assert sum(r['days_late']=='0' for r in variant)==240
 assert (PUB/'demo/output/late-followup.csv').read_bytes()==(PUB/'demo/output/parquet-readback.csv').read_bytes()==(BASE/'demo/output/late-followup.csv').read_bytes()
 assert sha(PUB/'demo/output/due-or-late.csv')==sha(BASE/'demo/output/due-or-late.csv')
 exports=[r['export_after_this_mode']['sha256'] for r in runs if r['name'].endswith('followup')];assert len(set(exports))==1
 result={'status':'PASS','scope':'Exact public-root ./duckdb commands actually executed on Linux using a symlink to the already validated official2.0 CLI. No binary bundled, no installation/network/AI-product use.','binary':{'path':str(BINARY),'sha256':sha(BINARY),'bytes':BINARY.stat().st_size,'version':(PUB/'runlogs/version.stdout.txt').read_text().strip()},'input_rows':1200,'preview_displayed':40,'preview_omitted':1160,'main_rows':480,'variant_rows':720,'variant_exactly_on_time_rows':240,'same_version_modes':True,'both_mode_full_csv_identical':True,'all_main_rows_all_values_equal_source_oracle':True,'all_variant_rows_all_values_equal_changed_predicate_oracle':True,'parquet_readback_byte_equal':True,'agent_error_json_line_valid':True,'whole_stderr_single_json':False,'original_main_csv_equal':True,'original_variant_csv_equal':True,'runs':runs}
 (PUB/'public-run-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 commands='\n\n'.join('```sh\n'+r['shell_command']+'\n```' for r in runs)
 readme='''# 完整配送清單教材：公開根目錄重做

本教材是原創1200筆虛構配送資料與確定性作者SQL，非真公司／個資／公共統計；沒有獨立AI產品或模型測試。原創fixture、SQL、文字與紀錄採CC0-1.0，DuckDB另採MIT。

解壓後，以這個README所在的根目錄為目前工作目錄。另從DuckDB官方取得適合自己平台的2.0 CLI，依其MIT授權使用。這份實際紀錄只測Linux amd64的v2.0.0 (Cyanoptera) d54cbbe3df；不承諾其他OS已實測。Linux範例把可執行檔放在根目錄，名稱為duckdb。執行檔／symlink／官方壓縮包不在教材內。

這輪工作區用symlink ./duckdb指向已驗官方同版本CLI，再執行以下原樣命令。公開路徑不是只改字，raw記錄在runlogs/，完整核對結果在public-run-results.json。跨平台的檔名與可執行方式可能不同，以下是本輪Linux實際命令。

setup.sql明確停用extension自動安裝／載入；每個查詢用臨時資料庫並略過初始化檔。先執行preview，再執行故意錯字示範；typo兩條預期exit1且不產生查詢結果。其餘命令預期exit0。輸出目錄demo/output/已在教材中；再次執行會重產生其中教學檔案。

## 完整原樣命令

'''+commands+'''

## 核對與自行改需求

完整SQL在demo/。followup.sql的主條件是status='delivered' AND actual_days>promised_days，交付480筆；先比較模式時，兩者使用同一版本和同一SQL。40是1200筆原表的顯示列數，1160 omitted只是沒有顯示，不是資料遺失。

CSV與Parquet含包裹代號、路線、承諾天數、實際天數、晚到天數，按包裹代號升冪。readback.sql讀回Parquet並存成CSV，與主CSV逐bytes相同；public-run-results.json另以標準函式庫逐列核對所有欄位及原始條件。

variant.sql把>改>=，另存due-or-late.csv；得到剛好準時或晚到720筆，其中240筆差值為0。不包含早到；不把這720筆全叫延遲。原480筆檔案保持。修改自己的需求時，同時改比較條件與目的檔名，再執行、核對。

agent-typo.stderr.txt第一行是啟動文字，第二行才是一個合法JSON物件。整個stderr不是單一JSON文件；讀取程式要先辨認訊息行，再解析JSON行。這是讀取契約的區分，不是DuckDB產生壞JSON，也不代表真第三方工具已故障。

完整輸入／SQL／輸出／raw紀錄的SHA在public-kit-manifest.json。SHA是核對檔案身份，不是AI正確性、速度、token或費用測試。
'''
 (PUB/'README.md').write_text(readme)
 files={str(p.relative_to(PUB)):record(p) for p in sorted(PUB.rglob('*')) if p.is_file() and not p.is_symlink() and p.name!='public-kit-manifest.json'}
 index={'scope':'Small original reproducible fixtures and exact Linux public-root run receipts; binary/symlink intentionally excluded.','self_excluded':'public-kit-manifest.json','files':files}
 (PUB/'public-kit-manifest.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n')
 dest=BASE/'duckdb-public-fixtures.zip'
 with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n in sorted(list(files)+['public-kit-manifest.json']):z.write(PUB/n,arcname='duckdb-followup-fixtures/'+n)
 with zipfile.ZipFile(dest) as z:
  assert z.testzip() is None and not any(n.endswith('/duckdb') for n in z.namelist())
  for n,r in files.items():assert hashlib.sha256(z.read('duckdb-followup-fixtures/'+n)).hexdigest()==r['sha256']
 (BASE/'public-command-proof.json').write_text(json.dumps({'verified_at_utc':datetime.now(timezone.utc).isoformat(),'path_scope_separate_from_story_rewrite':True,'results_path':'public-run/public-run-results.json','results':record(PUB/'public-run-results.json'),'readme':record(PUB/'README.md'),'zip':record(dest),'zip_entries':len(files)+1,'excluded_runtime_symlink':'public-run/duckdb','archive_before_r1_not_written':True,'fifth_demo_not_written':True},ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'status':'PASS','runs':len(runs),'main_rows':480,'variant_rows':720,'public_zip':record(dest),'zip_entries':len(files)+1},ensure_ascii=False))
if __name__=='__main__':main()
