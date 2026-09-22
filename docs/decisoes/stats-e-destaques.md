# Decisões · Stats e destaques

> Destaques do mês, rankings, aproveitamento, +/-, duelos, filtros e o painel.
> Índice de todas as decisões e regra de registro em [README.md](README.md).

---

<a id="d-12"></a>
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
**Onde:** [Stats §3](../produto/stats.md) · [Regras do racha §6](../produto/regras-do-racha.md) · RF-08.8/8.8b/8.8c · `destaques`, `statsBlock` · teste `[13]`.

<a id="d-13"></a>
### D-13 · O critério do destaque é o saldo acima do esperado
**18/08/2026.** `Σ (resultado do trecho − chance daquele lado) × peso` — a mesma conta que move a
patente, sem o K, expressa em vitórias. Piso: **2 rachas e 20 partidas** no período.
**Por quê:** com times equilibrados o aproveitamento de todo mundo tende a 50%, e vitória pura premia
quem caiu no time bom. O saldo desconta a dificuldade do confronto: a zebra que vence leva +0,88, o
favorito que confirma leva +0,12. Soma zero dentro da partida, então ninguém infla o número só jogando.
**Descartado:** aproveitamento, vitórias, e média por partida (presença faz parte do mérito num racha).
**Exibição:** o pódio mostra **nome, partidas e % de vitórias** — o número do saldo fica fora da tela,
porque ordena bem e comunica mal (fica quase sempre perto de zero).
**Onde:** [Stats §3](../produto/stats.md) · [Regras do racha §6](../produto/regras-do-racha.md) · RF-08.9 · `destaques`, `m.over` · teste `[13]`.

<a id="d-14"></a>
### D-14 · Artilheiro só quando os gols têm dono
**18/08/2026.** Aparece se **metade ou mais** dos gols do período tiverem autor; senão o card diz
quantos ficaram sem dono.
**Por quê:** autor de gol é opcional de propósito. Ranking com metade dos gols órfãos premia quem
lembrou de se cadastrar, não quem fez gol.
**Onde:** [Stats §3](../produto/stats.md) · RF-08.10 · teste `[13]`.

<a id="d-15"></a>
### D-15 · Goleiro menos vazado = gols sofridos por partida, por trecho
**18/08/2026.** Conta só os trechos em que a pessoa estava no gol.
**Por quê:** goleiro que entrou no meio não pode levar gol que tomou antes de entrar; no rodízio é justo
porque ele alterna de lado a noite toda.
**Onde:** [Stats §3](../produto/stats.md) · RF-08.11 · teste `[13]`.

<a id="d-16b"></a>
### D-16b · O histórico é por racha, não por partida
**18/08/2026.** A aba Jogos lista **uma linha por racha** (data, partidas, gols, contestações, e a marca de
quantas foram suas). As partidas aparecem depois de tocar no racha, com contestar e revisar.
**Por quê:** um racha rende 10 a 15 partidas; a lista corrida virava um mural de placares sem contexto.
Ninguém procura "a partida de 2 a 1", procura "o racha de sábado".
**Onde:** [Fluxo do racha §3](../produto/fluxo-do-racha.md) · RF-07.1/7.1b/7.1c · `rachasDe`, `viewHist` · smoke.

<a id="d-43"></a>
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

<a id="d-51"></a>
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
`test.py` [11] ("sem goleiros") · `smoke.py` ("numeros sem goleiros") · [Stats §2](../produto/stats.md).

<a id="d-54"></a>
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
noite abrem ate 10") · [Stats §2](../produto/stats.md).

<a id="d-69"></a>
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
`pSheet`, folha do duelo em `index.html` · [Stats §3](../produto/stats.md)/5.4 (definição, piso, ordem) ·
RF-08.9, RF-11.1, RNF-04.9 · `test.py` (aprDe e o bloco novo do piso OU).

<a id="d-70"></a>
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
[Stats](../produto/stats.md) (parágrafo dos rankings) · RF-11.8 · `smoke.py` ("inverter um ranking pela setinha
e voltar", e `statsInv` na lista de ações livres).

<a id="d-72"></a>
### D-72 · "Quem mais perdeu" sai do card da noite — a setinha já conta essa história
**31/08/2026.** O card do último racha perdeu a seção "😵 Quem mais perdeu" (nascida no D-54): com
a setinha de ordem (D-70) em "🏆 Quem mais ganhou", a leitura espelhada está a um toque, e duas
listas quase iguais uma embaixo da outra só esticavam a tela da noite. Rigorosamente a inversão
mostra "menos vitórias" (entre quem venceu), não "mais derrotas" — mas na prática da noite é a
mesma conversa, e quem quiser o número exato de derrotas tem o V/E/D em cada linha e o "Mais
derrotas" nos rankings de temporada, que fica.
**Descartado:** tirar também o "Mais derrotas" da temporada (lá a lista é longa, o recorte por
derrotas absolutas é outra pergunta, e ninguém pediu).
**Onde:** `cardsUmRacha` em `index.html` · [Stats](../produto/stats.md) (lista dos cards da noite) · `smoke.py`
(o passo agora garante que a seção NÃO volta).

<a id="d-76"></a>
### D-76 · Partida a partida na tela do jogador — com a chance da época e uma bolinha por gol
**31/08/2026.** A aba Stats → Jogador ganhou o card **"Partida a partida"**: uma linha por jogo da
pessoa no período do filtro, da mais recente para a mais antiga — V/E/D colorido, data, placar
**pelo lado dela**, a **chance no apito** (a mesma conta do histórico, D-75: `m.pre` sobre a
escalação de largada, do lado em que ela jogou) e os gols como **uma bolinha ⚽ por gol** (🙈 por
gol contra, a pedido — número só quando passa de 8 bolinhas). A coluna de chance segue a regra de
sempre: some com as patentes fechadas (D-52) e vira — quando o `pre` não cobre a escalação.
**Ajuste no mesmo dia:** o rótulo virou **"% = prob. de vitória"** (o "no apito" saiu das linhas,
que mostram só o número) e o "8 linhas → ver até 40" virou **paginação** de 10 em 10 (‹ recentes ·
antigas ›, com "11–20 de 87"), que aguenta histórico de qualquer tamanho; a página zera ao trocar
o período ou a pessoa.
**Por quê:** o painel resumia o período mas não contava a história jogo a jogo — e com a chance da
época na linha, dá para ver de bate-olho quem venceu de zebra e quem só confirmou favoritismo.
**Descartado:** placar sempre na ordem dos times (pelo lado da pessoa é o que o leitor daquela
tela quer); listar também na ficha (pSheet) — a ficha é cadastro/correção, estatística mora em
Stats.
**Onde:** `pps`/`ppRow`/`cardPP` em `viewStats` (`index.html`) · [Stats](../produto/stats.md) (tabela do painel)
· `smoke.py` ("partida a partida na tela do jogador").

<a id="d-97"></a>
### D-97 · No card do último racha, o realizado conta empate como meio — a mesma base da chance
**02/09/2026.** A linha `50% V (esp. 62%)` de cada time (D-77) comparava vitórias puras com a
probabilidade de vitória do Elo. Só que a chance do Elo não tem empate: é o **placar esperado**, em
que empate vale meio ponto. Comparar com vitórias puras puxava o "real" para baixo em toda noite
com empates. Agora o realizado é `(V + E/2) / partidas`, rotulado `55% real (esp. 62%)` — as duas
grandezas na mesma base. (A D-77 tinha descartado outra coisa: corrigir a *expectativa* pela taxa de
empate da noite, que contaminava a régua com o resultado. Aqui muda só a conta do realizado.)
**Onde:** card do último racha em `viewStats` (`index.html`) · [Protótipo](../tecnico/prototipo.md) "Minutos e ritmo".

<a id="d-108"></a>
### D-108 · Stats com cara de painel: gráficos, posição nos rankings, barras e ícones SVG
**03/09/2026.** O pedido foi "mais cara de dashboard profissional e interessante de usar". A aba
já tinha os números certos, mas era uma pilha de listas iguais, com emoji nos títulos. Mudanças,
sem mexer no motor nem no que é contado:
- ~~**Racha a racha** (aba Jogador)~~ — gráfico de colunas V/E/D por racha. **Removido no mesmo
  dia**: ficou horrível na tela (colunas empilhadas de três cores num espaço de 12 rachas viram
  ruído). A "partida a partida" já conta essa história; o gráfico que fica é só o da liga.
- **Gols por racha** (aba Racha): coluna por racha, o último em verde, média do período tracejada.
- **Posição nos rankings** (aba Jogador): fichas roláveis "4º aproveit. · 1º vitórias…", pódio em
  dourado. Sem "de N" (tirado no mesmo dia): cada ranking lista só quem tem o número que ordena
  — 18 em vitórias, 13 em gols, 5 em sequência — e o N mudando de ficha em ficha confundia. Responde "onde eu estou" sem rolar até a aba Racha. Usa as mesmas listas e o
  mesmo empate de posição dos rankings (D-89).
- **Ritmo com a média da liga** ao lado (gols/10 min, sofridos/10 min ou gols por partida), verde
  quando melhor que a liga, vermelho quando pior. O número sozinho não dizia se era muito ou pouco.
- **Barra proporcional ao líder** em cada linha de ranking, e a linha da própria pessoa destacada
  (`.rk3.me`, que existia como classe mas não tinha CSS). Sem barra quando o topo é ≤ 0 (+/−).
- **Ícones SVG de traço** (`SICO`/`ic()`) no lugar dos emojis de seção (📅🏆😵📈⚡🧤🔥⭐📊😤😎🤝🔗),
  cada seção com a sua cor. O ⚽ fica, porque é a marca do gol no app (D-107).
- **Conserto:** "sofridos a cada 10 min" aparecia com 0 min no gol e dava 21052,63; agora só com
  1 min ou mais no gol.
**Descartado:** gráfico de nível (Elo) ao longo do tempo — o rating não é público (D-84/D-94);
biblioteca de gráficos — colunas em CSS puro bastam, seguem o tema e não pesam.
**Onde:** `viewStats` (`cardRR`, `posHtml`, `ratesHtml`, gráfico da liga), `rkBars`, CSS `.chart`,
`.posrow`, `.rates`, `.pbar`, `.ic` em `index.html` · `scripts/.tmp/shot_stats.py` fotografa a
aba com 10 rachas de demonstração · [Stats §2](../produto/stats.md). `smoke.py` cobre o toggle "Sem goleiros".

<a id="d-109"></a>
### D-109 · Gols por tempo só sobre minutos de linha; destaque nos rankings é o dono do perfil
**03/09/2026.** Duas correções na D-108, do mesmo dia. (1) A média da liga em "gols a cada
10 min" somava os minutos de quem estava no gol — no rodízio, todo mundo tem minutos de goleiro,
e ninguém marca de lá. A média saía baixa e a comparação enganava. Agora gols por tempo (o cartão
da pessoa, a média da liga e o ranking "Gols a cada 10 min") usam **tempo de linha** = tempo em
quadra − tempo no gol; com o chip "Sem goleiros" ligado o tempo já vem sem o gol. "Sofridos a
cada 10 min" já era só sobre tempo no gol, para a pessoa e para a liga — posição com posição.
**Ajuste no mesmo dia — linha e gol estanques.** O que a pessoa fez no gol não entra em nenhum
número de linha, nem o contrário, e cada função se compara só com a liga na mesma função:
"gols / 10 min" e "gols por partida" usam gols, minutos de linha e **partidas sem passar pelo gol**
(jogos − jogos em que esteve no gol), contra a liga na linha; "sofridos / 10 min" usa gols
sofridos e minutos no gol, contra a liga no gol (soma de todo mundo enquanto estava no gol,
ponderada pelo tempo). Piso de **20 min em cada função** (o mesmo do "Menos vazado" do racha):
3 min no gol de um jogador de linha não geram cartão; goleiro fixo sem tempo de linha não vê
cartão de linha. Um cartão só ocupa a largura toda. O rótulo é
"média da liga" nos três cartões (era "liga na linha" / "liga no gol"): a função já está no título
do cartão.
(2) Na aba Racha, a linha destacada em verde era a do jogador **selecionado** na aba Jogador
("Trocar"); virou a do **dono do perfil** neste aparelho. Ver os números de outra pessoa não faz
dela "você" no ranking.
**Onde:** `minL`, `rkRitmo`, `ratesHtml` e `rkBars` em `viewStats` · [Stats §2](../produto/stats.md).

<a id="d-112"></a>
### D-112 · Rankings: top 3 limpo na página, lista inteira e ordem numa folha
**03/09/2026.** "Os rankings todos estão muito feios: a barra é redundante, o botão de expandir e
reduzir está confuso." Concordo com os três pontos. O que mudou:
- **Sem barra proporcional** (D-108): o número já diz a proporção; a barra só engordava a linha.
- **Sem setinha ↓/↑ no cabeçalho** e sem "▾ ver até 10 / ▴ menos" abrindo dentro da página.
  Cada ranking mostra o **top 3** (posição, nome, número) e um botão **"Ver os 10 ›"** (ou "Ver
  todos os N ›"). Ele abre uma **folha** com a lista inteira (até 10, cada linha com o detalhe que
  antes só aparecia expandido) e um seletor **"Do 1º ao último / Do último ao 1º"** — a leitura
  invertida continua existindo (quem mais perdeu = "quem mais ganhou" lido do fim, D-72), mas
  como escolha explícita dentro da folha, não como um botão misterioso ao lado do título.
- **Duelos e parcerias** seguem o mesmo padrão: 5 na página, "Ver todos os 18 ›" abre a folha
  (ordem "Mais confrontos / Menos confrontos").
- Um `rkSec` monta toda seção (temporada e último racha) — antes eram três geradores diferentes
  (`rkBars`, `corta`+`mais`, `listaDuelo`) com pequenas divergências.
**Ajustes no mesmo dia:** o "Ver os 10 ›" foi para a **linha do título** do ranking — solto embaixo
da lista, não se sabia de qual ranking ele era; a folha **sempre abre "Do 1º ao último"** e a
inversão vale só naquela abertura (a preferência por aparelho, herdada da setinha, deixava a
folha abrir invertida sem a pessoa lembrar por quê); e **Gol contra** no último racha virou
ranking de verdade — antes repetia o nome a cada gol e saía sem número.
**Descartado:** manter o expandir na página com texto melhor — dez rankings × 10 linhas ainda vira
um rolo; a folha isola o que a pessoa quer olhar.
**Onde:** `RK`, `rkRowHtml`, `rkSec`, `duelList`, `A.rkSheet`, `A.rkInv` em `index.html` ·
`smoke.py` ("abrir a folha de um ranking e inverter a ordem") · [Stats §2](../produto/stats.md).

<a id="d-114"></a>
### D-114 · Filtros da Stats: uma família só, sem card
**03/09/2026.** "O design dos filtros ainda me incomoda." Eram três controles de três estilos
dentro de um card: um seletor segmentado (Jogador/Racha), uma fileira de chips soltos (período)
e um chip largo sozinho numa linha ("Sem goleiros"). Agora: **dois seletores segmentados
empilhados** — modo e período, no mesmo desenho — e **"Sem goleiros" como interruptor** pequeno,
alinhado à direita, texto apagado quando desligado e verde quando ligado. Sem card em volta:
os seletores já têm fundo próprio, e o card só somava borda e respiro. O aviso "ninguém assumiu
um perfil" fica logo abaixo, em texto pequeno. Ganho: ~40 px de altura e um só vocabulário.
**Descartado:** período como abas de texto sublinhado (parecia navegação, não filtro); "Sem
goleiros" dentro do seletor de período (não é período).
**Onde:** `seg` em `viewStats`, CSS `.sfilt`/`.gksw` em `index.html` (`.sw` já existia, com outro
uso — daí o nome) · [Stats §2](../produto/stats.md).

<a id="d-134"></a>
### D-134 · Derrota não é ranking
**08/09/2026.** Sai o **Mais derrotas** dos rankings de temporada — o último herdeiro do D-54. O
"quem mais perdeu" do último racha já tinha saído no D-72; agora vai o irmão, e a lista de
rankings perde uma seção em todos os filtros.
**Por quê:** quem quer ler derrota inverte o "Mais vitórias" na folha (D-112) — a informação já
está lá. Um pódio de pior é número que ninguém pediu e que ocupa rolagem no celular.
**Descartado:** manter só no filtro "Sempre" (a mesma seção aparecendo e sumindo conforme o
filtro é pior que não existir).
**Onde:** `rkDer`, `SECS.der` e `ordem` em `viewStats` · `smoke.py` ("rankings do último racha
abrem ate 10, sem quem-mais-perdeu") · [Stats §2](../produto/stats.md).

<a id="d-135"></a>
### D-135 · Na aba Jogador, linha e gol são duas leituras — não um interruptor
**08/09/2026.** O **"Sem goleiros" saiu da aba Jogador**: lá ele não fazia sentido — um
interruptor que zerava a ficha do goleiro fixo (12 partidas viravam 0) e que, no meio do caminho,
somava as duas funções de quem reveza. No lugar entra um seletor **Linha | Gol**, que aparece só
para quem pegou no gol no período (pela função do trecho, não por minutos — partida antiga sem
cronômetro tem trecho de duração zero). Ele troca a leitura inteira: partidas, V/E/D,
aproveitamento, sequência, minutos, ano a ano, partida a partida (mesma régua e mesmo lado que o
tile de partidas), cartões de ritmo, a posição nos rankings — calculada **dentro da função** (3º
entre goleiros, não 3º entre todo mundo) — e a folha de cada duelo/parceria, que lê a mesma
função da ficha. Na leitura do gol os tiles viram "gols do gol" e "min no gol", e duelo e parceria
somem: o goleiro do rodízio troca de lado sem escolher com quem joga. Na leitura de linha, o
goleiro dos outros **continua** nas parcerias e nos duelos da pessoa — o filtro é da função
DELA; tirar o goleiro dos outros é coisa do interruptor da aba Racha. A ficha abre na função em
que a pessoa mais jogou no período; a escolha é guardada **com o id da pessoa**, então não vaza
para o próximo perfil, para outra liga nem para o fallback de "quem sou eu". O interruptor "Sem
goleiros" continua, intacto, na aba Racha — lá ele é dos rankings (D-51) — e a passada extra
por função só roda na aba Jogador.
`statsLiga(liga, per, papel)` passou a receber `'L'`/`'G'` (e `true` segue valendo por `'L'` +
goleiro fora das parcerias dos outros), `statsAnos` e `encontros` também; `pegouNoGol` e
`papelJogador` decidem a função; as listas de ranking saíram de dentro do `viewStats` para
`listasRk(J, PA, minL)` — a mesma função serve os rankings da aba Racha e a posição da pessoa.
**Por quê:** o que a pessoa faz de linha e o que faz no gol são duas histórias; somadas, não
descrevem nenhuma das duas, e um interruptor global escondia isso atrás de um estado que se
esquece ligado.
**Descartado:** manter o interruptor nas duas abas (o goleiro fixo lia a própria ficha zerada);
uma terceira opção "Tudo" (é a soma que não descreve ninguém); decidir "pegou no gol" por minutos
(zerava quem só tem partida antiga no gol).
**Onde:** `statsLiga`/`statsAnos`/`encontros` (parâmetro `papel`), `pegouNoGol`, `papelJogador`,
`listasRk`, `viewStats` (seletor `.seg.fn`, `naFicha`, `stP`, `RP`, tiles, cartões, posições,
partida a partida), `A.statsPapel`, `A.duelo` · `smoke.py` ("aba Jogador: quem ja pegou no gol
escolhe entre Linha e Gol (D-135)", "numeros sem goleiros… so na aba Racha") ·
[Stats §2](../produto/stats.md).

<a id="d-142"></a>
### D-142 · Os destaques de um racha existem para qualquer racha, não só o último
**Quando:** 2026-09-14.
**O quê:** o período "Último" da aba Stats ganha setas **‹ ›** no cabeçalho do card do racha, que
andam entre os rachas da liga (do mais novo ao mais velho); o racha escolhido fica em
`ui.statsRacha` e o botão do período mostra a data dele (tocar de novo volta ao mais novo). Na aba
Jogos, o racha aberto ganha **Destaques do racha ›**, que leva a essa leitura. Nada de cálculo novo:
`noPeriodo` já aceitava `racha:<id>` de qualquer racha; faltava um jeito de escolher.
**Por quê:** "Rendeu acima do esperado" e os outros rankings da noite só saíam para o último
racha; no domingo seguinte a leitura do sábado anterior sumia sem nunca ter sido vista por quem
não abriu o app no dia.
**Descartado:** lista de rachas dentro do seletor de período (não cabe na linha do celular);
repetir os rankings dentro da aba Jogos (duas telas com a mesma conta).
**Onde:** `idsRachas`, `statsPeriodo`, `viewStats` (botão do período, setas no card), `viewHist`
(botão Destaques), `A.statsRacha`, `A.statsPer` em `index.html` · `smoke.py` ("numeros: as setas
andam para o racha anterior…") · [Stats §2](../produto/stats.md).

<a id="d-143"></a>
### D-143 · "Rendeu acima do esperado" é ranking de todo período, não só do racha
**Quando:** 2026-09-14.
**O quê:** o saldo acima do esperado (D-13) entra em `statsLiga` (`J[pid].over`, somado de
`m.over`) e em `listasRk` (`over`, mín. `MIN_JOGOS` partidas, como o aproveitamento). Na aba
Racha ele aparece nos rankings de 30 dias, ano e Sempre, logo depois de "Maior aproveitamento"
(em 30 dias, logo depois dele no topo); na aba Jogador entra em "Posição nos rankings" como
"acima do esp.". Só com as patentes abertas — a conta nasce do nível de quem estava em quadra.
O saldo é da pessoa, não da função: sai igual nas leituras de linha e de gol.
**Por quê:** o ranking existia no último racha e no destaque do mês, mas quem queria saber quem
rende acima do nível na temporada ou na carreira não tinha onde olhar.
**Descartado:** piso próprio menor que o do aproveitamento (dois pisos na mesma tela confundem);
separar o saldo por função (o Δ de Elo já é por função; o saldo acima do esperado é do resultado da
pessoa em quadra).
**Onde:** `statsLiga`, `listasRk`, `viewStats` (`SECS.over`, `ordem`, `posicoes`) em `index.html` ·
`smoke.py` · [Stats §2](../produto/stats.md).

<a id="d-144"></a>
### D-144 · A linha de "Quem mais rendeu" mostra o saldo que a ordena
**Quando:** 2026-09-14.
**O quê:** em Destaques (aba Racha, 30 dias), cada linha de "Quem mais rendeu além do esperado"
ganha à direita o saldo acima do esperado (+1,5; com as patentes fechadas, as vitórias).
`linhaDestaque` recebe um `val` opcional.
**Por quê:** a lista já era ordenada pelo saldo, mas a linha só dizia rachas, partidas e
aproveitamento — e o aproveitamento não acompanha o saldo, então a ordem parecia errada.
**Onde:** `linhaDestaque`, `statsBlock` em `index.html` · [Stats §3](../produto/stats.md).

<a id="d-145"></a>
### D-145 · Rankings de temporada são taxas, com piso de metade dos rachas
**Quando:** 2026-09-14.
**O quê:** na aba Racha (30 dias, ano, Sempre) todo ranking vira estatística de longo prazo:
aproveitamento, rendeu acima do esperado **por partida** (pontos % de vitória real − esperada),
**+/− a cada 10 min**, gols a cada 10 min de linha, maior sequência, **tempo em quadra por racha**,
menos vazado e **gols de goleiro a cada 10 min no gol**, melhor dupla. Saem **Artilharia** (total de
gols) e **Mais vitórias**. A exceção é **Mais presenças**: presença é o próprio volume. Piso único:
**ter jogado metade dos rachas do período** (`minR = ceil(rachas/2)`, escrito em cada título como
"mín. N de M rachas"); as taxas por tempo pedem ainda 1 h na função (`MIN_RITMO`). `listasRk`
recebe `minR`; `pm10` e `overPct` são as taxas; a posição da pessoa na ficha usa as mesmas.
**Por quê:** total premia quem aparece mais, não quem joga melhor; num período longo a artilharia
era só a lista de presença com outro nome. Taxa com piso de metade dos rachas compara gente que
esteve lá de verdade.
**Descartado:** piso fixo em partidas (10 partidas é muito em 30 dias e pouco em "Sempre");
manter os totais ao lado das taxas (dois rankings da mesma coisa).
**Onde:** `listasRk`, `pm10`, `overPct`, `viewStats` (`minR`, `minTxt`, `SECS`, `ordem`,
`posicoes`) em `index.html` · `smoke.py` · [Stats §2 e §4](../produto/stats.md).

<a id="d-146"></a>
### D-146 · "Os melhores do racha" ordena por divisão e, dentro dela, por Elo
**Quando:** 2026-09-14.
**O quê:** a lista dos destaques dos 30 dias passa a ordenar por divisão e depois por Elo (antes,
por aproveitamento dentro da divisão, para não denunciar o rating).
**Por quê:** quem vê os Elos — o admin — via a ordem "errada". A divisão já é o que aparece no
badge; a ordem por Elo dentro dela só ordena, não mostra o número.
**Onde:** `destaques` (`melhores`) em `index.html` · [Stats §3](../produto/stats.md).

<a id="d-147"></a>
### D-147 · "Quem mais rendeu" nos Destaques também é por partida
**Quando:** 2026-09-14.
**O quê:** a lista dos destaques dos 30 dias ordena e mostra a **% de vitória real − esperada por
partida** (`overPct`), como o ranking de temporada (D-145), em vez do saldo somado (D-144).
**Por quê:** o saldo somado cresce com o volume; a % por partida compara quem jogou 8 e quem jogou
30 partidas no mês. Uma leitura só em todas as telas.
**Onde:** `destaques` (`top`), `statsBlock` em `index.html` · [Stats §3](../produto/stats.md).

<a id="d-148"></a>
### D-148 · Tempo em quadra é volume, como presença: total, sem piso
**Quando:** 2026-09-14.
**O quê:** "Tempo em quadra por racha" (D-145) volta a ser **Mais tempo em quadra**, total, sem o
piso de metade dos rachas — a mesma exceção da presença. A linha continua dizendo "N min por racha".
**Por quê:** tempo em quadra mede o mesmo que presença (quanto a pessoa esteve lá); dividir por
racha só premiava quem veio pouco e ficou o tempo todo.
**Onde:** `listasRk` (`min`), `viewStats` (`SECS.min`, `posicoes`) em `index.html` ·
[Stats §2](../produto/stats.md).

<a id="d-149"></a>
### D-149 · Período por mês e por ano, com setas; a história no passo abaixo do período
**Quando:** 2026-09-14.
**O quê:** o filtro da aba Stats vira `Último · Mês · Ano · Sempre`. "30 dias" (janela móvel) vira
**Mês** (calendário) e a lista de anos vira **Ano**; os três abrem no atual e uma linha
**‹ … ›** abaixo do filtro anda para o anterior/seguinte (racha, mês ou ano — as setas do card
do racha, D-142, subiram para cá). O botão mostra o escolhido (12/09, ago/26, 2025) e, tocado de
novo, volta ao atual. Estado: `ui.statsPer` (tipo) + `ui.statsRacha`/`statsMes`/`statsAno`;
`statsPeriodo` devolve `'mes:AAAA-MM'`, o ano, `'racha:<id>'` ou `'sempre'`, e `noPeriodo` lê.
Gráficos (`grafBarras`): na aba Racha, por mês (no ano; meses vazios como zero até hoje) e por
ano (em Sempre) — rachas, partidas, gols por partida; no mês continua o gols por racha. Na aba
Jogador, `statsGrupos` (generaliza `statsAnos`) quebra o período no passo abaixo dele — racha a
racha, mês a mês, ano a ano — com gráfico de aproveitamento (e partidas) e uma linha por grupo.
`rotPer` dá o rótulo do período em qualquer tela.
**Por quê:** "últimos 30 dias" não é o mês que as pessoas falam ("como foi agosto?") e a lista de
anos só crescia; escolher mês e ano com setas é o mesmo gesto do racha. E cada período pede a
sua curva: o mês em rachas, o ano em meses, a vida em anos.
**Descartado:** lista de meses no seletor (não cabe); manter os 30 dias ao lado do mês (dois
nomes para a mesma pergunta). Os destaques da tela do racha continuam em 30 dias móveis: lá não
há seletor, e o começo do mês ficaria vazio.
**Onde:** `MES_KEY`, `MESES`, `mesLabel`, `chavesPer`, `tipoPer`, `rotPer`, `statsPeriodo`,
`noPeriodo`, `statsGrupos`, `statsAnos`, `grafBarras`, `viewStats` (`navPer`, `labMes`,
`labAno`, gráficos da liga, `grupos`), `A.statsPer`/`statsMes`/`statsAno`, `A.duelo` em
`index.html` · `smoke.py` ("periodo por mes e por ano…") · [Stats §2](../produto/stats.md).

<a id="d-150"></a>
### D-150 · Momento: gols em barra, % acima do esperado em linha, ao longo do tempo
**Quando:** 2026-09-14.
**O quê:** na aba Jogador, o bloco racha a racha / mês a mês / ano a ano (D-149) ganha o gráfico
**Momento** (`grafMomento`): uma coluna por grupo com a barra dos **gols** e, por cima, a **linha
da % de vitória real − esperada por partida** (`overPct`, D-145), com o zero tracejado no meio
("jogou o que o nível dizia") e escala simétrica (o pior e o melhor mês têm o mesmo tamanho). O
valor da linha fica em cima de cada coluna, verde ou vermelho. `statsGrupos` passa a somar
`m.over` da pessoa no grupo. Substitui os dois gráficos de barras de D-149 (aproveitamento e
partidas): a linha por grupo já traz o aproveitamento. Com as patentes fechadas não há esperado,
e fica o gráfico de aproveitamento. No "Último" não há gráfico.
**Por quê:** "estou em fase?" é uma pergunta sobre tendência, não sobre um número; gols dizem o que
a pessoa produziu e a linha diz se rendeu acima do nível — juntos, numa tela, contam o mês.
**Descartado:** linha do aproveitamento (não desconta o time que a pessoa pegou); duas escalas
com eixos numéricos (não cabe no celular — os valores vão em cima das colunas).
**Onde:** `grafMomento`, `statsGrupos` (`over`), CSS `.chart.momento`, `viewStats` (bloco dos
grupos) em `index.html` · `smoke.py` (D-149) · `visual.py` (tela 18 "momento") ·
[Stats §2](../produto/stats.md).

<a id="d-151"></a>
### D-151 · Momento sem as barras de gol: só a linha
**Quando:** 2026-09-14.
**O quê:** o gráfico Momento (D-150) perde as barras de gols; fica a linha da % de vitória real −
esperada sobre o zero tracejado, com o valor em cima de cada coluna. Os gols continuam na linha
de cada grupo, logo abaixo.
**Por quê:** duas medidas numa coluna só (altura da barra e ponto da linha) confundiam a leitura.
**Onde:** `grafMomento`, CSS `.chart.momento` em `index.html` · [Stats §2](../produto/stats.md).

<a id="d-152"></a>
### D-152 · Momento: valor no ponto, área pintada, aproveitamento embaixo do eixo
**Quando:** 2026-09-14.
**O quê:** o valor da % fica colado ao ponto (acima se positivo, abaixo se negativo), a área entre
a linha e o zero é pintada (verde acima, vermelha abaixo, `clipPath` no SVG), ponto maior no
grupo atual, e o **aproveitamento** de cada grupo aparece em cinza pequeno embaixo do rótulo do
eixo (`opts.sub`).
**Por quê:** o valor no topo da coluna ficava longe do ponto; a área dá de relance quanto tempo
a pessoa passou acima ou abaixo do nível. Aproveitamento como segunda linha foi descartado: 0–100
com 50 no meio e −x…+x com zero no meio são duas escalas, e duas linhas no mesmo desenho
confundem — embaixo do eixo ele fica à mão sem competir.
**Onde:** `grafMomento`, CSS `.chart.momento`, `.chartx span small` em `index.html` ·
[Stats §2](../produto/stats.md).

<a id="d-153"></a>
### D-153 · Painel da liga em Mês/Ano/Sempre: o destaque de cada grupo, os níveis, tudo com toque
**Quando:** 2026-09-14.
**O quê:** dois cards novos na aba Racha fora do "Último". **Racha a racha / Mês a mês / Ano a
ano** (`cardGrupos`): uma linha por grupo do período com partidas, gols e chips — quem rendeu
acima do esperado (`statsLiga` do grupo, `overPct`, piso 3 partidas num racha e metade dos rachas
num mês/ano), artilheiro, ▲/▼ mudanças de nível — e a linha é um botão que abre o período
(`statsRacha`/`statsMes`/`statsAno`). **Níveis** (`cardNiveis`, só com `vePat`): faixa
proporcional das patentes de hoje entre quem apareceu (`.patbar`, toque → `irEscada`), tiles
subiram/caíram/no mesmo nível e rankings "Quem mais subiu"/"Quem mais caiu" a partir de
`m.moves` do período, com badges de → para. A dica dos rankings sai da linha do título e vai
para uma linha própria (no celular não cabia). Tela 19 no `visual.py`.
**Por quê:** em Mês, Ano e Sempre o painel era só tiles e rankings; faltava a história (o que
aconteceu em cada racha do mês, em cada mês do ano), faltava a escada (o app é sobre nível e o
painel não falava dela) e faltava por onde entrar — cada linha agora leva ao período.
**Descartado:** repetir os rankings inteiros por grupo (a linha com três chips diz o que importa,
o resto está a um toque); "Quem mais caiu" sem nomes (o resumo do racha já mostra quem caiu,
D-99).
**Onde:** `cardGrupos`, `cardNiveis`, `rkSec` (dica), `A.irEscada`, CSS `.grow`, `.chip`,
`.patbar`, `.patleg` em `index.html` · `smoke.py` (D-149) · `visual.py` (tela 19) ·
[Stats §2](../produto/stats.md).

<a id="d-154"></a>
### D-154 · Gols por racha no painel; média no título do gráfico; faixa de patentes limpa
**Quando:** 2026-09-14.
**O quê:** o gráfico da liga por mês/ano passa de "Gols por partida" para **Gols por racha**
(gols ÷ rachas do grupo). Em todo gráfico de colunas a **média** sai da linha tracejada e vai
para o título ("por ano · média 7,5"): o rótulo em cima da linha colidia com o valor da última
coluna. Na faixa de patentes, a legenda perde a contagem (o número já está no trecho), cada
trecho ganha largura mínima e uma borda leve (no escuro, Ferro sumia no fundo).
**Por quê:** revisão a olho dos prints (telas 19 e 8 do `visual.py`, 360 e 500 px, claro e
escuro) depois de D-153.
**Onde:** `grafBarras`, gráfico "Gols por racha" do mês, `cardNiveis`, CSS `.patbar i` em
`index.html` · `smoke.py` (D-149) · [Stats §2](../produto/stats.md).

<a id="d-156"></a>
### D-156 · A faixa de níveis conta o goleiro pela patente de goleiro
**Quando:** 2026-09-14.
**O quê:** no card Níveis (D-153), cada pessoa entra pela patente da função em que mais jogou no
período (tempo no gol × tempo de linha); se não tem patente nessa função, vale a outra.
**Por quê:** contava só a patente de linha — 14 presentes com nível viravam "12 com nível",
porque os dois goleiros fixos só têm a de goleiro.
**Onde:** `cardNiveis` em `index.html` · [Stats §2](../produto/stats.md).

<a id="d-157"></a>
### D-157 · A média dos gráficos por mês ignora os meses sem racha
**Quando:** 2026-09-14.
**O quê:** `grafBarras` aceita `opts.vazio(item)`; os itens vazios continuam no gráfico (o
buraco é informação) mas não entram na média. Os três gráficos por mês do Ano marcam como vazio
o mês sem racha.
**Por quê:** "média 1,5 rachas por mês" com quatro meses sem racha não descreve o racha — a
média é de quando houve racha.
**Onde:** `grafBarras`, gráficos por mês em `viewStats` em `index.html` ·
[Stats §2](../produto/stats.md).

<a id="d-158"></a>
### D-158 · Sem os gráficos de colunas por mês e por ano no painel da liga
**Quando:** 2026-09-14.
**O quê:** saem os três gráficos (rachas, partidas, gols por racha) por mês no Ano e por ano em
Sempre (D-149/D-154/D-157). Fica o "Gols por racha" do Mês. `grafBarras` continua (ficha com as
patentes fechadas).
**Por quê:** o mês a mês / ano a ano (D-153) já diz rachas, partidas e gols de cada grupo, com
o destaque e o toque que abre — três gráficos em cima disso era repetição.
**Onde:** `viewStats` (card "O racha …") em `index.html` · `smoke.py` · [Stats §2](../produto/stats.md).

<a id="d-159"></a>
### D-159 · Empate: primeiro o de maior patente; no chip, o nome e um "+N"
**Quando:** 2026-09-14.
**O quê:** `patDe(liga, x)` dá a patente de uma linha de estatística (a da função em que a
pessoa mais jogou no período; o Elo só desempata dentro da divisão). Toda lista de `listasRk`
usa isso como primeiro desempate, depois dos critérios de sempre; a posição continua dividida
(D-89). "Rendeu acima do esperado" empata pelo % mostrado (arredondado), não pela fração. Nos
chips do racha a racha / mês a mês / ano a ano (D-153), o empate mostra o de maior patente e
um **+N** com quantos empataram.
**Por quê:** empate escondido atrás de um nome só parecia escolha do app; e o desempate por
vitórias ou partidas premiava volume, não nível.
**Descartado:** listar todos os nomes empatados no chip (não cabe); desempatar por Elo entre
divisões (o número que ninguém vê decidindo o que todo mundo vê).
**Onde:** `patDe`, `listasRk`, `cardGrupos` (`topo`, `mais`) em `index.html` · `test.py`
([19]) · [Stats §2 e §4](../produto/stats.md).

<a id="d-160"></a>
### D-160 · Sem o interruptor "Sem goleiros"
**Quando:** 2026-09-14.
**O quê:** o interruptor da aba Racha (D-51) sai da tela, do estado (`ui.statsSemGk`) e do
despachante. `statsLiga(liga, per, true)` continua existindo no motor, sem uso na interface.
**Por quê:** ele nasceu para tirar o tempo no gol dos totais de time (o goleiro joga mais).
Com os rankings em taxa (D-145) sobrou pouco para ele fazer — e ele fazia mal: ao tirar as
partidas no gol, o goleiro fixo ficava com zero rachas e caía fora do piso dos rankings *de
goleiro* (menos vazado, gols de goleiro), que nunca deveriam ser filtrados. Dois caminhos
foram considerados: prender o interruptor aos poucos rankings de volume (presença, tempo em
quadra) ou tirá-lo; tirar é mais simples e esses dois já contam o goleiro de propósito (D-148).
**Onde:** `viewStats` (seletor), `A.statsSemGk` (removido), CSS `.gksw` (removido) em
`index.html` · `smoke.py` · [Stats §2](../produto/stats.md).

<a id="d-161"></a>
### D-161 · A seta do racha não troca de sub-aba
**Quando:** 2026-09-14.
**O quê:** `A.statsRacha` só muda a sub-aba (Jogador/Racha) quando o botão traz `data-tab` — o
"Destaques do racha ›" da aba Jogos. As setas ‹ › ficam onde a pessoa está.
**Por quê:** na ficha do jogador, trocar o racha jogava a pessoa para o painel da liga.
**Onde:** `A.statsRacha`, botão em `viewHist` em `index.html` · `smoke.py` (D-142) ·
[Stats §2](../produto/stats.md).

<a id="d-188"></a>
### D-188 · A aba Jogador de Stats fala do nível: hoje, melhor ou calibrando, e o que andou no período
**Quando:** 2026-09-15.
**O quê:** o card da pessoa ganha, depois das posições nos rankings, a seção **Nível na linha / no gol**
(a função que se está lendo, D-135): o título diz quantas divisões o nível andou no período ("▲ 2
divisões no período" / "sem mudança no período") e embaixo a **linha do tempo** (`linhaNivel`): quatro
marcos em ordem de data sobre um trilho — Entrada (Início fora de Sempre), Mínimo, Máximo, Hoje (Fim
num período fechado) — cada um com o ponto na cor da patente, o badge e a data. Mínimo e máximo são
o primeiro momento em que chegou lá; marcos no mesmo ponto se juntam num nó ("Entrada · Mínimo"),
e as pontas nunca se juntam. O nível em cada instante sai de `nivelApos` (o "de onde" da primeira
mudança registrada depois dele; sem mudança, o de hoje), a mesma régua da D-155. O racha a racha / mês a mês / ano a ano mostra o mini-badge do nível
no fim de cada grupo (▲/▼ quando mudou dentro dele; `statsGrupos` passou a guardar `fim`; a linha do grupo é uma grade de colunas fixas —
rótulo, nível, números, % — para o nível ficar alinhado). O
partida a partida **não** marca a mudança (entrou e saiu no mesmo dia: "isso pode ser invisível" —
o gráfico já conta).
Tudo some com as patentes fechadas.
**Por quê:** "a página de stats do jogador não fala nada sobre o nível dele" — o badge do cabeçalho
era a única menção, e o nível é o coração do produto. O período já quebrava a história em rachas e
meses; faltava dizer o que o nível fez nela.
**Descartado (três versões no mesmo dia):** dois cartões de "nível hoje" e "divisões no período" ao
lado dos de ritmo (o badge grande ficou pesado e desalinhado, e o nível de hoje já está no
cabeçalho); o **gráfico da trajetória** (escada no y com um badge por patente, tempo no x, linha em
degraus na cor da patente) — ficou bonito, mas pesado para o que diz: "em vez do gráfico, a
entrada, o máximo, o mínimo e o atual numa linha do tempo"; mostrar a distância para o próximo corte ou o Elo (§1 de patentes: o número não
existe para o jogador); repetir o bloco na aba Racha.
**Onde:** `nivelHtml`, linhas dos grupos em `viewStats`; `linhaNivel`, `nivelApos`, `statsGrupos` em
`index.html` · `scripts/smoke.py` (passo "D-188") · [Stats §2](../produto/stats.md).

<a id="d-190"></a>
### D-190 · Momento sem o aproveitamento embaixo do eixo; resumo do grupo sem minutos
**Quando:** 2026-09-15.
**O quê:** o gráfico Momento (aba Jogador) deixa de escrever o aproveitamento do grupo em cinza
embaixo de cada rótulo do eixo, e a legenda "aproveitamento embaixo" some com ele — o aproveitamento
fica só na linha do resumo (racha a racha / mês a mês / ano a ano), à direita, onde já estava. Essa
linha perde os minutos ("1 racha · 4 partidas · 2 gols").
**Por quê:** "o aproveitamento no gráfico de momento está meio confuso": eram duas escalas no mesmo
desenho (D-152), e o leitor lia o % embaixo como se fosse o ponto de cima. Minutos no resumo eram
número a mais numa linha que já diz partidas e gols.
**Descartado:** manter o % embaixo só quando o eixo tem poucos rótulos.
**Onde:** chamada de `grafMomento` e linhas dos grupos em `viewStats` (`index.html`) ·
[Stats §2](../produto/stats.md).

<a id="d-191"></a>
### D-191 · Linha do tempo só em Ano e Sempre, sempre com quatro marcos; sem os títulos "Nível na linha" e "Mês a mês"
**Quando:** 2026-09-15.
**O quê:** a linha do tempo do nível (D-188) só aparece nos períodos **Ano** e **Sempre**, e mostra
**sempre quatro nós**, mesmo que repitam o badge: Início/Entrada na ponta esquerda, Hoje/Fim na
direita, e Mínimo e Máximo no meio na ordem em que aconteceram (a versão anterior juntava marcos
iguais num nó só). Saem dois títulos: "Nível na linha / no gol" em cima da linha do tempo (fica só a
nota "▲ 2 divisões no período") e "Mês a mês / Racha a racha / Ano a ano" em cima do gráfico
Momento (o próprio título "Momento por mês" já diz o passo).
**Por quê:** "não será melhor sempre mostrar 4 badges mesmo que sejam os mesmos, início no começo e
hoje no final, com mínimo e máximo variando conforme o que aconteceu primeiro?" — com nós que se
juntam, a mesma ficha mudava de forma de um mês para o outro; quatro fixos se leem de relance.
"Dentro do mês tem muito pouca data": num mês o nível quase não anda, e quatro badges iguais não
dizem nada. Os dois títulos eram óbvios e, um em cima do outro com o Momento, confundiam.
**Descartado:** manter os títulos com fonte menor; mostrar a linha no mês só quando houve mudança.
**Onde:** `linhaNivel`, `nivelHtml` e o bloco dos grupos em `viewStats` (`index.html`) ·
`scripts/smoke.py` (passos "D-185" e "D-188") · [Stats §2](../produto/stats.md).

<a id="d-192"></a>
### D-192 · Com um período só, a linha ‹ 2026 › fica, com as setas apagadas
**Quando:** 2026-09-15.
**O quê:** a linha do período abaixo do filtro (‹ racha › / ‹ mês › / ‹ ano ›, D-149) passa a aparecer
mesmo quando só existe um período daquele tipo — só some quando não há nenhum. As duas setas ficam
apagadas (`disabled`) até haver outro racha, mês ou ano para onde ir.
**Por quê:** "em ano, só tem 2026 por enquanto: em vez de não mostrar o ano, mostre, sem a opção de
mudar" — sem a linha, a aba não dizia qual ano estava aberto.
**Descartado:** mostrar só o nome sem as setas (a linha mudaria de forma quando chegasse o segundo).
**Onde:** `navPer` em `viewStats` (`index.html`) · `scripts/smoke.py` (passo "D-149") ·
[Stats §2](../produto/stats.md).

<a id="d-193"></a>
### D-193 · Taxas por tempo em "por hora", com uma casa decimal
**Quando:** 2026-09-15.
**O quê:** toda taxa por tempo passa de "a cada 10 min" (duas casas) para **por hora** (uma casa):
gols por hora e sofridos por hora nos cartões de ritmo e na média da liga, os rankings Gols por
hora, Menos vazado ("sofridos por hora"), Gols de goleiro por hora e +/− por hora, a linha da ficha
do jogador e o "Menos vazado" do racha ("3,1/h"). `por10` virou `porHora`, `pm10` virou `pmHora`.
Ordem dos rankings e pisos (1 h na função) não mudam: é a mesma razão em outra unidade.
**Por quê:** "os números de gols a cada 10 minutos estão todos ficando entre 0 e 1" — 0,39 contra
0,31 ninguém compara; 2,3 contra 1,8 se lê de relance. Na quadra a pessoa joga 40 a 60 min por
racha, então gols por hora fica perto de "gols por noite", que é como todo mundo já pensa; e a
unidade passa a bater com o piso de 1 hora dos rankings.
**Descartado:** gols por partida como taxa única (partidas têm durações diferentes, D-109);
manter duas casas por hora (precisão que o dado não tem).
**Onde:** `porHora`, `pmHora`, `listasRk`, cartões de ritmo e rankings em `viewStats`, ficha em
`A.pSheet` (`index.html`) · `scripts/smoke.py` · [Stats §2](../produto/stats.md).

<a id="d-201"></a>
### D-201 · Corrigir os times do racha
**Quando:** 2026-09-20.
**O quê:** a folha de um time do racha (Stats → Times do racha → toque no time) ganha, para o admin,
**"Corrigir os times do racha"**. Abre a montagem gravada na sessão (`sess.teams`, `sess.gkPool`):
um bloco por time, o rodízio de goleiros e quem esteve no racha sem time (presença da sessão e quem
aparece nas partidas dela), mais "+ alguém do cadastro". Toque num nome → "Era de que time?" com um
botão por time, Rodízio de goleiros e Não era de time nenhum. Cada toque vale na hora (`sessSet`),
tira a pessoa de onde estava, registra `sessTeams` (quem, de onde, para onde) e sincroniza a sessão.
**Por quê:** a montagem gravada é o que as stats chamam de "time do racha" — o rótulo pelos primeiros
nomes, a regra da maioria (D-59) e o V/E/D do time. No racha de 19/09 os times foram montados errado,
o racha foi refeito, e a sessão gravada ficou com uma formação que nunca jogou junto aparecendo como
o time oficial. Sem correção, o card do racha e a folha do time contam vitórias de um time que não
existiu.
**Descartado:** derivar os times das partidas ignorando a montagem (a montagem é o fato; a
escalação da primeira partida já era o fallback de racha antigo e falha quando a primeira partida
tem substituição); rascunho com Salvar (a correção não toca em partida nem em nível, cada toque é
reversível com outro toque — um toque salva); edição durante o racha em andamento (ali a montagem
é a tela de times, D-129).
**Onde:** `viewSessTimes`, `ondeNaSessao`, `sessTimes`/`sessPick`/`sessAdd`/`sessSet`, `rachaTime`,
`LOG_TXT.sessTeams` em `index.html` · `scripts/smoke.py` (corrigir os times do racha) ·
`scripts/visual.py` (tela 27) · [Stats](../produto/stats.md) · [Interface §4](../produto/interface.md).

<a id="d-202"></a>
### D-202 · Sequência de vitórias zera no empate; sequência de derrotas na ficha
**Quando:** 2026-09-20.
**O quê:** em `statsLiga`, empate passa a zerar a sequência de vitórias (`seq`/`best`), como a
derrota já fazia. Entram `seqD`/`bestD`, a sequência de derrotas atual e a maior do período, zeradas
por vitória ou empate. A ficha mostra "NV seguidas agora" (verde) ou "ND seguidas agora" (vermelho)
a partir de 2, e "melhor sequência: NV" / "pior sequência: ND" a partir de 3 — V e D, não por
extenso, como pediu o dono da liga. Nos gerais do racha, logo abaixo de Maior sequência, entra **Pior sequência** (3 ou mais
derrotas seguidas, mesmo piso; desempate por patente e depois por mais derrotas) — pedido na mesma
conversa, depois de a ficha só ter mostrado o número para o próprio.
**Por quê:** a ficha dizia "melhor sequência: 4 vitórias" para uma série V E V V V — o empate era
transparente por um comentário no código, sem decisão registrada. Quem lê "seguidas" espera sem
nada no meio, e o dono da ficha não achou as quatro. A sequência de derrotas foi pedida junto: é o
mesmo número lido do outro lado, e cabe na mesma linha.
**Descartado:** manter o empate transparente e chamar de "invencibilidade" (é outro número, e não
foi pedido). A primeira versão deixou o ranking de derrotas de fora por parecer lista de vergonha;
o dono da liga pediu, e o racha lê isso como brincadeira, não como exposição.
**Onde:** `statsLiga` (`seq`, `best`, `seqD`, `bestD`), `listasRk` (`seqD`), ficha do jogador e o
ranking `seqd` em `viewStats` em `index.html` · `scripts/smoke.py` (V E V V V D D D → 3V, 3D; ranking
Pior sequência nos gerais) · [Stats](../produto/stats.md).

<a id="d-203"></a>
### D-203 · Acima do esperado com um pouco mais de destaque
**Quando:** 2026-09-20.
**O quê:** (1) na ficha do jogador, logo abaixo do anel de aproveitamento e da barra V/E/D, uma
linha com o número em destaque — "+12% acima do aproveitamento esperado" em verde, "−8% abaixo do
aproveitamento esperado" em vermelho, "0% dentro do aproveitamento esperado" — e nada mais (a
primeira versão trazia "vitórias reais − esperadas pelo confronto, por partida" ao lado; era texto
demais, e "aproveitamento esperado" já diz o que é); (2) nos gerais do racha, o ranking Rendeu acima do esperado passa a abrir
a lista em Mês, Ano e Sempre (era o segundo, atrás de aproveitamento ou presenças); (3) na faixa
Posição nos rankings da ficha, "acima do esp." vem antes de "aproveit.". Só com as patentes abertas,
como já era o ranking (D-143). Anel, tiles, ordem dos outros rankings e o momento não mudam.
**Por quê:** pedido do dono da liga: "como nem sempre as pessoas montam rachas equilibrados, a
métrica mais importante é o desempenho em relação ao esperado — um pouco mais de destaque, nada
exagerado". O aproveitamento premia quem caiu no time forte; o acima do esperado desconta o
confronto e é o que o motor de nível usa. Ele já existia como ranking e no gráfico do momento, mas
não aparecia na ficha como número.
**Descartado:** trocar o anel de aproveitamento pelo acima do esperado (o aproveitamento é a
leitura que todo mundo entende de cara; o pedido foi "nada exagerado"); tile na fileira (a
fileira já tem cinco no modo longo); mostrar com patentes fechadas (o número nasce do nível, que a
liga escolheu esconder).
**Onde:** ficha e ordem dos rankings em `viewStats`, `overPct` em `index.html` · `scripts/smoke.py`
(ficha com "do esperado"; Rendeu acima do esperado antes de Maior aproveitamento) ·
[Stats](../produto/stats.md).

<a id="d-208"></a>
### D-208 · Leão do fim do racha: quem faz mais gol por hora no fim do que no resto do racha
**Quando:** 2026-09-21 (quatro versões no mesmo dia — abaixo).
**O quê:** uma partida é **do fim do racha** quando quem começa em quadra nela já tem, em média,
**mais de 50 min de jogo naquele racha** (`fimDoRacha`: por sessão, em ordem, soma o tempo dos
trechos que contaram por pessoa e olha a média de quem está no primeiro trecho da partida;
`FIM_MIN`). `statsLiga` guarda, por pessoa, os gols de linha e os minutos de linha só nessas
partidas (`fim`); o resto é o total menos isso (`restoDe`). O **Leão** é `leaoDif`: gols por hora
de linha no fim − gols por hora de linha no resto. Ranking nos gerais de Mês, Ano e Sempre, logo
depois de Gols por hora, com a diferença e as duas taxas embaixo; **sem o piso de rachas** dos
outros rankings (`todos`, não `base`) — o piso é só 10 min de linha de cada lado (`FIM_MINL`,
`ehLeao`); quem não cresceu aparece negativo. No racha aberto (período Último), o Leão daquele racha
com a mesma conta dentro dele (tempo de linha dos dois lados). Na ficha, "fim do racha" na faixa Posição nos
rankings, só na leitura de linha.
**Por quê:** pedido do dono da liga: "no último racha todo mundo está muito cansado; seria
interessante uma métrica de Leão que mostra quem acaba fazendo muitos gols ou rendendo acima no
fim". Aguentar o cansaço é mérito de quem aguenta ([Ideias futuras §5](../produto/ideias-futuras.md):
o cansaço médio é o que se desconta do rating, um dia; o individual é leitura). Quatro versões no
dia, cada uma por uma correção do dono: (1) o fim era o **último terço das partidas**; "considere
quando as pessoas em campo começarem com mais de 50 min de jogo naquele dia em média" — cansaço é
tempo nas pernas, não posição na lista; a média é de quem começa a partida, porque é o cansaço
daquele confronto. (2) Havia dois rankings, o de resultado (acima do esperado no fim) na frente;
"você focou em resultados, vamos focar em gols". (3) Ficou gols por hora no fim; "está faltando
comparar com o resto do racha: quem fez 1 no fim mas 5 no resto não é leão; o leão é quem só faz no
final — e essa não precisa do piso de rachas, nem todo racha tem fim". Diferença de taxas, e não
razão, porque zero gol no resto é justamente o caso do leão e a razão explodiria. (4) O piso de gol
no fim saiu: "deixa todo mundo aparecer negativo" — a lista é de todo mundo, e o vermelho de quem
some no fim é informação. (5) O piso de tempo no fim caiu de 20 para 10 min de linha: medido nos
três rachas reais (29/08, 12/09 e 19/09 de 2026, arquivo corrigido), só o 19/09 passa dos 50 min,
nas 3 últimas partidas; quem liderava esse racha (4 gols no fim) tinha 19,8 min de linha ali e
sumia do mês. O fim rende ~3 partidas por racha e a pessoa joga 2 delas, então 10 min é o tamanho
de um fim. Rachas de 12 e 14 partidas com ~65 min de jogo não chegam aos 50 min de média — é o
esperado: racha curto não tem fim.
**Descartado:** último terço das partidas; relógio de parede (pausa e espera não cansam); só o
tempo de quem está lendo, sem média; ranking de resultado no fim; gols por hora no fim sem comparar
com o resto (premiava o artilheiro de sempre); razão fim/resto (divisão por zero no caso que
importa); piso de metade dos rachas (nem todo racha tem fim); piso de gol no fim (escondia o
negativo); 20 min de linha no fim (maior que o próprio fim); mexer no K ou no rating (D-83, D-195).
**Onde:** `FIM_MIN`, `FIM_MINL`, `fimDoRacha`, `restoDe`, `leaoDif`, `ehLeao`, campo `fim` em
`statsLiga`, `leao` em `listasRk`, rankings `leao`/`rleao` e a faixa de posições em `viewStats`,
ícone `hourglass` em `SICO`, tudo em `index.html` · `scripts/smoke.py` (12 partidas de 10 min, todo
mundo sempre em quadra: da 7ª em diante 60 min nas pernas; a pessoa só marca nas 6 do fim → +6/h e
abre a lista; o companheiro marca em todas → 0; quem só marcou no resto → negativo) ·
[Stats](../produto/stats.md).
