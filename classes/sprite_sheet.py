"""
Sprites do jogador (Pessoa 7 - Semana 1).

- SpriteSheet: recorta os quadros de uma imagem com vários quadros lado a lado
- Animation: troca de quadro no tempo certo
- PlayerAnimator: mostra o jogador parado ou andando, no mundo da Luz ou da Sombra
- draw_image_or_rect: se a imagem não carregar, desenha o retângulo de sempre (fallback)
"""
import pygame

PASTA_IMAGENS = "assets/images/"


def load_image(caminho):
    """Carrega uma imagem. Se não conseguir, avisa e devolve None."""
    try:
        imagem = pygame.image.load(caminho)
        return imagem
    except (pygame.error, FileNotFoundError):
        print("Imagem não encontrada:", caminho)
        return None


def draw_image_or_rect(screen, imagem, rect, cor, flip=False):
    """Desenha a imagem com os pés na base do rect. Sem imagem, desenha o retângulo."""
    if imagem is None:
        pygame.draw.rect(screen, cor, rect)
        return
    if flip:
        imagem = pygame.transform.flip(imagem, True, False)  # espelha para olhar para a esquerda
    x = rect.centerx - imagem.get_width() // 2
    y = rect.bottom - imagem.get_height()
    screen.blit(imagem, (x, y))


class SpriteSheet:
    """Uma imagem com vários quadros do mesmo tamanho, um do lado do outro."""

    def __init__(self, caminho, largura_quadro, altura_quadro):
        self.imagem = load_image(caminho)
        self.largura_quadro = largura_quadro
        self.altura_quadro = altura_quadro

    def get_frame(self, coluna, linha):
        """Recorta um quadro da folha."""
        if self.imagem is None:
            return None
        quadro = pygame.Surface((self.largura_quadro, self.altura_quadro), pygame.SRCALPHA)
        x = coluna * self.largura_quadro
        y = linha * self.altura_quadro
        area = pygame.Rect(x, y, self.largura_quadro, self.altura_quadro)
        quadro.blit(self.imagem, (0, 0), area)  # copia só a área do quadro
        return quadro

    def get_row(self, linha, quantidade):
        """Recorta os quadros de uma linha (uma animação)."""
        quadros = []
        if self.imagem is None:
            return quadros
        for coluna in range(quantidade):
            quadros.append(self.get_frame(coluna, linha))
        return quadros


class Animation:
    """Troca de quadro a cada 'velocidade' quadros do jogo (o jogo roda a 60 por segundo)."""

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
            if self.indice >= len(self.quadros):  # chegou no fim: volta para o começo
                self.indice = 0

    def reset(self):
        self.indice = 0
        self.contador = 0

    def get_image(self):
        if len(self.quadros) == 0:
            return None
        return self.quadros[self.indice]


class PlayerAnimator:
    """
    Mostra o jogador parado ou andando, sem precisar mudar a classe Player.
    Usa só o que o Player já tem: rect e color.

    Folha de sprites (32x32 cada quadro):
        linha 0 = parado (4 quadros)
        linha 1 = andando (6 quadros)
    jogador_luz.png    -> mundo da Luz (lâmpada apagada)
    jogador_sombra.png -> mundo da Sombra (lâmpada acesa)
    """

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

        # descobre se andou e para qual lado, comparando com o quadro anterior
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

        if novo_estado != self.estado:  # mudou de estado: começa a animação do início
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
