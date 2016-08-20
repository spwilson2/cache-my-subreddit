# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## UNRELEASED
### MODIFIED
- setup.py 
Changed the entrypoint (program name) to cachemysubreddit (previously typoed to cachemysubbreddit)
- develop.sh
Remove the --download flag to fix problems on other computers
- cachemysubreddit/main.py
Adds ability to download a subreddit with option `subreddit and -s <subreddit>`
- cachemysubreddit/reddit.py
Adds storage of mangled post titles as the folder name.

## [0.2.2] - 2016-04-15
### MODIFIED
- cachemysubreddit/imgur.py
- cachemysubreddit/main.py
imgur is not queried if the directories, for which images would be placed in, already exist.


## [0.2.1] - 2016-04-12
### MODIFIED
- cachemysubreddit/imgur.py
If there imgur album was deleted or does not exist don't create a blank folder and don't fail catastrophically.

## [0.2.0] - 2016-04-12
### ADDED
- CHANGELOG.md
- Considering this as an alpha release, although will tag as normal.

### Addition Notes
