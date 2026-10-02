"""Compatibility entry point; use the API environment with PYTHONPATH=apps/api.

On the production host, use python -m app.video_automation.planning_cli inside the
API container. All validation, transaction handling and audit live in the API code.
"""

from app.video_automation.planning_cli import main

if __name__ == "__main__":
    main()
