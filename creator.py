"""Get from URL the json thingie and download the pictures.
"""

import urllib
import json
import os
import Image
from random import shuffle

URL = "http://api.tumblr.com/v2/blog/i-like-breasts.tumblr.com/posts?api_key=suF4S0cT8bmYYE86p4wO7PRerBA1J33aFGfeVcVcyEGktDVVKh"

class Wallpaper(object):
    """A wallpaper can create itself and set itself."""

    def __init__(self, resolution=(1366, 768), columns=5, margin=10, url=URL, bg_color=(0,0,0)):
        self.resolution = resolution
        self.url = url
        self.columns = columns
        self.width = (resolution[0] - (columns+1)*margin)/columns
        self.margin = margin
        self.images = self.download_images()
        shuffle(self.images)
        self.bg_color = bg_color

    def _wsize(self, img, w):
        """Get the new size of img so that it has width == w keeping aspect ratio."""
        return (w, int(img.getbbox()[3] * float(w)/img.getbbox()[2]))

    def _wsized_image(self, img, w):
        """Resize so that width == w keeping aspect ratio."""
        return img.resize(self._wsize(img,w))

    def download_images(self):
        """Download the images."""
        picture_urls = self.image_links()
        ret = []

        print "Total pictures %d" % len(picture_urls)
        for i,pl in enumerate(picture_urls):
            print "%d: %s" % (i, pl)
            fname = "images/" + os.path.basename(pl)

            if not os.path.exists(fname):
                urllib.urlretrieve(pl, fname)

            ret.append(self._wsized_image(Image.open(fname), self.width))

        return ret

    def image_links(self):
        """Get image links from url"""
        response = urllib.urlopen(self.url)
        json_data = response.read()

        dict_data = json.loads(json_data)
        pics = [i['photos'] for i in dict_data['response']['posts']]
        return [pic[0]['original_size']['url'] for pic in pics]

    def height(self, img):
        return img.getbbox()[3]

    def image(self):
        (width, height) = self.resolution
        ret = Image.new("RGB", self.resolution, self.bg_color)

        for c in range(self.columns):
            wcursor = (self.width + self.margin) * c + self.margin
            cwidth = self.margin
            tmp_stack = []
            while cwidth + self.height(self.images[-1]) + self.margin < height:
                cwidth += self.height(self.images[-1]) + self.margin
                tmp_stack.append(self.images.pop())

            hcursor = (height - cwidth)/2
            print "Column %d: ( %d - %d )/2 + %d = %d" % (c, height, cwidth, self.margin, hcursor)

            for img in tmp_stack:
                ret.paste(img, (wcursor, hcursor))
                hcursor += self.margin + self.height(img)

        return ret


if __name__ == "__main__":
    w = Wallpaper()
    w.image().show()
