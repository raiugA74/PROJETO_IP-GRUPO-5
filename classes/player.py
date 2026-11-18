import pygame
from constants import PLAYER_SIZE, PLAYER_SPEED, PLAYER_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT


class Player:
    def __init__(self, x, y):
        # guarda posição e tamanho na tela
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.color = PLAYER_COLOR

    def move(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  # movimentação do personagem com AWSD ou setas.
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: #seta direita ou D
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]: #seta cima ou W
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: #seta baixo ou S
            self.rect.y += PLAYER_SPEED

        self.keep_inside_screen()   # garante que o player não sai dos limites da tela

    def keep_inside_screen(self):     # função do limite de tela
        tamanho_tela = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.rect.clamp_ip(tamanho_tela)

    def draw(self, screen):                             # desenha o jogador na tela
        pygame.draw.rect(screen, self.color, self.rect)