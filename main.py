import pygame
import json
import os

from pygame import rect
from pygame.image import save

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WINDOW_TITLE,
    WORLD_LIGHT, WORLD_SHADOW, BG_LIGHT, BG_SHADOW,
    PLAYER_LIGHT, PLAYER_SHADOW
)
from classes.player import Player
from classes.game_object import Platform
from classes.scoreboard import Scoreboard

pygame.init()  # liga o PyGame e inicia o jogo
som_clique = pygame.mixer.Sound("assets/sounds/click.wav") # carrega o som de clique
som_clique.set_volume(0.5)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # cria a janela
pygame.display.set_caption(WINDOW_TITLE)
clock = pygame.time.Clock()  # controla a velocidade do jogo

player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # cria o objeto jogador
current_world = WORLD_LIGHT  # começa no mundo da Luz

platforms = [
    Platform(0, 460, SCREEN_WIDTH, 40, world=None),          # Chão (existe nos dois)
    Platform(180, 350, 160, 20, world=WORLD_LIGHT),          # Só sólida na Luz
    Platform(460, 260, 160, 20, world=WORLD_SHADOW),         # Só sólida na Sombra
]

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
        for event in pygame.event.get(): # pega todos os eventos do PyGame (teclado, mouse, etc.)
            if event.type == pygame.QUIT: # fecha o jogo ao clicar no X da janela
                json.dump({
                    "player_x": player.rect.x,
                    "player_y": player.rect.y,
                    "current_world": current_world,
                    "scores": scoreboard.counts
                }, open("save/save.json", "w"))
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # marca o botão que está sendo pressionado
                pos = event.pos
                for rect in botoes_menu:
                    if rect.collidepoint(pos): # verifica se o mouse está sobre algum botão
                        botao_pressionado = rect
                        som_clique.play()  # reproduz o som de clique
                        break

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: # executa a ação do botão ao soltar
                pos = event.pos
                if botao_pressionado is not None and botao_pressionado.collidepoint(pos): # verifica se o botão pressionado é o mesmo que foi solto
                    if botao_pressionado == rect_novo_jogo:
                        player.rect.x = SCREEN_WIDTH // 2
                        player.rect.y = SCREEN_HEIGHT // 2
                        current_world = WORLD_LIGHT
                        estado = "jogo"
                    elif botao_pressionado == rect_continuar: # continua o jogo a partir do save.json
                        if os.path.exists("save/save.json"):
                            with open("save/save.json", "r") as f: # lê o arquivo save.json e carrega os dados salvos
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

    elif estado == "opções":    # botão de opções do jogo
        screen.fill((0, 0, 0))  # fundo preto
        font = pygame.font.SysFont("arial", 30)
        text_surface = font.render("Opções do Jogo", True, (255, 255, 255))
        screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 100)) # centraliza o texto horizontalmente
        font = pygame.font.SysFont("arial", 24)

        voltar_surface = font.render("Voltar", True, (255, 255, 255)) # renderiza o texto do botão "Voltar"
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
        if current_world == WORLD_LIGHT:  # se o mundo atual for claro
            bg_color = BG_LIGHT
            player.color = PLAYER_LIGHT   # jogador escuro no mundo da Luz
        else:                             # se o mundo for escuro
            bg_color = BG_SHADOW
            player.color = PLAYER_SHADOW  # jogador claro no mundo da Sombra

        # 4. Desenhar
        screen.fill(bg_color)
        for platform in platforms:
            platform.draw(screen, current_world)  # sólida no mundo dela, contorno no outro
        player.draw(screen)
        scoreboard.draw(screen, font)  # placar por cima de tudo
        pygame.display.flip()

        clock.tick(FPS)  # limita a 60 quadros por segundo

pygame.quit()