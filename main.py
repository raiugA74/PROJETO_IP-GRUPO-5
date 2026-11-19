import pygame
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WINDOW_TITLE,
    WORLD_LIGHT, WORLD_SHADOW, BG_LIGHT, BG_SHADOW,
    PLAYER_LIGHT, PLAYER_SHADOW
)
from classes.player import Player
from classes.scoreboard import Scoreboard


pygame.init()  # liga o PyGame e inicia o jogo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # cria a janela
pygame.display.set_caption(WINDOW_TITLE)
clock = pygame.time.Clock()  # controla a velocidade do jogo

player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # cria o objeto jogador
current_world = WORLD_LIGHT  # começa no mundo da Luz

font = pygame.font.SysFont("arial", 22)  # o scoreboard
scoreboard = Scoreboard()

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

    # 2. tras a função de movimento do player
    player.move(pygame.key.get_pressed())

    # 3. Cor da tela/jogador e mostra na janela
    if current_world == WORLD_LIGHT: #se o mundo atual for claro
        bg_color = BG_LIGHT 
        player.color = PLAYER_LIGHT #jogador na cor escura, player_light é o player no mundo light
    else: #se o mundo for escuro
        bg_color = BG_SHADOW 
        player.color = PLAYER_SHADOW #jogador na cor clara, player_shadow é o player no mundo shadow

    screen.fill(bg_color)
    scoreboard.draw(screen, font)
    player.draw(screen)
    pygame.display.flip()

    clock.tick(FPS)  # limita o clk a 60 quadros por segundo

pygame.quit()