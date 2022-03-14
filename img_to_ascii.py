from genericpath import isfile
import cv2
from matplotlib.pyplot import text
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io

from pyparsing import col


class image:
    def __init__(self, path, height) -> None:
        """
        Initialize image object.

        Args:
            path: [str]: path to the chosen image
            height: [int]: image height (after resizing)
        """

        # load image
        if not isfile(path):
            raise FileExistsError('Incorrect path or file does not exist')

        if not type(height) == int:
            raise ValueError(
                'Expected type int: got type {}'.format(type(height)))

        self.img = cv2.imread(path)

        r = self.img.shape[0] / self.img[1]  # image size ratio

        # resize image
        self.img = cv2.resize(self.img, dsize=(height, int(height * r)),
                              interpolation=cv2.INTER_NEAREST)

        # grex-scale
        self.img = np.mean(self.img, -1)

    def to_ascii(self) -> None:
        """
        Converts image to ascii art.
        """

        # characters to use
        ASCII_CHAR = "B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
        l = len(ASCII_CHAR)

        self.img_ascii = ''
        for i in range(0, len(self.img.shape[0])):
            self.img_ascii += [
                ASCII_CHAR[int((l - 1) * x / 255)] for x in self.img[i]
            ] + '\n'

    def start(self, fontname='arial.ttf', fontsize=11, height=200) -> None:
        """
        Create first image.

        Args:
            fontname: [str]: font to use for the ascii art (Default: Arial).
            fontsize: [int]: font size.
            height: [int]: height of final image.
        """

        # define Image Font
        font = ImageFont.truetype(fontname, fontsize)

        # get measurements
        testImg = Image.new('RGB', (1, 1))
        testDraw = ImageDraw.Draw(testImg)

        w, h = testDraw.textsize(self.img_ascii, font)

        # create img
        self.Img = Image.new(mode='RGB', size=(w+4, h+4), color=(0, 0, 0))
        d = ImageDraw.Draw(self.Img)
        d.text(xy=(0, 0), text=self.img_ascii,
               fill=(255, 255, 255), align='left')

        # resize
        w, h = self.Img.size
        r = w / h
        self.Img = self.Img.resize((int(height*r), height))

        # save image
        self.Img.save('result.png')


# load image
path = (input("image path: "))

while not(isfile(path)):
    print('\033[91m' + 'The file does not exist!' '\033[0m')
    path = input('Please enter a valid path: ')

img = cv2.imread(path)

# resize
img_ratio = img.shape[0] / img.shape[1]

img = cv2.resize(img, dsize=(48, int(48*img_ratio)),
                 interpolation=cv2.INTER_NEAREST)

# convert to grey-scale
img_grey = np.mean(img, -1)

# convert to ascii
img_ascii = np.zeros_like(img_grey, dtype=object)

for i in range(0, img_ascii.shape[0]):
    for j in range(0, img_ascii.shape[1]):
        img_ascii[i, j] = to_ascii(img_grey[i, j])

img_ascii2 = np.zeros_like(img_grey, dtype=np.dtype('U1'))

for i in range(0, img_ascii2.shape[0]):
    img_ascii2[i] = [
        ASCII_CHAR[int((len(ASCII_CHAR)-1) * x / 255.0)] for x in img_grey[i]]

print(np.all(img_ascii == img_ascii2))
