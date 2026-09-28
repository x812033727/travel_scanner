"""The one error the Shorts module raises; the routers turn it into the API's problem response."""

from __future__ import annotations


class ShortsRefused(Exception):
    """Why a Shorts request was not carried out, in the owner's words."""

    def __init__(self, status: int, code: str, detail: str):
        super().__init__(detail)
        self.status = status
        self.code = code
        self.detail = detail
