"""MiniMax as a music vendor in the drama settings: offered, accepted, stale names refused.

Kept out of test_video_automation_settings.py on purpose: that file is bound by the long-form
duration review receipt (tools/video/long-form/review.mjs REVIEW_FILES), so adding a test there
would need a DURATION_ONLY review increment; the helpers are imported from it instead.
"""

from __future__ import annotations

from app.config import Settings
from app.video_automation import settings as service
from app.video_automation.schemas import SettingsWrite
from tests.test_video_automation_settings import _drama, _values


def test_minimax_is_a_music_vendor_the_settings_tab_offers_and_accepts() -> None:
    """Switching the music vendor to MiniMax used to keep lyria-3.5 under it (MiniMax had no
    music model, so the tab had nothing to pick) and the save was refused by name. MiniMax now
    offers music-3.0 first, and both its models save on the key image-01 uses."""
    offered = service.media_options_view().music["minimax"]
    assert [option.value for option in offered] == ["music-3.0", "music-2.6"]
    assert all(option.usd_per_track == 0.15 for option in offered)
    assert "2026-08-20" in (offered[0].description or "")
    runtime = Settings(
        hotspot_guide_gemini_api_key="g",
        minimax_api_key="m",
        azure_speech_voices="zh-TW-HsiaoChenNeural",
    )
    for model in ("music-3.0", "music-2.6"):
        drama = _drama(drama_enabled=True, music_provider="minimax", music_model=model)
        assert service.settings_problems(SettingsWrite(**_values(drama=drama)), runtime) == []
    stale = _drama(music_provider="minimax", music_model="lyria-3.5")
    assert service.settings_problems(SettingsWrite(**_values(drama=stale)), runtime) == [
        "音樂：minimax 沒有 lyria-3.5 這個模型"
    ]
