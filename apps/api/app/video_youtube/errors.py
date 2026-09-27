"""The one exception the YouTube link raises for a request it will not carry out."""

from __future__ import annotations


class Refused(Exception):
    """Why the site will not do this: the admin routes answer it as an ``AppError`` with the same
    status, code and detail. The services raise this rather than ``AppError`` itself, the way
    ``StorageRefused`` and ``SeriesRefused`` do, so they stay usable outside a request."""

    def __init__(self, status: int, code: str, detail: str) -> None:
        super().__init__(detail)
        self.status = status
        self.code = code
        self.detail = detail
