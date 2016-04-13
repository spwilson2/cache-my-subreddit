import click
import re
import json
import os
from cachemysubreddit.reddit import RedditUser, get_user_submissions
from cachemysubreddit.imgur import Imgur


@click.group()
def cli():
    pass


@cli.command()
@click.option('-l', '--login', type=click.File('r'), required=True)
@click.option('-d', '--daemonize', default=False)
@click.option('-p', '--path', type=click.Path(), default='./')
def friend(login, daemonize, path):
    credentials = get_login(login)
    user = RedditUser()

    top_path = os.path.abspath(path)

    user.login(**credentials)
    for friend in user.list_friends():

        friend_path = clean_for_use_as_path(friend)
        friend_path = os.path.join(top_path, friend_path)

        submissions = get_user_submissions(friend)

        for title, url in submissions:

            title_path = clean_for_use_as_path(title)
            title_path = os.path.join(friend_path, title_path)

            if Imgur.is_imgur_link(url):
                Imgur(url).save_images(title_path, 'delete')


def daemon_entry_point(credentials):

    user = RedditUser()
    user.login(**credentials)

    #TODO Be smarter.
    for friend in user.list_friends():
        submissions = get_user_submissions(friend)
        for title, url in submissions:
            if Imgur.is_imgur_link(url):
                Imgur(url).save_images(title, 'delete')

def get_login(file_):
    return json.loads(file_.read())

def clean_for_use_as_path(string):
    string = re.sub(r'[^\w\- ]+', '', string)
    string = re.sub(r'[ ]+', '_', string)
    return string
