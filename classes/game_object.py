import pygame
from constants import (
    WORLD_LIGHT,
    PLAT_LIGHT, PLAT_SHADOW
)


class Platform:
    def __init__(self, x, y, width, height, world=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.world = world  # WORLD_LIGHT, WORLD_SHADOW ou None (nos dois mundos)

    def is_solid(self, current_world):
        # Retorna True se a plataforma existe no mundo atual
        if self.world is None or self.world == current_world:
            return True
        return False

    def draw(self, screen, current_world):
        # Só desenha a plataforma se ela existir no mundo atual (invisível no outro mundo)
        if self.is_solid(current_world):
            if current_world == WORLD_LIGHT:
                color = PLAT_LIGHT
            else:
                color = PLAT_SHADOW
            pygame.draw.rect(screen, color, self.rect, border_radius=4) 
        #só enxergamos a plataforma quando estamos no mesmo mundo que ela