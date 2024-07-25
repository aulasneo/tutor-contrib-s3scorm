"""
Tutor plugin to enable SCORM packages with S3 storage.
"""
from __future__ import annotations

import os.path
from glob import glob

import importlib_resources
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
for path in glob(str(importlib_resources.files("tutors3scorm") / "patches" / "*")):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))
