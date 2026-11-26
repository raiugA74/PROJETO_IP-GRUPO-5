# teste da minha parte (sprite do jogador, som de coletar e o retângulo quando falta imagem) - Thiago
# não faz parte do jogo, é só pra testar
# rodar: python demo_thiago.py
# A/D ou setas = andar, ESPAÇO = trocar de mundo, ESC = sair
import pygame
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WORLD_LIGHT, WORLD_SHADOW,
                       BG_LIGHT, BG_SHADOW, PLAYER_LIGHT, PLAYER_SHADOW, PLAYER_SIZE, PLAYER_SPEED)
from classes.sprite_sheet import PlayerAnimator
from audio import AudioManager


class JogadorTeste:
    # jogador simples só pro teste, tem rect e color igual o Player

    def __init__(self):
        self.rect = pygame.Rect(100, SCREEN_HEIGHT - 60 - PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)
        self.color = PLAYER_LIGHT

    def move(self, teclas):
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


def criar_itens():
    # quadrados amarelos no chão pra testar o som de coletar
    itens = []
    for x in [250, 400, 550, 700]:
        itens.append(pygame.Rect(x, SCREEN_HEIGHT - 60 - 24, 24, 24))
    return itens


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Teste - Thiago")
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont("arial", 18)

    jogador = JogadorTeste()
    animador = PlayerAnimator()
    audio = AudioManager()
    itens = criar_itens()
    mundo = WORLD_LIGHT
    coletados = 0

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                if evento.key == pygame.K_SPACE:  # troca de mundo
                    if mundo == WORLD_LIGHT:
                        mundo = WORLD_SHADOW
                    else:
                        mundo = WORLD_LIGHT

        jogador.move(pygame.key.get_pressed())
        if mundo == WORLD_LIGHT:
            jogador.color = PLAYER_LIGHT
        else:
            jogador.color = PLAYER_SHADOW
        animador.update(jogador, mundo)

        # pegou o item: tira da lista e toca o som
        for item in itens[:]:
            if jogador.rect.colliderect(item):
                itens.remove(item)
                coletados += 1
                audio.play("coletar")
        if len(itens) == 0:
            itens = criar_itens()

        if mundo == WORLD_LIGHT:
            screen.fill(BG_LIGHT)
            cor_texto = (40, 30, 60)
        else:
            screen.fill(BG_SHADOW)
            cor_texto = (240, 236, 255)
        pygame.draw.rect(screen, (120, 90, 60), (0, SCREEN_HEIGHT - 60, SCREEN_WIDTH, 60))  # chão
        for item in itens:
            pygame.draw.rect(screen, (255, 210, 80), item)
        animador.draw(screen, jogador)
        texto = fonte.render("Coletados: " + str(coletados) + "   |   A/D andar, ESPAÇO trocar mundo", True, cor_texto)
        screen.blit(texto, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
