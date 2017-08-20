# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## UNRELEASED

## TODO
- Optimize the parsing use a .find loop rather than multiple find\_all.
- Bring back support for reading list of all friends rather than through praw.
- Use a hash to detect duplicates of downloaded images 
    - Use symlinks to keep a structure and store hashes in a flat directory.
- Add support for downloading from multiple clients and saving to a single server.
- Add parsing of user comments to look for links.

## [0.5.8] - 2017-8-19
### ADDED
- Improved reliability when network connections temporarily fail.
  - Multiple attempts to download an album will be made before soft failing, an exception will no longer occur.
### MODIFIED
- Fix downloading of non jpg from imgur based on file type
- Automatically shorten filenames to appropriate length (Full titles can't be used)

## [0.5.7] - 2017-8-19
### ADDED
- `user` subcommand to download from a specific reddit user.

## [0.5.6] - 2017-8-19
### MODIFIED
- Fix subreddit names for reddit's new shortened urls
- Fix download for updated gyfcat

## [0.5.5] - 2016-12-27
### ADDED
- Support for EroShare

## [0.5.4] - 2016-12-27
### MODIFIED
- cms/main.py
  - Change subreddit argument to required, rather than option.

## [0.5.3] - 2016-12-27
### MODIFIED
- cms/main.py
  - Database saves entries even if unable to download
- cms/database.py
  - Queries database before looking at saving files

### ADDED
- Added support for gfycat posts

## [0.5.2] - 2016-12-24
### BUGFIX
- friends functionality fixed
  - Caused by inability to find friend name by parsing on submitted links

## [0.5.1] - 2016-12-24
### ADDED
- subreddit and friends options take --number flag to allow limit setting for downloads.

## [0.5.0] - 2016-12-24
### ADDED
- Addded a database for entries and their saved file paths.

### MODFIED
- cachemysubreddit/
  - Renamed to cms/

### REWRITTEN
- cms/imgur.py
  - Changed to requests only api, less likey to run into port issues.
- cms/config.py
  - Changed to an .ini based config
- cms/main.py
  - Removed subreddit functionality for this release
- cms/reddit.py
  - Changed to use praw-4.0 
  - Refactored submitted code

## [0.4.1] - 2016-08-20
### MODIFIED
- cachemysubreddit/imgur.py
 - Hotfix to fix attempts to remake directories.

## [0.4.0] - 2016-08-20
### MODIFIED
- cachemysubreddit/main.py
  - No longer need the argument -l for login, as auth is done with praw.ini
- cachemysubreddit/reddit.py
  - Login and inner workings are ported to praw3. Once reddit no longer supports logins with username and password, will need to rework.

## [0.3.0] - 2016-08-20
### MODIFIED
- setup.py 
  - Changed the entrypoint (program name) to cachemysubreddit (previously typoed to cachemysubbreddit)
- develop.sh
  - Remove the --download flag to fix problems on other computers
- cachemysubreddit/main.py
  - Adds ability to download a subreddit with option `subreddit and -s <subreddit>`
- cachemysubreddit/reddit.py
  - Adds storage of mangled post titles as the folder name.

## [0.2.2] - 2016-04-15
### MODIFIED
- cachemysubreddit/imgur.py
- cachemysubreddit/main.py
  - imgur is not queried if the directories, for which images would be placed in, already exist.


## [0.2.1] - 2016-04-12
### MODIFIED
- cachemysubreddit/imgur.py
  - If there imgur album was deleted or does not exist don't create a blank folder and don't fail catastrophically.

## [0.2.0] - 2016-04-12
### ADDED
- CHANGELOG.md
- Considering this as an alpha release, although will tag as normal.

### Addition Notes
