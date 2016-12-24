import requests
import time
import re

import praw

from cms.util import BeautifulSoup, _FAKE_HEADERS

SUBMITTED_FMT = 'https://www.reddit.com/user/%s/submitted/'
SUBREDDIT_FMT = 'https://www.reddit.com/r/%s/'
USER_AGENT='sheenrocks\' user agent'
RATE_LIMIT = 1

class Reddit(object):

    def __init__(self, username=None, password=None, client_id=None, client_secret=None):
        """Log in to reddit using the given credentials."""
        self._username = username
        self._password = password
        self._client_id = client_id
        self._client_secret = client_secret
        self._cookies=None
        self._authenticate()

        # Allow us to request instantly after setup.
        self._last_request = time.time() - RATE_LIMIT

    def _authenticate(self):

        response = requests.post(
                'https://www.reddit.com/api/login',
                {'user': self._username, 'passwd': self._password},
                headers = _FAKE_HEADERS
                )

        self._cookies = response.cookies

        self._reddit = praw.Reddit(user_agent=USER_AGENT,
                             client_id=self._client_id,
                             client_secret=self._client_secret,
                             username=self._username,
                             password=self._password)

    def _get_url(self, url):
        """Return the response from getting the url as the signed in user."""
        # Rate-limit by sleeping if we need to.
        time_left = self._last_request + RATE_LIMIT - time.time()
        if time_left > 0:
            print('Rate limiting; sleeping for %ss.' % time_left)
            time.sleep(time_left)

        self._last_request = time.time()
        print('GETting: ', str(url))
        return requests.get(
            url,
            cookies=self._cookies,
            headers=_FAKE_HEADERS
        )

    def list_friends(self):
        friends = self._reddit.user.friends()
        friends.limit = 1000
        for friend in friends:
            yield friend.name

    def _submissions(self, url, limit=10000):
        next_submitted_url = url
        while next_submitted_url:
            submissions_html = self._get_url(next_submitted_url).text
            bs_obj = BeautifulSoup(submissions_html)
            submissions = _get_metadata(bs_obj)
            for submission in submissions:
                yield submission
            next_submitted_url = _get_next_link(bs_obj)

    def subreddit_submissions(self, subreddit, limit=10):
        listings = self._reddit.subreddit(subreddit).hot()
        listings.limit = limit
        count = 0
        for listing in listings:
            count += 1
            if count > limit:
                return
            yield Post.wrap(listing)

    def user_submissions(self, user, limit=10000):
        count = 0
        submissions = self._submissions(SUBMITTED_FMT % user)
        for submission in submissions:
            count += 1
            if count > limit:
                return
            yield submission

class Post(object):
    def __init__(self, title, author, url, shortlink, subreddit):
        self.title = title
        self.author = author
        self.url = url
        self.shortlink = shortlink
        self.subreddit = subreddit

    @staticmethod
    def wrap(post):
        return Post(post.title, post.author.name, post.url, post.shortlink, post.subreddit.display_name)


def _get_next_link(bs_obj):
    possible_link = bs_obj.find('a', rel='nofollow next')
    if possible_link is not None:
        return possible_link['href']


def _get_metadata(bs_obj):
    title_link_url_anchors = None


    user_anchors = bs_obj.find_all('a', class_="author friend may-blank")
    subreddit_anchors = bs_obj.find_all('a', class_="subreddit hover may-blank")
    post_url_anchors = bs_obj.find_all('a', class_="bylink comments may-blank")
    title_link_url_anchors = bs_obj.find_all('a', class_="title may-blank outbound")
    if not title_link_url_anchors:
        title_link_url_anchors = bs_obj.find_all('a', class_="title may-blank loggedin outbound")

    # (title, url) generator
    titles_links = ((anchor.text, anchor['href']) for anchor in title_link_url_anchors)
    post_urls = (anchor.text for anchor in post_url_anchors)
    subreddits = (anchor.text[3:].replace('/','') for anchor in subreddit_anchors)
    users = (anchor.text for anchor in user_anchors)

    metadata_list = []

    for submission in zip(titles_links, post_urls, subreddits, users):
        (title, link_url), post_url, post_subreddit, user = submission
        metadata_list.append(Post(title, user, link_url, post_url, post_subreddit))

    #subreddit:
    #   <a href="https://www.reddit.com/r/GoneMild/" class="subreddit hover may-blank">/r/GoneMild</a>

    #post_url:
    #   <a href="/r/GoneMild/comments/5jn5ao/about_to_work_out/" data-inbound-url="/r/GoneMild/comments/5jn5ao/about_to_work_out/?utm_content=comments&amp;utm_medium=user&amp;utm_source=reddit&amp;utm_name=frontpage" data-href-url="/r/GoneMild/comments/5jn5ao/about_to_work_out/" data-event-action="comments" class="bylink comments may-blank" rel="nofollow">7 comments</a>

    #link_url:
    #   <a class="title may-blank loggedin outbound" data-event-action="title" href="http://i.imgur.com/fnXnhfK.jpg" tabindex="1" data-href-url="http://i.imgur.com/fnXnhfK.jpg" data-outbound-url="https://out.reddit.com/t3_5jn5ao?url=http%3A%2F%2Fi.imgur.com%2FfnXnhfK.jpg&amp;token=AQAAq-ZdWMcR1gXU5EWru4O3HuYimaam0xNWwa2a_pGd08Drf1wN&amp;app_name=reddit.com" data-outbound-expiration="1482548907000" rel="">About to work out :)</a>
    return metadata_list

if __name__ == '__main__':
    val = requests.get('https://www.reddit.com/r/AskReddit/').text
    bs_obj = BeautifulSoup(val)
    res = bs_obj.find_all('a', class_="title")
