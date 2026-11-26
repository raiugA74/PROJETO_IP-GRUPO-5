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

    def update(self, keys, platforms, current_world):
        # Atualiza o jogador em um quadro, sempre nesta ordem.   

        # keys: teclas pressionadas (pygame.key.get_pressed()).
        # platforms: lista de plataformas da fase.
        # current_world: mundo atual (luz ou sombra).
        
        # Só as plataformas sólidas no mundo atual contam como obstáculo.
        # As do outro mundo aparecem como contorno e podem ser atravessadas.
        solid_platforms = [p for p in platforms if p.is_solid(current_world)]

        self.move_horizontally(keys, solid_platforms)
        self.apply_jump_and_gravity(keys)
        self.land_on_platforms(solid_platforms)
        self.keep_inside_screen()

    def move_horizontally(self, keys, solid_platforms): # função da movimentaçã lateral em função de x
            dx = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx = -PLAYER_SPEED   # esquerda: diminui x
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx = PLAYER_SPEED    # direita: aumenta x

            self.rect.x += dx

            # Se entrou em uma plataforma, volta para a borda dela
            for platform in solid_platforms:
                if self.rect.colliderect(platform.rect):
                    if dx > 0:    # indo para a direita: bateu no lado esquerdo da plataforma
                        self.rect.right = platform.rect.left
                    elif dx < 0:  # indo para a esquerda: bateu no lado direito da plataforma
                        self.rect.left = platform.rect.right

    def apply_jump_and_gravity(self, keys):       # função controla a gravidadee e o deslocamento vertical
        pressing_jump = keys[pygame.K_UP] or keys[pygame.K_w]

        # Pulo: só começa se estava no chão (evita pulo infinito no ar)
        if pressing_jump and self.on_ground:
            self.vel_y = JUMP_FORCE

        # Pulo variável: soltou a tecla enquanto ainda subia, então o pulo fica incompleto(menor).
        # Toque rápido dá um pulo baixo, segurar dá o pulo completo.
        if not pressing_jump and self.vel_y < 0:
            self.vel_y *= JUMP_CUT

        # Gravidade: a cada quadro a velocidade de queda aumenta, até o limite
        self.vel_y = min(self.vel_y + GRAVITY, MAX_FALL_SPEED)
        self.rect.y += self.vel_y

    def land_on_platforms(self, solid_platforms):     # resolve a colisão de cair em cima da plataforma e ao bater a cabeça na plataforma não atravesar ela
        self.on_ground = False   # recalculado a cada quadro

        for platform in solid_platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:      # caindo: do alto em cima da plataforma
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                elif self.vel_y < 0:    # subindo: bateu a cabeça embaixo dela
                    self.rect.top = platform.rect.bottom
                self.vel_y = 0          # para de subir ou de cair

    def keep_inside_screen(self):     # função do limite de tela
        tamanho_tela = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.rect.clamp_ip(tamanho_tela)

        if self.rect.bottom >= SCREEN_HEIGHT:   # tocou o chão ai pode pular
            self.vel_y = 0
            self.on_ground = True

    def draw(self, screen):                             # desenha o jogador na tela
        pygame.draw.rect(screen, self.color, self.rect)