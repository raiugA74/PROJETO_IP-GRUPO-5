from levels.data import get_level_1


class Level:
    def __init__(self, level_number=1):
        self.level_number = level_number

        if level_number == 1:
            data = get_level_1()
        else:
            data = get_level_1()  # Depois adicionamos get_level_2() e get_level_3()

        self.name = data["name"]
        self.player_spawn = data["player_spawn"]
        self.platforms = data["platforms"]
        self.collectibles = data["collectibles"]
        self.enemies = data["enemies"]

    def is_completed(self):
        # A fase termina quando todos os coletáveis forem recolhidos
        if len(self.collectibles) == 0:
            return True
        else:
            return False

    def draw(self, screen, current_world):
        for platform in self.platforms:
            platform.draw(screen, current_world)
