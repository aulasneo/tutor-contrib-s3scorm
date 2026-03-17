"""
Tutor plugin to enable SCORM packages with S3 storage.
"""
from __future__ import annotations

from importlib import resources

from tutor import hooks

from .__about__ import __version__

# Configuration
config = {
    "defaults": {
        "USE_SSL": True,
        "PATH": "",
        "VERSION": __version__,
    }
}

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"S3SCORM_{key}", value) for key, value in config["defaults"].items()]
)

# Load patches from files
patches_dir = resources.files("tutors3scorm").joinpath("patches")
for path in sorted(patches_dir.iterdir(), key=lambda item: item.name):
    if not path.is_file() or path.name.startswith("."):
        continue
    hooks.Filters.ENV_PATCHES.add_item((path.name, path.read_text(encoding="utf-8")))
