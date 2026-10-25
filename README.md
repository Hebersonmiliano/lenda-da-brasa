# Lenda da Brasa

RPG de ação em pixel art no estilo Zelda clássico, ambientado no mundo de **Brasa Eterna**.
O Rei Umbra raptou a Princesa Lírian. Atravesse os reinos da **Brasa**, das **Marés** e dos **Ventos**,
conquiste os 3 cristais que libertam a **Espada dos Reinos** e depois busque os **8 Pendentes Celestiais**
que abrem o caminho até o Reino Sombrio.

**Jogar:** abra `index.html` no navegador (funciona com dois cliques, sem instalar nada)
ou jogue no [Portal Pixel](https://hebersonmiliano.github.io/portal-jogos/jogo.html?id=lenda-da-brasa).

![Capa](capa.png)

## O que já dá para jogar

- **Capítulos 1 a 3**: Reino da Brasa, Reino das Marés e Reino dos Ventos, cada um com mundo aberto, castelo e chefe.
- **Castelos com exploração de verdade** (52 salas no total), com mapa, bússola, chaves pequenas e chave mestra:
  - *Castelo da Brasa* (20 salas, térreo e subsolo): salas escuras, lava, orbes e pinos, Bastão de Brasa.
  - *Castelo das Marés* (16 salas): uma alavanca sobe e baixa a água de todo o castelo; Gancho.
  - *Castelo dos Ventos* (16 salas, 3 andares): pisos que desabam, correntes de vento, abismos; Pena.
- **Santuários** do Fogo e do Mar, com mini-chefes (Salamandra de Lava e Caranguejo Rei).
- Movimento e ataque em **8 direções**, menu de itens no formato Zelda SNES, música de cada área,
  **3 espaços de salvamento**, suporte a **controle** e a **toque** no celular.

## Controles

| Ação | Teclado | Controle |
|---|---|---|
| Mover | WASD / setas | Direcional ou analógico |
| Espada, falar, abrir | J / Espaço / Z | A |
| Usar item | K / X | B ou X |
| Itens | I | Y |
| Pausa | Enter / Esc | Start |
| Mapa do castelo | TAB | Select |
| Som | M | — |

## Estrutura

```
index.html                     jogo pronto (folha de sprites embutida)
lenda-da-brasa-sprites.png     folha de sprites (o jogo usa esta se existir ao lado)
src/lenda-da-brasa.template.html   código do jogo (HTML + JavaScript)
src/castelos.js                dados dos castelos gerados por ferramentas/castelos.py
ferramentas/castelos.py        desenho das salas dos 3 castelos (com validação de portas e escadas)
ferramentas/gerar_brasa.py     gera todos os sprites em pixel art
ferramentas/build.py           monta o index.html
sprites/                       folha, atlas e prévia ampliada dos sprites
```

## Como atualizar

```
python3 ferramentas/gerar_brasa.py   # só se mudar os sprites (precisa de Pillow)
python3 ferramentas/build.py         # gera index.html a partir do template e dos castelos
```

Para atualizar o Portal Pixel, copie `index.html`, `lenda-da-brasa-sprites.png` e `capa.png`
para `jogos/lenda-da-brasa/` no repositório do portal e aumente `versao` em `jogos.js`.

## Próximos passos

Santuários do Sol (Deserto), da Floresta, da Sombra, do Gelo, da Lua e da Estrela,
o Reino Sombrio, a batalha final contra o Rei Umbra e o resgate da princesa.

---
Criado por Heberson Miliano.
