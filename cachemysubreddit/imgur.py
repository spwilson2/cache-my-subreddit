"""
MIT License
Copyright Alex Gisby <alex@solution10.com>
Copyright Sean Wilson <spwilson27@gmail.com>
"""

# Copyright (C) 2016 Sean Wilson
# Copyright (C) 2012 Alex Gisby
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
imguralbum.py - Download a whole imgur album in one go.
Provides both a class and a command line utility in a single script
to download Imgur albums.
MIT License
Copyright Alex Gisby <alex@solution10.com>
"""
import sys
import re
import urllib.request, urllib.parse, urllib.error
import os
import math


class ImgurAlbumException(Exception):
    def __init__(self, msg=False):
        self.msg = msg


class ImgurAlbumDownloader:
    def __init__(self, album_url):
        """
        Constructor. Pass in the album_url that you want to download.
        """
        self.album_url = album_url

        # Callback members:
        self.image_callbacks = []
        self.complete_callbacks = []

        # Check the URL is actually imgur:
        match = re.match("(https?)\:\/\/(www\.)?(?:[mi]\.)?imgur\.com/((gallery)/)?([a-zA-Z0-9/]+)(#[0-9]+)?", album_url)
        if not match:
            raise ImgurAlbumException("URL must be a valid Imgur Album")

        self.protocol = match.group(1)
        self.album_key = match.group(5)

        # Read the no-script version of the page for all the images:
        fullListURL = "http://imgur.com/" + self.album_key

        try:
            self.response = urllib.request.urlopen(url=fullListURL)
            response_code = self.response.getcode()
        except Exception as e:
            self.response = False
            response_code = e.code

        if not self.response or self.response.getcode() != 200:
            raise ImgurAlbumException("Error reading Imgur: Error Code %d" % response_code)

        # Read in the images now so we can get stats and stuff:
        html = self.response.read().decode('utf-8')
        self.imageIDs = re.findall('<div id="([a-zA-Z0-9]+)" class="post-image-container', html)


    def num_images(self):
        """
        Returns the number of images that are present in this album.
        """
        return len(self.imageIDs)


    def album_key(self):
        """
        Returns the key of this album. Helpful if you plan on generating your own
        folder names.
        """
        return self.album_key


    def on_image_download(self, callback):
        """
        Allows you to bind a function that will be called just before an image is
        about to be downloaded. You'll be given the 1-indexed position of the image, it's URL
        and it's destination file in the callback like so:
            my_awesome_callback(1, "http://i.imgur.com/fGWX0.jpg", "~/Downloads/1-fGWX0.jpg")
        """
        self.image_callbacks.append(callback)


    def on_complete(self, callback):
        """
        Allows you to bind onto the end of the process, displaying any lovely messages
        to your users, or carrying on with the rest of the program. Whichever.
        """
        self.complete_callbacks.append(callback)


    def save_images(self, foldername=False):
        """
        Saves the images from the album into a folder given by foldername.
        If no foldername is given, it'll use the cwd and the album key.
        And if the folder doesn't exist, it'll try and create it.
        """
        # Try and create the album folder:
        if foldername:
            albumFolder = foldername
        else:
            albumFolder = self.album_key

        if not os.path.exists(albumFolder):
            os.makedirs(albumFolder)

        # And finally loop through and save the images:
        for (counter, image) in enumerate(self.imageIDs, start=1):
            image_url = "http://i.imgur.com/"+image+".jpg"

            prefix = "%0*d-" % (
                int(math.ceil(math.log(len(self.imageIDs) + 1, 10))),
                counter
            )
            path = os.path.join(albumFolder, prefix + image + ".jpg")

            # Run the callbacks:
            for fn in self.image_callbacks:
                fn(counter, image_url, path)

            # Actually download the thing
            if os.path.isfile(path):
                print ("Skipping, already exists.")
            else:
                try:
                    urllib.request.urlretrieve(image_url, path)
                except:
                    print ("Download failed.")

        # Run the complete callbacks:
        for fn in self.complete_callbacks:
            fn()
