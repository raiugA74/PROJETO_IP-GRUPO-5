from re import sub

import pygame
import json
import os
import math
import random

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

def desenhar_hover_menu(tela, lista_botoes, mouse_pos, particulas):
    tempo_ms = pygame.time.get_ticks()
    pulso = int((math.sin(tempo_ms * 0.008) + 1) * 20)

    botao_hover = None
    for rect in lista_botoes:
        if rect.collidepoint(mouse_pos):
            botao_hover = rect
            break

    novas_particulas = []
    if botao_hover is not None and random.random() < 0.65:
        px = random.randint(botao_hover.left - 10, botao_hover.right + 18)
        py = random.randint(botao_hover.top - 4, botao_hover.bottom + 4)
        vx = random.uniform(0.3, 1.2)
        vy = random.uniform(-0.8, 0.8)
        particulas.append([px, py, vx, vy, 220])

    for p in particulas:
        p[0] += p[2]
        p[1] += p[3]
        p[4] -= 5
        if p[4] > 0:
            surf_p = pygame.Surface((8, 8), pygame.SRCALPHA)
            pygame.draw.circle(surf_p, (255, 235, 160, p[4]), (4, 4), 2)
            tela.blit(surf_p, (int(p[0]), int(p[1])))
            novas_particulas.append(p)
    particulas[:] = novas_particulas

    if botao_hover is not None:
        # Brilho encaixado dentro do retângulo branco (descontando 4px em cada lado)
        margem = 4
        largura_glow = max(1, botao_hover.width - margem * 2) # 
        altura_glow = max(1, botao_hover.height - margem * 2) # 

        glow = pygame.Surface((largura_glow, altura_glow), pygame.SRCALPHA)
        glow.fill((255, 230, 150, 35 + pulso))
        tela.blit(glow, (botao_hover.x + margem, botao_hover.y + margem))

        pygame.draw.rect(tela, (220, 220, 220), botao_hover, 2)

        desloc_seta = int(math.sin(tempo_ms * 0.01) * 3)
        sx = botao_hover.left - 18 + desloc_seta
        sy = botao_hover.centery
        seta = [(sx, sy - 7), (sx + 10, sy), (sx, sy + 7)]
        pygame.draw.polygon(tela, (255, 240, 170), seta)
    else:
        particulas.clear()

pygame.init()  # liga o PyGame e inicia o jogo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # cria a janela
pygame.display.set_caption(WINDOW_TITLE) # define o título da janela
clock = pygame.time.Clock()  # controla a velocidade do jogo

som_clique = pygame.mixer.Sound("assets/sounds/click.wav")  # carrega o som de clique
som_clique.set_volume(0.5) # define o volume do som de clique (0.0 a 1.0)

volume_atual = 0.5  # <-- variáveis do áudio fora do while
mudo = False

def aplicar_audio():  # <-- função definida fora e antes do while
    volume_efetivo = 0.0 if mudo else volume_atual
    som_clique.set_volume(volume_efetivo)
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.set_volume(volume_efetivo)

level = Level(1)  # carrega a Fase 1
spawn_x, spawn_y = level.player_spawn
player = Player(spawn_x, spawn_y)  # cria o jogador no canto esquerdo sobre o chão
animador = PlayerAnimator()        # sprite do jogador (parado/andando)
audio = AudioManager()             # gerenciador de sons

current_world = WORLD_LIGHT  # começa no mundo da Luz

font = pygame.font.SysFont("arial", 22)  # fonte do placar
scoreboard = Scoreboard()                # placar com a contagem por tipo

estado = "menu"         # menu do jogo
menu_image = pygame.image.load("assets/images/menu.png") #  carrega a imagem do menu
opções_image = pygame.image.load("assets/images/opções.png") # carrega a imagem da tela de opções
controle_image = pygame.image.load("assets/images/controle.png") # carrega a imagem da tela de controle
som_image = pygame.image.load("assets/images/som.png") # carrega a imagem da tela de som

rect_novo_jogo = pygame.Rect(550, 505, 181, 37) # cria retângulos para os botões do menu
rect_continuar = pygame.Rect(545, 552, 190, 31) # define a posição e tamanho dos botões do menu
rect_opcoes = pygame.Rect(577, 595, 125, 38) # define a posição e tamanho dos botões do menu
rect_sair = pygame.Rect(602, 643, 78, 30) # define a posição e tamanho dos botões do menu

botoes_menu = [rect_novo_jogo, rect_continuar, rect_opcoes, rect_sair]
botao_pressionado = None  # botão que está sendo pressionado no momento

hits = 0        # quantas vezes o jogador tomou dano (contador de teste)
hit_timer = 0   # cronômetro pra não contar dano 60 vezes por segundo

particulas_menu = []  # cada item: [x, y, vx, vy, alpha]

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
            botao_pressionado = None
            desenhar_hover_menu(screen, botoes_menu, mouse_pos, particulas_menu)

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
        screen.blit(opções_image, (0, 0))

        font_titulo = pygame.font.SysFont("arial", 30)
        text_surface = font_titulo.render("Opções do Jogo", True, (255, 255, 255))
        text_som = font_titulo.render("som", True, (255, 255, 255))
        text_controle = font_titulo.render("controle", True, (255, 255, 255))
        text_menu = font_titulo.render("menu", True, (255, 255, 255))

        screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 100))
        screen.blit(text_som, (SCREEN_WIDTH // 2 - text_som.get_width() // 2, 150))
        screen.blit(text_controle, (SCREEN_WIDTH // 2 - text_controle.get_width() // 2, 200))

        rect_som = pygame.Rect(SCREEN_WIDTH // 2 - 40, 155, 80, 30)
        rect_controle = pygame.Rect(SCREEN_WIDTH // 2 - 50, 205, 100, 30)

        botoes_opcoes = [rect_som, rect_controle]
        rect_menu = None

        if estado_anterior == 'jogo':
            text_menu = font_titulo.render("menu", True, (255, 255, 255))
            screen.blit(text_menu, (SCREEN_WIDTH // 2 - text_menu.get_width() // 2, 250))
            rect_menu = pygame.Rect(SCREEN_WIDTH // 2 - 40, 255, 80, 30)
            botoes_opcoes.append(rect_menu)

        if botao_pressionado is not None and pygame.mouse.get_pressed()[0]:
            overlay = pygame.Surface((botao_pressionado.width, botao_pressionado.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 110))
            screen.blit(overlay, botao_pressionado.topleft)
            pygame.draw.rect(screen, (255, 255, 255), botao_pressionado.move(2, 2), 2)
        else:
            botao_pressionado = None
            desenhar_hover_menu(screen, botoes_opcoes, mouse_pos, particulas_menu)

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
                    elif rect_menu is not None and botao_pressionado == rect_menu:
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

        # 1. Botão de Mudo (mostra OFF quando normal, ON quando mutado)
        texto_mudo = "Mudo: ON" if mudo else "Mudo: OFF"
        mudo_surface = font.render(texto_mudo, True, (255, 255, 255))
        rect_mudo = mudo_surface.get_rect(center=(SCREEN_WIDTH // 2, 170))
        rect_mudo.inflate_ip(20, 10)
        screen.blit(mudo_surface, mudo_surface.get_rect(center=rect_mudo.center))

        # 2. Barra de Volume (0 à esquerda, 1 à direita)
        barra_x = SCREEN_WIDTH // 2 - 100
        barra_y = 230
        barra_largura = 200
        barra_altura = 20
        rect_barra = pygame.Rect(barra_x, barra_y, barra_largura, barra_altura)

        lbl_zero = font.render("0", True, (255, 255, 255))
        lbl_um = font.render("1", True, (255, 255, 255))
        lbl_valor = font.render(f"{volume_atual:.1f}", True, (200, 200, 200))

        screen.blit(lbl_zero, (barra_x - lbl_zero.get_width() - 12, barra_y - 2))
        screen.blit(lbl_um, (barra_x + barra_largura + 12, barra_y - 2))
        screen.blit(lbl_valor, (SCREEN_WIDTH // 2 - lbl_valor.get_width() // 2, barra_y + 28))

        # Fundo e preenchimento da barra (0 na tela se mudo, mas volume_atual não é perdido)
        pygame.draw.rect(screen, (70, 70, 70), rect_barra)
        nivel_visual = 0.0 if mudo else volume_atual
        largura_preenchida = int(barra_largura * nivel_visual)
        if largura_preenchida > 0:
            pygame.draw.rect(screen, (255, 255, 255), (barra_x, barra_y, largura_preenchida, barra_altura))
        pygame.draw.rect(screen, (220, 220, 220), rect_barra, 2)

        # Hover no botão de mudo
        if rect_mudo.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (220, 220, 220), rect_mudo, 2)

        # Arrastar ou clicar na barra para ajustar volume_atual (0.0 a 1.0)
        if pygame.mouse.get_pressed()[0] and rect_barra.collidepoint(mouse_pos):
            rel_x = (mouse_pos[0] - barra_x) / barra_largura
            volume_atual = max(0.0, min(1.0, round(rel_x, 1)))
            mudo = False
            aplicar_audio()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                som_clique.play()
                estado = "opções"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rect_mudo.collidepoint(event.pos):
                    mudo = not mudo
                    aplicar_audio()
                    if not mudo:
                        som_clique.play()
                elif rect_barra.collidepoint(event.pos):
                    rel_x = (event.pos[0] - barra_x) / barra_largura
                    volume_atual = max(0.0, min(1.0, round(rel_x, 1)))
                    mudo = False
                    aplicar_audio()
                    som_clique.play()

        pygame.display.flip()

    elif estado == "controle":
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(controle_image, (0, 0))

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