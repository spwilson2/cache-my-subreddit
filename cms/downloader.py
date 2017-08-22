import re
import os

import requests

from cms.util import UnsupportedLinkException, BadPathException, BeautifulSoup

IMGUR_IMAGE_URL_REGEX = (r'^https?\:\/\/(www\.)?(?:[mi]\.)?imgur\.com\/'
                         '((gallery)\/)?(?P<album_id>[a-zA-Z0-9/]+)'
                         '(#[0-9]+)?$')
BASE_IMGUR_URL_REGEX = r'^https?\:\/\/(www\.)?(?:[mi]\.)?imgur\.com\/'

GFYCAT_URL_REGEX = r'^https?\:\/\/(www\.)?gfycat\.com/[a-zA-Z0-9]+$'

IREDDIT_URL_REGEX = r'^https?\:\/\/(www\.)?i\.redd\.it/[a-zA-Z0-9.]+$'

EROSHARE_URL_REGEX = r'^https?\:\/\/(www\.)?eroshare\.com/[a-zA-Z0-9#]+$'
EROSHARE_ID_REGEX = re.compile(r'player-(?P<id>\w+)')
EROSHARE_FMT_URL = 'https://v.eroshare.com/%s.mp4'

GLOB_ALL = re.compile('.?')

class DownloaderBase(object):
    def __init__(self, album_url):
        # Get album actual url
        self._init_link(album_url)
        self._initialized = False

    @classmethod
    def is_link(cls, url):
        return True if re.search(cls.url_regex, url) else False

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
            file_ext = self.file_ext_from_url(image_url) if ext is None else ext

            dl_path = os.path.join(folder, pfx+sfx+count+file_ext)

            if os.path.exists(dl_path):
                # We explicitily print instead of raise.
                print(BadPathException('%s already exists.' % dl_path))
            else:
                _download(image_url, dl_path)

        return count

class Gfycat(DownloaderBase):
    url_regex = GFYCAT_URL_REGEX
    def __init__(self, album_url):
        DownloaderBase.__init__(self, album_url)

    def _init_link(self, url):
        match = re.search(Gfycat.url_regex, url)
        if match:
            self.album_url = url
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
        match = response_bs.find(id='share-video')
        if match is None:
            print("Didn't find:", str(self.album_url))
            self.img_urls = []
            return

        match = match.find('source', type=re.compile('type/(mp4)|(webm)|(jpg)'))
        if match:
            self.img_urls = [(os.path.basename(match['src']), match['src'])]

        self._initialized = True

class Imgur(DownloaderBase):
    url_regex = BASE_IMGUR_URL_REGEX
    def __init__(self, album_url):
        # Get album actual url
        self._initialized = False
        self._init_link(album_url)

    def _init_link(self, url):
        # First check with a more specific regex, the album regex
        match = re.search(IMGUR_IMAGE_URL_REGEX, url)
        if match:
            self.album_url = 'http://imgur.com/' + match.group('album_id')
        else:
            # Otherwise check with a single item regex.
            match = re.search(self.url_regex, url)
            if match:
                self.album_url = url
                self.img_urls = ((os.path.basename(url), url),)
                self._initialized = True
                print('That match')
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
        #print(response.text)
        print(self.album_url)
        response_bs = BeautifulSoup(response.text)
        matches = response_bs.find_all(
                'div',
                id=re.compile('[a-zA-Z0-9]+'),
                class_='post-image-container')

        # Get the src tag from each post-image-container.
        self.img_urls = []
        for match in matches:
            source = match.find(src=GLOB_ALL)
            if source:
                source = source.get('src')
                if source:
                    self.img_urls.append((match['id'], 'http://' + source.lstrip('/')))

        self._initialized = True

class IReddit(DownloaderBase):
    url_regex = IREDDIT_URL_REGEX

    def __init__(self, album_url):
        # Make sure that the url is a match.
        self._init_link(album_url)
        self._initialized = True

    def _init_link(self, url):
        match = re.search(IReddit.url_regex, url)
        if match:
            self.album_url = url
            self.img_urls = ((os.path.basename(url), url),)
        else:
            raise UnsupportedLinkException()

class EroShare(DownloaderBase):
    url_regex = EROSHARE_URL_REGEX

    def __init__(self, album_url):
        # Get album actual url
        self._init_link(album_url)
        self._initialized = False

    def _init_link(self, url):
        match = re.search(EroShare.url_regex, url)
        if match:
            self.album_url = url
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
        match = response_bs.find('video')
        self.img_urls = None
        if match:
            id_ = EROSHARE_ID_REGEX.search(match['id']).groupdict()['id']
            self.img_urls = [(id_, EROSHARE_FMT_URL % id_)]

        self._initialized = True


class UniversalDownloader(object):
    def __init__(self, album_url):
        self.downloader = None
        for downloader in [Imgur, Gfycat, EroShare, IReddit]:
            if downloader.is_link(album_url):
                self.downloader = downloader(album_url)
                return


def _download(url, path):
    r = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

if __name__ == '__main__':
    #url = 'https://eroshare.com/pibgaw80#'
    url = 'https://i.imgur.com/DcggnoL.jpg'
    savedir = 'output'
    downloader = UniversalDownloader(url).downloader
    regex = re.compile(IMGUR_IMAGE_URL_REGEX)
    print(regex.search(url))
    print(downloader)
    if downloader:
        if not os.path.exists(savedir):
            os.makedirs(savedir)
        downloader.save(savedir, pfx='Post')
