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
        # --- CHÃO PRINCIPAL (Aparece na Luz e na Sombra) ---
        Platform(0, ground_y, SCREEN_WIDTH, ground_height, world=None),

        # MUNDO DA LUZ 
        # 1. Barranco baixo esquerdo (encaixa na pedra da arte)
        Platform(190, 560, 145, 100, world=WORLD_LIGHT),
        # 2. Barranco alto esquerdo (canto superior esquerdo - bom para cristal difícil)
        Platform(0, 445, 110, 215, world=WORLD_LIGHT),
        # 3. Ilha flutuante centro-esquerda (livre de inimigo para dar impulso no pulo)
        Platform(415, 470, 130, 28, world=WORLD_LIGHT),
        # 4. Ilha flutuante centro-direita (ponto mais alto da fase)
        Platform(770, 315, 135, 28, world=WORLD_LIGHT),
        # 5. Degrau alto direito (obriga troca Luz -> Sombra para alcançar a plataforma 7)
        Platform(1010, 365, 115, 28, world=WORLD_LIGHT),

        # MUNDO DA SOMBRA 
        # 6. Ponte flutuante central (liga as duas ilhas de Luz)
        Platform(590, 390, 130, 28, world=WORLD_SHADOW),
        # 7. Plataforma flutuante direita (ponto intermediário com bom espaço de pouso)
        Platform(910, 460, 130, 28, world=WORLD_SHADOW),
        # 8. Barranco baixo direito (encaixa na pedra da área roxa da arte)
        Platform(1095, 555, 185, 105, world=WORLD_SHADOW),
    ]

    collectibles = []

    enemies = [
        #     ESPINHOS NO CHÃO (Espaçados para dar área segura entre eles) 
        Hazard(450, ground_y - 20, 48, 20, world=WORLD_LIGHT),
        Hazard(640, ground_y - 20, 48, 20, world=WORLD_SHADOW),
        Hazard(810, ground_y - 20, 48, 20, world=WORLD_LIGHT),

        #     ESPINHOS EM PLATAFORMAS (Posicionados no fundo, deixando a entrada livre) 
        # Espinho na ponta direita da ilha mais alta (deixa 95px livres à esquerda para pousar)
        Hazard(865, 315 - 20, 36, 20, world=WORLD_LIGHT),
        # Espinho bem no canto direito do barranco roxo (deixa 130px livres na entrada)
        Hazard(1225, 555 - 20, 45, 20, world=WORLD_SHADOW),

        #     INIMIGOS DE PATRULHA (Apenas no chão, com rotas amplas) 
        # Patrulha da Luz no chão central
        Enemy(370, ground_y - ENEMY_SIZE, 345, 730, world=WORLD_LIGHT),
        # Patrulha da Sombra no chão centro-direito (para antes do barranco)
        Enemy(750, ground_y - ENEMY_SIZE, 700, 1065, world=WORLD_SHADOW),
    ]

    return {
        "name": "Floresta dos Elfos",
        "player_spawn": player_spawn,
        "platforms": platforms,
        "collectibles": collectibles,
        "enemies": enemies,
    }