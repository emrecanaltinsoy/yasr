#!/bin/bash
source .env
twine upload dist/* -u $TWINE_USERNAME -p $TWINE_PASSWORD