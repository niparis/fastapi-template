#!/bin/bash
set -euxo pipefail

poetry run mypy --ignore-missing-imports app/
poetry run safety check  --ignore 38624 --ignore 38625 # A curated database of insecure Python packages
poetry run bandit -r app/ -x app/utils/lifecycle.py,app/utils/migrations.py,app/core/gunicorn_conf.py
poetry run radon cc app -a