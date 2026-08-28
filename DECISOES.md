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
**Prata 2**, no meio. As cores acompanham os metais. Liga com qualquer escada antiga de fábrica
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

## Como registrar uma decisão nova

Uma linha por decisão, nesta ordem: **o que foi decidido** (com a data), **por quê**, **o que foi
descartado** e **onde ela vive** — documento, função e teste. Se não tem teste, diga que não tem.
Decisão sem "por quê" volta a ser discutida em três meses; decisão sem "onde" vira lenda.
