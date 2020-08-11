# coding: utf-8
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB

metadata = MetaData()


t_rdbms_connections = Table(
    "rdbms_connections",
    metadata,
    Column(
        "connection_id",
        BigInteger,
        primary_key=True,
        server_default=text(
            "nextval('\"public\".rdbms_connections_connection_id_seq'::regclass)"
        ),
    ),
    Column("client_id", BigInteger),
    Column("engine", String, nullable=False),
    Column("host", String, nullable=False),
    Column("username", String, nullable=False),
    Column("password", String, nullable=False),
    Column("port", Integer, nullable=False),
    Column("connection_schema", JSONB(astext_type=Text())),
    Column(
        "rdbms_role", Enum("SOURCE", "SINK", name="rdbms_role"), nullable=False
    ),
    schema="public",
)


t_users = Table(
    "users",
    metadata,
    Column(
        "user_id",
        BigInteger,
        primary_key=True,
        server_default=text(
            "nextval('\"public\".users_user_id_seq'::regclass)"
        ),
    ),
    Column("email", String, unique=True),
    Column("full_name", String),
    Column("password", String),
    Column("is_active", Boolean, nullable=False, server_default=text("true")),
    Column(
        "is_superuser", Boolean, nullable=False, server_default=text("false")
    ),
    Column(
        "created_date", DateTime, nullable=False, server_default=text("now()")
    ),
    schema="public",
)


t_database_replications = Table(
    "database_replications",
    metadata,
    Column(
        "database_id",
        BigInteger,
        primary_key=True,
        server_default=text(
            "nextval('\"public\".database_replications_database_id_seq'::regclass)"
        ),
    ),
    Column(
        "connection_id", ForeignKey("public.rdbms_connections.connection_id")
    ),
    Column("name", String, nullable=False),
    Column("replicate_all", Boolean, server_default=text("false")),
    schema="public",
)


t_debeziumjobs = Table(
    "debeziumjobs",
    metadata,
    Column(
        "debeziumjob_id",
        BigInteger,
        primary_key=True,
        server_default=text(
            "nextval('\"public\".debeziumjobs_debeziumjob_id_seq'::regclass)"
        ),
    ),
    Column(
        "connection_id", ForeignKey("public.rdbms_connections.connection_id")
    ),
    Column("payload", JSONB(astext_type=Text())),
    schema="public",
)


t_tables_replications = Table(
    "tables_replications",
    metadata,
    Column(
        "table_id",
        BigInteger,
        primary_key=True,
        server_default=text(
            "nextval('\"public\".tables_replications_table_id_seq'::regclass)"
        ),
    ),
    Column(
        "database_id", ForeignKey("public.database_replications.database_id")
    ),
    Column("name", String, nullable=False),
    Column("selected_for_replication", Boolean, server_default=text("true")),
    Column(
        "replication_status",
        Enum(
            "STOPPED_BY_USER",
            "STOPPED_BY_EXCEPTION",
            "STARTED",
            name="replication_status",
        ),
    ),
    Column(
        "replication_type",
        Enum("CDC", "FULL", "INCREMENTAL", name="replication_type"),
    ),
    Column("incremental_key", String),
    Column(
        "replication_phase",
        Enum("INITAL", "ONGOING", name="replication_phase"),
    ),
    schema="public",
)


t_columns_exclusions = Table(
    "columns_exclusions",
    metadata,
    Column(
        "column_id",
        BigInteger,
        primary_key=True,
        server_default=text(
            "nextval('\"public\".columns_exclusions_column_id_seq'::regclass)"
        ),
    ),
    Column("table_id", ForeignKey("public.tables_replications.table_id")),
    Column("name", String, nullable=False),
    schema="public",
)
