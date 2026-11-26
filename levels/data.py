from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SIZE,
    WORLD_LIGHT, WORLD_SHADOW
)
from classes.game_object import Platform


def get_level_1():
    ground_height = 40
    ground_y = SCREEN_HEIGHT - ground_height

    # Nasce no canto esquerdo, exatamente em cima do chão
    player_spawn = (50, ground_y - PLAYER_SIZE)

    platforms = [
        # Chão principal (existe nos dois mundos)
        Platform(0, ground_y, SCREEN_WIDTH, ground_height, world=None),

        # Degraus alcançáveis alternando Luz e Sombra
        Platform(int(SCREEN_WIDTH * 0.22), ground_y - 80, 140, 20, world=WORLD_LIGHT),
        Platform(int(SCREEN_WIDTH * 0.46), ground_y - 160, 140, 20, world=WORLD_SHADOW),
        Platform(int(SCREEN_WIDTH * 0.70), ground_y - 240, 150, 20, world=WORLD_LIGHT),
    ]

    # Listas prontas para pessoa dos coletáveis e pessoa dos inimigos preencherem
    collectibles = []
    enemies = []

    return {
        "name": "Floresta dos Elfos",
        "player_spawn": player_spawn,
        "platforms": platforms,
        "collectibles": collectibles,
        "enemies": enemies,
    }