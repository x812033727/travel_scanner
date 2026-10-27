from pathlib import Path
import csv, json, sys, hashlib

root = Path(sys.argv[1])
def read(relative):
    with (root / relative).open(newline='') as f:
        return list(csv.DictReader(f))

source = read('demo/input/parcels.csv')
assert len(source) == 1200
def expected(inclusive):
    result = []
    for r in source:
        if r['status'] != 'delivered':
            continue
        actual, promised = int(r['actual_days']), int(r['promised_days'])
        if actual > promised or (inclusive and actual == promised):
            result.append({'parcel_id': r['parcel_id'], 'route': r['route'],
                           'promised_days': str(promised), 'actual_days': str(actual),
                           'days_late': str(actual-promised)})
    return sorted(result, key=lambda r: r['parcel_id'])

strict = read('demo/output/late-followup.csv')
inclusive = read('demo/output/due-or-late.csv')
assert strict == expected(False) and inclusive == expected(True)
assert len(strict) == 480 and len(inclusive) == 720
assert len({r['parcel_id'] for r in strict}) == 480
assert len({r['parcel_id'] for r in inclusive}) == 720
added = [r for r in inclusive if r['parcel_id'] not in {x['parcel_id'] for x in strict}]
assert len(added) == 240 and all(r['days_late'] == '0' for r in added)
left = (root/'demo/output/late-followup.csv').read_bytes()
right = (root/'demo/output/parquet-readback.csv').read_bytes()
assert left == right
print(json.dumps({'input_rows': len(source), 'strict_rows': len(strict),
                  'inclusive_rows': len(inclusive), 'on_time_added': len(added),
                  'all_rows_match': True, 'parquet_roundtrip_equal': True,
                  'strict_first': strict[0], 'strict_last': strict[-1],
                  'strict_csv_sha256': hashlib.sha256(left).hexdigest()}, ensure_ascii=False))
