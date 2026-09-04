# Patentes — o coração do produto

> Parte da documentação do Raxa — índice em [docs/README.md](../README.md).


## 1. O princípio inegociável: o número não existe para o jogador

Por baixo há um rating numérico (Elo). **Ele nunca aparece para quem joga.** Não aparece o valor, não aparece a distância para o próximo corte, não aparece quantos pontos a partida rendeu. A única exceção é o **admin** (D-52): na aba Jogadores ele vê o Elo cru num número pequeno e apagado no canto de cada linha — ferramenta de gestão para conferir a montagem e a convergência, não linguagem do racha.

Por quê:

- **Número vira fofoca e briga.** "Você tem 1487" é discussão; "você é Prata 2" é identidade.
- **O corte exposto vira jogo.** Se as pessoas sabem que faltam 12 pontos, elas passam a escolher partida em vez de jogar.
- **Patente é aspiracional, ponto é contábil.** O que faz alguém querer voltar na quinta é subir de patente, não somar pontos.

O que o app mostra a todo mundo é sempre: **patente + divisão**, a campanha (V/E/D) e o momento em que alguém sobe ou cai. Gols e forma recente ficam na ficha e na aba Stats — a escada é sobre nível (D-84). Fora da linha discreta do admin, o rating só existe no backup/servidor, como dado técnico.

## 2. A escada

**5 patentes × 3 divisões = 15 degraus.** Dentro de cada patente, **número maior é melhor**: a divisão 1 é a entrada e a 3 é o topo. Diamante 3 é o degrau mais alto da escada; Ferro 1, o mais baixo.

**Na tela, a cor diz a patente e o risco diz a divisão (D-80).** O badge é um **bloco de metal na cor da patente** — ouro é âmbar dourado (não amarelo-limão), prata é prata, diamante é gelo quase branco que escorrega para o violeta na sombra (pedra lapidada, não azul), bronze é laranja, ferro é aço escuro, **nos dois temas** (o que muda com o tema é a tinta por cima: escura nos metais claros, clara no ferro). E parece metal, não tinta: degradê vertical (luz em cima, sombra embaixo), chanfro nas bordas, reflexo diagonal e texto em relevo — tudo derivado da cor da patente, então cada metal tem o seu brilho. A cor sozinha identifica a patente de longe; o nome vai escrito por cima nos badges longos, mas ninguém precisa lê-lo. A divisão são **1, 2 ou 3 barras retas** na mesma tinta — `OURO I`, `OURO II`, `OURO III`. Mais riscos, mais alto. A cor é **a mesma nas três divisões** de uma patente; só a 3 ganha um halo discreto. O número existe em texto corrido ("agora é Ouro 3", toasts, registro de correções) e no `title`/`aria-label` de todo badge, que é o que o leitor de tela anuncia. É o mesmo desenho em **todo lugar** em que a patente aparece: badges longos e curtos, o pontinho dos chips de time e dos slots, a escada da aba Jogadores (só os riscos, porque o cabeçalho já diz a patente), a ficha, o editor de nível do admin, os cards de subida/queda do fim do racha e a variação de nível dos destaques.

| Patente | Divisões | Cor |
|---|---|---|
| **Diamante** | 1 · 2 · 3 | gelo quase branco, sombra violeta |
| **Ouro** | 1 · 2 · 3 | âmbar dourado |
| **Prata** | 1 · 2 · 3 | prata |
| **Bronze** | 1 · 2 · 3 | bronze |
| **Ferro** | 1 · 2 · 3 | aço escuro |

Os nomes seguem os materiais — *ferro → bronze → prata → ouro → diamante* — e as cores acompanham. A média da liga é **Prata** (o Elo é soma zero: o jogador mediano vive em 1500); Diamante é raro de propósito — a ponta vazia fica em cima, como ambição, e não embaixo, como constrangimento. Ninguém precisa decorar qual patente é maior.

Os nomes são **editáveis por Liga** — cada galera batiza a sua escada. As cores e a estrutura de 15 degraus são fixas.

## 3. Onde ficam os cortes (e por quê)

A referência é o próprio Arpad Elo: ele desenhou o sistema com **intervalo de classe de 200 pontos**, a distância em que o jogador mais forte vence cerca de **75%** dos confrontos. É a mesma largura usada pelas classes do xadrez (A, B, C…) há décadas, e é a granularidade em que a diferença é perceptível a olho nu numa quadra.

Então:

- **Cada patente = 200 pontos de rating.** Diferença de uma patente ≈ 75% de vitória esperada. Diferença de duas ≈ 91%.
- **Cada divisão = ~67 pontos.** Diferença de uma divisão ≈ 60% de vitória esperada — perceptível, mas não gritante.
- A escada cobre 1000–1999, **centrada em 1500**. Como o Elo é soma zero, a média da liga fica sempre perto do valor de entrada — então o meio da escada precisa ser a média, ou um nível enche e o outro fica vazio. O valor de entrada padrão (1500) cai em **Prata 2**: o degrau do meio, com dois níveis inteiros para cada lado.
- **Corrigir nível mexe sempre no nível de ENTRADA** (na ficha, só admin — D-74). O degrau escolhido vira o `base` (o palpite do cadastro); para quem já jogou, o histórico inteiro **reaplica por cima** (`rebuildAll`) e a patente atual sai do recálculo — **fato de quadra ninguém edita à mão**. A ficha deixa isso explícito (D-86): o seletor é rotulado **ENTRADA**, o nível de **HOJE** aparece ao lado como "não se edita", e ao mexer na entrada o app mostra **antes de salvar** o que o hoje vai virar ("Ouro 3 → Ouro 1 ao salvar") — porque a relação não é monotônica (baixar a entrada pode subir o hoje: as vitórias passam a valer mais) e ninguém deve ser surpreendido. Quem nunca jogou tem `base = elo`, então entra direto no degrau escolhido. Fica no registro de correções ("Ouro 3 → Ouro 1 (entrada Ouro 2 — histórico reaplicado)"); só `base` vai para o banco, Elo e patente são recalculados dele + histórico.
- **A entrada é feita de opiniões (D-95).** O nível de entrada de cada trilha não é um palpite de uma pessoa: é o que sai das **opiniões de quem lança** (admin, moderador, lançador) — uma por pessoa, todas visíveis a todos. Uma opinião vale ela; duas, a **média** (fica no meio: um erro de patente inteira vira meio erro); três ou mais, a **média aparada**: tira a mais alta e a mais baixa e faz a média do resto (com 3 é a mediana, com 4 as duas centrais, com 5 as três centrais — D-96). Uma opinião destoante não puxa a entrada, e as do meio pesam todas. Quando as opiniões **divergem** (desvio mediano de uma patente ou mais — Prata × Diamante, ou Bronze/Ouro/Lenda), a pessoa entra no meio, mas com o **K de quem está sem palpite**: as partidas decidem rápido, e a ficha avisa. Quem vira Jogador, ou sai da liga, leva as opiniões junto — deixam de valer, e o histórico reaplica sem elas. Não se opina sobre si mesmo. **Tirar a própria opinião** é tocar de novo na patente (ou o botão na ficha); o admin pode anular a de qualquer um. Cada mudança de opinião reaplica o histórico por cima da entrada nova, na hora. Tudo fica no registro de correções ("opinou sobre o nível", "anulou as opiniões"). **Sem nível até calibrar.** Quem entra sem um nível dado à mão (cadastro ou admin) não recebe rótulo enquanto calibra (15 partidas no racha curto; 3 rachas na partida única): o rating existe por baixo — monta time, entra na conta dos outros — mas a escada mostra a pessoa em "Sem nível ainda", com o progresso da calibração.

| Patente | Faixa interna de rating |
|---|---|
| Diamante | ≥ 1800 (85 %+ de vitória esperada contra a média) |
| Ouro | 1600 – 1799 (64–75 %) |
| Prata | 1400 – 1599 (a média) |
| Bronze | 1200 – 1399 |
| Ferro | < 1200 |

Fora dessa faixa o jogador fica preso na ponta: rating muito baixo é Ferro 1, muito alto é Diamante 3.

Essa tabela é documentação de engenharia. **Ela não é exposta no app.**

## 4. Como o rating se move (motor interno)

**A unidade não é a partida: é o trecho.** Uma substituição pode mudar bastante o nível dos dois lados — quem entrou não jogou o que quem saiu jogou. Então o motor quebra a partida em **trechos**: cada formação em campo é um trecho próprio, com placar contado a partir da troca e com o set novo de jogadores. É o mesmo espírito do **+/- da NBA**: importa o que você faz enquanto está em quadra e contra quem. *Se o seu time foi mal enquanto você estava no banco, isso não te afeta.*

Regras do trecho:

- **Fecha trecho:** qualquer substituição (inclusive a do atrasado que entra no meio) e qualquer troca de goleiro — quem está no gol muda o nível dos dois lados.
- **Trecho cortado por uma troca só conta se durou pelo menos 3 minutos — ou um terço da partida, o que for menor.** O limite é relativo de propósito: num racha de 7 minutos, 3 minutos fixos ainda descartariam trocas normais. Menos que isso, o trecho é descartado e ninguém ganha nem perde nada por ele. (Os 3 min são configuráveis nos ajustes da liga.)
- **Trecho curto sem gol não conta para ninguém — nem o final.** Com mais de um trecho, qualquer trecho com menos de **20 % da partida** e **sem gol** é descartado, mesmo que seja o que termina no apito (uma troca a 40 segundos do fim não cria uma "partida" de 40 segundos). Se o trecho final foi descartado, **o resultado da partida vai para o maior trecho que conta**. Com gol, o trecho curto conta.
- **Os trechos que contam dividem a partida em partes iguais.** Dois trechos válidos = K/2 em cada; três = K/3. A partida vale sempre exatamente uma partida, e uma troca no começo não a encolhe.
- **Partida única (longa) tem lógica própria.** Com trocas rolando em 50 minutos, o peso de cada trecho é **a fatia de tempo** que ele ocupou (quem jogou 10 minutos não pesa como quem jogou 40), todo trecho a partir do mínimo absoluto (3 min) conta — com ou sem gol — e o final conta sempre. A partida (vitória/derrota, contagem) só vai para quem esteve em quadra por **pelo menos 25 % do tempo que conta**: quem entrou 3 minutos mexe no rating pelo trecho dele, mas não "jogou a partida".
- **Vitória e derrota são da partida, não do trecho.** Quem esteve em quadra em algum trecho que conta recebe o resultado final da partida uma vez (pelo lado em que terminou) — nas contagens de V/E/D, forma, partidas jogadas, duelos e parcerias. Trecho serve para o rating saber quem estava em quadra e com que peso; não é uma partida própria.
- Vale igual para a partida longa: 50 minutos com muitas substituições viram muitos trechos, cada um com o seu peso e o seu placar.

Dentro de cada trecho, Elo por time:

```
Ra = média do rating dos que estão em quadra pelo time A
Rb = média do time B
Ea = 1 / (1 + 10^((Rb − Ra)/400))          ← chance esperada de A vencer
S  = 1 vitória | 0,5 empate | 0 derrota    ← pelo placar DO TRECHO
Δ  = round( K × (S − E_do_seu_time) × peso_do_trecho )
```

- **Só resultado move a patente.** Gol, assistência e defesa são estatística de vitrine — nunca entram na conta. Artilheiro de time que perde não sobe; zagueiro que só ganha, sobe.
- **Ganhar de quem é mais forte rende muito; de quem é mais fraco, quase nada.** É o mesmo espírito do rating do CS2.
- **Cada um pontua na patente do papel que fez naquele trecho** — quem estava no gol move a patente de goleiro, o resto move a de linha (seção 3.7).

**K pelo modo do racha.** Não existe controle separado de "ritmo": o peso de cada partida sai direto do modo escolhido na abertura daquele racha, porque é ele que determina quantas partidas cabem numa noite. (**Formato** é sempre 5v5/6v6/7v7/11v11; **modo** é várias curtas ou partida única.)

| Modo da liga | K ao entrar (sem / com palpite) | K assentado (depois de 3× a calibração) | Unidade e peso |
|---|---|---|---|
| **Várias curtas** *(padrão)* | 64 / 32 | 20 (em 45 partidas) | trecho; K/n por partida (D-37) |
| **Partida única** | 64 / 32 | 20 (em 9 rachas) | confronto; K × fatia de tempo, placar por margem (D-45) |

> **K por incerteza (D-82, 01/09/2026; reescreve os números da D-55).** O K de cada trilha não é fixo: é alto quando o app sabe pouco daquela pessoa e assenta conforme ela joga — a ideia do Glicko/TrueSkill traduzida para o motor. Quem entra **sem opinião** começa em 64; quem entra **com opiniões que concordam** começa em 32 (o app confia nelas); com opiniões **divergentes**, 64, como quem está sem palpite (D-95); os dois descem linearmente até o piso de **20** ao longo de **3× a calibração** (45 partidas no racha curto; 9 rachas na partida única) e ficam ali (piso 20 e não 16 por causa do vencedor-fica — D-83). Motivo, medido em simulação com o motor real (`scripts/converge.py`): com times equilibrados cada partida dá ±K/2 aos 4–5 do time por igual, e o movimento é quase todo ruído — a K fixo 32 um palpite bom se corrói até o piso de ruído (~100 pts, 1,5 divisão) em poucos meses; a 16 ele se preserva e refina. Um K menor "prende" um palpite errado só nos primeiros ~5 meses e depois o corrige melhor que o 32 (que estaciona no ruído); para esse caso o remédio é a correção do admin, na ficha (seção 3.8) — o app não tem como avisar antes (D-94). O rótulo *calibrando* continua sendo sobre mostrar a patente (15 partidas / 3 rachas), não sobre o K.

> **K de jogo de time (D-55, 29/08/2026; reescreve os números da D-46).** Em time equilibrado a expectativa é a média dos dez em quadra — o sinal individual dilui, e o 40/20 da FIDE (feito para 1×1) converge devagar demais. A referência testada em escala para jogo de time é o Elo do Faceit (CS2): K fixo ≈50 (±25 por vitória parelha) com níveis de ~200 pontos, como a nossa patente. Aqui: **base 32** (o K padrão fora da FIDE — USCF/online) e **64 na calibração** — ±16 e ±32 por vitória parelha, a mesma banda do Faceit, mantendo o desenho "dobro enquanto calibra". Continua sem acelerador de sequência e sem decaimento por histórico. O que separa os dois modos não é o K, é a unidade e o peso.

> **Formato e modo são da liga (D-44).** Tamanho do time (5v5, 6v6, 7v7, 11v11) e modo (várias curtas ou partida única) se escolhem na criação da liga e não mudam depois — grupo que muda de formato cria outra liga. Cada partida ainda **guarda** o modo com que foi jogada (o histórico antigo, de quando o modo era do racha, continua valendo).

**Em lançamento retroativo** (partida digitada depois, sem cronômetro) não há trechos: a partida entra inteira, com peso 1. Na prática é o que acontece com qualquer partida encerrada com menos de **45 segundos** de relógio — o app entende que o cronômetro não foi usado.

> **Trecho × partida.** O rating anda por trecho (com o peso 1/n); a proteção pós-promoção (3.5) também conta trechos. Já calibração (3.6), partidas jogadas, V/E/D, forma e estatística (seção 5) contam **partidas de relógio**: numa partida com duas substituições válidas, o jogador que ficou o tempo todo conta **uma** partida, não três.

> **Partida única: nível por confronto e por margem (D-45).** Na liga de partida única, trechos com **a mesma escalação dos dois lados** (e mesmos goleiros) se juntam num confronto só — quem sai e volta contra o mesmo time não vira dois jogos. O placar do confronto vale **por margem**, saturando: 0-0 é meio a meio (0,50), 1-0 vale 0,73 para quem fez, 2-0 0,88, 3-0 0,95. Gol importa muito, mas 5-0 não vale cinco vezes 1-0. Empatar com um time pior em quadra custa pontos ao melhor e rende ao pior, como no Elo. O peso continua sendo a fatia de tempo. No racha curto nada muda: trecho = unidade, V/E/D inteiro, peso 1/n (D-37).

## 5. Anti-ioiô: como a patente sobe e desce sem oscilar

Alternar entre duas patentes toda semana destrói a graça do sistema. Três mecanismos, todos testados:

1. **Margem de promoção/rebaixamento (histerese).** Passar do corte não basta: é preciso passar **do corte + margem** para subir, e cair **abaixo do corte − margem** para descer. A margem vale em **todo degrau**, e o degrau que importa é a divisão: ~67 pontos. Por isso ela é calibrada contra esse número, e não contra os 200 da patente — margem grande demais não estabiliza, trava. E ela acompanha o K: precisa ser **maior que meia vitória parelha** (K/2 = 16), senão alternar V-D-V-D em volta de um corte viraria ioiô. Com a margem padrão de **21 pontos** (D-55), quem oscila menos que isso em volta de um corte **não muda de degrau**, e a banda efetiva fica em ~109 no lugar de 67.
2. ~~Proteção pós-promoção~~ — **removida (D-46)**: com 10 a 15 partidas por racha, 3 trechos de proteção nem se percebiam.
3. **A patente é um estado, não um cálculo.** Ela fica guardada no jogador e só muda quando as condições acima são satisfeitas — não é recalculada do rating a cada tela.

Os valores são **fixos e iguais em toda liga**: margem **21** (banda efetiva de ~109 pontos, pouco mais de um degrau e meio). Não existe controle de "estabilidade" de propósito: se cada liga pudesse escolher, a mesma escada significaria coisas diferentes em lugares diferentes — e a opção era, na prática, uma pergunta que ninguém sabia responder.

Ordem de grandeza no racha curto, assentado (K=20, times parelhos): mover uma **divisão** exige cerca de **7 vitórias líquidas** (vitórias menos derrotas, já contando a margem), acumuladas ao longo das noites; uma **patente** inteira, cerca de 20. Ao entrar sem palpite (K=64) é a quarta parte disso; com palpite (K=32), a metade — e o K desce conforme a pessoa joga (D-82).

## 6. Entrada de um jogador novo

O padrão do cadastro é **sem nível**: o jogador entra no rating de entrada e o app descobre o nível dele na calibração (15 partidas no racha curto; 3 rachas na partida única), sem rótulo até lá. Quem conhece dá **a sua opinião** (um toque: Bronze … Lenda, só o nível — vale como a divisão 2); é a primeira de várias: qualquer pessoa que lança pode dar a dela depois, na ficha ou na tela **Minhas opiniões** (aba Jogadores), e a entrada fica no meio (seção 3.4, "A entrada é feita de opiniões"). O nível aparece desde o início.

O jogador fica **calibrando** até completar **15 partidas** (liga de várias curtas) ou **3 rachas** (liga de partida única). Nesse período o K é o dobro (64 no lugar de 32) e as margens de histerese não valem, então ele anda rápido e acha o lugar dele em uma ou duas noites.

A calibração vale **por patente**: quem tem 200 partidas de linha e vai para o gol pela primeira vez começa **calibrando no gol**, e a patente de goleiro dele acha o lugar em poucas partidas em vez de levar meses.

A regra é por modo de propósito: numa liga de **partida única** ele levaria semanas para calibrar se dependesse de partidas — então são 3 rachas; numa de **várias curtas** cada pessoa joga de 5 a 10 partidas por noite (no primeiro racha real o máximo foi 7) — então são 15 partidas, cerca de duas noites (D-53; era 25, que segurava a patente por um mês).

A opinião inicial de quem conhece o jogador **já é melhor que sorteio no olho** e a calibração corrige em poucas partidas. Esperar "dados suficientes" para ser útil é o mesmo que não ter app. E a régua da D-94 mostrou o limite: um erro grosseiro de uma pessoa só (o que "domina a bola" mas não decide, o que erra gol mas faz muitos) leva meses para os dados corrigirem — por isso a entrada é a **soma de olhares**: onde uma pessoa erra grosso, outras discordam, e a divergência é justamente o sinal que os resultados não dão.

## 7. Goleiro — duas patentes, não um interruptor

O caso real: **2 ou 3 goleiros para 12 a 16 jogadores de linha**. Eles não pertencem a um time — trocam de lado o tempo todo. E dá para ser excelente em um papel e ruim no outro.

- **A régua do goleiro é a mesma da linha** (D-90): o Elo dele entra na média do time igual ao de todo mundo, então "Prata 2 no gol" significa *um time com ele ganha como um time com um jogador de linha Prata 2* — o nível mede contribuição para vencer, não "qualidade de goleiro entre goleiros". Como esse palpite é difícil de dar, o app recomenda **deixar goleiro sem nível**: medido em simulação, um jogador sem palpite numa liga calibrada chega a ±1 divisão do lugar em 53% já no 1º mês e 79% em 6 meses, sem viés — muito melhor do que um palpite errado em uma patente (24% → 43%).
- **Todo jogador tem duas patentes: uma de linha e uma de goleiro.** São independentes: Ouro 2 na linha e Bronze 1 no gol é um resultado normal, não um bug. A aba Jogadores tem um botão para alternar entre as duas escadas.
- **Quem nunca jogou numa das duas não tem patente ali.** Ouro de linha que nunca pegou no gol não aparece na escada de goleiro, e a ficha dele diz *sem patente no gol*. Se ele for para o gol no meio do jogo, entra valendo **uma patente abaixo da entrada padrão** (Bronze 2 na escada padrão — D-110: no gol é mais difícil para quem não é goleiro, e o padrão superestimava o time dele) e começa a construir a patente de goleiro dali — em calibração, com o K de quem não tem palpite. Goleiro fixo entra no padrão, e uma opinião de goleiro sobre qualquer pessoa substitui a entrada automática. O palpite do cadastro vale só para a valência em que a pessoa vai jogar.
- **A patente que anda é a do papel que a pessoa fez naquele trecho.** Quem defendeu move a de goleiro; quem estava na linha move a de linha. Quem foi improvisado no gol por 4 minutos move a de goleiro nesses 4 minutos, e a de linha no resto.
- **O cadastro não define goleiro — o racha define.** Na tela de presença, além de tocar em quem chegou, você toca no 🧤 de quem **veio para ser goleiro hoje**. Isso muda de racha para racha, e muda no meio do racha: o slot 🧤 da tela da partida aceita qualquer um da escalação.
- O que existe no cadastro (`costuma ir ao gol`) é só uma **sugestão**: ao marcar presença, essa pessoa já entra com o 🧤 aceso, e você desmarca se hoje ela veio para a linha.
- **Um goleiro por time ou mais** → cada um fica fixo em um time e assume o gol automaticamente quando o time entra.
- **Menos goleiros que times** (o caso comum) → eles entram no **rodízio**: ficam fora dos times, e a cada partida o app escala um para cada lado, **alternando os lados**. Com 3 ou mais, há revezamento justo por fila.
- **O goleiro ganha e perde patente como todo mundo**, na escada dele. No rodízio isso é justo justamente porque ele alterna de lado: ao longo da noite a patente reflete o desempenho *dele*, não o de um time específico — se ele defende bem, o lado dele vence mais, independente de quem está na frente.
- **Não existe mais o interruptor "goleiro fora do ranking".** Ele existia para resolver um problema que a patente separada resolve melhor: o goleiro convidado não estragava nada, ele só não tinha onde ser medido. Agora tem.
- **Voltar ao rodízio é um toque.** O card de goleiros fica sempre visível na tela de times, alternando **Rodízio ⇄ Fixos nos times** nos dois sentidos.
- Racha em que todo mundo reveza no gol: não marque ninguém no 🧤 e ignore o slot — ou marque a cada partida quem pegou, e cada um vai construindo a patente de goleiro dele.

## 8. Quem enxerga as patentes

A escada é motivação para uns e constrangimento para outros. Então a Liga escolhe, nos ajustes, entre:

- **Todo mundo vê** *(padrão)* — a aba Jogadores mostra a escada completa para qualquer um.
- **Só o admin vê** — para os outros, a aba Jogadores vira uma lista de estatísticas (rachas, partidas, gols) sem patente nenhuma, e as patentes somem também da presença, dos times e do resumo do fim do racha. O equilíbrio continua funcionando igual: o app segue montando os times pelo nível, só não conta a ninguém qual é.

**As opiniões seguem a mesma regra.** Onde a patente aparece, a ficha mostra a **entrada** (badge, quantas opiniões, se é média ou mediana), o **hoje**, o aviso de divergência e a lista de opiniões com o nome de quem deu cada uma — para todo mundo, de qualquer papel. Quem lança vê também a escada da própria opinião (na ficha) e o card **Minhas opiniões** na aba Jogadores. Ele abre **uma pessoa por vez, num cartão**: avatar, nome, o nível de hoje, e as **cinco patentes como opções** — o badge de metal e, ao lado, uma frase curta do que cada uma representa em termos do que o *time ganha* com a pessoa em quadra ("bem abaixo da média: o time tem que carregar" · "abaixo da média: o time cobre algo por ele" · "a média do racha; na dúvida, é aqui" · "acima da média: faz falta quando não vem" · "o melhor da quadra: sozinho vira o jogo; raro"), porque é essa a régua do nível (D-90) e é o que corrige o olhar do drible. **O cartão inteiro cabe na tela de um celular sem rolar** (D-120): as frases são de uma linha no computador e duas no celular, e o que os outros opinaram fica na ficha da pessoa, não no cartão — a pergunta aqui é a *sua* opinião. Um toque salva e passa para a próxima pessoa ainda sem a sua opinião; "‹ Anterior" e "Pular ›" andam na ordem, que é fixada ao abrir (quem falta primeiro). A sexta opção é **"Não sei"** (nunca vi jogar direito): conta como resposta dada — a pessoa sai da sua lista de pendentes — mas fica fora da conta da entrada. Com **5 ou mais** opiniões pendentes, o card e a aba Jogadores **pulsam** devagar até você ir lá — e o caminho é guiado até o último passo: o card diz onde falta ("faltam 12 na linha · 2 no gol"), o toque abre a folha **na posição em que falta** e **na primeira pessoa pendente**, o seletor Linha/Gol mostra quantas faltam em cada, e o cartão de "todas dadas" oferece ir para a outra posição quando lá ainda falta. Embaixo, a lista de todos com a sua opinião ao lado, para conferir e voltar a qualquer um. A nota é dada **onde a pessoa joga**: na aba Linha os cartões são só de quem joga na linha; na aba Gol, só de quem vai ao gol (costuma, ou já pegou). Os outros aparecem no fim da lista, apagados e sem cartão — tocar abre a ficha. Com as patentes fechadas, some tudo.

O rating numérico é quase invisível: na aba Jogadores, **só o admin** vê o Elo cru de cada um, num número pequeno e apagado no canto da linha (com a dica "Elo — só o admin vê"). **Não existe aviso de "palpite errado"** (D-94, que removeu o da D-83). Medido com o motor real (`scripts/aviso.py`): o ranking de surpresa dos últimos 8 rachas apontava quem estava uma patente fora em 29% dos rachas — e quem estava certo em 29% também; nem a persistência (apontado em 4 dos últimos 8) nem a deriva do Elo desde a entrada separam os dois. Com times equilibrados, uma partida de 5v5 diz ~0,07 sobre uma pessoa; um erro de uma patente inteira leva uns 5 meses para o motor corrigir sozinho, e não há regra que enxergue antes. Um aviso que erra 5 em 6 ensina a ser ignorado, ou, pior, leva o admin a tirar o palpite de quem estava certo. O que a ficha do admin mostra é fato: a **entrada** (o palpite) e o **hoje**, lado a lado — quando os dois divergem por meses, quem conhece o jogador decide. As linhas dos rankings da aba Stats abrem a ficha, para a correção ser um toque. Para todo o resto — e para todos os outros papéis — o número não existe: a linguagem pública é a patente.

**A ordem dentro do degrau também muda com quem olha.** A escada é sempre agrupada por patente e divisão. Dentro de uma divisão, o **admin** vê a lista ordenada por **Elo** (do maior para o menor) — é a ordem verdadeira, e ele já enxerga o número mesmo. Para todos os outros a ordem continua sendo **aproveitamento, depois nome**, para a posição na lista não denunciar o rating de ninguém. O bloco "Sem nível ainda" segue a mesma regra: Elo para o admin, e número de partidas — quem está mais perto de sair da calibração — para os outros.

## 9. O que a patente garante, medido

Tudo acima é regra. Isto é medida: o motor real posto para rodar em ligas simuladas com habilidade verdadeira escondida (os estudos estão em [Estudos](../tecnico/estudos.md)).

**O que a patente garante, medido (D-113).** Com o motor real em simulação (`scripts/confianca.py`), quem já calibrou está a **±2 divisões** da verdade em 97% dos casos (palpites bons) ou 92% (palpites mistos); a ±1 divisão, 80% / 69%; na patente exata, 71% / 66%. Nenhum sinal observável — volume de partidas, estabilidade, circulação na patente — separa quem está certo de quem não está, por isso **não existe símbolo de "confiança"** além do "calibrando": calibrou é o sinal. Entre duas pessoas, **3 divisões de diferença mostrada** dizem que a de cima é mais forte em 91–96% dos pares (1 divisão: 66–72%, quase cara ou coroa), mas a diferença real só é de uma patente inteira em um terço deles.

**Diferença que se sustenta no tempo (D-115).** A régua acima é um retrato. Se a diferença **se mantém** — ao longo de um trimestre inteiro de racha, a menor diferença mostrada entre A e B foi de X divisões (`scripts/consistencia.py`, 3 meses de racha seguidos de mais 3) — ela vale mais: **1 divisão mantida** diz "mais forte" em 80–88% dos pares (palpites mistos / bons), contra 68–72% do retrato; **2 divisões mantidas**, 90–96% (retrato 81–87%); **3 divisões mantidas**, 95–99% (retrato 91–96%). Ou seja: um trimestre de consistência vale mais ou menos uma divisão a mais no retrato. "Uma patente inteira melhor" continua **não** garantida: com 3 divisões mantidas, a diferença real é de uma patente em 48–55% dos pares (retrato: 32–33%); só a partir de 5 divisões mantidas passa de 90%. Meio ano de consistência acrescenta 3–5 pontos, não mais.
