import click
import re
import json
import os
from cachemysubreddit.reddit import RedditUser, get_user_submissions, get_top_posts_from_subreddit
from cachemysubreddit.imgur import Imgur

_global_test_options = [
    click.option('-l', '--login', type=click.File('r'), required=True),
    click.option('-p', '--path', type=click.Path(), default='./')
]

def global_test_options(func):
    for option in reversed(_global_test_options):
        func = option(func)
    return func

@click.group()
def cli():
    pass


@cli.command()
@global_test_options
@click.option('-s', '--subreddit', type=str, required=True)
def subreddit(login, path, subreddit):
    credentials = get_login(login)
    user = RedditUser()
    user.login(**credentials)

    submissions = get_top_posts_from_subreddit(subreddit)

    top_path = os.path.abspath(path)

    subreddit_path = clean_for_use_as_path(subreddit)
    subreddit_path = os.path.join(top_path, subreddit_path)

    for title, url in submissions:

        title_path = clean_for_use_as_path(title)
        title_path = os.path.join(subreddit_path, title_path)

        if not Imgur.test_save_exists(title_path):
            if Imgur.is_imgur_link(url):
                Imgur(url).save_images(title_path, 'delete')


@cli.command()
@click.option('-d', '--daemonize', default=False)
@global_test_options
def friend(login, daemonize, path):
    credentials = get_login(login)
    user = RedditUser()


    top_path = os.path.abspath(path)

    user.login(**credentials)
    for friend in user.list_friends():
        friend_path = clean_for_use_as_path(friend.name)
        friend_path = os.path.join(top_path, friend_path)

        submissions = get_user_submissions(friend)

        for title, url in submissions:
            print(str(title), str(url))

            title_path = clean_for_use_as_path(title)
            title_path = os.path.join(friend_path, title_path)

            if not Imgur.test_save_exists(title_path):
                if Imgur.is_imgur_link(url):
                    Imgur(url).save_images(title_path, 'delete')


def daemon_entry_point(credentials):
    # TODO
    pass

def get_login(file_):
    return json.loads(file_.read())

def clean_for_use_as_path(string):
    string = re.sub(r'[^\w\- ]+', '', string)
    string = re.sub(r'[ ]+', '_', string)
    return string
