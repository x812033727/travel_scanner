"""The Colab CLI accounts of the AI accounts agent: sign-in over pipes, the balance as the
status, the email from the token or Google, and the credential handoff for a paired session.

The fake CLI below behaves like google-colab-cli 0.7.5 as far as the agent reads it: without
a token it prints the sign-in URL and waits for a code on stdin; with one it prints the
compute-unit lines; with a token marked revoked it asks to sign in again and gives up at the
closed stdin with exit 0, which is what the real CLI does.
"""

import json
import sys
import textwrap
from pathlib import Path
from typing import Any
from uuid import uuid4

import pytest

from ai_accounts_agent.colab import (
    ACCOUNT_NAME,
    ColabAccounts,
    fetch_email,
    parse_usage,
    token_path,
)
from ai_accounts_agent.config import AgentConfig
from ai_accounts_agent.server import AgentApplication
from ai_accounts_agent.sessions import FAILED, SUCCEEDED
from tests.test_ai_accounts_agent import KEY, make_config, signed, slot_of, wait_until

posix_only = pytest.mark.skipif(sys.platform == "win32", reason="needs POSIX process groups")

FAKE_COLAB = textwrap.dedent(
    """
    import json, os, sys
    home = os.environ["HOME"]
    token_dir = os.path.join(home, ".config", "colab-cli")
    token = os.path.join(token_dir, "token.json")
    if "usage" not in sys.argv or "--auth=oauth2" not in sys.argv:
        sys.stderr.write("fake colab: unexpected " + " ".join(sys.argv[1:]) + "\\n")
        sys.exit(2)

    def balance(rate):
        print("Current balance: 187.5 compute units")
        print("Usage rate: " + rate + " / hr")
        print("Active assignments: 1")

    def ask():
        sys.stderr.write("\\nTo authorize colab-cli, visit this URL in any browser:\\n\\n"
                         "  https://accounts.google.com/o/oauth2/auth?client_id=x&state=secret"
                         "&redirect_uri=https%3A%2F%2Fsdk.cloud.google.com%2F"
                         "applicationdefaultauthcode.html\\n\\n"
                         "After approving, Google will display an authorization code.\\n")
        sys.stderr.flush()
        sys.stdout.write("Enter the authorization code: ")
        sys.stdout.flush()
        line = sys.stdin.readline()
        if not line:
            print("[colab] Warning: failed to fetch compute-unit info: EOF when reading a line")
            sys.exit(0)
        return line.strip()

    if os.path.exists(token):
        saved = json.load(open(token))
        if saved.get("refresh_token") != "revoked":
            balance("4.82")
            sys.exit(0)
        ask()
        sys.stderr.write("Error: invalid_grant: Token has been expired or revoked.\\n")
        sys.exit(1)
    code = ask()
    if code.startswith("4/good"):
        control = os.path.join(home, "fake-login-email")
        email = open(control).read().strip() if os.path.exists(control) else "owner@x.test"
        named = os.path.join(home, "fake-login-unnamed")
        os.makedirs(token_dir, exist_ok=True)
        json.dump({"token": "ya29.access", "refresh_token": "1//refresh", "client_id": "c",
                   "client_secret": "s", "scopes": ["openid"],
                   "account": "" if os.path.exists(named) else email}, open(token, "w"))
        balance("0")
        sys.exit(0)
    sys.stderr.write("Error: invalid_grant: Bad Request for owner@x.test\\n")
    sys.exit(1)
    """
)


def colab_config(tmp_path: Path, **overrides: Any) -> AgentConfig:
    fake = tmp_path / "fake_colab.py"
    fake.write_text(FAKE_COLAB, encoding="utf-8")
    return make_config(tmp_path, colab_command=(sys.executable, str(fake)), **overrides)


def finished(application: AgentApplication, login_id: str, state: str) -> bool:
    return bool(signed(application, "GET", f"/v1/logins/{login_id}")[1]["status"] == state)


def test_usage_lines_are_parsed_and_anything_else_is_not() -> None:
    usage = parse_usage(
        "Current balance: 1,187.5 compute units\nUsage rate: 4.82 / hr\nActive assignments: 2\n"
    )
    assert usage == {"balance": 1187.5, "rate_per_hour": 4.82, "active_assignments": 2}
    assert parse_usage("Current balance: 10 compute units") == {
        "balance": 10.0,
        "rate_per_hour": None,
        "active_assignments": None,
    }
    assert parse_usage("Warning: EOF when reading a line") is None


def test_fetch_email_reads_userinfo_and_gives_up_quietly() -> None:
    class Response:
        def __init__(self, payload: bytes) -> None:
            self.payload = payload

        def read(self) -> bytes:
            return self.payload

        def __enter__(self) -> "Response":
            return self

        def __exit__(self, *_: object) -> None:
            return None

    seen: list[Any] = []

    def opener(request: Any, timeout: float) -> Response:
        seen.append((request.full_url, request.get_header("Authorization"), timeout))
        return Response(b'{"sub": "1", "email": "owner@x.test", "email_verified": true}')

    assert fetch_email("ya29.access", opener=opener) == "owner@x.test"
    assert seen == [("https://www.googleapis.com/oauth2/v3/userinfo", "Bearer ya29.access", 10.0)]

    def broken(request: Any, timeout: float) -> Response:
        raise OSError("no network")

    assert fetch_email("ya29.access", opener=broken) is None
    assert fetch_email("ya29.access", opener=lambda *_, **__: Response(b"not json")) is None


@posix_only
def test_colab_login_signs_in_reads_the_balance_and_hands_out_credentials(
    tmp_path: Path,
) -> None:
    config = colab_config(tmp_path)
    application = AgentApplication(config)
    overview = signed(application, "GET", "/v1/accounts")[1]
    assert len(overview["slots"]) == 20
    assert overview["defaults"]["colab"] == "a"
    assert slot_of(overview, "colab", "b")["logged_in"] is False
    assert signed(application, "GET", "/v1/accounts/colab/b/credentials")[0] == 404

    status, login = signed(application, "POST", "/v1/accounts/colab/b/login")
    assert status == 201
    assert login["kind"] == "paste_code" and login["user_code"] is None
    assert login["url"].startswith("https://accounts.google.com/o/oauth2/auth?client_id=x")
    # The same login is handed back to a second click.
    assert signed(application, "POST", "/v1/accounts/colab/b/login")[1]["id"] == login["id"]
    rejected = signed(application, "POST", f"/v1/logins/{login['id']}/code", {"code": "a b"})
    assert (rejected[0], rejected[1]["code"]) == (422, "login_code_rejected")
    accepted = signed(
        application, "POST", f"/v1/logins/{login['id']}/code", {"code": "4/good-code_x"}
    )
    assert accepted[0] == 202
    wait_until(lambda: finished(application, login["id"], SUCCEEDED))

    colab_b = slot_of(signed(application, "GET", "/v1/accounts")[1], "colab", "b")
    assert colab_b["logged_in"] is True
    assert colab_b["auth_method"] == "google"
    assert colab_b["email"] == "owner@x.test"
    assert colab_b["plan"] is None
    assert colab_b["usage"] == {
        "source": "live",
        "windows": [],
        "compute_units": {"balance": 187.5, "rate_per_hour": 4.82, "active_assignments": 1},
    }
    # The email came from the token file's own account field and was remembered beside it.
    assert json.loads((config.slot_path("colab", "b") / ACCOUNT_NAME).read_text())["email"] == (
        "owner@x.test"
    )

    status, payload = signed(application, "GET", "/v1/accounts/colab/b/credentials")
    assert status == 200
    assert payload["slot"] == "b"
    assert payload["credentials"]["refresh_token"] == "1//refresh"
    # `default` resolves to the default slot, which is still A and empty.
    missing = signed(application, "GET", "/v1/accounts/colab/default/credentials")
    assert (missing[0], missing[1]["code"]) == (404, "colab_not_signed_in")
    signed(application, "PUT", "/v1/defaults/colab", {"slot": "b"})
    assert signed(application, "GET", "/v1/accounts/colab/default/credentials")[1]["slot"] == "b"
    # Only Colab hands its login out.
    assert signed(application, "GET", "/v1/accounts/claude/a/credentials")[0] == 404

    assert signed(application, "POST", "/v1/accounts/colab/b/logout")[0] == 200
    assert not token_path(config.slot_path("colab", "b")).exists()
    assert not (config.slot_path("colab", "b") / ACCOUNT_NAME).exists()
    after = slot_of(signed(application, "GET", "/v1/accounts")[1], "colab", "b")
    assert after["logged_in"] is False


@posix_only
def test_a_rejected_code_fails_without_the_code_and_puts_the_old_login_back(
    tmp_path: Path,
) -> None:
    config = colab_config(tmp_path)
    application = AgentApplication(config)
    first = signed(application, "POST", "/v1/accounts/colab/a/login")[1]
    signed(application, "POST", f"/v1/logins/{first['id']}/code", {"code": "4/good-first"})
    wait_until(lambda: finished(application, first["id"], SUCCEEDED))
    home = config.slot_path("colab", "a")
    saved = token_path(home).read_text(encoding="utf-8")

    # Signing in again moves the working token aside so the CLI prints a URL.
    again = signed(application, "POST", "/v1/accounts/colab/a/login")[1]
    assert again["id"] != first["id"] and again["url"]
    assert not token_path(home).exists()
    signed(application, "POST", f"/v1/logins/{again['id']}/code", {"code": "4/bad-code"})
    wait_until(lambda: finished(application, again["id"], FAILED))
    view = signed(application, "GET", f"/v1/logins/{again['id']}")[1]
    assert "invalid_grant" in view["error"]
    assert "4/bad-code" not in view["error"]
    assert "owner@x.test" not in view["error"]  # Emails are masked in what the page sees.
    assert token_path(home).read_text(encoding="utf-8") == saved
    restored = slot_of(signed(application, "GET", "/v1/accounts")[1], "colab", "a")
    assert restored["logged_in"] is True


@posix_only
def test_a_cancelled_login_puts_the_old_login_back_too(tmp_path: Path) -> None:
    config = colab_config(tmp_path)
    application = AgentApplication(config)
    first = signed(application, "POST", "/v1/accounts/colab/a/login")[1]
    signed(application, "POST", f"/v1/logins/{first['id']}/code", {"code": "4/good-first"})
    wait_until(lambda: finished(application, first["id"], SUCCEEDED))
    again = signed(application, "POST", "/v1/accounts/colab/a/login")[1]
    # A credential handoff waits while a sign-in holds the account.
    held = signed(application, "GET", "/v1/accounts/colab/a/credentials")
    assert (held[0], held[1]["code"]) == (409, "colab_login_in_progress")
    assert signed(application, "POST", f"/v1/logins/{again['id']}/cancel")[1]["status"] == (
        "cancelled"
    )
    assert token_path(config.slot_path("colab", "a")).exists()
    assert signed(application, "GET", "/v1/accounts/colab/a/credentials")[0] == 200


@posix_only
def test_a_login_outside_the_allowlist_is_signed_out_again(tmp_path: Path) -> None:
    config = colab_config(tmp_path, allowed_emails=frozenset({"owner@x.test"}))
    application = AgentApplication(config)
    home = config.slot_path("colab", "c")
    (home / "fake-login-email").write_text("intruder@x.test", encoding="utf-8")
    login = signed(application, "POST", "/v1/accounts/colab/c/login")[1]
    signed(application, "POST", f"/v1/logins/{login['id']}/code", {"code": "4/good-code"})
    wait_until(lambda: finished(application, login["id"], FAILED))
    view = signed(application, "GET", f"/v1/logins/{login['id']}")[1]
    assert "not in AI_ACCOUNTS_ALLOWED_EMAILS" in view["error"]
    assert not token_path(home).exists()


@posix_only
def test_a_revoked_token_reads_as_signed_out_and_the_email_comes_from_google_once(
    tmp_path: Path,
) -> None:
    config = colab_config(tmp_path)
    calls: list[str] = []

    class Response:
        def read(self) -> bytes:
            return b'{"email": "second@x.test"}'

        def __enter__(self) -> "Response":
            return self

        def __exit__(self, *_: object) -> None:
            return None

    def opener(request: Any, timeout: float) -> Response:
        calls.append(request.get_header("Authorization"))
        return Response()

    accounts = ColabAccounts(config, opener=opener)
    application = AgentApplication(config, colab=accounts)
    home = config.slot_path("colab", "d")
    (home / "fake-login-unnamed").write_text("", encoding="utf-8")  # No account field.
    login = signed(application, "POST", "/v1/accounts/colab/d/login")[1]
    signed(application, "POST", f"/v1/logins/{login['id']}/code", {"code": "4/good-code"})
    wait_until(lambda: finished(application, login["id"], SUCCEEDED))
    colab_d = slot_of(signed(application, "GET", "/v1/accounts?fresh=1")[1], "colab", "d")
    assert colab_d["email"] == "second@x.test"
    assert calls == ["Bearer ya29.access"]  # Remembered after the first read.

    path = token_path(home)
    revoked = {**json.loads(path.read_text(encoding="utf-8")), "refresh_token": "revoked"}
    path.write_text(json.dumps(revoked), encoding="utf-8")
    colab_d = slot_of(signed(application, "GET", "/v1/accounts?fresh=1")[1], "colab", "d")
    assert colab_d["logged_in"] is False
    assert colab_d["usage_error"] == "the saved sign-in no longer works; sign in again"
    assert colab_d["error"] is None


def test_credentials_need_a_refresh_token(tmp_path: Path) -> None:
    config = colab_config(tmp_path)
    accounts = ColabAccounts(config)
    home = config.slot_path("colab", "e")
    path = token_path(home)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"token": "only-an-access-token"}), encoding="utf-8")
    with pytest.raises(Exception, match="no saved sign-in"):
        accounts.credentials("e")
    assert accounts.has_credentials("e") is True
    assert KEY  # The shared signing key is what the routes above were signed with.
    assert uuid4()
