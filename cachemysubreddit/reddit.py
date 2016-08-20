import re
import itertools
import praw

USER_AGENT='sheenrocks\' user agent'
REDDIT_SITE='Reddit'
TIME_BETWEEN_GETS = 1
unauth_reddit = praw.Reddit(user_agent=USER_AGENT)


class RedditUser(object):

    def __init__(self):
        global main_user
        main_user = self

    def login(self):
        """Log in to reddit using the credentials given by praw.ini."""
        self.reddit = praw.Reddit(user_agent=USER_AGENT, site_name=REDDIT_SITE)

        self.reddit.login() # DEPRECATED careful about keeping.

    def list_friends(self):
        print(self.reddit.get_friends())
        return self.reddit.get_friends() # Deprecated

    def friends_submissions(self):
        submissions = (friend.get_submitted(list=1000) for friend in self.list_friends())

        if not submissions:
            return None

        chained_submissions = next(submissions)

        # Chain all generators into a single generator
        for submission_gen in submissions:
            chained_submissions = itertools.chain(chained_submissions,
                    submission_gen)

        return chained_submissions


def get_user_submissions(username):
    """Return a list of submitted content from the user."""

    redditor = unauth_reddit.get_redditor(username)

    if not reddit:
        return None

    return redditor.get_submitted()


def get_top_posts_from_subreddit(subreddit):
    """Return a list of the 'hot' links on a subreddit"""

    return unauth_reddit.get_subreddit(subreddit).get_hot(list=10)


def get_submission_from_url(url, depth=500):
    unauth_reddit.get_content(url)
