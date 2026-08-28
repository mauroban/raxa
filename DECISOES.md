# Decisões — o que foi decidido, e por quê

> O código é protótipo; **as decisões não são**. Este arquivo existe para que a v2 não precise
> redescobrir nada: cada decisão traz o motivo, o que foi descartado e onde ela vive hoje
> (documento, código e teste). Quando uma decisão mudar, ela é **reescrita aqui**, com a data nova
> e o motivo da virada — não some.
>
> Regras de quadra em [REGRAS-DO-RACHA.md](REGRAS-DO-RACHA.md) · produto em [DOCUMENTACAO.md](DOCUMENTACAO.md)
> · dados em [BANCO-DE-DADOS.md](BANCO-DE-DADOS.md).

---

## Motor de patente

### D-01 · A unidade de cálculo é o trecho — sempre
**18/08/2026.** Cada formação em campo é uma partida para o motor. Calibração, proteção pós-promoção e
os contadores de partidas jogadas contam **trechos**, não partidas de relógio.
**Por quê:** substituição muda o nível dos dois lados; medir por partida creditaria a alguém o que
aconteceu enquanto ele estava no banco.
**Descartado:** contar proteção e calibração em partidas de relógio (chegou a ser implementado e foi
revertido) — deixava duas unidades convivendo no mesmo motor.
**Onde:** DOCUMENTACAO §3.4 · `splitStints`, `applyMatch` · teste `[5]`.

### D-02 · O peso do trecho descartado é redistribuído
**18/08/2026.** Trecho curto cortado por substituição não conta, e o peso dele é **dividido entre os
trechos que contam**. Uma partida vale exatamente uma partida.
**Por quê:** antes, uma troca no começo fazia a partida inteira pesar 0,75 — a partida encolhia por
causa de uma decisão de quadra.
**Onde:** DOCUMENTACAO §3.4 · RF-03.3d · `splitStints` · teste `[5]`.

### D-03 · O mínimo de trecho é relativo: 4 min **ou ⅓ da partida**, o que for menor
**18/08/2026.** **Por quê:** o modo padrão é de 7 minutos; com 4 minutos fixos, duas trocas nunca
poderiam contar na mesma partida, e qualquer substituição antes dos 3 min descartava meia partida.
**Onde:** DOCUMENTACAO §3.4 · RF-03.3c · teste `[5]`.

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
**Onde:** DOCUMENTACAO §3.4–3.6 · `KMODE`, `RANK_MARGIN`, `PROTECT`, `CAL_*`, `normalize` · testes `[6]` `[7]`.

### D-05 · Patente por valência só existe se a pessoa jogou nela
**18/08/2026.** Quem nunca jogou na linha, ou nunca pegou no gol, **não tem patente ali**: fica fora
daquela escada e a ficha diz *sem patente*. Se entrar naquela posição, vale o **nível de entrada padrão**
e começa a construir a dele, em calibração. O palpite do cadastro vale só para a valência da pessoa.
**Por quê:** cadastrar um Diamante de linha fazia dele um Diamante no gol — a escada de goleiro vinha cheia
de gente que nunca defendeu.
**Descartado:** herdar a patente da outra valência (comportamento anterior, migrado na carga).
**Onde:** DOCUMENTACAO §3.7 · REGRAS-DO-RACHA §5 · RF-03.1c/1d · `newTrack`, `temPatente` · smoke.

---

## Montagem de times e rodízio

### D-06 · Time é sempre cheio; quem sobra é fila
**18/08/2026.** No 5v5 se joga 5 contra 5. O app monta **quantos times inteiros couberem** e o resto
espera. Não existe time de 3 esperando a vez. Nem forçando 3 ou 4 times: o botão que não cabe fica
apagado. Único caso de jogo com menos: quando nem dois times cheios dão (8 pessoas → 4v4, com aviso).
**Por quê:** quadra no Brasil não tem jogo menor que o formato. Time incompleto não é arranjo, é problema.
**Descartado:** "sobra ≥ 60% vira time menor" e a variante "times parelhos 5/4/4" — as duas produziam
lados desiguais em quadra.
**Onde:** REGRAS-DO-RACHA §2.1 · DOCUMENTACAO §4.2 · RF-05.2/5.3d · `planCaps`, `planTeams` · testes `[3]`, smoke.

### D-07 · Reserva presa a um time só existe na partida única
**18/08/2026.** No racha curto quem está fora é da **fila do racha**, não do banco de um time.
**Por quê:** no modo curto os times rodam; ficar preso ao banco de um time é ficar de fora sem entrar
na roda. No modo longo os dois times são fixos a noite toda — aí reserva é o desenho certo.
**Onde:** REGRAS-DO-RACHA §2.1 e §4 · RF-05.3d.

### D-08 · A fila é de pessoas: o "de próximo"
**18/08/2026.** Ao fim de cada partida: **quem ganhou fica, quem perdeu sai, a fila entra no lugar de
quem saiu, e quem sai vai para o fim da fila**. Se a fila não dá para trocar o time inteiro, **alguns do
time que perdeu ficam para completar** — entram 3, ficam 2, normalmente o goleiro e mais um. Sai quem
mais jogou na noite. Empate com 2 times não gira sozinho; existe **↻ Girar** para a mão.
**Por quê:** é o que todo racha já faz. O app antes deixava quem estava de fora parado a noite inteira.
**Onde:** REGRAS-DO-RACHA §2.2 · DOCUMENTACAO §4.2 · RF-05.3j/3k/3l · `filaDe`, `rodaFila` · smoke.

### D-09 · Time curto é completado, nunca compensado sentando alguém
**18/08/2026.** Quando um time entra com menos gente (alguém foi embora, alguém foi movido), o app
**completa com quem está na fila** — sugerindo quem menos jogou — e **quem escolhe é o usuário**. Quem
completa joga por empréstimo: volta para o time dele quando a partida acaba. Dá para recusar e jogar
com menos dos dois lados.
**Por quê:** o comportamento anterior encolhia o time maior — dois caras já escalados sentavam.
**Onde:** REGRAS-DO-RACHA §2.3 · RF-05.3g/3h/3i · `fillDe`, `cardCompletar` · smoke.

### D-10 · Quem fica de fora também é equilibrado
**18/08/2026.** A fila é uma **fatia que atravessa todos os níveis** (um sorteado de cada faixa), nunca
os piores do racha.
**Por quê:** o draft ia do melhor para o pior, então quem não cabia era sempre o fundo da lista.
**Onde:** DOCUMENTACAO §4.2 · REGRAS-DO-RACHA §2.1 · RF-05.14 · `fatiaEquilibrada` · teste `[2b]`.

### D-11 · Ruído na montagem para variar — e só na montagem
**18/08/2026.** O sorteio do draft usa o nível de cada um **mais um ruído de ±25 pontos internos**; o
refinamento (as centenas de trocas 1:1) e o desempate de panelinha usam o **nível real**.
**Por quê:** com gente parelha existem dezenas de arranjos igualmente equilibrados, e sem ruído
"Equilibrar" devolvia sempre o mesmo. Medido: 14 montagens dão 13-14 arranjos distintos, e o pior
desequilíbrio caiu para 6-10 pontos — melhor que o algoritmo determinístico anterior, porque cada
sorteio explora um ótimo local diferente.
**O ruído não sai do montador:** chance de vitória, barra de equilíbrio e veredito usam nível real.
**Onde:** DOCUMENTACAO §4.2 · RF-05.13/5.15 · `buildTeams` · teste `[2b]`.

---

## Destaques e números

### D-12 · A tela do racha mostra os últimos 30 dias, não o topo histórico
**18/08/2026.** Saiu "craque da liga + artilheiro de sempre", entrou **Destaques · últimos 30 dias**, em
**duas listas**: primeiro *os melhores do racha* (maior patente entre quem apareceu no período, cada um pela
valência que mais jogou), depois *quem mais rendeu além do esperado*. Cada linha escreve o que cada número
é — rachas, partidas e % de vitórias.
**Por quê:** o topo histórico premiava quem começou bem em março e sumiu. Racha é presente. E as duas
listas respondem perguntas diferentes: *quem é bom* e *quem está rendendo*.
**Detalhe que não é óbvio:** a lista dos melhores ordena por **degrau, aproveitamento e nome** — a mesma
regra do ranking. Ordenar por rating dentro da mesma divisão revelaria quem está na frente, que é
exatamente o que o produto decidiu não mostrar (RNF-05.4).
**Onde:** DOCUMENTACAO §5.3 · REGRAS-DO-RACHA §6 · RF-08.8/8.8b/8.8c · `destaques`, `statsBlock` · teste `[13]`.

### D-13 · O critério do destaque é o saldo acima do esperado
**18/08/2026.** `Σ (resultado do trecho − chance daquele lado) × peso` — a mesma conta que move a
patente, sem o K, expressa em vitórias. Piso: **2 rachas e 20 partidas** no período.
**Por quê:** com times equilibrados o aproveitamento de todo mundo tende a 50%, e vitória pura premia
quem caiu no time bom. O saldo desconta a dificuldade do confronto: a zebra que vence leva +0,88, o
favorito que confirma leva +0,12. Soma zero dentro da partida, então ninguém infla o número só jogando.
**Descartado:** aproveitamento, vitórias, e média por partida (presença faz parte do mérito num racha).
**Exibição:** o pódio mostra **nome, partidas e % de vitórias** — o número do saldo fica fora da tela,
porque ordena bem e comunica mal (fica quase sempre perto de zero).
**Onde:** DOCUMENTACAO §5.3 · REGRAS-DO-RACHA §6 · RF-08.9 · `destaques`, `m.over` · teste `[13]`.

### D-14 · Artilheiro só quando os gols têm dono
**18/08/2026.** Aparece se **metade ou mais** dos gols do período tiverem autor; senão o card diz
quantos ficaram sem dono.
**Por quê:** autor de gol é opcional de propósito. Ranking com metade dos gols órfãos premia quem
lembrou de se cadastrar, não quem fez gol.
**Onde:** DOCUMENTACAO §5.3 · RF-08.10 · teste `[13]`.

### D-15 · Goleiro menos vazado = gols sofridos por partida, por trecho
**18/08/2026.** Conta só os trechos em que a pessoa estava no gol.
**Por quê:** goleiro que entrou no meio não pode levar gol que tomou antes de entrar; no rodízio é justo
porque ele alterna de lado a noite toda.
**Onde:** DOCUMENTACAO §5.3 · RF-08.11 · teste `[13]`.

### D-16 · Estatística é derivada; o que a partida guarda é saída do motor
**18/08/2026.** Duelos, parcerias, presenças, aproveitamento e destaques são calculados do histórico a
cada tela. A partida guarda `deltas` e `over` (acima do esperado) — que são **saída do cálculo**, refeitas
por `rebuildAll`, não contadores mantidos à mão.
**Por quê:** contador gravado é contador que um dia desencontra do histórico, e aí ninguém sabe qual dos
dois está certo.
**Onde:** RNF-04.9 · RF-11.12 · teste `[13]` (recálculo reproduz o `over`).

---

## Interface

### D-16b · O histórico é por racha, não por partida
**18/08/2026.** A aba Jogos lista **uma linha por racha** (data, partidas, gols, contestações, e a marca de
quantas foram suas). As partidas aparecem depois de tocar no racha, com contestar e revisar.
**Por quê:** um racha rende 10 a 15 partidas; a lista corrida virava um mural de placares sem contexto.
Ninguém procura "a partida de 2 a 1", procura "o racha de sábado".
**Onde:** DOCUMENTACAO §4.3 · RF-07.1/7.1b/7.1c · `rachasDe`, `viewHist` · smoke.

### D-17 · Tema claro é o padrão
**18/08/2026.** Claro por padrão; escuro e automático a um toque, por aparelho.
**Por quê:** o pior caso de leitura é celular no sol, em quadra descoberta — é nele que o app tem que
funcionar. Racha à noite escolhe o escuro em um toque.
**Onde:** RNF-08.5 · DOCUMENTACAO §9 (decisão 21) · verificado por teste visual nos dois temas.

### D-18 · A tela da partida é o placar
**18/08/2026.** Relógio compacto no topo (com ⏸ e ✕ como ícones), **placar ocupando ~31vh** logo acima
da barra fixa, `−` no canto de cada time para tirar o último gol, e a barra de baixo com **só** `↶` e
`✓ Fim · placar`.
**Por quê:** é a tela usada 12 vezes por noite, em pé, com uma mão. E "Encerrar racha" estava colado no
"Fim": um toque errado com o próximo time entrando acabava com a noite.
**Onde:** DOCUMENTACAO §4.3 · RF-06.11c/11d/6.18 · RNF-01.6 · teste visual.

---

## Contas e dados (v2)

### D-19 · Um membro é um jogador — e só um
**18/08/2026.** Dentro de uma Liga, uma conta corresponde a exatamente um perfil. Garantido no banco
(`unique (liga_id, player_id)` em `liga_members`), não na tela.
**Por quê:** é o que faz "quantas vezes joguei contra o Rodrigo" ter uma resposta única.
**Onde:** DOCUMENTACAO §7.1 · BANCO-DE-DADOS §4 · RF-09.2b.

### D-20 · Três caminhos para entrar, uma regra só
**18/08/2026.** Link de convite (vence em 7 dias, revogável), código de 6 caracteres (gera pedido para o
admin aprovar, salvo se a liga ligar *entrada livre*) e busca por `@usuário` com convite direto de uso
único. **Ninguém entra sem aceitar e sem o admin abrir a porta.** O admin tem controle total sobre
membros, e remover um membro não apaga o jogador nem o histórico.
**Onde:** DOCUMENTACAO §7.3/7.4 · BANCO-DE-DADOS §5 · RF-01.6* e RF-09.8/9.9/9.10/9.11.

### D-21 · O histórico é a fonte da verdade
**18/08/2026.** Rating e patente são cache: `rebuildAll` reconstrói tudo a partir das partidas válidas,
em ordem. Toda correção, anulação ou exclusão dispara o recálculo integral, em transação.
**Por quê:** é o que permite corrigir uma partida de três semanas atrás sem deixar resíduo em ninguém.
**Onde:** BANCO-DE-DADOS §1 e §8 · RNF-04.2/04.6 · teste `[8]`.

---

### D-22 · Revisar é do admin; o primeiro perfil vinculado é o admin
**28/08/2026.** Corrigir resultado, anular, apagar partida do histórico, corrigir patente e mudar
permissão são ações **só de admin**. Contestar continua aberto a todo membro. Desfazer a última
partida do racha em andamento continua de quem está lançando.
Enquanto **ninguém** vinculou um perfil, todo mundo é admin (senão a liga nasce trancada). O **primeiro**
a vincular vira admin automaticamente, e a liga **nunca fica sem admin**: o último não pode ser rebaixado.
**Por quê:** revisão aberta a qualquer membro fazia duas pessoas anularem uma partida e qualquer um
reescrever o resultado. Sem a regra do primeiro, o criador da liga virava "lançador" ao se vincular e
ninguém mais tinha poder de revisão.
**Limite conhecido:** a checagem é na interface; no banco qualquer membro ainda grava a liga inteira
(ver README "Estado" e BANCO-DE-DADOS.md).
**Onde:** `souAdmin`, `A.claim`, `A.setRole`, `A.review`… · Ajustes → **Membros** · smoke "assumir perfil".

### D-23 · Stats é a segunda aba, e Membros mora nos Ajustes
**28/08/2026.** A aba **Números** virou **📊 Stats**, logo depois de Racha: é a tela que a galera abre
entre uma semana e outra, e o nome antigo não dizia nada. Ganhou o retrato da liga no período (rachas,
partidas, gols, média, empates, maior goleada), forma recente e sequência de vitórias do jogador, e
rankings de sequência, goleiro menos vazado e melhor dupla. **Membros** (quem tem conta, com que papel)
vive no topo da aba **Jogadores** (ex-Patentes), acima da escada — é a mesma pergunta: "quem está aqui?".
**Onde:** `viewStats`, `statsLiga` (seq/best/ultimos/sofridos), `membrosCard`.

### D-24 · Os níveis são metais, e na interface "patente" se chama "nível"
**28/08/2026.** Escada padrão: **Ferro · Bronze · Prata · Ouro · Diamante** — quem entra nasce
**Prata 2**, no meio (revisto em D-25: Prata 1). As cores acompanham os metais. Liga com qualquer escada antiga de fábrica
(Iniciante…, Raiz…, Bronze…Platina) migra sozinha; nome editado à mão fica.
**Por quê:** "Iniciante" e "Promessa" descrevem quem está começando — e a base da escada é cheia de
gente que joga há vinte anos. Metal é um *rank*, não um adjetivo: Ferro não diz nada sobre idade,
experiência ou talento, todo mundo entende sem explicação e a cor vem de graça. Entrar em Prata (o
meio) e não em Ouro deixa dois degraus acima para subir e dois abaixo para achar o lugar.
Na **interface** a palavra é **nível** ("nível de goleiro", "Níveis fechados"); "patente" continua
sendo o termo interno (código e documentação), porque é o nome do conceito, não do que o usuário lê.
**Descartado:** Raiz · Boleiro · Titular · Destaque · Craque; Bronze · Prata · Ouro · Platina · Diamante
(entrada em Ouro 2, alto demais); "Lata" na base (é o único metal que diz "ruim").
**Onde:** `defCfg().patNames`, `PATSHORT`, `PATC_*`, `normalize` · Ajustes → Nomes dos níveis.

### D-25 · Quatro níveis: sai o Diamante
**28/08/2026.** Escada padrão: **Ferro · Bronze · Prata · Ouro** — 4 níveis × 3 divisões = 12 degraus,
**1100–1899, centrada em 1500**. Quem entra (1500) nasce **Prata 1**; Ouro 3 é o topo e segura tudo acima de 1900.
**Por quê:** num racha de 15–20 pessoas o quinto nível ficava vazio ou com uma pessoa só — o Diamante
virava um troféu isolado em vez de uma faixa. Com quatro, cada nível tem gente e a escada inteira se
lê num relance. O passo de 200 pontos (75% de vitória esperada) fica. A base subiu de 1000 para 1100
porque o Elo é soma zero: a média da liga fica cravada perto da entrada (1500), e a escada antiga
tinha 500 pontos abaixo e 300 acima — Ouro encheria e Ferro ficaria vazio. Centrada, cada nível
significa uma distância da média: Bronze/Prata = um pouco abaixo/acima, Ferro/Ouro = muito.
Entrar em Prata 1 (a fronteira) em vez de Prata 2 é consequência, e até ajuda: a primeira noite já
diz de que lado da média a pessoa está.
**Migração:** liga com 5 nomes perde o quinto; rank/peak acima de 11 são reclampados no `fixTrack`, e o
recálculo do zero reposiciona todo mundo. Nome editado à mão nos quatro primeiros fica.
**Onde:** `BASE=1100`, `TOP=11`, `PATC_*`, `PATSHORT`, `defCfg().patNames`, `normalize`, `fixTrack`.

### D-26 · Código gera pedido; o admin aprova
**28/08/2026.** Digitar o código da liga não entra mais direto: cria um pedido em `league_requests`.
O admin vê o pedido no card **Membros** (primeiro da lista, "pediu para entrar") e aprova ou recusa;
quem pediu vê "Aguardando aprovação" na home e, aprovado, a liga aparece sozinha (Realtime em
`league_members`, RLS entrega só o próprio vínculo). O mesmo canal avisa quem foi removido.
**Por quê:** o código vaza (print no grupo, encaminhado) e qualquer um entraria numa liga que grava
o documento inteiro. Um racha tem dono; entrada é decisão dele. Sem "entrada livre" por enquanto —
se um grupo grande sentir falta, vira ajuste da liga.
**Onde:** `join_league` (devolve `{status}`), `my_requests`, `approve_request`/`reject_request`,
`league_accounts` (coluna `pending`), `PEND`, `A.doJoin`/`accApprove`/`accReject`, `watch()`.

### D-27 · Quem entra é Jogador; Lançador é dado pelo admin
**28/08/2026.** Papel padrão de jogador novo (e de conta sem perfil vinculado) passa de Lançador para
**Jogador** — só leitura, contestação e vincular o próprio perfil. O admin promove a Lançador quem
conduz o racha. Editor continua corrigindo resultado; Ajustes são só do admin.
**Por quê:** com entrada por código e aprovação, a liga vai ter gente que só quer ver o próprio nível.
Todo mundo podendo mexer em presença, times e placar é convite para bagunça acidental — e "lançar"
é responsabilidade de quem está com o celular na quadra, não de quem entrou.
**Como:** a checagem é uma só, no despachante de cliques (`ACOES_LANCAR`, `ACOES_ADMIN`): botão
aparece, mas para Jogador responde com um aviso. Liga nova sem vínculo continua com todo mundo admin.
Jogadores já existentes com papel Lançador não mudam.
**Onde:** `meuPapel`, `podeLancar`, `mkPlayer`/`migPlayer`, despachante de `click`/`change`.

### D-28 · Fatos completos na partida, registro de correções, gol contra
**28/08/2026.** (1) A partida passa a guardar o log bruto (`events`: gols, substituições, pausas,
com hora) e cada gol leva `t`/`min` e `own`. (2) A liga ganha `log[]`: toda correção (nível,
resultado, anular/reativar/manter, apagar partida, papel, vínculo de conta, remover/cadastrar por
conta) registra quem, quando, de quê para quê — nunca é apagado e não entra em cálculo; o admin vê
em Ajustes → Registro de correções. (3) Gol contra: a barra "Quem fez?" e a folha de correção têm a
abinha discreta **do time | contra** que troca os nomes para os do outro time; o gol vai para o
placar do time que ganhou o ponto, o autor não pontua na artilharia e acumula `gc` (aparece só na
ficha, "· 1 contra").
**Por quê:** nível, divisão e estatística são deriváveis de `matches` via `rebuildAll` — trocar o
sistema de nivelamento é trocar o motor e recalcular. Mas o minuto do gol, a ordem dos eventos e o
motivo de uma correção manual eram descartados no fechamento da partida: informação que nenhum
recálculo futuro recupera. Agora o app registra os fatos independentemente de como os usa.
**Onde:** `finish` (events/goals), `logAdd`/`LOG_TXT`/`logCard`, `scorerTabs`/`showScorer`,
`goalScorer`/`setGoalScorer`/`scorer`/`scorerSide`, `applyMatch` (gc).

### D-29 · A liga deixa de ser um JSON só: partes por entidade e sync incremental
**28/08/2026.** `leagues.data` (documento inteiro) sai de cena. Entram `league_players`,
`league_matches`, `league_sessions`, `league_live` e `league_log`, cada linha com payload jsonb e
`v` = versão da liga em que foi gravada. Duas funções fazem tudo: `league_delta(id, desde)` devolve
o que mudou desde uma versão (0 = carga inicial) e `save_parts(id, versão, partes)` grava só as
partes que mudaram, com o mesmo compare-and-swap de antes. Em conflito o servidor devolve o delta e
o cliente reenvia o que ainda difere — perde-se só o que os dois mexeram. Só **fatos** vão para o
banco: `playerFacts` (nome, conta, papel, palpite de entrada) e `matchFacts` (sem `deltas`/`moves`);
`rebuildAll` refaz nível e estatística ao carregar. Ligas antigas migram sozinhas na primeira
leitura (`migrate_league`). Ajustes mostra o tamanho real no servidor (`league_size`).
**Por quê:** armazenamento nunca foi o problema; transporte era. Com o documento único, cada gol
subia e descia a liga inteira para todo aparelho aberto — em um ano de racha semanal, ~1 MB por
toque, e a saída do plano gratuito estourava numa noite cheia. Agora um gol custa ~1 KB, e o
histórico só desce uma vez, na carga.
**Por que não o relacional completo (BANCO-DE-DADOS.md) agora:** o motor roda no cliente e lê a
partida como um objeto (trechos, escalações, gols). Quebrar em linhas de trecho/gol obrigaria a
remontar tudo no load sem ganho de transporte — é o passo certo quando o recálculo for para o
servidor. Partida como linha jsonb é a granularidade em que o app pensa.
**Descartado:** manter o documento e só separar o `live` (resolvia o gol, não o histórico que
cresce); normalizar trechos e gols já (ver acima).
**Onde:** `supabase/schema.sql` (bloco "LIGA EM PARTES"), `playerFacts`/`matchFacts`/`factsDoc`,
`diffParts`/`commitSnap`, `flush`, `applyDelta`, `loadAll`, `refetch`, `logCard` (tamanho).

### D-30 · Substituição é da partida, não do time; "foi embora" tira a pessoa do racha
**28/08/2026.** Trocar alguém durante a partida não mexe mais em `lv.teams`: quem entra emprestado
(da fila ou de outro time) volta para onde estava na partida seguinte, e quem saiu continua no time
dele. A única troca que fica é titular ⇄ reserva dentro do mesmo time. Novo: **Foi embora /
machucou** (na folha de substituição e em "Chegou agora → Alguém foi embora?") tira a pessoa da
presença, do time, da fila e do rodízio; se estava em quadra, sai sem substituto — evento `sub`
com `in:null`, e o trecho seguinte conta com um a menos, como aconteceu.
**Por quê:** mexer no time a cada substituição deixava um time com um a menos e mandava o
substituído para a fila sem ninguém pedir — a fila "sugerida" ficava errada a partir daí. Sair do
racha é outra coisa, e precisa de um botão próprio.
**Onde:** `doSub`, `undo` (sub), `splitStints` (`in:null`), `A.leaveRacha`, `outPick`, `lateSheet`.

### D-31 · A vaga mora no cartão do time
**28/08/2026.** Time com jogador a menos mostra uma vaga tracejada por lugar vazio dentro do próprio
cartão — na montagem (`slotPick`: fila e reservas de outros times, quem jogou menos hoje primeiro)
e na pré-partida (`fillPick`: completa só aquela partida; o emprestado aparece no cartão com ✕).
**Por quê:** "falta 1" escrito no cabeçalho não dizia o que fazer; o card "Completar" embaixo
resolvia a pré-partida mas a montagem não tinha caminho direto. A vaga é o próprio convite.
**Onde:** `timeCard` (vagas/emprestados), `A.slotPick`/`slotSet`, `viewProxima`.

### D-32 · Goleiro do vencedor fica; escolha manual antes do apito; sem "girar"
**28/08/2026.** O rodízio de goleiros deixa de alternar lados a cada partida: **o goleiro do time que
venceu fica com o time** (quando "vencedor fica" está ligado); o outro lado recebe quem está há mais
tempo na fila do rodízio (`gkPool` é a fila; quem vai ao gol vai para o fim). A pré-partida mostra
os dois goleiros e deixa trocar na mão (`lv.nextGks`, válido só para aquele par de times). Sai o
botão "↻ Girar no time X" — troca fora do automático é toque/arraste. "Foi embora" vira botão da
pré-partida (`leaveSheet`), não da substituição.
**Por quê:** o critério da quadra é esse, e o app sugerindo outra coisa gerava correção a cada
partida. Os botões de girar eram atalho para um caso raro e confundiam com a substituição.
**Onde:** `planGks`/`commitGks`, `finish` (`lv.lastGks`), `viewProxima` (card "No gol"),
`A.preGk`/`setPreGk`, `A.leaveSheet`.

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

### D-35 · O app aponta duplas inseparáveis em vez de fingir que as separa
**28/08/2026.** `inseparaveis()` lista duplas com ≥35 partidas e ≥80 % do histórico do menor dos
dois em comum; aparecem em Stats → Racha e como aviso na ficha de cada um.
**Por quê:** é limite do modelo, não bug — no Elo por time, dois jogadores sempre no mesmo lado
recebem exatamente os mesmos deltas e terminam com o mesmo rating. Tentar "descontar" isso no motor
(peso por contribuição, gols, etc.) inventaria informação que o app não tem. Mostrar onde o dado
está cego e dizer o remédio (separar por algumas noites; `avoidRepeat` já existe) é honesto e
funciona.
**Onde:** `inseparaveis`, `JUNTOS_MIN`/`JUNTOS_PCT`, `viewStats` (cardJuntos), `pSheet`.

### D-36 · De volta a 5 níveis — Diamante no topo, Prata no meio; sem nível até calibrar
**28/08/2026.** Escada: **Ferro · Bronze · Prata · Ouro · Diamante**, 15 degraus, 1000–1999,
entrada (1500) em **Prata 2** — o degrau do meio. Cortes: Ferro <1200 · Bronze 1200 · Prata 1400 ·
Ouro 1600 · Diamante 1800. Ferro é aço escuro (a prata é quase branca, não confundem); Diamante é
azul-gelo. E: quem não tem nível dado à mão (cadastro/admin) fica **sem nível** até sair da
calibração — a escada o lista em "Sem nível ainda" com o progresso.
**Por quê:** com 4 níveis a entrada caía numa fronteira (Prata 1). Cinco níveis em 1000 pontos
sempre deixam uma ponta rara (±300 da média = 85 %+ de expectativa). A primeira tentativa do dia
pôs o quinto degrau embaixo ("Madeira", entrada em Bronze 2); foi revertida na mesma hora porque o
jogador mediano — metade do racha — viraria "Bronze", e a ponta vazia ficaria embaixo, como
constrangimento. Com Diamante em cima, a média é Prata (a leitura que todo mundo já traz de jogo) e
a ponta vazia é ambição. O acolhimento de quem chega, que era a razão da Madeira, é feito pelo
"sem nível até calibrar", que não carimba ninguém.
**Descartado:** Madeira/Papel/Pedra embaixo (média vira Bronze); Platina no topo (visualmente irmã
da Prata e não lê como topo para quem não joga videogame); entrada em Prata 1 com 5 níveis.
**Onde:** `BASE=1000`, `TOP=14`, `PATC_*`, `PATSHORT`, `defCfg().patNames`, `normalize`,
`temPatente`, `viewEscada` (bloco "Sem nível ainda").

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

### D-38 · Partida única tem regra de trecho própria
**28/08/2026.** No modo **partida única** (longa): peso do trecho = fatia de tempo (não 1/n);
trecho conta a partir de `stintMin` com ou sem gol; o final conta sempre; e vitória/derrota/partida
jogada só para quem esteve em quadra por ≥ 25 % do tempo que conta (`UNICA_MIN_SHARE`). O modo
curto mantém a D-37 (curto sem gol descartado, K/n, qualquer trecho válido dá a partida).
**Por quê:** em 50 minutos com trocas rolando, "1/n" faria um trecho de 3 minutos pesar como um
de 30, e "qualquer trecho válido dá a vitória" entregaria a partida a quem entrou para cumprir
tabela. Os dois formatos são jogos diferentes; a régua tem que ser diferente.
**Onde:** `splitStints(…, mode)`, `contaPartida`, `applyMatch`, `statsLiga`, `statsAnos`, `destaques`.

### D-39 · Empate com 3 times: um fica; goleiro fica com o time que fica
**28/08/2026.** `lv.lastStay` guarda quem ficou em quadra depois de cada partida: o vencedor; no
empate com 3 times, o que entrou por último (o que já estava sai); com 4 times, ninguém; com 2,
os dois. `planGks` segura o goleiro do rodízio para todo time em `lastStay` — não só o vencedor.
**Por quê:** é a regra da quadra; "empate os dois saem" com 3 times deixava a quadra vazia para o
único time da fila.
**Onde:** `finish` (rotação), `planGks`, `suggestPair` (via `lastWinner`).

### D-40 · Visual da quadra: tinta, coletes e navegação embaixo
**28/08/2026.** Redesenho visual com foco em celular. Tema claro vira "quadra ao sol": fundo
`#E3E9D9`, tinta `#0F1F16`, botão principal em tinta (sem cor de destaque); escuro é o mesmo
sistema invertido. Times ganham cor de **colete** sólida (verde, vermelho, azul, amarelo) no
cabeçalho, no slot da próxima partida e no placar — o placar da partida ao vivo são dois coletes
com numeral de até 120 px. Fontes: Big Shoulders Display (display, botões, rótulos) e Archivo
(texto). As cinco abas saem do topo e viram **barra de navegação fixa embaixo** (`#nav`, ícones +
rótulo, 60 px + safe-area); a barra de ação (`#bar`) fica logo acima dela e `body.hasbar` abre
espaço no fim da página. O topo encolhe para 56 px, sticky. Alvos de toque mínimos de 44 px
(chips de presença 50 px, botões 48 px, barra 54 px). Sai a textura de ruído e a grade de giz do
fundo (custavam no celular e apareciam por entre os cartões).
**Por quê:** abas no topo ficavam fora do alcance do polegar; o lime brilhante sobre claro perdia
contraste no sol; os tons pastel dos times não se distinguiam a um braço de distância. Colete é o
que a pessoa já usa para saber o time dela.
**Descartado:** manter as abas no topo com ícones (polegar não chega); fundo escuro por padrão
(D-17 continua); desenho da quadra (linha do meio e círculo) atrás do conteúdo — vazava entre
os cartões e parecia defeito.
**Onde:** `index.html` (`<style>`, `NAV_TABS`, `setNav`, `drawApp`) · DOCUMENTACAO §9 (decisão 24)
· `scripts/visual.py` ignora `.nav` na checagem de sobreposição · RNF-08.

### D-41 · Menos contorno, menos texto
**28/08/2026.** Passada de limpeza depois do D-40. Chips, botões secundários, campos e blocos
internos deixam de ter contorno escuro e viram preenchimento suave (`--fill`); cartões perdem a
borda (sombra de 1 px). Os textos de instrução repetidos em cada tela (como arrastar, como a fila
gira, o que conta como partida, quem vê o quê) saem das telas de uso — presença, times, próxima
partida, partida ao vivo, Stats, Jogadores — e fica só uma linha curta quando ela orienta uma
ação ("Toque em quem chegou · 🧤 marca goleiro"). A explicação completa continua em Ajustes e
na DOCUMENTACAO.
**Por quê:** o usuário sentiu a tela poluída, e o motivo era texto demais: parágrafo explicativo
embaixo de cada bloco, lido uma vez e ignorado para sempre.
**Descartado:** esconder as instruções atrás de um "?" por bloco — mais um alvo em cada tela.
**Onde:** `index.html` (`<style>`, `viewPresenca`, `viewTimes`, `viewProxima`, `viewJogo`,
`statsBlock`, `viewStats`, `viewRanking`) · smoke continua cobrindo os textos que importam.

## Como registrar uma decisão nova

Uma linha por decisão, nesta ordem: **o que foi decidido** (com a data), **por quê**, **o que foi
descartado** e **onde ela vive** — documento, função e teste. Se não tem teste, diga que não tem.
Decisão sem "por quê" volta a ser discutida em três meses; decisão sem "onde" vira lenda.
