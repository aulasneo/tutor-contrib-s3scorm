"""
Tutor plugin to enable SCORM packages with S3 storage.
"""

from __future__ import annotations

import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    from importlib.resources import files
else:

    def files(_: str) -> Path:
        return Path(__file__).resolve().parent


from tutor import hooks

from .__about__ import __version__

# Configuration
config = {
    "defaults": {
        "BUCKET": "{{ S3_STORAGE_BUCKET | default('', true) }}",
        "ENDPOINT": "",
        "URL_STYLE": "virtual",
        "USE_SSL": True,
        "PATH": "",
        # CDN domain (e.g. a CloudFront distribution) fronting the bucket above.
        # When set, the Caddy reverse proxy targets this domain instead of the
        # S3 endpoint directly, so requests benefit from edge caching and
        # compression while still being served from the LMS/CMS origin.
        "CLOUDFRONT_DOMAIN": "",
        # Seconds browsers/intermediate caches may keep SCORM assets before
        # revalidating. SCORM asset paths are keyed by block usage id and are
        # typically overwritten in place when a course team republishes a
        # package, so this is intentionally conservative by default. Set to
        # 0 to disable the Cache-Control header entirely.
        "CACHE_MAX_AGE": 86400,
        # Let Caddy compress text-based responses (JS/HTML/JSON) on the fly
        # for upstreams that don't already send a compressed representation.
        "COMPRESS": True,
        "VERSION": __version__,
    }
}

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"S3SCORM_{key}", value) for key, value in config["defaults"].items()],
    priority=hooks.priorities.LOW,
)

# Load patches from files
patches_dir = files("tutors3scorm").joinpath("patches")
for path in sorted(patches_dir.iterdir(), key=lambda item: str(item.name)):
    if not path.is_file() or path.name.startswith("."):
        continue
    hooks.Filters.ENV_PATCHES.add_item(
        (path.name, path.read_text(encoding="utf-8")),
        priority=hooks.priorities.LOW,
    )
