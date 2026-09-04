# Decisões · Contas, perfis e permissões

> Membro = jogador, entrada na liga, papéis, admin no servidor, juntar cadastros, apagar liga.
> Índice de todas as decisões e regra de registro em [README.md](README.md).

---

<a id="d-19"></a>
### D-19 · Um membro é um jogador — e só um
**18/08/2026.** Dentro de uma Liga, uma conta corresponde a exatamente um perfil. Garantido no banco
(`unique (liga_id, player_id)` em `liga_members`), não na tela.
**Por quê:** é o que faz "quantas vezes joguei contra o Rodrigo" ter uma resposta única.
**Onde:** [Contas e permissões §1](../produto/contas-e-permissoes.md) · [Banco de dados §4](../tecnico/banco-de-dados.md) · RF-09.2b.

<a id="d-20"></a>
### D-20 · Três caminhos para entrar, uma regra só
**18/08/2026.** Link de convite (vence em 7 dias, revogável), código de 6 caracteres (gera pedido para o
admin aprovar, salvo se a liga ligar *entrada livre*) e busca por `@usuário` com convite direto de uso
único. **Ninguém entra sem aceitar e sem o admin abrir a porta.** O admin tem controle total sobre
membros, e remover um membro não apaga o jogador nem o histórico.
**Onde:** [Contas e permissões §3](../produto/contas-e-permissoes.md)/7.4 · [Banco de dados §5](../tecnico/banco-de-dados.md) · RF-01.6* e RF-09.8/9.9/9.10/9.11.

<a id="d-22"></a>
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
(ver README "Estado" e [Banco de dados](../tecnico/banco-de-dados.md)).
**Onde:** `souAdmin`, `A.claim`, `A.setRole`, `A.review`… · Ajustes → **Membros** · smoke "assumir perfil".

<a id="d-26"></a>
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

<a id="d-27"></a>
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

<a id="d-62"></a>
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
(o esquema relacional de [Banco de dados](../tecnico/banco-de-dados.md)); ficou registrado como limitação em [Deploy](../tecnico/deploy.md).
**Onde:** `supabase/schema.sql` (`is_league_admin`, `migrate_league`, drop `save_league`,
`profiles_read`) · [Deploy](../tecnico/deploy.md) (§1.2 e "O que esperar") · sem teste novo: o Supabase falso de
`sync.py` só emula o dono-como-admin, e a regra nova é SQL puro.
**Correção no mesmo dia:** o script ainda guardava as versões superadas de `join_league` (retornava
`leagues`) e `league_accounts` (sem `pending`) antes das definitivas — num banco já migrado o
`create or replace` delas quebrava com `cannot change return type`, violando o "pode rodar de novo".
Só a versão definitiva de cada uma fica no arquivo; a promessa de idempotência voltou a valer.

<a id="d-85"></a>
### D-85 · Membros sai da aba Jogadores: papel na linha da escada, e um card só de pendências
**01/09/2026.** O card Membros respondia três coisas: quem tem conta e com que papel, "você é X",
e — para o admin — pedidos para entrar e contas sem jogador. As duas primeiras cabem na linha do
jogador e na ficha: quem tem conta com papel acima de jogador leva o **badge do papel** (ADMIN /
EDITOR / LANÇADOR) ao lado do nome; quem tem conta e é só jogador, o pontinho; a ficha já diz
`@usuário · papel`. O que **não cabe na linha de ninguém** é o que ainda não é jogador: pedido
pendente e conta solta. Isso virou o card **Pendências**, só para o admin e só quando há o que
fazer (senão não aparece). Enquanto ninguém vinculou conta, um lembrete para todos ("abra o seu
nome e toque em Este perfil sou eu; enquanto isso todo mundo é admin"). A aba Jogadores volta a
ser uma pergunta só: quem é de que nível.
**Descartado:** manter a lista completa de contas para o admin (é a escada de novo, com outra
ordem); mover Membros para Ajustes (D-23 já tinha trazido para Jogadores; a lista é que sobrava).
**Onde:** `pendenciasCard`, `papelMarca`, `viewRanking`/`viewEscada` (`index.html`) ·
`membrosCard`/`membrosCardBase` removidos · `sync.py` (pedido aparece) · [Contas e permissões](../produto/contas-e-permissoes.md).

<a id="d-93"></a>
### D-93 · Juntar dois cadastros da mesma pessoa — reversível pela ficha
**02/09/2026.** Erro fácil de acontecer: o lançador não acha o jogador na presença e cadastra
outro; o repetido joga a noite e o histórico da pessoa se divide. Agora o admin junta os dois pela
ficha ("⇆ É a mesma pessoa que outro cadastro…" → escolhe o outro → diz **qual fica**). `mergeDo`
reescreve os fatos: `trocaId` troca o id do que some pelo do que fica em todas as partidas onde ele
aparece (escalação, trechos, goleiros, gols, eventos), nas sessões e no racha em andamento (listas de
ids sem repetir), move a conta se só o que some tinha, apaga o cadastro repetido e recalcula do zero.
**Reversível de verdade:** a entrada `merge` do registro de correções guarda os fatos do cadastro
que sumiu (`playerFacts`), os ids das partidas reescritas, a foto das sessões tocadas e se o
cadastro que ficou já estava no racha em andamento. "Separar de novo" (`unmerge`, na ficha de quem
ficou) recria o cadastro com o mesmo id, troca o id de volta nas partidas listadas, restaura as
sessões pela foto, devolve a conta e recalcula. **Guardas:** só dá para juntar quem **nunca esteve
na mesma partida** (aí são duas pessoas — e é essa condição que torna a volta exata: nas partidas
reescritas só havia o que sumiu) e quem não está ligado a **duas contas diferentes**.
**Por quê:** a alternativa "apaga o repetido e corrige a escalação partida por partida" é o que
ninguém faz. E como o histórico é a fonte da verdade (D-21), juntar é reescrever fatos — o que exige
o caminho de volta gravado junto.
**Descartado:** apelido (`mergedInto`) resolvido na leitura em vez de reescrever (todo lugar que lê
id teria que resolver — motor, estatística, sessões, live — e o histórico deixaria de ser
auto-suficiente); guardar a cópia inteira das partidas reescritas no log (a condição "nunca juntos"
já torna a troca de volta exata, e o log sobe para todo aparelho); juntar durante o racha sem tocar
o live (o cenário típico é descobrir o repetido no meio da noite); permitir para Editor (é reescrita
de fatos: revisão, e revisão é do admin — D-22).
**Onde:** `trocaId`, `temId`, `partidasCom`, `juntaveis`, `juncoesDe`, ações `mergeSheet`,
`mergePick`, `mergeDo`, `unmerge`, `mergeFiltra`, `LOG_TXT`/`logCard` em `index.html` ·
`smoke.py` ("juntar dois cadastros da mesma pessoa — e separar de novo") · [Contestação e correção](../produto/contestacao-e-correcao.md) e [Protótipo](../tecnico/prototipo.md) ·
RF-02.6b.

<a id="d-105"></a>
### D-105 · Apagar liga: só o dono, só sem outros membros, digitando o nome
**03/09/2026.** Apagar uma liga eram dois toques (botão + confirm), para qualquer membro (quem não
era dono "apenas saía", mas o botão e o texto eram os mesmos). Apagar leva o histórico e os níveis
de todo mundo. **Decidido:** o botão "Apagar liga" só aparece para o dono (`DONO[id]`, que vem no
delta como `owner`); só funciona quando não há nenhum outro membro (o app confere pela lista de
contas e o banco confere de novo na policy `leagues_delete`, via `has_other_members`, porque a RLS
de `league_members` só deixa cada um ver o próprio vínculo); e pede o nome da liga digitado. Quem
não é dono vê "Sair da liga", com confirmação própria.
**Descartado:** tirar o poder de apagar de vez (liga de teste ou criada errada precisa sumir);
soft delete com purga em 30 dias (é o desenho de [Banco de dados](../tecnico/banco-de-dados.md), fica para quando o esquema
relacional entrar).
**Onde:** `A.delLiga`, `A.leaveLiga`, `DONO` e o card Dados de `viewCfg` em `index.html` ·
`supabase/schema.sql` (`has_other_members`, `leagues_delete`) · `scripts/sync.py` ("o dono nao
apaga enquanto ha outro membro", "quem nao e dono so sai", "so com o nome certo") · [Contas e permissões §4](../produto/contas-e-permissoes.md) · [Deploy](../tecnico/deploy.md) · [Banco de dados](../tecnico/banco-de-dados.md).

<a id="d-128"></a>
### D-128 · Arquivar em vez de remover; ficha por blocos; ajustes e permissão só para o admin
**04/09/2026.** (1) **Remover jogador** apagava o cadastro (nome, conta, papel, hábito de gol), as
opiniões recebidas e as dadas (só a quantidade ia para o log), e o `rebuildAll` recalculava o nível
de todo mundo — nas partidas dele o time passava a ter um a menos na média. O histórico "continuava",
mas com um "—" no lugar do nome, e podia ser feito por moderador, num toque, sem volta. Virou
**Arquivar** (`p.arq` = data, reversível): fora do elenco (`ativos(liga)` em presença, Chegou,
escadas, Minhas opiniões, revisão, junção, vínculo de conta), tudo guardado, histórico e nome intactos;
as opiniões dadas deixam de valer enquanto arquivado (`opAtiva`, D-121) e voltam ao reativar. Card
"Arquivados" nos ajustes (admin/moderador). **Apagar** só para cadastro sem partida e sem presença.
(2) **Ficha por blocos**: olhar (cabeçalho, nível, números) → Cadastro (formulário, Salvar fecha o
bloco) → Admin → Arquivar. Antes o nome era campo de texto no topo, leitura no meio, campos de novo
embaixo e quatro botões depois do Salvar. (3) Quem não é admin **não vê o bloco de permissão** (o
papel está no cabeçalho); **"Sou eu"** só para quem não tem perfil nesta liga (`podeConta`).
(4) **Ajustes por papel**: só o admin vê os controles; os outros veem formato/alvo, como o nível
anda, aparência e sair da liga. (5) *Minhas opiniões* não avisa "sua opinião passa a valer quando
você for Lançador": se a opinião vale é conta da liga.
**Por quê:** medo real de perder dado valioso por um descuido — e um dado que muda o nível dos
outros. Tela que mostra controle que a pessoa não pode usar ensina a ignorar a tela.
**Descartado:** confirmar o remover com o nome digitado (continua destrutivo); esconder os
arquivados da estatística (jogaram; é fato).
**Onde:** `ativos`, `opAtiva`, `playerFacts` (`arq`), `A.arquivar`/`A.reativar`/`A.delPlayer`,
`pSheet`, `cardArquivados`, `viewCfgBody`, `opSheet` em `index.html` · `scripts/smoke.py` bloco
D-128 · [Contas e permissões §7](../produto/contas-e-permissoes.md) · [Banco](../tecnico/banco-de-dados.md).
**Ajuste no mesmo dia:** o bloco "Cadastro" saiu — o nome volta a se editar **no próprio nome**, no
cabeçalho, e ganhou embaixo uma **descrição** discreta (`p.bio`, até 120 caracteres: apelido, "amigo
do Matheus", como chegou), editável por quem lança e lida pelos outros. Papéis afinados: **nome e
descrição, quem lança**; **qualquer outra alteração** (hábito de gol, permissão, arquivar, reativar,
apagar, card "Arquivados") **só o admin** — moderador deixou de arquivar. As linhas de gol/conta/
permissão ficam depois dos números, com o Cancelar/Salvar logo abaixo, e arquivar/apagar dentro do
bloco Admin, no fim. Log: `bio` ("mudou a descrição").
