"""The copy of each uploaded video in the owner's Google Drive (docs/videos/BACKUP.md).

The video worker does the copying with rclone; this package holds what the owner sets on the
settings tab of /admin/videos (where in Drive, how much of each series) and what the worker
reports about each video, so the page can say whether every uploaded video is safely in
``AI/備份`` before the host deletes its files.
"""
