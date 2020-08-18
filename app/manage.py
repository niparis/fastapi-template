"""
    isort:skip_file
"""
import sys

import click

sys.path.extend(["./", "../"])

from app.core.config import settings


@click.group(f"{settings.SERVICE_NAME} manager")
def manage() -> None:
    # the main group of commands
    pass


@manage.command(help="init db")
@click.option(
    "--dropdb",
    default=False,
    help="Drop your database and re-creates it. Use sparringly.",
    is_flag=True,
)
@click.option(
    "--silent",
    default=False,
    help="Drop your database and re-creates it. Use sparringly.",
    is_flag=True,
)
def sync_db(silent: bool = False, dropdb: bool = False) -> None:
    """
        Syncs the DDL with the database, and generates sqlalchemy models
    """
    from app.core.config import settings
    from app.utils.migrations import sync, export_all_tables

    sync(settings, silent=silent, dropdb=dropdb)
    export_all_tables(settings)


@manage.command(help="commit and push new version")
def commit_new_version() -> None:
    from app.utils.lifecycle import commit_new_version_and_push

    commit_new_version_and_push()


if __name__ == "__main__":
    manage()
