# cache-my-subreddit

cachemysubreddit is currently in the early stages of development, however it has reached a point where it is usable! So development will now tend to be done in separate branches, for users this means you can at least use this script for it's basic purpose of downloading user's submissions.

## Developing

To set up the development environment source develop.sh by running 

```
source develop.sh
```

or 

```
. develop.sh
```

To run the all unit tests use the alias `test_package` which is  provided after sourcing develop. If you want to reload the development environment after already having sourced develop, use the provided alias `develop`

## Installation

To install simply clone and use the setuptools setup.py.

```
git clone https://github.com/spwilson2/cache-my-subreddit
cd cache-my-subreddit
sudo python3 setup.py install
```

## Running

To run after instillation or sourcing develop.sh

```
cachemysubreddit friends [-p <path to top level directory>]

cachemysubreddit subreddit <subreddit> [-p <path to top level directory>]
```
Your login file must be a praw.ini file stored in $HOME/.config/ constructed as follows:


```
[Reddit]
username: 
password: 
client_id: 
client_secret: 
```

To get your client_id and client secret go to https://www.reddit.com/prefs/apps/

Make sure to change the permissions after writing the file!

```
chmod 400 praw.ini
```
