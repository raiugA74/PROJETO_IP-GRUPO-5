from constants import SCREEN_WIDTH, SCREEN_HEIGHT, LEVEL_WIDTH, LEVEL_HEIGHT

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self, alvo_rect, suave=True):
        alvo_x = alvo_rect.centerx - SCREEN_WIDTH // 2    # deixar o player no centro da tela enquanto esiver em movimento
        alvo_y = alvo_rect.centery - SCREEN_HEIGHT // 2

        if suave:
            self.x += (alvo_x - self.x) * 0.1
            self.y += (alvo_y - self.y) * 0.1
        else:
            self.x, self.y = alvo_x, alvo_y   # pula direto (respawn / carregar save)

        self.x = max(0, min(self.x, LEVEL_WIDTH - SCREEN_WIDTH))
        self.y = max(0, min(self.y, LEVEL_HEIGHT - SCREEN_HEIGHT))