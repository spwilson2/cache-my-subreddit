from setuptools import setup, find_packages

setup(
    name = "cachemysubreddit",
    version = "0.4.0",
    packages = find_packages(),

    install_requires = ['praw', 'click', 'bs4', 'urllib3'],
    include_package_data = True,

    entry_points="""
        [console_scripts]
        cachemysubreddit=cachemysubreddit.main:cli
        """,

    test_suite='nose.collector',
    tests_require=['nose'],#, 'nose-cover3'],

    author = 'Sean Wilson',
    author_email = 'spwilson27@gmail.com',
    description = 'Cache redditor\'s submissions.',
    license = 'MIT',
    url = 'https://github.com/spwilson2/cache-my-subreddit',

)
