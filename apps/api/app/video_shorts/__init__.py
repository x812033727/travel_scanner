"""The Shorts tab on /admin/videos (docs/videos/SHORTS.md).

A Short is a row of ``video_projects`` whose ``shorts_line`` is set. This package holds what
is the Shorts' own: their settings and the owner's standing consent to publish, the slot
calendar, the numbers YouTube reported, and the ledger of what they cost. The review gates,
the file store and the YouTube sync stay where they are (``app.video_reviews``,
``app.video_youtube``); they call in here for the rules that differ.
"""
