"""Shared evidence storage boundary; model requests have separate input budgets."""

# Keep the extractor's existing 40,000-character ceiling. The scanner and refresh used
# to discard another 80% of that body, including rollout details and closing footnotes.
# This is a per-page storage limit, not permission to send an unbounded set of pages.
MAX_EVIDENCE_CHARACTERS = 40_000


def evidence_excerpt(text: str) -> str:
    return text[:MAX_EVIDENCE_CHARACTERS]


class NewsInputTooLarge(ValueError):
    """The complete stage input needs editorial attention before a model can see it.

    ValueError is deliberately non-retryable in jobs.run_candidate: retrying the same
    oversized evidence would not make it fit, and silently cutting it would hide facts.
    """
