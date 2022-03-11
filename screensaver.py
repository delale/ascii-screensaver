import pygame
import time
from numpy.random import uniform

pygame.init()

# params
screenWidth, screenHeight = 1920, 1080
bgColor = 0, 0, 0
speed = [uniform(1.75, 2.25), uniform(1.75, 2.25)]

# initialize screen
screen = pygame.display.set_mode((screenWidth, screenHeight))

# load image
img = pygame.image.load('result.jpg')

# resize
# img = pygame.transform.scale(img, (100, 100))

# create rectangle
imgRect = img.get_rect()

# animate
while True:

    # background color fill
    screen.fill(color=bgColor)

    # add img
    screen.blit(img, imgRect)

    # moving
    imgRect = imgRect.move(speed)

    # collision
    if imgRect.left < 0 or imgRect.right > screenWidth:
        speed[0] *= -1
        img = pygame.image.load('result2.jpg')  # mock update

    if imgRect.top < 0 or imgRect.bottom > screenHeight:
        speed[1] *= -1

    # refresh screen
    pygame.display.flip()
    time.sleep(10/1000)
