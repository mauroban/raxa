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
Na mesma passada, respiro entre texto e gráfico: anel de aproveitamento com o rótulo
afastado dos cartões, coluna de V/E/D que cabe "Derrotas", barras dos rankings a 8 px do
texto, presença em uma coluna até 460 px (nome inteiro em vez de "Jefferso…"), placar com o
"−" longe do nome do time.
**Descartado:** esconder as instruções atrás de um "?" por bloco — mais um alvo em cada tela.
**Onde:** `index.html` (`<style>`, `viewPresenca`, `viewTimes`, `viewProxima`, `viewJogo`,
`statsBlock`, `viewStats`, `viewRanking`) · smoke continua cobrindo os textos que importam.

### D-42 · Goleiro fixo é um dos N; gols abaixo das substituições
**28/08/2026.** Na escalação (`escCol`), o número de lugares de linha é `per` menos 1 quando o
goleiro é fixo (fora do rodízio) — ele ocupa um dos `per` lugares. Goleiro do rodízio continua
entrando além de `per`. Na partida ao vivo, o cartão **Gols** passa para baixo do cartão de
reservas/fora (substituições), antes de "Partidas de hoje".
**Por quê:** na partida única (e em qualquer racha com um goleiro por time) aparecia uma vaga
fantasma em cada time. E na partida longa a lista de gols cresce muito e empurrava para longe
os nomes de quem pode entrar.
**Onde:** `escCol`, `viewJogo` · smoke "partida unica com goleiro fixo: escalacao sem vaga fantasma".

### D-43 · +/- é a estatística principal
**28/08/2026.** Cada jogador tem um **+/-** (como na NBA): gols do seu lado menos gols do outro
enquanto esteve em quadra, somando todos os trechos — gol é gol, mesmo em trecho curto. Aparece
em primeiro nos cartões do jogador (Stats e ficha), como primeiro ranking do período e do último
racha. V/E/D continua por partida (D-37/D-38).
**Por quê:** na partida única existe uma partida só por racha — vitória e derrota viram um dado
por noite e não separam ninguém. O que separa é o placar enquanto cada um estava dentro.
**Descartado (por ora):** contar V/E/D por trecho na partida única — a vitória é da partida
inteira; o que precisa variar por trecho é o *nível*, e isso ainda está em desenho (ver
conversa: juntar trechos com o mesmo confronto, pontuar um pouco por gol).
**Onde:** `plusMinus`, `applyMatch` (`p.pm`), `statsLiga`/`statsAnos` (`pm`), `viewStats`, `pSheet` ·
`test.py` "+/-".

### D-44 · Formato e modo são da liga, escolhidos na criação
**28/08/2026.** A folha "Nova liga" pede nome, **tamanho do time** e **modo** (várias curtas /
partida única). Saem os seletores da tela de presença e de Ajustes; Ajustes mostra o formato só
de leitura ("definido na criação; para outro formato, crie outra liga"). O racha herda
`cfg.matchMode`; `m.mode` continua gravado por partida (histórico antigo com modos mistos segue
valendo). As ações `setFormat`/`setMatchMode` continuam existindo para os testes, sem botão.
**Por quê:** nível e estatística só fazem sentido dentro de um formato; trocar no meio da vida
da liga mistura réguas. Substitui a decisão 13 antiga ("o modo é do racha").
**Descartado:** permitir mudar em Ajustes com aviso — ninguém lê aviso na quadra.
**Onde:** `newLiga`/`novaSheet`/`novaOpt`/`saveLiga`, `cfgNova`, `viewPresenca`, `viewCfg` ·
DOCUMENTACAO §9 (decisão 13) · smoke "nova liga escolhe formato e modo na criacao".

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
`test.py` (confronto juntado, margem, 0-0 contra time pior) · DOCUMENTACAO §3.

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
**Onde:** `KMODE`, `kFor`, `streakK`, `PROTECT`, `calibrando`, `calMeta` · DOCUMENTACAO §3.4–3.6,
§9 (decisão 9) · RF-03.6/03.7/03.10 · `test.py` [5]–[6], [8c].

### D-47 · Trocar o goleiro pelo do outro lado é troca de lugar — gol E escalação
**29/08/2026.** Escolher para um gol o goleiro que estava no gol do outro time faz os **dois
trocarem de lado por inteiro**: cada um passa para o gol E para a escalação (`lineups`) do lado
novo, na partida ao vivo (`setGk`) e na pré-partida (`setPreGk`). O evento `gk` grava os
movimentos (`mv`), que a reconstrução dos trechos (`splitStints`, via `aplicaMv`) reaplica e o
`↶` desfaz. Goleiro do rodízio escolhido de fora de quadra também entra na escalação do lado dele.
**Por quê:** antes só `gks` mudava e a escalação ficava para trás: cada goleiro aparecia como
goleiro de um lado **e** jogador de linha do outro, contava na estatística pelo time errado e nem
aparecia na lista de autor quando fazia gol pelo time novo. E o comportamento antigo ("libera o
outro lado") não era o que o usuário esperava: na quadra, os goleiros **trocam de lugar**.
O que a versão com o bug deixou para trás também é curado: evento `gk` **sem** `mv` é
normalizado na reconstrução (quem defende um gol joga daquele lado — isso é fato físico, não
intenção) e `normalize` conserta a partida ao vivo gravada com a escalação errada ao carregar.
**Descartado:** mandar o goleiro substituído para fora de quadra; deixar o estado antigo como
está (o ⇄ e o nome na linha continuavam aparecendo para quem já tinha feito a troca).
**Onde:** `movesGk`, `aplicaMv`, `setGk`, `setPreGk`, `splitStints`, `undo`, `normalize` ·
`test.py` [11] (troca de gol no meio, evento antigo sem `mv`) · `smoke.py` (trocar o goleiro de
um time pelo do outro; troca gravada pela versão antiga) · DOCUMENTACAO §4.3.

### D-48 · Fim sem querer tem volta: "Voltar a partida"
**29/08/2026.** O Fim continua 1 toque sem confirmação, mas agora deixa um instantâneo
(`lv.lastEnd`: cópia da partida e do estado da rodada **antes do giro** — times, fila, vencedor,
goleiros). Enquanto a próxima não começa, o bloco de partidas de hoje mostra **"↩ Voltar a
partida"** (`voltarPartida`): apaga o registro, recalcula os níveis do zero e devolve a partida
ao relógio com tudo no lugar; o intervalo entre o Fim e a volta entra como par pausa/retomada,
então o relógio não conta esse tempo. Começar outra partida (ou apagar a registrada) descarta o
instantâneo.
**Por quê:** o Fim é 1 toque por design — confirmar atrasaria toda partida por causa do caso
raro. Mas o toque errado só tinha o "Desfazer a última", que apaga o registro e perde o relógio
e os gols, além de não desfazer o giro da fila (quem entrou da fila já tinha entrado no time).
**Descartado:** confirmação no Fim; manter o instantâneo depois que outra partida começa (fila e
rodízio de goleiros já giraram de novo — a volta deixaria o estado inconsistente).
**Onde:** `finish` (instantâneo), `voltarPartida`, `todayBlock`, `startMatch`/`delMatch`
(descarte), `backMatch` no registro de correções · `smoke.py` ("o fim foi sem querer") ·
DOCUMENTACAO §4.3.

### D-49 · Presença do racha conta desde o começo, não a foto do fim
**29/08/2026** (aprendizado do primeiro racha real). Quem foi embora no meio continua contando
como presente: `leaveRacha` registra em `lv.leftIds`, e a sessão grava a **união** de quem passou
pelo racha. O tile "presentes" do período "Último" usa sessão ∪ quem jogou nas partidas — o que
também cura racha antigo, cuja sessão só fotografou o fim.
**Por quê:** a lista de presença era mutável (sair removia), então "presentes" encolhia ao longo
da noite — no primeiro racha real o número do fim não batia com quem de fato apareceu.
**Descartado:** nunca remover da presença (quebra fila, montagem e "foi embora"); contar só quem
jogou (quem veio e não entrou também esteve lá).
**Onde:** `leaveRacha`, `endRacha`, `cardsUmRacha` (tile presentes) · `smoke.py` ("sessao guarda
presenca desde o comeco", "presentes do ultimo racha") · DOCUMENTACAO §5.2.

### D-50 · A sessão guarda os times como foram montados; tocar no time mostra a escalação
**29/08/2026.** `endRacha` grava em cada sessão `teams` (nome + ids da montagem original,
`t.orig`) e `gkPool`. Na aba Números, período "Último", tocar num time de "Times do racha" abre a
escalação original (com o rodízio à parte); cada nome leva à ficha. Racha gravado antes disso cai
no fallback: a escalação da primeira partida daquele time.
**Por quê:** pedido do primeiro racha real — "quem eram os jogadores de cada time?" não tinha
resposta no app: as partidas guardam escalações por partida, mas a montagem da noite não ficava
em lugar nenhum.
**Descartado:** derivar sempre das partidas (substituições e empréstimos poluem; a montagem é um
fato próprio).
**Onde:** `endRacha`, `rachaTime`, `cardsUmRacha` · `smoke.py` ("times do racha: toque abre a
escalacao original") · DOCUMENTACAO §5.2.

### D-51 · Números com a opção "sem goleiros"
**29/08/2026.** Chip 🧤 na aba Números (`S.ui.statsSemGk`): quando ligado, o trecho em que a
pessoa estava **no gol** sai das contas de time — jogos, V/E/D, +/−, tempo em quadra, sequência,
duelos e parcerias (`statsLiga(liga, per, semGk)`). Os números *de goleiro* (menos vazado,
sofridos, tempo no gol) continuam, e gol marcado por goleiro segue na artilharia.
**Por quê:** o goleiro do rodízio troca de lado sem escolher time — a vitória "dele" é do acaso
do rodízio, e misturá-la com a de linha distorce aproveitamento, +/− e duplas.
**Descartado:** excluir os goleiros por completo (o menos vazado sumiria); um filtro por pessoa
(o papel é do trecho, não da pessoa — o improvisado conta como linha no resto da partida).
**Onde:** `statsLiga`, `plusMinus` (papel no callback), `viewStats` (chip), `statsSemGk` ·
`test.py` [11] ("sem goleiros") · `smoke.py` ("numeros sem goleiros") · DOCUMENTACAO §5.2.

### D-52 · O admin vê o Elo cru, discreto, na aba Jogadores
**29/08/2026** (reescreve o "nem para o admin" da D-histórica de 3.1). Na escada, cada linha
mostra ao **admin** o Elo arredondado num número pequeno e apagado (opacidade 0,4, fonte 10px,
title "Elo — só o admin vê") — inclusive no bloco "sem nível ainda". Para lançador, editor e
jogador, nada muda: o número continua inexistente.
**Por quê:** pedido do usuário após o primeiro racha real: o admin precisa conferir montagem e
convergência do rating sem abrir o export JSON. Sutil de propósito: é ferramenta de gestão, não
linguagem do racha — patente continua sendo a única língua pública.
**Descartado:** mostrar a distância para o próximo corte (reintroduz o jogo de pontos); expor
para lançadores (quem conduz o racha não precisa do número para nada).
**Onde:** `viewEscada` (`souAdmin`) · `smoke.py` ("admin ve o elo cru"; não-admin não vê) ·
DOCUMENTACAO §3.1, §3.8, §9.1.

### D-53 · Calibração do racha curto: 15 partidas (o nível aparece em ~2 rachas)
**29/08/2026** (ajusta o número da D-46; o K 40/20 não muda). `CAL_GAMES` 25 → **15**. No
primeiro racha real, o máximo que alguém jogou foi **7 partidas** — com 25, quem entra sem
palpite ficaria ~4 rachas (um mês de racha semanal) sem patente, e o K de calibração duraria o
mesmo tanto. Com 15, o nível aparece em ~2 rachas e o K cai para 20 no mesmo ponto.
**Por quê:** a calibração tem duas funções acopladas — quando a patente APARECE e até quando o K
anda dobrado — e as duas estavam dimensionadas para "10 a 15 partidas por pessoa por noite", que
o racha real desmentiu (rodízio de 4 times ≈ metade das partidas para cada um). Mexer aqui
preserva o Elo clássico (D-46); mexer no K não.
**Descartado:** subir o K pós-calibração (só com 3–4 rachas de dados, se a escada parecer
congelada); separar o portão da patente do fim do K (duas regras para explicar, ganho pequeno);
encerrar calibração por rachas no racha curto (partida é a unidade natural dele, D-46).
**Onde:** `CAL_GAMES` · `test.py` [6] ("calibracao e fixa: 15 partidas") · DOCUMENTACAO §3.2,
§3.6, §9.9.

### D-54 · Rankings da noite abrem até 10, e existe "quem mais perdeu"
**29/08/2026.** Nos destaques do último racha, cada ranking (melhor +/−, quem mais ganhou,
artilheiro, rendeu acima, tempo em quadra, menos vazado) mostra 3 e abre até **10** com o mesmo
"▾ ver até N" dos rankings de temporada (`corta`/`mais`, chaves próprias em `S.ui.statsOpen`).
Entram também **"😵 Quem mais perdeu"** na noite e **"😵 Mais derrotas"** nos rankings de
temporada — derrotas, desempate por menos vitórias e mais partidas.
**Por quê:** pedido pós-primeiro racha: com 15+ presentes, o top 3 esconde o meio da tabela; e a
zoeira do "quem mais perdeu" é metade da graça do racha.
**Descartado:** listas sempre completas (parede de lista; o padrão 3+abrir já existia na
temporada).
**Onde:** `cardsUmRacha`, `rkDer`/seção "Mais derrotas" em `viewStats` · `smoke.py` ("rankings da
noite abrem ate 10") · DOCUMENTACAO §5.2.

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
(histerese) · DOCUMENTACAO §3.4 (tabela e nota D-55), §3.5, §3.6.

### D-56 · Dupla inseparável: aviso a partir de 20 partidas juntos
**29/08/2026.** `JUNTOS_MIN` 35 → **20** (o critério de 80 % do histórico em comum não muda).
Com as ~7 partidas por pessoa por noite do racha real, 35 eram ~5 rachas sempre juntos antes do
aviso; 20 são ~3 — proporcional ao encurtamento da calibração (D-53) e ao K mais rápido (D-55):
se o nível converge em 2 rachas, a dupla colada precisa ser apontada na mesma escala, antes de os
dois Elos se fundirem por construção.
**Descartado:** baixar também os 80 % (quem joga separado às vezes já dá sinal ao motor); piso em
rachas em vez de partidas (a parceria é contada por partida no histórico).
**Onde:** `JUNTOS_MIN` · `test.py` [15] · DOCUMENTACAO §8 (duplas inseparáveis).

### D-57 · Na aba Jogadores, o admin vê a escada ordenada por Elo
**29/08/2026.** Dentro de cada divisão, a lista da aba Jogadores passa a ser ordenada por **Elo
decrescente** — mas **só para o admin**. Para todos os outros papéis a ordem continua degrau →
aproveitamento → nome. Motivo: a divisão só muda com histerese (margem 21, D-55), então dois do
mesmo degrau podem estar a mais de um degrau de distância em Elo; para quem monta os times, a
ordem verdadeira é informação de trabalho — e o admin já enxerga o Elo cru na própria linha, então
ordenar por ele não revela nada novo. Para os outros a ordem neutra segue valendo: a posição na
lista não pode denunciar o rating de ninguém.
**Descartado:** ordenar por Elo para todo mundo (transformaria a lista num ranking numérico
implícito — é exatamente o que a ordem por aproveitamento existia para evitar); ordenar por Elo
ignorando o degrau (as seções de patente se repetiriam na tela, porque a histerese quebra a
monotonia entre degrau e Elo); mudar também "Os melhores do racha" (card que todo mundo abre
junto no racha — lá a ordem neutra vale para o admin também); deixar o bloco "Sem nível ainda"
sempre por partidas (quem calibra é justamente de quem o admin menos sabe o nível — é ali que a
ordem verdadeira ajuda mais a montar os times; para os outros continua por partidas, que é o
progresso que a linha mostra).
**Onde:** `viewEscada` (`porElo`, usado na escada e no bloco "Sem nível ainda") · sem teste novo (é ordem de tela; `smoke.py` cobre a
renderização) · DOCUMENTACAO §3.8 (ordem dentro do degrau) e §7 (nota no card dos melhores).

### D-58 · Revisar é abrir a partida inteira, não só o placar
**31/08/2026.** A revisão passa a mostrar **tudo o que a partida guardou**, antes dos botões de
correção: resumo (minutos de jogo, quantas pessoas jogaram, gols, trechos que contam); **quem jogou
de cada lado**, com tempo em quadra, 🧤 e tempo no gol, gols, gols contra e o que aconteceu com
a pessoa (entrou aos 4'30, saiu aos 7'00, saiu e voltou); a **linha do tempo** com cada gol,
substituição, troca de goleiro e pausa, no minuto de jogo e com o placar corrido; os **trechos**,
com escalação dos dois lados, placar, se conta e com que peso; e o **efeito no nível**. A correção
de autor de gol saiu da lista separada de gols e virou o próprio gol na linha do tempo.
**Por quê:** revisar é decidir se o registro está certo, e o registro é muito maior que 2×1 — quem
contesta quase nunca discorda do placar, discorda de *quem estava em quadra*, de *quando a troca
aconteceu* ou de *qual trecho contou*. Tudo isso já estava gravado (`stints`, `events`, `goals`,
`deltas`, `moves`, D-01/D-29) e não aparecia em lugar nenhum: o admin tinha que decidir no escuro
ou abrir o JSON. A linha do tempo também é o único lugar onde a partida volta a ser uma história em
ordem — é o que faz o admin lembrar do que aconteceu.
**Descartado:** abas dentro do sheet (esconderiam justamente o que se quer comparar de relance —
quem jogou × o que aconteceu); mostrar tudo aberto (numa partida única de 50 minutos vira parede de
rolagem: linha do tempo abre por padrão, trechos e nível abrem com um toque); expor a mesma ficha
para todo mundo no histórico (é tela de decisão do admin, e mostra Elo cru — a ficha pública de
partida fica para depois, se pedirem); recalcular qualquer coisa para a tela (a revisão só lê o que
a partida gravou; nada de estatística nova por baixo).
**31/08/2026, mesmo dia:** o +/− saiu dessa lista. Sem rótulo, na ponta da linha do nome, ele lia
como um número solto ("o que é esse −2?") — e +/− já tem lugar próprio, com título e explicação,
nos rankings da noite e da temporada. A ficha ficou com o que se explica sozinho: tempo, papel,
gols e o que aconteceu com a pessoa.
**Onde:** DOCUMENTACAO §6 e §8 · `fichaPartida`, `fichaLinha`, `revTempo`, `revTrechos`, `revNivel`,
`revDetalhe`, `corTime`, `A.review`, `A.revSec` · `smoke.py` ("revisar partida mostra a partida
inteira", "ficha da partida conta tempo e gols de quem jogou" — o +/− da ficha é conferido
contra `plusMinus`, o motor) · `layout.py` (snapshots com trechos e nível abertos).


### D-59 · A vitória é do time que jogou — a composição, não o nome no placar
**31/08/2026.** O V/E/D dos "Times do racha" (e o "Hoje: ..." da pré-partida) passa a ser atribuído
por **composição**: um lado da partida só conta como o time X se **mais da metade dos jogadores
originais de X** esteve em quadra em algum trecho. Se duas composições passam da metade — o time
trocou inteiro no meio e a formação nova é a maioria de outro time da noite — leva **quem ficou
mais tempo em quadra** (minutos-jogador dos originais); empatado nisso, quem cobriu maior parte do
próprio time; e só então o time do nome. Formação que não é maioria de ninguém **não conta para
time nenhum**, e o card diz quantas foram.
**Por quê:** o nome do time (`m.names`/`m.teamIdx`) é só o rótulo de quem entrou em quadra naquele
confronto. Com empréstimo, "completar" e substituição, dava para o Time A vencer com cinco pessoas
que não são do Time A — e o ranking da noite premiava um time que não jogou. Presença em **algum
trecho** (e não na partida inteira) é de propósito: substituição normal não pode custar a vitória a
quem montou o time.
**Descartado:** exigir maioria no trecho final (uma troca nos últimos segundos trocaria o dono da
vitória); exigir maioria em todos os trechos (qualquer rodízio de goleiro derrubaria); atribuir
sempre pelo maior tempo sem exigir maioria (dois desfalques bastariam para a vitória migrar); dar a
vitória aos dois times quando as duas composições passam da metade (inflaria o V/E/D da noite);
mexer no V/E/D **do jogador** — esse continua sendo de quem estava em quadra, que é o que o motor
de nível mede (D-01).
**Onde:** DOCUMENTACAO §7 (período "Último") · `emQuadraNo`, `timeDoLado`, `timesDoRacha`,
`teamRecord`, `cardsUmRacha` · `smoke.py` ("vitoria e do time que jogou, nao do nome no placar" —
partida normal, time trocado do começo, trocado no meio, uma substituição só e formação sem dono).

### D-60 · O time é a lista de quem jogou (até 5v5), no card da noite e no histórico
**31/08/2026.** No "Times do racha", o título da linha passa a ser o **primeiro nome de cada
jogador original** ("Vinashow, Maike, João, Halisson"); o nome do time vira nota na linha de baixo,
com os gols em **8/3 G** — feitos em verde, sofridos em vermelho.
**Por quê:** "Time A" é a cor do colete, não o time — ninguém lembra qual era qual no dia seguinte.
Quem lê o card quer saber *quem* ganhou a noite. E "8 gols feitos · 3 sofridos" gastava uma linha
inteira para dois números.
**Descartado:** trocar o nome do time em todo lugar (no placar e ao vivo o nome curto é o que cabe
e é como se chamam em quadra); mostrar a lista em ligas maiores que 5v5 (7 nomes não cabem numa
linha de celular — lá continua o nome do time); repetir o sobrenome inteiro (só a inicial, e só
quando dois jogadores do mesmo time têm o mesmo primeiro nome).
**31/08/2026, mesmo dia:** o **goleiro de rodízio fica fora** da composição do time — no rótulo e
na conta da maioria (D-59). Ele roda entre os times por regra do racha (o goleiro fica com quem fica
em quadra), então não identifica time nenhum: aparecia num racha inteiro trocando de lado e sujava
tanto o nome do time quanto o critério de maioria. Goleiro **fixo** de um time continua na
composição, porque aí ele é do time. A lista sai de `sess.gkPool`; com o racha ainda **aberto** a sessão nem
existe (ela nasce no encerrar), então times e rodízio vêm de `liga.live`. Sem lista nenhuma (racha
antigo) vale a evidência: **quem pegou no gol por mais de um time na mesma noite estava rodando**.
**31/08/2026, mesmo dia:** vale também para o **histórico**. Cada partida mostra os dois lados como
a lista dos primeiros nomes da escalação de largada, com os gols de cada lado à direita; o nome do
time fica no "venceu ..." da linha de baixo. A fonte cai para 12,5 px (texto, não display) para
caber, e quebra em duas linhas se precisar — cortar nome no meio seria pior. Acima do 5v5 continua o
nome do time com o placar `2 - 1`.
**Onde:** DOCUMENTACAO §5.2 e §6 · `nomesCurtos`, `timesDoRacha` (filtra o rodízio), `rotuloTime`
em `cardsUmRacha`, `teamRecord`, `mrow` · CSS
`.rk3.time` e `.mrow.nomes` (o rótulo pode ocupar duas linhas) · `smoke.py` (teste do D-59 no card
da noite; "abrir um racha mostra as partidas dele" confere a lista no histórico e a volta ao nome
do time acima do 5v5).


### D-61 · Escalação e trocas são corrigíveis depois — reescrevendo o que a partida gravou
**31/08/2026.** A revisão ganha a tela **"Escalação e trocas"** (só admin): quem começou de cada
lado, com o goleiro de largada, e a lista das trocas. Dá para trocar uma pessoa por outra (vale para
a partida inteira, gols inclusive), pôr quem faltou, tirar quem não jogou (as trocas dele somem e
os gols dele ficam sem autor), marcar o goleiro de largada, corrigir *quem saiu* / *quem entrou* de
uma troca, apagá-la, ou criar uma troca nova — minuto (passo de 30 s), time e as duas pontas — e
também uma troca de goleiro. Tudo isso acontece num **rascunho** (uma cópia da partida, fora de
`S`): a tela lista as mudanças pendentes e mostra a prévia dos trechos ("Como fica"), e só o
**Salvar** escreve na partida, manda cada mudança para o log e roda `rebuildAll`. Descartar — ou
fechar a folha — joga o rascunho fora. Quem refaz os trechos é `recalcPartida`, com o **mesmo
`splitStints` do apito final** sobre a escalação de largada + o log de eventos.
**Por quê:** a revisão já mostrava tudo (D-58), e a resposta natural de quem olha era "mas não foi
isso que aconteceu". Faltava o inverso do mostrar. E como trecho é a unidade de nível (D-01), errar
quem estava em quadra erra o nível de todo mundo daquela partida — era o único erro grande que o
app não deixava consertar.
**Como fica consistente:** os trechos são sempre **derivados**, nunca editados à mão; a partida passa
a gravar `startGks` (antes só existia no ao vivo, e a reconstrução dependia dele); o instantâneo de
goleiro que cada evento carrega (`ev.gks`) é corrigido até o próximo evento de goleiro daquele lado
(`ajustaGksEventos`), senão a partida "voltava" para o goleiro antigo na primeira troca; o minuto
digitado vira hora de parede somando o tempo pausado (`tDoMinuto`); e quem pode entrar numa troca é
só quem não está em quadra **dos dois lados** naquele minuto.
**Descartado:** aplicar cada toque na hora (foi a primeira versão: cada correção já recalculava a
liga e voltava para a tela — sem lugar para salvar, ficava confuso, e um toque errado já valia);
editar os trechos direto (viraria duas fontes de verdade — o log de eventos deixaria
de mandar); recalcular só a partida (correção antiga tem que percorrer a liga inteira, D-07);
apagar `ev.gks` de todos os eventos ao corrigir (perderia o goleiro que assumiu as luvas numa
substituição); deixar o admin escrever o minuto num campo de texto (passo de 30 s resolve e não
abre teclado no celular); permitir corrigir partida gravada sem cronômetro (sem `startedAt`/eventos
não há o que reconstruir — a tela avisa e não abre).
**Onde:** DOCUMENTACAO §6 e §8 · `recalcPartida`, `gksIni`, `podeCorrigirEsc`, `escalaEm`,
`genteDaPartida`, `foraDeQuadra`, `ajustaGksEventos`, `tDoMinuto`, `aplicaCorrecaoEsc`,
`rascunhoEsc`, `mudaEsc`, `viewEditEsc`, `viewNovaTroca`, ações `editEsc`/`escPick`/`escGk`/`escDel`/`escSwap`/`escAdd`/
`escAddDo`/`evPick`/`evSet`/`evDel`/`novaTroca`/`ntSet`/`ntOk`/`escSalvar`/`escDescartar` · log `esc` · `smoke.py`
("corrigir escalacao e trocas: rascunho ate o Salvar" — partida de 10 min montada à mão, com troca,
goleiro e gol, conferindo que a partida real só muda no Salvar, que cada mudança vira uma linha do
log, que o Descartar não deixa nada e que o nível bate com o recálculo do zero; "partida antiga nao
aceita correcao de escalacao") · `layout.py` (4 snapshots novos).


### D-62 · Papel de admin vale no servidor — e a migração para de travar leitura
**31/08/2026.** Quatro correções no `schema.sql` (rodar de novo no SQL Editor): **(1)**
`is_league_admin` passa a ler os jogadores de **`league_players`** (`data->>'owner'`,
`data->>'role'`, ignorando `deleted`) em vez de `leagues.data` — a migração esvazia `data`, então a
regra "enquanto ninguém vinculou, todo membro é admin" disparava sempre e **qualquer membro
aprovava/removia contas pelo console**. **(2)** `migrate_league` sai **antes** do `select … for
update` quando a liga já migrou, e só roda para membro — antes, todo `league_delta` pegava lock
exclusivo na linha da liga e serializava os aparelhos do racha (12 celulares reagindo ao mesmo
evento de realtime entravam em fila). **(3)** o `save_league` legado (documento único) é dropado:
gravava em `leagues.data` (que o `league_delta` ignora) e bumpava a versão — cliente antigo ou
chamada maliciosa mandava todo mundo para o loop de conflito. **(4)** a policy `profiles_read`
deixa de ser `using (true)`: cada um lê só o próprio perfil, porque o username é metade da
credencial (o e-mail de login é derivado dele) e a lista completa vazava para qualquer conta.
**Por quê:** o cliente esconde os botões pelo papel, mas RPC se chama pelo console; a fronteira que
o servidor prometia (só admin gerencia contas) não existia de fato.
**Descartado:** checar papel também no `save_parts` — jogador legitimamente grava (contestação,
assumir o próprio perfil), e separar o que cada papel pode mudar exige validar o conteúdo do diff
(o esquema relacional de BANCO-DE-DADOS.md); ficou registrado como limitação em DEPLOY.md.
**Onde:** `supabase/schema.sql` (`is_league_admin`, `migrate_league`, drop `save_league`,
`profiles_read`) · DEPLOY.md (§1.2 e "O que esperar") · sem teste novo: o Supabase falso de
`sync.py` só emula o dono-como-admin, e a regra nova é SQL puro.
**Correção no mesmo dia:** o script ainda guardava as versões superadas de `join_league` (retornava
`leagues`) e `league_accounts` (sem `pending`) antes das definitivas — num banco já migrado o
`create or replace` delas quebrava com `cannot change return type`, violando o "pode rodar de novo".
Só a versão definitiva de cada uma fica no arquivo; a promessa de idempotência voltou a valer.


### D-63 · Sync sem derivado, sem log dobrado e sem RPC em rajada
**31/08/2026.** Quatro consertos na camada de sincronização. **(1)** `matchFacts` também remove
`m.over` — é derivado (o `applyMatch` recalcula a partir do Elo corrente), e como ia junto no
payload, qualquer `rebuildAll` que mexesse no Elo (corrigir partida antiga, anular, corrigir
escalação) mudava o `over` de todas as partidas seguintes e o `diffParts` reenviava **o histórico
inteiro** pelo 4G da quadra. **(2)** o log deixa de ser cortado em 2000 entradas: o `diffParts` usa
o comprimento como cursor, e com o corte o comprimento parava de crescer — dali em diante nenhuma
correção nova subia; a carga inicial já traz o log inteiro do servidor, então o corte nem limitava
memória. **(3)** `applyDelta` deduplica o log e preserva o que ainda não subiu: num conflito de
versão, as entradas que nós mesmos tínhamos acabado de gravar voltavam no delta e dobravam na tela;
e entradas locais pendentes eram marcadas como sincronizadas sem nunca terem ido. **(4)**
`loadSize` tinha o `Object.assign` invertido (o `at` velho vencia o `Date.now()` novo) e não tinha
guarda de requisição em voo: RPC falhando = um `league_size` novo a cada render dos Ajustes.
**Por quê:** todos os quatro quebravam a promessa do D-29 ("um gol é ~1 KB") ou a do log ("nunca é
apagado, sempre aparece uma vez").
**Descartado:** cursor do log por id/seq em vez de comprimento (exigia mudar o formato da entrada e
o schema; dedup por JSON cobre o caso real — colisão só se duas entradas idênticas nascerem no
mesmo milissegundo).
**Onde:** `matchFacts`, `logAdd`, `applyDelta`, `loadSize` em `index.html` · sem teste novo
dedicado: `sync.py` cobre o caminho de conflito e continua passando.


### D-64 · Racha ao vivo à prova de tela atrasada — e o Voltar devolve a fila de verdade
**31/08/2026.** Quatro consertos no racha em andamento. **(1)** "↩ Voltar a partida" passa a
restaurar também **`lv.fila`** (a fila de pessoas): o instantâneo `lastEnd` guardava times, fila de
times, vencedor e goleiros, mas o `finish` já tinha girado a fila — quem ia entrar era reclassificado
como "chegou agora" e ia para o fundo. A DOCUMENTACAO (§"Fim sem querer tem volta") sempre prometeu
que a fila volta; agora o código cumpre. **(2)** Guarda de `null` em todas as ações que mexem na
partida corrente (`goal`, `ungoal`, `scorer`, `scorerSide`, `delGoal`, `goalScorer`,
`setGoalScorer`, `gkSheet`, `setGk`, `undo`, `endMatch`, `pauseMatch`, `cancelMatch`, `clearSel`,
`cancelRacha`, `pres`, `presGk`, `showScorer`): com dois celulares lançando, a tela pode estar um
delta atrasada (refetch adiado por folha aberta) e a partida já ter acabado no outro aparelho —
tocar em "gol" dava `TypeError` silencioso. **(3)** `onDrop` (arrastar) chama `A.doSub`/`A.sel`/
`A.toPool`/`A.toTeam` por fora do dispatcher de `[data-a]`, então quem é só **Jogador** conseguia
fazer substituição arrastando um nome; agora o arraste também exige `podeLancar`. `delPlayer` ganha
a checagem de editor que o botão da ficha já sugeria. **(4)** Racha que vira a madrugada aparecia
com duas datas: Stats rotulava pela primeira partida e Jogos pela última — a aba Jogos passa a usar
a data em que o racha **começou** (a noite é de quinta, mesmo acabando 00h40 de sexta).
**Descartado:** try/catch em volta do dispatcher (esconderia o erro em vez de tratá-lo — a guarda
no handler diz exatamente o que ignorar); reagrupar partidas avulsas que cruzam a meia-noite num
grupo só (mudaria a chave do grupo, e avulsa de madrugada é caso raro sem dono claro).
**Onde:** `finish`/`voltarPartida` (instantâneo `fila`), ações citadas, `onDrop`, `delPlayer`,
`viewHist` (`DIA(r.ts)`) em `index.html` · coberto pelos roteiros existentes de `smoke.py`.


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
**Por quê:** a DOCUMENTACAO (§Calibração) já descrevia o critério único por modo — o código é que
tinha ficado para trás; e comentário errado sobre constante é bug em incubação.
**Descartado:** manter o OU dos dois critérios "por segurança" (é exatamente o que criava o estado
contraditório patente+calibrando); piso configurável por liga (mais um botão para ninguém mexer).
**Onde:** `temPatente`, `calibrando`, `destaques` em `index.html` · DOCUMENTACAO §"Acima do
esperado" (piso) · `test.py` (blocos de patente e destaques, assinatura nova).


### D-66 · Limpeza: uma definição só por ação, sem sombras e sem texto mentindo
**31/08/2026.** Passa a valer "cada conceito existe uma vez". **(1)** Apagadas as versões do
protótipo que o bloco de conta sobrepunha (`resetAll`, `saveLiga`, `delLiga`, `demo`, `doImport`) e
as ações que nenhum `data-a` chama desde que a ficha (D-58) e o D-44 as substituíram: `setRank`,
`bumpRank`, `setRole`, `togGkP`, `claim` (as duas versões), `unclaim`, `giraFila`, `setFormat`,
`setMatchMode` — o `smoke.py` que as usava como atalho passou a testar o caminho real
(`pSheet → pdRank/pdOwner/pdRole/pdBump → pdSave`) e ganhou helpers próprios de formato/modo.
Também caíram o `planGks` de assinatura antiga (o hoisting da segunda declaração o apagava em
silêncio), `suggestTeams`, a constante `KEY` e os campos `res`/`side` que `benchList` devolvia sem
ninguém ler. `ACOES_LANCAR`/`ACOES_ADMIN` só listam ações que existem. **(2)** Sombras renomeadas:
em `viewStats`, `nRachas` (número) escondia `nRachas()` (função) e `pct` escondia `pct()`; em
`statsAnos`, `const A={}` escondia o objeto global de ações — viraram `nRachasPer`, `pctMe`,
`porAno`. **(3)** `esc()` também escapa apóstrofo (atributo com aspas simples deixa de ser armadilha
de XSS). **(4)** `pSheet` varre o histórico uma vez só (o `statsLiga` rodava de novo dentro de
`inseparaveis`). **(5)** `doImport` ensaia o `normalize` numa cópia isolada antes de empurrar em
`S.ligas` — JSON torto estourava depois do push e a liga inválida ficava quebrando todo
`applyDelta` até o reload. **(6)** Textos que mentiam: Ajustes dizia "K 20" (é 32/64), a folha de
código dizia "6 letras" (tem dígitos), e o botão da tela de erro dizia "Apagar tudo e recomeçar"
quando só fazia logout — agora diz "Sair da conta".
**Por quê:** seis handlers com duas definições e três funções com sombra eram a maior fonte de
leitura errada do arquivo — a primeira versão parece viva e não é.
**Descartado:** manter as ações mortas "como API de teste" (teste que exercita código morto não
protege nada; o fluxo da ficha é o que o usuário usa).
**Onde:** `index.html` (bloco AÇÕES, `esc`, `benchList`, `viewStats`, `statsAnos`, `pSheet`,
`doImport`) · `scripts/smoke.py` (passos reescritos pelo fluxo da ficha).


### D-67 · Fim do monkey-patch — e os contratos com os testes viram texto no código
**31/08/2026.** Três mudanças de estrutura, comportamento idêntico. **(1)** As três funções que o
bloco de conta **reatribuía** viram definição única: `membrosCard` é a função que decide (admin com
backend → lista de contas; senão → `membrosCardBase`), `viewCfg` é a composição declarada (cartão
do convite + `viewCfgBody` + `logCard`), e `renderHome` ganhou no próprio template o botão "Entrar
com um código", o card "Aguardando aprovação" e o rodapé de conta — o patch antigo fazia cirurgia
no DOM pronto (`insertAdjacentHTML` antes da `.hr`), o que amarrava o backend ao layout da home:
mudar a `<div class="hr">` quebrava o botão em silêncio. De quebra morreu o último texto
pré-backend do app ("Dados salvos só neste aparelho… funciona offline"). **(2)** O corte que o
`test.py` fazia por `split('   RENDER')` (três espaços, contrato invisível) virou o marcador
explícito `@@FIM-DO-MOTOR@@` no `index.html`, com `assert` no teste; os dois `replace` mortos do
`test.py` (apontavam para código de localStorage que não existe mais) viraram um stub real de
`save()` com `assert`. **(3)** `smoke.py` ganhou o teste de cobertura de papel: toda ação de `A`
tem que estar em `ACOES_LANCAR`, `ACOES_ADMIN` ou na lista explícita de LIVRES (só-leitura,
checagem interna ou conta) — ação nova esquecida fora dos conjuntos derruba o teste em vez de
nascer desprotegida; e os conjuntos não podem listar ação que não existe. `scorerSide` e
`clearSel` entraram em `ACOES_LANCAR` (o `scorerSide` despachava para `goalScorer` por dentro,
pulando a checagem do dispatcher).
**Por quê:** eram os três pontos onde ler o código enganava — a função que se lê não é a que roda —
e os dois contratos por convenção que nenhum aviso protegia.
**Descartado:** separar em `engine.js`/`ui.js`/`sync.js` via `<script src>` (funciona e os testes
até melhorariam, mas abandona o "é uma página só" sem necessidade atual — fica documentado como
opção); ES modules (strict mode quebraria o que restasse de reatribuição e `file://` deixa de
abrir).
**Onde:** `index.html` (`membrosCard`/`membrosCardBase`, `viewCfg`/`viewCfgBody`, `renderHome`,
marcador `@@FIM-DO-MOTOR@@`, `ACOES_LANCAR`) · `scripts/test.py` (extração com assert) ·
`scripts/smoke.py` (passo "toda acao tem classificacao de papel").


### D-68 · A documentação alcança o backend — a §8 sai da era do localStorage
**31/08/2026.** Varredura de documentação contra o código. **DOCUMENTACAO.md:** a §8 ("estado do
protótipo") ainda descrevia a v1 — "tudo em localStorage, funciona offline", backend/contas/sync
listados como v2 futura, sequências e edição de nome como inexistentes (tudo isso já existia);
reescrita para o estado real, com a lista "ainda não existe" de verdade (link de convite, offline,
recuperação de senha, papel de escrita no servidor, temporadas…). Corrigidas as duas menções
erradas ao empate com 3 times ("os dois saem" — contradizia a própria §"Fila com 3–4 times" e o
código, D-39), o botão "↻ Girar" que não existe desde D-32 (também em REGRAS-DO-RACHA.md e
RF-05.3l), o rótulo real do botão de vincular ("Sou eu", não "Este perfil sou eu"), a §7.3 marcando
link/busca como v2 e removendo a "entrada livre" que nunca existiu, e o princípio 11 que ainda
citava a proteção pós-promoção (D-46). **REQUISITOS:** RF-03.7/03.10 atualizados para 15 partidas
e K 64/32 (D-53/D-55); RF-10.1/10.2 deixam de afirmar "local e offline" (a versão com backend
precisa de rede); RF-10.3 (sincronização) marcado ✅; RF-11.15 parcial (sequências existem);
RNF-03.1/03.5 idem. **README:** modelo em partes (não "um documento jsonb"), botão do demo só sem
liga nenhuma, `sync.py` na lista de testes, `config.js`/`schema.sql` na estrutura, "sem
dependências" corrigido (supabase-js via CDN + fontes). **CLAUDE.md e DEPLOY.md:** a lista de
testes vira os 4 obrigatórios + `visual.py` opcional — os três documentos citavam conjuntos
diferentes. **BANCO-DE-DADOS.md:** cabeçalho sem localStorage; §8 explica que hoje a concorrência
é a trava de `leagues.version` (o `unique(session_id, ordem)` é alvo); §9 offline marcado como
alvo; nota sobre derivados (o esquema atual não grava nenhum — D-63).
**Por quê:** doc que contradiz o código (ou a si mesma, caso do empate) ensina errado exatamente
quem ela existe para ensinar.
**Descartado:** apagar a parte "alvo relacional" de BANCO-DE-DADOS.md (continua sendo o desenho da
v2 — só ganhou as notas de "hoje é assim").
**Onde:** DOCUMENTACAO.md (§2, §4.2, §5.5, §7.3, §8, §8.1, §9) · REGRAS-DO-RACHA.md ·
REQUISITOS-FUNCIONAIS.md · REQUISITOS-NAO-FUNCIONAIS.md · README.md · CLAUDE.md · DEPLOY.md ·
BANCO-DE-DADOS.md · `.gitignore` (exemplo_partida_real.json, dados reais, fora do repositório).


### D-69 · Aproveitamento vira pontos (V=3, E=1) — e cada filtro de Stats responde à própria pergunta
**31/08/2026.** Três mudanças na leitura dos números. **(1) Aproveitamento passa a ser pontos, como
o futebol conta:** (3·V + E) / (3·partidas), via `aprDe` no motor. A % de vitórias pura tratava
empate como derrota — e racha empata muito. Vale em todo lugar que diz "aproveitamento": o anel do
painel (a linha `X de Y pontos` que explicava a conta foi testada e removida no mesmo dia — poluía
mais do que explicava; a fórmula fica na doc e no título do ranking), o ranking "Maior
aproveitamento", os sub-rótulos de vitórias/derrotas, duelos, parcerias, melhor dupla, a folha do
confronto, o ano a ano, a ficha do jogador (antes rotulada "% vitórias") e o desempate dentro do
degrau da escada (para quem não é admin — o critério continua não denunciando o rating, D-57).
**(2) O piso dos destaques vira 2 rachas OU 15 partidas** (era E com 20): duas noites já mostram
constância; uma noite inteira — 15 partidas, o tamanho da calibração — já mostra volume. O OU também
elimina o caso especial da partida única (D-65): lá 2 rachas bastam. **(3) A ordem dos rankings da
aba Stats → Racha segue a pergunta do filtro:** *30 dias* pergunta FORMA (aproveitamento, vitórias,
sequência, artilharia abrem); um *ano* pergunta TEMPORADA (presenças e campanha primeiro); *Sempre*
pergunta CARREIRA (volume: presenças, tempo em quadra). Na partida única o +/− abre em qualquer
filtro (D-45). As seções são as mesmas; só a ordem muda com o filtro.
**Por quê:** "aproveitamento" com outra fórmula que não a dos pontos surpreende qualquer pessoa de
futebol; e uma lista fixa de rankings obrigava quem filtra "30 dias" a rolar por presenças de
carreira antes de chegar na forma.
**Descartado:** trocar TODA % por pontos (a "% de empates" da liga e a chance esperada do confronto
são frações de outra coisa e ficam como estão); piso configurável; esconder seções por filtro (a
ordem resolve sem tirar informação).
**Onde:** `aprDe`, `destaques` (piso e desempate), `linhaDestaque`, `viewRanking` (desempate),
`viewStats` (anel + pontos, duelos, parcerias, duplas, ano a ano, SECS com ordem por filtro),
`pSheet`, folha do duelo em `index.html` · DOCUMENTACAO §5.3/5.4 (definição, piso, ordem) ·
RF-08.9, RF-11.1, RNF-04.9 · `test.py` (aprDe e o bloco novo do piso OU).


### D-70 · Cada ranking tem uma setinha — e vira o próprio ranking do fim
**31/08/2026.** Todo ranking da aba Stats → Racha (presenças, tempo, vitórias, derrotas, +/−,
aproveitamento, artilharia, ritmo, menos vazado, sequência e melhor dupla) ganhou uma **setinha de
ordem** no cabeçalho: **↓** é o padrão (do melhor para o pior) e **↑** lê a MESMA lista inteira do
fim — quem está pior naquele número. Não é o top 10 de cabeça para baixo: as listas deixaram de ser
cortadas na origem (o corte para 3/10 desceu para o `rkBars`), então inverter mostra o outro
extremo de todo mundo que entra no ranking (respeitando os pisos — o pior aproveitamento continua
exigindo as 10 partidas). A posição volta a contar do 1, porque é outro pódio. A escolha fica por
ranking em `S.ui.statsInv`, preferência do aparelho (localStorage), como aba e tema.
**Por quê:** "quem mais perdeu" já existia como espelho de "quem mais ganhou" no card da noite —
a pergunta espelhada é natural em todo ranking ("quem menos aparece?", "qual goleiro mais sofre?"),
e uma setinha custa menos que onze rankings-espelho.
**Descartado:** inverter só o top 10 visível (mostraria o 10º como "pior" da liga, mentira);
títulos que trocam de texto quando invertidos ("Menos presenças…") — a seta e o title do botão já
dizem, e onze títulos duplicados envelheceriam mal; setinha nos cards do último racha —
**revisto no dia seguinte, a pedido**: lá também é ranking, e a setinha entrou em ganhou/perdeu,
+/−, artilheiro, rendeu, tempo e menos vazado (gol contra e nível são listas, não rankings). No mesmo dia saiu a linha
`X de Y pontos` do anel (D-69): poluía mais do que explicava.
**Onde:** `inv`/`ordBtn`/`rkBars` e a ação `statsInv` em `index.html` · CSS `.k2 .ord` ·
DOCUMENTACAO §5 (parágrafo dos rankings) · RF-11.8 · `smoke.py` ("inverter um ranking pela setinha
e voltar", e `statsInv` na lista de ações livres).


### D-71 · Quem fica não troca de lado — e a folha de trocar time fala nomes no 5v5
**31/08/2026.** Dois consertos na pré-partida. **(1)** O `suggestPair` sempre punha o time que
ficou (venceu, ou ficou no empate com 3 times) no lado **esquerdo** da tela, mesmo que ele tivesse
acabado de jogar do direito — na quadra ninguém se moveu, mas no app o confronto aparecia
espelhado, e quem lança se perdia. O `finish` agora grava **de que lado** o time que fica jogou
(`lv.lastSide`) e a sugestão o mantém ali: só o lado de quem saiu recebe o time da fila. O
instantâneo do "↩ Voltar a partida" e o remontar de times carregam/zeram o lado junto; racha antigo
sem `lastSide` cai no comportamento de antes (esquerda). **(2)** A folha "Quem joga deste lado?"
(trocar qual time entra) mostrava só "Time A (5)" — em liga até 5v5, onde o time é a lista de quem
joga (D-60), agora mostra **os nomes** (via `nomesCurtos`), com o apelido da cor e a contagem na
linha de baixo. Acima do 5v5 fica como era: a lista não caberia.
**Descartado:** guardar o lado por time em vez de só o de quem ficou (só quem fica tem lado a
preservar — quem entra da fila entra no lado vago por definição); deixar o usuário arrastar times
entre lados (o toque em cada lado já resolve).
**Onde:** `suggestPair`, `finish` (`lv.lastSide`), `voltarPartida`, `applyPlan`, `pickSide` em
`index.html` · DOCUMENTACAO §"a próxima partida" · `smoke.py` (os roteiros de 4 times e de empate
com 3 times agora afirmam o lado mantido — inclusive o goleiro que fica, pelo lado certo).


### D-72 · "Quem mais perdeu" sai do card da noite — a setinha já conta essa história
**31/08/2026.** O card do último racha perdeu a seção "😵 Quem mais perdeu" (nascida no D-54): com
a setinha de ordem (D-70) em "🏆 Quem mais ganhou", a leitura espelhada está a um toque, e duas
listas quase iguais uma embaixo da outra só esticavam a tela da noite. Rigorosamente a inversão
mostra "menos vitórias" (entre quem venceu), não "mais derrotas" — mas na prática da noite é a
mesma conversa, e quem quiser o número exato de derrotas tem o V/E/D em cada linha e o "Mais
derrotas" nos rankings de temporada, que fica.
**Descartado:** tirar também o "Mais derrotas" da temporada (lá a lista é longa, o recorte por
derrotas absolutas é outra pergunta, e ninguém pediu).
**Onde:** `cardsUmRacha` em `index.html` · DOCUMENTACAO §5 (lista dos cards da noite) · `smoke.py`
(o passo agora garante que a seção NÃO volta).


## Como registrar uma decisão nova

Uma linha por decisão, nesta ordem: **o que foi decidido** (com a data), **por quê**, **o que foi
descartado** e **onde ela vive** — documento, função e teste. Se não tem teste, diga que não tem.
Decisão sem "por quê" volta a ser discutida em três meses; decisão sem "onde" vira lenda.
