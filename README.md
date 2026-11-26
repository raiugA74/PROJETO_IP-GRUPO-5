# PROJETO_IP-GRUPO-5
# One Vessel

Jogo de plataforma 2D desenvolvido em Python com **PyGame** e **Programação Orientada a Objetos (POO)** para a disciplina de Introdução à Programação (CIn - UFPE).

## Sobre o Jogo

Em **One Vessel**, o jogador atravessa diferentes regiões alternando em tempo real entre dois planos — o **Mundo da Luz** e o **Mundo da Sombra**. Plataformas e desafios mudam de estado conforme o plano ativo, exigindo raciocínio e precisão para coletar os ingredientes necessários em cada fase antes do confronto final no castelo.

## Mecânicas Principais

* **Alternância de Mundos (Luz e Sombra):** Ao pressionar `ESPAÇO`, o cenário alterna entre o Mundo da Luz e o Mundo da Sombra. Plataformas exclusivas de um plano tornam-se sólidas apenas quando aquele mundo está ativo, aparecendo como contornos ("fantasmas") no plano oposto.
* **Física e Movimentação:** Movimentação lateral, gravidade contínua e pulo com altura variável (soltar a tecla de pulo interrompe a subida mais cedo).
* **Sistema de Coletáveis e Placar:** Três tipos distintos de itens coletáveis contabilizados em tempo real na tela.
* **Progressão por Fases:** Estrutura modular que carrega mapas, pontos de spawn, plataformas, coletáveis e inimigos de forma independente para cada fase.

## Controles

| Tecla | Ação |
| :--- | :--- |
| `A` / `D` ou `←` / `→` | Mover para a esquerda / direita |
| `W` ou `↑` | Pular (segure para pular mais alto) |
| `ESPAÇO` | Alternar entre Mundo da Luz e Mundo da Sombra |
| `ESC` | Pausar / Voltar ao menu |
