#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

clean () {

EXTRA="`find "$DIR" | grep -E -e ".*[.]{1}egg.*" -e "__pycache__" `"

rm -rf build cache_my_subreddit.egg-info dist venv $EXTRA

}

if [ "$1" = 'clean' ]; then
clean

else

virtualenv --clear --download -p /usr/bin/python3 venv --no-site-packages &&

source venv/bin/activate  &&

#python3 setup.py develop
#pip install -r develrequirements.txt
pip3 install nose &&

pip3 install -e $DIR &&

alias test_package='python $DIR/setup.py test'

if [ $? ]; then printf "
==================================================================
SUCCESS

    You are now running a virtual environment for Reddit Image Bot
    run 'deactivate' to leave
==================================================================
"

fi

fi
