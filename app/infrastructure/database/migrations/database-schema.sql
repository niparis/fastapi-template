
create table users (
    user_id bigserial primary key,
    email varchar unique,
    full_name varchar,
    password varchar,
    is_active Boolean default true not null,
    is_superuser Boolean default false not null,
    created_date Timestamp default now() not null
);


CREATE TYPE "rdbms_role" AS ENUM (
  'SOURCE',
  'SINK'
);

CREATE TYPE "replication_status" AS ENUM (
  'STOPPED_BY_USER',
  'STOPPED_BY_EXCEPTION',
  'STARTED'
);

CREATE TYPE "replication_type" AS ENUM (
  'CDC',
  'FULL',
  'INCREMENTAL'
);

CREATE TYPE "replication_phase" AS ENUM (
  'INITAL',
  'ONGOING'
);

CREATE TABLE "rdbms_connections" (
  "connection_id" bigserial PRIMARY KEY,
  "client_id" bigint,
  "engine" varchar NOT NULL,
  "rdbms_role" rdbms_role NOT NULL,
  "host" varchar NOT NULL,
  "username" varchar NOT NULL,
  "password" varchar NOT NULL,
  "port" int NOT NULL,
  "connection_schema" jsonb
);

CREATE TABLE "database_replications" (
  "database_id" bigserial PRIMARY KEY,
  "connection_id" bigint,
  "name" varchar NOT NULL,
  "replicate_all" boolean DEFAULT false
);

CREATE TABLE "tables_replications" (
  "table_id" bigserial PRIMARY KEY,
  "database_id" bigint,
  "name" varchar NOT NULL,
  "selected_for_replication" boolean DEFAULT true,
  "replication_status" replication_status,
  "replication_type" replication_type,
  "incremental_key" varchar,
  "replication_phase" replication_phase
);

CREATE TABLE "columns_exclusions" (
  "column_id" bigserial PRIMARY KEY,
  "table_id" bigint,
  "name" varchar NOT NULL
);

CREATE TABLE "debeziumjobs" (
  "debeziumjob_id" bigserial PRIMARY KEY,
  "connection_id" bigint,
  "payload" jsonb
);

ALTER TABLE "database_replications" ADD FOREIGN KEY ("connection_id") REFERENCES "rdbms_connections" ("connection_id");

ALTER TABLE "tables_replications" ADD FOREIGN KEY ("database_id") REFERENCES "database_replications" ("database_id");

ALTER TABLE "columns_exclusions" ADD FOREIGN KEY ("table_id") REFERENCES "tables_replications" ("table_id");

ALTER TABLE "debeziumjobs" ADD FOREIGN KEY ("connection_id") REFERENCES "rdbms_connections" ("connection_id");

COMMENT ON COLUMN "database_replications"."replicate_all" IS 'if true all the tables should be replicated';

COMMENT ON COLUMN "tables_replications"."selected_for_replication" IS 'by default all tables are proposed to be replicated';

COMMENT ON COLUMN "tables_replications"."replication_type" IS 'can be CDC, INCREMENTAL, FULL. Overrides parent settings';

COMMENT ON COLUMN "tables_replications"."incremental_key" IS 'column name to be used for incremental replication';

COMMENT ON COLUMN "tables_replications"."replication_phase" IS 'used to distinguised ';

COMMENT ON COLUMN "debeziumjobs"."payload" IS 'last payload sent to dbz';
