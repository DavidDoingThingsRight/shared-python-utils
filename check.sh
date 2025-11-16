#!/bin/bash

poetry run ruff check .
poetry run mypy .
poetry run pytest .
poetry check