#!/bin/bash
source .env
poetry publish --username $PYPI_USERNAME --password $PYPI_PASSWORD