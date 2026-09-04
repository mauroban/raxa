# Decisões · Escada, calibração e palpite

> Nomes e número de níveis, divisões, o que aparece antes de calibrar, palpite de entrada e opiniões, visão do admin.
> Índice de todas as decisões e regra de registro em [README.md](README.md).

---

<a id="d-24"></a>
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

<a id="d-25"></a>
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

<a id="d-36"></a>
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

<a id="d-52"></a>
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
[Patentes §1](../produto/patentes.md), [Patentes §8](../produto/patentes.md), [Princípios §1](../produto/principios.md).

<a id="d-53"></a>
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
**Onde:** `CAL_GAMES` · `test.py` [6] ("calibracao e fixa: 15 partidas") · [Patentes §2](../produto/patentes.md),
[Patentes §6](../produto/patentes.md), [Princípios §9](../produto/principios.md).

<a id="d-57"></a>
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
renderização) · [Patentes §8](../produto/patentes.md) (ordem dentro do degrau) e [Contas e permissões](../produto/contas-e-permissoes.md) (nota no card dos melhores).

<a id="d-73"></a>
### D-73 · Corrigir nível "desde a entrada" — o palpite que faltou, com o racha contando por cima
**31/08/2026.** O painel "Corrigir nível" da ficha ganhou um seletor com dois modos. **A partir de
agora** (o comportamento que já existia, e continua o padrão): o Elo atual vira o meio do degrau
escolhido — `base += alvo − elo` — e o efeito das partidas já jogadas fica absorvido no ajuste.
**Desde a entrada** (novo, só aparece para quem já jogou): o degrau escolhido vira o **próprio
`base`** e o histórico inteiro **reaplica por cima** (`rebuildAll`) — é o palpite que faltou no
cadastro, dado depois do primeiro racha, com o racha valendo a partir do nível certo. O log de
correções grava o modo ("desde a entrada — histórico reaplicado").
**Por quê:** o caso real que motivou — um racha já aconteceu com todo mundo entrando em 1500 sem
palpite, e a simulação de convergência mostrou que o palpite vale meses de racha (ρ 0,94 contra
0,28 no segundo racha). Sem este modo, dar o palpite atrasado anulava justamente o racha que já
tinha sido jogado: a correção antiga ancorava o Elo corrente, "engolindo" os deltas da noite.
**Descartado:** trocar o comportamento padrão (a correção "discordei da escada de hoje" continua
sendo a mais comum no dia a dia); permitir "desde a entrada" também no Zerar (zerar já é, por
definição, voltar à entrada padrão); um terceiro modo com data de corte (ninguém precisa disso e a
partida é o único relógio que importa).
**Onde:** `pSheet` (seletor `pdDesde`), `pdSave` (ramo `desde`, com `rebuildAll`), `logCard` em
`index.html` · [Patentes](../produto/patentes.md) §"O sistema de nível" (bullet "Corrigir nível tem dois modos") ·
`smoke.py` ("corrigir nivel DESDE A ENTRADA": base no degrau, recálculo estável, modo no log).

<a id="d-74"></a>
### D-74 · Nada supera fatos: correção de nível só existe no nível de entrada
**31/08/2026.** O seletor do D-73 viveu horas: o modo **"a partir de agora"** (ancorar o Elo
corrente no degrau escolhido) **foi removido para quem já jogou**. Corrigir nível agora é sempre
mexer no **nível de entrada**: o degrau vira o `base`, o histórico reaplica por cima
(`rebuildAll`) e a patente atual sai do recálculo — nunca da mão do admin. O painel da ficha
passou a se chamar "Nível de entrada (o palpite)" para quem tem partidas, a régua e o stepper
partem do degrau do `base` (não da patente corrente), e o texto avisa: as N partidas já jogadas
reaplicam por cima. Quem nunca jogou tem `base = elo`, então continua entrando direto no degrau.
**Por quê (nas palavras do dono do racha): "nada supera fatos."** Ancorar o Elo corrente era o
admin sobrescrevendo o que as partidas disseram — e os times não são fechados a ponto de os fatos
não separarem as pessoas (os dados reais mostram ~8 companheiros distintos por noite). O único
palpite legítimo é sobre o que o app não viu: o nível com que a pessoa chegou.
**Descartado:** manter os dois modos com o "agora" escondido (dois caminhos para o mesmo botão é
como nasce inconsistência); editar a patente corrente diretamente (era exatamente o problema).
**Onde:** `pSheet` (painel e `rankSel`), `pdBump`, `pdSave` (ramo único pelo `base`) em
`index.html` · [Patentes](../produto/patentes.md) §"O sistema de nível" · `smoke.py` ("corrigir nivel de quem ja jogou
mexe no BASE", "quem NUNCA jogou entra direto no degrau").

<a id="d-79"></a>
### D-79 · Divisão 3 finalmente parece rara: o "polido" prometido virou CSS de verdade
**31/08/2026.** A intenção sempre esteve escrita no código — "1 fosca → 2 metal → 3 POLIDA
(reflexo + halo)", e o comentário do motor registra que **clarear a cor foi testado e rejeitado**
("lavava a cor, parecia transparente") — mas o CSS entregava menos que a promessa: a d3 tinha só um
halo quase invisível e o reflexo não existia; os fundos 9%→15%→22% não contavam história nenhuma.
Agora a rampa grita "quanto maior, mais raro": **d1** apagada (fundo 6%, borda rala, número a 55%),
**d2** o metal, **d3** a única com brilho — **banda de luz diagonal** (o reflexo do metal polido),
borda na cor cheia, halo externo + interno e o número com glow. A mesma rampa vale em TODOS os
lugares onde a patente aparece: badges (`.pat`, longos e curtos), pontinhos (`.pdot`), chips de
nível dos slots (`.tp.lv`), os **cards de promoção do fim de racha** (`.promo`, que só tinham a
cor) e os **avatares** da ficha e do painel (d3 ganha o halo).
**Descartado (de novo):** clarear a cor por divisão (já reprovado antes, o registro no comentário
segurou a recaída); número de estrelas/pips (o número da divisão continua sendo a leitura
principal — princípio de sempre); animação no brilho (bateria de celular na quadra).
**Onde:** CSS `.pat.d1/.d2/.d3`, `.pdot`, `.tp.lv`, `.promo.d1/.d3`, `.avatar.d3` e as classes
`divCls` em `endRacha`/avatares (`index.html`) · conferido no claro e no escuro pelo `visual.py`.

<a id="d-80"></a>
### D-80 · Divisão em riscos (I, II, III), não em número — e 3 continua sendo o topo
**01/09/2026.** O badge deixa de escrever "OURO 3" e passa a mostrar **OURO III**: o nome da
patente e uma, duas ou três barras retas, uma por divisão (nasceram inclinadas, `///`; retas
lêem como algarismo romano e ficam mais firmes no chip). A cor continua distinguindo a
patente, mas a divisão não podia depender só de tom (fosco/metal/polido, D-79) nem de um dígito
de 11px — no chip do time montado o pontinho era só cor, e ninguém lia a divisão ali. Contagem
se lê de longe e é auto-explicativa: **mais riscos, mais alto**. Isso também fecha a pergunta
"3 > 1 ou 1 > 3?": **fica 3 no topo**, como sempre foi (Diamante 3 é o degrau mais alto). Com
riscos, a ordem crescente é a única que faz sentido — três traços obviamente valem mais que um;
inverter (1 melhor, como no LoL/Overwatch, que usam algarismo romano) daria um risco ao melhor e
três ao pior, além de virar o motor, os testes e a documentação de cabeça para baixo sem ganho.
Valorant, Rocket League e Apex usam a mesma ordem crescente. O número não sumiu: segue em texto
corrido (`rankLabel`: "agora é Ouro 3", toast, registro de correções) e no `title`/`aria-label`
de todo badge. O mesmo desenho vale em TODO lugar em que a patente aparece: `patBadge`,
`patBadgeShort`, `patDot` (o pontinho dos chips virou riscos, na altura do chip), a escada
(`patDivOnly`: só os riscos, porque o cabeçalho já agrupa por patente), o editor de nível do
admin (badge grande no lugar do texto), os cards de promoção do fim do racha (badge no lugar do
texto) e a variação de nível dos destaques. Os pontinhos de **cor de time** que dividiam a classe
`.pdot` viraram `.swatch`, para não herdar os riscos.
Com os riscos dizendo a divisão, a **rampa de cor entre divisões da mesma patente afrouxou**:
a divisão 1 deixa de escurecer a cor (`patColor` devolve sempre a cor da patente — Ouro 1 escuro
parecia outro metal), o reflexo diagonal e o halo forte da 3 (D-79) saem, e fica só um halo
discreto na 3 — em badges, chips, cards de promoção e avatares. Duas coisas dizendo a mesma
coisa era ruído; a cor volta a ser só patente.
E a cor virou **a leitura principal da patente**: o badge deixou de ser texto colorido em fundo
tingido (12% da cor — ouro e prata lavados, quase iguais) e passou a ser um **bloco sólido na cor
do metal**, com texto e riscos na tinta que contrasta (`patInk`: escura em ouro/prata/bronze/
diamante, clara em ferro). O metal é o mesmo nos dois temas (`PATFILL`, sempre a paleta viva —
ouro tem que parecer ouro em cima do card branco); a paleta fechada do tema claro (`PATC_CLARO`)
fica só para texto na cor (cabeçalho da escada, botões de nível). O pontinho dos chips virou um
mini-badge sólido com os riscos, e os avatares da ficha recebem a mesma tinta. O nome continua
escrito nos badges longos (é editável por liga), mas dá para não ler: a cor basta.
A primeira versão do bloco sólido era cor chapada — ficou clara, mas **"parecia botão pintado,
não metal"**. O acabamento voltou por cima da cor, agora como metal de verdade e igual em badge,
pontinho e avatar: **degradê vertical** (luz no alto, sombra na base), **chanfro** (fio claro em
cima, fio escuro embaixo, borda na cor puxada para o preto), **reflexo diagonal** (`::after`) e
**texto e riscos em relevo** (`--emb`: sombra clara sob a tinta escura, escura sob a clara). Tudo
`color-mix` a partir de `--pc`, então cada metal tem o próprio brilho e nada muda por tema.
Os riscos têm largura em **px inteiro** (3px; 4px no badge grande): em `em` (.26em = 3,12px) o
subpixel arredondava um "I" para 3px e o vizinho para 4px, e saíam de grossuras diferentes.
Cada metal passou a ter **dois tons** (`PATFILL` = a peça, `PATFILL2` = a sombra embaixo do
degradê): com um tom só, ouro `#FFD84D` era amarelo-limão ("amarelo, não dourado") — agora é
âmbar `#E4AE1E` com sombra marrom-dourada; e diamante `#B9E6FF` era só azul-claro — agora é gelo
quase branco (`#D9F3FF`; depois `#C6EBFF`, um passo mais azul: em tela só de badges, prata e
diamante ficavam próximos) cuja sombra escorrega para o violeta `#8C93F0`, com o reflexo mais forte
(`PATSH`): brilho de pedra lapidada, que é o que faz parecer raro. Prata, bronze e ferro ficaram
como estavam. O ouro do texto no tema escuro (`PATC_ESCURO`) acompanhou para `#F0BE2A`.
O reflexo diagonal nasceu largo (banda de 28% a 66% da peça) e cobria o meio do nome; virou um
**risco fino de luz** (40% → 54%, pico a 30% de branco em 46%) — brilha sem apagar letra.
**Metal só em quem tem patente**: o degradê, o chanfro e o reflexo valem para `.pat`/`.avatar`
com classe de divisão (`d1/d2/d3`) e para o `.pdot`; os outros `.pat` — papel (Jogador/Admin/
Dono), "Pedido", o ⏳ de quem ainda calibra na escada — e o avatar sem nível ficam chapados e
foscos, como eram. Brilho é de patente, não de rótulo.
**Largura fixa**: o bloco de riscos (`.dv`) mede sempre a largura de III (13px; 18px no badge
grande; o `.pdot` 18px) com os riscos centralizados — OURO I, OURO II e OURO III têm o mesmo
tamanho, e a coluna da escada e os chips não dançam com a divisão.
**Sem fundo colorido atrás do nome**: com o badge dizendo tudo, os chips de jogador (`.tp.lv`,
times e slots) e os cards de subida/queda do fim do racha (`.promo`) perderam o tingimento na cor
da patente e a borda/halo por divisão — fundo neutro, e a cor só no mini-badge/badge. Tingir o
chip inteiro era a mesma informação duas vezes e deixava o time montado parecendo um mosaico.
**Botões de nível sem vazar** (ficha do jogador e "Novo jogador"): em 360px "DIAMANTE" precisava
de 58px num botão de 54 e saía pela borda. Os botões (`.ladder4`) passaram para a fonte condensada
dos cabeçalhos (12px, sem espaçamento), vão de 4px, e o nome vai num `span` com reticências — nome
de nível editado pela liga, comprido demais, corta em vez de vazar. O picker do cadastro ("Sem
nível" + 5 níveis) virou grade 3×2 (`.ladder4.six`) em vez de seis botões espremidos numa linha.
Medido em Chrome headless a 360px com a fonte de verdade: DIAMANTE ocupa 48px de um botão de 56.
Não bastou: no iPhone SE (320/375px, e com a fonte que o iOS tiver) continuou vazando. Então o
layout deixou de depender de fonte: em folha de até 420px os 5 níveis viram **3 + 2** (grade de 6
colunas — 2+2+2 em cima, 3+3 embaixo, os dois de baixo esticados), via **container query** na
`.sheet` (`container-type:inline-size`) e não media query — mede a largura real da folha e dá
para testar em Chrome headless, que não abre janela menor que 500px. Medido a 320/375/414/500:
DIAMANTE tem 128px em 320 e volta a 5 numa linha em 500 (84px). O `span` do nome é `display:block;
width:100%` (o `max-width:100%` em item de flex-coluna não corta no Safari).
**Descartado:** estrelas/pips (D-79 os rejeitou por parecerem "prêmio"; risco é patente militar,
não medalha); chevron em V (mais largo, estoura o chip); barras inclinadas (a primeira versão —
lembravam barra de URL); manter o número ao lado dos riscos (redundante e mais largo); manter a
rampa forte fosco/metal/polido junto com os riscos (redundante); inverter a ordem (acima).
**Onde:** CSS `.dv`, `.pdot`, `.swatch` e `divMarks`/`patBadge`/`patBadgeShort`/`patDivOnly`/
`patDot` em `index.html` · texto da tela Ajustes ("marcadas por riscos") · [Patentes §2](../produto/patentes.md)
· conferido nos dois temas, nos 15 degraus, com galeria em Chrome headless (sem teste automático
do desenho; `layout.py`/`smoke.py` cobrem o HTML).

<a id="d-86"></a>
### D-86 · A ficha deixa claro que o admin edita a ENTRADA — e mostra o HOJE que vai sair, antes de salvar
**01/09/2026.** A regra da D-74 ("só a entrada é editável; o hoje sai do histórico") está certa
e continua. O problema era a ficha: pedia a entrada sem dizer que era a entrada, e mostrava a
entrada escolhida no card de cima como se fosse o hoje. Aí o admin abria um Ouro 3, "baixava" para
Ouro 2 e, ao salvar, o jogador aparecia Diamante: com a entrada mais baixa cada vitória do
histórico passa a valer mais, e o resultado da reaplicação **não é monotônico**. Certo por
dentro, inexplicável por fora. Agora: o seletor é rotulado **ENTRADA**; ao lado, **HOJE** com o
nível atual e "não se edita"; ao mexer na entrada, `hojeCom` recalcula a liga com aquela entrada
(~20 ms, lido e desfeito, com cache por entrada) e a ficha mostra **antes de salvar** "HOJE Ouro 3
→ Ouro 1 ao salvar" e o texto "com a entrada em Ouro 2 (era Ouro 3), hoje fica Ouro 1". Os cards
de cima mostram o hoje previsto. O registro de correções guarda hoje-de → hoje-para e a entrada
usada. Quem nunca jogou: hoje = entrada.
**Descartado (tentado e recusado no mesmo dia):** inverter o controle — o admin escolher o hoje e
o app procurar a entrada que chega lá. Funcionava, mas trocava o modelo mental que a D-74 fixou:
o admin sabe qual era o palpite e é isso que ele corrige; o hoje é consequência, não pedido.
Também descartados: editar o hoje direto com um "ajuste manual" por cima do Elo (viola D-74: vira
fato inventado, e some no próximo recálculo); aba separada de "níveis base" (afasta a correção
de onde o admin já olha o jogador); só um sinal de "entrada" na escada (não resolve a surpresa).
**Onde:** `hojeCom` (motor), `pdEntrada`, `pdRank`/`pdBump`/`pdSave`, painel da ficha, `LOG_TXT`
de rank (`index.html`) · `scripts/smoke.py` (prévia na ficha, base vira o degrau escolhido, hoje
bate com a prévia, log guarda os dois, `hojeCom` não deixa rastro) · `scripts/test.py` (sem
histórico) · `scripts/visual.py` tela 11 "ficha admin" (a ficha com a entrada editada, nas duas
larguras) · [Patentes §2](../produto/patentes.md). Layout do painel: duas linhas rotuladas — ENTRADA (− badge +,
"era X") e HOJE (atual → previsto, "ao salvar") — em vez de − e + soltos nas bordas.

<a id="d-90"></a>
### D-90 · Nível de goleiro: a régua é a da linha, e a recomendação é NÃO dar palpite
**01/09/2026.** Dificuldade real do dono: "não sei como goleiro se compara com jogador de linha"
ao dar o palpite. A resposta conceitual: o Elo do goleiro entra na média do time como o de
qualquer um (`lvlOf`), então o nível dele já É na régua da linha — mede o quanto o time ganha
com ele, não a qualidade dele entre goleiros. Como "trocá-lo por um linha de que nível deixaria
o time igual?" é pergunta difícil, medimos a alternativa na régua de sempre
(`scripts/converge.py`-família): UM jogador **sem palpite** (entra 1500, K 64 assentando) numa
liga calibrada, com cansaço: frequente chega a ±1 divisão em 53% no 1º mês, 69% no 3º, 79% no
6º, sem viés (+0,1 degrau) — contra 24% → 43% de quem entra com palpite errado em uma patente.
Esporádico (1 em 3): 40% → 56%, também melhor que o palpite errado. Conclusão: **na dúvida
(típico em goleiro), sem nível é melhor que chute** — e virou a recomendação escrita: dica no
painel de nível da ficha (só quando a trilha é a de goleiro) e no cadastro.
Medida específica do goleiro de rodízio (`scripts/converge_gk.py`, motor real: liga inteira com
palpite exato, goleiro entra sem nível e joga as 12 partidas da noite, ora num gol, ora no
outro): ±1 divisão em 47% no 1º mês, 63% no 3º, 70–71% do 6º em diante — à frente do jogador
de linha sem palpite no começo (41% no 1º mês), porque joga todas as partidas da noite, e no
mesmo teto depois: a vantagem do rodízio é VOLUME (12 partidas/noite), não informação por
partida — o sinal dele dilui na média do time como o de qualquer um. Goleiro que vem 1 racha em
3: 38% → 67% no 9º mês. Goleiro muito acima/abaixo de Prata (≥1 patente) demora mais: 47% só
no 3º mês — mais um motivo para o palpite errado não ficar preso (D-91).
**Descartado:** escada de goleiro com régua própria "GK-Ouro ≠ Ouro" (quebraria a montagem de
times, que soma tudo numa média só); multiplicador de impacto do goleiro (não há dado medido).
**Onde:** dica em `pSheet` (painel de nível, role G) e na folha de novo jogador (`index.html`) ·
[Patentes §7](../produto/patentes.md) · `scripts/converge_gk.py` · números da simulação neste registro.

<a id="d-91"></a>
### D-91 · Tirar o palpite vale para qualquer um — o histórico reaplica sem ele
**01/09/2026.** "Tirar o nível — calibrar do zero" só existia para quem nunca tinha jogado;
agora tirar o palpite vale para todos. A dor é a da D-90: o palpite de goleiro é o mais difícil
de dar, e o palpite errado dado no cadastro ficava preso — a única correção era chutar OUTRA
entrada. Agora o admin desfaz o chute: `def` desliga, `base` volta ao padrão e o histórico
reaplica por cima (`rebuildAll`) com o K de quem calibra sem palpite (64 assentando) — as
partidas mandam mais, e a própria D-90 mediu que sem palpite converge melhor que palpite errado.
A prévia do hoje aparece antes de salvar, como em qualquer correção de entrada (D-86); quem
ainda está em calibração volta a "sem nível" até completá-la. No registro de correções:
"palpite removido — histórico reaplicado".
**Descartado:** manter a trava "só quem não jogou" (protegia um palpite, não um fato — fato de
quadra continua ineditável); apagar o histórico junto (partidas são fatos, D-74).
**Onde:** `pSheet` (botão e prévia), `hojeCom`/`pdRank` (entrada 'none'), `pdSave` (ramo none
reaplica) e o registro de correções em `index.html` · [Patentes §6](../produto/patentes.md) §"Tirar o palpite" ·
`scripts/smoke.py` ("tirar o palpite de quem ja jogou").

<a id="d-94"></a>
### D-94 · Sai o aviso "revisar palpite?" — ele apontava quem estava certo tanto quanto quem estava errado
**02/09/2026.** Pergunta: "em quanto tempo o aviso da D-83 pega um jogador uma patente inteira
fora?". Régua nova, `scripts/aviso.py` (mesmo modelo do `converge.py`, 200 ligas, motor real,
ranking da D-83 reimplementado): o errado assíduo entra nas 3 pontas pela primeira vez em mediana
no racha 4 (69% até o 8) — mas **num racha qualquer ele é apontado em 29% das vezes, e uma pessoa
certa (±1 divisão) também em 29%**; "apontado em 4 dos últimos 8" acontece com 32% dos errados e
26% dos certos; a deriva do Elo desde a entrada (≥100 pts no racha 16) com 44% dos errados e 19%
dos certos. Ou seja: 6 nomes por semana, 5 sem nada a revisar, e o admin sem como saber qual é
qual. A D-83 avaliou o aviso por "apareceu no top 5 alguma vez em 2–3 meses" — critério que
qualquer pessoa certa também cumpre. Mais remontagens por noite (0 a 3) aceleram a convergência
do Elo (35% → 46% dentro de ±1 divisão no racha 10) e não mudam nada no aviso. Também medido:
**K que sobe quando o Elo se afasta do palpite** (≥67/100/134 pts → K 32/48) é *pior* para o
errado (23–36% contra 48% dentro de ±1 divisão no racha 10) — o K maior vira ruído antes de
virar correção, o mesmo motivo do piso 20 na D-83. É limite de informação: ~0,07 de sinal por
partida de 5v5, contra um ruído de rating de ~1 divisão com 100 partidas.
**Decidido:** remover `rankingSurpresa`/`revisar`/`revisarTxt`, as constantes `REVISAR_*`, o
`m.overR` do `applyMatch` e o texto na escada, na ficha e no card de ajuda. A ficha do admin
continua mostrando **entrada** e **hoje** lado a lado (D-86) — o fato, sem chamada para agir.
Para os poucos erros grosseiros (quem "domina a bola" mas não decide, quem erra gol mas faz
muitos, quem marca bem e organiza sem aparecer nos gols), o caminho é humano: a **segunda
opinião** de quem vê o jogo — e, se a liga quiser um sinal automático, o único honesto é a
distância entre hoje e entrada depois de meses, que a ficha já mostra.
**Descartado:** limiar mais duro nas pontas (k≥6 dos últimos 8: 16% contra 10% — mesma razão,
menos avisos); manter o ranking "acima/abaixo do esperado nos últimos 8 rachas" como número na
Stats (a Stats já tem o "além do esperado" do período — dois números parecidos com nomes
parecidos confundem); K por deriva (acima); volatilidade à la Glicko (mesmo sinal, mesmo ruído —
não testada por isso).
**Onde:** `applyMatch`, escada (`viewRanking`), `pSheet`, card de ajuda em `index.html` ·
`scripts/test.py` (bloco D-83 removido) · `scripts/aviso.py` (régua) · [Patentes §4](../produto/patentes.md)/[Patentes §8](../produto/patentes.md).

<a id="d-95"></a>
### D-95 · A entrada é a junção das opiniões de quem lança; "Editor" vira "Moderador"
**02/09/2026.** A D-94 mostrou que os resultados não corrigem um erro grosseiro de palpite em
menos de meses, e que nenhum aviso automático enxerga isso antes. Os erros grosseiros que existem
de verdade (o que domina a bola mas não decide; o que erra gol mas faz muitos; o que marca e
organiza sem aparecer nos gols) têm uma marca em comum: **olhares diferentes discordam**. Então a
entrada deixa de ser o palpite de uma pessoa e passa a ser a **junção das opiniões de quem lança**
(admin, moderador, lançador — "quanto mais opiniões da patente base, melhor").
**O motor de juntar** (`juntaOpinioes`, `consolida`): cada trilha guarda `op` = uma opinião por
pessoa ({by, e, ts}; `by` nulo é o palpite do cadastro de antes). A ENTRADA (`base`/`def`/`dv`)
é **derivada** no começo de todo `rebuildAll` — base nunca mais se edita à mão. 1 opinião vale
ela; 2, a **média** (fica no meio: erro de patente inteira vira meio erro, que o motor corrige
em semanas); 3+, a **mediana** (uma destoante não puxa). **Divergência** = desvio *mediano* ≥ uma
patente (200 pts): Prata × Diamante, ou Bronze/Ouro/Lenda; Prata/Prata/Lenda não é (a mediana
está firme, e a Lenda aparece como "destoa"). Divergente entra no meio com o **K de quem está sem
palpite** (`kFor` lê `tr.dv`): os dados decidem rápido, e a ficha avisa. Opinião de quem virou
Jogador não conta (`opAtiva`); rebaixar a Jogador, ou remover o jogador, **anula** as opiniões
dele (`anulaOpinioes`, registro `opClear`) e o histórico reaplica sem elas. Ninguém opina sobre
si. Toda mudança de opinião reaplica o histórico na hora (a prévia da D-86 vira o resultado
mostrado depois de um toque — sem rascunho: opinião é um toque, tocar de novo tira).
**UX:** na ficha, um painel só — ENTRADA (badge, quantas opiniões, média/mediana) e HOJE lado a
lado, o aviso de divergência, a lista de opiniões com nome (todo mundo vê; o admin pode anular a
dos outros) e, para quem lança, a escada "Sua opinião". Na aba Jogadores, o card **Minhas
opiniões** (n de N) abre **uma pessoa por vez, num cartão**: avatar, nome, nível de hoje, o que os
outros opinaram, e as cinco patentes como **opções grandes** com o badge de metal e o que cada uma
representa em termos do que o time ganha com a pessoa (o texto que corrige o olhar do drible) —
não há legenda para ler nem lista de 16 × 5 botões para varrer. Um toque salva e passa para a
próxima pessoa sem a sua opinião; anterior/pular andam na ordem, fixada ao abrir (quem falta
primeiro, para ninguém pular de lugar); barra de progresso no topo; a lista de todos embaixo, com
a opinião dada ao lado, para conferir e voltar. A nota é dada onde a pessoa joga — na aba Linha
os cartões são só de quem joga na linha, na aba Gol só de quem vai ao gol; os outros ficam no
fim da lista, apagados e sem cartão (tocar abre a ficha). A
primeira versão (lista com escada de 5 botões por pessoa e uma legenda em texto no topo) foi
descartada: repetitiva e cansativa de olhar. Sexta opção **"Não sei"** (`e` nulo: resposta dada,
fora da conta — ninguém é cobrado por chutar); com **5+** pessoas esperando a sua opinião
(`opPendentesPor`, por posição), o card e a aba Jogadores **pulsam** devagar — e guiam até o último
passo: o card diz onde falta, o toque abre na posição certa e na primeira pessoa pendente, o
seletor Linha/Gol carrega a contagem e o cartão final aponta para a outra posição. O cadastro pede "sua
opinião" no lugar de "nível de entrada",
com o autor registrado. "Editor" vira **Moderador** (`souModerador`, `PAPEL`, migração do papel
gravado). Junção de cadastros (D-93) move as opiniões dadas pelo repetido para quem fica e as
devolve ao separar (`opsMov`/`opsDrop` no registro).
**Descartado:** opinião por divisão (o olho não distingue Ouro I de Ouro II; a entrada cai numa
divisão sozinha, pela média); média em vez de mediana com 3+ (uma opinião absurda puxava a
entrada); divergência pelo desvio médio (marcava Prata/Prata/Lenda como incerto — a mediana não
está); manter a opinião de quem virou Jogador "guardada" para voltar se for promovido (voltava
sem ninguém pedir, e apareceria na lista como fantasma — anular é o combinado); só moderador
opina (a base melhora com mais olhares, e o lançador é quem vê o jogo); rascunho + Salvar para a
opinião (na lista de 19 pessoas seria 19 salvamentos).
**Onde:** `PODE_OPINAR`, `OP_DIVERGE`/`OP_DESTOA`, `juntaOpinioes`, `opAtiva`/`opsAtivas`,
`consolida`, `anulaOpinioes`, `kFor` (dv), `hojeCom` (simula por opinião), `migPlayer` (op e
papel), `playerFacts` (op), `mkPlayer` (opinião do cadastro com autor), ações `opSet`/`opDel`/
`opSheet`/`opRole`, `opCard`, `pSheet` (painel), `pdSave`/`delPlayer` (anulação), `mergeDo`/
`unmerge` (opsMov/opsDrop), `LOG_TXT`/`logCard` em `index.html` · `scripts/test.py` [5b] ·
`scripts/smoke.py` ("opinar sobre o nivel", "rebaixar quem opinou", "minhas opinioes") ·
`scripts/visual.py` (tela 12) · [Patentes §4](../produto/patentes.md), [Patentes §6](../produto/patentes.md), [Patentes §8](../produto/patentes.md), [Contas e permissões §5](../produto/contas-e-permissoes.md), [Protótipo](../tecnico/prototipo.md) · RF-02.2/02.5/02.5b/
03.1d/09.5.

<a id="d-96"></a>
### D-96 · Com 3+ opiniões, média aparada (sem a mais alta e a mais baixa), não a mediana pura
**02/09/2026.** Com 5 opiniões, a mediana usa uma só e joga fora quatro — inclusive as duas
vizinhas, que concordam entre si. Agora `juntaOpinioes` tira a mais alta e a mais baixa e faz a
média do resto: com 3 é a mediana, com 4 as duas centrais, com 5 as três centrais, com 6 as
quatro. Uma destoante continua não puxando; as do meio pesam todas. Divergência segue pelo desvio
mediano (D-95).
**Descartado:** aparar mais de uma ponta de cada lado (com 5 a 7 opiniões sobraria quase nada);
média simples (a destoante puxa); pesar ou reescalar a opinião de quem dá muito Ferro e Diamante
(viés e escala por avaliador) — fica para depois, com a régua: precisa de 8+ opiniões por
avaliador sobre gente com 2+ outras opiniões para estimar sem ruído, e tem que aparecer para a
própria pessoa ("suas notas ficam meia patente acima das dos outros; o app compensa"), não na
ficha dos avaliados.
**Onde:** `juntaOpinioes` em `index.html` · `scripts/test.py` [5b] ("cinco opinioes") ·
[Patentes §4](../produto/patentes.md).

<a id="d-121"></a>
### D-121 · Sem anular opinião de uma pessoa; rebaixar a Jogador invalida (não apaga), e Jogador também opina
**04/09/2026.** O admin podia anular a opinião de uma pessoa específica sobre um jogador (o ✕ ao
lado de cada opinião na ficha). Isso saiu: é um poder cirúrgico demais — "não gostei dessa nota" —
e a D-95 já diz que a entrada é a junção de várias opiniões, não a escolha do admin. O único jeito
de tirar o peso das opiniões de alguém é **rebaixar a pessoa a Jogador**, e aí todas as dela deixam
de valer, de uma vez. E rebaixar **não apaga**: as opiniões ficam registradas (a ficha as mostra
apagadas, "não vale (Jogador)"), só saem da conta; promover de volta as revalida. `opAtiva` já
olhava o papel de hoje de quem opinou — o que mudou é que `pdSave` parou de chamar `anulaOpinioes`
(que segue existindo só para quem é removido da liga) e o log `opClear` deixou de ser gerado
(o rótulo fica, para o histórico antigo). Por fim, **Jogador também pode dar opinião**: ela fica
registrada e passa a valer quando ele subir — o card e a folha avisam ("valem quando você for
Lançador") e o card não pulsa para quem a opinião ainda não vale. `podeOpinar` passou a ser "tem
perfil vinculado"; `opinaoVale` é "lançador ou acima". E na folha "Minhas opiniões", quem não
joga naquela posição (goleiro na aba Linha, e vice-versa) continua fora da fila obrigatória, mas
**tocar no nome abre o cartão dele** (`OPV.solto`), não a ficha: ninguém é forçado a opinar, e
ninguém é impedido.
**Descartado:** manter o ✕ só para o admin com confirmação (já era assim); apagar as opiniões do
rebaixado (perde informação que volta a servir se ele for promovido); impedir Jogador de opinar
(a opinião de quem joga junto tem valor futuro, e o custo de guardar é zero).
**Onde:** `podeOpinar`, `opinaoVale`, `opAtiva`, `opCard`, `opSheet`, `opSet`, ficha (`pSheet`,
lista "não vale"), `pdSave` em `index.html` · `scripts/smoke.py` (sem `opDel`; rebaixar invalida e
promover revalida; jogador opina sem valer) · [Patentes §3.4](../produto/patentes.md) ·
[Contas e permissões §5](../produto/contas-e-permissoes.md).
