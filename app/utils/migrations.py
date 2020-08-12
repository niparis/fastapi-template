import io
import os
from contextlib import contextmanager

from sqlbag.createdrop import create_database, drop_database


def export_all_tables(settings):
    from sqlacodegen.codegen import CodeGenerator
    from sqlalchemy.engine import create_engine
    from sqlalchemy.schema import MetaData

    # Use reflection to fill in the metadata
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    metadata = MetaData(engine)
    metadata.reflect(engine, "public", False, None)
    outfile = io.open(
        os.path.join(settings.MODELS_PATH, "sqla_tables.py"),
        "w",
        encoding="utf-8",
    )
    generator = CodeGenerator(metadata, noclasses=True)
    generator.collector["sqlalchemy"].add("Text")
    generator.render(outfile)
    print("SQLAlchemy tables have been updated")


@contextmanager
def temporary_postgres_database(
    host: str, username: str, password: str, dbname: str = "temp-db"
):
    url = f"postgres://{username}:{password}@{host}:5432/{dbname}"
    try:
        create_database(url)
        print(f"created {url}")
        yield url
    finally:
        drop_database(url)


def sync(settings, silent: bool = True):
    """
        settings: a framework settings object
    """
    from sqlbag import S, temporary_database as temporary_db
    from migra import Migration

    with open(
        os.path.join(settings.DDL_PATH, "database-schema.sql"), "r"
    ) as f:
        ddl = f.read()

    # creates main db if needed
    create_database(settings.SQLALCHEMY_DATABASE_URI)

    with temporary_postgres_database(
        host=settings.DB_HOST,
        username=settings.DB_USER,
        password=settings.DB_PASSWORD,
    ) as TEMP_DB_URL:
        with S(TEMP_DB_URL) as s:
            s.execute(ddl)

        with S(settings.SQLALCHEMY_DATABASE_URI) as s_current, S(
            TEMP_DB_URL
        ) as s_target:
            m = Migration(s_current, s_target)
            m.set_safety(False)
            m.add_all_changes()

            if m.statements:
                print("THE FOLLOWING CHANGES ARE PENDING:", end="\n\n")
                print(m.sql)
                print()
                if (
                    silent
                    or input("Apply these changes (type `yes` to continue)? ")
                    == "yes"
                ):
                    print("Applying...")
                    m.apply()
                else:
                    print("Not applying.")
            else:
                print("Already synced.")
