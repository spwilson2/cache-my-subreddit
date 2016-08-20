import re
import os
from bs4 import BeautifulSoup as _BS
from urllib.request import urlopen, urlretrieve

def BeautifulSoup(*args, **kwargs):
    return _BS(*args, 'html.parser', **kwargs)

class Imgur(object):
    def __init__(self, album_url):
        self._init_link(album_url)
        self._init_images()

    @staticmethod
    def is_imgur_link(url):
        return True if re.search(IMGUR_IMAGE_URL_REGEX, url) else False

    def _init_link(self, url):

        match = re.search(IMGUR_IMAGE_URL_REGEX, url)

        if match:
            self.album_url = 'http://imgur.com/' + match.group('album_id')
        else:
            raise NotAnImgurAlbumException()

    def _init_images(self):

        try:
            response = urlopen(url=self.album_url)
        except Exception:
            self.img_urls = []
            return
            #raise

        # Read in the images now so we can get stats and stuff:
        response_bs = BeautifulSoup(response)
        matches = response_bs.find_all(
                'div',
                id=re.compile('[a-zA-Z0-9]+'),
                class_='post-image-container')

        self.img_urls = [(match['id'], IMGUR_BASE_URL % match['id']) for match in matches]

    @staticmethod
    def test_save_exists(folder_path):

        folder_path = os.path.abspath(folder_path)

        if not os.path.exists(folder_path):
            return False
        return True

    def save_images(self, folder_path, name_prefix=''):

        # If there weren't any images to download fuck off
        if not self.img_urls:
            return

        if name_prefix:
            name_prefix += '-'

        folder_path = os.path.abspath(folder_path)

        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
            except:
                raise

        for count, (id_, image_url) in enumerate(self.img_urls):

            image_path = os.path.join(
                    folder_path, name_prefix + str(count) + '.jpg')

            if os.path.isfile(image_path):
                print("Skipping, already exists.")
            else:
                try:
                    urlretrieve(image_url, image_path)
                except:
                    raise


class NotAnImgurAlbumException(Exception):
    pass

IMGUR_IMAGE_URL_REGEX = r'^https?\:\/\/(www\.)?(?:[mi]\.)?imgur\.com/' +\
                r'((gallery)/)?(?P<album_id>[a-zA-Z0-9/]+)(#[0-9]+)?$'

IMGUR_BASE_URL = 'http://i.imgur.com/%s.jpg'

if __name__ == '__main__':
    Imgur('http://imgur.com/IfcMa5N').save_images('./imgur_album/')
