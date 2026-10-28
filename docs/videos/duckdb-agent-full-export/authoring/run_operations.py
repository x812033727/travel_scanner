#!/usr/bin/env python3
"""Readable teaching SQL replay, writes only this fifth-draft directory."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,csv
BASE=Path(__file__).resolve().parent
OLD=BASE.parent/'fifth-demo'
BIN=Path('../fifth-demo/bin/duckdb')
FILES={
'setup.sql':"""SET autoinstall_known_extensions=false;
SET autoload_known_extensions=false;
SET threads=1;
SET memory_limit='128MB';
CREATE TABLE parcels AS
SELECT * FROM read_csv('demo/input/parcels.csv',
  columns={'parcel_id':'VARCHAR','route':'VARCHAR',
           'promised_days':'INTEGER','status':'VARCHAR',
           'actual_days':'INTEGER'},header=true);
""",
'preview.sql':""".read demo/setup.sql
SELECT * FROM parcels
ORDER BY parcel_id;
""",
'typo.sql':""".read demo/setup.sql
SELECT parcel_id, actual_day
FROM parcels LIMIT 1;
""",
'followup.sql':""".read demo/setup.sql
DESCRIBE parcels;
SELECT status,count(*) AS records
FROM parcels GROUP BY status ORDER BY status;
SELECT route,count(*) AS delivered_late
FROM parcels
WHERE status='delivered' AND actual_days>promised_days
GROUP BY route ORDER BY route;
COPY (
 SELECT parcel_id,route,promised_days,actual_days,
        actual_days-promised_days AS days_late
 FROM parcels
 WHERE status='delivered' AND actual_days>promised_days
 ORDER BY parcel_id
) TO 'demo/output/late-followup.csv' (HEADER,DELIMITER ',');
COPY (
 SELECT parcel_id,route,promised_days,actual_days,
        actual_days-promised_days AS days_late
 FROM parcels
 WHERE status='delivered' AND actual_days>promised_days
 ORDER BY parcel_id
) TO 'demo/output/late-followup.parquet' (FORMAT PARQUET);
SELECT count(*) AS exported_rows
FROM read_csv('demo/output/late-followup.csv');
""",
'readback.sql':"""SET autoinstall_known_extensions=false;
SET autoload_known_extensions=false;
COPY (
 SELECT * FROM 'demo/output/late-followup.parquet'
 ORDER BY parcel_id
) TO 'demo/output/parquet-readback.csv' (HEADER,DELIMITER ',');
"""}
def main():
 for p in ['demo/input','demo/output','runlogs']:(BASE/p).mkdir(parents=True,exist_ok=True)
 (BASE/'demo/input/parcels.csv').write_bytes((OLD/'input/parcels.csv').read_bytes())
 for n,s in FILES.items():(BASE/'demo'/n).write_text(s)
 runs=[]
 for name,mode,file in [('human-preview','-no-agent','preview.sql'),('agent-preview','-agent','preview.sql'),('human-typo','-no-agent','typo.sql'),('agent-typo','-agent','typo.sql'),('followup','-agent','followup.sql'),('human-followup','-no-agent','followup.sql'),('readback','-no-agent','readback.sql')]:
  cmd=[str(BIN),'-no-init',mode,':memory:','-f','demo/'+file]
  r=subprocess.run(cmd,cwd=BASE,text=True,capture_output=True,timeout=15)
  (BASE/'runlogs'/(name+'.stdout.txt')).write_text(r.stdout)
  (BASE/'runlogs'/(name+'.stderr.txt')).write_text(r.stderr)
  rec={'argv':cmd,'cwd':str(BASE),'observed_at_utc':datetime.now(timezone.utc).isoformat(),'exit_code':r.returncode,'stdout_sha256':hashlib.sha256(r.stdout.encode()).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr.encode()).hexdigest()}
  (BASE/'runlogs'/(name+'.command.json')).write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n');runs.append({'name':name,**rec})
  assert (r.returncode!=0)==('typo' in name),(name,r.stderr)
 a=(BASE/'demo/output/late-followup.csv').read_bytes();z=(BASE/'demo/output/parquet-readback.csv').read_bytes()
 assert a==z==(OLD/'output/late-followup.csv').read_bytes()
 with (BASE/'demo/output/late-followup.csv').open() as f:rows=list(csv.DictReader(f))
 assert len(rows)==480
 source=(BASE/'demo/input/parcels.csv').read_bytes()
 result={'status':'PASS','input_same_sha_as_research':hashlib.sha256(source).hexdigest()==hashlib.sha256((OLD/'input/parcels.csv').read_bytes()).hexdigest(),'full_csv_sha256':hashlib.sha256(a).hexdigest(),'full_csv_rows':480,'parquet_roundtrip_byte_equal':True,'equivalent_to_original_research_csv':True,'replay_scope':'Readable SQL formatting, same fixed2.0 binary; author deterministic fixture and script, no independently prompted model or AI product session.','runs':runs}
 (BASE/'demo/replay-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='runs'},ensure_ascii=False))
if __name__=='__main__':main()
