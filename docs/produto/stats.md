# Stats — o racha, você e os outros

> Parte da documentação do Raxa — índice em [docs/README.md](../README.md).


O ranking responde "quem é o melhor". O que ninguém consegue responder no fim do ano é o resto: *quantas vezes eu joguei contra o Rodrigo? Quem me ganha sempre? Com quem eu ganho mais? Quantos rachas eu peguei esse ano?* A aba **Stats** existe para isso — e ela é sobre você **e** sobre todo mundo, porque metade da graça é comparar.

## 1. A unidade: quem estava em quadra

Tudo aqui sai dos **trechos** (seção 3.4), não das partidas. Um **confronto** entre duas pessoas é um trecho em que as duas estavam em quadra **ao mesmo tempo, em lados opostos**; uma **parceria** é um trecho com as duas do mesmo lado.

Duas consequências que importam:

- **Vale igual em qualquer formato.** 1v1, 2v2, 5v5, 1v3 — o que conta é ter estado em campo junto. O histórico do duelo mostra o formato de cada encontro (`5v5`, `3v2`) para dar o contexto.
- **Substituição é respeitada.** Se você saiu aos 4 minutos e o seu time tomou dois depois, aquele trecho não é seu — nem no rating, nem nas estatísticas. É a mesma regra em toda parte.

## 2. O painel

**Período (D-149):** `Último` (racha), `Mês`, `Ano` ou `Sempre`. Os três primeiros abrem no **atual** (último racha, mês de hoje, ano de hoje) e ganham uma linha **‹ setembro de 2026 ›** logo abaixo do filtro, que anda para o racha, o mês ou o ano anterior; o botão passa a mostrar o escolhido (12/09, ago/26, 2025) e, tocado de novo, volta ao atual. Cada período traz a história quebrada **no passo abaixo dele**: no mês, **racha a racha**; no ano, **mês a mês**; em Sempre, **ano a ano** — com o gráfico **Momento** (D-150, D-151) — uma **linha com a % de vitória real − esperada** de cada grupo, o valor colado em cada ponto, a área entre a linha e o zero pintada (verde acima, vermelha abaixo), o zero tracejado no meio como "jogou o que o nível dizia", escala simétrica para cima e para baixo, e o **aproveitamento** do grupo em cinza embaixo do rótulo do eixo (D-152; não é uma segunda linha: são duas escalas) — e uma linha por grupo (rachas, partidas, gols, tempo, aproveitamento). Com as patentes fechadas a linha não existe e fica o gráfico de aproveitamento. No "Último" (um racha) não há gráfico: a história de um racha é o partida a partida. É a resposta direta para "quantos rachas joguei esse ano" e "e na vida?".

| Bloco | O que mostra |
|---|---|
| **A pessoa** | rachas no período, partidas, aproveitamento, vitórias, gols, minutos, barra V/E/D e as duas patentes; **ritmo com a média da liga ao lado** (D-109): linha e gol são leituras estanques — "gols / 10 min" e "gols por partida" contam só gols, minutos e partidas **de linha** e se comparam com a liga na linha; "sofridos / 10 min" conta só tempo no gol e se compara com a liga no gol. Cada cartão pede 20 min na função; a linha de baixo diz "média da liga" (calculada só na mesma função), verde se melhor, vermelho se pior. **Gol feito de dentro do gol** é conta de goleiro (D-110): sai da artilharia e dos gols de linha, aparece em dourado no cartão de goleiro ("2 gols feitos do gol"), no tile "gols de linha" e no ranking **Gols de goleiro** — a função é a do instante do gol, pelo trecho da partida e a faixa **Posição nos rankings** ("4º aproveit.", "1º vitórias", pódio em dourado — D-108; sem "de N", porque cada ranking lista só quem tem o número que ele ordena e o N variava). E o card **Partida a partida** (D-76): uma linha por jogo com V/E/D, placar pelo lado da pessoa, a **prob. de vitória** no início do jogo e um ⚽ por gol e o mesmo ⚽ **tingido de vermelho** por gol contra (D-107); paginado de 10 em 10 (‹ recentes · antigas ›) |
| **Duelos** | **Maior carrasco** e **Freguês** em destaque, e a lista de quem você mais enfrenta com V/E/D (5 na página; "Ver todos ›" abre a folha com a lista inteira e a ordem — D-112). Tocar em um nome abre o histórico completo do confronto: data, placar, formato e resultado |
| **Parcerias** | **Mais jogou junto** e **Melhor dupla**, e a lista de quem mais joga do seu lado — também com histórico ao toque. No ranking "Melhor dupla" da aba Racha, o % vem com a quantidade de partidas da dupla em letra pequena ao lado |
| **O racha no período** | tiles da liga e, só no mês, o gráfico de colunas **Gols por racha** (último em verde, média tracejada, média no título). No ano e em Sempre não há gráfico de colunas (D-158): a história fica no mês a mês / ano a ano logo abaixo; rankings de **longo prazo** (D-145): tudo é **taxa**, não total — aproveitamento, rendeu acima do esperado (% de vitória real − esperada por partida; só com as patentes abertas, D-143), +/− a cada 10 min, gols a cada 10 min de linha, maior sequência, menos vazado e gols de goleiro a cada 10 min no gol, melhor dupla. As exceções são **Mais presenças** e **Mais tempo em quadra**, que são o próprio volume (D-148) e não têm piso. Não há mais Artilharia (total de gols) nem Mais vitórias na temporada. **Piso: ter jogado metade dos rachas do período** (escrito em cada título como "mín. N de M rachas"); as taxas por tempo pedem ainda 1 h na função. Top 3 cada, com "Ver os 10 ›" abrindo a folha (D-112) e a linha do dono do perfil destacada (D-109); títulos com ícone SVG, sem emoji; **a ordem segue o filtro** (mês = forma; ano = temporada; sempre = carreira) |

**O painel da liga em Mês, Ano e Sempre (D-153)** tem, entre os tiles e os rankings:
- **Racha a racha / Mês a mês / Ano a ano** — uma linha por grupo do período (os rachas do mês, os meses do ano, os anos da vida), com partidas e gols e três chips: quem **rendeu acima do esperado** (com a % por partida; piso de 3 partidas num racha, metade dos rachas num mês ou ano), o **artilheiro** (gols de linha + do gol) e **▲ quantos subiram ▼ quantos caíram** de nível. **Empate** no número (D-159): o chip mostra o de **maior patente** e um **+N** com quantos empataram (o título do chip diz "empate com mais N"). **Tocar na linha abre aquele período** (racha, mês ou ano). Com um grupo só a lista não aparece: ele é o próprio período.
- **Níveis** (só com as patentes abertas) — a **escada de hoje** entre quem apareceu no período (cada pessoa pela patente da função em que mais jogou no período — goleiro fixo conta pela de goleiro; sem patente nela, vale a outra — D-156), como uma faixa proporcional com uma cor por patente e a contagem dentro de cada trecho (a legenda só nomeia; toque abre a aba Jogadores); tiles de quantos **subiram**, **caíram** e ficaram **no mesmo nível**; e os rankings **Quem mais subiu** e **Quem mais caiu**, em divisões, com o badge de onde saiu → onde chegou. **O "de onde" é o nível no início do período e o "para onde" é o nível no fim dele** (D-155) — não o nível de hoje: quem subiu em agosto e caiu em setembro aparece em agosto saindo de onde estava em agosto. Quem caiu e voltou dentro do período não mudou.
- A dica de cada ranking (o piso, a unidade) fica numa linha abaixo do título.

**"Trocar jogador"** abre os mesmos números de qualquer pessoa da liga (cada nome com o mini-badge de patente, igual ao da presença) — dá para conferir o carrasco do outro também.

**Linha e Gol** (seletor abaixo do período, só na aba **Jogador**): quem já pegou no gol no período tem duas leituras, e a ficha abre na função em que ele mais jogou (D-135). **Linha** conta só o que ele fez de linha; **Gol**, só o que ele fez no gol — partidas, V/E/D, aproveitamento, sequência, minutos, ano a ano, partida a partida, os cartões de ritmo e a posição nos rankings (no gol, a posição é *entre goleiros*). Na leitura do gol os tiles viram **gols do gol** e **min no gol**, e não há duelo nem parceria: o goleiro do rodízio troca de lado sem escolher com quem joga. Na leitura de linha, o goleiro dos outros continua nos seus duelos e parcerias — o filtro é da sua função, e a folha de cada confronto lê a mesma função da ficha. Quem nunca pegou no gol não vê o seletor.

**Goleiro conta em tudo.** O interruptor "Sem goleiros" (D-51) saiu (D-160): com os rankings em taxa (D-145) ele só mexia nos totais e ainda escondia o goleiro fixo dos rankings de goleiro. Os números *de goleiro* (menos vazado, gols de goleiro, tempo no gol) vêm do tempo no gol; os de time (V/E/D, aproveitamento, +/−, duelos, parcerias) contam a pessoa em qualquer função.

**No período "Último" (um racha):**
- **Qualquer racha, não só o último** (D-142): a linha **‹ Racha de 12/09 ›** abaixo do filtro anda para o racha anterior e o seguinte (a mesma linha serve para mês e ano, D-149); o botão do período passa a mostrar a **data** do racha aberto e, tocado de novo, volta ao mais novo. Na aba **Jogos**, um racha aberto tem o botão **Destaques do racha ›**, que cai nesta mesma leitura. Os destaques (rendeu acima do esperado, quem mais ganhou, artilheiro, times do racha…) existem para todo racha, não só o último.
- **Presentes** conta quem esteve no racha **desde o começo** — quem foi embora antes do fim continua contando (a sessão guarda a união de quem passou por lá, e rachas antigos são completados por quem aparece nas partidas).
- **Times do racha**: cada time aparece pelos **primeiros nomes dos jogadores originais** (até 5v5; **goleiro de rodízio não entra** — ele roda entre os times, então não é de time nenhum, nem no rótulo nem na conta da maioria abaixo; goleiro **fixo** de um time continua, porque aí ele é do time. Racha antigo, sem a lista do rodízio gravada, é resolvido pela evidência: quem pegou no gol por mais de um time na mesma noite estava rodando) — "Vinashow, Maike, João, Halisson" identifica melhor que "Time A"; o nome do time fica na linha de baixo, junto com os gols no formato **8/3 G** (feitos em verde, sofridos em vermelho). Tocar num time abre **a escalação original da montagem** (com o rodízio de goleiros à parte). Racha gravado antes dessa versão mostra a escalação da primeira partida, que era o que ficou registrado.
- **A vitória é do time que jogou, não do nome no placar.** Um lado da partida só conta como aquele time se **mais da metade dos jogadores originais** dele esteve em quadra em algum trecho. Time inteiro trocado não leva a vitória; se a formação que entrou é a maioria de **outro** time da noite, a partida conta para esse outro (empate de maioria: leva quem passou mais tempo em quadra). Formação que não é maioria de nenhum time não conta para time nenhum — o card avisa quantas foram. Isso vale no card da noite e no "Hoje: ..." da pré-partida; para o jogador, nada muda: V/E/D e nível continuam sendo de quem estava em quadra.
- **Cada ranking da noite** (melhor +/−, quem mais ganhou, artilheiro, rendeu acima, tempo em quadra, menos vazado) mostra 3 e abre **até 10** com o "▾ ver até N" — o mesmo padrão da temporada. Não há ranking de derrotas em lugar nenhum (D-134).

## 3. Destaques do mês — e por que não é aproveitamento

A primeira tela do racha mostra os **destaques dos últimos 30 dias** — a foto do mês, não o histórico
inteiro: o "craque da liga" premiava quem começou bem em março e sumiu. São duas listas e dois cards:

1. **Os melhores do racha** — a maior patente **entre quem apareceu no período**, por divisão e, dentro dela, por Elo (D-146). É a escada, filtrada por
   presença: quem some do racha some do pódio. Cada um entra pela **valência que mais jogou no mês** — quem
   passou metade do período no gol aparece com a patente de goleiro. A ordem é degrau, depois aproveitamento,
   depois nome — para qualquer papel, inclusive o admin: este card é a tela que todo mundo abre junto no
   racha, então a posição não denuncia quem está na frente dentro da mesma divisão. (A ordem por Elo do
   admin vale só na aba Jogadores — [Patentes §8](patentes.md).)
2. **Quem mais rendeu além do esperado** — o critério explicado abaixo; cada linha mostra à direita a **% de vitória real − esperada, por partida** (+8%), que é o que ordena a lista (D-144, D-147 — a mesma leitura dos rankings de temporada). Com as patentes fechadas, mostra as vitórias.
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

## 4. Por que existe um mínimo de partidas

**Aproveitamento é no idioma do futebol: pontos.** V vale 3, E vale 1, e o aproveitamento é a fração dos
pontos disputados que a pessoa levou — (3·V + E) / (3·partidas) (D-69). 100% é só vitória; empatar tudo dá
33%. A % de vitórias pura tratava empate como derrota, e racha empata muito. Vale em todo lugar que diz
"aproveitamento": o anel do painel, os rankings, duelos, parcerias, duplas, a ficha e o desempate da escada.

Aproveitamento com 3 jogos é ruído, e ruído no topo de um ranking destrói a credibilidade dele. Então:

- **empate** em qualquer ranking: quem empata **divide a mesma posição** (1, 2, 2, 4 — D-89) e, dentro do empate, **vem primeiro o de maior patente** (a da função em que mais jogou no período; D-159);
- os rankings de temporada da liga só consideram quem **jogou pelo menos metade dos rachas do período** (D-145; o piso aparece escrito em cada título) — o piso de 10 partidas ficou só para a melhor dupla;
- nos destaques pessoais (carrasco, freguês, melhor dupla) o piso é menor — 10, ou 10% das suas partidas, o que for menor, nunca abaixo de 3 — porque duelo individual acumula bem mais devagar que partida.

O resto das listas (mais enfrentados, mais jogou junto) não tem piso: elas são ordenadas por **quantidade**, então não têm como ser distorcidas por amostra pequena.

## 5. "Quem é você"

Quando alguém assume um perfil (**Sou eu**, na ficha do jogador), o app passa a saber quais partidas são suas:

- na aba **Jogos** (o histórico), as suas partidas ficam com uma **borda verde** e o selo `VOCÊ` do lado em que você jogou, colorido pelo seu resultado;
- um filtro **Todas / Só as minhas** no topo do histórico;
- o painel de Números abre direto em você.

Sem ninguém assumido, nada quebra: o painel abre em quem mais aparece nos rachas e o histórico fica sem marcação.

**Nada disso usa rating.** É contagem de resultado puro — por isso continua visível mesmo quando a liga esconde as patentes. Nesse caso só as duas patentes somem do bloco "A pessoa"; rachas, duelos, parcerias e aproveitamento ficam iguais.
