import json
import os

from constants import PLAYER_LIVES


def salvar_jogo(g):
    os.makedirs("save", exist_ok=True)
    with open("save/save.json", "w", encoding="utf-8") as f:
        json.dump({
            "player_x": g.player.rect.x,
            "player_y": g.player.rect.y,
            "current_world": g.current_world,
            "scores": g.scoreboard.counts,
            "vidas": g.vidas,
            "hits": g.hits
        }, f)


def carregar_jogo(g):
    if os.path.exists("save/save.json"): # verifica se o arquivo de save existe
        with open("save/save.json", "r") as f: # abre o arquivo de save
            save_data = json.load(f) # carrega os dados do save
            g.player.rect.x = save_data["player_x"] # atualiza a posição do jogador
            g.player.rect.y = save_data["player_y"] # atualiza a posição do jogador
            g.current_world = save_data["current_world"] # atualiza o mundo atual
            g.scoreboard.counts = save_data["scores"] # atualiza os pontos
            g.vidas = save_data.get("vidas", PLAYER_LIVES) # saves antigos não têm vidas
            g.hits = save_data.get("hits", 0)
            g.hit_timer = 0
        g.estado = "jogo"
