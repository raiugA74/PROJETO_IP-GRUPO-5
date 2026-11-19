import pygame
from constants import (
    WORLD_LIGHT, WORLD_SHADOW,
    PLAT_LIGHT, PLAT_SHADOW,
    PLAT_GHOST_LIGHT, PLAT_GHOST_SHADOW
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
        if self.is_solid(current_world):
            # Desenha preenchida se estiver ativa no mundo atual
            if current_world == WORLD_LIGHT:
                color = PLAT_LIGHT
            else:
                color = PLAT_SHADOW
            pygame.draw.rect(screen, color, self.rect, border_radius=4)
        else:
            # Desenha apenas a borda (fantasma) se pertencer ao outro mundo
            if self.world == WORLD_LIGHT:
                ghost_color = PLAT_GHOST_LIGHT
            else:
                ghost_color = PLAT_GHOST_SHADOW
            pygame.draw.rect(screen, ghost_color, self.rect, 2, border_radius=4)