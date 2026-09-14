"""Create the fixed batch's scoped release tools; no host action."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent;OLD=HERE.parent/'ai-news-2026-09'
slugs=json.loads((HERE/'slugs.json').read_text(encoding='utf8'))
assert len(slugs)==22
s=(OLD/'publish_batch.py').read_text(encoding='utf8')
start=s.index('SLUGS = ');end=s.index('\nLOCALES =',start)
s=s[:start]+'SLUGS = '+repr(slugs)+'\nassert len(SLUGS)==len(set(SLUGS))==22'+s[end:]
s=s.replace('len(packs)==10','len(packs)==22').replace("len(plan['articles'])==10","len(plan['articles'])==22").replace('/tmp/mokaair-ai-news-20260914','/tmp/mokaair-ai-news-ytd-publication')
(HERE/'publish_batch.py').write_text(s,encoding='utf8')
s=(OLD/'deploy_release.py').read_text(encoding='utf8')
start=s.index('# Reviewed integrations:');end=s.index("ROOT = Path('/root/travel_scanner')",start)
s=s[:start]+'''# The initial reviewed baseline is the current production commit. If main advances,
# record and inspect the exact intervening integrations before adding their pair here.
if CONTENT_BASE != PREVIOUS:
    reviewed_pairs = {
        ('46298e2863e9c2c4d6776e9d58a821be683a4b32', 'fc0c6763875ed7693ef2a94974a06338b6001968'),
        # PR #476: web minor/patch dependency updates; all 14 PR checks passed.
        ('a9d5b40e7067b321ee886a817b1712aec44afc1b', '673a64b67bc525686dd9959e9b521a0c7662137e'),
        # PR #478: backend lockfile updates; all 14 PR checks passed.
        ('a9d5b40e7067b321ee886a817b1712aec44afc1b', '5a00f72e7aae229de0f77a51c4d9afdcb967b0cf'),
        ('673a64b67bc525686dd9959e9b521a0c7662137e', '5a00f72e7aae229de0f77a51c4d9afdcb967b0cf'),
        # PR #480: pytest-cov development dependency only; all 14 PR checks passed.
        ('a9d5b40e7067b321ee886a817b1712aec44afc1b', '05d0b671efddedb75da1c20093cce42f8b2f09ca'),
    }
    assert (PREVIOUS, CONTENT_BASE) in reviewed_pairs, 'unreviewed integration baseline'
'''+s[end:]
s=s.replace("'/root/mokaair-release-ai-news-'","'/root/mokaair-release-ai-news-ytd-'")
s=s.replace("phase = sys.argv[1]","from release_hold import acquire, verify\nphase = sys.argv[1]\nif phase == 'prepare':\n    acquire(BASE, TARGET)\nelse:\n    verify(BASE, TARGET)")
a="allowed = ('apps/api/app/guides/content/ai-news-', 'apps/web/public/guides/ai-news-', 'docs/ai-news-2026-09/', 'tasks/')"
b="allowed = ('docs/ai-news-2026-ytd/', 'tasks/open/2026-09-14-ai-news-2026-year-to-date.md', 'tasks/done/2026-09-14-ai-news-2026-year-to-date.md', *[f'apps/api/app/guides/content/{slug}.json' for slug in SLUGS], *[f'apps/web/public/guides/{slug}/' for slug in SLUGS])"
assert a in s;s=s.replace(a,b)
s=s.replace("TARGET = os.environ['NEWS_RELEASE_SHA']","SLUGS = "+repr(slugs)+"\nTARGET = os.environ['NEWS_RELEASE_SHA']")
a="assert len(list(Path('/app/app/guides/content').glob('ai-news-*.json'))) == 10"
b="assert all(Path('/app/app/guides/content', slug+'.json').is_file() for slug in "+repr(slugs)+")"
assert a in s;s=s.replace(a,b)
# SLUGS repr uses single quotes inside a double-quoted Python source string.
(HERE/'deploy_release.py').write_text(s,encoding='utf8')
print('Prepared exact-slug publisher and guarded release tools')
