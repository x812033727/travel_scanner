"""Freeze the editor's completed review of normal public browser captures."""
import datetime
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
reviewed = json.loads((HERE / 'renders/public-reviewed-sheets.json').read_text(encoding='utf-8-sig'))
expected = sorted(
    f'public-{mode}-{locale}-{group}.jpg'
    for locale in ['zh-TW', 'en', 'ja', 'ko', 'zh-CN']
    for mode in ['desktop', 'mobile', 'table']
    for group in range(1, 6)
)
assert sorted(reviewed) == expected and len(set(reviewed)) == 75
pages = json.loads((HERE / 'public-verification.json').read_text(encoding='utf8'))
crops = json.loads((HERE / 'table-crop-verification.json').read_text(encoding='utf8'))
assert len(pages['pages']) == 220
assert all(p['status'] == 200 and p['full_text'] and p['metadata'] for p in pages['pages'])
listing_sheets = json.loads((HERE / 'renders/listing-reviewed-sheets.json').read_text(encoding='utf8'))
assert sorted(listing_sheets) == ['listing-desktop-review.jpg', 'listing-mobile-review.jpg']
assert len(pages['listings']) == 10 and all(p['status'] == 200 for p in pages['listings'])
assert len(crops) == 110 and all(
    c.get('matching_text_scanlines', 0) >= .65
    or (c.get('exact_matching_text_rows', 0) >= 6 and c.get('matching_text_span_pixels', 0) >= 300)
    or c.get('native_horizontal_scroll_verified') is True
    for c in crops
)
receipt = {
    'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'authenticated': False,
    'desktop_mobile_pages': 220,
    'mobile_table_crops': 110,
    'reviewed_contact_sheets': [
        {'path': name, 'sha256': hashlib.sha256((HERE / name).read_bytes()).hexdigest()}
        for name in expected
    ],
    'reviewed_listing_sheets': [
        {'path': name, 'sha256': hashlib.sha256((HERE / name).read_bytes()).hexdigest()}
        for name in listing_sheets
    ],
    'all_passed': True,
    'method': 'Editor inspected all 75 sheets of desktop and mobile viewport captures and mobile tables. Full article text, links, images and metadata were checked against every published locale document by the signed-out browser verifier. Table crops come from normal full-page screenshots. Wide tables are captured at their native left and right scrollbar positions and stitched at the measured offset. No page content or style was changed for visual proof.',
    'mobile_device': 'Chromium iPhone 13 emulation, not a physical phone.',
}
(HERE / 'public-visual-verification.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf8')
print('Recorded all 75 inspected public layout sheets and 110 normal-page table crops')
