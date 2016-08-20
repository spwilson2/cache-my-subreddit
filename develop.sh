#!/bin/bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

clean () {

EXTRA="`find "$DIR" | grep -E -e ".*[.]{1}egg.*" -e "__pycache__" `"

rm -rf build cache_my_subreddit.egg-info dist venv $EXTRA

}

if [ "$1" = 'clean' ]; then
clean

else

virtualenv --clear -p /usr/bin/python3 venv --no-site-packages

source venv/bin/activate

pip3 install -e $DIR

alias test_package='python $DIR/setup.py test'
alias develop='source $DIR/develop.sh' 

if [ $? ]; then printf "
==================================================================
SUCCESS

    You are now running a virtual environment for Cache My 
	Subreddit run 'deactivate' to leave
==================================================================
"

fi

fi
