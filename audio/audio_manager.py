# sons do jogo - Thiago
import pygame

PASTA_SONS = "assets/sounds/"

# nome do som : arquivo dentro de assets/sounds
# pra colocar um som novo é só botar o arquivo na pasta e adicionar aqui
SONS = {
    "coletar": "coletar.wav",
}


class AudioManager:
    def __init__(self, volume=0.5):
        self.sons = {}
        self.ligado = True
        try:
            pygame.mixer.init()
        except pygame.error:
            print("Sem placa de som: o jogo vai rodar sem áudio.")  # o jogo continua mesmo sem som
            self.ligado = False
        if self.ligado:
            for nome in SONS:
                self.sons[nome] = self.carregar_som(PASTA_SONS + SONS[nome], volume)

    def carregar_som(self, caminho, volume):
        try:
            som = pygame.mixer.Sound(caminho)
            som.set_volume(volume)
            return som
        except (pygame.error, FileNotFoundError):
            print("Som não encontrado:", caminho)
            return None

    def play(self, nome):
        # ex: audio.play("coletar")
        if nome in self.sons and self.sons[nome] is not None:
            self.sons[nome].play()
