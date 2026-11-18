import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WINDOW_TITLE, BACKGROUND_COLOR
from classes.player import Player

pygame.init()  # liga o PyGame e inicia o jogo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # cria a janela
pygame.display.set_caption(WINDOW_TITLE)
clock = pygame.time.Clock()  # controla a velocidade do jogo

player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # cria o objeto jogador

running = True
while running:  # loop principal: repete até fechar a janela
    # 1. Eventos: o que o jogador fez?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            running = False

    # 2. tras a função de movimento do player
    player.move(pygame.key.get_pressed())

    # 3. Cor da tela/jogador e mostra na janela
    screen.fill(BACKGROUND_COLOR)
    player.draw(screen)
    pygame.display.flip()

    clock.tick(FPS)  # limita o clk a 60 quadros por segundo

pygame.quit()