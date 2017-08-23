import os
import re

import click
import requests

import cms.downloader
import cms.reddit
from cms.config import read_oauth_info, write_oauth_info
from cms.database import Database

CHAR_WHITELIST = r'\w,.\- '

_download_options = [
    click.option('-c', '--config', type=click.Path(), default='./login.ini',
        help='Path of the config file.'),
		click.option('-o', '--output', type=click.Path(), default='./output', help='Dir to output all files to.'),
		click.option('-d', '--databasedir', type=click.Path(), default='./output', help='Dir to place the sqlite database in.'),
        click.option('-n', '--number', type=click.INT, default=10, help='The number of posts to download.'),
]

def _add_options(options):
    def __add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return __add_options


@click.group()
def cli():
    pass

@cli.command()
@click.option('-c', '--config', type=click.Path(), default='./login.ini', help='Path of the config file.')
def config(config):
    write_oauth_info(config)

@cli.command()
@click.argument('subreddit', type=click.STRING)
@_add_options(_download_options)
def subreddit(output, number, config, subreddit, databasedir):

    client_id, client_secret, username, password =\
        read_oauth_info(config)

    r = cms.reddit.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password)

    database = Database(databasedir)

    for submission in r.subreddit_submissions(subreddit, limit=number):
        save(submission, database, basedir=output)


@cli.command()
@_add_options(_download_options)
def friends(output, config, databasedir, number):
    client_id, client_secret, username, password =\
        read_oauth_info(config)

    r = cms.reddit.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password)

    friends = r.list_friends()

    database = Database(databasedir)

    for friend in friends:
        print('==================================================================')
        print('Downloading uploads for %s' % friend)
        print('==================================================================')
        def save_user_submissions():
            for submission in r.user_submissions(friend, limit=number):
                save(submission, database, basedir=output)
        retval = _retry_on_connection_fail(save_user_submissions)
        if retval is None:
            print ('ConnectionError! There may be something wrong with your'
                    ' connection.')

@cli.command()
@click.argument('username', type=click.STRING)
@_add_options(_download_options)
def user(output, config, databasedir, number, username):

    client_id, client_secret, client_username, password =\
            read_oauth_info(config)

    r = cms.reddit.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=client_username,
            password=password)

    database = Database(databasedir)

    print('==================================================================')
    print('Downloading uploads for %s' % username)
    print('==================================================================')
    def save_user_submissions():
        for submission in r.user_submissions(username, limit=number):
            save(submission, database, basedir=output)
            pass
    retval = _retry_on_connection_fail(save_user_submissions)
    if retval is None:
        print ('ConnectionError! There may be something wrong with your'
                ' connection.')


def clean_for_use_as_path(string):
    string = re.sub(r'[^%s]' % CHAR_WHITELIST, '-', string)
    string = re.sub(r'[ ]+', '_', string) # Replace spaces with _
    # Shorten the title so the path is reasonable.
    return string[:60]

def save(submission, database, basedir='output'):
    basedir = os.path.dirname(os.path.abspath(__file__)) if basedir is None else basedir

    if database.exists(submission):
        print('%s already exists, skipping...' % submission.title)
        return

    # Download files if have a suitable downloader...
    downloader = cms.downloader.UniversalDownloader(submission.url).downloader
    images = 0
    savedir = ''
    if downloader:

        # subreddit/user/PostName
        clean_title = clean_for_use_as_path(submission.title)
        savedir = os.path.join(basedir, submission.subreddit, submission.author, clean_title)

        if os.path.exists(savedir):
            pass
        else:
            os.makedirs(savedir)

        # Number of retries to download
        images = _retry_on_connection_fail(lambda:downloader.save(savedir,
                pfx='Post'))
        if images is None:
            # We failed the allotted number of times don't add it to the
            # database.
            print('Unable to reach the destination of %s, skipping...' % submission.title)
            return
        else:
            images = images[0]

        # Add the file to our database.
        print('Title: %-30s\tFriend: %-15s\tSubreddit: %-15s' %
                (submission.title, submission.author, submission.subreddit))
        database.add_post(submission, images, savedir)

def _retry_on_connection_fail(func, retries=3):
    for _ in range(retries):
        try:
            return (func(),)
        except requests.exceptions.ConnectionError:
            # Retry again if failed to connect
            pass
if __name__ == '__main__':
    friends('./')
