#!/usr/bin/env python3
"""One Colab account per agent: lease an account from the site, run the CLI in its own home.

Several agents can make videos at the same time, each on a Colab account of its own. The site
holds who uses which account (a lease per account, /api/video/colab-accounts); this script takes
one, fetches its token.json into a home of its own and puts a `colab` shim in front of PATH, so
that two agents on the same machine never read each other's token or Colab session list.

  accounts.py list [--json]                     every account: signed in, compute units, holder
  accounts.py claim --holder NAME [--slot a-e|auto] [--ttl-minutes 240] [--min-balance N] [--no-verify]
                                                lease (auto: the free account with the most units),
                                                fetch the token, write the shim, run `colab usage`
  accounts.py renew --holder NAME --slot S [--ttl-minutes N]
  accounts.py release --holder NAME --slot S    give it back and delete the local token
  accounts.py env --slot S                      print the PATH line that selects the account

After `claim`, run every h3.sh / h3_detached.py / images.py call with
COLAB_ACCOUNT_SLOT=<slot> COLAB_ACCOUNT_HOLDER=<name> in the environment: they put the
account's shim first on PATH (activate()), and h3_detached.py renews the lease while it works.

NAME is the agent's own name (letters, digits and . _ : @ -), the same one it claimed its board
task with. The site is MOKAAIR_SITE (default https://mokaair.com), the token MOKAAIR_VIDEO_TOKEN
or ~/.mokaair/video-tool.json (the video tool token, paired with `login --colab`). Accounts live
under COLAB_ACCOUNTS_ROOT (default ~/.cache/minimax-h3-colab/accounts/<slot>). Exit codes:
0 done, 2 usage, 3 the site refused (taken, not signed in, none free), 4 the account does not
answer `colab usage`, 5 the site cannot be reached. Standard library only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

SLOT_RE = re.compile(r"^[a-e]$")
HOLDER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@-]{0,79}$")
RENEW_EVERY_S = 30 * 60


class SiteError(RuntimeError):
    def __init__(self, status: int, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}" if code else detail)
        self.status, self.code, self.detail = status, code, detail


def say(message: str) -> None:
    print(f"[minimax-h3-colab] {message}", file=sys.stderr, flush=True)


def accounts_root() -> Path:
    configured = os.environ.get("COLAB_ACCOUNTS_ROOT")
    return Path(configured).expanduser() if configured else Path.home() / ".cache" / "minimax-h3-colab" / "accounts"


def account_home(slot: str) -> Path:
    return accounts_root() / slot


def shim_dir(slot: str) -> Path:
    return account_home(slot) / "bin"


def _tool_file() -> Path:
    return Path(os.environ.get("MOKAAIR_VIDEO_TOOL_FILE") or Path.home() / ".mokaair" / "video-tool.json")


def site_token() -> str:
    token = os.environ.get("MOKAAIR_VIDEO_TOKEN", "")
    if token:
        return token
    try:
        data = json.loads(_tool_file().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        data = {}
    token = data.get("token") if isinstance(data, dict) else None
    if isinstance(token, str) and token.startswith("mkv_"):
        return token
    raise SiteError(0, "no_video_tool_token", "no video tool token: pair with `node tools/video/cli.mjs login --colab` "
                    "or set MOKAAIR_VIDEO_TOKEN")


def site_url() -> str:
    configured = os.environ.get("MOKAAIR_SITE", "")
    if configured:
        return configured.rstrip("/")
    try:
        site = json.loads(_tool_file().read_text(encoding="utf-8")).get("site")
    except (OSError, ValueError, AttributeError):
        site = None
    if isinstance(site, str) and site.startswith("https://"):
        return site.rstrip("/")
    return "https://mokaair.com"


def request(method: str, path: str, body: dict[str, Any] | None = None) -> Any:
    """One call to the site's video tool routes; a refusal is a SiteError with its code."""
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        f"{site_url()}/api/video/{path}",
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {site_token()}",
            "Accept": "application/json",
            **({"Content-Type": "application/json"} if data is not None else {}),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            return json.loads(response.read() or b"null")
    except urllib.error.HTTPError as exc:
        try:
            payload = json.loads(exc.read() or b"{}")
        except ValueError:
            payload = {}
        raise SiteError(exc.code, str(payload.get("code") or ""), str(payload.get("detail") or exc.reason)) from None
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise SiteError(0, "site_unreachable", f"cannot reach {site_url()}: {exc}") from None


def real_colab() -> str:
    """The installed CLI, never one of the shims (a shim calling itself would loop)."""
    root = accounts_root().resolve()
    extra = str(Path.home() / ".local" / "bin")
    for entry in [*os.environ.get("PATH", "").split(os.pathsep), extra]:
        if not entry:
            continue
        try:
            if Path(entry).resolve().is_relative_to(root):
                continue
        except OSError:
            continue
        found = shutil.which("colab", path=entry)
        if found:
            return found
    raise SystemExit("[minimax-h3-colab] the colab CLI is not installed; run bootstrap.sh install")


def write_account(slot: str, credentials: dict[str, Any]) -> Path:
    """token.json in the account's own HOME, and a `colab` that runs with that HOME."""
    home = account_home(slot)
    config = home / ".config" / "colab-cli"
    config.mkdir(parents=True, exist_ok=True)
    os.chmod(home, 0o700)
    os.chmod(config, 0o700)
    token_path = config / "token.json"
    temp = config / ".token.tmp"
    fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(credentials, handle)
        handle.write("\n")
    os.replace(temp, token_path)
    bin_dir = shim_dir(slot)
    bin_dir.mkdir(parents=True, exist_ok=True)
    shim = bin_dir / "colab"
    # The CLI reads ~/.config/colab-cli/{token,sessions}.json with no flag to move them, so the
    # account is chosen by HOME. Only this process gets it: the agent's own HOME stays.
    shim.write_text(
        "#!/bin/sh\n"
        f"# Colab account {slot.upper()} (accounts.py claim). The token is in this HOME, not the agent's.\n"
        f"HOME={shlex.quote(str(home))} exec {shlex.quote(real_colab())} \"$@\"\n",
        encoding="utf-8",
    )
    os.chmod(shim, 0o755)
    return token_path


def activate(environ: dict[str, str] | None = None) -> str | None:
    """Put COLAB_ACCOUNT_SLOT's shim first on PATH (in place); the slot, or None for the default.

    Scripts call it before they run `colab`. A slot that was never claimed on this machine is an
    error: falling back to the agent's own token would run on whichever account that is.
    """
    env = os.environ if environ is None else environ
    slot = env.get("COLAB_ACCOUNT_SLOT", "").strip().lower()
    if slot in ("", "default"):
        return None
    if not SLOT_RE.match(slot):
        raise SystemExit("[minimax-h3-colab] COLAB_ACCOUNT_SLOT must be a-e or default")
    shim = shim_dir(slot)
    if not (shim / "colab").is_file():
        raise SystemExit(f"[minimax-h3-colab] account {slot.upper()} is not set up on this machine; "
                         f"run: accounts.py claim --slot {slot} --holder <name>")
    parts = [p for p in env.get("PATH", "").split(os.pathsep) if p and p != str(shim)]
    env["PATH"] = os.pathsep.join([str(shim), *parts])
    return slot


_last_renewal: dict[str, float] = {}


def renew_if_due(*, every_s: float = RENEW_EVERY_S, log=say) -> None:
    """Keep this agent's lease alive during a long run; never stops the run if the site is down."""
    slot = os.environ.get("COLAB_ACCOUNT_SLOT", "").strip().lower()
    holder = os.environ.get("COLAB_ACCOUNT_HOLDER", "").strip()
    if not SLOT_RE.match(slot) or not HOLDER_RE.match(holder):
        return
    now = time.monotonic()
    if now - _last_renewal.get(slot, -every_s) < every_s:
        return
    _last_renewal[slot] = now
    ttl = int(os.environ.get("COLAB_ACCOUNT_TTL_MINUTES", "240"))
    try:
        lease = request("POST", f"colab-accounts/{slot}/lease", {"holder": holder, "ttl_minutes": ttl})
        log(f"lease on account {slot.upper()} renewed until {time.strftime('%H:%M', time.localtime(lease['expires_at']))}")
    except SiteError as exc:
        log(f"could not renew the lease on account {slot.upper()}: {exc}")


def verify(slot: str) -> str:
    try:
        result = subprocess.run([str(shim_dir(slot) / "colab"), "--auth=oauth2", "usage"], capture_output=True,
                                text=True, timeout=90, stdin=subprocess.DEVNULL)
        output = (result.stdout or "") + (result.stderr or "")
    except subprocess.TimeoutExpired:
        output = ""
    lines = [line for line in output.splitlines() if re.search(r"Current balance|Usage rate|Active assignments", line)]
    if not any("Current balance" in line for line in lines):
        raise SystemExit(4)
    return "\n".join(lines)


def _holder(value: str | None) -> str:
    holder = (value or os.environ.get("COLAB_ACCOUNT_HOLDER", "")).strip()
    if not HOLDER_RE.match(holder):
        raise SystemExit("[minimax-h3-colab] --holder (or COLAB_ACCOUNT_HOLDER) is required: letters, digits and . _ : @ -")
    return holder


def _slot(value: str | None, *, allow_auto: bool = False) -> str:
    slot = (value or os.environ.get("COLAB_ACCOUNT_SLOT", "")).strip().lower()
    if SLOT_RE.match(slot) or (allow_auto and slot == "auto"):
        return slot
    raise SystemExit("[minimax-h3-colab] --slot must be a-e" + (" or auto" if allow_auto else ""))


def _when(epoch: int) -> str:
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(epoch))


def cmd_list(args: argparse.Namespace) -> int:
    data = request("GET", "colab-accounts")
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0
    print("slot  signed-in  balance  rate/h  holder (until)")
    for item in data["accounts"]:
        units = item.get("compute_units") or {}
        balance = units.get("balance")
        rate = units.get("rate_per_hour")
        lease = item.get("lease")
        holder = f"{lease['holder']} ({_when(lease['expires_at'])})" if lease else "-"
        mark = "*" if item.get("is_default") else " "
        print(f"{item['slot'].upper()}{mark}    {'yes' if item['signed_in'] else 'no ':<9}  "
              f"{'' if balance is None else f'{balance:.1f}':>7}  {'' if rate is None else f'{rate:.2f}':>6}  {holder}")
    return 0


def cmd_claim(args: argparse.Namespace) -> int:
    holder = _holder(args.holder)
    wanted = _slot(args.slot or "auto", allow_auto=True)
    body: dict[str, Any] = {"holder": holder, "ttl_minutes": args.ttl_minutes}
    if args.min_balance is not None:
        body["min_balance"] = args.min_balance
    lease = request("POST", f"colab-accounts/{wanted}/lease", body)
    slot = lease["slot"]
    query = urllib.parse.urlencode({"slot": slot, "holder": holder})
    try:
        credentials = request("GET", f"colab-credentials?{query}")
        token = credentials.get("credentials") if isinstance(credentials, dict) else None
        if not isinstance(token, dict) or not token.get("refresh_token"):
            raise SiteError(0, "colab_credentials_unusable", "the site answered without a usable token")
    except SiteError:
        # A lease without a token on this machine would only keep the account from the others.
        try:
            request("POST", f"colab-accounts/{slot}/lease/release", {"holder": holder})
        except SiteError:
            pass
        raise
    path = write_account(slot, token)
    say(f"account {slot.upper()} leased to {holder} until {_when(lease['expires_at'])}; token at {path}")
    if not args.no_verify:
        try:
            print(verify(slot), file=sys.stderr)
        except SystemExit:
            say(f"account {slot.upper()} does not answer `colab usage` (signed out on the admin page, or no network); "
                f"releasing it")
            request("POST", f"colab-accounts/{slot}/lease/release", {"holder": holder})
            return 4
    # The one line on stdout: what the agent puts in front of every later call.
    print(f"export COLAB_ACCOUNT_SLOT={slot} COLAB_ACCOUNT_HOLDER={holder}")
    return 0


def cmd_renew(args: argparse.Namespace) -> int:
    holder, slot = _holder(args.holder), _slot(args.slot)
    lease = request("POST", f"colab-accounts/{slot}/lease", {"holder": holder, "ttl_minutes": args.ttl_minutes})
    say(f"account {slot.upper()} leased to {holder} until {_when(lease['expires_at'])}")
    return 0


def cmd_release(args: argparse.Namespace) -> int:
    holder, slot = _holder(args.holder), _slot(args.slot)
    result = request("POST", f"colab-accounts/{slot}/lease/release", {"holder": holder})
    token = account_home(slot) / ".config" / "colab-cli" / "token.json"
    if token.exists():
        token.unlink()
    say(f"account {slot.upper()} {'released' if result.get('released') else 'had no lease left'}; local token removed")
    return 0


def cmd_env(args: argparse.Namespace) -> int:
    slot = _slot(args.slot)
    print(f"export PATH={shlex.quote(str(shim_dir(slot)))}:\"$PATH\"")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="accounts.py", description=__doc__.split("\n\n", 1)[0])
    sub = parser.add_subparsers(dest="command", required=True)
    listing = sub.add_parser("list")
    listing.add_argument("--json", action="store_true")
    claim = sub.add_parser("claim")
    claim.add_argument("--holder")
    claim.add_argument("--slot")
    claim.add_argument("--ttl-minutes", type=int, default=240)
    claim.add_argument("--min-balance", type=float)
    claim.add_argument("--no-verify", action="store_true")
    renew = sub.add_parser("renew")
    renew.add_argument("--holder")
    renew.add_argument("--slot")
    renew.add_argument("--ttl-minutes", type=int, default=240)
    release = sub.add_parser("release")
    release.add_argument("--holder")
    release.add_argument("--slot")
    env = sub.add_parser("env")
    env.add_argument("--slot")
    args = parser.parse_args(argv)
    handlers = {"list": cmd_list, "claim": cmd_claim, "renew": cmd_renew, "release": cmd_release, "env": cmd_env}
    try:
        return handlers[args.command](args)
    except SiteError as exc:
        say(f"the site refused ({exc.status or 'no answer'}): {exc}")
        return 5 if exc.code in ("site_unreachable", "no_video_tool_token") else 3


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
