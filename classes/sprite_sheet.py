# sprites e animação do jogador - Thiago
import pygame

PASTA_IMAGENS = "assets/images/"


def load_image(caminho):
    # tenta carregar a imagem, se não achar o arquivo retorna None
    try:
        imagem = pygame.image.load(caminho)
        return imagem
    except (pygame.error, FileNotFoundError):
        print("Imagem não encontrada:", caminho)
        return None


def draw_image_or_rect(screen, imagem, rect, cor, flip=False):
    # se a imagem não carregou desenha o retângulo normal, assim o jogo não quebra
    if imagem is None:
        pygame.draw.rect(screen, cor, rect)
        return
    if flip:
        imagem = pygame.transform.flip(imagem, True, False)  # vira a imagem pra esquerda
    # centraliza a imagem no rect e deixa os pés embaixo
    x = rect.centerx - imagem.get_width() // 2
    y = rect.bottom - imagem.get_height()
    screen.blit(imagem, (x, y))


class SpriteSheet:
    # imagem com vários quadros um do lado do outro

    def __init__(self, caminho, largura_quadro, altura_quadro):
        self.imagem = load_image(caminho)
        self.largura_quadro = largura_quadro
        self.altura_quadro = altura_quadro

    def get_frame(self, coluna, linha):
        # recorta um quadro da imagem
        if self.imagem is None:
            return None
        quadro = pygame.Surface((self.largura_quadro, self.altura_quadro), pygame.SRCALPHA)
        x = coluna * self.largura_quadro
        y = linha * self.altura_quadro
        area = pygame.Rect(x, y, self.largura_quadro, self.altura_quadro)
        quadro.blit(self.imagem, (0, 0), area)
        return quadro

    def get_row(self, linha, quantidade):
        # pega todos os quadros de uma linha (cada linha é uma animação)
        quadros = []
        if self.imagem is None:
            return quadros
        for coluna in range(quantidade):
            quadros.append(self.get_frame(coluna, linha))
        return quadros


class Animation:
    # troca o quadro a cada "velocidade" frames do jogo

    def __init__(self, quadros, velocidade):
        self.quadros = quadros
        self.velocidade = velocidade
        self.indice = 0
        self.contador = 0

    def update(self):
        if len(self.quadros) == 0:
            return
        self.contador += 1
        if self.contador >= self.velocidade:
            self.contador = 0
            self.indice += 1
            if self.indice >= len(self.quadros):  # acabou, volta pro primeiro
                self.indice = 0

    def reset(self):
        self.indice = 0
        self.contador = 0

    def get_image(self):
        if len(self.quadros) == 0:
            return None
        return self.quadros[self.indice]


class PlayerAnimator:
    # cuida da animação do jogador (parado/andando) sem mexer na classe Player
    # jogador_luz.png = lâmpada apagada (mundo da luz)
    # jogador_sombra.png = lâmpada acesa (mundo da sombra)
    # linha 0 da imagem = parado, linha 1 = andando, cada quadro tem 32x32

    def __init__(self):
        folha_luz = SpriteSheet(PASTA_IMAGENS + "player/jogador_luz.png", 32, 32)
        folha_sombra = SpriteSheet(PASTA_IMAGENS + "player/jogador_sombra.png", 32, 32)
        self.animacoes_luz = self.criar_animacoes(folha_luz)
        self.animacoes_sombra = self.criar_animacoes(folha_sombra)
        self.estado = "parado"
        self.olhando_esquerda = False
        self.ultimo_x = None
        self.mundo = "light"

    def criar_animacoes(self, folha):
        animacoes = {}
        animacoes["parado"] = Animation(folha.get_row(0, 4), 10)
        animacoes["andando"] = Animation(folha.get_row(1, 6), 5)
        return animacoes

    def update(self, player, mundo_atual):
        self.mundo = mundo_atual

        # compara com a posição do frame anterior pra saber se andou
        movimento = 0
        if self.ultimo_x is not None:
            movimento = player.rect.x - self.ultimo_x
        self.ultimo_x = player.rect.x
        if movimento < 0:
            self.olhando_esquerda = True
        if movimento > 0:
            self.olhando_esquerda = False

        if movimento != 0:
            novo_estado = "andando"
        else:
            novo_estado = "parado"

        # se mudou de parado pra andando (ou o contrário) começa a animação do zero
        if novo_estado != self.estado:
            self.estado = novo_estado
            self.animacoes_luz[novo_estado].reset()
            self.animacoes_sombra[novo_estado].reset()

        self.animacoes_luz[self.estado].update()
        self.animacoes_sombra[self.estado].update()

    def draw(self, screen, player):
        if self.mundo == "shadow":
            animacao = self.animacoes_sombra[self.estado]
        else:
            animacao = self.animacoes_luz[self.estado]
        draw_image_or_rect(screen, animacao.get_image(), player.rect, player.color, self.olhando_esquerda)
