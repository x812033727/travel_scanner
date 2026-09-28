"""Where the worker's Shorts jobs go (ticket video-shorts-automation-api): the next job, the
weekly plan, new topics, the weekly report, and a Short's start and finish; and the tab's
topics, assets and reports. Registered in ``app.main`` already, so that ticket adds routes
here and nowhere else.

The file name carries ``admin`` on purpose: its errors are the operator's, in Traditional
Chinese, and ``tests/test_error_localization.py`` asks for four more languages of any
``AppError`` raised outside an admin file.
"""

from __future__ import annotations

from fastapi import APIRouter

admin_router = APIRouter(prefix="/admin/video-shorts", tags=["admin video shorts"])
tool_router = APIRouter(prefix="/video/automation/shorts", tags=["video shorts (pipeline)"])
