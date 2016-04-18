import requests
from time import sleep
import re
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

class RedditUser(object):

    def __init__(self):
        pass

    def login(self, user, passwd):
        """Log in to reddit using the given credentials."""
        response = requests.post(
                'https://www.reddit.com/api/login',
                {'user': user, 'passwd': passwd},
                headers = FAKE_HEADERS
                )
        self.cookies = response.cookies

    def list_friends(self):
        """Return a list of friend's usernames."""
        response = requests.get(
                'https://www.reddit.com/prefs/friends/',
            cookies=self.cookies,
            headers=FAKE_HEADERS
        )

        friends_bsobj = BeautifulSoup(response.text)

        #print(friends_bsobj.find('table'))
        assert(friends_bsobj.find('table'))

        friend_anchors = friends_bsobj.find('table').find_all('a',
              href=re.compile('^https://www.reddit.com/user/[^/]*/$'))

        return [anchor.text for anchor in friend_anchors]

class RedditSubmission(object):
    def __init__(self, title, user, post_url, link_url):
        self.title = title
        self.user = user
        self.post_url = post_url
        self.link_url = link_url


def get_user_submissions(username):
    """Return a list of all urls to submitted content from the user."""

    submitted_url = 'https://www.reddit.com/user/%s/submitted/' % (username)

    return _get_submissions_from_url(submitted_url)



def get_top_posts_from_subreddit(subreddit):
    subreddit_url = 'https://www.reddit.com/r/%s/top/' % (subreddit)

    return _get_submissions_from_url(subreddit_url, depth=0)


def _get_submissions_from_url(url, depth=500):

    def get_next_link(response):
        possible_link = BeautifulSoup(response.text).find(
                'a',
                rel='nofollow next')

        if possible_link is not None:
            return possible_link['href']

    def get_submission_links_and_titles(submission_html):
        bs_obj = BeautifulSoup(submission_html)
        anchors = bs_obj.find_all('a', class_="title may-blank ")

        if anchors:
            return ((anchor.text, anchor['href']) for anchor in anchors)

    response = requests.get(
            url,
            headers = FAKE_HEADERS
            )

    submission_links = []

    submissions = get_submissions(response.text)

    get_post_metadata(response.text)

    if submissions is not None:
        submission_links.extend(submissions)

    # Traverse all the user's submitted pages.
    next_link = get_next_link(response)
    while next_link and depth > 0:
        sleep(TIME_BETWEEN_GETS)

        response = requests.get(
                next_link,
                headers=FAKE_HEADERS
                )

        submissions = get_submission_links_and_titles(response.text)

        if submissions:
            submission_links.extend(submissions)
        next_link = get_next_link(response)
        --depth

    return(submission_links)

def get_post_metadata(post_url):
    """Return a RedditSubmission object from the post_url."""
    response = requests.get(
            post_url,
            headers = FAKE_HEADERS
            )

def get_submissions_on_page(page_url):
    """Return all submission links from on page_url."""
    response = requests.get(
            page_url,
            headers = FAKE_HEADERS
            )




FAKE_HEADERS = {'User-Agent': UserAgent().google}
TIME_BETWEEN_GETS = 1
