import pygame
from constants import (ENEMY_COLOR, ENEMY_SPEED, ENEMY_SIZE,
                       WORLD_LIGHT, WORLD_SHADOW)


class Enemy:
    """Inimigo que patrulha de um lado ao outro, existe em um mundo só."""

    def __init__(self, x, y, left_limit, right_limit, world):
        # obriga a escolher Luz ou Sombra, pra nunca existir nos dois
        if world not in (WORLD_LIGHT, WORLD_SHADOW):
            raise ValueError("Enemy precisa de um mundo: WORLD_LIGHT ou WORLD_SHADOW")
        self.rect = pygame.Rect(x, y, ENEMY_SIZE, ENEMY_SIZE)  # posição e tamanho do inimigo
        self.left_limit = left_limit     # até onde ele vai pra esquerda
        self.right_limit = right_limit   # até onde ele vai pra direita
        self.speed = ENEMY_SPEED         # velocidade (o sinal define a direção)
        self.world = world               # em qual mundo ele existe

    def is_active(self, current_world):
        # o inimigo só vale se o jogador estiver no mundo dele
        return self.world == current_world

    def update(self):
        self.rect.x += self.speed  # anda um passo na direção atual
        if self.rect.left <= self.left_limit or self.rect.right >= self.right_limit:
            self.speed = -self.speed  # chegou no limite: vira pro outro lado

    def hits(self, player, current_world):
        # machuca só se estiver ativo no mundo atual E encostar no jogador
        return self.is_active(current_world) and self.rect.colliderect(player.rect)

    def draw(self, screen, current_world):
        if self.is_active(current_world):
            pygame.draw.rect(screen, ENEMY_COLOR, self.rect)  # só aparece no mundo dele