from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SIZE, ENEMY_SIZE,
    WORLD_LIGHT, WORLD_SHADOW
)
from classes.game_object import Platform
from classes.hazard import Hazard
from classes.enemy import Enemy


def get_level_1():
    ground_height = 60
    ground_y = SCREEN_HEIGHT - ground_height  # y = 660 (alinha com a grama da arte)

    # Nasce no canto esquerdo, em cima do chão
    player_spawn = (130, ground_y - PLAYER_SIZE)

    platforms = [
        # --- CHÃO PRINCIPAL (Neutro: aparece na Luz e na Sombra) ---
        Platform(0, ground_y, SCREEN_WIDTH, ground_height, world=None),

        # --- MUNDO DA LUZ ---
        # 1. Barranco baixo esquerdo (encaixa na pedra da arte)
        Platform(190, 560, 145, 100, world=WORLD_LIGHT),
        # 2. Barranco alto esquerdo (canto superior esquerdo da arte - bom para cristal)
        Platform(0, 445, 110, 215, world=WORLD_LIGHT),
        # 3. Ilha flutuante centro-esquerda
        Platform(430, 465, 160, 28, world=WORLD_LIGHT),
        # 4. Ilha flutuante centro-direita (ponto mais alto da fase)
        Platform(760, 320, 170, 28, world=WORLD_LIGHT),

        # --- MUNDO DA SOMBRA ---
        # 5. Ponte flutuante central (liga as duas ilhas de Luz)
        Platform(590, 390, 150, 28, world=WORLD_SHADOW),
        # 6. Plataforma flutuante direita
        Platform(970, 430, 150, 28, world=WORLD_SHADOW),
        # 7. Barranco baixo direito (encaixa na pedra da área roxa da arte)
        Platform(1095, 555, 185, 105, world=WORLD_SHADOW),
    ]

    collectibles = []

    enemies = [
        # Espinho da Luz no chão central (obriga a subir pelas plataformas ou trocar pra Sombra)
        Hazard(500, ground_y - 20, 48, 20, world=WORLD_LIGHT),
        # Espinho da Sombra no chão centro-direito
        Hazard(820, ground_y - 20, 48, 20, world=WORLD_SHADOW),

        # Inimigo da Luz patrulhando o chão do meio
        Enemy(380, ground_y - ENEMY_SIZE, 350, 680, world=WORLD_LIGHT),
        # Inimigo da Sombra patrulhando o chão da direita (antes do barranco)
        Enemy(900, ground_y - ENEMY_SIZE, 720, 1070, world=WORLD_SHADOW),
    ]

    return {
        "name": "Floresta dos Elfos",
        "player_spawn": player_spawn,
        "platforms": platforms,
        "collectibles": collectibles,
        "enemies": enemies,
    }