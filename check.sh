#!/bin/bash

poetry run ruff check .
poetry run mypy .
poetry run pytest .
# Currently, mutmut mutation test has around 30% survival rate.
# This is not good enough and I may want to improve it in the future
poetry run mutmut run
poetry check