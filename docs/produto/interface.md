# Interface — o que cabe na tela, em que ordem, e do que tamanho

> Parte da documentação do Raxa — índice em [docs/README.md](../README.md).
> Este guia é sobre **uso**: tamanhos, o que cabe numa tela de celular, a ordem das coisas e as
> regras para desenhar uma tela nova. Cor, fonte e acabamento ficam no CSS e nas decisões de
> [interface](../decisoes/interface.md); não são assunto aqui. O comportamento de cada tela está
> em [Fluxo do racha](fluxo-do-racha.md), [Confirmação de presença](confirmacao-de-presenca.md),
> [Stats](stats.md) e [Contas](contas-e-permissoes.md).
>
> **Referência de tamanho:** celular estreito de **360 × 780 px** (o pior caso que o app suporta) e
> celular comum de **390 × 844**. O `scripts/visual.py` confere as telas em 360 e 500 px e salva os
> prints em `scripts/.tmp/shots/` — são a referência visual de cada tela.

## 1. A tela: o que é fixo e o que rola

De baixo para cima, o que não sai do lugar:

| Faixa | Altura | O que é |
|---|---|---|
| **Navegação** (5 abas: Racha · Stats · Jogadores · Jogos · Ajustes) | 60 px + área segura do iPhone | Fixa embaixo, onde o polegar chega. Ícone em cima, rótulo de 12 px embaixo. Ponto vermelho na aba Racha = racha ao vivo; ponto verde em Jogadores = opiniões pendentes. |
| **Barra de ação** (só quando há ação principal) | 54 px de botão + 10 px de folga em cima e embaixo | Logo acima da navegação. É onde vive a **ação primária** da tela: Iniciar racha, Montar times (N), Começar racha, Começar partida, Fim · placar, Encerrar racha. No máximo **dois botões** lado a lado (secundário à esquerda, primário à direita) mais, na partida, o ↩ de 62 px. |
| **Conteúdo** | o resto, rolável | Cards de 14 px de padding e 10 px entre eles, largura total até 640 px (no computador o app é uma coluna centrada). Folga de 12 px nas laterais. |

Não existe cabeçalho fixo em cima: o nome da liga mora em Ajustes (D-137). O primeiro pixel da
tela é conteúdo.

**Sobre o conteúdo, quando preciso:**

- **Folha** (sheet): sobe de baixo, até **88 % da altura**, com a alça de 40 px em cima; é onde
  ficam ações secundárias e formulários (ficha do jogador, novo jogador, autor do gol, vagas, quem sou).
  Fecha tocando fora, na alça ou em Cancelar.
- **Toast**: 1 linha, 84 px acima da navegação, some sozinho. É o único "feedback" escrito do app.

## 2. Tamanhos que valem em toda tela

| Elemento | Tamanho | Regra |
|---|---|---|
| Botão da barra de ação | 54 px de altura, fonte 17 px | uma ação = um toque; o rótulo diz o resultado ("Fim · Empate 1-1", "Montar times (14)") |
| Botão normal (`.btn`) | 48 px | primário (tinta) ou fantasma (`ghost`, cinza claro) |
| Botão pequeno (`.btn.sm`) | 38 px, fonte 13,5 px | dentro de cards e folhas; nunca é a ação principal da tela |
| Campo de texto | 48 px; nos Ajustes 40 px | fonte **16 px** sempre (abaixo disso o iPhone dá zoom ao focar) |
| Chip de nome (presença, quem sou) | 42 px, 2 colunas, 6 px de folga | nome em 13 px com reticências; badge compacto à direita; 🧤 de 38 × 42 ao lado |
| Chip da chamada | 32 px, 2 colunas, 4 px de folga | número à esquerda, badge à direita (D-168) |
| Linha da escada (Jogadores) | **44 px**, uma linha só | badge de divisão de 28 px, nome 14 px e, à direita, só o que muda: "⏳ 3/15" calibrando e o Elo do admin; seta › (D-175) |
| Linha de lista (ranking, contas) | 52 px | nome 15 px + uma linha de meta em 11 px; seta › à direita |
| Linha de racha (aba Jogos) | 60 px | data, partidas, gols; faixa verde à esquerda quando "VOCÊ" jogou |
| Placar na partida | numeral 52 a 76 px (14 % da largura), bloco de 96 a 148 px | o bloco inteiro é o botão de gol |
| Rótulo de seção (`.k`) | 11 px maiúsculo | em cima de cada bloco, sem texto de ajuda embaixo |
| Segmentado (`.seg`) | 36 px | filtros de Stats e Linha/Gol |
| Interruptor (`.sw`) | 46 × 28 px | só em folhas e Ajustes |
| Alvo de toque mínimo | **32 px** de altura (medido pelo `visual.py`) | 44 px para tudo que é da quadra (gol, presença, fim) |

## 3. O que cabe numa tela de 360 × 780

Descontando navegação (60) e barra de ação (74), sobram **~645 px** de conteúdo quando há barra e
**~720 px** quando não há. Contas de referência (a partir dos prints):

| Tela | O que cabe sem rolar |
|---|---|
| Presença | cabeçalho + busca + **14 chips** (7 linhas de 42 px em 2 colunas) — a galera de sempre |
| Chamada (aba Racha fora do dia) | data (+ endereço em uma linha) + o meu estado + Gol (2 + espera) + Linha (12) + espera + "Confirmar alguém" |
| Quem é você | rótulo + busca + **18 nomes** (9 linhas) + "criar meu jogador" |
| Montagem | cabeçalho com 2/3/4 times e Equilibrar + goleiros + **2 times de 4 lado a lado** por dobra; 4 times pedem uma rolagem |
| Partida ao vivo | relógio + 2 colunas (placar + goleiro + 4 de linha) + "entram no próximo" (2 linhas) + "depois" (1 linha) + gols do jogo; o placar fica na metade de cima e a barra Fim embaixo |
| Próxima partida | placar registrado + os dois lados + fila (entram / depois) + Chegou · Foi embora · Refazer |
| Jogadores | opinião pendente + Linha/Gol + **17 linhas** de escada (44 px cada) |
| Stats · Jogador | 3 filtros + cabeçalho da pessoa + anel + 4 tiles + posições; partida a partida rola |
| Ajustes | liga + código + Liga + Chamada (1 dia) até a dobra; Partida, Contestação, Aparência, Exportar e Registro rolam |

Quando a tela é de 500 px de largura as colunas não aumentam de número; só o nome cabe inteiro.

## 4. A ordem de cada tela, de cima para baixo

**Aba Racha, sem racha** — 1. *Quem é você nesta liga?* (só sem perfil) · 2. *Próximo racha*:
data grande, endereço da quadra (link do mapa, quando há),
**o meu estado ou Vou / Vou no gol** (confirmado por outro: "X confirmou você" + **Confirmo** / Não vou), lista Gol
(dentro, espera), lista Linha (dentro, espera), *+ Confirmar alguém* (quem lança), *Vagas deste
racha · Cancelar este racha* (admin). Barra: **Iniciar racha** (quem lança).

**Presença** — contador grande à direita · dica de uma linha (com "12 de 14 confirmados" quando há chamada) · *Marcar os N confirmados* (quando
há) · busca com ✕ · grade de chips (marcados primeiro, depois confirmados dentro, depois espera,
depois quem mais joga) · *+ Novo jogador*. Barra: **Cancelar · Montar times (N)**.

**Montagem** — cabeçalho (formato, veredito, barra de equilíbrio) · 2/3/4 times + Equilibrar + 🎲 ·
goleiros à parte (quando há) · times em 2 colunas com badge e contador n/n · quem ficou de fora.
Barra: **Voltar · Começar racha**.

**Partida ao vivo** — relógio + alvo + pausa/cancelar · duas colunas: **placar (botão de gol)**,
goleiro, linha · aviso de gol sem autor (quando há) · fila: *entram no próximo* / *depois* ·
Chegou · Foi embora · Refazer times · gols do jogo (com ✕). Barra: **↩ · Fim · resultado**.

**Próxima partida** — placar registrado + *Voltar a partida* · resumo de quem sai e entra · os dois
lados (chance, "fica", ▲ quem entra) · reserva de goleiro · fila · Chegou · Foi embora · Refazer ·
partidas de hoje + *Desfazer a última*. Barra: **Encerrar racha · Começar partida**.

**Jogadores** — *Minhas opiniões* (uma linha, quando há pendência) · Linha / Gol · escada por
patente (cabeçalho com o nome do nível e a contagem), cada linha: badge da divisão, nome, e à direita
só "⏳ 3/15" enquanto calibra (e o Elo cru para o admin) · *Sem nível ainda* · Pendências (admin).
Toque na linha abre a ficha em folha, onde mora a campanha V/E/D.

**Stats** — Jogador / Racha · Último / Mês / Ano / Sempre · Linha / Gol · painel.

**Jogos** — contestadas (quando há) · Todas / Só as minhas · lista de rachas (60 px cada); dentro
do racha: cabeçalho, *Destaques do racha ›*, bloco Chamada (quando há), partidas.

**Ajustes** — liga (nome, números, *Trocar de liga*) · código de convite · Liga (formato, quem vê,
nomes dos níveis) · Confirmação de presença · Partida · Contestação · Aparência · arquivados ·
Exportar / Importar / Apagar ou Sair · Tamanho da liga · Registro de correções (admin).

## 5. Regras para desenhar uma tela nova

1. **A ação principal vai para a barra de baixo**, com o resultado escrito no botão. Nunca no meio
   do conteúdo, nunca exigindo rolagem (RNF-01.7).
2. **Um toque grava.** Confirmação só no que não tem volta (encerrar, cancelar com presença marcada,
   apagar). Tudo que é repetido durante o racha (gol, presença, confirmar alguém) não pergunta nada
   e não fecha a folha.
3. **Nenhum texto de ajuda parado.** Dica só de uma linha, dizendo o próximo passo, e no meio do
   gesto ("Toque em quem chegou"). Se precisa explicar, a tela está errada.
4. **Lista de gente é em duas colunas**, chip de 42 px (tocar em quadra) ou 32 px (ler uma lista).
   Nome com reticências, nunca quebra de linha. Três colunas não cabem nome mais badge em 360 px.
5. **Quem importa primeiro.** Toda lista tem uma ordem que responde "quem eu procuro": marcados,
   confirmados, quem mais joga; depois alfabético. Marcar alguém não reordena a lista embaixo do dedo.
6. **Cada tela tem um número grande** que diz o estado: presentes, placar, data do racha, cronômetro.
7. **Secundário vai para folha**, não para outra tela. Folha abre e fecha em um toque; formulário
   tem Cancelar e Salvar no pé.
8. **Admin e lançador veem mais, no mesmo lugar.** O que o papel não pode fazer não aparece — sem
   botão desabilitado e sem cadeado.
9. **Testar em 360 px** antes de considerar pronto: `python scripts/visual.py` e olhar o print.

## 6. Sugestões de melhoria (não feitas — para decidir)

1. **Chamada: colapsar a lista de quem já está dentro quando está cheia.** Com 12 + 3 dentro e 4
   na espera, quem abre a tela quer ver **a espera e o próprio estado**; os 15 nomes de dentro
   poderiam vir recolhidos numa linha ("12/12 · ver") quando a pessoa já está confirmada. Mais
   nomes por tela nos dias cheios.
2. **Partida ao vivo: a fila "depois" poderia ser uma linha só** ("depois: Juliano, Mauro, Igor, +2")
   em vez de chips. Ganha 2 linhas para o placar e os gols, que são o que se olha a cada 30 s.
3. **Ajustes ganhou altura:** com dois dias de chamada, Partida e Contestação saem da primeira
   dobra. Os cards de Chamada e Partida poderiam ser recolhíveis (título + resumo em uma linha,
   abre ao tocar), como o admin só mexe neles uma vez.

Feitas em 2026-09-14 (D-174): o contador "12 de 14 confirmados" na presença, "Sem racha marcado" na
aba Racha vazia e a folha só de leitura ao tocar num nome da chamada como jogador comum. E (D-175) a
escada de Jogadores em uma linha por pessoa, sem V/E/D. (D-178) "Você vai na linha" sem a posição;
quem foi confirmado por outro vê **Confirmo** / Não vou no lugar de ir para o gol / Não vou. (D-179)
endereço da quadra em uma linha embaixo da data e um campo a mais no card Chamada dos Ajustes, com
sugestões (até 5 botões de 40 px, texto à esquerda) logo abaixo enquanto digita (D-180). (D-181) a
linha de contadores embaixo da data saiu: "Gol 2/3" e "Linha 12/12" já estão no título de cada
lista, e a espera passou a mostrar o número dela ("Espera · 1").
