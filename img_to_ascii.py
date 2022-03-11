from genericpath import isfile
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import io

from pyparsing import col


def to_ascii(pxl):
    """
    transform a pixel to a ascii character
    """

    # def ASCII character list
    ASCII_CHAR = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

    # min max scaling pixel value to find corresponding index of ASCII_CHAR
    idx = int((len(ASCII_CHAR)-1) * pxl / 255.0)

    return ASCII_CHAR[idx]


def getSize(txt, font):
    """
    Get the size of the text to print
    """
    testImg = Image.new('RGB', (1, 1))
    testDraw = ImageDraw.Draw(testImg)
    return testDraw.textsize(txt, font)


def display(img) -> None:
    """
    display ascii image
    """

    # join all rows
    img_str = np.apply_along_axis(
        func1d=lambda x: "".join(list(x)),
        axis=1, arr=img
    )

    # add newline at end of each row
    img_str = "\n".join(list(img_str))

    # display as image
    fontname = 'arial.ttf'
    fontsize = 11
    font = ImageFont.truetype(fontname, fontsize)

    w, h = getSize(img_str, font)

    Img = Image.new('RGB', (w+4, h+4), color=(0, 0, 0))
    d = ImageDraw.Draw(Img)
    d.text((0, 0), img_str, fill=(255, 0, 0), align='left')

    w, h = Img.size
    r = h / w
    Img = Img.resize((int(200*r), 200))

    Img.save('result2.jpg')


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

display(img_ascii)
