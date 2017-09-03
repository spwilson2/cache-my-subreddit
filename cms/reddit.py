import praw
import prawcore
import praw.exceptions

USER_AGENT='sheenrocks\' user agent'

class Reddit(object):

    def __init__(self, username=None, password=None, client_id=None, client_secret=None):
        """Log in to reddit using the given credentials."""
        self._username = username
        self._password = password
        self._client_id = client_id
        self._client_secret = client_secret
        self._authenticate()

    def _authenticate(self):
        self._reddit = praw.Reddit(user_agent=USER_AGENT,
                             client_id=self._client_id,
                             client_secret=self._client_secret,
                             username=self._username,
                             password=self._password)

    def list_friends(self):
        friends = self._reddit.user.friends()
        friends.limit = 100000
        for friend in friends:
            yield friend.name

    def subreddit_submissions(self, subreddit, limit=10):
        submissions = self._reddit.subreddit(subreddit).hot()
        submissions.limit = limit
        for submission in submissions:
            yield Post(submission)

    def user_submissions(self, user, limit=1000):
        try:
            submissions = self._reddit.redditor(user).submissions.new()
            submissions.limit = limit
            for submission in submissions:
                yield Post.wrap(submission)
        except prawcore.exceptions.Forbidden:
            print('Unable to get user_submissions, were they banned?')

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
