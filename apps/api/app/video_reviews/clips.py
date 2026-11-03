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

Since 2026-11-03 a package sent with `review-push` from a work directory the worker did not make
(a cloud session's 奇聞檔案局 episode) carries the rest of the full backup tier the same way, so the
host holds the whole video before it goes up (owner, 2026-11-03; docs/videos/BACKUP.md): each
keyframe as ``kf_<name>`` (an episode has 230-320 of them), and ``keyframes_manifest``,
``full_narration`` (narration.wav), ``full_timeline`` (timeline.json) and the line recordings
``recording_<locale>``/``recordings_manifest`` that `import --publish` already sends. They count
apart from the 48 as well; nothing that reads a package looks at these roles either.
"""

from __future__ import annotations

from typing import Self

from pydantic import Field, model_validator

from app.video_reviews.schemas import MAX_REVIEW_FILES, ReviewFile, ReviewIn

MAX_CLIP_FILES = 120
CLIP_ROLE_PREFIX = "clip_"
MAX_KEYFRAME_FILES = 400
KEYFRAME_ROLE_PREFIX = "kf_"
# The full tier's other files: a few per video (one recording a language).
MAX_BACKUP_FILES = 24
BACKUP_ROLES = frozenset(
    {"keyframes_manifest", "full_narration", "full_timeline", "recordings_manifest"}
)
RECORDING_ROLE_PREFIX = "recording_"


def _backup_only(role: str) -> bool:
    return role in BACKUP_ROLES or role.startswith(RECORDING_ROLE_PREFIX)


class SubmittedReview(ReviewIn):
    """A review as the video tool submits it: ``ReviewIn`` with room for a package's clips."""

    files: list[ReviewFile] = Field(
        default_factory=list,
        max_length=MAX_REVIEW_FILES + MAX_CLIP_FILES + MAX_KEYFRAME_FILES + MAX_BACKUP_FILES,
    )

    @model_validator(mode="after")
    def _clips_only_in_a_package(self) -> Self:
        clips = [item for item in self.files if item.role.startswith(CLIP_ROLE_PREFIX)]
        keyframes = [item for item in self.files if item.role.startswith(KEYFRAME_ROLE_PREFIX)]
        backup = [item for item in self.files if _backup_only(item.role)]
        if len(self.files) - len(clips) - len(keyframes) - len(backup) > MAX_REVIEW_FILES:
            raise ValueError(
                f"a review carries at most {MAX_REVIEW_FILES} files besides the backup tier's"
            )
        if clips and self.gate != "publish":
            raise ValueError("only an upload package (the publish gate) carries clip_ files")
        if len(clips) > MAX_CLIP_FILES:
            raise ValueError(f"an upload package carries at most {MAX_CLIP_FILES} clips")
        if any(item.content_type != "video/mp4" for item in clips):
            raise ValueError("a clip_ file is an mp4")
        if keyframes and self.gate != "publish":
            raise ValueError("only an upload package (the publish gate) carries kf_ files")
        if len(keyframes) > MAX_KEYFRAME_FILES:
            raise ValueError(f"an upload package carries at most {MAX_KEYFRAME_FILES} keyframes")
        if any(item.content_type not in ("image/png", "image/jpeg") for item in keyframes):
            raise ValueError("a kf_ file is a png or a jpeg")
        if len(backup) > MAX_BACKUP_FILES:
            raise ValueError(f"a review carries at most {MAX_BACKUP_FILES} other backup-tier files")
        return self
