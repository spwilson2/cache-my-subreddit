import tempfile
import shutil
import os
from time import sleep

from unittest import TestCase

from cachemysubreddit.imgur import ImgurAlbumDownloader

NORMAL_URL = 'http://imgur.com/ZNovyuz'
GALLERY_URL = 'http://imgur.com/gallery/F3ogc'
A_URL = 'http://imgur.com/a/H8rJQ'
I_URL = 'http://i.imgur.com/8HGZoqy.jpg'

class TestJoke(TestCase):

    def setUp(self):
        self.tempdirs = []


    def tearDown(self):
        for directory in self.tempdirs:
            shutil.rmtree(directory)
        sleep(1)  # Be nice to imgur

    def setup_download(self):
        tempdir = tempfile.mkdtemp(suffix='')
        self.tempdirs.append(tempdir)
        return tempdir

    def download_image_and_return_files(self, dir_, url):
        imgur_obj = ImgurAlbumDownloader(url)
        imgur_obj.save_images(foldername=dir_)
        files = os.listdir(path=dir_)

        return files

    def test_num_images_function_for_normal_url(self):
        self.assertEqual(ImgurAlbumDownloader(NORMAL_URL).num_images(), 1)

    def test_num_images_function_for_a_url(self):
        self.assertEqual(ImgurAlbumDownloader(A_URL).num_images(), 7)

    def test_num_images_function_for_gallery_url(self):
        self.assertEqual(ImgurAlbumDownloader(GALLERY_URL).num_images(), 1)

    def test_num_images_function_for_i_url(self):
        self.assertEqual(ImgurAlbumDownloader(I_URL).num_images(), 1)

    def test_normal_url(self):
        imgur_obj = ImgurAlbumDownloader(NORMAL_URL)
        self.assertIsInstance(imgur_obj, ImgurAlbumDownloader)

    def test_gallery_url(self):
        imgur_obj = ImgurAlbumDownloader(GALLERY_URL)
        self.assertIsInstance(imgur_obj, ImgurAlbumDownloader)

    def test_i_url(self):
        imgur_obj = ImgurAlbumDownloader(I_URL)
        self.assertIsInstance(imgur_obj, ImgurAlbumDownloader)

    def test_a_url(self):
        imgur_obj = ImgurAlbumDownloader(A_URL)
        self.assertIsInstance(imgur_obj, ImgurAlbumDownloader)

    def test_download_of_normal_url_images(self):
        tempdir = self.setup_download()
        url = NORMAL_URL

        files = self.download_image_and_return_files(tempdir, url)
        num_files = ImgurAlbumDownloader(url).num_images()

        self.assertEqual(len(files), num_files)

        for file_ in files:
            self.assertRegex(file_, '^.*[.]{1}jpg$')

    def test_download_of_i_url_images(self):
        tempdir = self.setup_download()
        url = I_URL

        files = self.download_image_and_return_files(tempdir, url)
        num_files = ImgurAlbumDownloader(url).num_images()

        self.assertEqual(len(files), num_files)

        for file_ in files:
            self.assertRegex(file_, '^.*[.]{1}jpg$')

    def test_download_of_gallery_url_images(self):
        tempdir = self.setup_download()
        url = GALLERY_URL

        files = self.download_image_and_return_files(tempdir, url)
        num_files = ImgurAlbumDownloader(url).num_images()

        self.assertEqual(len(files), num_files)

        for file_ in files:
            self.assertRegex(file_, '^.*[.]{1}jpg$')

    def test_download_of_a_url_images(self):
        tempdir = self.setup_download()
        url = A_URL

        files = self.download_image_and_return_files(tempdir, url)
        num_files = ImgurAlbumDownloader(url).num_images()

        self.assertEqual(len(files), num_files)

        for file_ in files:
            self.assertRegex(file_, '^.*[.]{1}jpg$')
