"""The one error the stage runners raise; admin_api turns it into the API's problem response."""

from __future__ import annotations


class StageFailed(Exception):
    """Why a stage did not run or did not finish. The router turns it into the API's error."""

    def __init__(self, status: int, code: str, detail: str, retry_after: str | None = None):
        super().__init__(detail)
        self.status = status
        self.code = code
        self.detail = detail
        self.retry_after = retry_after
