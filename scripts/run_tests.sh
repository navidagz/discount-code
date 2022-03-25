#!/usr/bin/bash

if [ "$1" == "html" ]; then
    pytest --cov=app --cov-report=html  tests/
else
    pytest --cov=app tests/test*
fi

rm -rf ./test.db