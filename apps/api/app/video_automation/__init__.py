"""The video pipeline running on the host from the owner's settings (docs/videos/AUTOMATION.md).

The owner chooses on /admin/videos which model writes and checks each stage, how often a draft
is made and on what topics, how the finished video sounds and looks, what it may spend, and
whether narration Jev passes line by line is approved without them. The worker reads these
settings with its video tool token; the site's AI keys never leave the API.
"""
