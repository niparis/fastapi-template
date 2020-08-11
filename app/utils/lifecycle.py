import subprocess
from typing import Tuple

import tomlkit


def ask_confirm(text):
    while True:
        answer = input(f"{text} [y/n]: ").lower()
        if answer in ("j", "y", "ja", "yes"):
            return True
        if answer in ("n", "no", "nein"):
            return False


def _get_project_meta():
    with open("pyproject.toml") as pyproject:
        file_contents = pyproject.read()

    return tomlkit.parse(file_contents)["tool"]["poetry"]


def get_version_and_service_name() -> Tuple[str, str]:
    """
        Pre-requisite: Poetry. Uses name and version number from pyproject.toml
        Usage: in the main `__init__.py`

            from app.utils.lifecycle import get_version_and_service_name
            __version__, SERVICE_NAME = get_version_and_service_name()
    """
    pkg_meta = _get_project_meta()
    return str(pkg_meta["version"]), str(pkg_meta["name"])


def commit_new_version_and_push() -> None:
    version, _ = get_version_and_service_name()

    if ask_confirm(f"Commit and push new version (v{version})?"):
        subprocess.run(["git", "add", "-u"])
        subprocess.run(["git", "commit", "-m", f"bump version to v{version}"])
        subprocess.run(
            ["git", "tag", "-a", f"v{version}", "-m", f"v{version}"]
        )
        subprocess.run(["git", "push", "--follow-tags"], check=True)
