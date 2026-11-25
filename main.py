import pygame
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WINDOW_TITLE,
    WORLD_LIGHT, WORLD_SHADOW, BG_LIGHT, BG_SHADOW,
    PLAYER_LIGHT, PLAYER_SHADOW
)
from classes.player import Player
from classes.game_object import Platform
from classes.scoreboard import Scoreboard
from levels.level import Level

pygame.init()  # liga o PyGame e inicia o jogo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # cria a janela
pygame.display.set_caption(WINDOW_TITLE)
clock = pygame.time.Clock()  # controla a velocidade do jogo

level = Level(1)  # carrega a Fase 1
spawn_x, spawn_y = level.player_spawn
player = Player(spawn_x, spawn_y)  # cria o jogador no canto esquerdo sobre o chão

current_world = WORLD_LIGHT  # começa no mundo da Luz

font = pygame.font.SysFont("arial", 22)  # fonte do placar
scoreboard = Scoreboard()                # placar com a contagem por tipo

running = True
while running:  # loop principal: repete até fechar a janela
    # 1. Eventos: o que o jogador fez?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # alterna o mundo ao apertar ESPAÇO
                if current_world == WORLD_LIGHT:
                    current_world = WORLD_SHADOW
                else:
                    current_world = WORLD_LIGHT

    # 2. Atualizar: movimento do jogador
    player.move(pygame.key.get_pressed())

    # 3. Cor da tela e do jogador conforme o mundo
    if current_world == WORLD_LIGHT:  # se o mundo atual for claro
        bg_color = BG_LIGHT
        player.color = PLAYER_LIGHT   # jogador escuro no mundo da Luz
    else:                             # se o mundo for escuro
        bg_color = BG_SHADOW
        player.color = PLAYER_SHADOW  # jogador claro no mundo da Sombra

    # 4. Desenhar
    screen.fill(bg_color)
    level.draw(screen, current_world)  # desenha todas as plataformas da fase
    player.draw(screen)
    scoreboard.draw(screen, font)      # placar por cima de tudo
    pygame.display.flip()

    clock.tick(FPS)  # limita a 60 fps

pygame.quit()