import requests
from time import sleep
import re
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as _B
import praw

USER_AGENT='sheenrocks\' user agent'
REDDIT_SITE='Reddit'

def BeautifulSoup(*args, **kwargs):
    return _B(*args, 'html.parser', **kwargs)

class RedditUser(object):

    def __init__(self):
        global main_user
        main_user = self

    def login(self, user, passwd):
        """Log in to reddit using the given credentials."""
        self.reddit = praw.Reddit(user_agent=USER_AGENT, site_name=REDDIT_SITE)

        self.reddit.login() # DEPRECATED careful about keeping.
        self.reddit.get_submissions

        response = requests.post(
                'https://www.reddit.com/api/login',
                {'user': user, 'passwd': passwd},
                headers = FAKE_HEADERS
                )
        self.cookies = response.cookies

    def list_friends(self):
        print(self.reddit.get_friends())
        return self.reddit.get_friends() # Deprecated

    #    """Return a list of friend's usernames."""
    #    response = self.get_url( 'https://www.reddit.com/prefs/friends/')

    #    friends_bsobj = BeautifulSoup(response.text)

    #    assert(friends_bsobj.find('table'))

    #    friend_anchors = friends_bsobj.find('table').find_all('a',
    #          href=re.compile('^https://www.reddit.com/user/[^/]*/$'))

    #    return [anchor.text for anchor in friend_anchors]

    def get_url(self, url):
        """Return the response from getting the url as the signed in user."""
        return requests.get(
                url,
            cookies=self.cookies,
            headers=FAKE_HEADERS
        )

    def friends_submissions():
        for friend in self.list_friends():
            print(friend.get_submitted(limit=1000))



def get_user_submissions(username):
    """Return a list of all urls to submitted content from the user."""

    submitted_url = 'https://www.reddit.com/user/%s/submitted/' % (username)

    return _get_submissions_from_url(submitted_url)



def get_top_posts_from_subreddit(subreddit):
    """Return a list of the 'hot' links on a subreddit"""
    subreddit_url = 'https://www.reddit.com/r/%s/hot/' % (subreddit)

    return _get_submissions_from_url(subreddit_url, depth=1)


def _get_submissions_from_url(url, depth=500):

    def get_next_link(response):
        possible_link = BeautifulSoup(response.text).find(
                'a',
                rel='nofollow next')

        if possible_link is not None:
            return possible_link['href']

    def get_submission_links_and_titles(submission_html):
        bs_obj = BeautifulSoup(submission_html)
        anchors = bs_obj.find_all('a', class_="title may-blank outbound ")
        # NOTE: Need to use the following if we try to access the submission
        # while logged in
        if not anchors:
            anchors = bs_obj.find_all('a', class_="title may-blank loggedin outbound ")
        if anchors:
            return ((anchor.text, anchor['href']) for anchor in anchors)

    response = get_url(url)
    submission_links = []

    # Get the next submission
    submissions = get_submission_links_and_titles(response.text)

    #submissions = [ (post_url, get_post_metadata(post_url)) for post_url in submissions]

    if submissions is None:
        return []

    submission_links.extend(submissions)

    # Traverse all the user's submitted pages.
    next_link = get_next_link(response)

    num_submissions = len(submission_links)

    submissions_gathered = 1

    while (submissions_gathered < num_submissions) and (depth > 0) and next_link:

        sleep(TIME_BETWEEN_GETS)

        response = get_url(next_link)
        submissions = get_submission_links_and_titles(response.text)

        if submissions is not None:
            submission_links.extend(submissions)

        next_link = get_next_link(response)

        num_submissions = len(submission_links)
        submissions_gathered += 1
        depth -= 1

    return(submission_links)

def get_post_metadata_from_url(post_url):
    """Return a RedditSubmission object from the post_url."""
    response = get_url(post_url)

def get_submissions_on_page(page_url):
    """Return all submission links from on page_url."""
    response = get_url(page_url)

def get_url(url):
    """Return the response from a url."""
    return main_user.get_url(url)

FAKE_HEADERS = {'User-Agent': UserAgent().google}
TIME_BETWEEN_GETS = 1
