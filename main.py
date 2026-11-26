import pygame
import json
import os

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WINDOW_TITLE,
    WORLD_LIGHT, WORLD_SHADOW, BG_LIGHT, BG_SHADOW,
    PLAYER_LIGHT, PLAYER_SHADOW
)
from classes.player import Player
from classes.scoreboard import Scoreboard
from levels.level import Level

pygame.init()  # liga o PyGame e inicia o jogo
som_clique = pygame.mixer.Sound("assets/sounds/click.wav")  # carrega o som de clique
som_clique.set_volume(0.5)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # cria a janela
pygame.display.set_caption(WINDOW_TITLE)
clock = pygame.time.Clock()  # controla a velocidade do jogo

level = Level(1)  # carrega a Fase 1
spawn_x, spawn_y = level.player_spawn
player = Player(spawn_x, spawn_y)  # cria o jogador no canto esquerdo sobre o chão

current_world = WORLD_LIGHT  # começa no mundo da Luz

font = pygame.font.SysFont("arial", 22)  # fonte do placar
scoreboard = Scoreboard()                # placar com a contagem por tipo

estado = "menu"         # menu do jogo
menu_image = pygame.image.load("assets/images/menu.png")

rect_novo_jogo = pygame.Rect(550, 514, 181, 34)
rect_continuar = pygame.Rect(548, 558, 185, 30)
rect_opcoes = pygame.Rect(578, 602, 125, 38)
rect_sair = pygame.Rect(602, 649, 78, 29)
rect_voltar = pygame.Rect(20, 20, 100, 30)

botoes_menu = [rect_novo_jogo, rect_continuar, rect_opcoes, rect_sair]
botao_pressionado = None  # botão que está sendo pressionado no momento

running = True
while running:  # loop principal: repete até fechar a janela

    if estado == "menu":
        screen.blit(menu_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # 1. Efeito visual enquanto segura o clique
        if botao_pressionado is not None and pygame.mouse.get_pressed()[0]:
            overlay = pygame.Surface((botao_pressionado.width, botao_pressionado.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 110))
            screen.blit(overlay, botao_pressionado.topleft)
            pygame.draw.rect(screen, (255, 255, 255), botao_pressionado.move(2, 2), 2)
        else:
            botao_pressionado = None
            for rect in botoes_menu:
                if rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, (220, 220, 220), rect, 2)

        # 2. Eventos: marca ao apertar (MOUSEBUTTONDOWN) e executa ao soltar (MOUSEBUTTONUP)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                json.dump({
                    "player_x": player.rect.x,
                    "player_y": player.rect.y,
                    "current_world": current_world,
                    "scores": scoreboard.counts
                }, open("save/save.json", "w"))
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                for rect in botoes_menu:
                    if rect.collidepoint(pos):
                        botao_pressionado = rect
                        som_clique.play()
                        break

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = event.pos
                if botao_pressionado is not None and botao_pressionado.collidepoint(pos):
                    if botao_pressionado == rect_novo_jogo:
                        player.rect.x, player.rect.y = level.player_spawn
                        current_world = WORLD_LIGHT
                        estado = "jogo"
                    elif botao_pressionado == rect_continuar:
                        if os.path.exists("save/save.json"):
                            with open("save/save.json", "r") as f:
                                save_data = json.load(f)
                                player.rect.x = save_data["player_x"]
                                player.rect.y = save_data["player_y"]
                                current_world = save_data["current_world"]
                                scoreboard.counts = save_data["scores"]
                            estado = "jogo"
                    elif botao_pressionado == rect_opcoes:
                        estado = "opções"
                    elif botao_pressionado == rect_sair:
                        running = False
                botao_pressionado = None

        pygame.display.flip()

    elif estado == "opções":
        screen.fill((0, 0, 0))
        font_titulo = pygame.font.SysFont("arial", 30)
        text_surface = font_titulo.render("Opções do Jogo", True, (255, 255, 255))
        screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 100))

        voltar_surface = font.render("Voltar", True, (255, 255, 255))
        voltar_rect = voltar_surface.get_rect(topleft=(20, 20))
        screen.blit(voltar_surface, voltar_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                json.dump({
                    "player_x": player.rect.x,
                    "player_y": player.rect.y,
                    "current_world": current_world,
                    "scores": scoreboard.counts
                }, open("save/save.json", "w"))
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if voltar_rect.collidepoint(mouse_pos):
                    som_clique.play()
                    estado = "menu"
        pygame.display.flip()

    elif estado == "jogo":
        # 1. Eventos: o que o jogador fez?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                json.dump({
                    "player_x": player.rect.x,
                    "player_y": player.rect.y,
                    "current_world": current_world,
                    "scores": scoreboard.counts
                }, open("save/save.json", "w"))
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
        if current_world == WORLD_LIGHT:
            bg_color = BG_LIGHT
            player.color = PLAYER_LIGHT
        else:
            bg_color = BG_SHADOW
            player.color = PLAYER_SHADOW

        # 4. Desenhar
        screen.fill(bg_color)
        level.draw(screen, current_world)  # desenha todas as plataformas da fase
        player.draw(screen)
        scoreboard.draw(screen, font)      # placar por cima de tudo
        pygame.display.flip()

        clock.tick(FPS)  # limita a 60 quadros por segundo

pygame.quit()