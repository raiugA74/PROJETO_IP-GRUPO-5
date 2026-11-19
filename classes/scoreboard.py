class Scoreboard:
    """Conta quantos itens de cada tipo foram coletados."""

    def __init__(self):
        self.counts = {"coletavel1": 0, "coletavel2": 0, "coletavel3": 0}  # dicionarios dos coletaveis

    def add(self, type_name):   # conta a quantidade de coletaveis somando 1 ao que foi coletado
        self.counts[type_name] += 1

    def draw(self, screen, font):    # mostra os coletaveis na tela   # Escreve uma linha por tipo, de cima para baixo, no canto da tela.
        y = 10
        for name, amount in self.counts.items():
            text = font.render(f"{name}: {amount}", True, (255, 255, 255))
            screen.blit(text, (10, y))
            y += 26