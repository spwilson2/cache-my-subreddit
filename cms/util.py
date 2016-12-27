from bs4 import BeautifulSoup as _B
from fake_useragent import UserAgent

_FAKE_HEADERS = {'User-Agent': UserAgent().google}

def BeautifulSoup(*args, **kwargs):
    parser = 'lxml'
    return _B(args[0], parser, **kwargs)

class UnsupportedLinkException(Exception):
    pass

class BadPathException(Exception):
    pass
