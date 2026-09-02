# Raxa — patentes e times para futsal / fut7 / pelada

> Documento de funcionamento do produto. Protótipo funcional em `index.html`.
> Requisitos detalhados em [REQUISITOS-FUNCIONAIS.md](REQUISITOS-FUNCIONAIS.md) e [REQUISITOS-NAO-FUNCIONAIS.md](REQUISITOS-NAO-FUNCIONAIS.md).
> Regras de quadra (fila, vencedor fica, quem completa) em [REGRAS-DO-RACHA.md](REGRAS-DO-RACHA.md).
> O porquê de cada decisão, com o que foi descartado, em [DECISOES.md](DECISOES.md).
> Modelo de dados da v2 em [BANCO-DE-DADOS.md](BANCO-DE-DADOS.md).

---

## 1. O problema

Todo racha tem os mesmos três atritos:

1. **Dividir os times leva 10 minutos** e sempre gera discussão ("esse time tá muito forte").
2. **Ninguém registra nada.** No fim do ano ninguém sabe quem ganhou mais, quem fez mais gol, quem evoluiu.
3. **Registrar dá trabalho.** Um racha que troca a cada 2 gols ou 7 minutos tem **10 a 15 partidas por noite**. Qualquer app que peça mais de 2 toques por partida morre no primeiro dia.

A regra de ouro do produto:

> **Ninguém precisa dizer quem ganhou.**
> Você marca os gols enquanto eles acontecem (1 toque cada) e toca em **Fim**. O placar decide o resultado — inclusive o 0-0, que é empate. Autor do gol, substituições, nomes de time, goleiro: tudo opcional, nada bloqueia o fluxo.

---

## 2. Conceitos e nomenclatura

| Conceito | Nome adotado | O que é |
|---|---|---|
| Contexto de racha | **Liga** | O universo isolado de patentes. Todo jogador, ranking e histórico vive dentro de uma Liga. |
| O evento do dia | **Racha** (sessão) | "Quinta 20h, quadra do Zé". Agrupa as partidas daquela noite. |
| Confronto | **Partida** | Time A x Time B, do apito ao apito, com um placar. |
| Formação em campo | **Trecho** | O pedaço da partida em que os 10 (ou 8, ou 14) em quadra são exatamente os mesmos. Toda substituição fecha um trecho e abre outro. **É o trecho que move patente**; vitória e derrota, porém, são da partida. |
| Pessoa dentro da liga | **Jogador** | Perfil com patente, estatísticas e histórico. |
| Conta de verdade | **Usuário** | Login que pode *assumir* perfis de Jogador em Ligas diferentes. |

**Por que "Liga" e não "racha"?** Porque o nível não pertence ao evento, pertence ao grupo de pessoas. Se você joga terça no society e quinta no futsal com **as mesmas pessoas**, é a mesma Liga com dois rachas por semana. Se a galera de quinta é outra, é **outra Liga** — e o mesmo jogador terá patentes independentes nas duas. Isso é proposital: Ouro na pelada do trabalho não é Ouro no fut7 competitivo de domingo.

*Alternativas descartadas: Panela, Circuito, Roda, Comunidade, Grupo.*

---

## 3. Patentes — o coração do produto

### 3.1 O princípio inegociável: o número não existe para o jogador

Por baixo há um rating numérico (Elo). **Ele nunca aparece para quem joga.** Não aparece o valor, não aparece a distância para o próximo corte, não aparece quantos pontos a partida rendeu. A única exceção é o **admin** (D-52): na aba Jogadores ele vê o Elo cru num número pequeno e apagado no canto de cada linha — ferramenta de gestão para conferir a montagem e a convergência, não linguagem do racha.

Por quê:

- **Número vira fofoca e briga.** "Você tem 1487" é discussão; "você é Prata 2" é identidade.
- **O corte exposto vira jogo.** Se as pessoas sabem que faltam 12 pontos, elas passam a escolher partida em vez de jogar.
- **Patente é aspiracional, ponto é contábil.** O que faz alguém querer voltar na quinta é subir de patente, não somar pontos.

O que o app mostra a todo mundo é sempre: **patente + divisão**, a campanha (V/E/D) e o momento em que alguém sobe ou cai. Gols e forma recente ficam na ficha e na aba Stats — a escada é sobre nível (D-84). Fora da linha discreta do admin, o rating só existe no backup/servidor, como dado técnico.

### 3.2 A escada

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

### 3.3 Onde ficam os cortes (e por quê)

A referência é o próprio Arpad Elo: ele desenhou o sistema com **intervalo de classe de 200 pontos**, a distância em que o jogador mais forte vence cerca de **75%** dos confrontos. É a mesma largura usada pelas classes do xadrez (A, B, C…) há décadas, e é a granularidade em que a diferença é perceptível a olho nu numa quadra.

Então:

- **Cada patente = 200 pontos de rating.** Diferença de uma patente ≈ 75% de vitória esperada. Diferença de duas ≈ 91%.
- **Cada divisão = ~67 pontos.** Diferença de uma divisão ≈ 60% de vitória esperada — perceptível, mas não gritante.
- A escada cobre 1000–1999, **centrada em 1500**. Como o Elo é soma zero, a média da liga fica sempre perto do valor de entrada — então o meio da escada precisa ser a média, ou um nível enche e o outro fica vazio. O valor de entrada padrão (1500) cai em **Prata 2**: o degrau do meio, com dois níveis inteiros para cada lado.
- **Corrigir nível mexe sempre no nível de ENTRADA** (na ficha, só admin — D-74). O degrau escolhido vira o `base` (o palpite do cadastro); para quem já jogou, o histórico inteiro **reaplica por cima** (`rebuildAll`) e a patente atual sai do recálculo — **fato de quadra ninguém edita à mão**. A ficha deixa isso explícito (D-86): o seletor é rotulado **ENTRADA**, o nível de **HOJE** aparece ao lado como "não se edita", e ao mexer na entrada o app mostra **antes de salvar** o que o hoje vai virar ("Ouro 3 → Ouro 1 ao salvar") — porque a relação não é monotônica (baixar a entrada pode subir o hoje: as vitórias passam a valer mais) e ninguém deve ser surpreendido. Quem nunca jogou tem `base = elo`, então entra direto no degrau escolhido. Fica no registro de correções ("Ouro 3 → Ouro 1 (entrada Ouro 2 — histórico reaplicado)"); só `base` vai para o banco, Elo e patente são recalculados dele + histórico.
- **A entrada é feita de opiniões (D-95).** O nível de entrada de cada trilha não é um palpite de uma pessoa: é o que sai das **opiniões de quem lança** (admin, moderador, lançador) — uma por pessoa, todas visíveis a todos. Uma opinião vale ela; duas, a **média** (fica no meio: um erro de patente inteira vira meio erro); três ou mais, a **mediana** (uma opinião destoante não puxa a entrada). Quando as opiniões **divergem** (desvio mediano de uma patente ou mais — Prata × Diamante, ou Bronze/Ouro/Lenda), a pessoa entra no meio, mas com o **K de quem está sem palpite**: as partidas decidem rápido, e a ficha avisa. Quem vira Jogador, ou sai da liga, leva as opiniões junto — deixam de valer, e o histórico reaplica sem elas. Não se opina sobre si mesmo. **Tirar a própria opinião** é tocar de novo na patente (ou o botão na ficha); o admin pode anular a de qualquer um. Cada mudança de opinião reaplica o histórico por cima da entrada nova, na hora. Tudo fica no registro de correções ("opinou sobre o nível", "anulou as opiniões"). **Sem nível até calibrar.** Quem entra sem um nível dado à mão (cadastro ou admin) não recebe rótulo enquanto calibra (15 partidas no racha curto; 3 rachas na partida única): o rating existe por baixo — monta time, entra na conta dos outros — mas a escada mostra a pessoa em "Sem nível ainda", com o progresso da calibração.

| Patente | Faixa interna de rating |
|---|---|
| Diamante | ≥ 1800 (85 %+ de vitória esperada contra a média) |
| Ouro | 1600 – 1799 (64–75 %) |
| Prata | 1400 – 1599 (a média) |
| Bronze | 1200 – 1399 |
| Ferro | < 1200 |

Fora dessa faixa o jogador fica preso na ponta: rating muito baixo é Ferro 1, muito alto é Diamante 3.

Essa tabela é documentação de engenharia. **Ela não é exposta no app.**

### 3.4 Como o rating se move (motor interno)

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

### 3.5 Anti-ioiô: como a patente sobe e desce sem oscilar

Alternar entre duas patentes toda semana destrói a graça do sistema. Três mecanismos, todos testados:

1. **Margem de promoção/rebaixamento (histerese).** Passar do corte não basta: é preciso passar **do corte + margem** para subir, e cair **abaixo do corte − margem** para descer. A margem vale em **todo degrau**, e o degrau que importa é a divisão: ~67 pontos. Por isso ela é calibrada contra esse número, e não contra os 200 da patente — margem grande demais não estabiliza, trava. E ela acompanha o K: precisa ser **maior que meia vitória parelha** (K/2 = 16), senão alternar V-D-V-D em volta de um corte viraria ioiô. Com a margem padrão de **21 pontos** (D-55), quem oscila menos que isso em volta de um corte **não muda de degrau**, e a banda efetiva fica em ~109 no lugar de 67.
2. ~~Proteção pós-promoção~~ — **removida (D-46)**: com 10 a 15 partidas por racha, 3 trechos de proteção nem se percebiam.
3. **A patente é um estado, não um cálculo.** Ela fica guardada no jogador e só muda quando as condições acima são satisfeitas — não é recalculada do rating a cada tela.

Os valores são **fixos e iguais em toda liga**: margem **21** (banda efetiva de ~109 pontos, pouco mais de um degrau e meio). Não existe controle de "estabilidade" de propósito: se cada liga pudesse escolher, a mesma escada significaria coisas diferentes em lugares diferentes — e a opção era, na prática, uma pergunta que ninguém sabia responder.

Ordem de grandeza no racha curto, assentado (K=20, times parelhos): mover uma **divisão** exige cerca de **7 vitórias líquidas** (vitórias menos derrotas, já contando a margem), acumuladas ao longo das noites; uma **patente** inteira, cerca de 20. Ao entrar sem palpite (K=64) é a quarta parte disso; com palpite (K=32), a metade — e o K desce conforme a pessoa joga (D-82).

### 3.6 Entrada de um jogador novo

O padrão do cadastro é **sem nível**: o jogador entra no rating de entrada e o app descobre o nível dele na calibração (15 partidas no racha curto; 3 rachas na partida única), sem rótulo até lá. Quem conhece dá **a sua opinião** (um toque: Bronze … Lenda, só o nível — vale como a divisão 2); é a primeira de várias: qualquer pessoa que lança pode dar a dela depois, na ficha ou na tela **Minhas opiniões** (aba Jogadores), e a entrada fica no meio (seção 3.4, "A entrada é feita de opiniões"). O nível aparece desde o início.

O jogador fica **calibrando** até completar **15 partidas** (liga de várias curtas) ou **3 rachas** (liga de partida única). Nesse período o K é o dobro (64 no lugar de 32) e as margens de histerese não valem, então ele anda rápido e acha o lugar dele em uma ou duas noites.

A calibração vale **por patente**: quem tem 200 partidas de linha e vai para o gol pela primeira vez começa **calibrando no gol**, e a patente de goleiro dele acha o lugar em poucas partidas em vez de levar meses.

A regra é por modo de propósito: numa liga de **partida única** ele levaria semanas para calibrar se dependesse de partidas — então são 3 rachas; numa de **várias curtas** cada pessoa joga de 5 a 10 partidas por noite (no primeiro racha real o máximo foi 7) — então são 15 partidas, cerca de duas noites (D-53; era 25, que segurava a patente por um mês).

A opinião inicial de quem conhece o jogador **já é melhor que sorteio no olho** e a calibração corrige em poucas partidas. Esperar "dados suficientes" para ser útil é o mesmo que não ter app. E a régua da D-94 mostrou o limite: um erro grosseiro de uma pessoa só (o que "domina a bola" mas não decide, o que erra gol mas faz muitos) leva meses para os dados corrigirem — por isso a entrada é a **soma de olhares**: onde uma pessoa erra grosso, outras discordam, e a divergência é justamente o sinal que os resultados não dão.

### 3.7 Goleiro — duas patentes, não um interruptor

O caso real: **2 ou 3 goleiros para 12 a 16 jogadores de linha**. Eles não pertencem a um time — trocam de lado o tempo todo. E dá para ser excelente em um papel e ruim no outro.

- **A régua do goleiro é a mesma da linha** (D-90): o Elo dele entra na média do time igual ao de todo mundo, então "Prata 2 no gol" significa *um time com ele ganha como um time com um jogador de linha Prata 2* — o nível mede contribuição para vencer, não "qualidade de goleiro entre goleiros". Como esse palpite é difícil de dar, o app recomenda **deixar goleiro sem nível**: medido em simulação, um jogador sem palpite numa liga calibrada chega a ±1 divisão do lugar em 53% já no 1º mês e 79% em 6 meses, sem viés — muito melhor do que um palpite errado em uma patente (24% → 43%).
- **Todo jogador tem duas patentes: uma de linha e uma de goleiro.** São independentes: Ouro 2 na linha e Bronze 1 no gol é um resultado normal, não um bug. A aba Jogadores tem um botão para alternar entre as duas escadas.
- **Quem nunca jogou numa das duas não tem patente ali.** Ouro de linha que nunca pegou no gol não aparece na escada de goleiro, e a ficha dele diz *sem patente no gol*. Se ele for para o gol no meio do jogo, entra valendo o **nível de entrada padrão** e começa a construir a patente de goleiro dali — em calibração, como todo mundo. O palpite do cadastro vale só para a valência em que a pessoa vai jogar.
- **A patente que anda é a do papel que a pessoa fez naquele trecho.** Quem defendeu move a de goleiro; quem estava na linha move a de linha. Quem foi improvisado no gol por 4 minutos move a de goleiro nesses 4 minutos, e a de linha no resto.
- **O cadastro não define goleiro — o racha define.** Na tela de presença, além de tocar em quem chegou, você toca no 🧤 de quem **veio para ser goleiro hoje**. Isso muda de racha para racha, e muda no meio do racha: o slot 🧤 da tela da partida aceita qualquer um da escalação.
- O que existe no cadastro (`costuma ir ao gol`) é só uma **sugestão**: ao marcar presença, essa pessoa já entra com o 🧤 aceso, e você desmarca se hoje ela veio para a linha.
- **Um goleiro por time ou mais** → cada um fica fixo em um time e assume o gol automaticamente quando o time entra.
- **Menos goleiros que times** (o caso comum) → eles entram no **rodízio**: ficam fora dos times, e a cada partida o app escala um para cada lado, **alternando os lados**. Com 3 ou mais, há revezamento justo por fila.
- **O goleiro ganha e perde patente como todo mundo**, na escada dele. No rodízio isso é justo justamente porque ele alterna de lado: ao longo da noite a patente reflete o desempenho *dele*, não o de um time específico — se ele defende bem, o lado dele vence mais, independente de quem está na frente.
- **Não existe mais o interruptor "goleiro fora do ranking".** Ele existia para resolver um problema que a patente separada resolve melhor: o goleiro convidado não estragava nada, ele só não tinha onde ser medido. Agora tem.
- **Voltar ao rodízio é um toque.** O card de goleiros fica sempre visível na tela de times, alternando **Rodízio ⇄ Fixos nos times** nos dois sentidos.
- Racha em que todo mundo reveza no gol: não marque ninguém no 🧤 e ignore o slot — ou marque a cada partida quem pegou, e cada um vai construindo a patente de goleiro dele.

### 3.8 Quem enxerga as patentes

A escada é motivação para uns e constrangimento para outros. Então a Liga escolhe, nos ajustes, entre:

- **Todo mundo vê** *(padrão)* — a aba Jogadores mostra a escada completa para qualquer um.
- **Só o admin vê** — para os outros, a aba Jogadores vira uma lista de estatísticas (rachas, partidas, gols) sem patente nenhuma, e as patentes somem também da presença, dos times e do resumo do fim do racha. O equilíbrio continua funcionando igual: o app segue montando os times pelo nível, só não conta a ninguém qual é.

**As opiniões seguem a mesma regra.** Onde a patente aparece, a ficha mostra a **entrada** (badge, quantas opiniões, se é média ou mediana), o **hoje**, o aviso de divergência e a lista de opiniões com o nome de quem deu cada uma — para todo mundo, de qualquer papel. Quem lança vê também a escada da própria opinião (na ficha) e o card **Minhas opiniões** na aba Jogadores, que abre a lista de todo mundo com um toque por pessoa e conta quantas faltam. No topo da lista, em vez de instruções, a **legenda do que cada patente representa** — em termos do que o *time ganha* com a pessoa em quadra (bem abaixo da média · abaixo · a média, onde a maioria está · acima · muito acima, raro), porque é essa a régua do nível (D-90) e é o que corrige o olhar do drible. A prioridade é dar nota **onde a pessoa joga**: na aba Linha, quem costuma ir ao gol (e nunca jogou na linha) vai para o fim, apagado e fora da conta; na aba Gol, o contrário. Com as patentes fechadas, some tudo.

O rating numérico é quase invisível: na aba Jogadores, **só o admin** vê o Elo cru de cada um, num número pequeno e apagado no canto da linha (com a dica "Elo — só o admin vê"). **Não existe aviso de "palpite errado"** (D-94, que removeu o da D-83). Medido com o motor real (`scripts/aviso.py`): o ranking de surpresa dos últimos 8 rachas apontava quem estava uma patente fora em 29% dos rachas — e quem estava certo em 29% também; nem a persistência (apontado em 4 dos últimos 8) nem a deriva do Elo desde a entrada separam os dois. Com times equilibrados, uma partida de 5v5 diz ~0,07 sobre uma pessoa; um erro de uma patente inteira leva uns 5 meses para o motor corrigir sozinho, e não há regra que enxergue antes. Um aviso que erra 5 em 6 ensina a ser ignorado, ou, pior, leva o admin a tirar o palpite de quem estava certo. O que a ficha do admin mostra é fato: a **entrada** (o palpite) e o **hoje**, lado a lado — quando os dois divergem por meses, quem conhece o jogador decide. As linhas dos rankings da aba Stats abrem a ficha, para a correção ser um toque. Para todo o resto — e para todos os outros papéis — o número não existe: a linguagem pública é a patente.

**A ordem dentro do degrau também muda com quem olha.** A escada é sempre agrupada por patente e divisão. Dentro de uma divisão, o **admin** vê a lista ordenada por **Elo** (do maior para o menor) — é a ordem verdadeira, e ele já enxerga o número mesmo. Para todos os outros a ordem continua sendo **aproveitamento, depois nome**, para a posição na lista não denunciar o rating de ninguém. O bloco "Sem nível ainda" segue a mesma regra: Elo para o admin, e número de partidas — quem está mais perto de sair da calibração — para os outros.

---

## 4. Fluxo de uso

### 4.1 Antes — 30 segundos

**Formato.** Um toque: `5v5` (futsal), `6v6` (society), `7v7` (fut7), `11v11` (campo). O formato define quantos cabem por time e é usado para sugerir a quantidade de times.

**Como vai ser hoje.** Dois modelos de racha, um toque:

| Modo | O que muda |
|---|---|
| **Várias curtas** *(padrão)* | alvo de 2 gols ou 7 min, vencedor fica em quadra (empate: com 4 times os dois saem; com 3, fica o que entrou por último — D-39), cada partida pesa pouco no rating — **10 a 15 partidas por noite** |
| **Partida única** | **sempre 2 times**, fixos, com titulares e reservas; uma partida longa (50 min, sem alvo de gols); substituição é a operação principal; cada partida pesa muito mais |

Os dois convivem na mesma Liga: o modo é do racha, não do grupo.

**Presença.** Grade com todos os jogadores da Liga, em **duas colunas mesmo no celular estreito** — chips compactos (42px, nome em 13px com reticências) para o cenário real de "50 cadastrados, achar os 18 de hoje" caber na tela (D-88). A busca tem um **✕** que limpa o campo num toque (achou um, limpa, procura o próximo). Toca no nome de quem chegou — e no arrasto (segurar e pintar), quando o dedo chega à borda da tela ela **rola sozinha**, marcando quem passa por baixo.  Uma Liga pode ter 50 cadastrados e 14 presentes, e o contador fica grande no topo. Os presentes sobem para o começo da lista **quando a tela é redesenhada** — marcar presença não reordena nada embaixo do seu dedo, senão marcar 14 pessoas seguidas viraria uma caça ao nome que pulou de lugar.

- **A lista vem ordenada por quem mais aparece nos rachas.** Quem joga toda semana está sempre nas primeiras linhas; quem apareceu uma vez em março fica no fim. É o que faz achar a galera de sempre sem usar a busca.
- **Ao lado de cada nome tem um 🧤:** toque nele para dizer que essa pessoa **veio para ser goleiro hoje**. Quem tem o hábito já entra marcado, e dá para mudar a qualquer momento — inclusive no meio do racha, em partidas específicas.
- **O badge do chip é o nível do papel de hoje** (D-81), no formato compacto de cor + riscos (sem o nome da patente — com 50 nomes em duas colunas, o nome do nível comia o do jogador; D-88): com o 🧤 aceso aparece a patente de goleiro; apagado, a de linha. Troca na hora ao tocar no 🧤. Quem não tem nível naquele papel fica sem badge. Antes de marcar presença vale o **padrão da pessoa**: quem costuma ir ao gol mostra a de goleiro, o resto a de linha (sem nível no papel de costume, mostra o outro).
- Busca instantânea e **"+ Novo jogador"** que cadastra sem sair da tela (nome + patente + costuma ir ao gol).

### 4.2 Times — 1 toque

O app calcula sozinho quantos times cabem: no formato NvN cada time tem N−1 de linha quando os goleiros revezam. **12 de linha + 2 goleiros em 5v5 → 3 times de 4 + 2 goleiros no rodízio.** Dá para forçar 2, 3 ou 4 times.

**"Equilibrar"** faz:
1. distribui goleiros (um por time) ou separa o rodízio — cada goleiro entra na conta pela **patente de goleiro** dele, e os de linha pela de linha;
2. **escolhe quem fica de fora**, quando sobra gente: uma fatia que atravessa todos os níveis, um sorteado de cada faixa. A fila tem que ser tão equilibrada quanto os times — jogar os piores todos para fora seria o pior jeito de montar um racha;
3. **sorteia o draft com um ruído pequeno no nível de cada um** e monta pelo guloso: o melhor disponível cai sempre no time mais fraco que ainda tem vaga;
4. algumas centenas de trocas 1:1 buscando minimizar a diferença de nível entre os times — e essa parte usa o **nível de verdade**, sem ruído nenhum, preservando tamanho e goleiros;
5. **desmancha panelinha**: uma segunda rodada de trocas que separa quem já jogou junto em outros rachas — mas **só aceita trocas que não estragam o equilíbrio** (margem de 8 pontos internos, invisível em quadra). A prioridade é o equilíbrio; a repetição é critério de desempate.

**Por que o ruído.** Com gente parelha não existe *um* arranjo equilibrado — existem dezenas. Sem ruído, tocar em "Equilibrar" de novo devolveria exatamente os mesmos times, e a única saída seria o sorteio no dádo. Com ele, cada toque dá um arranjo **diferente e igualmente equilibrado**: nos testes, 14 montagens seguidas dão 13 ou 14 times distintos, todos com menos de 10 pontos internos de diferença.

O ruído vive **só dentro do montador**. A chance de vitória do confronto, a barra de equilíbrio e o veredito ("Times equilibrados") usam sempre o nível real — o que você lê na tela não é chutado.

Por que isso importa: se os mesmos quatro caem sempre no mesmo time, o Elo deles vira o Elo *do time* e ninguém descobre o nível individual de ninguém. Misturar as duplas é o que faz a patente convergir para a pessoa.

O resultado aparece **sem número nenhum**: uma barra de equilíbrio e o veredito ("Times equilibrados" / "Leve vantagem: Time B").

**Quantos por time.** No formato NvN cada time entra com N. Quando os goleiros revezam, o time é de N−1 de linha mais o goleiro da vez. A partir daí:

- **time é sempre cheio.** No 5v5 se joga 5 contra 5 — não existe time de 3 esperando a vez, nem lado com um a menos. O app monta quantos times **inteiros** couberem: 10 de linha + 2 goleiros no 5v5 são **2 times de 4 + goleiro** e **2 de fora**, nunca 3 times de 4, 3 e 3;
- **quem não completa um time fica de fora**, num banco compartilhado, e entra por substituição ou completando quem ficou curto. No racha curto ninguém é reserva de um time específico — isso só existe na **partida única**, onde os dois times são fixos a noite inteira;
- **os dois times que entram juntos têm sempre o mesmo número.** Se um time ficou curto (alguém foi embora, alguém foi movido), ele é **completado com quem está de fora** (veja abaixo);
- **só se joga com menos quando não dá dois times cheios**: 8 pessoas no 5v5 viram 4v4, com aviso na tela — e nunca 5x3;
- na **partida única** são **sempre 2 times**: todo mundo dividido entre eles, N em quadra e o resto como reserva do próprio time;
- na **partida única**, dentro do time os **primeiros da lista são os titulares** e o resto aparece marcado como reserva; no racha curto isso não existe — todo mundo do time entra.

| Presentes (formato 5v5) | O que o app monta |
|---|---|
| 12 de linha + 2 goleiros | 3 times de 4, goleiros revezando — ninguém de fora |
| 11 de linha + 2 goleiros | 2 times de 5 (4 + goleiro fixo) e **3 de fora** |
| 10 de linha + 2 goleiros | 2 times de 5 (4 + goleiro fixo) e **2 de fora** |
| 13 sem goleiro marcado | 2 times de 5 e **3 de fora** |
| 16 de linha + 3 goleiros | 4 times de 4, goleiros revezando |
| 8 pessoas | 4v4 — único caso em que se joga com menos, e a tela avisa |
| Partida única, 10 de linha + 2 goleiros | 2 times de 6: 5 em quadra + 1 reserva cada |

**A fila — o "de próximo".** Quem não coube num time inteiro não fica parado: forma a **fila**, e a fila é de pessoas, não de times. Ao fim de cada partida o ciclo é o de todo racha: **quem ganhou fica, quem perdeu sai, e a fila entra no lugar de quem saiu** — primeiro quem está esperando há mais tempo. Se a fila não dá para trocar o time inteiro, **alguns do time que perdeu ficam para completar**: entram 3, ficam 2, normalmente o goleiro e mais um. Quem sai vai para o fim da fila, e sai quem mais jogou na noite — é o que faz a roda girar parelha.

No empate com 2 times ninguém sai automaticamente; se a galera combinar outra coisa, é trocar os times na tela da próxima partida — toque ou arraste (não há botão de girar a fila, D-32). O ciclo inteiro está em [REGRAS-DO-RACHA.md](REGRAS-DO-RACHA.md).

**Completar o time que ficou curto.** Times nascem cheios, mas racha é racha: alguém vai embora no meio, alguém é puxado para outro time. Quando o time da vez entra com menos gente que o outro, ninguém joga em inferioridade e ninguém senta: a tela da próxima partida mostra **quem completa**, escolhido entre os que estão de fora — normalmente quem acabou de sair. Quem completa **joga aquela partida por aquele time e volta para o dele depois**; o rating enxerga isso naturalmente, porque a unidade é o trecho e o trecho guarda quem estava em quadra.

O app **sugere** quem completa (quem menos jogou na noite, para a fila girar), mas **quem decide é você**: toque no nome para tirar e escolher outro, ou toque em *Jogar 4v4 assim* para os dois lados entrarem menores.

Se mesmo assim um time entra incompleto, a tela avisa (“jogando 4v4 — puxe alguém de fora para fechar 5v5”) em vez de esconder o problema.

Cada cartão de time mostra, ao lado do nome, a **patente média do time** (D-87) — a média dos níveis de quem está nele (goleiro pela patente de goleiro), no mesmo badge da escada. É a leitura rápida de "esse time está de que tamanho?" antes da barra de equilíbrio; some com as patentes fechadas (D-52), como tudo que expõe nível.

**Mexer nos times é a operação mais frequente depois da presença**, então ela é a mais visível da tela:

- todos os nomes ficam em botões grandes, e **quem está de fora tem card próprio com contador** — nunca escondido;
- **arraste um nome sobre o outro para trocar de lugar**, ou arraste para dentro de um time, para o card "fora" ou para o card de goleiros — no celular, segure um instante antes de arrastar;
- quem preferir tocar: toca em um jogador e em outro para trocar; toca no espaço de um time (ou no card "fora") para mover;
- enquanto alguém está selecionado, uma barra fixa no topo mostra quem é e permite cancelar;
- "Equilibrar" refaz tudo, 🎲 sorteia ignorando o nível, e os botões 2/3/4 times remontam na hora.

### 4.3 Durante — 1 toque por partida

Cronômetro grande, dois blocos coloridos e os slots de goleiro:

- **Tocar no bloco do time = +1 gol.** Aparece uma tirinha com os nomes daquele time para marcar o autor — toca ou ignora, ela some sozinha em 6s. **Nunca bloqueia.**
- **Os gols ficam listados abaixo do placar**, com minuto e autor: `3'12 — Rodrigo ✕`. Toque no nome para corrigir o autor (ou colocar um que você tinha pulado), e no **✕** para apagar aquele gol específico. É mais direto que um "desfazer" cego, porque você vê exatamente o que está removendo.
- O cronômetro mostra o alvo configurado na Liga ("2 gols ou 7 min") e pisca quando bate. Quando o **tempo** bate, o celular também **vibra e apita**, uma vez por partida: a tela está no chão da quadra e ninguém está olhando para ela. O alvo de gols não apita — é um toque da própria pessoa. O **alvo** é a única coisa que continua sendo da Liga; o **modo** (curtas ou única) é de cada racha.
- **Encerrar é um toque só, e o botão já diz o resultado**: `✓ Fim · Time A 2-1`. Ele grava exatamente o que está no placar e **não pergunta nada** — nem no 0-0, que é gravado como empate. Ninguém precisa tocar no time que venceu: os gols já disseram.
- **Fim sem querer tem volta.** Na tela seguinte, o bloco de partidas de hoje mostra **"↩ Voltar a partida"** enquanto a próxima não começa: apaga o registro e devolve a partida ao relógio exatamente como estava — gols, escalações, times, fila e goleiros do rodízio voltam ao lugar, e o tempo parado entre o Fim e a volta entra como pausa (o relógio não conta o intervalo). É diferente do "↶ Desfazer a última", que apaga a partida de vez, sem devolvê-la ao relógio. Logo depois do Fim, o aviso do placar fica **7 s** na tela com um **↩ voltar** — o erro mais comum se desfaz sem rolar até o bloco de partidas; começar outra partida fecha o aviso.
- **Pausar e cancelar** ficam no topo, como ícones ao lado do relógio: `⏸` congela o relógio (bola na rua, discussão, chuva) e o tempo parado não conta para nada — nem para a duração dos trechos. `✕` joga fora a partida inteira, e **pede confirmação** antes, porque não tem volta. Cancelar devolve o rodízio de goleiros a como estava antes da largada e deixa o **mesmo confronto** sugerido — cancelar quase sempre é "recomeça essa".
- **A barra de baixo tem duas coisas e só duas**: `↶` (desfaz o último gol, troca ou pausa — e, se não houver nada na partida, oferece apagar a partida anterior, **perguntando antes** com o placar dela: um ↶ por reflexo aos 10 s da partida nova não pode apagar a anterior em silêncio) e `✓ Fim · placar`. **"Encerrar racha" não mora aqui**: com o próximo time entrando, um toque errado do lado do "Fim" não pode acabar com a noite. Ele fica na tela entre partidas.
- **O placar é o maior elemento da tela** e ocupa a metade de baixo, no alcance do polegar: tocar no bloco do time é gol, e o `−` no canto tira o último gol daquele lado sem precisar rolar até a lista. O `−` fica numa **zona morta**: tocar perto dele, mas fora, não faz nada (antes virava gol — o contrário da intenção). E **toque duplo não é dois gols**: o segundo toque em menos de 0,6 s é ignorado.
- **A chance de vitória de cada lado** aparece embaixo do placar, em letra pequena: `52% de chance`. É a expectativa do Elo para aquele confronto, atualizada conforme entra e sai gente. Fala do **confronto**, nunca de uma pessoa — e some junto com as patentes quando a liga escolhe deixá-las só para o admin.
- Patentes aplicadas na hora, **trecho por trecho**: quem entrou no meio leva só o que aconteceu depois que entrou. Mas **entre uma partida e outra o app não fala de patente**: encerrar leva direto para a tela da próxima partida, com um aviso curto do placar registrado. Quem subiu e quem caiu aparece **no fim do racha** (seção 4.4) — no meio do jogo isso vira assunto, e assunto atrasa a próxima bola.
- Cada partida do histórico mostra a **chance de cada lado no apito**, colada à esquerda do placar (até o 5v5, o % de cada time na linha dele; acima, `62% × 38%` ao lado do placar único), calculada com o nível que cada um tinha **naquele momento** — é % de confronto, a mesma da pré-partida, e some junto com as patentes quando a liga as fecha (D-75).
- No histórico (aba **Jogos**), as partidas ficam **agrupadas por racha**: uma linha por noite com data, quantas partidas, quantos gols e as contestações — e as partidas aparecem depois de tocar no racha. Uma noite de 12 partidas é uma linha, não doze.
- **Até o 5v5, a partida é identificada por quem jogou, não pela cor do colete**: cada lado aparece como a lista dos primeiros nomes da escalação de largada, com os gols daquele lado ao lado, e o nome do time fica no "venceu ..." da linha de baixo. A fonte é menor para caber; se ainda não couber, o nome quebra para a linha seguinte — nome cortado no meio seria pior. Em ligas maiores (7v7, 11v11) a lista não cabe e vale o nome do time, com o placar no formato `2 - 1`.
- Se o resultado saiu errado: **"Desfazer a última"** no bloco de partidas de hoje resolve, depois de confirmar com o placar (apagar não tem volta, e o botão mora ao lado do "Voltar a partida", que tem); correção fina (mudar o vencedor, anular, apagar) fica no **Histórico → Revisar**, onde dá para olhar com calma depois.
- **Empate: com 4 times os dois saem; com 3, um fica — o que entrou por último** (o que já estava sai, D-39). Não dá para o "vencedor fica" decidir sozinho quando ninguém venceu; com 4 times deixar os dois faria a fila nunca andar, e com 3 tirar os dois esvaziaria a quadra. Com 2 times, empate não muda nada — eles jogam de novo.
- **Entre uma partida e outra existe uma tela inteira: a próxima partida.** Não é um modal que some — é a tela padrão do racha enquanto nada está rolando, e ela mostra:
  - o confronto `Time A VS Time C`, com a **chance de cada lado** e o retrospecto de hoje;
  - **as duas escalações que vão entrar**, editáveis ali mesmo: toque num nome e depois no outro para trocar de lugar (ou arraste), inclusive puxando alguém de um time que está esperando ou de fora;
  - quem está de fora, agrupado por time, e o rodízio de goleiros da vez;
  - `＋ Chegou agora`, `🚑 Foi embora` e `Refazer times` (reequilibrar é refazer os times — não há botão separado).
- **Quem entra é sugestão, não regra.** Tocar em qualquer um dos dois lados troca aquele time por outro (até o 5v5 a folha mostra **os nomes de quem joga** em cada time, não só o apelido da cor — D-60/D-71). O app sugere seguindo "vencedor fica" e a fila de quem está esperando — e **quem venceu (ou ficou no empate) continua do mesmo lado da quadra** em que jogou (D-71); só o lado de quem saiu troca. Mas você decide — inclusive repetir o mesmo confronto ou pular a vez de alguém. Só depois de conferir tudo é que você toca em **▶ Começar partida**.
- **Substituição: arraste ou toque.** Arraste o nome de quem está fora sobre quem está em quadra e a troca acontece (no celular: segure o nome por um instante e arraste; no computador, arraste direto). Se preferir, o toque continua funcionando: toca em quem sai → escolhe quem entra, ou toca em quem está fora → escolhe quem sai. Trocar titular por reserva do mesmo time só inverte os dois.
- **Trocar o goleiro é tocar no slot 🧤.** A folha oferece quem está no rodízio e a opção de improvisar alguém do time. Escolher **o goleiro do outro lado** (marcado como *do outro lado*) faz os dois **trocarem de lugar por inteiro**: cada um passa para o gol e para a escalação do lado novo — inclusive na lista de autor do gol e na conta dos trechos. O mesmo vale no slot 🧤 da tela de próxima partida. `↶` desfaz a troca inteira.
- **Toda troca fecha um trecho** e a tela avisa em letra pequena: `Trecho 2 desde a última troca · 1-0 em 3'20`. O placar do trecho novo é o que vale para quem entrou (seção 3.4).
- **"Chegou agora"** (o atrasado): marca presença e manda direto para um time — ou para o rodízio de goleiros — no meio do racha.
- **"Foi embora"**: quem já jogou hoje (ou está em quadra) sai contando presença (D-49). Quem **ainda não jogou** ganha a escolha: *🚑 Foi embora — esteve no racha* (conta presença) ou *✕ Marquei errado — não veio* (sai sem contar). Presença marcada por engano depois de montar os times não pode virar frequência.
- **Dois celulares na mesma partida.** O racha em andamento é um bloco só no servidor; quando os dois gravam quase juntos, o que chegou depois recebe o estado do outro. Se os dois estão na **mesma partida** (mesmo apito), os eventos se **somam**: gol de um e gol do outro ficam os dois, placar e escalação são refeitos a partir da largada, e autor marcado só aqui vai junto. Se o outro celular já encerrou a partida, vale o dele (o gol atrasado daqui se perde, e o aviso "atualizado por outra pessoa" diz isso). Fora da partida (presença, times) continua valendo o que chegou por último.
- **"Desfazer a última"** fica no bloco de partidas de hoje e reverte a partida inteira, patentes incluídas.

### 4.4 Depois — o resumo

Dá para **cancelar o racha** em vez de encerrar: as partidas já lançadas continuam no histórico e valendo, só a sessão some. Encerrar e cancelar **perguntam antes**: encerrar não tem volta e o botão fica ao lado do "Começar partida"; a pergunta diz quantas partidas foram registradas e, se houver partida rolando, que ela será descartada.

Ao encerrar: partidas jogadas, artilheiro da noite e **a lista de quem subiu e quem caiu de patente** — é o único momento em que o app fala de patente durante um racha, e é de propósito: no fim, vira comemoração; no meio, viraria discussão. É a tela que vai para o grupo do WhatsApp.

---

## 5. Stats: o racha, você e os outros

O ranking responde "quem é o melhor". O que ninguém consegue responder no fim do ano é o resto: *quantas vezes eu joguei contra o Rodrigo? Quem me ganha sempre? Com quem eu ganho mais? Quantos rachas eu peguei esse ano?* A aba **Stats** existe para isso — e ela é sobre você **e** sobre todo mundo, porque metade da graça é comparar.

### 5.1 A unidade: quem estava em quadra

Tudo aqui sai dos **trechos** (seção 3.4), não das partidas. Um **confronto** entre duas pessoas é um trecho em que as duas estavam em quadra **ao mesmo tempo, em lados opostos**; uma **parceria** é um trecho com as duas do mesmo lado.

Duas consequências que importam:

- **Vale igual em qualquer formato.** 1v1, 2v2, 5v5, 1v3 — o que conta é ter estado em campo junto. O histórico do duelo mostra o formato de cada encontro (`5v5`, `3v2`) para dar o contexto.
- **Substituição é respeitada.** Se você saiu aos 4 minutos e o seu time tomou dois depois, aquele trecho não é seu — nem no rating, nem nas estatísticas. É a mesma regra em toda parte.

### 5.2 O painel

**Período:** `Último` (racha), `30 dias`, `2026` ou `Sempre`, com uma quebra **ano a ano** (rachas, partidas, gols e aproveitamento de cada temporada). É a resposta direta para "quantos rachas joguei esse ano" e "e na vida?".

| Bloco | O que mostra |
|---|---|
| **A pessoa** | rachas no período, partidas, aproveitamento, vitórias, gols, partidas no gol, barra V/E/D e as duas patentes — e o card **Partida a partida** (D-76): uma linha por jogo com V/E/D, placar pelo lado da pessoa, a **prob. de vitória** no início do jogo e uma bolinha ⚽ por gol (🙈 por gol contra); paginado de 10 em 10 (‹ recentes · antigas ›) |
| **Duelos** | **Maior carrasco** e **Freguês** em destaque, e a lista de quem você mais enfrenta com V/E/D e barra. Tocar em um nome abre o histórico completo do confronto: data, placar, formato e resultado |
| **Parcerias** | **Mais jogou junto** e **Melhor dupla**, e a lista de quem mais joga do seu lado — também com histórico ao toque |
| **O racha no período** | rankings de presença, campanha, artilharia, ritmo, goleiro, sequência e dupla — 3 linhas cada, abrindo até 10; **a ordem segue o filtro** (30 dias = forma; ano = temporada; sempre = carreira) |

**"Trocar jogador"** abre os mesmos números de qualquer pessoa da liga — dá para conferir o carrasco do outro também.

**🧤 Sem goleiros** (chip ao lado do período): tira o tempo no gol das contas de time — jogos, V/E/D, +/−, tempo em quadra, duelos e parcerias. É a leitura justa para o rodízio, que troca de lado sem escolher o time: vitória de goleiro não diz o mesmo que vitória de linha. Os números *de goleiro* (menos vazado, gols sofridos, tempo no gol) continuam contando normalmente, e gol de goleiro segue valendo na artilharia.

**No período "Último" (um racha):**
- **Presentes** conta quem esteve no racha **desde o começo** — quem foi embora antes do fim continua contando (a sessão guarda a união de quem passou por lá, e rachas antigos são completados por quem aparece nas partidas).
- **Times do racha**: cada time aparece pelos **primeiros nomes dos jogadores originais** (até 5v5; **goleiro de rodízio não entra** — ele roda entre os times, então não é de time nenhum, nem no rótulo nem na conta da maioria abaixo; goleiro **fixo** de um time continua, porque aí ele é do time. Racha antigo, sem a lista do rodízio gravada, é resolvido pela evidência: quem pegou no gol por mais de um time na mesma noite estava rodando) — "Vinashow, Maike, João, Halisson" identifica melhor que "Time A"; o nome do time fica na linha de baixo, junto com os gols no formato **8/3 G** (feitos em verde, sofridos em vermelho). Tocar num time abre **a escalação original da montagem** (com o rodízio de goleiros à parte). Racha gravado antes dessa versão mostra a escalação da primeira partida, que era o que ficou registrado.
- **A vitória é do time que jogou, não do nome no placar.** Um lado da partida só conta como aquele time se **mais da metade dos jogadores originais** dele esteve em quadra em algum trecho. Time inteiro trocado não leva a vitória; se a formação que entrou é a maioria de **outro** time da noite, a partida conta para esse outro (empate de maioria: leva quem passou mais tempo em quadra). Formação que não é maioria de nenhum time não conta para time nenhum — o card avisa quantas foram. Isso vale no card da noite e no "Hoje: ..." da pré-partida; para o jogador, nada muda: V/E/D e nível continuam sendo de quem estava em quadra.
- **Cada ranking da noite** (melhor +/−, quem mais ganhou, artilheiro, rendeu acima, tempo em quadra, menos vazado) mostra 3 e abre **até 10** com o "▾ ver até N" — o mesmo padrão da temporada. E há o ranking de **😵 quem mais perdeu**, com o irmão **Mais derrotas** nos rankings de temporada.

### 5.3 Destaques do mês — e por que não é aproveitamento

A primeira tela do racha mostra os **destaques dos últimos 30 dias** — a foto do mês, não o histórico
inteiro: o "craque da liga" premiava quem começou bem em março e sumiu. São duas listas e dois cards:

1. **Os melhores do racha** — a maior patente **entre quem apareceu no período**. É a escada, filtrada por
   presença: quem some do racha some do pódio. Cada um entra pela **valência que mais jogou no mês** — quem
   passou metade do período no gol aparece com a patente de goleiro. A ordem é degrau, depois aproveitamento,
   depois nome — para qualquer papel, inclusive o admin: este card é a tela que todo mundo abre junto no
   racha, então a posição não denuncia quem está na frente dentro da mesma divisão. (A ordem por Elo do
   admin vale só na aba Jogadores — §3.8.)
2. **Quem mais rendeu além do esperado** — o critério explicado abaixo.
3. **Artilheiro** e **goleiro menos vazado**, lado a lado, mais **quem mais apareceu**.

Cada linha do pódio escreve o que cada número é: `4 rachas · 21 partidas · 62% de aproveitamento`.

**Na segunda lista, o critério não é aproveitamento, e não é vitória.** Num racha com times equilibrados, o aproveitamento de
todo mundo tende a 50% — é justamente o que o app persegue. E contar vitória pura premia quem caiu no time
bom. O critério é o **saldo acima do esperado**:

```
acima do esperado = Σ (resultado do trecho − chance que aquele lado tinha) × peso do trecho
                    resultado = 1 vitória | 0,5 empate | 0 derrota
```

Ou seja: **a mesma conta que move a patente, sem o K** — o que sobra está em vitórias, que é a unidade que
qualquer um entende. **+1,0 quer dizer "uma vitória inteira a mais do que o confronto pedia".**

Por que isso funciona num racha:

- **desconta o time.** Ganhar carregando os mais fracos rende muito; confirmar favoritismo rende pouco. No teste,
  a zebra que vence leva +0,88 e o favorito que confirma leva +0,12 pela mesma vitória;
- **soma zero dentro da partida.** O que um lado ganha acima do esperado, o outro perde — ninguém infla o
  número jogando muito, só rendendo acima do que se esperava dele;
- **respeita substituição**, porque a unidade é o trecho: o que o time fez com você no banco não entra;
- **é acumulado, não média** — num racha, aparecer faz parte do mérito. E o piso é **2 rachas ou 15
  partidas no período** (D-69): duas noites já mostram constância, e uma noite inteira (15 partidas,
  o tamanho da calibração) já mostra volume. Vale igual nos dois modos — na partida única, 2 rachas bastam.

**Artilheiro** só aparece quando a maioria dos gols tem dono (metade ou mais). Autor de gol é opcional de
propósito — e ranking de artilharia com metade dos gols sem dono é pior do que ranking nenhum. Quando falta
dado, o card diz quantos gols ficaram sem autor em vez de premiar quem lembrou de se cadastrar.

**Goleiro menos vazado** é a média de **gols sofridos por partida enquanto ele estava no gol** — também sai dos
trechos, então o goleiro que entrou no meio só leva os gols que tomou. No rodízio isso é justo porque ele
alterna de lado a noite toda.

Com as **patentes fechadas** (seção 3.8) o destaque cai para vitórias no período: "acima do esperado" nasce do
nível de quem estava em quadra, então sai de cena junto com as patentes.

### 5.4 Por que existe um mínimo de partidas

**Aproveitamento é no idioma do futebol: pontos.** V vale 3, E vale 1, e o aproveitamento é a fração dos
pontos disputados que a pessoa levou — (3·V + E) / (3·partidas) (D-69). 100% é só vitória; empatar tudo dá
33%. A % de vitórias pura tratava empate como derrota, e racha empata muito. Vale em todo lugar que diz
"aproveitamento": o anel do painel, os rankings, duelos, parcerias, duplas, a ficha e o desempate da escada.

Aproveitamento com 3 jogos é ruído, e ruído no topo de um ranking destrói a credibilidade dele. Então:

- o ranking de **aproveitamento da liga** só considera quem tem **10 partidas ou mais no período** (e o número aparece escrito na tela);
- nos destaques pessoais (carrasco, freguês, melhor dupla) o piso é menor — 10, ou 10% das suas partidas, o que for menor, nunca abaixo de 3 — porque duelo individual acumula bem mais devagar que partida.

O resto das listas (mais enfrentados, mais jogou junto) não tem piso: elas são ordenadas por **quantidade**, então não têm como ser distorcidas por amostra pequena.

### 5.5 "Quem é você"

Quando alguém assume um perfil (**Sou eu**, na ficha do jogador), o app passa a saber quais partidas são suas:

- na aba **Jogos** (o histórico), as suas partidas ficam com uma **borda verde** e o selo `VOCÊ` do lado em que você jogou, colorido pelo seu resultado;
- um filtro **Todas / Só as minhas** no topo do histórico;
- o painel de Números abre direto em você.

Sem ninguém assumido, nada quebra: o painel abre em quem mais aparece nos rachas e o histórico fica sem marcação.

**Nada disso usa rating.** É contagem de resultado puro — por isso continua visível mesmo quando a liga esconde as patentes. Nesse caso só as duas patentes somem do bloco "A pessoa"; rachas, duelos, parcerias e aproveitamento ficam iguais.

---

## 6. Contestação e correção

Quem lança resultado no meio de um racha erra — e às vezes o outro time discorda. Sem um caminho para reclamar, o histórico perde credibilidade e as pessoas param de lançar.

- **Qualquer participante pode contestar uma partida** pelo histórico (botão ⚑). Uma pessoa contesta uma vez.
- Ao atingir o limite de contestações (padrão **2**), a Liga escolhe o que acontece:
  - **Sinaliza** *(padrão)* — a partida é marcada com ⚑ e continua valendo até alguém revisar;
  - **Suspende** — a partida deixa de valer imediatamente e as patentes são recalculadas sem ela, até um admin decidir.
- **A revisão abre a partida inteira, não só o placar.** Antes dos botões de correção o admin vê: o placar com os dois times, a data, o modo e um resumo (minutos de jogo, quantas pessoas jogaram, gols, trechos que contam); **quem jogou de cada lado**, com tempo em quadra, 🧤 e quanto tempo ficou no gol, gols, gols contra e o que aconteceu com a pessoa na partida (entrou aos 4'30, saiu aos 7'00, saiu e voltou); a **linha do tempo** com cada gol (autor, time, placar corrido), cada substituição (quem saiu, quem entrou), cada troca de goleiro e cada pausa, com o minuto de jogo; os **trechos**, com a escalação dos dois lados, o placar do trecho, se ele conta e com que peso; e o **efeito no nível** de cada um. Linha do tempo vem aberta; trechos e nível abrem com um toque.
- Na revisão, um admin pode: **manter**, **corrigir o resultado**, **anular** (fica no histórico, sem efeito) ou **apagar**. O Editor pode manter e corrigir; anular e apagar são só do admin.
- **Corrigir escalação e trocas** (botão na revisão, só admin) abre a tela que reescreve o que a partida gravou: quem **começou** de cada lado (com o goleiro de largada) e as **trocas** que aconteceram. Dá para (a) dizer que *era outra pessoa* — a troca vale para a partida inteira, inclusive os gols dela; (b) **pôr alguém** que faltava na escalação de largada; (c) **tirar quem não jogou** — as trocas em que ele aparece são apagadas e os gols dele ficam sem autor; (d) marcar quem **começou no gol**; (e) tocar numa troca para corrigir *quem saiu*, *quem entrou* ou **apagá-la**; (f) **＋ nova troca**: minuto (passo de 30 s), time, quem sai e quem entra — ou uma troca de goleiro. Nada disso vale na hora: as mudanças ficam num **rascunho**, a tela lista o que vai mudar e mostra a prévia em **"Como fica"** (os trechos já com a correção). Só o **Salvar** escreve na partida, refaz os trechos com a mesma conta do apito final, registra cada mudança no log e recalcula a liga do zero; **Descartar** (ou fechar a folha) joga o rascunho fora sem deixar rastro. Partida gravada sem cronômetro (versão antiga) não abre a tela.
- Quem entra numa troca é escolhido entre quem **não estava em quadra** naquele minuto (dos dois lados) — ninguém joga dos dois lados na mesma partida. E se, depois de uma correção, o autor de um gol não tiver jogado naquele lado, a linha do tempo marca **⚠ o autor não estava em quadra**: o gol continua valendo, mas o admin vê o que consertar.
- **Toda correção recalcula a liga inteira do zero**, a partir do nível de entrada de cada jogador e de todas as partidas válidas em ordem. Corrigir uma partida de três semanas atrás não deixa resíduo em ninguém — é a mesma matemática rodando de novo. Isso é testado: recálculo do zero bate exatamente com o cálculo incremental.
- Corrigir o vencedor de uma partida com substituições muda **o trecho que fechou a partida** — os trechos anteriores já tinham vencedor próprio, cada um com o seu placar.

- **Dois cadastros da mesma pessoa.** Quem lança na pressa não acha o "Rodrigo" e cadastra outro; o repetido joga uma noite e o histórico se divide. Na ficha de qualquer um dos dois o admin toca em **"⇆ É a mesma pessoa que outro cadastro…"**, escolhe o outro e diz **qual fica**: as partidas, sessões e o racha em andamento do que some passam para quem fica (a conta vai junto, se só um tinha), o cadastro repetido é apagado e os níveis são recalculados do zero. O app **recusa** juntar quem já esteve na mesma partida (são duas pessoas) e quem está ligado a duas contas diferentes. **Entendeu errado, separa:** a ficha de quem ficou lista os cadastros juntados ali com **"Separar de novo"** — recria o cadastro (mesmo id, nome, nível de entrada, conta) e devolve as partidas e sessões dele. Tudo fica no registro de correções ("juntou cadastros" / "separou cadastros").

*A decidir na v2:* se muitas contestações devem **obrigar** revisão antes de a partida valer (hoje é a opção "Suspende") e se a contestação deve exigir um motivo em texto.

---

## 7. Contas, perfis e permissões

### 7.1 Um membro é um jogador — e só um

A regra que organiza tudo nesta seção: **dentro de uma Liga, uma conta corresponde a exatamente um perfil de jogador.** Não existe conta com dois perfis na mesma Liga, nem perfil dividido entre duas contas. Isso é o que faz "quantas vezes eu joguei contra o Rodrigo" ter uma resposta única.

Fora dessa regra, tudo continua valendo: a mesma pessoa tem **patentes independentes em cada Liga**, e um perfil pode existir muito antes de a pessoa ter conta.

### 7.2 Perfil sem dono

Quando alguém cadastra "Bruninho" na tela de presença, nasce um **perfil sem dono**: existe, joga, acumula patente e estatística, mas não pertence a nenhuma conta. Esse é o caso normal — num racha de 16, metade nunca vai abrir o app.

Quando o Bruninho entra na Liga, ele vê os perfis sem dono e **assume o seu**, já com todo o histórico anterior. A partir daí acompanha as próprias patentes em todas as Ligas dele num lugar só. Se alguém assumir o perfil errado, o admin desfaz o vínculo com um toque e o perfil volta a ficar sem dono.

### 7.3 Entrar numa Liga: três caminhos, uma regra

| Caminho | Como é | Quando serve |
|---|---|---|
| **Link de convite** — *ainda não existe (v2)* | o admin gera o link e joga no grupo do WhatsApp; quem abre escolhe o próprio perfil e entra | começar uma Liga, chamar a galera toda de uma vez |
| **Código da Liga** | código curto de 6 caracteres (`RXA7Q2`), visível nos ajustes; quem digita **pede para entrar** e o admin aprova em Membros — **implementado** | alguém que ouviu falar do racha e quer entrar |
| **Busca dentro do app** — *ainda não existe (v2)* | o admin procura a pessoa por `@usuário` ou nome e convida direto — já apontando qual perfil é dela | o mais comum: a pessoa já joga há meses e só agora criou conta |

A regra única, nos três: **ninguém entra sem aceitar, e ninguém entra sem o admin querer.** Hoje só o código existe, e ele **gera pedido, não entrada** — o admin aprova em Membros. O link com vencimento, a entrada livre e o convite direto de uso único são desenho da v2.

Convidar já pode **reservar o perfil**: quem aceita cai direto no lugar certo — *"você é o Bruninho, 42 partidas, Prata 2"* — em vez de escolher numa lista e errar.

### 7.4 O admin manda nos membros

Controle total, sem meio-termo, porque um racha tem dono:

- convidar, revogar convite, aprovar ou recusar pedido;
- **vincular e desvincular** um perfil de uma conta;
- trocar o papel de qualquer membro;
- **remover um membro** — o jogador e todo o histórico dele **ficam**; só o acesso sai;
- cadastrar jogador sem conta nenhuma (o caso normal);
- passar o admin adiante — uma Liga nunca fica sem admin;
- apagar a Liga.

Toda ação de membro fica registrada: quem fez, em quem, quando.

### 7.5 Papéis

| Papel | Pode |
|---|---|
| **Admin** | Tudo: configurar a liga, revisar/corrigir/anular partidas, cadastrar e remover jogadores, juntar cadastros, anular opiniões dos outros, dar papéis |
| **Moderador** | Cadastrar e editar jogadores, montar times e corrigir o resultado de partidas (anular, revisar contestação e apagar são só do admin) |
| **Lançador** | Conduzir o racha: presença, times, partidas, gols, cadastrar jogador — e **opinar sobre o nível** de entrada de qualquer um (como moderador e admin) |
| **Jogador** | **Padrão de quem entra.** Vê ranking, histórico e as próprias estatísticas; vincula o próprio perfil; pode contestar. Não lança nada |

O padrão de quem entra é **Jogador**: só olha. O admin dá **Lançador** a quem conduz o racha (quem está com o celular na mão). Conta ainda sem perfil vinculado também é tratada como Jogador.

**Visibilidade das patentes** (seção 3.8) é decisão do admin: todo mundo vê, ou só ele. Em v1, sem backend, isso vale por aparelho — a checagem já é por papel, e é a mesma que o servidor vai aplicar na v2. No app hoje o que está de fato aplicado é: **admin** = revisar/anular/apagar partida, dar papel, vincular/desvincular conta de outra pessoa, gerenciar contas da liga; **editor** = corrigir resultado de partida (nível é só admin); **lançador** = tudo que é conduzir o racha; **jogador** = só leitura (a checagem é central, no despachante de ações — `ACOES_LANCAR`/`ACOES_ADMIN`).

**Contas sem jogador.** Quem entra na liga pelo código vira *conta* antes de ser *jogador*. Para o admin, o card **Pendências** (aba Jogadores) lista as contas — com jogador ou sem —, e é ali que ele vincula a conta a um perfil sem dono, cria um jogador com o nome da conta ou tira a conta da liga (o jogador e o histórico ficam). Os outros membros veem só os jogadores e se cada um tem perfil atrelado.

---

## 8. Estado do protótipo (`index.html`)

**Revisão mostra a partida inteira e corrige autor de gol.** A revisão (admin) remonta a partida a partir dos trechos e do log de eventos: ficha de quem jogou (tempo em quadra, papel, gols, entrou/saiu), linha do tempo com gols, substituições, trocas de goleiro e pausas, os trechos com escalação e peso, e o efeito no nível. Cada gol da linha do tempo é um botão: tocar abre a escolha entre quem estava em quadra pelo time que marcou (ou pelo outro, na abinha "contra"). A artilharia é recontada e a correção fica no registro.

**Substituição, vaga e "foi embora".** Trocar alguém durante a partida vale só para aquela partida: os times voltam iguais na seguinte (a única troca que fica é titular ⇄ reserva do mesmo time). Time com gente a menos mostra **vagas tracejadas dentro do cartão**: na montagem a vaga puxa alguém da fila ou da reserva de outro time; na pré-partida ela escolhe quem completa só aquela partida (o emprestado aparece no cartão com ✕ e volta para o time dele depois). Quem se machuca ou precisa ir embora sai por **🚑 Foi embora** (botão na pré-partida): sai da presença, do time, da fila e do rodízio; se estava em quadra, a partida segue com um a menos e o trecho seguinte registra isso. Quem ainda não jogou hoje pode sair como **marcado por engano**, sem contar presença.

**Escalação sempre à vista.** Na pré-partida e na partida ao vivo, logo abaixo do nome/placar de cada time, aparece a escalação em duas colunas: o goleiro num slot próprio em cima (🧤, com ↻ se vier do rodízio) e um slot por vaga de linha (5 no 5v5; vaga vazia fica tracejada). Quem não estava no time quando o racha começou (composição original, guardada em "Começar racha") leva um ⇄ discreto — emprestado, completando, substituto ou movido depois. Ao vivo, tocar num nome substitui (ou arraste um reserva/alguém de fora sobre ele); tocar no goleiro troca o goleiro. Na pré-partida a coluna tem o nome do time em cima e as reservas embaixo, e é ali que se edita: toque num nome e depois no outro (ou arraste) para trocar, toque em ⇄ para tirar quem completa, em “＋ completar” para escolher quem entra, e no 🧤 para escolher o goleiro — não há mais seções separadas de “No gol” e de times.

**Goleiro da próxima partida.** Com rodízio, a sugestão do app segue a regra do racha: **o goleiro fica com o time que fica em quadra** — o que venceu ou, no empate, o que ficou (com 3 times um fica no empate: o que entrou por último; com 4, os dois saem); só o outro lado troca, e recebe quem está há mais tempo esperando no rodízio. A pré-partida mostra os dois goleiros ("🧤 No gol") e qualquer um pode ser trocado na mão — por outro do rodízio ou por alguém do time — antes do apito; a escolha vale só para aquele confronto. "Foi embora" fica na pré-partida (ao lado de "Chegou agora"), e não na substituição. Não há botão de "girar a fila": troca fora do automático é toque/arraste entre fila e time.

**Duplas inseparáveis.** Elo por time não separa quem joga sempre junto: os dois ganham e perdem os mesmos pontos e convergem para o mesmo nível, seja qual for a diferença real. Quando uma dupla tem ≥20 partidas (≈3 rachas sempre juntos, D-56) e ≥80 % do histórico de um deles em comum, o app avisa em Stats → Racha ("🔗 Sempre no mesmo time", com a % de partidas juntos) e na ficha de cada um. O remédio é separá-los na montagem por algumas noites — ou ligar "Evitar repetir quem já jogou junto" nos Ajustes.

**Fila com 3–4 times.** Quem espera há mais tempo joga antes; vencedor fica (se ligado), perdedor vai para o fim da fila. Empate: com 3 times **um fica** — o que entrou por último (o que já estava sai); com 4, os dois saem.

**Sem "maior goleada".** Partida de racha é curta e termina em 2 gols; placar não mede nada. Retirada da aba Racha.

**+/-.** Na liga de partida única, a estatística principal de cada jogador (no racha curto ela existe, mas fica depois das vitórias): gols a favor menos gols contra enquanto ele estava em quadra, em todos os trechos. É o primeiro número do cartão do jogador (Stats e ficha) e o primeiro ranking do período e do último racha. Na partida longa, onde a noite tem uma partida só, é o que separa quem esteve dentro nos bons momentos de quem não esteve.

**Minutos e ritmo.** Cada trecho guarda a duração de jogo (sem pausas), então minutos em quadra e no gol são somas exatas por jogador. A aba Stats mostra minutos, **gols a cada 10 min** e, para goleiros, **sofridos a cada 10 min** (rankings de ritmo e o destaque "Menos vazado" pedem 1 h em quadra/no gol; goleiro é sempre medido por tempo, nunca por partida). Stats tem duas abas — **Jogador** (a pessoa: aproveitamento, ano a ano, duelos, parcerias) e **Racha** (a liga no período e os rankings) — e o período (ano ou desde sempre) é filtro, não aba. Rankings mostram 3 linhas e abrem até 10; **empate no número divide a mesma posição** (1, 2, 2, 4 — D-89); cada um tem uma **setinha de ordem** no cabeçalho (↓ = do melhor para o pior, padrão; ↑ = a mesma lista lida do fim — quem está pior naquele número), lembrada por aparelho. E **a ordem deles responde à pergunta do filtro**: em *30 dias* a forma abre a lista (aproveitamento, vitórias, sequência, artilharia); num *ano*, presenças e campanha; em *Sempre*, o volume de carreira (presenças, tempo em quadra) vem primeiro. Na partida única o +/− abre em qualquer filtro (D-45). Os filtros de período (Último · 30 dias · ano · Sempre) dividem uma linha só. Além dos anos e de "desde sempre", o filtro tem **Último mês** (30 dias) e **Último racha**; neste, a aba Racha troca os rankings de temporada por uma leitura da noite (as listas ranqueadas têm a mesma setinha de ordem) — presentes, partidas, gols, minutos de jogo, os times da noite com V/E/D e gols (e, discreto sob a contagem, a **% de vitórias realizada × a probabilidade média de vitória no apito** — D-77), **quem mais ganhou** (vitórias; desempate por menos derrotas — a leitura "quem mais perdeu" é a setinha invertida), artilheiro, quem rendeu acima do esperado, tempo em quadra, menos vazado (mín. 20 min no gol), gols contra e quem subiu/caiu de nível.

**No servidor, a liga vive em partes.** Cada jogador, partida, racha e entrada do log é uma linha própria (payload jsonb de fatos), mais uma linha `live` para o racha em andamento. O app grava só o que mudou (`save_parts`) e recebe só o que mudou desde a versão que conhece (`league_delta`); um gol é ~1 KB subindo e ~1 KB descendo em cada aparelho, independentemente do tamanho do histórico. Nível e estatística nunca vão para o banco.

**Fatos vs. derivados.** `matches` (escalações de largada `startLineups`/`startGks`, trechos, placar, gols com autor/minuto/contra, `events` bruto) e `sessions` são fatos; nível, Elo, forma, gols e contagens em `players` são derivados e `rebuildAll()` os refaz do zero. `log[]` na liga registra toda correção manual (quem, quando, antes → depois) e nunca é apagado. Gol contra: abinha "contra" ao marcar o autor; não conta na artilharia, aparece só na ficha.

**Presença em lote.** Na tela "Quem chegou", segurar um nome e arrastar marca todo mundo por onde o dedo passa (ou desmarca, se o primeiro nome apagou). No computador é clicar e arrastar. O "segurar" existe para não brigar com a rolagem da lista.


**Funciona de verdade, hoje:**

- Múltiplas Ligas isoladas, cada uma com patentes, jogadores, ajustes e histórico próprios
- Escada de 15 degraus com nomes editáveis, histerese e calibração (a proteção pós-promoção foi removida — D-46)
- **Duas patentes por jogador** (linha e goleiro), independentes, com calibração própria
- **Motor por trecho**: cada formação em campo é uma partida, com descarte de trecho curto e peso proporcional
- **Rating 100% invisível em todas as telas**, com opção de esconder até a patente de quem não é admin (o admin vê o Elo cru discreto — D-52)
- Formato 5v5 / 6v6 / 7v7 / 11v11 com sugestão automática de quantidade de times
- Presença, montagem automática equilibrada, troca manual por toque, sorteio aleatório
- Goleiros: fixos por time, rodízio com alternância de lado, improviso no meio da partida
- Partida ao vivo: cronômetro com pausa (vibra e apita quando o tempo bate), gol em um toque (toque duplo não dobra), autor opcional, substituição com trecho próprio, cancelar com confirmação, "chegou agora", desfazer; confirmação em tudo que não tem volta (encerrar racha, apagar partida); dois celulares na mesma partida somam eventos
- Presença ordenada por quem mais aparece, com marcação de goleiro por racha
- Equilíbrio que evita repetir quem já jogou junto, sem abrir mão do equilíbrio
- Vencedor fica, com fila de times, e tela de próxima partida com escalação editável e chance esperada de cada lado
- Contestação, revisão, correção, anulação e recálculo integral
- Ranking agrupado por patente, com escadas separadas de linha e de goleiro, histórico, resumo de fim de racha
- **Destaques dos últimos 30 dias** na tela do racha: top 3 por saldo acima do esperado, artilheiro (quando os gols têm dono), goleiro menos vazado e presença
- **Painel de números**: duelos e parcerias por pessoa (com histórico encontro a encontro), destaques (carrasco, freguês, melhor dupla), quebra ano a ano e rankings do racha no período
- Histórico agrupado por racha, com os rachas do dono do perfil marcados e filtro "só as minhas"
- Contas por usuário e senha; assumir perfil (**Sou eu**) e papéis por conta — as ações de conta do admin valem no servidor (D-62)
- Entrar numa liga por **código com aprovação do admin**; membros, contas e pedidos em Jogadores → Pendências
- **Sequências** (maior série de vitórias, atual e recorde) nos rankings
- Editar nome, "costuma ir ao gol", conta e permissão pela ficha do jogador (rascunho + Salvar); **opiniões sobre o nível** de quem lança, um toque por pessoa, na ficha ou na tela "Minhas opiniões" (D-95)
- **Juntar dois cadastros** da mesma pessoa (admin), reversível pela ficha ("Separar de novo")
- **Corrigir escalação e trocas** de partida encerrada, reescrevendo os trechos (D-61); registro de correções por liga
- Exportar/importar a liga inteira em JSON, com migração automática de ligas gravadas por versões anteriores
- **Tudo no Supabase** (Postgres + Auth + Realtime): sync incremental por versão, só fatos no banco, tempo real entre os celulares do racha — precisa de internet; no aparelho fica só a preferência de aba/tema

**Ainda não existe (v2):**

- Entrar por **link de convite** ou **convite direto com busca** (seção 7.3) — hoje só o código com aprovação
- **Funcionar offline** — o protótipo funcionava; a versão com backend precisa de rede (DEPLOY.md)
- Recuperação de senha e e-mail de verdade
- Papel de escrita valendo no servidor para a gravação da liga (`save_parts` só exige ser membro — D-62)
- Temporadas com reset parcial
- Gráfico de evolução da patente ao longo do tempo
- Motivo escrito na contestação e aviso para os admins
- Rivalidade por trio/quarteto e exportar o painel de números

### 8.1 Como o backend está montado (e o que falta)

O app roda contra o **Supabase** (Postgres + Auth + Realtime) com o esquema intermediário de `supabase/schema.sql`: a liga vive em **partes** (`league_players`, `league_matches`, `league_sessions`, `league_live`, `league_log`), o cliente grava só o que mudou (`save_parts`) e recebe só o que mudou (`league_delta`), com trava otimista por versão. O **alvo relacional completo** — trechos, gols e vínculos como linhas próprias, papel de escrita no servidor — está em **[BANCO-DE-DADOS.md](BANCO-DE-DADOS.md)**; o resumo:

As **estatísticas não são guardadas**: duelos, parcerias, presenças e aproveitamento são derivados dos trechos na hora de desenhar a tela. Não existe contador para desincronizar — corrigir uma partida de três semanas atrás conserta o painel junto.

**O que fica guardado em cada partida** (e por que importa): placar e resultado, a **lista de trechos** (cada um com escalação dos dois lados, goleiro de cada lado, duração, peso, placar próprio e se conta), gols com autor, **o modo do racha** (que define o K) e o **id da sessão** (que alimenta a contagem de rachas da calibração). Com isso, o histórico é auto-suficiente: dá para recalcular a liga inteira do zero sem depender de nenhuma configuração atual.

```
profiles       (id, handle, nome)
ligas          (id, nome, codigo, entrada_livre, cfg_json)
liga_members   (liga_id, user_id, player_id, papel, status)   ← unique(liga_id,player_id): 1 membro = 1 jogador
liga_invites   (id, liga_id, tipo, token, para_user, player_id, expira_em, status)
join_requests  (id, liga_id, user_id, status)
players        (id, liga_id, nome, rating_linha, rank_linha, rating_gol, rank_gol, costuma_gol, removido)
sessions       (id, liga_id, data, modo, formato)
matches        (id, liga_id, session_id, ordem, modo, formato, placar, resultado, deltas_json, anulada)
stints         (id, match_id, ordem, ini_ms, dur_ms, peso, conta, lineups_json, gks_json, placar, resultado)
goals          (id, match_id, stint_id, player_id NULL, lado, t_ms)
disputes       (id, match_id, user_id, motivo, ts)
audit_log      (id, liga_id, actor, acao, alvo, payload, ts)
```

O vínculo conta↔jogador mora em `liga_members`, e não em `players`: é uma `unique (liga_id, player_id)` que
garante, no banco, que **um membro é um jogador só**. Jogador sem linha em `liga_members` é perfil sem dono.

O motor (`splitStints`, `stintPart`, `computeElo`, `updateRank`, `applyMatch`, `rebuildAll`, `buildTeams`, `pairCounts`, `statsLiga`, `encontros`, `statsAnos`) é todo função pura, sem DOM — hoje roda no cliente (`rebuildAll` a cada delta) e pode subir para o servidor sem reescrita quando fizer sentido. Offline com fila de sincronização continua sendo desenho futuro: a versão atual precisa de rede.

---

## 9. Decisões de produto que valem defender

> Os princípios estão aqui; o **registro datado** de cada decisão, com alternativas descartadas e onde ela vive no código e nos testes, está em [DECISOES.md](DECISOES.md).

1. **O número não existe para o jogador.** Patente é identidade; ponto é contabilidade. Expor o ponto muda o comportamento das pessoas dentro da quadra — inclusive o corte entre patentes, que também é secreto. O **admin** é a exceção (D-52): vê o Elo cru discreto na aba Jogadores, como ferramenta de gestão. E se a liga preferir, nem a patente aparece aos demais: só o admin vê. A **única** porcentagem que o app mostra é a chance esperada **do confronto** — ela descreve quão parelho está o jogo, não o nível de ninguém em particular, e desaparece quando as patentes estão fechadas.
2. **Patente é assunto de fim de racha.** Entre partidas o app não anuncia promoção nem queda: encerrar cai direto na tela da próxima partida. Quem subiu e quem caiu sai tudo junto no resumo do fim.
3. **Ninguém precisa apontar o vencedor.** Marcar os gols já diz quem ganhou; encerrar é 1 toque e grava o placar, 0-0 incluído (empate). Um toque a menos por partida, doze vezes por noite.
4. **A unidade de medida é o trecho, não a partida.** Substituição muda o nível dos dois lados, então cada formação em campo conta como uma partida própria — como o +/- da NBA. O que o seu time fez enquanto você estava no banco não é problema seu. Trecho de menos de 3 minutos cortado por troca é descartado em vez de virar ruído.
5. **Uma partida vale uma partida.** O peso de cada trecho é a fatia da partida que ele ocupou, então quebrar uma partida em cinco trechos não multiplica o efeito dela na patente por cinco.
6. **Gol não move patente.** Só vitória, empate e derrota — é o que reflete o racha. Gol é estatística de vitrine.
7. **Duas patentes por pessoa: linha e goleiro.** Dá para ser Ouro na linha e Prata no gol; medir os dois no mesmo número não descreve ninguém. Foi isso que aposentou o interruptor "goleiro fora do ranking" — o problema não era o goleiro pontuar, era pontuar na escada errada.
8. **Goleiro é papel do dia, não atributo da pessoa.** Quem veio para o gol se marca na presença, e muda no meio do racha se a pessoa mudar.
9. **Palpite inicial + calibração rápida** vence "esperar dados suficientes". A calibração termina em **15 partidas** (várias curtas) ou **3 rachas** (partida única), e vale separado para cada uma das duas patentes.
10. **Desfazer e contestar em todo lugar — mas cada coisa no seu lugar.** Se errar dói, ninguém lança. Gols têm remoção individual, a partida pode ser pausada ou cancelada (com confirmação) e a última tem "Desfazer" na própria tela do racha. Já **corrigir resultado, anular e apagar moram no Histórico**: são decisões de mesa, não de quadra, e ninguém quer esse botão perto do dedo enquanto o próximo time já está entrando.
11. **Subir tem que ser possível; cair não pode ser humilhação diária.** Margem de histerese e patente guardada como estado existem só para isso (a proteção pós-promoção foi testada e removida — D-46).
12. **Patente por Liga, sempre.** A mesma pessoa pode ser referência num grupo e novata em outro, sem quebrar nenhum dos dois rankings.
13. **Formato e modo são da liga, definidos na criação.** Uma liga é um grupo, um tamanho de time e um modo. Nível de 5v5 não se compara com nível de 11v11, e uma noite de partida única não se compara com uma de dez curtas — então quem muda de formato começa outra liga. Cada partida guarda o próprio modo.
14. **Equilíbrio primeiro, panelinha depois.** O app tenta separar quem sempre joga junto — mas só quando isso não custa equilíbrio. Times equilibrados são o produto; misturar as duplas é o que faz a patente convergir para a pessoa em vez de para o time.
15. **A fila é sugestão, não regra.** O app propõe o próximo confronto pelo "vencedor fica", mas trocar qualquer um dos dois times custa 2 toques. Racha real não obedece fila.
16. **Número maior é melhor dentro da patente.** Diamante 3 é o topo, Diamante 1 é o primeiro degrau — e os nomes (Ferro → Bronze → Prata → Ouro → Diamante) se leem sem ninguém explicar.
17. **Estatística é derivada, nunca guardada.** Duelo, parceria, presença e aproveitamento saem dos trechos na hora. Contador gravado é contador que um dia desencontra do histórico — e aí ninguém sabe qual dos dois está certo.
18. **Ranking de aproveitamento tem piso de partidas.** Sem piso, o topo é sempre de quem jogou três vezes, e a lista inteira perde a graça.
19. **Time é sempre cheio; quem sobra é a fila.** No 5v5 se joga 5 contra 5 — quadra no Brasil não tem jogo menor que isso. O app monta quantos times inteiros couberem e o resto espera de fora; time de 3 "esperando a vez" não existe. E quando um time fica curto, ele é **completado** com quem está de fora, nunca compensado sentando alguém do outro lado. O app sugere quem completa; quem escolhe é quem está com o celular.
20. **Reserva só existe na partida única.** No racha curto ninguém fica preso ao banco de um time: quem sobra é de fora, do racha, e entra na próxima troca.
21. **Tema claro por padrão, escuro por escolha.** Celular no sol, em quadra descoberta, é o caso mais duro de leitura — e é nele que o app tem que funcionar. Para o racha da noite, o escuro está a um toque. É preferência do aparelho, não da liga.
23. **A fila é de pessoas, não de times.** Quem perde sai, quem espera entra no lugar dele, e quem fica completa — é o "de próximo" que todo racha já joga, sem nome novo e sem tela nova para aprender.
22. **Arrastar e tocar, os dois.** O arraste é mais direto para substituir e trocar de time; o toque continua funcionando porque no celular, com a mão suada, arraste erra.
24. **A cara do app é a da quadra: papel esverdeado, tinta e coletes.** Fundo verde-claro de quadra descoberta, texto quase preto e o botão principal em tinta (preto sobre claro, giz sobre escuro) — nada de cor de destaque brilhante, porque no sol ela some. As cores fortes são só dos **coletes**: Time A verde, B vermelho, C azul, D amarelo, sólidas, no cabeçalho de cada time e no placar (dois coletes lado a lado com o numeral gigante). Tipografia condensada de placar (Big Shoulders Display) para números, títulos e botões; Archivo para texto. Ao abrir o app volta a última aba usada neste aparelho (atualizar a página cai no mesmo lugar). A **navegação fica embaixo** (Racha · Stats · Jogadores · Jogos · Ajustes), na zona do polegar, e a barra de ação (Montar times, Fim…) logo acima dela; o topo é só o nome da liga. Alvos de toque de 44–50 px. Pouco contorno e pouco texto: as telas de uso trazem uma linha de instrução no máximo; o resto está em Ajustes e aqui.
