# Decisões · Times, fila e goleiro

> Montagem, fila do "de próximo", vencedor fica, goleiros fixos e rodízio, formato e modo da liga, duplas.
> Índice de todas as decisões e regra de registro em [README.md](README.md).

---

<a id="d-06"></a>
### D-06 · Time é sempre cheio; quem sobra é fila
**18/08/2026.** No 5v5 se joga 5 contra 5. O app monta **quantos times inteiros couberem** e o resto
espera. Não existe time de 3 esperando a vez. Nem forçando 3 ou 4 times: o botão que não cabe fica
apagado. Único caso de jogo com menos: quando nem dois times cheios dão (8 pessoas → 4v4, com aviso).
**Por quê:** quadra no Brasil não tem jogo menor que o formato. Time incompleto não é arranjo, é problema.
**Descartado:** "sobra ≥ 60% vira time menor" e a variante "times parelhos 5/4/4" — as duas produziam
lados desiguais em quadra.
**Onde:** [Regras do racha §2.1](../produto/regras-do-racha.md) · [Fluxo do racha §2](../produto/fluxo-do-racha.md) · RF-05.2/5.3d · `planCaps`, `planTeams` · testes `[3]`, smoke.

<a id="d-07"></a>
### D-07 · Reserva presa a um time só existe na partida única
**18/08/2026.** No racha curto quem está fora é da **fila do racha**, não do banco de um time.
**Por quê:** no modo curto os times rodam; ficar preso ao banco de um time é ficar de fora sem entrar
na roda. No modo longo os dois times são fixos a noite toda — aí reserva é o desenho certo.
**Onde:** [Regras do racha §2.1 e §4](../produto/regras-do-racha.md) · RF-05.3d.

<a id="d-08"></a>
### D-08 · A fila é de pessoas: o "de próximo"
**18/08/2026.** Ao fim de cada partida: **quem ganhou fica, quem perdeu sai, a fila entra no lugar de
quem saiu, e quem sai vai para o fim da fila**. Se a fila não dá para trocar o time inteiro, **alguns do
time que perdeu ficam para completar** — entram 3, ficam 2, normalmente o goleiro e mais um. Sai quem
mais jogou na noite. Empate com 2 times não gira sozinho; existe **↻ Girar** para a mão.
**Por quê:** é o que todo racha já faz. O app antes deixava quem estava de fora parado a noite inteira.
**Onde:** [Regras do racha §2.2](../produto/regras-do-racha.md) · [Fluxo do racha §2](../produto/fluxo-do-racha.md) · RF-05.3j/3k/3l · `filaDe`, `rodaFila` · smoke.

<a id="d-09"></a>
### D-09 · Time curto é completado, nunca compensado sentando alguém
**18/08/2026.** Quando um time entra com menos gente (alguém foi embora, alguém foi movido), o app
**completa com quem está na fila** — sugerindo quem menos jogou — e **quem escolhe é o usuário**. Quem
completa joga por empréstimo: volta para o time dele quando a partida acaba. Dá para recusar e jogar
com menos dos dois lados.
**Por quê:** o comportamento anterior encolhia o time maior — dois caras já escalados sentavam.
**Onde:** [Regras do racha §2.3](../produto/regras-do-racha.md) · RF-05.3g/3h/3i · `fillDe`, `cardCompletar` · smoke.

<a id="d-10"></a>
### D-10 · Quem fica de fora também é equilibrado
**18/08/2026.** A fila é uma **fatia que atravessa todos os níveis** (um sorteado de cada faixa), nunca
os piores do racha.
**Por quê:** o draft ia do melhor para o pior, então quem não cabia era sempre o fundo da lista.
**Onde:** [Fluxo do racha §2](../produto/fluxo-do-racha.md) · [Regras do racha §2.1](../produto/regras-do-racha.md) · RF-05.14 · `fatiaEquilibrada` · teste `[2b]`.

<a id="d-11"></a>
### D-11 · Ruído na montagem para variar — e só na montagem
**18/08/2026.** O sorteio do draft usa o nível de cada um **mais um ruído de ±25 pontos internos**; o
refinamento (as centenas de trocas 1:1) e o desempate de panelinha usam o **nível real**.
**Por quê:** com gente parelha existem dezenas de arranjos igualmente equilibrados, e sem ruído
"Equilibrar" devolvia sempre o mesmo. Medido: 14 montagens dão 13-14 arranjos distintos, e o pior
desequilíbrio caiu para 6-10 pontos — melhor que o algoritmo determinístico anterior, porque cada
sorteio explora um ótimo local diferente.
**O ruído não sai do montador:** chance de vitória, barra de equilíbrio e veredito usam nível real.
**Onde:** [Fluxo do racha §2](../produto/fluxo-do-racha.md) · RF-05.13/5.15 · `buildTeams` · teste `[2b]`.

---

## Destaques e números

<a id="d-32"></a>
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

<a id="d-35"></a>
### D-35 · O app aponta duplas inseparáveis em vez de fingir que as separa
**28/08/2026.** `inseparaveis()` lista duplas com ≥35 partidas e ≥80 % do histórico do menor dos
dois em comum; aparecem em Stats → Racha e como aviso na ficha de cada um.
**Por quê:** é limite do modelo, não bug — no Elo por time, dois jogadores sempre no mesmo lado
recebem exatamente os mesmos deltas e terminam com o mesmo rating. Tentar "descontar" isso no motor
(peso por contribuição, gols, etc.) inventaria informação que o app não tem. Mostrar onde o dado
está cego e dizer o remédio (separar por algumas noites; `avoidRepeat` já existe) é honesto e
funciona.
**Onde:** `inseparaveis`, `JUNTOS_MIN`/`JUNTOS_PCT`, `viewStats` (cardJuntos), `pSheet`.

<a id="d-39"></a>
### D-39 · Empate com 3 times: um fica; goleiro fica com o time que fica
**28/08/2026.** `lv.lastStay` guarda quem ficou em quadra depois de cada partida: o vencedor; no
empate com 3 times, o que entrou por último (o que já estava sai); com 4 times, ninguém; com 2,
os dois. `planGks` segura o goleiro do rodízio para todo time em `lastStay` — não só o vencedor.
**Por quê:** é a regra da quadra; "empate os dois saem" com 3 times deixava a quadra vazia para o
único time da fila.
**Onde:** `finish` (rotação), `planGks`, `suggestPair` (via `lastWinner`).

<a id="d-42"></a>
### D-42 · Goleiro fixo é um dos N; gols abaixo das substituições
**28/08/2026.** Na escalação (`escCol`), o número de lugares de linha é `per` menos 1 quando o
goleiro é fixo (fora do rodízio) — ele ocupa um dos `per` lugares. Goleiro do rodízio continua
entrando além de `per`. Na partida ao vivo, o cartão **Gols** passa para baixo do cartão de
reservas/fora (substituições), antes de "Partidas de hoje".
**Por quê:** na partida única (e em qualquer racha com um goleiro por time) aparecia uma vaga
fantasma em cada time. E na partida longa a lista de gols cresce muito e empurrava para longe
os nomes de quem pode entrar.
**Onde:** `escCol`, `viewJogo` · smoke "partida unica com goleiro fixo: escalacao sem vaga fantasma".

<a id="d-44"></a>
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
[Princípios](../produto/principios.md) (decisão 13) · smoke "nova liga escolhe formato e modo na criacao".

<a id="d-49"></a>
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
presenca desde o comeco", "presentes do ultimo racha") · [Stats §2](../produto/stats.md).

<a id="d-50"></a>
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
escalacao original") · [Stats §2](../produto/stats.md).

<a id="d-56"></a>
### D-56 · Dupla inseparável: aviso a partir de 20 partidas juntos
**29/08/2026.** `JUNTOS_MIN` 35 → **20** (o critério de 80 % do histórico em comum não muda).
Com as ~7 partidas por pessoa por noite do racha real, 35 eram ~5 rachas sempre juntos antes do
aviso; 20 são ~3 — proporcional ao encurtamento da calibração (D-53) e ao K mais rápido (D-55):
se o nível converge em 2 rachas, a dupla colada precisa ser apontada na mesma escala, antes de os
dois Elos se fundirem por construção.
**Descartado:** baixar também os 80 % (quem joga separado às vezes já dá sinal ao motor); piso em
rachas em vez de partidas (a parceria é contada por partida no histórico).
**Onde:** `JUNTOS_MIN` · `test.py` [15] · [Protótipo](../tecnico/prototipo.md) (duplas inseparáveis).

<a id="d-71"></a>
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
`index.html` · [Fluxo do racha §2](../produto/fluxo-do-racha.md) §"a próxima partida" · `smoke.py` (os roteiros de 4 times e de empate
com 3 times agora afirmam o lado mantido — inclusive o goleiro que fica, pelo lado certo).

<a id="d-77"></a>
### D-77 · Times do racha: % de vitórias realizada × probabilidade de vitória no apito
**31/08/2026.** No card do último racha, cada time ganhou uma linha discreta **abaixo da contagem
V E D**: `50% V (esp. 62%)` — a % de vitórias que o time de fato teve na noite contra a **média das
probabilidades de vitória** que ele tinha no apito de cada partida (a mesma chance do histórico,
D-75, agregada pelo dono da partida via `timeDoLado`/D-59). Só nível entra no "esperado" — nada do
resultado da noite contamina a régua (a primeira versão corrigia pela taxa de empate da noite e
saiu a pedido: comparar chance com vitórias puras é mais honesto e mais legível). Some com as
patentes fechadas, como toda % de confronto (D-52).
**Por quê:** é a versão de time do "rendeu acima do esperado" — mostra em um relance se o time
que mais venceu era mesmo o favorito ou se atropelou o nível.
**Descartado:** aproveitamento em pontos esperado×realizado (exigia modelo de empate e misturava
resultado da noite na expectativa); coluna própria (chamaria atenção demais — o pedido era
discrição).
**Onde:** `cardsUmRacha` (acumulador `esp`/`jE` e a linha sob o V E D) em `index.html` ·
[Stats](../produto/stats.md) (leitura da noite) · `smoke.py` (regex `esp. N%` no card da noite).

<a id="d-87"></a>
### D-87 · Patente média do time no cabeçalho do cartão
**01/09/2026.** Na tela de times, a única leitura de força era a barra de equilíbrio e o
veredito ("leve vantagem…") — globais. Agora cada cartão mostra, ao lado do nome, a **patente
média** de quem está nele (média dos Elos pelo papel — goleiro pela patente de goleiro —
convertida no degrau da escada, `stepOf(teamAvg)`), no badge curto padrão, pequeno para não
competir com o nome. Respeita `vePat`: com patentes fechadas (só admin), some para os demais.
**Descartado:** número (viola "o número não existe"); média só da linha (o goleiro joga e conta
no equilíbrio, então conta na leitura).
**Onde:** `.team .hd .pat` e o cartão de time em `viewTimes` (`index.html`) · conferido no
`visual.py` (tela 2, claro/escuro) · [Fluxo do racha §2](../produto/fluxo-do-racha.md).

<a id="d-111"></a>
### D-111 · Folha do time do racha: patentes e as partidas do time
**03/09/2026.** Em Stats → Último racha, tocar num time mostrava só a lista de nomes. Agora cada
nome vem com o mini-badge de patente (o da presença, D-88; goleiro do rodízio pela trilha de
goleiro) e embaixo entra **Partidas do time**: uma linha por partida com resultado, placar pelo
lado do time, o adversário (até o 5v5, quem estava em quadra do outro lado, como no histórico —
D-60) e a **chance no apito** (D-75; some com as patentes fechadas), com o V/E/D somado no
cabeçalho. A partida é do time pela composição em quadra (`timeDoLado`, D-59), a mesma regra do
card — então o V/E/D da folha bate com o da lista. Racha em andamento usa os times do próprio racha.
**Ajuste no mesmo dia:** o rótulo é "prob. de vitória", nunca "chance no apito" (o app inteiro fala
em probabilidade de vitória); a dica do card virou "toque para ver detalhes"; e as linhas dos
times ficaram compactas (12,5px, menos respiro) — ocupavam a tela como se fossem cards. No rodízio
a luva 🧤 voltou ao lado de quem é goleiro de fato (`p.gk`): jogador de linha também roda, e sem
ela os dois pareciam iguais — é informação, não enfeite.
**Onde:** `A.rachaTime` em `index.html` · [Stats §2](../produto/stats.md) · `scripts/.tmp/shot_stats.py time`.

<a id="d-122"></a>
### D-122 · Mexer no elenco no meio do racha: sair e voltar, goleiro que chega, improvisado no gol, refazer times
**Quando:** 2026-09-04.
**O quê:** uma varredura de todos os cenários de substituição, chegada e saída (pré-partida e ao
vivo) rodada no motor real achou seis quebras, todas corrigidas no mesmo commit:
1. **"Foi embora" em quadra + `↶`** devolvia a pessoa só à escalação: fora da presença, do time e
   da fila, ela sumia do racha na partida seguinte (e nem aparecia na folha do "Foi embora"). O
   evento de saída agora guarda onde ela estava (`left`: posição na escalação, time e posição
   nele, 🧤 do dia, lugar no rodízio, "completando") e o `↶` devolve tudo (`voltaDoEmbora`).
2. **Goleiro escolhido na mão para a próxima** (folha do 🧤) que ia embora **entrava em quadra**
   mesmo assim: `leaveDo` não limpava `nextGks`. Agora a escolha manual cai e volta a sugestão.
3. **Rodízio, alguém do time improvisa no gol na pré-partida:** a tela mostrava a vaga e sugeria
   quem completa (D-117), mas a largada media o time pelo total da escalação e cortava quem
   completava — 4v5. `startMatch` agora conta a linha **sem o goleiro** quando há rodízio.
4. **Racha com goleiro fixo, "chegou para ser goleiro":** ia para um `gkPool` num racha sem
   rodízio e a largada o escalava além dos 5 de um lado só — 6v5, sem aviso. Agora entra na
   **fila com o 🧤 do dia**: completa ou troca de lugar como qualquer um, e é o goleiro do lado em
   que entrar. Descartado: virar rodízio sozinho (mudaria o tamanho dos times no meio do racha) e
   perguntar em qual time entra (o time cheio não tem vaga de goleiro).
5. **Aviso "jogando 4v5"** só olhava o lado esquerdo; agora o menor dos dois.
6. **Refazer times** deixava `lastStay`/`lastGks`/`nextGks` da rodada antiga: o time novo de
   mesmo número herdava "🧤 fica" e o goleiro do vencedor. `applyPlan` zera os três.
**Por quê:** racha é racha — gente chega, sai, volta, improvisa; cada um desses cenários tinha um
caminho que deixava o estado do racha e o da partida em desacordo. Consistência acima de tudo
(D-104): o `↶` tem que desfazer o lance **inteiro**, e ninguém que foi embora pode ser escalado.
**Verificado e deixado como está:** de fora → linha/🧤/vaga e `↶`; linha ⇄ 🧤; 🧤 → vaga; goleiro
em quadra indo embora; time que espera perdendo gente e entrando completado; 4 times com dois
faltando; sair e voltar no mesmo racha (presença única na sessão); "marquei errado" com time
escalado; partida única titular ⇄ reserva e reserva do outro time; cancelar; empate com 2 times
(D-39). **Atritos anotados, sem mudança:** chegou → time cheio vira "reserva" que só entra à mão
quando não há fila; não há "Foi embora" na tela de times (voltar à presença remonta tudo); ao
vivo não há gesto linha ⇄ linha entre lados (é em dois lances, por alguém de fora).
**Onde:** `leaveDo`, `voltaDoEmbora`, `undo`, `startMatch`, `lateGk`, `applyPlan`, `viewJogo` em
`index.html` · [Fluxo §3](../produto/fluxo-do-racha.md) · `scripts/smoke.py` bloco
"elenco no meio do racha (D-122)".

<a id="d-123"></a>
### D-123 · Pré-partida com a gramática da partida ao vivo: 🧤, gol vazio e vaga são slots; a vaga fica sempre à vista
**Quando:** 2026-09-04.
**O quê:** a substituição de goleiro na tela da próxima partida deixou de passar por folha
("No rodízio / Alguém do time / Sem goleiro"): o 🧤, o gol vazio e a vaga de linha entram na
**mesma gramática de toque e arraste da partida ao vivo** (D-103/D-117) — primeiro toque marca,
o par elegível ganha o tracejado verde, segundo toque resolve, mesmo slot desmarca. Como ali não há
partida rodando, cada par mexe no **estado da rodada** (`lancePre`): nome ⇄ nome troca de lugar de
vez (a da montagem, `trocaLugar` — inclusive goleiro fixo ⇄ linha do outro lado); de fora → 🧤 com
rodízio é goleiro só desta partida (`nextGks`) e o do rodízio descansa (agora aparece como chip no
grupo "🧤 Rodízio" do card Fora, de onde volta por toque); de fora → 🧤 com goleiro fixo entra **no
time** no lugar do goleiro e ganha o 🧤 do dia (o goleiro é do time; o antigo vai para a fila com o
🧤); de linha ⇄ 🧤 do mesmo lado trocam de papel nesta partida (com rodízio abre a vaga, D-117);
de fora → vaga completa (empréstimo); 🧤 ⇄ 🧤 trocam de gol (fixo: de time); 🧤 → vaga põe o
goleiro na linha (o do rodízio entra completando). Quem completa (⇄) sai com um toque sem marca.
A folha antiga e a lista de quem completa (com "X hoje") ficam a um toque na dica ("outras opções"
/ "escolher da lista"), porque "sem goleiro definido" e "voltar à sugestão" não têm gesto.
**E a vaga fica sempre à vista:** "Jogar 4v4 assim" tirava o slot da tela; agora um time com um a
menos sempre mostra a vaga tracejada — um toque nela e outro em quem está fora (ou arrastar) volta
a completar.
**Por quê:** o lançador aprendeu um gesto na partida ao vivo e encontrava outro, pior, um passo
antes; e "com um a menos" tem que ter onde encaixar alguém sem procurar botão.
**Descartado:** manter a folha como gesto principal (era o problema); tratar de fora → 🧤 no racha
de goleiro fixo como "só esta partida" (o time ficaria com 6 e o goleiro antigo na linha).
**Onde:** `escalPre`, `pecaPre`, `parPre`, `lancePre`, `trocaLugar`, `mudaFill`, `defineGkPre`,
`A.prePick`, `viewProxima`, `onDrop` em `index.html` · [Fluxo §2–3](../produto/fluxo-do-racha.md)
· `scripts/smoke.py` bloco "pré-partida com a gramática da partida ao vivo (D-123)".
**Ajuste no mesmo dia:** (a) os **times que esperam** também mostram a vaga no card "Fora"
(`vagaT:i`): quem é tocado ou arrastado nela entra naquele time de vez, venha da fila, de outro
time ou de um dos lados que jogam; (b) o chip do card "Fora" carrega a chave **`fora:ID`** — é a
pessoa aí fora, não o slot que ela ocupa. Antes, quem improvisava no gol emprestado (vindo de um
time que espera) continuava listado no time dele e, ao trocá-lo ali com alguém de outro time, a
troca caía no par "de fora → 🧤" e **trocava o goleiro** em vez de trocar de time. Agora troca de
time e ele segue no gol. Teste: os dois últimos passos do bloco D-123 do smoke.
**Ajuste no mesmo dia (2):** o slot do 🧤 na escalação (pré-partida e ao vivo) leva o ponto do
nível pela **patente de goleiro**, como os chips do rodízio no card "Fora" já levavam — o goleiro
era o único nome da escalação sem nível.
