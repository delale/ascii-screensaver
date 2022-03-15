import ctypes
import time
import tkinter as tk

import cv2
from genericpath import isfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import pygame


class image:
    def __init__(self, path, height=128, color_palette=None) -> None:
        """
        Initialize image object.

        Args:
            path: [str]: path to the chosen image.
            height: [int]: image height after resizing (Default=48).
            color_palette: [list]: list of colors to use in RGB values tuples (Default=None).
        """

        # input args checking
        if not isfile(path):
            raise FileExistsError('Incorrect path or file does not exist')

        if not type(height) is int:
            raise ValueError(
                'Expected type int: got type {}'.format(type(height)))

        # load image
        self.img = cv2.imread(path)

        # grey-scale
        self.img = np.mean(self.img, -1)

        r = self.img.shape[0] / self.img.shape[1]  # image size ratio

        # resize image
        self.img = cv2.resize(self.img, dsize=(height, int(height * r)+1),
                              interpolation=cv2.INTER_NEAREST)

        # define color palette
        if color_palette is None:
            self.color_palette = [
                (np.random.randint(0, 255), np.random.randint(
                    0, 255), np.random.randint(0, 255))
                for i in range(10)]
        else:
            self.color_palette = color_palette

    def to_ascii(self) -> None:
        """
        Converts image to ascii art.
        """

        # characters to use
        ASCII_CHAR = "B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
        l = len(ASCII_CHAR)

        self.img_ascii = ''
        for i in range(0, self.img.shape[0]):
            self.img_ascii += "".join([
                ASCII_CHAR[int((l - 1) * x / 255)] for x in self.img[i]
            ]) + '\n'

    def start(self, fontname='/Windows/Fonts/cour.ttf', fontsize=11, height=500):
        """
        Create first image.

        Args:
            fontname: [str]: font to use for the ascii art (Default: Arial).
            fontsize: [int]: font size.
            height: [int]: height of final image (Default=350).

        Returns:
            PyGame image to animate.
        """

        self.height = height

        # define Image Font
        font = ImageFont.truetype(fontname, fontsize)

        # get measurements
        testImg = Image.new('RGB', (1, 1))
        testDraw = ImageDraw.Draw(testImg)

        self.w, self.h = testDraw.textsize(self.img_ascii, font)

        # create img
        self.Img = Image.new(mode='RGB', size=(
            self.w+4, self.h+4), color=(0, 0, 0))
        d = ImageDraw.Draw(self.Img)
        d.text(xy=(0, 0), text=self.img_ascii,
               fill=self.color_palette[0], align='left')

        # resize
        w, h = self.Img.size
        self.r = w / h
        self.Img = self.Img.resize((self.height, int(self.height*self.r)+1))

        # save image
        self.Img.save('result.png')

        # counter for color palette list
        self.i = 1

        # load in pygame
        return pygame.image.load('result.png')

    def update(self):
        """
        Update image.

        Returns:
            PyGame image.
        """

        if self.i == len(self.color_palette):
            self.i = 0

        # update image
        self.Img = Image.new(mode='RGB', size=(
            self.w+4, self.h+4), color=(0, 0, 0))
        d = ImageDraw.Draw(self.Img)
        d.text(xy=(0, 0), text=self.img_ascii,
               fill=self.color_palette[self.i], align='left')

        self.Img = self.Img.resize((self.height, int(self.height*self.r)+1))

        self.i += 1

        # save image
        self.Img.save('result.png')

        return pygame.image.load('result.png')


def get_display_size():
    try:  # Windows 8.1 and later
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception as e:
        pass
    try:  # Before Windows 8.1
        ctypes.windll.user32.SetProcessDPIAware()
    except:  # Windows 8 or before
        pass

    root = tk.Tk()
    root.update_idletasks()
    root.attributes('-fullscreen', True)
    root.state('iconic')
    height = root.winfo_screenheight()
    width = root.winfo_screenwidth()
    root.destroy()

    return height, width


def main(img_path):

    # image class
    Img = image(
        path=img_path
    )
    Img.to_ascii()
    img = Img.start()

    # initialize pygame
    pygame.init()

    # params
    screenHeight, screenWidth = get_display_size()
    bgColor = (0, 0, 0)
    speed = [
        np.random.uniform(1.75, 2.25),
        np.random.uniform(1.75, 2.25)
    ]

    # initialize screen
    screen = pygame.display.set_mode((screenWidth, screenHeight))

    # create rectangle
    imgRect = img.get_rect()

    done = False

    # animate
    while not done:

        # background color fill
        screen.fill(color=bgColor)

        # add img
        screen.blit(img, imgRect)

        # moving
        imgRect = imgRect.move(speed)

        # collision
        if imgRect.left < 0 or imgRect.right > screenWidth:
            speed[0] *= -1
            img = Img.update()

        if imgRect.top < 0 or imgRect.bottom > screenHeight:
            speed[1] *= -1
            img = Img.update()

        # refresh screen
        pygame.display.flip()
        time.sleep(10/1000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True


if __name__ == '__main__':
    main(img_path='Big_chungus.png')
