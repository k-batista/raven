#!/bin/sh

command=""

if [ ! -z "$1" ]; then
    command=$1
fi

if [ "$command" = "-t" ]; then
    echo 'Run pytest'   
    pytest --cov=app/ --cov-report=html -s
fi

if [ "$command" = "-test" ]; then
    echo 'Run pytest'
    pytest --cov=app/ --cov-report=html -s
    exit 1
fi

# Usando --exclude "*/application.py"
# Por causa do import gevent.monkey; gevent.monkey.patch_all() 
# que deve ser a primeira coisa a ser importada

if [ "$command" = "-lint" ]; then
    autopep8 --in-place --aggressive --aggressive --max-line-length 79  --exclude="*/application.py" -r app 
    autoflake -i --remove-all-unused-imports -r app
    flake8 app/  --exclude "*/application.py"
    exit 1
fi


if [ "$command" = "-lint-test" ]; then
    autopep8 --in-place --aggressive --aggressive --max-line-length 79  --exclude="*/application.py" -r tests 
    autoflake -i --remove-all-unused-imports -r tests
    flake8 tests/  --exclude "*/application.py"
    exit 1
fi

if [ "$command" = "-format" ]; then
    autopep8 --in-place --aggressive --aggressive --max-line-length 79  --exclude="*/application.py" -r app 
    exit 1
fi

if [ "$command" = "-preload" ]; then
    gunicorn --preload --bind 0.0.0.0:5005 --worker-class=gevent --worker-connections=1000 --workers=1 app.application:app
    exit 1
fi


gunicorn --bind 0.0.0.0:5005 --worker-class=gevent --worker-connections=1000 --workers=1 app.application:app
