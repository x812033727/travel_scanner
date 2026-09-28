"""Where the routes that send Shorts to YouTube go (ticket video-shorts-youtube-auto): the
worker's ``POST /video/automation/shorts/tick``, and the tab's claim-by-filename, recall and
batch download. Registered in ``app.main`` already, so that ticket adds routes here and
nowhere else.

The file name carries ``admin`` on purpose: its errors are the operator's, in Traditional
Chinese, and ``tests/test_error_localization.py`` asks for four more languages of any
``AppError`` raised outside an admin file.
"""

from __future__ import annotations

from fastapi import APIRouter

admin_router = APIRouter(prefix="/admin/video-shorts", tags=["admin video shorts"])
tool_router = APIRouter(prefix="/video/automation/shorts", tags=["video shorts (pipeline)"])
