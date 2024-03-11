from __future__ import annotations

import os
import os.path
from glob import glob

import click
import pkg_resources
from tutor import hooks

from .__about__ import __version__

########################################
# CONFIGURATION
########################################

config = {
    # Add here your new settings
    "defaults": {
        "USE_SSL": True,
        "PATH": ""
    }
}

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"S3SCORM_{key}", value) for key, value in config["defaults"].items()]
)

########################################
# PATCH LOADING
########################################

# For each file in tutors3scorm/patches,
# apply a patch based on the file's name and contents.
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutors3scorm", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))
