#!/bin/bash
set -euxo pipefail

poetry run pre-commit run --all-files