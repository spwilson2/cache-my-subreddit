import re
import os

import requests

from cms.util import UnsupportedLinkException, BadPathException, BeautifulSoup

IMGUR_IMAGE_URL_REGEX = r'^https?\:\/\/(www\.)?(?:[mi]\.)?imgur\.com/' +\
                r'((gallery)/)?(?P<album_id>[a-zA-Z0-9/]+)(#[0-9]+)?$'
IMGUR_FMT_URL = 'http://i.imgur.com/%s.jpg'

class Imgur(object):
    def __init__(self, album_url):
        # Get album actual url
        self._init_link(album_url)
        self._initialized = False

    @staticmethod
    def is_link(url):
        return True if re.search(IMGUR_IMAGE_URL_REGEX, url) else False

    def _init_link(self, url):
        match = re.search(IMGUR_IMAGE_URL_REGEX, url)
        if match:
            self.album_url = 'http://imgur.com/' + match.group('album_id')
        else:
            raise UnsupportedLinkException()

    def _init_images(self):
        try:
            response = requests.get(self.album_url)
        except Exception:
            print("Didn't find:", str(self.album_url))
            self.img_urls = []
            return

        # Read in the images now so we can get stats and stuff:
        response_bs = BeautifulSoup(response.text)
        matches = response_bs.find_all(
                'div',
                id=re.compile('[a-zA-Z0-9]+'),
                class_='post-image-container')

        self.img_urls = [(match['id'], IMGUR_FMT_URL % match['id']) for match in matches]

        self._initialized = True

    @staticmethod
    def file_ext_from_url(url):
        return os.path.splitext(url)[1]

    def save(self, folder, pfx='', sfx='', ext=None):

        if not self._initialized:
            self._init_images()

        # If there weren't any images to download, return
        if not self.img_urls:
            return 0

        folder= os.path.abspath(folder)

        if not os.path.isdir(folder):
            raise BadPathException('%s is not a folder.' % folder)

        for count, (id_, image_url) in enumerate(self.img_urls):

            count = '-'+str(count) if count else ''
            file_ext = Imgur.file_ext_from_url(image_url) if ext is None else ext

            dl_path = os.path.join(folder, pfx+sfx+count+file_ext)

            if os.path.exists(dl_path):
                raise BadPathException('%s already exists.' % dl_path)
            else:
                _download(image_url, dl_path)

        return count

def _download(url, path):
    r = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)


if __name__ == '__main__':
    folder = './imgur_album/'
    if not os.path.isdir(folder):
        os.mkdir(folder)
    Imgur('http://imgur.com/IfcMa5N').save_images(folder, pfx='CoolBeans')
