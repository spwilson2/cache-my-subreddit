import requests
import re
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

class RedditUser(object):

    def __init__(self):
        pass

    def login(self, user, passwd):
        response = requests.post(
                'https://www.reddit.com/api/login',
                {'user': user, 'passwd': passwd},
                headers = FAKE_HEADERS
                )
        self.cookies = response.cookies

    def list_friends(self):
        response = requests.get(
                'https://www.reddit.com/prefs/friends/',
            cookies=self.cookies,
            headers=FAKE_HEADERS
        )

        friends_bsobj = BeautifulSoup(response.text)

        friend_anchors = friends_bsobj.find('table').find_all('a',
              href=re.compile('^https://www.reddit.com/user/[^/]*/$'))

        return [anchor.text for anchor in friend_anchors]

FAKE_HEADERS = {'User-Agent': UserAgent().google}

if __name__ == '__main__':
    import json
    user = RedditUser()
    credentials = json.loads(open('login-config.json').read())
    user.login(**credentials)
    user.list_friends()
