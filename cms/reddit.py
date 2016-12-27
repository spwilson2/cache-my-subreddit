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

    def _submissions(self, url, user=None):
        next_submitted_url = url
        while next_submitted_url:
            submissions_html = self._get_url(next_submitted_url).text
            bs_obj = BeautifulSoup(submissions_html)
            submissions = _get_metadata(bs_obj, user)
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
        submissions = self._submissions(SUBMITTED_FMT % user, user)
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

class _ClassParser(object):
    RE_EXTENDER = '(?P<%s>%s)'
    class _ClassParserRegex(object):

        def __init__(self, class_regex, callback):
            self.class_regex = class_regex
            self.compiled_regex = re.compile(class_regex)
            self.callback = callback

        def do_if_match(self, bs_match):
            if self._compiled_regex.search(bs_match.class_):
                return self.callback(bs_match)

    def __init__(self, bs_obj):
        self.bs_obj = bs_obj
        self.regex = ''
        self.compiled_re = None

        self.parsers = {}
        self.parsers_counter = 0

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        vals = []
        for _ in range(len(self.parsers)):
            vals.append(self.bs_parse())
        if len(vals) != len(self.parsers):
            raise StopIteration
        else:
            return vals

    def bs_parse(self):
        match = str(self.bs_obj.find_next('a', self.regex))
        re_match = self.compiled_re.search(match)
        if re_match:
            print(re_match)
            print(re_match.groupdict())
            return re_self.parsers[re_match.groupdict().keys()[0]].do_if_match(match)

    def compile(self):
        self.compiled_re = re.compile(self.regex)

    def add(self, class_regex, callback, name):
        self.parsers[name] = class_regex
        self.regex += _ClassParser.RE_EXTENDER % (name, class_regex)


def _get_metadata(bs_obj, user=None):
    title_link_url_anchors = None

    class_parser = _ClassParser(bs_obj)

    subreddit_parser = class_parser.add("subreddit hover may-blank",
            lambda bs_match: anchor.text[3:].replace('/',''),
            name='subreddit')

    post_parser = class_parser.add("bylink comments may-blank",
            lambda bs_match: bs_match.text,
            name='name')

    title_link_parser = class_parser.add("title may-blank outbound",
            lambda bs_match: (bs_match.text, bs_match['href']),
            name='title_link')

    if user is None:
        user_anchors_parser = class_parser.add("title may-blank outbound",
                lambda bs_match: bs_match.text,
                name='user')

    class_parser.compile()

    #if user is None:
    #    user_anchors = bs_obj.find_all('a', class_="author friend may-blank")

    for submission in class_parser:
        print(submission)
        yield submission

    #subreddit_anchors = bs_obj.find_all('a', class_="subreddit hover may-blank")
    #subreddits = (anchor.text[3:].replace('/','') for anchor in subreddit_anchors)

    #post_url_anchors = bs_obj.find_all('a', class_="bylink comments may-blank")
    #post_urls = [anchor.text for anchor in post_url_anchors]

    #title_link_url_anchors = bs_obj.find_all('a', class_="title may-blank outbound")
    #if not title_link_url_anchors:
    #    title_link_url_anchors = bs_obj.find_all('a', class_="title may-blank loggedin outbound")

    # (title, url) generator
    #titles_links = ((anchor.text, anchor['href']) for anchor in title_link_url_anchors)
    #if user is None:
    #    users = (anchor.text for anchor in user_anchors)
    #else:
    #    users = (user for _ in post_urls)

    #for submission in zip(titles_links, post_urls, subreddits, users):
    #    (title, link_url), post_url, post_subreddit, user = submission
    #    yield Post(title, user, link_url, post_url, post_subreddit)

    #subreddit:
    #   <a href="https://www.reddit.com/r/GoneMild/" class="subreddit hover may-blank">/r/GoneMild</a>

    #post_url:
    #   <a href="/r/GoneMild/comments/5jn5ao/about_to_work_out/" data-inbound-url="/r/GoneMild/comments/5jn5ao/about_to_work_out/?utm_content=comments&amp;utm_medium=user&amp;utm_source=reddit&amp;utm_name=frontpage" data-href-url="/r/GoneMild/comments/5jn5ao/about_to_work_out/" data-event-action="comments" class="bylink comments may-blank" rel="nofollow">7 comments</a>

    #link_url:
    #   <a class="title may-blank loggedin outbound" data-event-action="title" href="http://i.imgur.com/fnXnhfK.jpg" tabindex="1" data-href-url="http://i.imgur.com/fnXnhfK.jpg" data-outbound-url="https://out.reddit.com/t3_5jn5ao?url=http%3A%2F%2Fi.imgur.com%2FfnXnhfK.jpg&amp;token=AQAAq-ZdWMcR1gXU5EWru4O3HuYimaam0xNWwa2a_pGd08Drf1wN&amp;app_name=reddit.com" data-outbound-expiration="1482548907000" rel="">About to work out :)</a>

if __name__ == '__main__':
    val = requests.get('https://www.reddit.com/r/AskReddit/').text
    bs_obj = BeautifulSoup(val)
    res = bs_obj.find_all('a', class_="title")
