from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import AwareDatetime, BaseModel, Field

# A web application client of a Google Cloud project: "<number>-<id>.apps.googleusercontent.com".
CLIENT_ID_PATTERN = r"^[0-9]{6,20}-[a-z0-9]{8,64}\.apps\.googleusercontent\.com$"
Mode = Literal["upload", "studio"]
Visibility = Literal["scheduled", "unlisted", "private"]


class ConnectionView(BaseModel):
    """The settings tab's YouTube card. The client secret and the refresh token never appear."""

    client_id: str | None
    client_secret_set: bool
    # What the owner registers as the client's authorized redirect URI in Google Cloud.
    redirect_uri: str
    scope: str
    configured: bool
    linked: bool
    channel_id: str | None
    channel_title: str | None
    channel_url: str | None
    linked_at: datetime | None
    verified_at: datetime | None
    problem: str | None
    audited: bool


class ClientIn(BaseModel):
    """The owner's OAuth client. A null secret keeps the stored one."""

    client_id: str = Field(pattern=CLIENT_ID_PATTERN, max_length=255)
    client_secret: str | None = Field(default=None, min_length=8, max_length=200, pattern=r"^\S+$")
    audited: bool = False


class OAuthStartIn(BaseModel):
    # A random value the web route keeps in an HttpOnly cookie; the callback must bring it back.
    browser_binding: str = Field(min_length=32, max_length=200)


class OAuthStartOut(BaseModel):
    authorization_url: str
    flow_id: str
    state: str
    expires_in: int


class OAuthExchangeIn(BaseModel):
    flow_id: str = Field(min_length=16, max_length=200)
    state: str = Field(min_length=16, max_length=200)
    code: str = Field(min_length=1, max_length=2000)
    browser_binding: str = Field(min_length=32, max_length=200)


class UnlinkOut(BaseModel):
    # False when Google could not be told; the owner then removes the access in their account.
    revoked: bool
    connection: ConnectionView


class PublishIn(BaseModel):
    """What the owner sends from the "ready to upload" card.

    ``upload``: the site uploads the approved mp4 itself (until the project passes the API audit,
    YouTube locks such an upload private, so ``accept_private_lock`` must say the owner knows).
    ``studio``: the owner uploaded the mp4 in Studio and pastes its address in ``url``. Either way
    the site then writes the details, the captions and the thumbnail. ``visibility`` "scheduled"
    needs ``publish_at``: the video stays private until YouTube publishes it then.
    """

    mode: Mode
    url: str | None = Field(default=None, max_length=500)
    visibility: Visibility = "scheduled"
    publish_at: AwareDatetime | None = None
    # The zh-TW title and description as the owner left them on the card (YouTube's Required
    # Minimum Functionality: the uploader sets them); None takes the package's own.
    title: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=5000)
    accept_private_lock: bool = False
