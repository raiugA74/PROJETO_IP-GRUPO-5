import pygame
from constants import (HAZARD_COLOR, HAZARD_GHOST_COLOR,
                       WORLD_LIGHT, WORLD_SHADOW)


class Hazard:
    """Espinho parado que machuca o jogador, existe em um mundo só."""

    def __init__(self, x, y, width, height, world):
        # obriga a escolher Luz ou Sombra, pra nunca existir nos dois
        if world not in (WORLD_LIGHT, WORLD_SHADOW):
            raise ValueError("Hazard precisa de um mundo: WORLD_LIGHT ou WORLD_SHADOW")
        self.rect = pygame.Rect(x, y, width, height)  # posição e tamanho do espinho
        self.world = world                            # em qual mundo ele existe

    def is_active(self, current_world):
        # o espinho só vale se o jogador estiver no mundo dele
        return self.world == current_world

    def update(self):
        # espinho não se mexe, mas tem update() pra ficar igual ao inimigo
        pass

    def hits(self, player, current_world):
        # machuca só se estiver ativo no mundo atual E encostar no jogador
        return self.is_active(current_world) and self.rect.colliderect(player.rect)

    def draw(self, screen, current_world):
        if self.is_active(current_world):
            pygame.draw.rect(screen, HAZARD_COLOR, self.rect)         # ativo: vermelho cheio
        else:
            pygame.draw.rect(screen, HAZARD_GHOST_COLOR, self.rect, 2)  # outro mundo: só contorno