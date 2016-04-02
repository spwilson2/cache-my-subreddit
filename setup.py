from setuptools import setup, find_packages
setup(
    name = "cachemysubreddit",
    version = "0.0.1",
    packages = find_packages('cachemysubreddit'),

    install_requires = ['selenium', 'praw', 'beautifulsoup4', 'click'],
    include_package_data = True,

    entry_points="""
        [console_scripts]
        cachemysubbreddit=cachemysubreddit.main:cli
        """,

    author = 'Sean Wilson',
    author_email = 'spwilson27@gmail.com',
    description = 'Cache redditor\'s submissions.',
    license = 'MIT',
    url = 'https://github.com/spwilson2/cache-my-subreddit',

)
