# Decisões · Dados, sync e código

> Fatos no banco, histórico como fonte da verdade, sync incremental, consistência entre celulares, limpeza de código e testes.
> Índice de todas as decisões e regra de registro em [README.md](README.md).

---

<a id="d-16"></a>
### D-16 · Estatística é derivada; o que a partida guarda é saída do motor
**18/08/2026.** Duelos, parcerias, presenças, aproveitamento e destaques são calculados do histórico a
cada tela. A partida guarda `deltas` e `over` (acima do esperado) — que são **saída do cálculo**, refeitas
por `rebuildAll`, não contadores mantidos à mão.
**Por quê:** contador gravado é contador que um dia desencontra do histórico, e aí ninguém sabe qual dos
dois está certo.
**Onde:** RNF-04.9 · RF-11.12 · teste `[13]` (recálculo reproduz o `over`).

---

## Interface

<a id="d-21"></a>
### D-21 · O histórico é a fonte da verdade
**18/08/2026.** Rating e patente são cache: `rebuildAll` reconstrói tudo a partir das partidas válidas,
em ordem. Toda correção, anulação ou exclusão dispara o recálculo integral, em transação.
**Por quê:** é o que permite corrigir uma partida de três semanas atrás sem deixar resíduo em ninguém.
**Onde:** [Banco de dados §1 e §8](../tecnico/banco-de-dados.md) · RNF-04.2/04.6 · teste `[8]`.

---

<a id="d-29"></a>
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
**Por que não o relacional completo ([Banco de dados](../tecnico/banco-de-dados.md)) agora:** o motor roda no cliente e lê a
partida como um objeto (trechos, escalações, gols). Quebrar em linhas de trecho/gol obrigaria a
remontar tudo no load sem ganho de transporte — é o passo certo quando o recálculo for para o
servidor. Partida como linha jsonb é a granularidade em que o app pensa.
**Descartado:** manter o documento e só separar o `live` (resolvia o gol, não o histórico que
cresce); normalizar trechos e gols já (ver acima).
**Onde:** `supabase/schema.sql` (bloco "LIGA EM PARTES"), `playerFacts`/`matchFacts`/`factsDoc`,
`diffParts`/`commitSnap`, `flush`, `applyDelta`, `loadAll`, `refetch`, `logCard` (tamanho).

<a id="d-63"></a>
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

<a id="d-66"></a>
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

<a id="d-67"></a>
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

<a id="d-68"></a>
### D-68 · A documentação alcança o backend — a [Protótipo](../tecnico/prototipo.md) sai da era do localStorage
**31/08/2026.** Varredura de documentação contra o código. **produto:** a seção "estado do protótipo" (hoje [Protótipo](../tecnico/prototipo.md), "estado do
protótipo") ainda descrevia a v1 — "tudo em localStorage, funciona offline", backend/contas/sync
listados como v2 futura, sequências e edição de nome como inexistentes (tudo isso já existia);
reescrita para o estado real, com a lista "ainda não existe" de verdade (link de convite, offline,
recuperação de senha, papel de escrita no servidor, temporadas…). Corrigidas as duas menções
erradas ao empate com 3 times ("os dois saem" — contradizia a própria §"Fila com 3–4 times" e o
código, D-39), o botão "↻ Girar" que não existe desde D-32 (também em [Regras do racha](../produto/regras-do-racha.md) e
RF-05.3l), o rótulo real do botão de vincular ("Sou eu", não "Este perfil sou eu"), a [Contas e permissões §3](../produto/contas-e-permissoes.md) marcando
link/busca como v2 e removendo a "entrada livre" que nunca existiu, e o princípio 11 que ainda
citava a proteção pós-promoção (D-46). **REQUISITOS:** RF-03.7/03.10 atualizados para 15 partidas
e K 64/32 (D-53/D-55); RF-10.1/10.2 deixam de afirmar "local e offline" (a versão com backend
precisa de rede); RF-10.3 (sincronização) marcado ✅; RF-11.15 parcial (sequências existem);
RNF-03.1/03.5 idem. **README:** modelo em partes (não "um documento jsonb"), botão do demo só sem
liga nenhuma, `sync.py` na lista de testes, `config.js`/`schema.sql` na estrutura, "sem
dependências" corrigido (supabase-js via CDN + fontes). **CLAUDE.md e [Deploy](../tecnico/deploy.md):** a lista de
testes vira os 4 obrigatórios + `visual.py` opcional — os três documentos citavam conjuntos
diferentes. **[Banco de dados](../tecnico/banco-de-dados.md):** cabeçalho sem localStorage; §8 explica que hoje a concorrência
é a trava de `leagues.version` (o `unique(session_id, ordem)` é alvo); [Princípios](../produto/principios.md) offline marcado como
alvo; nota sobre derivados (o esquema atual não grava nenhum — D-63).
**Por quê:** doc que contradiz o código (ou a si mesma, caso do empate) ensina errado exatamente
quem ela existe para ensinar.
**Descartado:** apagar a parte "alvo relacional" de [Banco de dados](../tecnico/banco-de-dados.md) (continua sendo o desenho da
v2 — só ganhou as notas de "hoje é assim").
**Onde:** documentação de produto ([Conceitos §2](../produto/conceitos.md), [Fluxo do racha §2](../produto/fluxo-do-racha.md), [Stats §5](../produto/stats.md), [Contas e permissões §3](../produto/contas-e-permissoes.md), [Protótipo](../tecnico/prototipo.md), [Protótipo](../tecnico/prototipo.md), [Princípios](../produto/principios.md)) · [Regras do racha](../produto/regras-do-racha.md) ·
[Requisitos funcionais](../produto/requisitos-funcionais.md) · [Requisitos não funcionais](../produto/requisitos-nao-funcionais.md) · README.md · CLAUDE.md · [Deploy](../tecnico/deploy.md) ·
[Banco de dados](../tecnico/banco-de-dados.md) · `.gitignore` (exemplo_partida_real.json, dados reais, fora do repositório).

<a id="d-102"></a>
### D-102 · Pronto para a quadra: cópia da liga no aparelho, prazo por pedido, batida de rede e avisos de mesclagem
**02/09/2026.** Revisão do racha ao vivo para o cenário real — várias pessoas ao mesmo tempo e sinal
que vai e volta. O que quebrava: (1) o navegador do celular mata a aba em segundo plano; reabrir sem
sinal caía em "não consegui carregar as ligas" e o que não tinha subido ia junto; (2) um pedido
pendurado numa rede meio morta travava o sincronizador por minutos (nada gravava, nada chegava);
(3) o aviso do Realtime se perde enquanto o celular dorme, e só a troca de aba buscava o que passou;
(4) a mesclagem descartava em silêncio: partida começada aqui sumia se o outro celular só marcou
presença antes, gol atrasado se perdia com um "atualizado por outra pessoa" genérico, e o mesmo gol
marcado nos dois celulares virava dois sem ninguém saber.
**Decidido:** a liga inteira (só fatos, como no servidor) fica no `localStorage` a cada mudança, por
conta, com a versão conhecida e a **diferença** para o que o servidor tem (não o snapshot inteiro —
seria a liga em dobro). Abrir mostra a cópia na hora; a carga pede só o delta desde ela; sem rede
segue lançando e sobe depois. Todo pedido ao servidor tem prazo de 12 s (corrida entre pedido e
prazo, além do abort). Batida de rede: a liga aberta é conferida a cada 15 s com racha ao vivo (60 s
fora) se nada chegou nesse intervalo, e ao reassinar o Realtime. Quem só olha vê "sem conexão" quando
o aparelho cai; quem lança vê "sem conexão · guardado no aparelho". Erro do servidor (com código) vira
"erro ao gravar" + toast uma vez, em vez de fingir que é rede. Mesclagem: partida começada aqui, sem
o servidor a conhecer, fica por cima de um `live` remoto sem partida com os mesmos times e o mesmo
tanto de partidas (levando o que a largada mexeu: rodízio de goleiros, completar); gol que não entrou
porque a partida acabou lá é dito com o número; gol do mesmo lado nos dois celulares com menos de
8 s de diferença fica (os dois) com aviso para conferir.
**Descartado:** IndexedDB (mais código para o mesmo ganho num racha de poucos MB); reescrever a
partida já encerrada no outro celular para encaixar o gol atrasado (mexe em vencedor, rodízio e
fila — o aviso e a correção pelo histórico são mais honestos); apagar sozinho o "gol dobrado" (dois
gols em 8 s acontecem de verdade); entrar sem rede com sessão vencida (raro: a sessão renova sozinha
com o app aberto).
**Onde:** `cacheAgora`/`cacheLoad`/`cacheSnapDiff`, `comPrazo`/`rpcT`, `loadAll` (incremental),
`recarrega`, `pulso`/`ligaPulso`, `mesclaLive` (`MESCLA.aviso`), `flush`, `refetch`, `afterLogin` e
os eventos `online`/`offline`/`pagehide` em `index.html` · `scripts/sync.py` (bloco "na quadra:
sinal caindo", 8 cenários) · [Fluxo do racha §3](../produto/fluxo-do-racha.md)/[Protótipo](../tecnico/prototipo.md)/[Protótipo](../tecnico/prototipo.md) · [Deploy](../tecnico/deploy.md) · RNF-03.

<a id="d-104"></a>
### D-104 · Consistência acima de tudo: o mesmo lance conta uma vez, e sem sinal há 20 s é só leitura
**03/09/2026.** Com dois lançadores, um com sinal e outro sem, a mesclagem somava o mesmo gol duas
vezes (com aviso) e a mesma substituição deixava o jogador duplicado em quadra (sem aviso nenhum). E
quanto mais tempo um celular ficava lançando às cegas, mais lances tinham que ser mesclados depois
sem ninguém ver. **Decidido:** (1) o mesmo lance visto de dois lugares é um só — gol do mesmo time em
menos de 8 s, mesma troca ou mesmo goleiro em menos de 60 s; fica o do outro (já no servidor), com o
autor do gol se só este tinha, e o aviso diz "contei um só — se foram gols diferentes, toque de
novo"; `replayCur` e `splitStints` nunca empurram em quadra quem já está lá. (2) **Trava de sinal:**
quem está sem sinal há mais de 20 s passa a só olhar (botões apagados, "sem sinal · só leitura",
toque explica), até o primeiro contato bom. "Sem sinal" é fato constatado — pedido que falhou, prazo
estourado, aparelho avisou — nunca silêncio; a batida do racha ao vivo passou de 15 s para 5 s para a
queda ser descoberta a tempo, e com gravação pendente a própria gravação é a batida. O último
contato bom vai para a cópia do aparelho: reabrir o app não zera. 20 s é a régua comum de app com
interação ao vivo (batida a cada poucos segundos, "caiu" depois de 3–4 perdidas; Socket.IO, jogos
multiplayer, editores colaborativos ficam entre 15 e 45 s). O usuário pediu explicitamente esse
corte, mesmo que impeça de usar o app numa quadra sem sinal nenhum.
**Descartado:** somar e avisar (D-102): dois gols do mesmo time em 8 s são raros demais para valer
o placar dobrado; travar só durante a partida (presença e times também se mesclam às cegas);
travar por silêncio (quem está parado com rede travaria); 60 s (a primeira versão — o usuário
pediu 20).
**Onde:** `mesclaLive` (`mesmoLance`), `replayCur`, `splitStints`, `PRAZO_SEM_SINAL`,
`BATIDA_VIVO`, `travado`/`semSinal`/`contato`/`msgTrava`, `pulso`, `dispara`, `onDrop`,
`beginPaint`, o `change` de ajustes e CSS `body.travado` em `index.html` · `scripts/sync.py`
("a mesma troca nos dois celulares e uma so", "os dois celulares marcam o mesmo gol", "sem sinal
ha mais de 20 s") · [Fluxo do racha §3](../produto/fluxo-do-racha.md) · [Deploy](../tecnico/deploy.md) · RNF-03.

<a id="d-116"></a>
### D-116 · Documentação dividida por assunto em `docs/`, decisões em arquivos por tema
**04/09/2026.** "As documentações não estão muito confusas? Misturando assuntos?" Estavam. `DOCUMENTACAO.md`
(99 KB) juntava produto, estado do código (§8, um changelog disfarçado) e uma cópia dos princípios
(§9); os bullets "o que a patente garante" (D-113) moravam dentro de §3.7 *Goleiro*. `DECISOES.md`
(179 KB, 116 entradas) tinha cinco seções por tema, mas 97 das 116 decisões estavam na última —
tudo desde a D-20 foi só anexado no fim, e a D-113 (motor) e a D-114 (filtros da Stats) dormiam sob
"Contas e dados (v2)". Nove `.md` na raiz. **Agora:** `docs/produto/` (um documento por assunto:
conceitos, patentes, fluxo do racha, stats, contestação, contas, princípios + regras de quadra e
requisitos), `docs/tecnico/` (protótipo, banco de dados, deploy, **estudos** — novo: o que cada
simulação mede e o número que ficou), `docs/decisoes/` (oito arquivos por tema, decisões em ordem
de número dentro de cada um, âncora `<a id="d-nn">` em cada uma, e um `README.md` com o índice de
todas e a regra de registro). Na raiz ficam só `README.md` e `CLAUDE.md`; o `CLAUDE.md` virou o mapa
"preciso de X → abrir Y", para que o assistente leia só o que a tarefa pede. Patentes ganhou a
seção 9 "O que a patente garante, medido" (D-113, D-115), saindo de Goleiro.
**Por quê:** navegar era rolar 2 100 linhas ou dar Ctrl+F; para a v2 e para quem chega, o
"por quê" de um tema precisa estar num lugar só, e um agente que carrega 280 KB de documentação para
mexer num botão gasta contexto com o que não precisa.
**Como foi feito:** script único (`git mv` para o que só mudou de lugar; divisão de `DOCUMENTACAO` por
seção de nível 1, renumerando as subseções; classificação das 116 decisões por título), reescrita de
todas as referências cruzadas (`DOCUMENTACAO §3.4` → `[Patentes §4](../produto/patentes.md)` etc.,
~100 ocorrências) e verificação automática de que todo link relativo e toda âncora resolvem.
**Descartado:** manter tudo na raiz com nomes em caixa alta (nove arquivos já não cabiam); um
arquivo por decisão (116 arquivos é pior de navegar que oito); reordenar as decisões dentro do tema
por importância (a ordem do tempo é a que conta a história); renumerar decisões (D-NN é citado em
código, testes e commits).
**Onde:** `docs/README.md` (mapa) · `docs/decisoes/README.md` (índice) · `CLAUDE.md` · sem teste — a
verificação de links foi um script descartável no momento da mudança.
