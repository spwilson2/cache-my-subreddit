import re
import os
from urllib.request import urlopen, urlretrieve


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
            print(url)
            self.album_url = 'http://imgur.com/' + match.group('album_id')
        else:
            raise NotAnImgurAlbumException()

    def _init_images(self):

        try:
            response = urlopen(url=self.album_url)
        except Exception:
            print(self.album_url)
            self.img_urls = []
            return
            #raise

        # Read in the images now so we can get stats and stuff:
        html = response.read().decode('utf-8')
        matches = re.findall('<div id="(?P<id>[a-zA-Z0-9]+)"' +
                             'class="post-image-container', html)

        self.img_urls = [(match, IMGUR_BASE_URL % match) for match in matches]

    def save_images(self, folder_path, name_prefix=''):

        if name_prefix:
            name_prefix += '-'

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
