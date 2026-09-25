import json
import os
import sys
import textwrap
import time
from pathlib import Path
from typing import Any

import pytest

from ai_accounts_agent.antigravity import (
    ACCOUNT_NAME,
    CODE_PATTERN,
    DATA_DIR,
    TOKEN_NAME,
    AntigravityAccounts,
    email_from_logs,
    extract_authorize_url,
    is_authorize_url,
    mask_emails,
    parse_quota,
)
from ai_accounts_agent.config import AgentConfig
from ai_accounts_agent.screen import Screen
from ai_accounts_agent.security import sanitize
from ai_accounts_agent.server import AgentApplication
from ai_accounts_agent.statusline import SNAPSHOT_NAME
from tests.test_ai_accounts_agent import make_config, signed, slot_of, wait_until

posix_only = pytest.mark.skipif(sys.platform == "win32", reason="needs a POSIX terminal")

GOOGLE_URL = (
    "https://accounts.google.com/o/oauth2/auth?access_type=offline&client_id=x.apps."
    "googleusercontent.com&code_challenge=abc&redirect_uri=https%3A%2F%2Fantigravity.google"
    "%2Foauth-callback&response_type=code&state=s1"
)

# What agy 1.2.11 drew on the host (2026-09-25) before and during a sign-in, reduced to the
# parts the agent reads; the quota page after `/usage` follows the strings in the binary.
FAKE_AGY = textwrap.dedent(
    """
    import os, sys, time
    home = os.environ["HOME"]
    data = os.path.join(home, ".gemini", "antigravity-cli")
    os.makedirs(data, exist_ok=True)
    token = os.path.join(data, "jetski-standalone-oauth-token")

    def show(text):
        sys.stdout.write(text)
        sys.stdout.flush()

    if not os.environ.get("DBUS_SESSION_BUS_ADDRESS", "").startswith("unix:path=/dev/null/"):
        show("a keyring would hold every account's login")
        sys.exit(3)
    if not os.path.exists(token):
        show("\\x1b[?1049h\\x1b[2J\\x1b[1;2HWelcome to the \\x1b[1mAntigravity CLI\\x1b[0m. "
             "You are currently not signed in.")
        show("\\x1b[3;2HSelect login method:\\x1b[4;2H> 1. Google OAuth"
             "\\x1b[5;4H2. Use a Google Cloud project")
        sys.stdin.readline()
        url = URL
        show("\\x1b[2J\\x1b[1;2HYour browser should open automatically. If not:")
        show("\\x1b[2;2H\\x1b]8;id=x;" + url + "\\x1b\\\\" + url[:60] + "\\x1b]8;;\\x1b\\\\")
        show("\\x1b[5;2HIf you aren't automatically redirected, paste the authorization "
             "code below:\\x1b[6;2H")
        code = sys.stdin.readline().strip()
        if code.startswith("4/good"):
            control = os.path.join(home, "fake-email")
            email = open(control).read().strip() if os.path.exists(control) else "g@x.test"
            open(token, "w").write("{}")
            with open(os.path.join(data, "cli.log"), "a") as log:
                log.write("I0925 server.go:1] OAuth: authenticated successfully as "
                          + email + "\\n")
            show("\\x1b[2J\\x1b[1;2H" + email + " \\u00b7 Google AI Ultra")
        else:
            show("\\x1b[8;2HError: failed to exchange authorization code for token: "
                 "invalid_grant")
        time.sleep(30)
        sys.exit(0)
    if os.path.exists(os.path.join(home, "fake-trust")):
        show("\\x1b[?1049h\\x1b[2J\\x1b[1;2HDo you trust the contents of this project?"
             "\\x1b[3;2H> Yes, I trust this folder\\x1b[4;4HNo, exit")
        if sys.stdin.readline().strip():
            sys.exit(1)
    if os.path.exists(os.path.join(home, "fake-terms")):
        show("\\x1b[2J\\x1b[1;2HTerms of Service & Data Use\\x1b[3;2H> Accept")
        time.sleep(30)
        sys.exit(0)
    show("\\x1b[?1049h\\x1b[2J\\x1b[1;2Hg@x.test \\u00b7 Google AI Ultra"
         "\\x1b[20;2H> \\x1b[21;2HGemini 3.1 Pro 82%")
    if sys.stdin.readline().strip() != "/usage":
        sys.exit(1)
    bar = "\\u2588" * 8 + "\\u2591" * 2
    show("\\x1b[2J\\x1b[1;2HModels & Quota\\x1b[3;2HGemini Models")
    show("\\x1b[4;4H5-hour limit  " + bar + "  80%  Refreshes in 1h 52m")
    show("\\x1b[5;4HWeekly limit  " + bar + "  50%  Refreshes in 4d 21h")
    show("\\x1b[7;2HClaude and GPT Models\\x1b[8;4HWeekly limit  Disabled")
    time.sleep(30)
    """
).replace("URL", repr(GOOGLE_URL))


def agy_config(tmp_path: Path, **overrides: Any) -> AgentConfig:
    fake = tmp_path / "fake_agy.py"
    fake.write_text(FAKE_AGY, encoding="utf-8")
    values: dict[str, Any] = {
        "agy_command": (sys.executable, str(fake)),
        "code_exchange_timeout_seconds": 4.0,
        "agy_usage_start_seconds": 0.5,
        "agy_usage_page_seconds": 0.5,
        "agy_usage_timeout_seconds": 15.0,
    }
    values.update(overrides)
    return make_config(tmp_path, **values)


def sign_in_on_disk(config: AgentConfig, slot: str, email: str | None = None) -> Path:
    home = config.slot_path("agy", slot)
    data = home / DATA_DIR
    data.mkdir(parents=True, exist_ok=True)
    (data / TOKEN_NAME).write_text("{}", encoding="utf-8")
    if email:
        (data / "cli.log").write_text(
            f"I0925 server.go:1] OAuth: authenticated successfully as {email}\n", "utf-8"
        )
    return home


# --- the terminal screen --------------------------------------------------------------


def test_screen_places_text_where_the_cursor_moves_it() -> None:
    screen = Screen(40, 6)
    screen.feed("\x1b[2;4Hworld\x1b[2;1Hhi\x1b[4;1Hgone\x1b[4;1H\x1b[K\x1b[1;1Htop")
    assert screen.lines() == ["top", "hi world"]


def test_screen_skips_strings_and_waits_for_split_sequences() -> None:
    screen = Screen(40, 4)
    screen.feed("\x1b_Ga=q,f=32;AAAA\x1b\\\x1b]8;id=1;https://x.test\x1b\\link\x1b]8;;\x1b")
    screen.feed("\\ ok\x1b[")
    screen.feed("31mred\x1b[0m")
    assert screen.lines() == ["link okred"]


def test_screen_alternate_buffer_and_scrolling() -> None:
    screen = Screen(10, 2)
    screen.feed("one\r\ntwo\r\nthree")
    assert screen.lines() == ["two", "three"]
    # Like xterm, the alternate screen starts blank with the cursor where it was.
    screen.feed("\x1b[?1049h\x1b[Hpage")
    assert screen.lines() == ["page"]
    screen.feed("\x1b[?1049l")
    assert screen.lines() == ["two", "three"]


# --- the quota page -------------------------------------------------------------------


def test_quota_page_rows_become_windows_per_model_group() -> None:
    lines = [
        "g@x.test · Google AI Ultra",
        "Models & Quota",
        "Gemini Models",
        "  5-hour limit  ████████░░  80%  Refreshes in 1h 52m",
        "  Weekly limit  █████░░░░░  50% remaining  Refreshes in 4d 21h",
        "Claude and GPT Models",
        "  Weekly limit  Disabled",
        "Gemini 3.1 Pro  30% used",
    ]
    windows = parse_quota(lines, now=1_000)
    assert windows == [
        {
            "label": "Gemini Models",
            "window_minutes": 300,
            "used_percent": 20.0,
            "resets_at": 1_000 + 3_600 + 52 * 60,
        },
        {
            "label": "Gemini Models",
            "window_minutes": 10_080,
            "used_percent": 50.0,
            "resets_at": 1_000 + 4 * 86_400 + 21 * 3_600,
        },
        {
            "label": "Gemini 3.1 Pro",
            "window_minutes": None,
            "used_percent": 30.0,
            "resets_at": None,
        },
    ]
    assert parse_quota(["Loading quota…", "Press esc to close"], now=0) == []


# --- sign-in pieces -------------------------------------------------------------------


def test_only_google_authorize_urls_and_codes_pass() -> None:
    assert is_authorize_url(GOOGLE_URL)
    for url in (
        "http://accounts.google.com/o/oauth2/auth",
        "https://accounts.google.com.evil.test/o/oauth2/auth",
        "https://evil.test/o/oauth2/auth?x=accounts.google.com",
        "https://accounts.google.com/signin",
    ):
        assert not is_authorize_url(url)
    output = f"\x1b]8;id=a;{GOOGLE_URL}\x1b\\Click here\x1b]8;;\x1b\\"
    assert extract_authorize_url(output) == GOOGLE_URL
    assert extract_authorize_url(f"visit {GOOGLE_URL} now") == GOOGLE_URL
    assert CODE_PATTERN.fullmatch("4/0AVGzR1Bq-example_code.part")
    for code in ("4/0A code", "4/0A\rkey", "short", "4/0A;rm -rf"):
        assert not CODE_PATTERN.fullmatch(code)


def test_sanitize_hides_google_tokens_and_codes() -> None:
    text = "token ya29.a0AfB_secret refresh 1//0gSecretRefresh code 4/0AVGzR1Bq-secret"
    cleaned = sanitize(text)
    for secret in ("a0AfB_secret", "0gSecretRefresh", "AVGzR1Bq-secret"):
        assert secret not in cleaned
    assert mask_emails("signed in as owner@x.test") == "signed in as ***@x.test"


def test_email_comes_from_the_newest_log(tmp_path: Path) -> None:
    data = tmp_path / DATA_DIR
    (data / "log").mkdir(parents=True)
    old = data / "log" / "cli-1.log"
    old.write_text("OAuth: authenticated successfully as old@x.test\n", "utf-8")
    os.utime(old, (1, 1))
    assert email_from_logs(data) == "old@x.test"
    (data / "cli.log").write_text(
        "noise\nOAuth: authenticated successfully as new@x.test\nmore noise\n", "utf-8"
    )
    assert email_from_logs(data) == "new@x.test"
    assert email_from_logs(tmp_path / "missing") is None


# --- accounts from files --------------------------------------------------------------


def test_status_details_and_logout_read_and_clear_the_files(tmp_path: Path) -> None:
    config = agy_config(tmp_path)
    accounts = AntigravityAccounts(config)
    assert accounts.status("a")["logged_in"] is False
    home = sign_in_on_disk(config, "a", "g@x.test")
    (home / ACCOUNT_NAME).write_text(json.dumps({"plan": "Pro"}), "utf-8")
    status = accounts.status("a")
    assert status == {
        "logged_in": True,
        "auth_method": "google",
        "email": "g@x.test",
        "organization": None,
        "plan": "Pro",
    }
    assert accounts.details("a") == {"usage": None}
    window = {"label": "Gemini", "window_minutes": 300, "used_percent": 20.0, "resets_at": 9}
    (home / SNAPSHOT_NAME).write_text(
        json.dumps({"recorded_at": 5, "windows": [window, {"bad": 1}], "error": None}), "utf-8"
    )
    assert accounts.details("a") == {
        "usage": {"source": "snapshot", "recorded_at": 5, "windows": [window]},
        "usage_error": None,
    }
    accounts.logout("a")
    assert accounts.status("a")["logged_in"] is False
    assert not (home / SNAPSHOT_NAME).exists()
    assert not (home / ACCOUNT_NAME).exists()


def test_environment_gives_each_account_its_own_home_and_no_keyring(tmp_path: Path) -> None:
    config = agy_config(tmp_path)
    environment = AntigravityAccounts(config).environment("c")
    assert environment["HOME"] == str(config.slot_path("agy", "c"))
    assert environment["DBUS_SESSION_BUS_ADDRESS"].startswith("unix:path=/dev/null/")
    assert environment["AGY_CLI_DISABLE_AUTO_UPDATE"] == "true"
    assert "AI_ACCOUNTS_AGENT_HMAC_KEY" not in environment


# --- the CLI in a terminal ------------------------------------------------------------


@posix_only
def test_page_login_picks_google_takes_the_code_and_reads_the_quota(tmp_path: Path) -> None:
    config = agy_config(tmp_path, allowed_emails=frozenset({"g@x.test"}))
    application = AgentApplication(config)
    status, login = signed(application, "POST", "/v1/accounts/agy/a/login")
    assert status == 201
    assert (login["kind"], login["url"]) == ("paste_code", GOOGLE_URL)
    status, _ = signed(
        application, "POST", f"/v1/logins/{login['id']}/code", {"code": "4/good-code-123"}
    )
    assert status == 202
    wait_until(
        lambda: signed(application, "GET", f"/v1/logins/{login['id']}")[1]["status"] == "succeeded",
        20,
    )

    def account() -> dict[str, Any]:
        return slot_of(signed(application, "GET", "/v1/accounts")[1], "agy", "a")

    # The finished login probes the quota page at once.
    wait_until(lambda: bool(account()["usage"]), 30)
    card = account()
    assert (card["logged_in"], card["email"], card["auth_method"]) == (True, "g@x.test", "google")
    assert card["plan"] == "Ultra"
    assert [
        (w["label"], w["window_minutes"], w["used_percent"]) for w in card["usage"]["windows"]
    ] == [
        ("Gemini Models", 300, 20.0),
        ("Gemini Models", 10_080, 50.0),
    ]


@posix_only
def test_a_rejected_code_fails_without_echoing_it(tmp_path: Path) -> None:
    config = agy_config(tmp_path)
    application = AgentApplication(config)
    login = signed(application, "POST", "/v1/accounts/agy/b/login")[1]
    signed(application, "POST", f"/v1/logins/{login['id']}/code", {"code": "4/bad-code-456"})
    wait_until(
        lambda: signed(application, "GET", f"/v1/logins/{login['id']}")[1]["status"] == "failed",
        20,
    )
    view = signed(application, "GET", f"/v1/logins/{login['id']}")[1]
    assert "failed to exchange" in view["error"]
    assert "bad-code" not in view["error"]


@posix_only
def test_an_account_outside_the_list_is_signed_out_again(tmp_path: Path) -> None:
    config = agy_config(tmp_path, allowed_emails=frozenset({"owner@x.test"}))
    (config.slot_path("agy", "c")).mkdir(parents=True, exist_ok=True)
    (config.slot_path("agy", "c") / "fake-email").write_text("stranger@x.test", "utf-8")
    application = AgentApplication(config)
    login = signed(application, "POST", "/v1/accounts/agy/c/login")[1]
    signed(application, "POST", f"/v1/logins/{login['id']}/code", {"code": "4/good-code-789"})
    wait_until(
        lambda: signed(application, "GET", f"/v1/logins/{login['id']}")[1]["status"] == "failed",
        20,
    )
    assert "stranger@x.test" in signed(application, "GET", f"/v1/logins/{login['id']}")[1]["error"]
    assert not AntigravityAccounts(config).has_credentials("c")


@posix_only
def test_the_probe_leaves_first_run_pages_to_the_owner(tmp_path: Path) -> None:
    config = agy_config(tmp_path)
    home = sign_in_on_disk(config, "d", "g@x.test")
    (home / "fake-terms").write_text("", "utf-8")
    started = time.monotonic()
    accounts = AntigravityAccounts(config)
    assert accounts.refresh_usage("d") is False
    assert time.monotonic() - started < 10
    assert accounts.details("d")["usage_error"] == "setup_needed"


@posix_only
def test_the_probe_records_windows_email_and_plan(tmp_path: Path) -> None:
    config = agy_config(tmp_path)
    home = sign_in_on_disk(config, "e")
    # The probe's own folder is trusted on the way; nothing else on the host is.
    (home / "fake-trust").write_text("", "utf-8")
    accounts = AntigravityAccounts(config)
    assert accounts.refresh_usage("e") is True
    usage = accounts.details("e")["usage"]
    assert [window["used_percent"] for window in usage["windows"]] == [20.0, 50.0]
    status = accounts.status("e")
    assert (status["email"], status["plan"]) == ("g@x.test", "Ultra")
