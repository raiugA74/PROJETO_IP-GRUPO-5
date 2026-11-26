from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SIZE, ENEMY_SIZE,
    WORLD_LIGHT, WORLD_SHADOW
)
from classes.game_object import Platform
from classes.hazard import Hazard
from classes.enemy import Enemy

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

    enemies = [
        # espinho que só existe na Luz, parado no chão
        Hazard(int(SCREEN_WIDTH * 0.34), ground_y - 20, 40, 20, world=WORLD_LIGHT),
        # espinho que só existe na Sombra, parado no chão
        Hazard(int(SCREEN_WIDTH * 0.58), ground_y - 20, 40, 20, world=WORLD_SHADOW),
        # inimigo da Luz patrulhando perto do começo da fase
        Enemy(int(SCREEN_WIDTH * 0.10), ground_y - ENEMY_SIZE,
              int(SCREEN_WIDTH * 0.08), int(SCREEN_WIDTH * 0.20), world=WORLD_LIGHT),
        # inimigo da Sombra patrulhando no fim da fase
        Enemy(int(SCREEN_WIDTH * 0.80), ground_y - ENEMY_SIZE,
              int(SCREEN_WIDTH * 0.75), int(SCREEN_WIDTH * 0.92), world=WORLD_SHADOW),]

    return {
        "name": "Floresta dos Elfos",
        "player_spawn": player_spawn,
        "platforms": platforms,
        "collectibles": collectibles,
        "enemies": enemies,
    }