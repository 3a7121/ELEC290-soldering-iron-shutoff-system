"""Entry point: `python3 -m shutoff` (used by deploy/shutoff.service)."""

from .main import main

raise SystemExit(main())
