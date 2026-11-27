import pygame
from constants import COLLECTIBLE_SIZE


class Collectible:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, COLLECTIBLE_SIZE, COLLECTIBLE_SIZE)