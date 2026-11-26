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
from classes.sprite_sheet import PlayerAnimator  # animação do jogador
from audio import AudioManager                   # sons do jogo

pygame.init()  # liga o PyGame e inicia o jogo
som_clique = pygame.mixer.Sound("assets/sounds/click.wav")  # carrega o som de clique
som_clique.set_volume(0.5)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # cria a janela
pygame.display.set_caption(WINDOW_TITLE)
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
rect_voltar = pygame.Rect(20, 20, 100, 30) # define a posição e tamanho do botão de voltar no menu de opções

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
            # 3. Executa a ação do botão ao soltar o clique
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
    # 4. Tela de opções
    elif estado == "opções":

        screen.fill((0, 0, 0)) # preenche a tela de opções com preto
        font_titulo = pygame.font.SysFont("arial", 30) # cria a fonte para os títulos
        text_surface = font_titulo.render("Opções do Jogo", True, (255, 255, 255)) # cria a superfície do texto do título
        text_som = font_titulo.render("som", True, (255, 255, 255)) # cria a superfície do texto do título
        text_controle = font_titulo.render("controle", True, (255, 255, 255)) # cria a superfície do texto do título
        screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 100)) # centraliza o título na tela
        screen.blit(text_som, (SCREEN_WIDTH // 2 - text_som.get_width() // 2, 150)) # centraliza o texto "som" na tela
        screen.blit(text_controle, (SCREEN_WIDTH // 2 - text_controle.get_width() // 2, 200)) # centraliza o texto "controle" na tela

        voltar_surface = font.render("Voltar", True, (255, 255, 255)) # cria a superfície do texto do botão de voltar
        rect_voltar = voltar_surface.get_rect()  # cria um retângulo para o botão de voltar
        rect_voltar.inflate_ip(6, 3) # aumenta o retângulo para dar espaço ao texto
        rect_voltar.topleft = (20, 20) # define a posição do retângulo
        text_pos = voltar_surface.get_rect(center=rect_voltar.center) # centraliza o texto no retângulo
        screen.blit(voltar_surface, text_pos) # desenha o texto do botão de voltar

        rect_som = pygame.Rect(SCREEN_WIDTH // 2 - 40, 155, 80, 30) # cria um retângulo para o botão de som
        rect_controle = pygame.Rect(SCREEN_WIDTH // 2 - 50, 205, 100, 30) # cria um retângulo para o botão de controle

        botoes_opcoes = [rect_voltar, rect_som, rect_controle]  # lista de botões na tela de opções
        mouse_pos = pygame.mouse.get_pos()
        
        if botao_pressionado is not None and pygame.mouse.get_pressed()[0]: # se o botão está sendo pressionado...
            overlay = pygame.Surface((botao_pressionado.width, botao_pressionado.height), pygame.SRCALPHA) # cria uma superfície transparente do tamanho do botão
            overlay.fill((0, 0, 0, 110)) # preenche a superfície com uma cor preta semi-transparente (110 = 43% de opacidade)
            screen.blit(overlay, botao_pressionado.topleft) # desenha a superfície sobre o botão pressionado
            pygame.draw.rect(screen, (255, 255, 255), botao_pressionado.move(2, 2), 2) # desenha um contorno branco no botão pressionado, deslocado 2 pixels para baixo e para a direita
        else:
            botao_pressionado = None # se o botão não está sendo pressionado, zera a variável
            for rect in botoes_opcoes: # passa por cada botão das opções
                if rect.collidepoint(mouse_pos): # se o mouse está sobre o botão, desenha um contorno branco
                    pygame.draw.rect(screen, (220, 220, 220), rect, 2) # desenha um contorno branco no botão que o mouse está sobre
        
        for event in pygame.event.get(): # eventos do menu de opções
            if event.type == pygame.QUIT: # se o jogador fecha a janela, salva o jogo e encerra
                json.dump({ # salva a posição do jogador, mundo atual e pontuação em um arquivo JSON
                    "player_x": player.rect.x,
                    "player_y": player.rect.y,
                    "current_world": current_world,
                    "scores": scoreboard.counts
                }, open("save/save.json", "w"))
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN: # se o jogador apertou o botão do mouse, verifica se clicou em algum botão
                mouse_pos = event.pos
                mouse_pos = pygame.mouse.get_pos() # obtém a posição do mouse
                for rect in botoes_opcoes:
                    if rect.collidepoint(mouse_pos): # se o mouse está sobre o botão, marca como pressionado
                        botao_pressionado = rect
                        som_clique.play() # toca o som de clique
                        break
                if rect_voltar.collidepoint(mouse_pos): # se o jogador clicou no botão de voltar, volta para o menu principal
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

        # 2. Atualizar: movimento do jogador e inimigos
        player.move(pygame.key.get_pressed())

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