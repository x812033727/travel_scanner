#!/usr/bin/env python3
"""Same fictional fixture, an explicitly changed >= requirement, local output only."""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,csv,hashlib
BASE=Path(__file__).resolve().parent
SQL=""".read demo/setup.sql
COPY (
 SELECT parcel_id,route,promised_days,actual_days,
        actual_days-promised_days AS days_late
 FROM parcels
 WHERE status='delivered' AND actual_days>=promised_days
 ORDER BY parcel_id
) TO 'demo/output/due-or-late.csv' (HEADER,DELIMITER ',');
SELECT count(*) AS due_or_late_rows
FROM read_csv('demo/output/due-or-late.csv');
"""
def main():
 (BASE/'demo/variant.sql').write_text(SQL)
 cmd=['../fifth-demo/bin/duckdb','-no-init','-agent',':memory:','-f','demo/variant.sql']
 r=subprocess.run(cmd,cwd=BASE,text=True,capture_output=True,timeout=15)
 (BASE/'runlogs/variant.stdout.txt').write_text(r.stdout);(BASE/'runlogs/variant.stderr.txt').write_text(r.stderr)
 (BASE/'runlogs/variant.command.json').write_text(json.dumps({'argv':cmd,'cwd':str(BASE),'observed_at_utc':datetime.now(timezone.utc).isoformat(),'exit_code':r.returncode},ensure_ascii=False,indent=2)+'\n');assert r.returncode==0,r.stderr
 with (BASE/'demo/output/due-or-late.csv').open() as f:rows=list(csv.DictReader(f))
 with (BASE/'demo/input/parcels.csv').open() as f:source=list(csv.DictReader(f))
 expected=[x['parcel_id'] for x in source if x['status']=='delivered' and int(x['actual_days'])>=int(x['promised_days'])]
 assert len(rows)==720 and [x['parcel_id'] for x in rows]==expected
 result={'status':'PASS','changed_requirement':'Delivered and actual_days>=promised_days; due-or-late, not the original strictly-late list.','rows':len(rows),'zero_days_late_rows':sum(x['days_late']=='0' for x in rows),'independent_source_predicate_matches':True,'sha256':hashlib.sha256((BASE/'demo/output/due-or-late.csv').read_bytes()).hexdigest()}
 (BASE/'demo/variant-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
