import getpass
import os
import stat

# Fix safe input for python
try: input = raw_input
except NameError: pass

try:
    from configparser import ConfigParser
except:
    from ConfigParser import ConfigParser

REDDIT_SECTION = 'Reddit'

def read_oauth_info(file_='login.ini'):
    parser = ConfigParser()
    print(file_)
    parser.read(file_)
    section = parser[REDDIT_SECTION]

    return section['client_id'], section['client_secret'], \
            section['username'], section['password']

def write_oauth_info(file_='login.ini'):
    parser = ConfigParser()
    parser.add_section(REDDIT_SECTION)
    options = {}
    options['username'] = input('Reddit username: ')
    options['password'] = getpass.getpass('Reddit password: ')
    options['client_id'] = getpass.getpass('client_id: ')
    options['client_secret'] = getpass.getpass('client_secret: ')

    with open(file_, 'w') as f:
        for key, val in options.items():
            parser.set(REDDIT_SECTION, key, val)
        parser.write(f)
    os.chmod(file_, stat.S_IRUSR|stat.S_IRGRP)
