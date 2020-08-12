import subprocess  # nosec
import sys

import click

sys.path.extend(["./", "../"])


@click.group("Fast-api App manager")
def manage() -> None:
    # the main group of commands
    pass


@manage.command(help="init db")
def dbconn() -> None:
    from app.core.config import settings

    print(settings.SQLALCHEMY_DATABASE_URI)


@manage.command(help="init db")
def sync_db() -> None:
    """
        Syncs the DDL with the database, and generates sqlalchemy models
    """
    from app.core.config import settings
    from app.utils.migrations import sync, export_all_tables

    sync(settings)
    export_all_tables(settings)


@manage.command(help="commit and push new version")
def commit_new_version() -> None:
    from app.utils.lifecycle import commit_new_version_and_push

    commit_new_version_and_push()


if __name__ == "__main__":
    manage()
