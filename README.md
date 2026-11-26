# PROJETO_IP-GRUPO-5
# One Vessel

Jogo de plataforma 2D desenvolvido em Python com **PyGame** e **Programação Orientada a Objetos (POO)** para a disciplina de Introdução à Programação (CIn - UFPE).

## Sobre o Jogo

Em **One Vessel**, o jogador atravessa diferentes regiões alternando em tempo real entre dois planos — o **Mundo da Luz** e o **Mundo da Sombra**. Plataformas, inimigos e obstáculos existem apenas em seus respectivos planos, exigindo memória, raciocínio e precisão para coletar os ingredientes necessários em cada fase.

## Mecânicas Principais

- **Alternância de Mundos (Luz e Sombra):** Ao pressionar `ESPAÇO`, o cenário alterna entre o Mundo da Luz e o Mundo da Sombra. Plataformas, espinhos e inimigos exclusivos de um plano tornam-se visíveis e ativos apenas quando aquele mundo está em vigor, permanecendo ocultos e intangíveis no plano oposto.
- **Física e Movimentação:** Movimentação lateral, gravidade contínua e pulo com altura variável (soltar a tecla de pulo interrompe a subida mais cedo).
- **Sistema de Coletáveis e Placar:** Três tipos distintos de itens coletáveis contabilizados em tempo real na tela.
- **Progressão por Fases:** Estrutura modular que carrega mapas, pontos de spawn, plataformas, coletáveis e inimigos de forma independente para cada fase.

## Controles

| Tecla | Ação |
| :--- | :--- |
| `A` / `D` ou `←` / `→` | Mover para a esquerda / direita |
| `W` ou `↑` | Pular (segure para pular mais alto) |
| `ESPAÇO` | Alternar entre Mundo da Luz e Mundo da Sombra |
| `ESC` | Pausar / Voltar ao menu |

## Equipe e Responsabilidades

| Integrante | Módulo / Função | Atividades no Projeto |
| :--- | :--- | :--- |
| **Luiz Henrique** | Núcleo e Integração | Loop principal (`main.py`), máquina de estados do jogo, alternância de planos e integração geral dos módulos. |
| **Lucas Monteraso** | Jogador (`Player`) | Física de movimento, gravidade, pulo com altura variável, colisão com plataformas, sistema de vidas e revisão de PRs. |
| **Lucas Aguiar** | Fases, Plataformas e Level Design | Arquitetura das fases (`Level` e `levels/data.py`), plataformas (`game_object.py`), layout de mapas e revisão de PRs. |
| **Felipe Borges** | Coletáveis e Placar | Lógica dos itens coletáveis (cristais de Luz/Sombra e pó de penumbra), detecção de coleta e placar (`Scoreboard`). |
| **Kaike Silva** | Inimigos e Obstáculos | Inimigos com patrulha (`Enemy`), espinhos/armadilhas (`Hazard`), visibilidade por mundo e detecção de dano. |
| **Juan Henrique** | Menus e Narrativa | Interface do menu inicial e opções, persistência de configurações (`save.json`) e narrativa/ambientação do jogo. |
| **Tiago Cardoso** | Sprites, Áudio e Efeitos | Animações do personagem (`PlayerAnimator` e `SpriteSheet`), artes de cenário/interface e efeitos sonoros (`AudioManager`). |