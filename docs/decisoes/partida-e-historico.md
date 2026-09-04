# Decisões · Partida ao vivo e histórico

> Placar, gols, substituição, fim e volta, revisão da partida, resumo do racha, avisos ao vivo.
> Índice de todas as decisões e regra de registro em [README.md](README.md).

---

<a id="d-18"></a>
### D-18 · A tela da partida é o placar
**18/08/2026.** Relógio compacto no topo (com ⏸ e ✕ como ícones), **placar ocupando ~31vh** logo acima
da barra fixa, `−` no canto de cada time para tirar o último gol, e a barra de baixo com **só** `↶` e
`✓ Fim · placar`.
**Por quê:** é a tela usada 12 vezes por noite, em pé, com uma mão. E "Encerrar racha" estava colado no
"Fim": um toque errado com o próximo time entrando acabava com a noite.
**Onde:** [Fluxo do racha §3](../produto/fluxo-do-racha.md) · RF-06.11c/11d/6.18 · RNF-01.6 · teste visual.

---

## Contas e dados (v2)

<a id="d-28"></a>
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

<a id="d-30"></a>
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

<a id="d-31"></a>
### D-31 · A vaga mora no cartão do time
**28/08/2026.** Time com jogador a menos mostra uma vaga tracejada por lugar vazio dentro do próprio
cartão — na montagem (`slotPick`: fila e reservas de outros times, quem jogou menos hoje primeiro)
e na pré-partida (`fillPick`: completa só aquela partida; o emprestado aparece no cartão com ✕).
**Por quê:** "falta 1" escrito no cabeçalho não dizia o que fazer; o card "Completar" embaixo
resolvia a pré-partida mas a montagem não tinha caminho direto. A vaga é o próprio convite.
**Onde:** `timeCard` (vagas/emprestados), `A.slotPick`/`slotSet`, `viewProxima`.

<a id="d-47"></a>
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
um time pelo do outro; troca gravada pela versão antiga) · [Fluxo do racha §3](../produto/fluxo-do-racha.md).

<a id="d-48"></a>
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
[Fluxo do racha §3](../produto/fluxo-do-racha.md).

<a id="d-58"></a>
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
**Onde:** [Contestação e correção](../produto/contestacao-e-correcao.md) e [Protótipo](../tecnico/prototipo.md) · `fichaPartida`, `fichaLinha`, `revTempo`, `revTrechos`, `revNivel`,
`revDetalhe`, `corTime`, `A.review`, `A.revSec` · `smoke.py` ("revisar partida mostra a partida
inteira", "ficha da partida conta tempo e gols de quem jogou" — o +/− da ficha é conferido
contra `plusMinus`, o motor) · `layout.py` (snapshots com trechos e nível abertos).

<a id="d-59"></a>
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
**Onde:** [Contas e permissões](../produto/contas-e-permissoes.md) (período "Último") · `emQuadraNo`, `timeDoLado`, `timesDoRacha`,
`teamRecord`, `cardsUmRacha` · `smoke.py` ("vitoria e do time que jogou, nao do nome no placar" —
partida normal, time trocado do começo, trocado no meio, uma substituição só e formação sem dono).

<a id="d-60"></a>
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
**Onde:** [Stats §2](../produto/stats.md) e [Contestação e correção](../produto/contestacao-e-correcao.md) · `nomesCurtos`, `timesDoRacha` (filtra o rodízio), `rotuloTime`
em `cardsUmRacha`, `teamRecord`, `mrow` · CSS
`.rk3.time` e `.mrow.nomes` (o rótulo pode ocupar duas linhas) · `smoke.py` (teste do D-59 no card
da noite; "abrir um racha mostra as partidas dele" confere a lista no histórico e a volta ao nome
do time acima do 5v5).

<a id="d-61"></a>
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
**Onde:** [Contestação e correção](../produto/contestacao-e-correcao.md) e [Protótipo](../tecnico/prototipo.md) · `recalcPartida`, `gksIni`, `podeCorrigirEsc`, `escalaEm`,
`genteDaPartida`, `foraDeQuadra`, `ajustaGksEventos`, `tDoMinuto`, `aplicaCorrecaoEsc`,
`rascunhoEsc`, `mudaEsc`, `viewEditEsc`, `viewNovaTroca`, ações `editEsc`/`escPick`/`escGk`/`escDel`/`escSwap`/`escAdd`/
`escAddDo`/`evPick`/`evSet`/`evDel`/`novaTroca`/`ntSet`/`ntOk`/`escSalvar`/`escDescartar` · log `esc` · `smoke.py`
("corrigir escalacao e trocas: rascunho ate o Salvar" — partida de 10 min montada à mão, com troca,
goleiro e gol, conferindo que a partida real só muda no Salvar, que cada mudança vira uma linha do
log, que o Descartar não deixa nada e que o nível bate com o recálculo do zero; "partida antiga nao
aceita correcao de escalacao") · `layout.py` (4 snapshots novos).

<a id="d-64"></a>
### D-64 · Racha ao vivo à prova de tela atrasada — e o Voltar devolve a fila de verdade
**31/08/2026.** Quatro consertos no racha em andamento. **(1)** "↩ Voltar a partida" passa a
restaurar também **`lv.fila`** (a fila de pessoas): o instantâneo `lastEnd` guardava times, fila de
times, vencedor e goleiros, mas o `finish` já tinha girado a fila — quem ia entrar era reclassificado
como "chegou agora" e ia para o fundo. A documentação ([Fluxo do racha](../produto/fluxo-do-racha.md), "Fim sem querer tem volta") sempre prometeu
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

<a id="d-75"></a>
### D-75 · O histórico mostra a chance de cada lado no apito
**31/08/2026.** Cada linha de partida na aba Jogos ganhou, na linha de detalhes, a chance esperada
dos dois lados **no momento em que a bola rolou** — `62% × 38% no apito`. A conta sai de `m.pre`
(o Elo de cada jogador antes daquela partida, que o `rebuildAll` refaz do zero a cada recálculo)
sobre a escalação de largada: média por lado e a curva do Elo. Nada novo é gravado — é derivado,
como todo o resto. A % some quando a liga fecha as patentes (é % de confronto, mesma regra da
pré-partida, D-52) e em partida onde o `pre` não cobre a escalação inteira (jogador removido do
cadastro, partida anulada recém-sincronizada).
**Por quê:** "ganhamos, mas éramos favoritos ou zebra?" é a pergunta que dá graça ao histórico — e
é a mesma informação que o "rendeu acima do esperado" já usa por baixo, só que visível por partida.
**Descartado:** gravar a chance na partida (derivado não sobe, D-63); mostrar dentro da revisão
apenas (a graça é bater o olho na lista da noite); recomputar com o nível de HOJE (mentiria — a
zebra de ontem pode ser o favorito de hoje).
**Onde:** `chanceHist` e `mrow` em `index.html` · [Fluxo do racha](../produto/fluxo-do-racha.md) §"como o racha acontece"
(histórico) · `smoke.py` ("historico mostra a chance de cada lado no apito").

<a id="d-92"></a>
### D-92 · Toque errado fora da partida pergunta; dois celulares somam; o celular avisa quando o tempo bate
**02/09/2026.** Revisão do racha ao vivo pensando em erro e pressa, momento a momento. **(1)**
Tudo que não tem volta e mora perto de um botão frequente passa a **perguntar**: "Encerrar racha"
(ficava ao lado do "Começar partida" e fechava a noite em um toque, sem volta), "Desfazer a última"
(ao lado do "Voltar a partida", que tem volta; a pergunta traz o placar), o `↶` numa partida ainda
sem eventos (caía em apagar a partida anterior, sem confirmar) e "Cancelar racha" com presença
marcada. O Fim continua sem confirmação (D-48): ganha um **toast de 7 s com "↩ voltar"**, e começar
outra partida fecha o toast. **(2)** Placar: **toque duplo não é dois gols** (0,6 s, na camada de
clique — o motor e os testes seguem chamando `goal` à vontade) e o `−` fica numa **zona morta**
(`data-a="nada"`): errar por pouco não vira gol. **(3)** Bateu o **tempo**: vibra e apita, uma vez
por partida — a tela está no chão da quadra. O alvo de gols não apita, é um toque da própria pessoa.
O `AudioContext` nasce no "Começar partida" (gesto do usuário) para o navegador liberar o som.
**(4)** Cancelar partida devolve o rodízio de goleiros (foto `cur.pre` tirada antes de `commitGks`)
e deixa o mesmo confronto sugerido. **(5)** "Foi embora" para quem **ainda não jogou** vira uma
escolha: *esteve no racha* (conta presença, D-49) ou *marquei errado* (`leaveDo` com `modo:'nao'`,
não entra em `leftIds`); quem já jogou sai contando, sem pergunta nova. **(6)** **Dois celulares na
mesma partida**: no conflito de versão o `live` local era substituído pelo remoto e a ação
recém-lançada sumia em silêncio. Agora `mesclaLive` soma os eventos da partida corrente quando as
duas têm a mesma largada (`startedAt`): união por chave (`t|type|side|out|in|id`), placar,
escalação, goleiros e pausa refeitos por `replayCur` (o mesmo caminho do `splitStints`), autor de
gol marcado só aqui levado junto; o snapshot guarda o remoto para a soma subir na gravação seguinte.
Partida encerrada no outro aparelho prevalece; presença e times seguem "último que gravou". **(7)**
A tirinha "quem fez?" conta como tela ocupada: um delta não a apaga; quando ela some, o que ficou
pendente é buscado.
**Por quê:** a tela da partida é usada 12 vezes por noite, em pé, com uma mão, e o Fim é de propósito
um toque só. O que faltava era a proteção do que fica **em volta** dele: os toques errados mais caros
eram justamente os sem confirmação e sem volta. E o cenário de dois celulares não era exótico — bastava
uma folha aberta (o refetch espera ela fechar) para o gol do outro lado apagar o daqui.
**Descartado:** confirmação no Fim (D-48); mover "Encerrar racha" para os Ajustes (a noite acaba na
quadra, tem que estar ali — só precisa perguntar); trava de "quem está lançando" (um celular só) para
resolver o conflito (a soma resolve o caso real sem impedir os dois de lançar); mesclar presença e
times (fora da partida não há eventos com carimbo; substituir é previsível); espelho em
`localStorage` para funcionar sem rede (é o desenho offline com fila, [Protótipo](../tecnico/prototipo.md) da doc — decisão à parte);
"Lançador corrige resultado das partidas de hoje" (RF-06.2c/D-22: correção é revisão, e revisão é
do admin — vale discutir, mas não é "claramente melhoria"); fim retroativo no momento do gol
decisivo (muda a duração da partida por conta própria).
**Onde:** `endRacha`, `cancelRacha`, `delMatch` (`ok`), `undo`, `cancelMatch`/`startMatch` (`pre`,
`preparaApito`), `leaveRacha`/`leaveDo`, `toast(msg,{ms,act})`/`fechaToast`, `avisaAlvo` em
`tickClock`, o debounce no dispatcher de clique, `.minuszone`/`nada`, `ocupado`/`showScorer`,
`mesclaLive`/`replayCur`/`chaveEv` em `applyDelta` — tudo em `index.html` · `smoke.py` ("toques que
nao tem volta perguntam antes", "o fim deixa um toast com voltar", "marcado por engano sai sem contar
presenca", "cancelar a partida descarta tudo") · `sync.py` ("dois celulares na mesma partida") ·
[Fluxo do racha §3](../produto/fluxo-do-racha.md)/[Fluxo do racha §4](../produto/fluxo-do-racha.md)/[Protótipo](../tecnico/prototipo.md) · RF-04.4b/04.6/04.7/06.2b/06.6/06.11/06.11c/06.14/06.18/06.19 ·
[Banco de dados](../tecnico/banco-de-dados.md) §"concorrência".

<a id="d-99"></a>
### D-99 · O resumo do fim do racha conta a noite inteira
**02/09/2026.** O resumo tinha três números e uma lista de "mudanças de nível" com a mesma seta
para quem subiu e quem caiu. Agora (`resumoRacha`): data e tempo de bola rolando; partidas, gols,
pessoas e minutos; **times da noite** pela composição original (D-59), com V/E/D (V verde, D
vermelho), gols marcados·sofridos e realizado × esperado (D-77/D-97); **artilheiros** e **quem
mais ganhou** (top 3, mínimo 2 partidas); **subiu** (▲ verde) e **caiu** (▼ vermelho) de nível,
cada um com o badge de onde saiu → onde chegou (o `from` do primeiro movimento da noite e o nível
atual). Tudo em linhas de colunas fixas (`.sumrow`), a mesma gramática dos rankings da Stats.
**Descartado:** repetir aqui o card inteiro do "Último racha" da Stats (tempo em quadra, menos
vazado, gols contra…): o resumo é para mandar no grupo, cabe numa tela; o resto está na Stats.
**Onde:** `resumoRacha` (chamado por `endRacha`) e CSS `.sumrow` em `index.html` ·
`scripts/visual.py` (tela 14) · [Fluxo do racha §4](../produto/fluxo-do-racha.md).

<a id="d-100"></a>
### D-100 · O racha em andamento se anuncia: selo "● ao vivo" e ponto vermelho na aba
**02/09/2026.** Quem abre o app com um racha rolando (o outro celular lançando, ou a própria
pessoa em outra aba) não tinha sinal nenhum. Agora `aoVivo(liga)` acende um ponto vermelho
pulsando na aba **Racha** quando se está em outra aba, o selo **● ao vivo** na linha do racha de
hoje na aba **Jogos** (e no cabeçalho dele), e na lista de ligas ("montando" enquanto ainda é
presença ou times; "ao vivo" com o racha começado). Vermelho e pulso curto, para não se
confundir com o ponto verde e lento das opiniões pendentes (D-95).
**Onde:** `aoVivo`/`seloVivo`, `drawApp` (nav), `renderHome`, `viewHist` em `index.html` ·
`scripts/smoke.py` ("o racha de hoje aparece como ao vivo") · [Fluxo do racha §3](../produto/fluxo-do-racha.md).

<a id="d-101"></a>
### D-101 · Sem faixa "Trocando X"; autor do gol no polegar, com aviso enquanto faltar
**02/09/2026.** (1) A faixa "Trocando Fulano — toque em quem entra" saiu da montagem e da
pré-partida: o nome selecionado já fica marcado, e tocar nele de novo desmarca — a faixa era um
segundo aviso da mesma coisa. (2) A tirinha "quem fez?" sumia em 6 s; agora fica 10 s (15 s no gol contra), logo abaixo
do placar, onde o olho já está (uma versão flutuando acima da barra de ação foi testada e
descartada: ficava baixa demais na tela), e, enquanto houver gol sem autor, um aviso discreto abaixo do placar ("⚠️ 1 gol
sem autor — toque para marcar") abre a escolha do autor do último deles. Gol sem autor continua
valendo como sempre (D-14 decide se a artilharia é confiável); o aviso é para o esquecimento, não
um bloqueio.
**Onde:** `viewTimes`/`viewProxima` (sem `selBar`), `viewJogo` (`.noauthor`), `showScorer`
(tempo) e CSS `.scorerbar` em `index.html` · `scripts/smoke.py` ("gol sem autor avisa") ·
[Fluxo do racha §2](../produto/fluxo-do-racha.md)/[Fluxo do racha §3](../produto/fluxo-do-racha.md).

<a id="d-103"></a>
### D-103 · Substituição por toque sem folha: marca um, toca no par
**02/09/2026.** A substituição por toque abria uma folha ("Sai Fulano — quem entra?") que escondia a
escalação e quem estava fora — justamente o que a pessoa precisa olhar para escolher. E segurar um
nome sem arrastar (o dedo demora mais de 150 ms, comum com a mão suada) armava o arraste, soltava no
lugar e caía no vazio: o nome "não respondia". Agora o toque marca o nome (em quadra ou fora), o par
elegível ganha o tracejado verde do arraste, a dica abaixo da escalação diz o próximo passo ("Sai
Fulano — toque em quem entra" / "Fulano entra — toque em quem sai"), e o segundo toque faz a troca.
Mesmo nome desmarca; outro do mesmo lado move a marca (dois em quadra nunca trocam de time por
toque). Segurar e soltar no lugar vale como toque. A dica padrão passou a "Toque ou arraste num nome
para substituir". Mesma gramática da montagem de times (D-101).
**Descartado:** manter a folha como segundo caminho (dois jeitos de fazer a mesma coisa confundem);
toast a cada marca (a dica já muda no lugar).
**Onde:** `A.subPick` (substitui `outPick`/`inPick`), `viewJogo` (`chipFora`, `dicaSub`,
`data-alvo`), `dispara` + `pointerup` do arraste e CSS `[data-alvo]` em `index.html` ·
`scripts/smoke.py` (marca/desmarca, troca pelos dois lados, dois em quadra só movem a marca) ·
`scripts/layout.py` ("partida com nome marcado para substituir") · [Fluxo do racha §3](../produto/fluxo-do-racha.md).

<a id="d-117"></a>
### D-117 · O 🧤 é um slot como os outros: goleiro entra pela gramática da substituição, e improvisar não encurta o time
**04/09/2026.** Colocar alguém no gol no meio da partida não funcionava como o resto da tela: o slot 🧤
abria uma folha própria que só oferecia o rodízio e "improvisar alguém do time" — e o caso mais comum,
**alguém que não é do time ir para o gol** (o goleiro do rodízio que estava descansando, alguém da fila),
não estava lá. Pior: "improvisar alguém do time" só mudava `gks`, o improvisado continuava contado na
linha e o time **ficava com um a menos** sem que nada mostrasse a vaga (a escalação calculava as vagas
de linha como `per−1` quando o goleiro não era do rodízio, então a vaga nem aparecia). A folha de
goleiro foi apagada. O 🧤 (ocupado ou vazio) e a **vaga** de linha entram na mesma gramática de toque
e arraste da D-103: `pecaAoVivo` classifica o que foi tocado (fora, linha, goleiro, gol vazio, vaga),
`parAoVivo` diz quem é par de quem (é o tracejado verde), `lanceAoVivo` resolve o par — de fora para
qualquer slot (`doSub`, com `out` nulo quando entra numa vaga e `gol` quando entra no gol); de linha ⇄
🧤 do mesmo lado troca de papel (`vaiProGol`, evento `gk` sem `mv`); de linha → 🧤 vazio vai para o gol
**e deixa a vaga de linha já marcada** para o próximo toque; 🧤 → vaga deixa o gol vazio; 🧤 ⇄ 🧤 do
outro lado é a troca de lugar da D-47. **Quem entra no lugar do goleiro é o goleiro**, venha do rodízio ou
não (antes o lado ficava sem goleiro fixo quando o substituto não era do rodízio). Os goleiros do
rodízio que estão descansando deixaram de ser texto ("Descansando: …") e viraram chips no grupo
"🧤 Rodízio" entre os de fora, tocáveis e arrastáveis como todo mundo. A escalação passou a calcular as
vagas de linha pelo **racha**, não pelo goleiro da vez: `lv.rot` (montado com rodízio → o goleiro é
sempre além dos `per` de linha; `comRodizio`). O mesmo bug existia na pré-partida ("Alguém do time" na
folha do 🧤 entrava com um a menos): `fillInfo` desconta o goleiro tirado do time e a vaga aparece como
"＋ completar", como qualquer time curto. Evento `sub` com `out` nulo (entrou numa vaga) é lido pela
reconstrução dos trechos, pelo `↶`, pela mesclagem de dois celulares e pela revisão (que ganhou
"ninguém" em "quem saiu" e mostra "(no gol)" quando o substituto entrou no gol).
**Descartado:** manter a folha como segundo caminho (D-103: dois jeitos confundem); mandar quem estava no
gol para fora de quadra quando alguém de linha vai para o gol (na quadra ele volta para a linha — o
time não fica com um a menos); esconder a vaga e completar sozinho (quem entra é escolha de quem está
com o celular).
**Onde:** `foraList`, `pecaAoVivo`, `parAoVivo`, `lanceAoVivo`, `comRodizio`, `applyPlan` (`lv.rot`),
`normalize`, `escCol`, `viewJogo`, `A.subPick`, `A.doSub`, `A.vaiProGol` (no lugar de `gkSheet`/`setGk`),
`A.undo`, `onDrop` (`data-drop-slot`), `fillInfo`, revisão (`evSet`, linha do tempo) em `index.html` ·
`scripts/smoke.py` (alguém do time vai para o gol; 🧤 ⇄ 🧤; goleiro foi embora → gol vazio → vaga →
rodízio entra; de fora direto para o gol; goleiro para a vaga; arraste sobre o 🧤) ·
`scripts/layout.py` ("partida com goleiro marcado para trocar") · [Fluxo do racha §3](../produto/fluxo-do-racha.md)
· [Regras do racha §3](../produto/regras-do-racha.md).

<a id="d-118"></a>
### D-118 · Elo de largada de todos os titulares; efeito no nível por papel
**04/09/2026.** Dois problemas vistos numa partida real (racha de 04/09): (1) a **chance no
apito sumiu** da Stats e do histórico — o goleiro titular foi substituído 6 s depois da largada,
o trecho foi descartado, e `applyMatch` só gravava o Elo "antes" (`m.pre`) de quem esteve em trecho
que conta; `chanceHist` (D-75) exige o Elo de largada dos cinco de cada lado, então devolvia vazio.
Agora `m.pre` é preenchido **antes** de aplicar os trechos, para toda a escalação de largada, no
papel em que cada um começou (goleiro do primeiro trecho pela patente de goleiro). (2) O **efeito no
nível** da revisão mostrava um número só por pessoa somando as duas patentes: o João Gabriel apareceu
com +18 "mais que todo mundo", quando eram +1 na linha (igual aos colegas naquele trecho) e +17 no
gol — patente nova, sem opinião e em calibração (K 64 contra K 32 dos que têm opinião). A partida
passou a guardar `m.papel[pid][L|G] = {pre, d}` e a revisão lista **uma linha por papel**, com o Δ e
o "antes → depois" daquela patente e a marca *no gol*. `m.deltas` continua sendo a soma (é o que
ordena). `papel` é derivado, como `pre`/`deltas`/`moves`: sai de `matchFacts` e não vai para o banco.
**Descartado:** mostrar a soma com um asterisco (esconde a informação que explica o número); pesar
a chance pelo tamanho dos lados e o mínimo de tempo para trecho com gol (regras do motor, fora do
escopo — passariam pela simulação de convergência, D-82).
**Onde:** `applyMatch` (`m.pre` dos titulares, `m.papel`), `matchFacts`, `revNivel` em `index.html` ·
`scripts/test.py` [17] · `scripts/smoke.py` (revisão: uma linha por papel, titular sem Elo de largada) ·
[Contestação e correção](../produto/contestacao-e-correcao.md).
