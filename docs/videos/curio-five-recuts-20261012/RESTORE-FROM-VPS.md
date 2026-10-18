# Restore the five Curio remasters

The isolated backup was verified on 2026-10-12 at 17:33 UTC at
`/var/backups/curio-video/20261012-five-recuts/curio-five-recuts-20261012`
on the production VPS. The transfer archive SHA-256 matched before extraction;
the remote and local `backup-verify.py` checks each returned **2,697 files and
5,014,559,774 bytes** against the same manifest. Freshly re-run the command
below before a restore or deletion. The backup contains the
five upload packages, source and editorial evidence, cached new narration,
and the batch index. The separate original-video source directories are not
part of this snapshot.

The immutable manifest SHA-256 is
`a71389c4be3bec7c20e3495eb2c8b3750093f568a714bdf217ab9026235565e7`.
The separate local verification receipt is
`<home>/mokaair-work/backup-receipts/curio-five-recuts-20261012-backup-verified.json`.
Verify the VPS copy before downloading:
Replace `<saved-session>` with the PuTTY session configured on your machine.

```powershell
$plink = 'C:/Program Files/PuTTY/plink.exe'
$savedSession = '<saved-session>'
$remote = '/var/backups/curio-video/20261012-five-recuts/curio-five-recuts-20261012'
$manifestSha = 'a71389c4be3bec7c20e3495eb2c8b3750093f568a714bdf217ab9026235565e7'
& $plink -batch -load $savedSession -l root "python3 '$remote/backup-verify.py' '$remote' $manifestSha"
if ($LASTEXITCODE -ne 0) { throw 'VPS backup verification failed' }
```

Restore to a new directory so an existing work folder cannot be overwritten.
The saved PuTTY session supplies the SSH configuration; use its configured
host name for PSCP's remote path:

```powershell
$savedSession = '<saved-session>'
$remote = '/var/backups/curio-video/20261012-five-recuts/curio-five-recuts-20261012'
$manifestSha = 'a71389c4be3bec7c20e3495eb2c8b3750093f568a714bdf217ab9026235565e7'
$hostName = (Get-ItemProperty ("HKCU:/Software/SimonTatham/PuTTY/Sessions/$savedSession")).HostName
$targetParent = Join-Path ([Environment]::GetFolderPath('UserProfile')) 'mokaair-work/curio-restore-staging'
if (Test-Path -LiteralPath $targetParent) { throw 'Choose a fresh restore directory' }
New-Item -ItemType Directory -Path $targetParent | Out-Null
& 'C:/Program Files/PuTTY/pscp.exe' -batch -load $savedSession -l root -sftp -r ("${hostName}:${remote}") $targetParent
if ($LASTEXITCODE -ne 0) { throw 'Restore transfer failed' }
$restored = Join-Path $targetParent 'curio-five-recuts-20261012'
python (Join-Path $restored 'backup-verify.py') $restored $manifestSha
if ($LASTEXITCODE -ne 0) { throw 'Restored file verification failed' }
```

The `upload/` directory under each of `curio-h02`, `curio-u02`, `curio-h03`,
`curio-l08` and `curio-h01` contains the complete MP4, thumbnail, four CC
files, three dub WAV files and localized description/metadata. The backup is
an exact snapshot of the local production batch; later Studio video IDs,
verification receipts and corrected live titles are recorded separately
from this manifest to keep its integrity check repeatable. Publication
remains the owner's decision.

Keep the restored directory immutable when checking the backup. In particular,
`delivery-index.mjs` rewrites two manifest-listed index files and still uses
some absolute evidence paths from the original work location. Do not run it
inside the restored snapshot. If a new delivery-readiness review is needed,
make a separate working copy and reconcile those paths before producing a new
index and receipt.
