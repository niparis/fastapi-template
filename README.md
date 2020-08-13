# FAST-api base service

Implementing the [hexagonal architecture](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)), a simplified version of the Clean architecture from uncle bob.

## Stack

- Using [fastapi](https://fastapi.tiangolo.com), a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- An async database driver, using [encode](https://www.encode.io/databases/) and [asyncpg](https://github.com/MagicStack/asyncpg), the fastest Postgres database driver for python
- Environment and dependencies handled by [poetry](https://python-poetry.org/)
- Automatic code formatting using [Black](https://black.readthedocs.io/en/stable/installation_and_usage.html#) and automatic sorting of imports using [isort](https://github.com/timothycrosley/isort)

## Preparation

You can run the app in ways: in a docker container or locally.
I recommend to try the docker method first as it's easier to set up. Revert to the local method if docker is eating too much of your RAM.

The docker container way uses VS Code Remote containers. Like any docker based development, the main benefit is the automated setup - you don't have to worry about 

VS Code remote containers adds a few benefits to this:
- Code auto-completion uses the python version and libraries installed in the container (normally it uses what is on your local machine)
- The configuration specified which IDE extension should be installed, so that we have a consistent dev experience
- Easily use the vscode debugger 

### First time [container]

#### Pre-requisites: 

1. Docker installed (and running)
2. Using VS Code as your IDE


#### Steps

1. Start VS Code in the folder. 
2. Install the "Remote - Containers" extension
3. Add your ssh credentials to the ssh agent. This ensures you'll be able to push/pull from the container
    ex : `ssh-add $HOME/.ssh/id_rsa` (you might have to modify this if you're not using the default key)
Note: does NOT work if you're using a passphrase
4. Click on the green box at the lower left corner of VS Code and select "Remote-Containers: Open in Container"
5. Wait for the container to build
6. Update the database schema and genrate the SQLalchmey tables (`poetry run task manage sync-db`)
7. Run the app with the development server (`poetry run task app`)

Go to http://127.0.0.1:8000/doc for the swagger doc

#### Steps - Later

1. Run the app with the development server (`poetry run task app`)

### First time [local]

#### Pre-requisites
:
1. Install Python 3.8: I recommend using [PyEnv](https://github.com/pyenv/pyenv)
2. Install [poetry](https://python-poetry.org/docs/)
3. Install [postgresapp](https://postgresapp.com)

#### Steps - Setup

1. Start your IDE in the folder. 
2. Create a copy of the settings (`cp .dist.env .env`). Modify the database user (`DB_USER`) - unless you're bob - , it should be your system user if you're using postgresapp.
3. Install depencies and create a virtual environment (`poetry install`)
4. Activate the virtual environment (`poetry shell`)
5. Activate pre-commit hooks (after `poetry shell`, run `pre-commit install`).
6. Update the database schema and genrate the SQLalchmey tables (`poetry run task manage sync-db`)
7. Run the app with the development server (`poetry run task app`)

Go to http://127.0.0.1:8000/doc for the swagger doc

#### Steps - Later

1. Activate the virtual environment (`poetry shell`) (might be automatic depending on your IDE)
2. Run the app with the development server (`poetry run task app`)

## Typical development workflow

1. Update the DDL (`database-schema.sql`)
2. Run `poetry run task manage sync-db` to update the database and the SQLA tables
3. Create a query file & a class to query the new table (`infrastructure/database/queries`)
4. Create the schemas in the `domain` folder 
5. Create the service in the `domain` folder
6. Create a *service factory* in the `servicesfac.py` file
7. Create a new *router* as a new file in the `api/endpoints` folder)
8. Link the router to the main router in `api.py`

### run tests

1. poetry run task tests

## code organisation

- `api`    : the http layer. Deserialize request. Chooses which status code to return. Serializes the response. No logic behind that.
- `core`   : config (app and gunicorn) and db initialization
- `domain` : Business logic. Each entity has one subfolder, with 2 files: a schema file, and a service file. Schema file defines how to ser/des the business objects, while the service contains all the business logic
- `infrastructure`: Code to interface with any infra (database, cache, queue, other apis)
- `infrastructure/database`: Database code. Contains: `migrations`: DDL to setup database, as `.sql`, `models`: the SQLAlchemy core table representation of the database, `queries`: Classes to manage all the data access.
- `tasks` : Contains any asynchronous task [doc](https://www.starlette.io/background/)
- `utils` : Generic code, reusable for any service. to be moved in a library at a later point
- `root`  :  `main` application factory, `manage` python scripts 

## Important commands

All commands to be executed after `poetry shell` if your IDE does'nt do it automatically

### Development

- poetry run app : Runs the app with the dev server
- poetry run app-prod: Runs the app with the production server
- poetry run manage db-sync: Syncs changes to the DDL file (`database-schema.sql`) to the database and the sqlalchemy models
- poetry run test : Runs the test suite

### Release

- poetry version <patch|minor|major>: updates the version 
- poetry run task manage commit-new-version: updates git tag, add changed files, commits, pushes (including version)


## notes

Couple of caveats:
- some endpoints still are using the old sync model


