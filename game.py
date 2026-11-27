import pygame

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
import menu
from save_manager import salvar_jogo


class Game:
    def __init__(self):
        pygame.init()  # liga o PyGame e inicia o jogo
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # cria a janela
        pygame.display.set_caption(WINDOW_TITLE) # define o título da janela
        self.clock = pygame.time.Clock()  # controla a velocidade do jogo

        self.som_clique = pygame.mixer.Sound("assets/sounds/click.wav")  # carrega o som de clique
        self.som_clique.set_volume(0.5) # define o volume do som de clique (0.0 a 1.0)

        self.volume_atual = 0.5  # <-- variáveis do áudio fora do while
        self.mudo = False

        self.level = Level(1)  # carrega a Fase 1
        spawn_x, spawn_y = self.level.player_spawn
        self.player = Player(spawn_x, spawn_y)  # cria o jogador no canto esquerdo sobre o chão
        self.animador = PlayerAnimator()        # sprite do jogador (parado/andando)
        self.audio = AudioManager()             # gerenciador de sons

        self.current_world = WORLD_LIGHT  # começa no mundo da Luz

        self.font = pygame.font.SysFont("arial", 22)  # fonte do placar
        self.scoreboard = Scoreboard()                # placar com a contagem por tipo

        self.estado = "menu"         # menu do jogo
        self.menu_image = pygame.image.load("assets/images/menu.png") #  carrega a imagem do menu
        self.opções_image = pygame.image.load("assets/images/opções.png") # carrega a imagem da tela de opções
        self.controle_image = pygame.image.load("assets/images/controle.png") # carrega a imagem da tela de controle
        self.som_image = pygame.image.load("assets/images/som.png") # carrega a imagem da tela de som

        self.rect_novo_jogo = pygame.Rect(550, 505, 181, 37) # cria retângulos para os botões do menu
        self.rect_continuar = pygame.Rect(545, 552, 190, 31) # define a posição e tamanho dos botões do menu
        self.rect_opcoes = pygame.Rect(577, 595, 125, 38) # define a posição e tamanho dos botões do menu
        self.rect_sair = pygame.Rect(602, 643, 78, 30) # define a posição e tamanho dos botões do menu

        self.botoes_menu = [self.rect_novo_jogo, self.rect_continuar, self.rect_opcoes, self.rect_sair]
        self.botao_pressionado = None  # botão que está sendo pressionado no momento

        self.hits = 0        # quantas vezes o jogador tomou dano (contador de teste)
        self.hit_timer = 0   # cronômetro pra não contar dano 60 vezes por segundo

        self.vidas = PLAYER_LIVES                # vidas restantes
        self.respawn_point = self.level.player_spawn  # onde o jogador renasce

        self.particulas_menu = []  # cada item: [x, y, vx, vy, alpha]

        self.running = True

    def aplicar_audio(self):  # <-- função definida fora e antes do while
        volume_efetivo = 0.0 if self.mudo else self.volume_atual
        self.som_clique.set_volume(volume_efetivo)
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(volume_efetivo)

    def respawnar(self):
        # leva o jogador de volta ao ponto de respawn, sem perder o progresso
        self.player.rect.x, self.player.rect.y = self.respawn_point
        self.player.vel_y = 0                  # zera a velocidade de queda
        self.current_world = WORLD_LIGHT       # volta ao mundo da Luz
        self.hit_timer = INVULN_FRAMES         # invulnerável por um tempo logo após renascer
        self.animador.olhando_esquerda = False # renasce olhando para a direita, no sentido da fase até então
        self.animador.ultimo_x = self.player.rect.x # o teleporte não conta como "andou para a esquerda"

    def reiniciar_partida(self):
        # começa tudo do zero: vidas, danos e posição
        self.vidas = PLAYER_LIVES
        self.hits = 0
        self.respawn_point = self.level.player_spawn
        self.respawnar()
        self.estado = "jogo"

    def run(self):
        while self.running:  # loop principal: repete até fechar a janela

            if self.estado == "menu":
                menu.tela_menu(self)

            elif self.estado == "opções":
                menu.tela_opcoes(self)

            elif self.estado == "som":
                menu.tela_som(self)

            elif self.estado == "controle":
                menu.tela_controle(self)

            elif self.estado == "game_over":
                menu.tela_game_over(self)

            elif self.estado == "jogo":
                self.tela_jogo()

    def tela_jogo(self):
        # 1. Eventos: o que o jogador fez?
        for event in pygame.event.get(): # detecta eventos do jogo (teclado, mouse, etc.)
            if event.type == pygame.QUIT: # encerrar o jogo ao fechar a janela
                salvar_jogo(self)
                self.running = False
            if event.type == pygame.KEYDOWN: # detecta quando uma tecla é pressionada
                if event.key == pygame.K_SPACE:  # alterna o mundo ao apertar ESPAÇO
                    if self.current_world == WORLD_LIGHT: # se o mundo atual é o da Luz, muda para o da Sombra
                        self.current_world = WORLD_SHADOW # alterna para o mundo da Sombra
                    else:
                        self.current_world = WORLD_LIGHT # alterna para o mundo da Luz
                elif event.key == pygame.K_ESCAPE: # volta para o menu ao apertar ESC
                    self.som_clique.play()
                    self.estado_anterior = "jogo"
                    self.estado = "opções"

        # 2. Atualizar: movimento do jogador
        self.player.update(pygame.key.get_pressed(), self.level.platforms, self.current_world)

        for enemy in self.level.enemies:                 # passa por cada inimigo e espinho da fase
            enemy.update()                          # inimigo dá um passo (espinho não faz nada)

        if self.hit_timer > 0:                           # se ainda está no tempo de espera...
            self.hit_timer -= 1                          # ...diminui 1 por quadro (60 = 1 segundo)

        tocou = any(e.hits(self.player, self.current_world) for e in self.level.enemies)  # algo perigoso encostou?
        if tocou and self.hit_timer == 0:                # encostou e já passou o tempo de espera
            self.hits += 1                               # conta 1 dano/ PRECISA CONTAR DANO?
            self.vidas -= 1                              # perde 1 vida
            if self.vidas <= 0:
                self.estado = "game_over"                # fim de jogo quando acabarem as vidas
            else:
                self.respawnar()                         # volta ao ponto de respawn 

        # 3. Cor da tela e animação do jogador conforme o mundo
        if self.current_world == WORLD_LIGHT:
            bg_color = BG_LIGHT
            self.player.color = PLAYER_LIGHT
        else:
            bg_color = BG_SHADOW
            self.player.color = PLAYER_SHADOW

        self.animador.update(self.player, self.current_world)  # escolhe a animação (parado ou andando)

        # 4. Desenhar
        self.screen.fill(bg_color)
        self.level.draw(self.screen, self.current_world)       # desenha todas as plataformas da fase

        for enemy in self.level.enemies:             # desenha inimigos e espinhos
            enemy.draw(self.screen, self.current_world)

        if self.hit_timer == 0 or (self.hit_timer // 5) % 2 == 0:   # pisca enquanto está invulnerável
            self.animador.draw(self.screen, self.player)       # desenha a sprite do jogador (no lugar de player.draw)
        self.scoreboard.draw(self.screen, self.font)           # placar por cima de tudo

        texto_vidas = self.font.render(f"Vidas: {self.vidas}", True, (255, 255, 255)) #fica no canto direito como um contador númerico, mas penso que três corações possam representar melhor, não seigit add .
        self.screen.blit(texto_vidas, (SCREEN_WIDTH - 140, 10))

        pygame.display.flip()

        self.clock.tick(FPS)  # limita a 60 quadros por segundo
