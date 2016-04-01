from setuptools import setup, find_packages
setup(
    name = "cache-my-subreddit",
    version = "0.0.1",
    packages = find_packages('cache-my-subreddit'),

    install_requires = ['selenium', 'praw', 'beautifulsoup4'],

    scripts = ['cache-my-subreddit/main.py'],

    #entry_points={
    #    'main_entry': [
    #        'cache-my-subreddit=main:main'
    #        ]
    #    },

    author = 'Sean Wilson',
    author_email = 'spwilson27@gmail.com',
    description = 'Cache redditor\'s submissions.',
    license = 'MIT',
    url = 'https://github.com/spwilson2/cache-my-subreddit',

)
