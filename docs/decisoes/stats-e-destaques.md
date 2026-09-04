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
