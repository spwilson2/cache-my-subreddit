#!/bin/bash

clean () {

EXTRA="`find . | grep -E ".*[.]{1}egg.*"`"

rm -rf build cache_my_subreddit.egg-info dist venv $EXTRA
}

if [ "$1" = 'clean' ]; then
clean

else

virtualenv --clear --download -p /usr/bin/python3 venv --no-site-packages

source venv/bin/activate

#pip install -r scripts/requirements.txt


if [ $? ]; then printf "
==================================================================
SUCCESS

    You are now running a virtual environment for Reddit Image Bot
    run 'deactivate' to leave
==================================================================
"

fi

fi
