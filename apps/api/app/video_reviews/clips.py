"""An imported drama's upload package also carries its per-shot clips (``clip_<shot>`` mp4s).

`import --publish` (tools/video/import/import.mjs) runs where the episode was made, a cloud
session's Colab workdir, and its 1080p clips (about 40 a season-one episode, 300 MB) are gone
with the container. Sent with the upload package, they sit in the review store until the host's
worker fetches the approved package into video_work/<slug>/ (tools/video/automation/
review-package.mjs), and the full-tier Drive backup then keeps ``clips/`` with the episode
(docs/videos/BACKUP.md §匯入的影片; tasks/open/2026-10-31-zhong-tian-clip-backup.md).

They count apart from the 48 files a review may carry (``schemas.MAX_REVIEW_FILES``), and only
the publish gate takes them. This lives beside ``schemas.ReviewIn`` rather than in it because
``schemas.py`` is bound by the long-form duration review receipt
(docs/videos/long-form/review.json).
Nothing that reads a package (the YouTube upload, the manual upload page and zip, the language
package) looks at a ``clip_`` role; ``prune_published_previews`` lets them go with the other mp4s.
"""

from __future__ import annotations

from typing import Self

from pydantic import Field, model_validator

from app.video_reviews.schemas import MAX_REVIEW_FILES, ReviewFile, ReviewIn

MAX_CLIP_FILES = 120
CLIP_ROLE_PREFIX = "clip_"


class SubmittedReview(ReviewIn):
    """A review as the video tool submits it: ``ReviewIn`` with room for a package's clips."""

    files: list[ReviewFile] = Field(
        default_factory=list, max_length=MAX_REVIEW_FILES + MAX_CLIP_FILES
    )

    @model_validator(mode="after")
    def _clips_only_in_a_package(self) -> Self:
        clips = [item for item in self.files if item.role.startswith(CLIP_ROLE_PREFIX)]
        if len(self.files) - len(clips) > MAX_REVIEW_FILES:
            raise ValueError(f"a review carries at most {MAX_REVIEW_FILES} files besides clips")
        if clips and self.gate != "publish":
            raise ValueError("only an upload package (the publish gate) carries clip_ files")
        if len(clips) > MAX_CLIP_FILES:
            raise ValueError(f"an upload package carries at most {MAX_CLIP_FILES} clips")
        if any(item.content_type != "video/mp4" for item in clips):
            raise ValueError("a clip_ file is an mp4")
        return self
