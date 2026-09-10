# Decisões · Interface

> Tema, visual da quadra, navegação, densidade, ícones, emoji.
> Índice de todas as decisões e regra de registro em [README.md](README.md).

---

<a id="d-17"></a>
### D-17 · Tema claro é o padrão
**18/08/2026.** Claro por padrão; escuro e automático a um toque, por aparelho.
**Por quê:** o pior caso de leitura é celular no sol, em quadra descoberta — é nele que o app tem que
funcionar. Racha à noite escolhe o escuro em um toque.
**Onde:** RNF-08.5 · [Princípios](../produto/principios.md) (decisão 21) · verificado por teste visual nos dois temas.

<a id="d-23"></a>
### D-23 · Stats é a segunda aba, e Membros mora nos Ajustes
**28/08/2026.** A aba **Números** virou **📊 Stats**, logo depois de Racha: é a tela que a galera abre
entre uma semana e outra, e o nome antigo não dizia nada. Ganhou o retrato da liga no período (rachas,
partidas, gols, média, empates, maior goleada), forma recente e sequência de vitórias do jogador, e
rankings de sequência, goleiro menos vazado e melhor dupla. **Membros** (quem tem conta, com que papel)
vive no topo da aba **Jogadores** (ex-Patentes), acima da escada — é a mesma pergunta: "quem está aqui?".
**Onde:** `viewStats`, `statsLiga` (seq/best/ultimos/sofridos), `membrosCard`.

<a id="d-40"></a>
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
**Onde:** `index.html` (`<style>`, `NAV_TABS`, `setNav`, `drawApp`) · [Princípios](../produto/principios.md) (decisão 24)
· `scripts/visual.py` ignora `.nav` na checagem de sobreposição · RNF-08.

<a id="d-41"></a>
### D-41 · Menos contorno, menos texto
**28/08/2026.** Passada de limpeza depois do D-40. Chips, botões secundários, campos e blocos
internos deixam de ter contorno escuro e viram preenchimento suave (`--fill`); cartões perdem a
borda (sombra de 1 px). Os textos de instrução repetidos em cada tela (como arrastar, como a fila
gira, o que conta como partida, quem vê o quê) saem das telas de uso — presença, times, próxima
partida, partida ao vivo, Stats, Jogadores — e fica só uma linha curta quando ela orienta uma
ação ("Toque em quem chegou · 🧤 marca goleiro"). A explicação completa continua em Ajustes e
na documentação de produto.
**Por quê:** o usuário sentiu a tela poluída, e o motivo era texto demais: parágrafo explicativo
embaixo de cada bloco, lido uma vez e ignorado para sempre.
Na mesma passada, respiro entre texto e gráfico: anel de aproveitamento com o rótulo
afastado dos cartões, coluna de V/E/D que cabe "Derrotas", barras dos rankings a 8 px do
texto, presença em uma coluna até 460 px (nome inteiro em vez de "Jefferso…"), placar com o
"−" longe do nome do time.
**Descartado:** esconder as instruções atrás de um "?" por bloco — mais um alvo em cada tela.
**Onde:** `index.html` (`<style>`, `viewPresenca`, `viewTimes`, `viewProxima`, `viewJogo`,
`statsBlock`, `viewStats`, `viewRanking`) · smoke continua cobrindo os textos que importam.

<a id="d-78"></a>
### D-78 · Variação de nível da noite legível: seta colorida, uma por divisão, e o caminho escrito
**31/08/2026.** O bloco "Nível" do card do último racha usava 🔺/🔻 — os dois emojis são
**vermelhos**, então subir e cair pareciam a mesma coisa — e mostrava só a patente final, sem dizer
quanto a pessoa andou. Agora: seta de texto **▲ verde / ▼ vermelha**, repetida **uma vez por
divisão** (▲▲ = subiu duas; trava em três), o caminho escrito na linha (`Prata 1 → Prata 3 · 2
divisões`), a patente nova como badge colorido à direita, e quem andou mais aparece primeiro
(subidas, depois quedas). De quebra o bloco passou a respeitar `vePat` — com as patentes fechadas
para não-admin, os rótulos de nível não vazavam mais ali (era o único lugar da noite sem a
checagem).
**Ajuste no mesmo dia:** o caminho virou visual — badge da patente **anterior → badge da nova**
na direita da linha (`PRA 1 → Prata 3`), com "N divisões" no texto pequeno. E o teste do smoke que
exigia o "(esp. N%)" dos times ficou intermitente (o `pre` não cobre escalação com trecho curto
descartado, D-75) — passou a exigir só a "% V", que sempre sai; o commit anterior subiu com o
smoke vermelho por um `;` no lugar de `&&` no encadeamento, corrigido aqui.
**Descartado:** manter os emojis com cor no texto ao lado (a seta é o sinal — se ela não carrega a
cor, nada carrega); mostrar o delta de Elo cru (número não aparece para ninguém, D-52).
**Onde:** `cardsUmRacha` (IIFE do bloco Nível) em `index.html` · sem doc de produto nova (a [Stats](../produto/stats.md) já
descrevia "quem subiu/caiu de nível" sem prescrever a forma).

<a id="d-81"></a>
### D-81 · Chip de presença mostra o nível do papel de hoje (🧤 aceso = nível de goleiro)
**01/09/2026.** Em "Quem chegou", o badge ao lado do nome era sempre o nível **de linha** — quem
só tinha patente no gol (goleiro fixo) aparecia sem badge nenhum, e quem tinha as duas mostrava a
errada quando vinha de goleiro. Agora o badge é o do **papel em que a pessoa vai jogar hoje**:
🧤 aceso → nível de goleiro; apagado → nível de linha (`presBadge`). E troca **no lugar** ao tocar
no 🧤 ou ao marcar presença (que pode acender o 🧤 sozinho para quem costuma ir ao gol) —
`presBadgeUpd` substitui só o `<span class="pb">` do chip, porque redesenhar a lista reordenaria
embaixo do dedo (regra antiga da presença). Sem nível naquele papel, sem badge — igual à escada.
**Antes de marcar** não existe papel de hoje, então o chip mostra **o padrão da pessoa**: quem
"costuma ir ao gol" (cadastro) mostra o nível de goleiro, o resto o de linha; se o papel de
costume ainda não tem nível, vale o outro — é o que ela tem para mostrar. Ao marcar, passa a
valer o papel de hoje (e o 🧤 já acende para quem costuma).
**Descartado:** mostrar os dois badges (ocupa o chip inteiro em 360px e a informação relevante é
uma só: o papel de hoje); redesenhar a lista ao trocar (reordena embaixo do dedo).
**Onde:** `presBadge`/`presBadgeUpd`, `viewPresenca`, handlers `pres` e `presGk` (`index.html`) ·
[Fluxo do racha §1](../produto/fluxo-do-racha.md) · coberto pelo `smoke.py` (presença com goleiro marcado).

<a id="d-84"></a>
### D-84 · A escada só fala de nível: sem gols e sem bolinhas de forma na linha do jogador
**01/09/2026.** A linha da aba Jogadores tinha patente, V/E/D, ⚽ gols, calibrando, Elo (admin),
aviso de revisão (admin) e seis bolinhas das últimas partidas — informação demais para a pergunta
que a aba responde ("quem é de que nível?"). Saem os gols e as bolinhas; ficam patente, V/E/D e o
que é do admin. Gols e forma continuam na ficha e na aba Stats, que é onde se olha desempenho.
**Descartado:** tirar também o V/E/D (é o único número que justifica a posição para quem não vê
Elo). **Onde:** `viewEscada` (`index.html`) · [Patentes §1](../produto/patentes.md).

<a id="d-88"></a>
### D-88 · Presença densa no celular: duas colunas, chip menor, e ✕ na busca
**01/09/2026.** Cenário real: 50 cadastrados, achar os 18 que vieram. No celular estreito a
grade caía para UMA coluna de chips de 50px — ~12 nomes por tela, e marcar presença virava
rolagem e busca sem fim. Agora: **duas colunas sempre** (o media query que virava 1 coluna em
<460px saiu), chip de 42px, nome em 13px com reticências, badge e luva menores — cabe
aproximadamente o dobro de nomes por tela, com alvo de toque ainda acima de 40px. E a busca
ganhou o **✕** (aparece quando há texto): achou e marcou, limpa num toque e procura o próximo —
antes era apagar letra por letra no teclado.
**Descartado:** abreviar nomes por código ("Matheus B."): a reticência faz o mesmo sem inventar
apelido; lista corrida de uma coluna com fonte menor ainda (duas colunas rendem mais tela).
E o **arrasto rola a tela**: pintando presença com o dedo na borda (100px de cada ponta), a
página desce/sobe sozinha (`paintScroll`, via `requestAnimationFrame` + `scrollBy`) e continua
marcando quem passa sob o dedo — o `overflow:hidden` do modo pintura saiu (o `preventDefault` do
`touchmove` já segura a rolagem nativa; o hidden também travava o `scrollBy`). O ✕ da busca
ganhou `[hidden]{display:none}` (o `display:grid` da classe vencia o hidden do navegador).
O badge do chip virou **só cor + riscos** (o mini-badge dos times): escrever a patente comia o
nome do jogador — sobravam 4 letras. E o segurar-e-arrastar ficou menos "questão de timing":
espera de 180 → **150 ms**, tolerância de tremida de 12 → **20 px** (com 12, o polegar normal
cancelava o segurar), e a **linha inteira** (chip + luva + vãos) conta como área de pintura —
antes só o retângulo exato do chip marcava, e o arrasto pulava gente. O contador "12×" (rachas
que jogou) saiu do chip — a ORDEM por frequência fica (é o que acha a galera de sempre), o número
não precisava aparecer, e o espaço é do nome.
**Onde:** `.grid`/`.pchip`/`.gktog`/`.qwrap`/`.qclear`, `filterPlayers`/`limparBusca`,
`paintScroll`, `paintChipAt`, `presBadge`, `viewPresenca` (`index.html`) · conferido no
`visual.py` (tela 1, 360px) · [Fluxo do racha §1](../produto/fluxo-do-racha.md).

<a id="d-89"></a>
### D-89 · Menos densidade nos números: destaques recolhidos, V/E/D seco, duelos sem ruído, empate divide posição
**01/09/2026.** Quatro cortes de densidade, todos na direção "a tela responde uma pergunta":
**(1)** A aba Racha serve para iniciar racha; os destaques dos últimos 30 dias viraram um card
de UMA linha ("Destaques · últimos 30 dias · 3 rachas · 28 partidas ▾") que abre num toque
(`S.ui.destAberto`, lembrado) — e sem partidas no período o card nem aparece (antes ocupava a
tela explicando que não tinha nada). **(2)** Nas linhas de duelos e
parcerias, a barrinha V/E/D saiu — o "xVyEzD" ao lado já diz o mesmo (as três barras do HERÓI do
jogador ficam: primeiro tiramos as do herói por engano, o dono mandou voltar — a redundância era
nas linhas, não no painel). **(3)** Ainda em duelos e parcerias: a setinha ▲▼ por linha saiu
(o placar da linha conta a história); "Maior carrasco" e "Freguês" agora exigem,
além do mínimo de confrontos, **saldo de 3+** (2V×1D coroava freguês — ruído virando manchete;
a mesma régua vale para "Melhor dupla"); e os dois blocos ganharam a setinha de ordem dos
rankings (a lista lida do fim). **(4)** Em TODO ranking numerado, **empate no número divide a
mesma posição** (1, 2, 2, 4 — `posEmpate`): rankings de temporada (`rkBars`), +/− e times do
último racha, quem mais ganhou, melhores duplas.
**Descartado:** esconder os destaques atrás de uma aba (curiosidade boa quer um toque, não uma
navegação).
**Onde:** `statsBlock`/`toggleDestaques`, `.vednum`, `listaDuelo`/`carrasco`/`fregues`/`dupla`,
`posEmpate` e os cinco rankings numerados (`index.html`) · `scripts/test.py` (posEmpate) ·
[Stats](../produto/stats.md).

<a id="d-98"></a>
### D-98 · Montagem: times em duas colunas, um nome por linha
**02/09/2026.** No celular, os cartões de time empilhados com os nomes em chips soltos quebravam
em duas linhas por time e não cabiam quatro times na tela. Agora a montagem usa uma grade de
**duas colunas** (`.teamwrap.cols2`): cada time é um cartão vertical, um nome por linha (nome
longo corta com reticências), cabeçalho mais baixo. Toque e arraste continuam iguais. A
pré-partida (escalação por colunas) não muda.
O mesmo desenho vale para **quem está fora** na partida ao vivo e na pré-partida (`.foragrid`:
colunas por time de origem, um nome por linha) — os chips soltos com "TIME C" atrás do nome
quebravam em três linhas. E o **arrastar no toque** ganha a régua da presença (D-88): segurar
150 ms, 20 px de tolerância à tremida, e um `touchmove` não passivo que segura a rolagem
enquanto o arraste está ligado — `preventDefault` no `pointermove` não segura rolagem no toque,
então o navegador assumia o gesto, disparava `pointercancel` e o nome voltava no meio do caminho.
Ao vivo, o relógio cresce (58 px) e o placar encolhe na vertical; o botão **"Foi embora"** vira
alvo de arraste (`data-drop-zone="leave"`), com a mesma confirmação do toque.
**Descartado:** cartões na horizontal com rolagem lateral (esconde time); uma coluna com chips
menores (continuava quebrando); `touch-action:none` nos chips (impediria rolar a tela quando o
dedo começa em cima de um nome, que é quase sempre).
**Onde:** `viewTimes`/`timeCard`/`tpChip`, `viewJogo`/`viewProxima` (fora), CSS `.teamwrap.cols2`
e `.foragrid`, e os handlers de arraste (`pointerdown`/`touchmove`/`pointermove`) em
`index.html` · `scripts/visual.py` (telas 2, 3, 4) · [Fluxo do racha §2](../produto/fluxo-do-racha.md).

<a id="d-106"></a>
### D-106 · Sem emoji no botão de iniciar; bolinha vermelha para gol contra
**03/09/2026.** "▶ Iniciar racha" virou "Iniciar racha" — emoji no botão principal passa sensação
de amador. Na Stats, "Partida a partida" mostrava ⚽ por gol e 🙈 por gol contra; agora é uma
bolinha por gol e **a mesma bolinha, vermelha**, por gol contra (`.gball`/`.gball.own`), inclusive
no título "Gol contra" do resumo do racha. Os ⚽ de título (Artilheiro, Artilharia) ficaram por
enquanto.
**Onde:** `viewRacha` (botão), `ppRow` e o resumo em `index.html` · [Stats §2](../produto/stats.md).

<a id="d-107"></a>
### D-107 · Gol volta a ser ⚽ na "partida a partida"; gol contra é o mesmo ⚽, vermelho
**03/09/2026.** A bolinha em CSS da D-106 ficou pior que o emoji: o ⚽ já aparece na mesma tela
("⚽ 0,44 gols a cada 10 min") e a linha de cada partida ficava destoando. Voltou o ⚽ por gol
e o gol contra é **o mesmo ⚽ tingido de vermelho** por `filter` (grayscale → brightness .75 →
sepia → saturate → hue-rotate −45°), porque emoji não aceita `color`. O `brightness` antes do
`sepia` é o que faz o branco virar vermelho e não rosa; conferido em print no Chrome/Windows,
onde o ⚽ é azulado. Mantida a regra geral de não usar emoji em botão e indicador novo — a
exceção é o ⚽, que é a marca do gol no app inteiro.
**Descartado:** silhueta via `text-shadow` (vira um disco liso, igual à bolinha de CSS);
`mix-blend-mode: multiply` sobre círculo vermelho (borda do glifo varia por aparelho).
**Onde:** `.gball`/`.gball.own` em `index.html`, `ppRow` e o título "Gol contra" do resumo do
racha · [Stats §2](../produto/stats.md). Sem teste automático de cor; `layout.py` cobre a estrutura.
**Ajuste no mesmo dia:** a primeira versão saiu com 11px e `vertical-align:-1px` — pequena e
caindo abaixo da linha no celular, porque o glifo do emoji desce da linha de base de um jeito
diferente em cada aparelho. Agora é 14px (tamanho do placar ao lado) e a célula (`.gcell`) é
`inline-flex` centralizado, sem `vertical-align`.
**Segundo ajuste, mesmo dia:** o pedido era a parte **azul** da bola ficar vermelha, não a
branca. Trocado o tingimento (sepia) por `hue-rotate(135deg)`, que gira só o que tem cor e
preserva branco e preto. Como no Android/iPhone o ⚽ é preto e branco e o giro não faz nada,
e o celular é o que importa, entra um segundo passo: `url(#gcred)`, filtro SVG inline
(`feColorMatrix`) que manda preto para vermelho e deixa branco branco. Resultado: no celular a
bola fica branca com gomos vermelhos; no Windows, o azul vira vermelho. Descartado o `drop-shadow`
vermelho (halo borrado em 14px, e não pinta os gomos).

<a id="d-119"></a>
### D-119 · Sem o botão "Carregar o racha de sábado"
**04/09/2026.** A tela de ligas oferecia, para quem ainda não tinha liga, um botão que criava a
liga de exemplo "Racha de sábado" com 19 nomes. Era resto do protótipo: em uso real, alguém que
toca nele por curiosidade cria uma liga inteira de gente que não existe na conta dele. O botão
saiu. A ação `A.demo` continua no código **sem botão**: é a massa de dados de `smoke.py`,
`layout.py`, `visual.py` e `sync.py`, que a chamam direto.
**Descartado:** mover a montagem do exemplo para os scripts (quatro cópias do mesmo seed, ou um
prelúdio compartilhado só para isso); apagar o exemplo e reescrever os quatro scripts.
**Onde:** tela inicial (`renderHome`) e `A.demo` em `index.html` · [Deploy §3](../tecnico/deploy.md).

<a id="d-120"></a>
### D-120 · O cartão de opinião cabe na tela do celular
**04/09/2026.** O cartão de "Minhas opiniões" (nome, cinco patentes, "Não sei", anterior/próximo)
passava da tela num celular: as descrições de cada patente tinham duas frases e quebravam em três
ou quatro linhas no 360 px, a linha com as opiniões dos outros e a contagem "3 de 16 · faltam 13"
empurravam tudo para baixo, e a pessoa rolava para achar o Ferro e o "Não sei". Medido em Chrome
headless a 360 px: o cartão terminava a **633 px** do topo da folha, e a folha tem 88% da altura
da tela (563 px num celular de 640 px). Agora termina a **550 px**: descrição de **uma frase** por
patente (12 px; uma linha no computador, duas no celular), "Não sei — nunca vi jogar", opções de
44 px em vez de 56, avatar e nome menores, a contagem saiu da folha (o seletor Linha/Gol já mostra
quantas faltam; fica só "faltam N" ao lado do título e a barra de progresso) e a linha com **o que
os outros opinaram saiu do cartão** — fica na ficha; aqui a pergunta é a sua. A contagem de
opiniões recebidas na lista de baixo **fica** (é o que diz quem ainda precisa de opinião).
**Descartado:** cortar o "Não sei" ou a navegação; esconder a régua e deixar só o badge (a frase é o
que corrige o olhar do drible, D-90); folha em duas páginas.
**Onde:** `A.opSheet` (`SIGNIF`, cabeçalho, cartão) e CSS `.opcard`/`.opopt`/`.opbar`/`.opnav` em
`index.html` · medida: Chrome headless a 360 px (`scripts/visual.py` cobre a estrutura) ·
[Patentes §8](../produto/patentes.md).
**Ajuste no mesmo dia:** o Diamante deixou de ser "o melhor da quadra" (relativo: em todo racha
alguém é o melhor) e virou "muda o patamar do time sozinho" — é o que a patente garante. A dica
abaixo do cartão parou em "Pense no que o time ganha com a pessoa em quadra"; o "não só no drible.
Tocar de novo tira" saiu. E com **todas as opiniões dadas** a folha abre no "✓ todas dadas", não
no cartão da primeira pessoa da lista (`OPV.i = -1`): o cartão por padrão dava a sensação de que
ainda faltava opinar. Tocar num nome da lista continua abrindo o cartão dele.

<a id="d-131"></a>
### D-131 · Ajustes enxutos: só o que se mexe
**Quando:** 2026-09-07.
**O quê:** a tela de Ajustes perdeu todo texto que explicava o óbvio ou repetia a documentação:
"Quem tiver esse código entra", "Definido na criação…", o parágrafo inteiro de "Como o nível anda"
(K, calibração, D-94), as frases sob "Quem vê os níveis", sob os nomes dos níveis, sob Aparência,
sob "Trecho mínimo" e sob Dados. Os cartões foram agrupados: **Liga** (formato, quem vê, nomes dos
níveis), **Partida** (gols, minutos e trecho mínimo numa linha; os três interruptores), Contestação
numa linha, Aparência, arquivados, Dados. A tela do admin caiu de ~10 telas de rolagem para ~3.
**Por quê:** "a tela de ajustes tem muito texto que não devia estar lá". O que precisa de explicação
mora em `docs/produto/`, não na quadra (mesma régua de D-129: não explicar o óbvio).
**Onde:** `viewCfg`, `viewCfgBody` em `index.html` · `scripts/visual.py` (tela 7 passa a ser a do admin).

<a id="d-133"></a>
### D-133 · O placar é o cabeçalho da coluna do time
**Quando:** 2026-09-07.
**O quê:** na partida ao vivo e na próxima partida, cada lado é **uma coluna na cor do time**
(`.esc2 .col.team`, moldura e fundo tingidos por `--tc`): o bloco do placar (toque = gol) ou o nome com a
chance é o cabeçalho, e os jogadores vêm logo abaixo, dentro da mesma moldura. Some o placar solto
acima da escalação e o "VS" do meio (ele estreitava as colunas). A fila fica fora das molduras, no
mesmo cartão. O aviso de gol sem autor e a tirinha do autor ficam logo abaixo das colunas.
**Por quê:** "os jogadores em campo podem estar mais ligados ao seu time, como uma continuação de
TIME A e TIME B — fica claro quem está em campo e quem está fora".
*Ajuste no mesmo dia:* a moldura ficou sem fundo tingido (o chip do jogador misturado com a cor do
time ficava estranho) — só a borda e o cabeçalho levam a cor; e o cartão dos lados abriu mão do
respiro (`.card.lados`, 8px) para as colunas ficarem mais largas no celular.
**Onde:** `escCol` (`extra.cls`), `viewJogo` (`placar(s)` como `head`), `viewProxima` em `index.html` ·
`scripts/visual.py` (telas 3, 4 e 15).

<a id="d-137"></a>
### D-137 · Sem cabeçalho de liga nas telas; a liga mora em Ajustes
**Quando:** 2026-09-10.
**O quê:** some o cabeçalho fixo de 56 px (marca, nome da liga, "N jogadores · N rachas · N partidas" e
a seta para a lista de ligas) que ficava no topo de todas as abas. Cada aba começa pelo próprio
conteúdo — na partida ao vivo, pelo relógio. O que o cabeçalho trazia foi para o **primeiro cartão de
Ajustes** (`.ligahdr`): inicial da liga, nome, os mesmos números e o botão **Trocar de liga** (mesma
ação `home`). `--toph` virou 0 (a barra de seleção da presença gruda no topo de verdade).
**Por quê:** "o cabeçalho com o nome da liga em cima está ocupando muito espaço inútil em todas as
telas". Trocar de liga é raro; o nome da liga a pessoa sabe. Uma tela inteira de celular na quadra vale
mais que 56 px de identidade.
**Descartado:** encolher o cabeçalho (continua sendo uma faixa parada); mostrar só na aba Racha (a
inconsistência confunde mais que ajuda); pôr o "Trocar de liga" no rodapé de navegação (é ajuste, não
aba).
**Onde:** `drawApp`, `viewCfg`, CSS `.ligahdr`/`--toph` em `index.html` · [Fluxo §3](../produto/fluxo-do-racha.md)
· [Contas e permissões](../produto/contas-e-permissoes.md) · `scripts/smoke.py` (passo "D-137").

<a id="d-138"></a>
### D-138 · O autor do gol se escolhe na coluna do time que marcou
**Quando:** 2026-09-10.
**O quê:**
1. O bloco do placar diz sempre **"＋ gol"** na linha de baixo; a chance de vitória foi para a linha do
   nome ("Time A · 52%"). Antes a linha de baixo mostrava a chance, e só "toque = gol" quando não havia
   chance — o bloco não parecia um botão.
2. Depois do toque, **um clarão na cor do time cobre a tela por um instante** (`#golflash`, 0,85 s),
   o celular vibra três vezes e **a folha "GOL!" sobe por cima de tudo** (`golSheet`): cabeçalho na cor
   do time com "GOL!", nome, minuto e placar (animação de pop); os nomes do lado (goleiro incluído)
   como chips grandes; o seletor **do time / contra** (a lista passa para o outro lado); **sem autor**;
   e **↶ Não foi gol** (`delGoal`), que tira o gol — o caminho do toque sem querer. A página rola para
   o topo. Fechar a folha pelo fundo deixa o gol sem autor. Enquanto está aberta, o delta do realtime
   espera, como qualquer folha (`ocupado()`).
3. O aviso "N gols sem autor — toque para marcar" e o toque no nome do card **Gols** abrem a mesma folha.
   A tirinha `#scorer`/`showScorer` abaixo das colunas deixou de existir.
*Ajuste no mesmo dia:* a primeira versão fazia a **própria coluna do time** virar a escolha do autor
(nomes verdes, outro lado apagado). Foi descartada: "fica meio confuso, porque é o mesmo lugar e a
mesma ação de trocar o jogador" — e o gol precisava de um efeito mais impactante, para ninguém marcar
sem perceber. Daí a folha por cima, o clarão e o "Não foi gol".
**Por quê:** "não está muito intuitivo marcar um gol e seu autor: dá a sensação que tem que clicar no
nome de alguém para marcar gol, e o autor do gol está aparecendo muito longe, lá embaixo". A tirinha
ficava abaixo das duas colunas inteiras — com 5 nomes por lado, longe do dedo que acabou de tocar o
placar. Os nomes que a tirinha repetia já estavam na tela, na coluna certa.
**Descartado:** escolha do autor na própria coluna do time (confunde com a substituição, ver acima);
tirinha flutuante sobre a coluna (tampa nomes); folha que não fecha sem escolher (bloqueia — D-101);
esconder o aviso de gol sem autor enquanto a folha está aberta (ela pode ser fechada sem escolher e o
aviso tem que continuar lá).
**Onde:** `golFlash`, `golSheet`, `viewJogo` (`placar(s)`), `A.goal`, `A.scorerSide`, `A.goalScorer`,
`A.delGoal`, CSS `.golflash`/`.golhdr` em `index.html` · [Fluxo §3](../produto/fluxo-do-racha.md) ·
`scripts/smoke.py` (passo "D-138") · `scripts/visual.py` (tela 17 "gol": a folha aberta).
