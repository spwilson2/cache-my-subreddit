import click
import requests
import json
from fake_useragent import UserAgent


@click.group()
def cli():
    pass

@cli.command()
def friend():
    pass

def login():
    login_info = json.loads('\n'.join(list(open('login-config.json'))))
    response = requests.post('https://www.reddit.com/api/login',
            login_info,
        headers= FAKE_HEADERS
        )
    return response.cookies

def list_friends(cookies):
    print(requests.get('https://www.reddit.com/r/friends/', cookies=cookies,
        headers=FAKE_HEADERS).text)

FAKE_HEADERS = {'User-Agent': UserAgent().google}

if __name__ == '__main__':
    cookies = login()
    list_friends(cookies)


