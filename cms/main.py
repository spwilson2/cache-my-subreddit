import os
import re

import click

import cms.imgur
import cms.reddit
from cms.config import read_oauth_info, write_oauth_info

CHAR_WHITELIST = r'\w,.\- '

@click.group()
def cli():
    pass

@cli.command()
@click.option('-c', '--config', type=click.Path(), default='./login.ini')
def config(config):
    write_oauth_info(config)

@cli.command()
@click.option('-s', '--subreddit', type=click.STRING)
@click.option('-c', '--config', type=click.Path(), default='./login.ini')
@click.option('-o', '--output', type=click.Path(), default='./output')
def subreddit(output, config, subreddit):

    client_id, client_secret, username, password =\
    read_oauth_info(config)

    r = cms.reddit.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password)

    for submission in r.subreddit_submissions(subreddit, limit=30):
        save(submission, basedir=output)


@cli.command()
@click.option('-c', '--config', type=click.Path(), default='./login.ini')
@click.option('-o', '--output', type=click.Path(), default='./output')
def friends(output, config):
    client_id, client_secret, username, password =\
    read_oauth_info(config)

    r = cms.reddit.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password)

    friends = r.list_friends()

    for friend in friends:
        print('==================================================================')
        print('Downloading uploads for %s' % friend)
        print('==================================================================')
        for submission in r.user_submissions(friend):
            save(submission, basedir=output)


def clean_for_use_as_path(string):
    string = re.sub(r'[^%s]' % CHAR_WHITELIST, '-', string)
    string = re.sub(r'[ ]+', '_', string) # Replace spaces with _
    return string

def save(submission, basedir='output'):
    basedir = os.path.dirname(os.path.abspath(__file__)) if basedir is None else basedir

    # subreddit/user/PostName
    clean_title = clean_for_use_as_path(submission.title)
    savedir = os.path.join(basedir, submission.subreddit, submission.author, clean_title)


    if not os.path.exists(savedir):
        os.makedirs(savedir)
    else:
        # If dir is made, assume save already exists.
        print('%s already exists, skipping...' % submission.title)
        return

    print('Title: %-30s\tFriend: %-15s\tSubreddit: %-15s' %
            (submission.title, submission.author, submission.subreddit))

    if cms.imgur.Imgur.is_link(submission.url):
        cms.imgur.Imgur(submission.url).save(savedir,pfx='Post')

if __name__ == '__main__':
    friends('./')
