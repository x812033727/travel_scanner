---
id: 2026-10-15-investigate-production-ssh-stop-and-boot
title: 查明正式主機 SSH 停止原因與開機啟動設定
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-10-15T14:33:55Z
completed_at:
branch: codex/a01-pilot-deploy-evidence-20261015
depends_on: []
scope:
  - docs/runbooks/ssh-access.md
  - tasks/open/2026-10-15-investigate-production-ssh-stop-and-boot.md
---

# 查明正式主機 SSH 停止原因與開機啟動設定

## Why

Production management access through the saved PuTTY `hostinger2` session timed out while HTTPS remained available. After the owner restored access, journal readback showed `ssh.service` stopped cleanly on 2026-10-15 at 06:29:50 UTC (14:29:50 Taiwan), then started after a new boot at 14:08:15 UTC. The initiating actor is unknown. At that readback the service was active/running but its unit was disabled; `ssh.socket` was inactive/disabled. A future restart could leave management access dependent on an unidentified startup path.

## Definition of done

- [ ] Identify the stop/start initiator from retained service, audit or provider activity evidence, or document that retention cannot establish it.
- [ ] Explain the effective boot-start path and confirm whether the disabled unit is intentional.
- [ ] If a configuration change is needed, prepare a concrete change and rollback plan for owner approval, apply only within that approval and verify service/listener access without an unnecessary reboot.
- [ ] Record the supported recovery procedure in `docs/runbooks/ssh-access.md`, excluding credentials and private host addresses.

## Steps

- [x] Confirm current management connection, SSH service state and listening port after owner restoration.
- [ ] Correlate the 06:29:50 UTC stop with existing retained audit/provider events and unit dependencies.
- [ ] Review boot-start configuration and prepare any required narrow remediation.

## How to verify

Use the authorized `hostinger2` PuTTY session with explicit root login and one batched read-only script. Read `systemctl show ssh.service` and `ssh.socket`, `ss -ltnp` for port 7788, the exact journal interval and dependency/startup configuration. Compare before/after state if an owner-approved change is made. A public HTTP 200 does not prove SSH access. Do not print environment files, private keys, passwords or authentication contents.

## Notes

The Hostinger cloud firewall already allowed TCP 7788, 80 and 443. Windows used the Wi-Fi route; no Tailscale exit route was active. Previous-boot journal showed `Stopping ssh.service`, SIGTERM, then `Deactivated successfully` and `Stopped`; this establishes a clean service stop but not who requested it. The current boot began at 14:08:07 UTC; SSH listened on IPv4 and IPv6 at 14:08:15 UTC. The agent did not change a password, firewall, service, boot setting or reboot the host. A01 deployment subsequently succeeded with the restored connection. This follow-up is not authorization to enable services or restart the host. See the latest recovery evidence in `tasks/open/2026-09-28-video-story-pilot.md`.
