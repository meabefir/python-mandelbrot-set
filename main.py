import pygame, math, sys
from pygame import gfxdraw
from helper import *
import time

pygame.init()
window_size = (600, 600)
screen = pygame.display.set_mode(window_size)

escape_steps = 50
ppu = 100
acc = 4
zoom = 2
zoom_amm = 4


class ComplexNumber():
    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary

    def add(self, other):
        return ComplexNumber(self.real + other.real, self.imaginary + other.imaginary)

    def mul(self, other):
        return ComplexNumber(self.real * other.real - self.imaginary * other.imaginary,
                             self.real * other.imaginary + self.imaginary * other.real)

    def steps_to_infinity(self):
        steps = 0
        extra = ComplexNumber(0, 0)
        for i in range(100):
            if extra.real * extra.real + extra.imaginary * extra.imaginary < 4:
                # print(extra,' * ',extra,' + ',self,' = ',end='')
                steps += 1
                extra = self.add(extra.mul(extra))
                # print(self)
            else:
                return steps
        return steps

    def __str__(self):
        return f'{self.real} + {self.imaginary}i'


class Camera():
    def __init__(self):
        self.x = -int(window_size[0] / 2)
        self.y = -int(window_size[1] / 2)

    def update(self, x, y):
        # self.x = x * ppu - window_size[0] / 2
        # self.y = y * ppu - window_size[1] / 2
        self.x = x * ppu - window_size[0] / 2
        self.y = y * ppu - window_size[1] / 2


def draw_mandelbrot():
    window_middle_x = (window_size[0] / 2 + camera.x)
    window_middle_y = (window_size[1] / 2 + camera.y)
    for y in range(int(window_middle_y-window_size[1]/2), int(window_middle_y+window_size[1]/2), acc):
        for x in range(int(window_middle_x-window_size[0]/2), int(window_middle_x+window_size[0]/2), acc):
            complex = ComplexNumber(x / ppu, y / ppu)
            steps = complex.steps_to_infinity()
            color = None
            if steps == escape_steps:
                color = (255, 255, 255)
            else:
                # print(steps)
                color = ((255 + steps * 10) % 255, (255 + steps * 10) % 255, (255 + steps * 10) % 255)
            pygame.draw.rect(screen, color, (x - camera.x, y - camera.y, acc, acc))
            #pygame.gfxdraw.pixel(screen, int(x - camera.x), int(y - camera.y), color)


camera = Camera()

while True:
    screen.fill((0, 0, 0))

    draw_mandelbrot()
    pygame.draw.rect(screen, (255, 0, 0), (window_size[0] / 2, window_size[1] / 2, 4, 4))
    pygame.display.update()

    ev = False
    while not ev:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x = (event.pos[0] + camera.x) / ppu
                mouse_y = (event.pos[1] + camera.y) / ppu
                if event.button == 1:
                    ppu *= zoom_amm
                    zoom /= zoom_amm
                    camera.update(mouse_x, mouse_y)
                    #print(mouse_x, mouse_y)

                    ev = True
                elif event.button == 3:
                    ppu /= zoom_amm
                    zoom *= zoom_amm
                    #print(mouse_x, mouse_y)
                    camera.update(mouse_x, mouse_y)
                    ev = True
