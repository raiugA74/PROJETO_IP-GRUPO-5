import pygame
from constants import (PLAYER_SIZE, PLAYER_SPEED, PLAYER_COLOR,
                       SCREEN_WIDTH, SCREEN_HEIGHT,
                       GRAVITY, JUMP_FORCE, MAX_FALL_SPEED, JUMP_CUT)


class Player:
    def __init__(self, x, y):
        # guarda posição e tamanho na tela
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.color = PLAYER_COLOR
        self.vel_y = 0            # velocidade vertical (positivo = descendo)
        self.on_ground = False    # True quando está pisando em algo

    def move(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  # movimentação do personagem com AWSD ou setas.
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: #seta direita ou D
            self.rect.x += PLAYER_SPEED

        # Pulo: só funciona se estiver no chão
        holding_jump = keys[pygame.K_UP] or keys[pygame.K_w]
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = JUMP_FORCE

        # Pulo variável: se soltou a tecla enquanto ainda subia,
        # corta a subida e o jogador começa a cair mais cedo
        if not holding_jump and self.vel_y < 0:
            self.vel_y *= JUMP_CUT

        self.vel_y = min(self.vel_y + GRAVITY, MAX_FALL_SPEED)     # Gravidade: a cada quadro a velocidade de queda aumenta,
        self.rect.y += self.vel_y                                  # até o limite MAX_FALL_SPEED
                                                                
        self.keep_inside_screen()   # garante que o player não sai dos limites da tela

    def keep_inside_screen(self):     # função do limite de tela
        tamanho_tela = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.rect.clamp_ip(tamanho_tela)

        if self.rect.bottom >= SCREEN_HEIGHT:   # tocou o chão ai pode pular
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

    def draw(self, screen):                             # desenha o jogador na tela
        pygame.draw.rect(screen, self.color, self.rect)