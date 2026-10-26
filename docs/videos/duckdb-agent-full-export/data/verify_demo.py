#!/usr/bin/env python3
"""Verify this small artifact set and its explicit output contract."""
from pathlib import Path
from datetime import datetime,timezone
import csv,hashlib,json,re
BASE=Path(__file__).resolve().parent
def main():
 with (BASE/'input/parcels.csv').open() as f:source=list(csv.DictReader(f))
 with (BASE/'output/late-followup.csv').open() as f:out=list(csv.DictReader(f))
 with (BASE/'output/parquet-readback.csv').open() as f:back=list(csv.DictReader(f))
 expected=[]
 for row in source:
  if row['status']=='delivered' and int(row['actual_days'])>int(row['promised_days']):
   expected.append({'parcel_id':row['parcel_id'],'route':row['route'],'promised_days':row['promised_days'],'actual_days':row['actual_days'],'days_late':str(int(row['actual_days'])-int(row['promised_days']))})
 assert len(source)==1200 and len(out)==480 and out==expected==back
 text=(BASE/'runlogs/typo-agent.stderr.txt').read_text()
 json_lines=[json.loads(line) for line in text.splitlines() if line.startswith('{')]
 assert len(json_lines)==1 and json_lines[0]['error_subtype']=='COLUMN_NOT_FOUND'
 whole_stream_is_json=True
 try:json.loads(text)
 except json.JSONDecodeError:whole_stream_is_json=False
 assert not whole_stream_is_json  # startup text + a valid JSON error, not bad error JSON
 a=(BASE/'runlogs/preview-agent.stdout.txt').read_text();b=(BASE/'runlogs/preview-agent-reversed.stdout.txt').read_text()
 assert '1160 rows omitted' in a and 'of 1200 rows' in a
 ha=re.search(r'hash ([a-f0-9]+)',a).group(1);hb=re.search(r'hash ([a-f0-9]+)',b).group(1);assert ha==hb
 r={'verified_at_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','source_rows':1200,'full_followup_rows':480,'independent_csv_predicate_matches_every_row':True,'parquet_roundtrip_matches_every_row':True,'json_error_line_valid':True,'whole_stderr_is_one_json_document':False,'stderr_contract':'One startup text line plus one valid JSON error object; consumer must parse the JSON line, not treat the whole mixed stream as one object. No vendor bug or real third-party consumer failure claimed.','preview_omitted_rows':1160,'preview_displayed_rows':40,'display_truncation_is_data_loss':False,'order_independent_result_hash_observed':ha,'result_hash_is_file_sha256':False,'comparison':'Same2.0 binary, agent versus no-agent; not a previous-version performance benchmark.'}
 (BASE/'artifact-verification.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(r,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
