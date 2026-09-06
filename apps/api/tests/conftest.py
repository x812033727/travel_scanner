"""Test-session environment.

The integration suite registers one account per test through the real
`/auth/register` endpoint, and the whole suite runs from a single client IP
against one Redis. The product cap of 30 registrations per IP per hour is the
right number for production and the wrong one for a test run that is now past
30: the last module to register got a 429 in CI, with nothing wrong in it.

`setdefault` keeps an explicit environment override in charge, and the value
must be in place before `app.config.get_settings()` is first called, which is
why it lives here rather than in a fixture.
"""

from __future__ import annotations

import os

os.environ.setdefault("AUTH_REGISTER_IP_LIMIT", "500")
