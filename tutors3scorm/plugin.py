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
        "BUCKET": "{{ S3_STORAGE_BUCKET }}",
        "USE_SSL": True,
        "PATH": "",
        "VERSION": __version__,
    }
}

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"S3SCORM_{key}", value) for key, value in config["defaults"].items()]
)

# Load patches from files
patches_dir = files("tutors3scorm").joinpath("patches")
for path in sorted(patches_dir.iterdir(), key=lambda item: str(item.name)):
    if not path.is_file() or path.name.startswith("."):
        continue
    hooks.Filters.ENV_PATCHES.add_item((path.name, path.read_text(encoding="utf-8")))
