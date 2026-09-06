"""A reader who cannot type 「綁定」 still has to be able to connect, and to be answered.

The keyword set used to be three Traditional Chinese words compared exactly, and anything
else was met with silence — which from the reader's side is indistinguishable from a bot
that is simply broken.
"""

from __future__ import annotations

import pytest

from app.line.router import LINK_KEYWORDS, UNKNOWN_MESSAGE_REPLY, wants_link


@pytest.mark.parametrize(
    "text",
    ["綁定", "連結帳號", "綁定帳號"],
)
def test_the_words_already_in_use_still_work(text: str) -> None:
    """These are printed on the alerts page and people are typing them today."""
    assert wants_link("message", text) is True


@pytest.mark.parametrize(
    "text",
    ["link", "connect", "連携", "リンク", "연결", "계정 연결", "绑定", "关联账号"],
)
def test_a_reader_can_use_a_word_from_their_own_language(text: str) -> None:
    assert wants_link("message", text) is True


@pytest.mark.parametrize("text", ["LINK", " Connect ", "  綁定  "])
def test_case_and_stray_spaces_do_not_decide_the_outcome(text: str) -> None:
    assert wants_link("message", text) is True


def test_following_the_bot_is_the_same_request() -> None:
    assert wants_link("follow", "") is True


@pytest.mark.parametrize("text", ["你好", "hello", "取消", "??"])
def test_anything_else_is_not_a_link_request(text: str) -> None:
    assert wants_link("message", text) is False


def test_the_reply_to_an_unknown_message_names_a_word_for_every_reader() -> None:
    """A reader who cannot read the sentence must still find the word to send."""
    for keyword in ("綁定", "link", "連携", "연결"):
        assert keyword in UNKNOWN_MESSAGE_REPLY
        assert keyword.casefold() in LINK_KEYWORDS
    assert len(UNKNOWN_MESSAGE_REPLY.splitlines()) == 4
