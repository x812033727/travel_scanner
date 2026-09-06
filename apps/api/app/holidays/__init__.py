"""Public holidays for Taiwan, Japan and Korea, vendored rather than fetched at runtime.

A national calendar changes once a year and is published months ahead, so the data lives
in ``data/*.json`` and is reviewed as a pull-request diff. ``refresh.py`` re-reads the two
government files and reports the difference; nothing here calls the network at runtime.
"""
