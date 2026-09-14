"""One reviewed taxonomy correction before the first successful batch dry-run.

Runs on the release host under the existing deployment locks. Keeps the original
failed preflight journal, records intent before the existing admin-service commit,
and advances its expected snapshot only after proving no content changed.
"""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
from datetime import datetime, timezone

TARGET = "3b8df68c693eb81ccde7793a2f89d71999dbb2c2"
MANIFEST = "96ad2cb050c0b31a678e446c08e428746d1e3e873343a9a72ae0353f48ca7d59"
BASE = Path("/root/mokaair-ai-terms-" + TARGET[:12])
os.umask(0o077)
env = {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "HOME": "/root"}
locks = []
for name in ["/var/lock/travel-scanner-deploy.lock", "/root/mokaair-deploy.lock", "/run/mokaair-manual-deploy.lock", "/run/travel-scanner-deployer/deploy.lock"]:
    handle = open(name, "r+")
    fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    locks.append(handle)

def require(ok, reason):
    if not ok:
        raise RuntimeError(reason)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def persist(path, value):
    temp = path.with_suffix(".json.next")
    with temp.open("w") as file:
        json.dump(value, file, indent=2)
        file.flush()
        os.fsync(file.fileno())
    temp.replace(path)
    fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)

release = json.loads((BASE / "state.json").read_text())
require(release.get("activated_at") and not release.get("failed_at") and release["target"] == TARGET, "Release not active")
require(digest(BASE / "predeploy.dump") == release["backup"]["sha256"], "Pre-change backup differs")
require(digest(BASE / "runtime.env") == digest(Path("/root/travel_scanner/.env")) == release["env_hash"], "Runtime differs")
for service, expected in release["after"].items():
    row = json.loads(subprocess.check_output(["docker", "inspect", "travel_scanner-" + service + "-1"], env=env))[0]
    require(row["Id"] == expected["id"] and row["Image"] == expected["image"] and row["State"]["Running"], "Release container changed")
    require(hashlib.sha256(json.dumps(sorted(row["Config"]["Env"])).encode()).hexdigest() == expected["env_hash"], "Container environment changed")
path = BASE / "publication-state/journal.json"
raw = path.read_bytes()
journal = json.loads(raw)
require(journal["manifest_sha256"] == MANIFEST and not journal["dry_run"] and journal["pending"] is None and all(not values for values in journal["done"].values()), "Correction only allowed before any article write")
require(journal["expected"]["ai-glossary-50-terms"]["topics"] == ["ai", "misc"], "Unexpected glossary topics")
archive = BASE / "journal-before-taxonomy.json"
require(not archive.exists() and not (BASE / "taxonomy-intent.json").exists(), "Existing correction requires inspection")
with archive.open("xb") as file:
    file.write(raw)
    file.flush()
    os.fsync(file.fileno())
started = datetime.now(timezone.utc).isoformat()
persist(BASE / "taxonomy-intent.json", {"started_at": started, "slug": "ai-glossary-50-terms", "from": ["ai", "misc"], "to": ["ai", "tutorial"], "journal_sha256": hashlib.sha256(raw).hexdigest(), "status": "pending"})
driver = (BASE / "source/docs/ai-terms-series/publish_batch.py").read_text()
prefix = "ns={'__name__':'reviewed_taxonomy_driver'}\nexec(compile(" + repr(driver) + ", 'reviewed_publish_batch', 'exec'), ns)\nexpected=" + repr(journal["expected"]) + "\n"
script = r'''
import asyncio,json,copy
from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.guides.schemas import ArticleUpdate
from app.guides import admin_service
async def main():
 engine=ns['engine']
 async with engine.connect() as connection:
  await connection.execution_options(isolation_level='SERIALIZABLE')
  locked=await connection.scalar(text('SELECT pg_try_advisory_lock(:key)'),{'key':ns['LOCK_KEY']})
  await connection.commit()
  ns['require'](bool(locked),'Publisher active')
  try:
   async with AsyncSession(bind=connection,expire_on_commit=False) as session:
    before=await ns['snapshot'](session,lock=True)
    ns['same_state'](before,expected)
    slug='ai-glossary-50-terms';old=before[slug]
    ns['require'](old['topics']==['ai','misc'],'Unexpected taxonomy')
    actor=await ns['active_actor'](session)
    payload=ArticleUpdate(expected_version=old['version'],kind='life',destination_id=None,topics=['ai','tutorial'],valid_until=None,featured=False,display_order=100)
    await admin_service.update_article(session,actor,UUID(old['id']),payload,'zh-TW')
    await session.rollback()
    after=await ns['snapshot'](session)
    allowed=copy.deepcopy(before)
    allowed[slug]['topics']=['ai','tutorial']
    allowed[slug]['version']+=1
    allowed[slug]['updated_at']=after[slug]['updated_at']
    ns['same_state'](after,allowed)
    print(json.dumps({'expected':after,'version_before':old['version'],'version_after':after[slug]['version']}))
  finally:
   await connection.rollback()
   await connection.execute(text('SELECT pg_advisory_unlock(:key)'),{'key':ns['LOCK_KEY']})
   await connection.commit()
 await engine.dispose()
asyncio.run(main())
'''
with (BASE / "taxonomy-private.log").open("a") as log:
    result = subprocess.run(["docker", "exec", "-i", "travel_scanner-api-1", "python", "-"], input=prefix+script, text=True, stdout=subprocess.PIPE, stderr=log, env=env, timeout=90)
require(result.returncode == 0, "Correction stopped; inspect intent and current state before retrying")
after = json.loads(result.stdout)
require(path.read_bytes() == raw, "Journal changed during correction")
journal["expected"] = after["expected"]
journal["history"].append({"phase": "taxonomy-correction", "status": "taxonomy_corrected", "slug": "ai-glossary-50-terms", "at": datetime.now(timezone.utc).isoformat(), "from": ["ai", "misc"], "to": ["ai", "tutorial"], "public_documents_unchanged": True})
persist(path, journal)
os.chown(path, 10001, 10001)
receipt = {"status": "complete", "slug": "ai-glossary-50-terms", "from": ["ai", "misc"], "to": ["ai", "tutorial"], "public_documents_unchanged": True, "version_before": after["version_before"], "version_after": after["version_after"], "started_at": started, "completed_at": datetime.now(timezone.utc).isoformat()}
persist(BASE / "taxonomy-correction.json", receipt)
print(json.dumps(receipt))
