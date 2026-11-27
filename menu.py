import pygame
import math
import random

from constants import SCREEN_WIDTH, FPS
from save_manager import salvar_jogo, carregar_jogo


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


def tela_menu(game):
    game.screen.blit(game.menu_image, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    # 1. Efeito visual enquanto segura o clique
    if game.botao_pressionado is not None and pygame.mouse.get_pressed()[0]: # se o botão está sendo pressionado...
        overlay = pygame.Surface((game.botao_pressionado.width, game.botao_pressionado.height), pygame.SRCALPHA) # cria uma superfície transparente do tamanho do botão
        overlay.fill((0, 0, 0, 110)) # preenche a superfície com uma cor preta semi-transparente (110 = 43% de opacidade)
        game.screen.blit(overlay, game.botao_pressionado.topleft) # desenha a superfície sobre o botão pressionado
        pygame.draw.rect(game.screen, (255, 255, 255), game.botao_pressionado.move(2, 2), 2) # desenha um contorno branco no botão pressionado, deslocado 2 pixels para baixo e para a direita
    else:
        game.botao_pressionado = None
        desenhar_hover_menu(game.screen, game.botoes_menu, mouse_pos, game.particulas_menu)

    # 2. Eventos: marca ao apertar (MOUSEBUTTONDOWN) e executa ao soltar (MOUSEBUTTONUP)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for rect in game.botoes_menu:
                if rect.collidepoint(pos):
                    game.botao_pressionado = rect
                    game.som_clique.play()
                    break
        # 3. Executa a ação do botão ao soltar o clique
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: # se o jogador soltou o botão esquerdo do mouse
            pos = event.pos # obtém a posição do mouse ao soltar o clique
            if game.botao_pressionado is not None and game.botao_pressionado.collidepoint(pos): # se o botão pressionado é o mesmo que o mouse está sobre ao soltar
                if game.botao_pressionado == game.rect_novo_jogo: # se o jogador clicou no botão de novo jogo, reinicia a fase e o jogador
                    game.reiniciar_partida() # zera vidas, danos e posição, e começa o jogo novamente
                elif game.botao_pressionado == game.rect_continuar: # se o jogador clicou no botão de continuar, carrega o save do jogo
                    carregar_jogo(game)
                elif game.botao_pressionado == game.rect_opcoes: # se o jogador clicou no botão de opções, muda para a tela de opções
                    game.estado_anterior = "menu"
                    game.estado = "opções"
                elif game.botao_pressionado == game.rect_sair: # se o jogador clicou no botão de sair, encerra o jogo
                    game.running = False
            game.botao_pressionado = None # zera a variável do botão pressionado ao soltar o clique

    pygame.display.flip()


# 4. Tela de opções
def tela_opcoes(game):
    mouse_pos = pygame.mouse.get_pos()
    game.screen.blit(game.opções_image, (0, 0))

    font_titulo = pygame.font.SysFont("arial", 30)
    text_surface = font_titulo.render("Opções do Jogo", True, (255, 255, 255))
    text_som = font_titulo.render("som", True, (255, 255, 255))
    text_controle = font_titulo.render("controle", True, (255, 255, 255))
    text_menu = font_titulo.render("menu", True, (255, 255, 255))

    game.screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 100))
    game.screen.blit(text_som, (SCREEN_WIDTH // 2 - text_som.get_width() // 2, 150))
    game.screen.blit(text_controle, (SCREEN_WIDTH // 2 - text_controle.get_width() // 2, 200))

    rect_som = pygame.Rect(SCREEN_WIDTH // 2 - 40, 155, 80, 30)
    rect_controle = pygame.Rect(SCREEN_WIDTH // 2 - 50, 205, 100, 30)

    botoes_opcoes = [rect_som, rect_controle]
    rect_menu = None

    if game.estado_anterior == 'jogo':
        text_menu = font_titulo.render("menu", True, (255, 255, 255))
        game.screen.blit(text_menu, (SCREEN_WIDTH // 2 - text_menu.get_width() // 2, 250))
        rect_menu = pygame.Rect(SCREEN_WIDTH // 2 - 40, 255, 80, 30)
        botoes_opcoes.append(rect_menu)

    if game.botao_pressionado is not None and pygame.mouse.get_pressed()[0]:
        overlay = pygame.Surface((game.botao_pressionado.width, game.botao_pressionado.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 110))
        game.screen.blit(overlay, game.botao_pressionado.topleft)
        pygame.draw.rect(game.screen, (255, 255, 255), game.botao_pressionado.move(2, 2), 2)
    else:
        game.botao_pressionado = None
        desenhar_hover_menu(game.screen, botoes_opcoes, mouse_pos, game.particulas_menu)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            game.som_clique.play()
            game.estado = game.estado_anterior
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for rect in botoes_opcoes:
                if rect.collidepoint(event.pos):
                    game.botao_pressionado = rect
                    game.som_clique.play()
                    break
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if game.botao_pressionado is not None and game.botao_pressionado.collidepoint(event.pos):
                if game.botao_pressionado == rect_som:
                    game.estado = "som"
                elif game.botao_pressionado == rect_controle:
                    game.estado = "controle"
                elif rect_menu is not None and game.botao_pressionado == rect_menu:
                    salvar_jogo(game)
                    game.estado = "menu"

            game.botao_pressionado = None

    pygame.display.flip()


def tela_som(game):
    mouse_pos = pygame.mouse.get_pos()
    game.screen.fill((0, 0, 0))

    font_titulo = pygame.font.SysFont("arial", 30)
    text_som = font_titulo.render("Som", True, (255, 255, 255))
    game.screen.blit(text_som, (SCREEN_WIDTH // 2 - text_som.get_width() // 2, 100))

    # 1. Botão de Mudo (mostra OFF quando normal, ON quando mutado)
    texto_mudo = "Mudo: ON" if game.mudo else "Mudo: OFF"
    mudo_surface = game.font.render(texto_mudo, True, (255, 255, 255))
    rect_mudo = mudo_surface.get_rect(center=(SCREEN_WIDTH // 2, 170))
    rect_mudo.inflate_ip(20, 10)
    game.screen.blit(mudo_surface, mudo_surface.get_rect(center=rect_mudo.center))

    # 2. Barra de Volume (0 à esquerda, 1 à direita)
    barra_x = SCREEN_WIDTH // 2 - 100
    barra_y = 230
    barra_largura = 200
    barra_altura = 20
    rect_barra = pygame.Rect(barra_x, barra_y, barra_largura, barra_altura)

    lbl_zero = game.font.render("0", True, (255, 255, 255))
    lbl_um = game.font.render("1", True, (255, 255, 255))
    lbl_valor = game.font.render(f"{game.volume_atual:.1f}", True, (200, 200, 200))

    game.screen.blit(lbl_zero, (barra_x - lbl_zero.get_width() - 12, barra_y - 2))
    game.screen.blit(lbl_um, (barra_x + barra_largura + 12, barra_y - 2))
    game.screen.blit(lbl_valor, (SCREEN_WIDTH // 2 - lbl_valor.get_width() // 2, barra_y + 28))

    # Fundo e preenchimento da barra (0 na tela se mudo, mas volume_atual não é perdido)
    pygame.draw.rect(game.screen, (70, 70, 70), rect_barra)
    nivel_visual = 0.0 if game.mudo else game.volume_atual
    largura_preenchida = int(barra_largura * nivel_visual)
    if largura_preenchida > 0:
        pygame.draw.rect(game.screen, (255, 255, 255), (barra_x, barra_y, largura_preenchida, barra_altura))
    pygame.draw.rect(game.screen, (220, 220, 220), rect_barra, 2)

    # Hover no botão de mudo
    if rect_mudo.collidepoint(mouse_pos):
        pygame.draw.rect(game.screen, (220, 220, 220), rect_mudo, 2)

    # Arrastar ou clicar na barra para ajustar volume_atual (0.0 a 1.0)
    if pygame.mouse.get_pressed()[0] and rect_barra.collidepoint(mouse_pos):
        rel_x = (mouse_pos[0] - barra_x) / barra_largura
        game.volume_atual = max(0.0, min(1.0, round(rel_x, 1)))
        game.mudo = False
        game.aplicar_audio()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            game.som_clique.play()
            game.estado = "opções"
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if rect_mudo.collidepoint(event.pos):
                game.mudo = not game.mudo
                game.aplicar_audio()
                if not game.mudo:
                    game.som_clique.play()
            elif rect_barra.collidepoint(event.pos):
                rel_x = (event.pos[0] - barra_x) / barra_largura
                game.volume_atual = max(0.0, min(1.0, round(rel_x, 1)))
                game.mudo = False
                game.aplicar_audio()
                game.som_clique.play()

    pygame.display.flip()


def tela_controle(game):
    mouse_pos = pygame.mouse.get_pos()
    game.screen.blit(game.controle_image, (0, 0))

    font_titulo = pygame.font.SysFont("arial", 30)
    text_controle = font_titulo.render("Controle", True, (255, 255, 255))
    game.screen.blit(text_controle, (SCREEN_WIDTH // 2 - text_controle.get_width() // 2, 100))

    rect_teclado = pygame.Rect(SCREEN_WIDTH // 2 - 50, 155, 100, 30)
    rect_mouse = pygame.Rect(SCREEN_WIDTH // 2 - 50, 205, 100, 30)
    botoes_controle = [rect_teclado, rect_mouse]

    if game.botao_pressionado is not None and pygame.mouse.get_pressed()[0]:
        overlay = pygame.Surface((game.botao_pressionado.width, game.botao_pressionado.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 110))
        game.screen.blit(overlay, game.botao_pressionado.topleft)
        pygame.draw.rect(game.screen, (255, 255, 255), game.botao_pressionado.move(2, 2), 2)
    else:
        game.botao_pressionado = None
        for rect in botoes_controle:
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(game.screen, (220, 220, 220), rect, 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            game.som_clique.play()
            game.estado = "opções"
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for rect in botoes_controle:
                if rect.collidepoint(event.pos):
                    game.botao_pressionado = rect
                    game.som_clique.play()
                    break
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if game.botao_pressionado is not None and game.botao_pressionado.collidepoint(event.pos):
                if game.botao_pressionado == rect_teclado:
                    game.estado = "teclado"
                elif game.botao_pressionado == rect_mouse:
                    game.estado = "mouse"
            game.botao_pressionado = None

    pygame.display.flip()


# para tela de game over com opções de continuar ou voltar ao menu
def tela_game_over(game):
    game.screen.fill((0, 0, 0))
    font_titulo = pygame.font.SysFont("arial", 30)
    t1 = font_titulo.render("Game Over", True, (255, 255, 255))
    t2 = game.font.render("ENTER: tentar de novo   |   ESC: menu", True, (200, 200, 200))
    game.screen.blit(t1, (SCREEN_WIDTH // 2 - t1.get_width() // 2, 250))
    game.screen.blit(t2, (SCREEN_WIDTH // 2 - t2.get_width() // 2, 310))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game.reiniciar_partida()
            elif event.key == pygame.K_ESCAPE:
                game.estado = "menu"

    pygame.display.flip()
    game.clock.tick(FPS)

