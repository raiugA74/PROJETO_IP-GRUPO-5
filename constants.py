SCREEN_WIDTH = 1280     # tamanho da tela, fps e nome do jogo.
SCREEN_HEIGHT = 720
FPS = 60
WINDOW_TITLE = "One Vessel"

PLAYER_SIZE = 32
PLAYER_SPEED = 5                 # tamanho do player/velocidade/cor
PLAYER_COLOR = (240, 240, 240)
PLAYER_LIVES = 3   # quantidade de vidas
INVULN_FRAMES = 60   # 1 segundo sem levar dano depois de ser atingido // Agora passa a ser 1 segundo sem levar dano após o respawn
# Cores do personagem em cada mundo (para contrastar com o fundo)
PLAYER_LIGHT = (58, 46, 84)     # Jogador escuro no mundo claro (Luz)
PLAYER_SHADOW = (238, 240, 255) # Jogador claro/branco no mundo escuro (Sombra)

GRAVITY = 1      # quanto a velocidade de queda aumenta por quadro
JUMP_FORCE = -16     # velocidade inicial do pulo (negativo = para cima)
MAX_FALL_SPEED = 15   # limite da velocidade de queda
JUMP_CUT = 0.5  

COLLECTIBLE_SIZE = 24
COLLECTIBLES_PER_TYPE = 5      # dimensoes dos coletaveis
SPAWN_MARGIN = 20

BACKGROUND_COLOR = (20, 20, 40)
TEXT_COLOR = (255, 255, 255)
SCOREBOARD_FONT_SIZE = 22       #features do cenário 
SCOREBOARD_LINE_HEIGHT = 26

# Para saber em qual mundo o jogador está
WORLD_LIGHT = "light"   # Representa o mundo da Luz
WORLD_SHADOW = "shadow" # Representa o mundo da Sombra

# Cores de fundo bg = background
BG_LIGHT = (255, 224, 178)  # Cor de fundo quente (bege/laranja claro) para o mundo da Luz
BG_SHADOW = (32, 18, 66)    # Cor de fundo escura (roxo profundo) para o mundo da Sombra

# Cores das plataformas por mundo
PLAT_LIGHT = (172, 118, 66)        # Marrom para plataforma sólida na Luz
PLAT_SHADOW = (88, 74, 168)        # Roxo para plataforma sólida na Sombra

# Inimigos e obstáculos
HAZARD_COLOR = (200, 40, 40)          # cor do espinho quando está ativo
HAZARD_GHOST_COLOR = (230, 150, 150)  # contorno do espinho quando é do outro mundo
ENEMY_COLOR = (160, 30, 30)           # cor do inimigo
ENEMY_SPEED = 2                       # quantos pixels o inimigo anda por quadro
ENEMY_SIZE = 32                       # tamanho do inimigo (quadrado)

LEVEL_WIDTH = 3000          # largura da fase em pixels (ajuste para a camera seguir o player)
LEVEL_HEIGHT = SCREEN_HEIGHT