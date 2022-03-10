import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

# grey-scale to ascii


def to_ascii(pxl):
    # def ASCII character list
    ASCII_CHAR = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

    # min max scaling pixel value to find corresponding index of ASCII_CHAR
    idx = int((len(ASCII_CHAR)-1) * pxl / 255.0)

    return ASCII_CHAR[idx]

# display ascii image


def display(img) -> None:
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if j < (img.shape[1] - 1):
                print(img[i, j], end='')
            else:
                print(img[i, j], end='\n')


# load image
path = (input("image path: "))
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
