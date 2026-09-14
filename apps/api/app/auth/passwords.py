"""What a password has to clear before it becomes an account's only credential.

The policy used to be `Field(min_length=10, max_length=128)` and nothing else, so
``1234567890``, ``password12`` and ``qwertyuiop`` all passed — at registration, at change,
and at reset.

Everything around it is already strong: Argon2 through ``pwdlib``, a dummy hash so a missing
account and a wrong password take the same time, per-account and per-IP login limits, and
``auth_version`` invalidating every live token the moment a password changes. Those bound how
fast someone can guess. They do nothing about a password that is guessed on the third try,
because the third try is well inside any rate limit: ten attempts per account per fifteen
minutes is roughly a thousand a day, which is a list this size several times over.

Two deliberate non-goals.

**No composition rules.** No "must contain an uppercase, a digit and a symbol". They push
people to ``Password1!``, which is on every list ever leaked, and NIST SP 800-63B advises
against them for that reason. A blocklist plus a length floor is the current guidance.

**This is a floor, not a strength meter.** It refuses the passwords that get guessed, not
every password that could be better. A list cannot be complete, so the structural rules below
matter more than the literal entries: they cover the shapes people invent when told their
first choice was rejected, which is where a bare list quietly fails.
"""

from __future__ import annotations

import re
import unicodedata

from app.problems import AppError

# The passwords that lead every published breach corpus, plus the ones this product invites
# by name. Kept short and readable on purpose: a bundled ten-thousand-line word list is a
# blob nobody reviews, and past the first few hundred entries the structural rules below are
# doing the work anyway. Entries are matched case-folded, so only one case appears here.
COMMON_PASSWORDS = frozenset(
    """
    123456 password 123456789 12345678 12345 1234567 1234567890 qwerty abc123 111111
    123123 admin letmein welcome monkey login princess qwertyuiop solo starwars dragon
    passw0rd master hello freedom whatever qazwsx trustno1 654321 jordan23 harley
    password1 password12 password123 password1234 passsword qwerty123 1q2w3e4r 1qaz2wsx
    zaq12wsx asdfghjkl zxcvbnm qwertyui 1234qwer q1w2e3r4 iloveyou sunshine ashley
    bailey shadow superman qazxsw baseball football soccer basketball hockey computer
    michael jennifer jessica charlie daniel hunter thomas summer george andrew joshua
    matthew robert buster ranger tigger pepper mustang corvette ferrari maggie chelsea
    diamond nicole hannah samantha taylor matrix silver internet service secret banana
    cookie chocolate orange purple yellow flower butterfly liverpool arsenal chelseafc
    barcelona realmadrid manchester samsung google facebook youtube twitter instagram
    linkedin whatsapp apple android windows microsoft yahoo hotmail gmail outlook
    aaaaaa aaaaaaaa abcdef abcdefg abcdefgh abcdefghij asdasd asdfasdf qweqwe qweasd
    000000 0000000000 1111111111 121212 112233 123321 555555 666666 696969 777777
    888888 999999 987654321 11111111 22222222 12341234 1234512345 147258369 159753
    a1b2c3d4 abc12345 test1234 temp1234 changeme letmein123 welcome1 welcome123
    admin123 administrator root toor guest default sample example demo1234
    mokaair mokaair123 travelscanner travel123 traveller traveling vacation holiday
    taiwan taipei japan tokyo osaka korea seoul hongkong singapore bangkok
    """.split()
)

# Anything under this is not a passphrase, it is a word with decoration.
_MIN_DISTINCT_CHARACTERS = 5
# Left-to-right runs on the rows people actually have in front of them. Reversed forms are
# derived rather than listed, so the two can never fall out of step.
_KEYBOARD_ROWS = ("qwertyuiop", "asdfghjkl", "zxcvbnm", "1234567890", "!@#$%^&*()")
_SEQUENCES = "abcdefghijklmnopqrstuvwxyz"
_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def _folded(password: str) -> str:
    """Compare the way a person typed it, not the way a codec encoded it.

    NFKC first, so a full-width ``１２３４５６`` is the same password as ``123456``: a
    Japanese or Chinese keyboard produces those without the reader intending anything clever,
    and a blocklist that misses them is a blocklist with a locale-shaped hole in it.
    """
    return unicodedata.normalize("NFKC", password).casefold()


def _is_run(value: str) -> bool:
    """A walk along one keyboard row or the alphabet, forwards or backwards."""
    if len(value) < 4:
        return False
    for row in (*_KEYBOARD_ROWS, _SEQUENCES):
        if value in row or value in row[::-1]:
            return True
    return False


def _is_repeated_unit(value: str) -> bool:
    """``abcabcabc``, ``12341234`` — one short unit typed until it is long enough."""
    for size in range(1, len(value) // 2 + 1):
        if len(value) % size == 0 and value == value[:size] * (len(value) // size):
            return True
    return False


def weak_password_reason(password: str, *, email: str | None = None) -> str | None:
    """Why this password is refused, or ``None`` when it is acceptable.

    Returns the reason rather than a bool so the caller can log which rule fired without
    logging the password. Nothing here is a secret: every rule is public, and knowing that
    ``123456`` is refused tells an attacker nothing they could not have guessed.
    """
    folded = _folded(password)
    if folded in COMMON_PASSWORDS:
        return "common"
    core = _NON_ALNUM.sub("", folded)
    # `password!` and `password123` are the two shapes a composition rule produces, so the
    # blocklist has to see through both rather than treating them as new passwords.
    if core in COMMON_PASSWORDS or core.rstrip("0123456789") in COMMON_PASSWORDS:
        return "common"
    if len(set(folded)) < _MIN_DISTINCT_CHARACTERS:
        return "too_few_distinct"
    if _is_run(folded) or _is_repeated_unit(folded):
        return "patterned"
    if email:
        # The local part is public — it is half of what the attacker already typed to get
        # here — so a password built from it starts the guessing game one move from the end.
        local = _NON_ALNUM.sub("", _folded(email.split("@", 1)[0]))
        if len(local) >= 4 and local in core:
            return "contains_email"
    return None


def reject_weak_password(password: str, *, email: str | None = None) -> None:
    """The single gate. Registration, change and reset all come through here.

    One function rather than a validator on each schema: a policy that holds at registration
    and not at reset is not a policy, and the reset path lives in another module
    (``app.community.accounts``) where a second copy would be easy to forget. A pydantic
    validator was the other candidate and was rejected because it can only raise
    ``validation_error``, whose detail falls back to one generic sentence outside zh-TW —
    the reader would be told to fix something without being told what.
    """
    if weak_password_reason(password, email=email) is None:
        return
    raise AppError(
        422,
        "password_too_common",
        "這個密碼太容易被猜到，請換一個不是常見字串、也和 Email 無關的密碼",
    )
