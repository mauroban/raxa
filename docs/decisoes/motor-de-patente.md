# Decisões · Motor de patente

> Elo, K, trecho, calibração como mecânica, proteção, goleiro no motor e os estudos de convergência.
> Índice de todas as decisões e regra de registro em [README.md](README.md).

---

<a id="d-01"></a>
### D-01 · A unidade de cálculo é o trecho — sempre
**18/08/2026.** Cada formação em campo é uma partida para o motor. Calibração, proteção pós-promoção e
os contadores de partidas jogadas contam **trechos**, não partidas de relógio.
**Por quê:** substituição muda o nível dos dois lados; medir por partida creditaria a alguém o que
aconteceu enquanto ele estava no banco.
**Descartado:** contar proteção e calibração em partidas de relógio (chegou a ser implementado e foi
revertido) — deixava duas unidades convivendo no mesmo motor.
**Onde:** [Patentes §4](../produto/patentes.md) · `splitStints`, `applyMatch` · teste `[5]`.

<a id="d-02"></a>
### D-02 · O peso do trecho descartado é redistribuído
**18/08/2026.** Trecho curto cortado por substituição não conta, e o peso dele é **dividido entre os
trechos que contam**. Uma partida vale exatamente uma partida.
**Por quê:** antes, uma troca no começo fazia a partida inteira pesar 0,75 — a partida encolhia por
causa de uma decisão de quadra.
**Onde:** [Patentes §4](../produto/patentes.md) · RF-03.3d · `splitStints` · teste `[5]`.

<a id="d-03"></a>
### D-03 · O mínimo de trecho é relativo: 4 min **ou ⅓ da partida**, o que for menor
**18/08/2026.** **Por quê:** o modo padrão é de 7 minutos; com 4 minutos fixos, duas trocas nunca
poderiam contar na mesma partida, e qualquer substituição antes dos 3 min descartava meia partida.
**Onde:** [Patentes §4](../produto/patentes.md) · RF-03.3c · teste `[5]`.

<a id="d-04"></a>
### D-04 · A variação de patente é fixa e igual em toda liga
**28/08/2026** (reescreve a de 18/08). Margem **13**, proteção **3 trechos**, calibração **5 rachas ou
25 partidas**, K **22/60** no racha curto e **30/70** na partida única. **Não existe opção de
"estabilidade"** — nem Baixa/Média/Alta, nem campo de calibração.
**Por quê:** (1) a opção era uma pergunta que nenhum admin sabia responder, e ligas diferentes com
escadas que significam coisas diferentes matam a comparação; (2) com K=16 e times equilibrados
(todo confronto ~50%), uma patente levava ~100 partidas — o palpite do cadastro mandava por meses, e a
calibração de 15 partidas a K=34 corrigia pouco mais de uma divisão. Agora um cadastro errado se
corrige em uma ou duas noites, e subir uma patente com 60% de vitórias leva ~4 sábados.
**Descartado:** presets Baixa 7/2 · Média 13/3 · Alta 20/5 (18/08); antes disso 10/20/34. Liga antiga
com preset gravado volta ao padrão na carga.
**Onde:** [Patentes §4–6](../produto/patentes.md) · `KMODE`, `RANK_MARGIN`, `PROTECT`, `CAL_*`, `normalize` · testes `[6]` `[7]`.

<a id="d-05"></a>
### D-05 · Patente por valência só existe se a pessoa jogou nela
**18/08/2026.** Quem nunca jogou na linha, ou nunca pegou no gol, **não tem patente ali**: fica fora
daquela escada e a ficha diz *sem patente*. Se entrar naquela posição, vale o **nível de entrada padrão**
e começa a construir a dele, em calibração. O palpite do cadastro vale só para a valência da pessoa.
**Por quê:** cadastrar um Diamante de linha fazia dele um Diamante no gol — a escada de goleiro vinha cheia
de gente que nunca defendeu.
**Descartado:** herdar a patente da outra valência (comportamento anterior, migrado na carga).
**Onde:** [Patentes §7](../produto/patentes.md) · [Regras do racha §5](../produto/regras-do-racha.md) · RF-03.1c/1d · `newTrack`, `temPatente` · smoke.

---

## Montagem de times e rodízio

<a id="d-33"></a>
### D-33 · K 36/44 e acelerador de sequência; chance igual na pré-partida e ao vivo
**28/08/2026.** K base sobe de 22 para **36** (racha curto) e de 30 para **44** (partida única);
calibração continua 60/70. Novo: `streakK` — 4+ resultados iguais seguidos multiplicam o K por 1,5
até a sequência quebrar (empate quebra), para cima e para baixo. Bug corrigido: a chance na
pré-partida não contava o goleiro do rodízio na escalação, e a partida ao vivo contava — os dois
números eram diferentes; agora a pré-partida monta a escalação como `startMatch`.
**Por quê:** um Ferro 1 estabelecido venceu 18 seguidas para subir 3 divisões (7 na primeira noite =
Ferro 2). Times parelhos dão 50 % de expectativa e 11 pontos por vitória com K=22; o racha ficava
desequilibrado por semanas. Sequência longa é o sinal mais claro de nível errado que o app tem, e
a histerese/proteção (D-?) já seguram o ioiô — não precisa de K pequeno para isso.
**Descartado:** só subir o K para 50+ (uma noite de sorte viraria uma patente); ajuste individual
por desvio da média do time (não distingue quem carrega de quem é carregado).
**Onde:** `KMODE`, `streakK`, `computeElo`, `viewProxima` (`escalCom`).

<a id="d-34"></a>
### D-34 · K decai com histórico; acelerador também por saldo de forma
**28/08/2026.** `kFor`: K cheio (36/44) até 60 partidas na trilha, depois `base·√(60/partidas)`
com piso 24/30. `streakK` passa a disparar também com saldo de ±6 nas últimas 10 (além dos 4+
iguais seguidos).
**Por quê:** num racha parelho o Elo por time tem puxão de volta diluído por 5, e um K fixo de 36
deixa um jogador mediano espalhar ±2 divisões só de sorte ao longo dos meses. O decaimento é o que
o Glicko faz com a incerteza: veterano balança ±1,5 divisão, novato converge em 1–2 noites. O
risco do K baixo — alguém calibrado em times ruins preso lá embaixo — é coberto pelo acelerador,
que agora também enxerga 7V-1D com empates no meio (sequência pura de 4 era estreita demais).
**Descartado:** K fixo alto (oscila sem parar); regressão à média por temporada (apaga histórico
real); ajuste individual por desvio da média do time (não separa quem carrega de quem é carregado).
**Onde:** `KMODE.min`, `K_FULL`, `kFor`, `FORM_GAP`, `streakK`, `computeElo`.

<a id="d-37"></a>
### D-37 · Trecho curto sem gol não conta; K dividido por trechos válidos; V/D é da partida
**28/08/2026.** Com mais de um trecho: trecho com menos de 20 % da partida e sem gol é descartado —
inclusive o final; nesse caso o resultado da partida vai para o maior trecho que conta. Os
trechos válidos dividem a partida em partes iguais (peso 1/n, ou seja K/n). Vitória, empate e
derrota passam a ser **da partida**: quem esteve num trecho que conta recebe o resultado final
uma vez, pelo lado em que terminou — em partidas jogadas, V/E/D, forma, duelos, parcerias,
calibração e estatística. Tempo em quadra, gols sofridos e tempo no gol continuam vindo dos trechos.
**Por quê:** uma troca a 40 segundos do fim criava uma "partida" de 40 segundos que contava
vitória/derrota para 10 pessoas e girava o K; e "2 trechos = 2 partidas" inflava os contadores de
quem fica em quadra. A partida é a unidade que o racha reconhece; o trecho é detalhe do motor.
**Descartado:** peso proporcional à duração (mantido só como critério de "curto"); contar o
resultado do trecho para quem entrou no meio.
**Onde:** `splitStints` (`STINT_MIN_W`), `finish` (alvo do resultado), `applyMatch` (por partida),
`statsLiga`, `statsAnos`, `destaques`.

<a id="d-38"></a>
### D-38 · Partida única tem regra de trecho própria
**28/08/2026.** No modo **partida única** (longa): peso do trecho = fatia de tempo (não 1/n);
trecho conta a partir de `stintMin` com ou sem gol; o final conta sempre; e vitória/derrota/partida
jogada só para quem esteve em quadra por ≥ 25 % do tempo que conta (`UNICA_MIN_SHARE`). O modo
curto mantém a D-37 (curto sem gol descartado, K/n, qualquer trecho válido dá a partida).
**Por quê:** em 50 minutos com trocas rolando, "1/n" faria um trecho de 3 minutos pesar como um
de 30, e "qualquer trecho válido dá a vitória" entregaria a partida a quem entrou para cumprir
tabela. Os dois formatos são jogos diferentes; a régua tem que ser diferente.
**Onde:** `splitStints(…, mode)`, `contaPartida`, `applyMatch`, `statsLiga`, `statsAnos`, `destaques`.

<a id="d-45"></a>
### D-45 · Partida única: nível por confronto, placar por margem; +/- em destaque só nela
**28/08/2026.** Na liga de partida única, `unidadesNivel` junta os trechos que contam e têm a
**mesma escalação dos dois lados** (e goleiros) num confronto só — placar, tempo e peso somados —
e o resultado do confronto é a **margem saturada** `S = 0,5 + 0,5·tanh((gf−gc)/2)` (1-0 → 0,73,
2-0 → 0,88, 3-0 → 0,95). `computeElo` aceita esse `[S0,S1]` fracionado; "acima do esperado" usa o
mesmo S. V/E/D continua da partida inteira (D-38). O +/- aparece em primeiro (cartão, rankings,
último racha, ficha) **só na liga de partida única**; no racha curto ele fica depois das vitórias
e o resto continua exatamente como antes.
**Por quê:** na partida longa os gols decidem o resultado e precisam pesar; mas um 0-0 contra
time pior também tem que valer — a margem saturada dá as duas coisas. Juntar trechos do mesmo
confronto evita que uma troca e a volta virem dois jogos. O racha curto já estava bom.
**Descartado:** V/E/D por trecho (a vitória é da partida); margem linear sem teto (5-0 valeria
cinco 1-0); +/- em destaque em toda liga.
**Onde:** `margemS`, `unidadesNivel`, `applyMatch`, `computeElo`, `viewStats`, `pSheet` ·
`test.py` (confronto juntado, margem, 0-0 contra time pior) · [Patentes](../produto/patentes.md).

<a id="d-46"></a>
### D-46 · Elo clássico: K 40/20, sem acelerador, sem proteção; calibração por modo
**28/08/2026** (K reescrito pela **D-55**: 64/32; calibração pela **D-53**: 15 partidas). `KMODE` vira 40 calibrando / 20 depois nos dois modos; `kFor` devolve K constante
e `streakK` devolve 1 (sem acelerador de sequência, sem decaimento por histórico). `PROTECT=0`:
sai a proteção pós-promoção (o campo `protect` continua no dado, sempre zero). Calibração por
modo da liga: partidas no racha curto (25 aqui; **15 desde a D-53**), **3 rachas** na partida
única (`calibrando`, `calMeta`, `calTxt`); os textos de "calibrando · x/N partidas" ou "x/3
rachas" seguem o modo.
**Por quê:** o usuário: "Elo já é muito bem testado e já sabemos o que funciona" — os números da
FIDE em vez de uma calibragem própria; e a proteção de 3 partidas num racha de 10–15 nem se
percebia. Substitui as calibragens de K das decisões anteriores (36/22, acelerador ×1,5).
**Descartado:** manter o acelerador só na calibração; proteção em rachas em vez de partidas.
**Onde:** `KMODE`, `kFor`, `streakK`, `PROTECT`, `calibrando`, `calMeta` · [Patentes §4–6](../produto/patentes.md),
[Princípios](../produto/principios.md) (decisão 9) · RF-03.6/03.7/03.10 · `test.py` [5]–[6], [8c].

<a id="d-55"></a>
### D-55 · K de jogo de time: 64 calibrando / 32 depois; margem de histerese 21
**29/08/2026** (reescreve o K da D-46 e a margem da D-04). `KMODE` vira **64/32** nos dois modos;
`RANK_MARGIN` 13 → **21**. Por vitória parelha: ±32 calibrando, ±16 depois — uma divisão (~67
pts) pede ~4 vitórias líquidas (um racha bom), uma patente ~13.
**Por quê:** o 40/20 da FIDE assume o sinal direto do 1×1; em time equilibrado a expectativa é a
média dos dez, o sinal individual dilui e o Elo converge devagar demais — com a calibração
encurtada para 15 partidas (D-53), o usuário pediu o que é aceito em sistemas de time testados
("tipo CS2"). Referência: o Elo do Faceit (CS2), K fixo ≈50 (±25 por vitória parelha) com níveis
de ~200 pontos como a nossa patente — o 64/32 fica na mesma banda mantendo o desenho FIDE de
"dobro enquanto calibra" e um K base clássico (32 = padrão USCF/online). A margem acompanha o K
por obrigação: precisa ser maior que meia vitória parelha (16), senão V-D-V-D em volta do corte
vira ioiô — 21 mantém a proporção da margem 13 sobre o ±10 antigo (banda ~109).
**Descartado:** K fixo ≈50 sem fase de calibração (a margem teria de passar de 25 e a banda
engoliria meia divisão); Glicko/TrueSkill (incerteza explícita é mais fiel, mas quebra a
simplicidade "Elo que todo mundo conhece" — fica para quando houver dados de vários rachas);
manter margem 13 com K 32 (ioiô matematicamente garantido no corte).
**Onde:** `KMODE`, `RANK_MARGIN` · `test.py` [4] (K de time, +16 parelho, margem > K/2), [7]
(histerese) · [Patentes §4](../produto/patentes.md) (tabela e nota D-55), [Patentes §5](../produto/patentes.md), [Patentes §6](../produto/patentes.md).

<a id="d-65"></a>
### D-65 · Patente e destaques seguem o critério do modo — como a doc sempre disse
**31/08/2026.** Dois consertos no motor. **(1)** `temPatente` passa a usar **o mesmo critério (e os
mesmos números da liga) que `calibrando`**: `t.def || !calibrando(liga, p, t)`. Antes era um OU dos
dois critérios com as constantes globais (`sessions>=3 || games>=15`, ignorando o modo e o cfg da
liga) — dava para aparecer na escada com patente e, na mesma linha, "calibrando · 12/15": três
rachas de 4 partidas davam o rótulo antes de a calibração terminar. A assinatura ganhou a liga
(`temPatente(liga, p, role)`); todos os chamadores e o `test.py` acompanharam. **(2)** O piso dos
destaques ("Os melhores do racha" / "Quem mais rendeu") acompanha o modo: na liga de **partida
única** cada racha é uma partida, então exigir 20 jogos era exigir 20 rachas — meses sem nenhum
destaque, com a tela dizendo só "ainda sem gente suficiente". Agora: curtas `{rachas:2, jogos:20}`,
única `{rachas:2, jogos:2}` (equivale ao piso de rachas). De quebra, os comentários do motor que
citavam números velhos (banda "~109", "4 rachas OU 15 partidas", "25 PARTIDAS", stintMin "padrão
4") foram corrigidos para os valores reais (banda 42, critério único por modo, 15, 3).
**Por quê:** a [Patentes §4](../produto/patentes.md) (calibração) já descrevia o critério único por modo — o código é que
tinha ficado para trás; e comentário errado sobre constante é bug em incubação.
**Descartado:** manter o OU dos dois critérios "por segurança" (é exatamente o que criava o estado
contraditório patente+calibrando); piso configurável por liga (mais um botão para ninguém mexer).
**Onde:** `temPatente`, `calibrando`, `destaques` em `index.html` · [Stats §3](../produto/stats.md) §"Acima do
esperado" (piso) · `test.py` (blocos de patente e destaques, assinatura nova).

<a id="d-82"></a>
### D-82 · K por incerteza (64/32 → 16) e aviso "revisar palpite?" para o admin — em vez de K fixo 32
**01/09/2026.** Pergunta de origem: "as patentes convergem bem com um mínimo de direcionamento
dos palpites?". Respondida com simulação usando o MOTOR REAL (`computeElo`/`updateRank`/
`buildTeams` importados do `index.html`, hoje `scripts/converge.py`): grupo de 20 com habilidade
verdadeira ~N(1500, 200), presença variável (13–18, quatro que vêm a cada 3 semanas), times
montados pelo app pelo Elo atual, vencedor fica, remontagem em 25% das noites, 12 partidas
curtas com gols Poisson (2 gols ou 7 min). Três cenários de palpite × sete regras, 80–300 ligas.
**O que se mediu.** (1) O palpite é o que decide: com palpite bom (±1 divisão) a ordem já nasce
em 0,90 e os times saem a ~30 pts do perfeito no 3º racha; sem palpite, os times ficam 75–100
pts desequilibrados por ~10 rachas em QUALQUER regra — inclusive num estimador em lote com todo
o histórico, o teto de informação. (2) **K fixo 32 corrói o palpite bom**: 73% de patente certa
no 1º racha → 57% no 30º, erro 57 → 103 pts — o piso de ruído do motor (~100 pts, 1,5 divisão).
Com times equilibrados a expectativa é 0,5 e cada partida dá ±16 aos 4 do time por igual: quase
todo movimento é passeio aleatório; a informação individual só entra quando os times se misturam.
(3) K 16 preserva o palpite (82% dentro de ±1 divisão em 30 rachas, contra 60%) e a convergência
de ORDEM sem palpite é igual em qualquer K (0,77) — o K só muda a escala. (4) O medo "K menor
prende palpite errado" é verdade só nos primeiros ~5 meses (racha 5: 39% corrigidos a K32, 20% a
K16); perto do racha 25 empata e depois o 16 corrige melhor (64% vs 53%) porque o 32 estaciona no
ruído. (5) **Bônus de sequência** (3+ iguais ×1,5, 5+ ×2) e **K adaptativo por surpresa** perdem
em TODOS os cenários, inclusive para os palpites errados que deveriam ajudar — sequência contra
o esperado é o que o acaso produz toda noite para alguém dos 16. (6) **K decrescente por
incerteza** (sem palpite 64→16, com palpite 32→16, em 45 partidas) foi a melhor ou empatada em
todos os cenários: misto 75% / bom 85% / sem palpite 74% dentro de ±1 divisão em 40 rachas,
contra 55 / 61 / 67 do K fixo 32. (7) O teto (reajuste em lote): 95% com palpite bom, 70–77% nos
outros — ou seja, sem palpite ou com palpite errado, ~70–75% É o limite da informação; a regra
nova chega perto dele, e com palpite bom chega a 2/3 do caminho entre o atual e o teto.
(8) O esporádico com palpite errado é o caso que nenhuma regra resolve com dados (teto: 26% em
40 rachas) — só a correção humana.
**Decidido.** `kFor(liga,km,tr)`: K = k0 − (k0 − 16) × min(1, progresso/(3 × calibração)), com
k0 = 64 sem palpite (`tr.def` falso) e 32 com palpite; progresso em partidas no racha curto e em
rachas na partida única (`calMeta`), como a calibração. O rótulo "calibrando" (D-65) não muda:
é sobre mostrar a patente. E o sinal de surpresa vira **aviso ao admin**, não K: cada trilha
guarda `surp` = média móvel (0,8/0,2) de resultado − esperado (`m.over`, já calculado); com 10+
partidas e |surp| ≥ 0,35 (~2 desvios do ruído de moeda, 0,17), a escada e a ficha mostram
"⚠ rende acima/abaixo do nível — revisar palpite?" só para o admin. `surp` é recalculado no
`rebuildAll` como tudo; não vai para o banco.
**Descartado:** K fixo 16 (empata com o por incerteza quando há palpite, mas sem palpite demora
mais para abrir a escala); K por incerteza "rápida" (48/96 → 16 em 30 partidas: corrige o
esporádico errado um pouco antes, mas chacoalha os palpites bons — 85% vs 92% no 3º racha);
bônus de sequência e K por surpresa (acima); incerteza que cresce com ausência (Glicko) — não
testada, fica como próximo experimento; mexer na margem de histerese (21 > 16/2 assentado; entre
15 e 45 partidas K/2 passa de 21 por um trecho curto, e o ioiô possível ali é de calibração,
aceito).
**Onde:** `KMODE`, `K_DECAI`, `kFor`, `computeElo`, `applyMatch` (surp), `revisar`/`revisarTxt`,
escada e ficha do admin, texto de Ajustes (`index.html`) · `scripts/test.py` [5] e bloco de
surpresa · `scripts/converge.py` (a régua: `python scripts/converge.py misto`) ·
[Patentes §4](../produto/patentes.md), [Patentes §5](../produto/patentes.md), [Patentes §8](../produto/patentes.md).

<a id="d-83"></a>
### D-83 · Piso do K em 20; aviso de revisão por RANKING (últimos 8 rachas); cansaço fica fora do rating
**01/09/2026.** Continuação da D-82, respondendo a três perguntas com a mesma régua
(`scripts/converge.py`, agora com cansaço opcional): "o que acontece com UM jogador mal
posicionado numa liga bem calibrada?", "precisamos corrigir cansaço?" e "o aviso de revisão
funciona?".
**Um jogador errado em uma patente inteira, liga bem classificada, cansaço ligado.** Frequente
(85% dos rachas): leva ~6 meses para ficar a uma divisão do lugar em QUALQUER regra (limite de
informação: +0,07 de sinal por partida). Mas com vencedor-fica apareceu uma assimetria: o
**subestimado** se corrige mais rápido (o time dele ganha, fica em quadra, joga mais partidas);
o **superestimado** perde, sai e joga menos — no piso 16, 40% dentro de ±1 divisão em 6 meses
contra 65% do subestimado; **no piso 20, 68% dos dois lados** (K fixo 32: 68%/64%, mas com a
liga a 72%). A liga bem classificada perde 2–4 pontos com o piso 20 (87–89% contra 91%). O
**esporádico** (1 em 3 rachas) errado não converge com dados em 6 meses em regra nenhuma
(26–51%) — só correção humana.
**Cansaço.** Testado cansaço real de −50 pts por partida seguida em quadra (até −150) e correção
no motor de 0/15/25/50 na expectativa: corrigir **não melhora nem com o valor exato** (89% → 85%
em 6 meses) e custa 2–5 pontos quando o cansaço não existe. Cansaço é simétrico — todo mundo
cansa, em todas as noites — e se cancela na média de cada pessoa; a correção só adiciona
variância à expectativa. Fica fora do rating. Onde ele importa é na probabilidade de vitória
mostrada no apito e na justiça do vencedor-fica; antes de qualquer coisa, medir do histórico real
(taxa de vitória por partida seguida em quadra — o app guarda ordem e duração) — item de Stats a
fazer, não decisão de motor.
**Aviso de revisão.** O da D-82 (média móvel fora de ±0,35) estava mal calibrado: para quem
está uma patente fora, dispara em ~5% das noites contra ~2% de quem está certo — quase nunca.
Trocado por **posição no ranking**: soma de (resultado − esperado) por trilha (`m.overR`,
pid+papel, calculado no `applyMatch` ao lado de `m.over`) nos **últimos 8 rachas**, normalizada
por √partidas, mínimo 10 partidas na janela; os **3 de cada ponta** (com 6+ na lista) ganham
"📈/📉 Nº de M em render acima/abaixo do esperado nos últimos 8 rachas — revisar palpite?" na
escada (só admin) e na ficha (que mostra a posição de todo mundo). Em simulação, o jogador uma
patente fora aparece no top 5 desse ranking em ~2/3 dos casos com 2–3 meses (frequente) e em
metade com 6 meses (esporádico). As linhas dos rankings da aba Stats passam a abrir a ficha.
**Decidido:** `KMODE.piso` 16 → 20 (os dois modos); `rankingSurpresa`/`revisar`/`revisarTxt`
substituem `tr.surp` (removido de `newTrack`/`rebuildAll`); sem correção de cansaço.
**Descartado:** piso 24 (devolve ruído: liga a 80–86%); corrigir cansaço no rating (acima);
limiar absoluto de surpresa (acima); incerteza que cresce com ausência (Glicko) — ainda não
testada.
**Onde:** `KMODE`, `applyMatch` (`m.overR`), `rankingSurpresa`, `revisar`, escada e ficha do
admin, `lin` da aba Stats (`index.html`) · `scripts/test.py` [5] e bloco D-83 ·
`scripts/converge.py` (argumento de cansaço) · [Patentes §4](../produto/patentes.md), [Patentes §5](../produto/patentes.md), [Patentes §8](../produto/patentes.md).

<a id="d-110"></a>
### D-110 · Gol de goleiro é conta de goleiro; improviso no gol entra uma patente abaixo
**03/09/2026.** Dois pedidos do mesmo dia, ambos sobre separar linha e gol.
**Gol feito de dentro do gol.** Alguns goleiros fazem gol, e é façanha maior que gol de linha —
então conta à parte: `roleNoGol` acha o trecho da partida em que o gol caiu e lê a função de quem
marcou naquele instante (trecho antigo sem carimbo usa a escalação gravada). `statsLiga` separa
`gols` (linha) de `golsGk` (gol); a artilharia (rankings, destaques do mês, último racha) é só de
linha; o gol de goleiro aparece em dourado no cartão de goleiro da pessoa, no tile "gols de linha"
e nos rankings **Gols de goleiro** (temporada e último racha). A ficha (`p.goals`) e o "ano a
ano" seguem com o total — são contagens da pessoa, não da função.
**Improviso no gol.** Jogador de linha sem opinião como goleiro entrava no gol valendo a entrada
padrão (Prata 2, 1500). Isso superestimava o time dele: no gol é mais difícil para quem não é
goleiro. Agora entra **uma patente abaixo** (`entradaImproviso`: Bronze 2 na escada padrão,
1300), ainda "calibrando" (sem patente visível até as 15 partidas) e com o K de quem não tem
palpite (64 → 20), como antes. Goleiro fixo segue no padrão; qualquer opinião de goleiro
substitui a entrada automática — é a mesma `consolida` de sempre, só o padrão mudou.
**Descartado:** entrada no Ferro (duas abaixo) — o K alto já corrige rápido, e no Ferro o time
dele ficava subestimado na montagem; marcar gol de goleiro na "partida a partida" com outra cor —
a linha é do jogo da pessoa, não da função. `converge.py` não modela goleiro, então não mede isso.
**Onde:** `entradaImproviso`, `consolida`, `mkPlayer`, `roleNoGol`, `statsLiga`, `viewStats` em
`index.html` · `scripts/test.py` [16] · [Conceitos §2](../produto/conceitos.md) (patente de goleiro) e [Stats §2](../produto/stats.md).

<a id="d-113"></a>
### D-113 · Sem "sinal de confiança" na patente: o estudo que decidiu (scripts/confianca.py)
**03/09/2026.** O pedido: um símbolo de "alta confiança / calibrado" depois do "calibrando · 12/15",
para dizer que a pessoa provavelmente está na patente certa. Antes de escolher os cortes, medimos
com o motor real (`scripts/confianca.py`, mesma simulação do `converge.py` — D-82: 20 pessoas com
habilidade verdadeira escondida, presença variável, times montados pelo app a cada racha, vencedor
fica, 12 partidas curtas; 60 ligas × 60 rachas; avaliação no fim de cada racha, só quem já calibrou).
**Sinais testados:** volume (15/30/45/90/150 partidas), circulação (das últimas 20/30/50/80
partidas, quantas terminaram na patente atual), distância do Elo à borda da patente, e combinações.
**Resultado (palpites bons, ±1 divisão da verdade para todos):** base 71% na patente certa, 80% a
±1 divisão, **97% a ±2 divisões**. Nenhum sinal muda o ±1 nem o ±2 — todas as linhas dão o mesmo
número. Volume não ajuda: 150 partidas acertam o mesmo que 15 (o K no piso de 20 põe tanto ruído
quanto informação). A circulação (≥40 das últimas 50) sobe a patente exata de 71% para 76%,
acendendo para 72% das pessoas; 72 das últimas 80 chega a 79% acendendo para metade. Com palpites
mistos (5 em 20 errados por uma patente): base 66% / 69% / 92%, e a circulação mal sai da base.
**Conclusão:** o motor garante a **patente com folga de ±2 divisões para todo mundo que calibrou**;
não garante a divisão para ninguém, e nenhum sinal observável separa quem está certo de quem não
está. Um check de "confiança" erraria 1 em 4 vezes que aparecesse — a lição da D-94 (aviso que
erra ensina a ser ignorado). **Decisão: nenhum símbolo além do "calibrando".** A ±2 divisões,
"calibrou" já é o sinal. O ruído é do dado, não do método: um resultado 5v5 é dividido entre dez
pessoas (~0,07 de informação sobre cada uma); o reajuste em lote com todo o histórico (teto de
qualquer método, `converge.py`) chega a 91% a ±1 contra 87% do motor.
**Pares — "3 divisões separam de verdade?"** Quando a diferença MOSTRADA entre duas pessoas é de d
divisões, o de cima é de fato mais forte em (bons / mistos): d=1: 72% / 66% · d=2: 87% / 81% ·
**d=3: 96% / 91%** · d=4: 99% / 97% · d≥5: 100%. A diferença real é de uma patente inteira em só
34% / 30% dos pares a d=3 (média real 2,4 / 2,2 divisões). Ou seja: **uma patente de diferença
diz "mais forte" com segurança, mas não "uma patente melhor"**; uma divisão sozinha é quase cara
ou coroa. É a régua para ler a escada e para qualquer texto que compare duas pessoas.
**Descartado:** "há N partidas nesta patente" (a pessoa sai e volta; e nem circulação separa);
percentual de certeza (Elo não tem incerteza formal); sinal "assentado" pelo K no piso (verdade
sobre o processo, mas não distingue ninguém — 89% acendem e a taxa de acerto é a da base).
**Onde:** `scripts/confianca.py [bom|misto|nada] [rachas] [ligas]` · [Patentes §9](../produto/patentes.md).

<a id="d-115"></a>
### D-115 · Diferença mantida no tempo vale ~1 divisão a mais que o retrato: o estudo (scripts/consistencia.py)
**04/09/2026.** A pergunta: a D-113 mediu um retrato ("hoje A está d divisões acima de B"). E se
as pessoas continuam jogando e a diferença **se mantém**? Depois de 3 meses de racha (13 rachas
semanais), mais 3 meses; se ao longo do 2º trimestre a **menor** diferença mostrada entre A e B foi
de X divisões (em nenhum fim de racha ficou abaixo, e em pelo menos um foi exatamente X), qual a
chance de A ser mais forte, e de ser uma patente inteira (3 divisões) melhor? Medido com o motor
real (`scripts/consistencia.py`, mesma simulação do `converge.py`/D-82; 200 ligas; só pares em que
os dois já calibraram no fim do 1º trimestre e jogaram no 2º — 98%).
**Resultado (palpites bons / mistos / sem palpite).** A é mais forte — X=1: **88% / 80% / 78%** ·
X=2: **96% / 90% / 88%** · X=3: **99% / 95% / 94%** · X=4: 100% / 98% / 97% · X≥5: 100% / 100% /
99%. Uma patente inteira de diferença real — X=1: 14% / 18% / 34% · X=2: 32% / 31% / 49% · X=3:
**55% / 48% / 64%** · X=4: 77% / 67% / 78% · X≥5: 97% / 91% / 92%. Diferença real média com X=3:
3,2 / 2,9 / 3,9 divisões.
**Retrato nos mesmos dados** (d exato no último racha, a régua da D-113, reproduzida): mais forte
X=1: 72% / 68% / 66% · X=2: 87% / 81% / 80% · X=3: 96% / 91% / 90% · X=4: 99% / 96% / 95%; uma
patente X=3: 33% / 32% / 49%. Segundo período de 6 meses em vez de 3: +3 a +5 pontos (X=1 mantido
sobe para 93% / 86%; uma patente com X=3 para 66% / 55%).
**Leitura:** um trimestre de consistência vale **cerca de uma divisão a mais** no retrato — 1
mantida ≈ 2 no retrato (88% vs 87%), 2 mantidas ≈ 3 no retrato (96% vs 96%), 3 mantidas ≈ 4 no
retrato (99% vs 99%). É informação real, mas não é mágica: "uma patente inteira melhor" continua
**não** garantida — 3 divisões mantidas dão só cara-ou-coroa (48–55%), e é preciso 5 mantidas
para passar de 90%. Dobrar o período rende 3–5 pontos, porque o ruído é do dado (um resultado 5v5
dividido entre dez), não da amostra. Sem palpite (`nada`) a ordem é um pouco pior e a "patente
inteira" um pouco melhor: sem palpite as pessoas ficam mais espalhadas na escada, então a mesma
diferença mostrada corresponde a uma diferença real maior.
**Consequência para o produto:** nenhuma mudança de UI agora. É a régua para qualquer texto ou
função futura que compare duas pessoas ao longo do tempo (ex.: "há três meses acima de"): a ordem
pode ser afirmada a partir de 2 divisões mantidas (≥90% em qualquer cenário); "uma patente
melhor" nunca só pela escada, nem com consistência.
**Descartado:** ler "no mínimo X" como "≥ X" (mistura pares com 1 e com 10 de diferença e infla
tudo — a primeira versão deste estudo fez isso e foi corrigida); medir pela média do período (fica
entre o retrato e o mínimo e é menos legível — "nunca ficou abaixo" é o que uma pessoa consegue
verificar olhando a escada); exigir presença dos dois em cada racha (a patente de quem faltou não
muda, então a comparação vale).
**Onde:** `scripts/consistencia.py [bom|misto|nada] [meses1] [meses2] [ligas]` · [Patentes §9](../produto/patentes.md).

## Como registrar uma decisão nova

Uma linha por decisão, nesta ordem: **o que foi decidido** (com a data), **por quê**, **o que foi
descartado** e **onde ela vive** — documento, função e teste. Se não tem teste, diga que não tem.
Decisão sem "por quê" volta a ser discutida em três meses; decisão sem "onde" vira lenda.
