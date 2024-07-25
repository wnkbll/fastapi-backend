#!/bin/bash

alembic upgrade head

# shellcheck disable=SC2164
cd src

fastapi run main.py
