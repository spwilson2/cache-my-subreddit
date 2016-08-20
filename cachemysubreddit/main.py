import click
import re
import json
import os
from cachemysubreddit.reddit import RedditUser, get_user_submissions, get_top_posts_from_subreddit
from cachemysubreddit.imgur import Imgur

_global_test_options = [
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
@click.argument('subreddit')
@global_test_options
def subreddit(path, subreddit):

    top_path = os.path.abspath(path)

    subreddit_path = clean_for_use_as_path(subreddit)
    subreddit_path = os.path.join(top_path, subreddit_path)

    for submission in get_top_posts_from_subreddit(subreddit):
        title = submission.title
        url = submission.url
        author = submission.author

        print('Title: %s\tAuthor: %s' % (title, author))

        title_path  = clean_for_use_as_path(title)
        author_path = clean_for_use_as_path(author.name)

        main_path = os.path.join(subreddit_path, author_path)
        main_path = os.path.join(main_path, title_path)

        if not Imgur.test_save_exists(main_path):
            if Imgur.is_imgur_link(url):
                Imgur(url).save_images(main_path, 'delete')


@cli.command()
@global_test_options
def friends(path):
    user = RedditUser()

    top_path = os.path.abspath(path)

    user.login()

    for submission in user.friends_submissions():
        title = submission.title
        url = submission.url
        friend = submission.author
        subreddit = submission.subreddit.display_name

        subreddit_path = clean_for_use_as_path(subreddit)
        friend_path = clean_for_use_as_path(friend.name)
        title_path = clean_for_use_as_path(title)

        main_path = os.path.join(top_path, subreddit_path)
        main_path = os.path.join(main_path, friend_path)
        main_path = os.path.join(main_path, title_path)

        if not Imgur.test_save_exists(main_path):
            if Imgur.is_imgur_link(url):
                print('Title: %s\tFriend: %s\tSubreddit: %s' % (title, friend, subreddit))
                Imgur(url).save_images(main_path, 'delete')

def clean_for_use_as_path(string):
    string = re.sub(r'[^\w\- ]+', '', string)
    string = re.sub(r'[ ]+', '_', string)
    return string
