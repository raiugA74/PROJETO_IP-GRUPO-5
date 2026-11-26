from re import sub

import pygame
import json
import os

from pygame import mouse

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WINDOW_TITLE,
    WORLD_LIGHT, WORLD_SHADOW, BG_LIGHT, BG_SHADOW,
    PLAYER_LIGHT, PLAYER_SHADOW, PLAYER_LIVES, INVULN_FRAMES
)
from classes.player import Player # a classe do jogador
from classes.scoreboard import Scoreboard # a classe do placar
from levels.level import Level # a classe da fase
from classes.sprite_sheet import PlayerAnimator  # animação do jogador
from audio import AudioManager                   # sons do jogo

pygame.init()  # liga o PyGame e inicia o jogo
som_clique = pygame.mixer.Sound("assets/sounds/click.wav")  # carrega o som de clique
som_clique.set_volume(0.5) # define o volume do som de clique (0.0 a 1.0)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # cria a janela
pygame.display.set_caption(WINDOW_TITLE) # define o título da janela
clock = pygame.time.Clock()  # controla a velocidade do jogo

level = Level(1)  # carrega a Fase 1
spawn_x, spawn_y = level.player_spawn
player = Player(spawn_x, spawn_y)  # cria o jogador no canto esquerdo sobre o chão
animador = PlayerAnimator()        # sprite do jogador (parado/andando)
audio = AudioManager()             # gerenciador de sons

current_world = WORLD_LIGHT  # começa no mundo da Luz

font = pygame.font.SysFont("arial", 22)  # fonte do placar
scoreboard = Scoreboard()                # placar com a contagem por tipo

estado = "menu"         # menu do jogo
menu_image = pygame.image.load("assets/images/menu.png")

rect_novo_jogo = pygame.Rect(550, 514, 181, 34) # cria retângulos para os botões do menu
rect_continuar = pygame.Rect(548, 559, 185, 30) # define a posição e tamanho dos botões do menu
rect_opcoes = pygame.Rect(578, 602, 125, 38) # define a posição e tamanho dos botões do menu
rect_sair = pygame.Rect(602, 649, 78, 29) # define a posição e tamanho dos botões do menu

def desenhar_botao_voltar(tela, fonte):
    voltar_surface = fonte.render("Voltar", True, (255, 255, 255))
    rect = voltar_surface.get_rect()
    rect.inflate_ip(12, 6)
    rect.topleft = (20, 20)
    tela.blit(voltar_surface, voltar_surface.get_rect(center=rect.center))
    return rect

botoes_menu = [rect_novo_jogo, rect_continuar, rect_opcoes, rect_sair]
botao_pressionado = None  # botão que está sendo pressionado no momento

hits = 0        # quantas vezes o jogador tomou dano (contador de teste)
hit_timer = 0   # cronômetro pra não contar dano 60 vezes por segundo

running = True
while running:  # loop principal: repete até fechar a janela

    if estado == "menu":
        screen.blit(menu_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # 1. Efeito visual enquanto segura o clique
        if botao_pressionado is not None and pygame.mouse.get_pressed()[0]: # se o botão está sendo pressionado...
            overlay = pygame.Surface((botao_pressionado.width, botao_pressionado.height), pygame.SRCALPHA) # cria uma superfície transparente do tamanho do botão
            overlay.fill((0, 0, 0, 110)) # preenche a superfície com uma cor preta semi-transparente (110 = 43% de opacidade)
            screen.blit(overlay, botao_pressionado.topleft) # desenha a superfície sobre o botão pressionado
            pygame.draw.rect(screen, (255, 255, 255), botao_pressionado.move(2, 2), 2) # desenha um contorno branco no botão pressionado, deslocado 2 pixels para baixo e para a direita
        else:
            botao_pressionado = None # se o botão não está sendo pressionado, zera a variável
            for rect in botoes_menu: # passa por cada botão do menu
                if rect.collidepoint(mouse_pos): # se o mouse está sobre o botão, desenha um contorno branco
                    pygame.draw.rect(screen, (220, 220, 220), rect, 2) # desenha um contorno branco no botão que o mouse está sobre

        # 2. Eventos: marca ao apertar (MOUSEBUTTONDOWN) e executa ao soltar (MOUSEBUTTONUP)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                for rect in botoes_menu:
                    if rect.collidepoint(pos):
                        botao_pressionado = rect
                        som_clique.play()
                        break
            # 3. Executa a ação do botão ao soltar o clique
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: # se o jogador soltou o botão esquerdo do mouse
                pos = event.pos # obtém a posição do mouse ao soltar o clique
                if botao_pressionado is not None and botao_pressionado.collidepoint(pos): # se o botão pressionado é o mesmo que o mouse está sobre ao soltar
                    if botao_pressionado == rect_novo_jogo: # se o jogador clicou no botão de novo jogo, reinicia a fase e o jogador
                        player.rect.x, player.rect.y = level.player_spawn # reinicia a posição do jogador
                        current_world = WORLD_LIGHT # reinicia o mundo para o da Luz
                        estado = "jogo" 
                    elif botao_pressionado == rect_continuar: # se o jogador clicou no botão de continuar, carrega o save do jogo
                        if os.path.exists("save/save.json"): # verifica se o arquivo de save existe
                            with open("save/save.json", "r") as f: # abre o arquivo de save
                                save_data = json.load(f) # carrega os dados do save
                                player.rect.x = save_data["player_x"] # atualiza a posição do jogador
                                player.rect.y = save_data["player_y"] # atualiza a posição do jogador
                                current_world = save_data["current_world"] # atualiza o mundo atual
                                scoreboard.counts = save_data["scores"] # atualiza os pontos
                            estado = "jogo"
                    elif botao_pressionado == rect_opcoes: # se o jogador clicou no botão de opções, muda para a tela de opções
                        estado_anterior = "menu"
                        estado = "opções"
                    elif botao_pressionado == rect_sair: # se o jogador clicou no botão de sair, encerra o jogo
                        running = False
                botao_pressionado = None # zera a variável do botão pressionado ao soltar o clique

        pygame.display.flip()

    # 4. Tela de opções
    elif estado == "opções":
        mouse_pos = pygame.mouse.get_pos()
        screen.fill((0, 0, 0))

        font_titulo = pygame.font.SysFont("arial", 30)
        text_surface = font_titulo.render("Opções do Jogo", True, (255, 255, 255))
        text_som = font_titulo.render("som", True, (255, 255, 255))
        text_controle = font_titulo.render("controle", True, (255, 255, 255))
        text_menu = font_titulo.render("menu", True, (255, 255, 255))

        screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 100))
        screen.blit(text_som, (SCREEN_WIDTH // 2 - text_som.get_width() // 2, 150))
        screen.blit(text_controle, (SCREEN_WIDTH // 2 - text_controle.get_width() // 2, 200))
        screen.blit(text_menu, (SCREEN_WIDTH // 2 - text_menu.get_width() // 2, 250))

        rect_som = pygame.Rect(SCREEN_WIDTH // 2 - 40, 155, 80, 30)
        rect_controle = pygame.Rect(SCREEN_WIDTH // 2 - 50, 205, 100, 30)
        rect_menu = pygame.Rect(SCREEN_WIDTH // 2 - 40, 255, 80, 30)
        botoes_opcoes = [rect_som, rect_controle, rect_menu]

        if botao_pressionado is not None and pygame.mouse.get_pressed()[0]:
            overlay = pygame.Surface((botao_pressionado.width, botao_pressionado.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 110))
            screen.blit(overlay, botao_pressionado.topleft)
            pygame.draw.rect(screen, (255, 255, 255), botao_pressionado.move(2, 2), 2)
        else:
            botao_pressionado = None
            for rect in botoes_opcoes:
                if rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, (220, 220, 220), rect, 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                som_clique.play()
                estado = estado_anterior
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect in botoes_opcoes:
                    if rect.collidepoint(event.pos):
                        botao_pressionado = rect
                        som_clique.play()
                        break
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if botao_pressionado is not None and botao_pressionado.collidepoint(event.pos):
                    if botao_pressionado == rect_som:
                        estado = "som"
                    elif botao_pressionado == rect_controle:
                        estado = "controle"
                    elif botao_pressionado == rect_menu:
                        os.makedirs("save", exist_ok=True)
                        with open("save/save.json", "w", encoding="utf-8") as f:
                            json.dump({
                                "player_x": player.rect.x,
                                "player_y": player.rect.y,
                                "current_world": current_world,
                                "scores": scoreboard.counts
                            }, f)
                        estado = "menu"

                botao_pressionado = None

        pygame.display.flip()

    elif estado == "som":
        mouse_pos = pygame.mouse.get_pos()
        screen.fill((0, 0, 0))

        font_titulo = pygame.font.SysFont("arial", 30)
        text_som = font_titulo.render("Som", True, (255, 255, 255))
        screen.blit(text_som, (SCREEN_WIDTH // 2 - text_som.get_width() // 2, 100))

        rect_mudo = pygame.Rect(SCREEN_WIDTH // 2 - 40, 155, 80, 30)
        rect_volume = pygame.Rect(SCREEN_WIDTH // 2 - 40, 205, 80, 30)
        botoes_som = [rect_mudo, rect_volume]

        if botao_pressionado is not None and pygame.mouse.get_pressed()[0]:
            overlay = pygame.Surface((botao_pressionado.width, botao_pressionado.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 110))
            screen.blit(overlay, botao_pressionado.topleft)
            pygame.draw.rect(screen, (255, 255, 255), botao_pressionado.move(2, 2), 2)
        else:
            botao_pressionado = None
            for rect in botoes_som:
                if rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, (220, 220, 220), rect, 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                som_clique.play()
                estado = "opções"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect in botoes_som:
                    if rect.collidepoint(event.pos):
                        botao_pressionado = rect
                        som_clique.play()
                        break
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if botao_pressionado is not None and botao_pressionado.collidepoint(event.pos):
                    if botao_pressionado == rect_mudo:
                        audio.toggle_mute()
                    elif botao_pressionado == rect_volume:
                        audio.adjust_volume()
                botao_pressionado = None

        pygame.display.flip()

    elif estado == "controle":
        mouse_pos = pygame.mouse.get_pos()
        screen.fill((0, 0, 0))

        font_titulo = pygame.font.SysFont("arial", 30)
        text_controle = font_titulo.render("Controle", True, (255, 255, 255))
        screen.blit(text_controle, (SCREEN_WIDTH // 2 - text_controle.get_width() // 2, 100))

        rect_teclado = pygame.Rect(SCREEN_WIDTH // 2 - 50, 155, 100, 30)
        rect_mouse = pygame.Rect(SCREEN_WIDTH // 2 - 50, 205, 100, 30)
        botoes_controle = [rect_teclado, rect_mouse]

        if botao_pressionado is not None and pygame.mouse.get_pressed()[0]:
            overlay = pygame.Surface((botao_pressionado.width, botao_pressionado.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 110))
            screen.blit(overlay, botao_pressionado.topleft)
            pygame.draw.rect(screen, (255, 255, 255), botao_pressionado.move(2, 2), 2)
        else:
            botao_pressionado = None
            for rect in botoes_controle:
                if rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, (220, 220, 220), rect, 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                som_clique.play()
                estado = "opções"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect in botoes_controle:
                    if rect.collidepoint(event.pos):
                        botao_pressionado = rect
                        som_clique.play()
                        break
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if botao_pressionado is not None and botao_pressionado.collidepoint(event.pos):
                    if botao_pressionado == rect_teclado:
                        estado = "teclado"
                    elif botao_pressionado == rect_mouse:
                        estado = "mouse"
                botao_pressionado = None

        pygame.display.flip()

    elif estado == "jogo":
        # 1. Eventos: o que o jogador fez?
        for event in pygame.event.get(): # detecta eventos do jogo (teclado, mouse, etc.)
            if event.type == pygame.QUIT: # encerrar o jogo ao fechar a janela
                os.makedirs("save", exist_ok=True)
                with open("save/save.json", "w", encoding="utf-8") as f:
                    json.dump({
                        "player_x": player.rect.x,
                        "player_y": player.rect.y,
                        "current_world": current_world,
                        "scores": scoreboard.counts
                    }, f)
                running = False
            if event.type == pygame.KEYDOWN: # detecta quando uma tecla é pressionada
                if event.key == pygame.K_SPACE:  # alterna o mundo ao apertar ESPAÇO
                    if current_world == WORLD_LIGHT: # se o mundo atual é o da Luz, muda para o da Sombra
                        current_world = WORLD_SHADOW # alterna para o mundo da Sombra
                    else:
                        current_world = WORLD_LIGHT # alterna para o mundo da Luz
                elif event.key == pygame.K_ESCAPE: # volta para o menu ao apertar ESC
                    som_clique.play()
                    estado_anterior = "jogo"
                    estado = "opções"

        # 2. Atualizar: movimento do jogador
        player.update(pygame.key.get_pressed(), level.platforms, current_world)

        for enemy in level.enemies:                 # passa por cada inimigo e espinho da fase
            enemy.update()                          # inimigo dá um passo (espinho não faz nada)

        if hit_timer > 0:                           # se ainda está no tempo de espera...
            hit_timer -= 1                          # ...diminui 1 por quadro (60 = 1 segundo)

        tocou = any(e.hits(player, current_world) for e in level.enemies)  # algo perigoso encostou?
        if tocou and hit_timer == 0:                # encostou e já passou o tempo de espera
            hits += 1                               # conta 1 dano
            hit_timer = 60                          # 1 segundo sem poder levar dano de novo

        # 3. Cor da tela e animação do jogador conforme o mundo
        if current_world == WORLD_LIGHT:
            bg_color = BG_LIGHT
            player.color = PLAYER_LIGHT
        else:
            bg_color = BG_SHADOW
            player.color = PLAYER_SHADOW

        animador.update(player, current_world)  # escolhe a animação (parado ou andando)

        # 4. Desenhar
        screen.fill(bg_color)
        level.draw(screen, current_world)       # desenha todas as plataformas da fase

        for enemy in level.enemies:             # desenha inimigos e espinhos
            enemy.draw(screen, current_world)

        animador.draw(screen, player)           # desenha a sprite do jogador (no lugar de player.draw)
        scoreboard.draw(screen, font)           # placar por cima de tudo

        texto = font.render(f"Danos: {hits}", True, (255, 255, 255))  # monta o texto "Danos: N"
        screen.blit(texto, (SCREEN_WIDTH - 140, 10))                  # põe no canto direito de cima

        pygame.display.flip()

        clock.tick(FPS)  # limita a 60 quadros por segundo

pygame.quit()