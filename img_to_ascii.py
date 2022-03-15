import cv2
from genericpath import isfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont


class image:
    def __init__(self, path, height=48, color_palette=None) -> None:
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
        self.img = cv2.resize(self.img, dsize=(height, int(height * r)),
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

    def start(self, fontname='arial.ttf', fontsize=11, height=200) -> None:
        """
        Create first image.

        Args:
            fontname: [str]: font to use for the ascii art (Default: Arial).
            fontsize: [int]: font size.
            height: [int]: height of final image.
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
        self.Img = self.Img.resize((int(self.height*self.r), self.height))

        # save image
        self.Img.save('result.png')

        # counter for color palette list
        self.i = 1

    def update(self) -> None:

        if self.i == len(self.color_palette):
            self.i = 0

        # update image
        self.Img = Image.new(mode='RGB', size=(
            self.w+4, self.h+4), color=(0, 0, 0))
        d = ImageDraw.Draw(self.Img)
        d.text(xy=(0, 0), text=self.img_ascii,
               fill=self.color_palette[self.i], align='left')

        self.Img = self.Img.resize((int(self.height*self.r), self.height))

        self.i += 1

        # save image
        self.Img.save('result.png')


if __name__ == '__main__':
    path = 'test_images/adidas.jpg'

    img = image(path=path)

    img.to_ascii()

    img.start()

    pause = input('Press <ENTER> to continue...')

    img.update()
