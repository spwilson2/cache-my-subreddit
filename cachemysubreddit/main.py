import click
import json
from cachemysubreddit.reddit import RedditUser, get_user_submissions
from cachemysubreddit.imgur import Imgur


@click.group()
def cli():
    pass


@cli.command()
@click.option('-l', '--login', type=click.File('r'), required=True)
def friend(login):
    credentials = get_login(login)
    user = RedditUser()

    user.login(**credentials)

    for friend in user.list_friends():
        submissions = get_user_submissions(friend)
        for submission in submissions:
            if Imgur.is_imgur_link(submission):
                Imgur(submission).save_images(submission, 'delete')


def get_login(file_):
    return json.loads(file_.read())
