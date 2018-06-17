#!/bin/bash

export UNIT_TEST='true'

if [[ "$APP_ENV" == "staging" ]]; then
    echo "Initating container services"
   ./start.sh &
    sleep 5
fi

RUN_ALL="yes"
ALL_TESTS="lib/*"
TEST=""
SCRIPT_NAME=$0
STOP_ON_ERROR_FLAG=''
DB_REBUILD="no"
RETVAL=0
CHANNEL=""
DB_MIGRATION="no"
LOG_LEVEL="DEBUG"

while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
        -o|--only)
        RUN_ALL="no"
        TEST="$TEST $2"
        shift
        ;;
        -h|--help)
            echo "Usage: $SCRIPT_NAME filename"
            echo "    -l --level: set logging level"
            echo "    -c --channel: channel to run tests against"
            echo "    -d --skip-db-rebuild: do not rebuild the DB"
            echo "    -m --skip-db-migration: do not run alembic"
            echo "    -o --only <test filename>: run only this filename,  can be used multiple times"
            echo "    -p --plat: plat to create databases against"
            echo "    -x --stop: stop on first test failure or error"
            echo "    -h --help: display this message"
            exit 1
        shift
        ;;
        -x|--stop)
        STOP_ON_ERROR_FLAG="-x"
        shift
        ;;
        -l|--level)
        LOG_LEVEL=$2
        shift
        ;;
        -d|--skip-db-rebuild)
        DB_REBUILD="no"
        shift
        ;;
        -c|--channel)
        CHANNEL=$2
        shift
        ;;
        -p|--plat)
        PLAT=$2
        shift
        ;;
        -m|--skip-db-migration)
        DB_MIGRATION="no"
        shift
        ;;
        *)
            echo "Option: $key is unknown" # unknown option
        ;;
    esac
    shift # past argument or value
done

if [[ -z "$TESTS_TO_RUN" ]] ; then
    TESTS_TO_RUN=$TEST
fi

if [[ "$RUN_ALL" == "yes" ]] ; then
  echo Running all tests. This may take some time.
  echo
  echo "***"
  TESTS_TO_RUN=$ALL_TESTS
else
  echo Running $TESTS_TO_RUN.
  echo
  echo "***"
  TESTS_TO_RUN=$TEST
fi


DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
export PYTHONPATH=$DIR/..

echo Removing any lingering .pyc files
find /srv -name "*.pyc" -exec rm -f {} \;

# add functionality to create databases on the fly, and execute alembic migrations

cd $PYTHONPATH/tests/

if [[ "$RUN_ALL" == "yes" ]] ; then
  nosetests -vv -s --cover-html \
  --cover-html-dir=htmlcov \
  --cover-erase \
  --cover-min-percentage=35 \
  --with-coverage \
  --cover-package=app.lib app.lib app.api \
  --logging-filter=root $TESTS_TO_RUN $STOP_ON_ERROR_FLAG \
  --logging-level=$LOG_LEVEL
else
  nosetests -vv $TESTS_TO_RUN $STOP_ON_ERROR_FLAG
fi
