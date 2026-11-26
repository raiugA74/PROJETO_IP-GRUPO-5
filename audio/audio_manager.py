"""
Sons do One Vessel (Pessoa 7 - Semana 1).

Uso:
    audio = AudioManager()      # crie depois do pygame.init()
    audio.play("coletar")       # quando o jogador pegar um item

Se não tiver placa de som ou faltar o arquivo, o jogo continua sem o som.
Novos sons: é só colocar o arquivo em assets/sounds/ e adicionar no dicionário SONS.
"""
import pygame

PASTA_SONS = "assets/sounds/"

SONS = {  # nome usado no código: arquivo em assets/sounds/
    "coletar": "coletar.wav",
}


class AudioManager:
    def __init__(self, volume=0.5):
        self.sons = {}
        self.ligado = True
        try:
            pygame.mixer.init()
        except pygame.error:
            print("Sem placa de som: o jogo vai rodar sem áudio.")
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
        """Toca um som pelo nome (veja o dicionário SONS)."""
        if nome in self.sons and self.sons[nome] is not None:
            self.sons[nome].play()
