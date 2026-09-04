# Estado do protótipo (`index.html`)

> Parte da documentação do Raxa — índice em [docs/README.md](../README.md).


**Revisão mostra a partida inteira e corrige autor de gol.** A revisão (admin) remonta a partida a partir dos trechos e do log de eventos: ficha de quem jogou (tempo em quadra, papel, gols, entrou/saiu), linha do tempo com gols, substituições, trocas de goleiro e pausas, os trechos com escalação e peso, e o efeito no nível — por papel, quando a pessoa fez linha e gol na mesma partida (D-118). Cada gol da linha do tempo é um botão: tocar abre a escolha entre quem estava em quadra pelo time que marcou (ou pelo outro, na abinha "contra"). A artilharia é recontada e a correção fica no registro.

**Substituição, vaga e "foi embora".** Trocar alguém durante a partida vale só para aquela partida: os times voltam iguais na seguinte (a única troca que fica é titular ⇄ reserva do mesmo time). Time com gente a menos mostra **vagas tracejadas dentro do cartão**: na montagem a vaga puxa alguém da fila ou da reserva de outro time; na pré-partida ela escolhe quem completa só aquela partida (o emprestado aparece no cartão com ✕ e volta para o time dele depois). Quem se machuca ou precisa ir embora sai por **🚑 Foi embora** (botão na pré-partida): sai da presença, do time, da fila e do rodízio; se estava em quadra, a partida segue com um a menos e o trecho seguinte registra isso. Quem ainda não jogou hoje pode sair como **marcado por engano**, sem contar presença.

**Escalação sempre à vista.** Na pré-partida e na partida ao vivo, logo abaixo do nome/placar de cada time, aparece a escalação em duas colunas: o goleiro num slot próprio em cima (🧤, o ponto do nível pela patente de goleiro, e ↻ se vier do rodízio) e um slot por vaga de linha (5 no 5v5; vaga vazia fica tracejada). Quem não estava no time quando o racha começou (composição original, guardada em "Começar racha") leva um ⇄ discreto — emprestado, completando, substituto ou movido depois. Ao vivo, tocar num nome substitui (ou arraste um reserva/alguém de fora sobre ele); o slot 🧤 e a vaga de linha entram na mesma gramática (de fora para o 🧤 = entra no gol e o goleiro sai; de linha para o 🧤 do mesmo lado = trocam de papel; 🧤 com 🧤 = trocam de lado; de linha para o 🧤 vazio = vai ao gol e a vaga da linha fica marcada), sem folha — D-117. Quem descansa no rodízio aparece entre os de fora, no grupo "🧤 Rodízio". Na pré-partida a coluna tem o nome do time em cima e as reservas embaixo, e é ali que se edita, **com a mesma gramática da partida ao vivo** (D-123): nome ⇄ nome troca de lugar de vez; de fora → 🧤 põe no gol (só nesta partida com rodízio; com goleiro fixo entra no time no lugar do goleiro); de linha ⇄ 🧤 trocam de papel nesta partida; de fora → vaga completa; 🧤 ⇄ 🧤 trocam de gol. Quem completa (⇄) sai com um toque sem marca. A vaga fica à vista mesmo "jogando 4v4 assim", e os times que esperam também mostram a sua ("＋ vaga" no card Fora: quem entra nela entra no time de vez). No card Fora o chip carrega a chave `fora:ID` — é a pessoa, não o slot do gol que ela ocupa emprestada, então trocar dois nomes ali troca de time sem mexer no goleiro. A folha antiga do goleiro e a lista de quem completa continuam por "outras opções" / "escolher da lista" na dica, com o 🧤 ou a vaga marcados.

**Goleiro da próxima partida.** Com rodízio, a sugestão do app segue a regra do racha: **o goleiro fica com o time que fica em quadra** — o que venceu ou, no empate, o que ficou (com 3 times um fica no empate: o que entrou por último; com 4, os dois saem); só o outro lado troca, e recebe quem está há mais tempo esperando no rodízio. A pré-partida mostra o goleiro no slot 🧤 de cada lado e qualquer um pode ser trocado por toque/arraste — por outro do rodízio (grupo "🧤 Rodízio" no card Fora), por alguém do time ou por alguém da fila — antes do apito; com rodízio a escolha vale só para aquele confronto (`nextGks`). "Foi embora" fica na pré-partida (ao lado de "Chegou agora"), e não na substituição. Não há botão de "girar a fila": troca fora do automático é toque/arraste entre fila e time.

**Duplas inseparáveis.** Elo por time não separa quem joga sempre junto: os dois ganham e perdem os mesmos pontos e convergem para o mesmo nível, seja qual for a diferença real. Quando uma dupla tem ≥20 partidas (≈3 rachas sempre juntos, D-56) e ≥80 % do histórico de um deles em comum, o app avisa em Stats → Racha ("🔗 Sempre no mesmo time", com a % de partidas juntos) e na ficha de cada um. O remédio é separá-los na montagem por algumas noites — ou ligar "Evitar repetir quem já jogou junto" nos Ajustes.

**Fila com 3–4 times.** Quem espera há mais tempo joga antes; vencedor fica (se ligado), perdedor vai para o fim da fila. Empate: com 3 times **um fica** — o que entrou por último (o que já estava sai); com 4, os dois saem.

**Sem "maior goleada".** Partida de racha é curta e termina em 2 gols; placar não mede nada. Retirada da aba Racha.

**+/-.** Na liga de partida única, a estatística principal de cada jogador (no racha curto ela existe, mas fica depois das vitórias): gols a favor menos gols contra enquanto ele estava em quadra, em todos os trechos. É o primeiro número do cartão do jogador (Stats e ficha) e o primeiro ranking do período e do último racha. Na partida longa, onde a noite tem uma partida só, é o que separa quem esteve dentro nos bons momentos de quem não esteve.

**Minutos e ritmo.** Cada trecho guarda a duração de jogo (sem pausas), então minutos em quadra e no gol são somas exatas por jogador. A aba Stats mostra minutos, **gols a cada 10 min de linha** (tempo no gol não conta, D-109) e, para goleiros, **sofridos a cada 10 min** (rankings de ritmo e o destaque "Menos vazado" pedem 1 h em quadra/no gol; goleiro é sempre medido por tempo, nunca por partida). Stats tem duas abas — **Jogador** (a pessoa: aproveitamento, ano a ano, duelos, parcerias) e **Racha** (a liga no período e os rankings) — e o período (ano ou desde sempre) é filtro, não aba. Cada ranking mostra o **top 3** na página, limpo (posição, nome, número), e, na linha do título, um botão **"Ver os 10 ›"** que abre uma folha com a lista inteira (até 10, com o detalhe de cada linha) e a **ordem** — abre sempre "Do 1º ao último"; "Do último ao 1º" é a mesma lista lida do fim, quem está pior naquele número, com a posição recomeçando do 1, e vale só naquela abertura (D-112; substitui a setinha no cabeçalho e o "ver até 10" que abria na página). **Empate no número divide a mesma posição** (1, 2, 2, 4 — D-89). E **a ordem deles responde à pergunta do filtro**: em *30 dias* a forma abre a lista (aproveitamento, vitórias, sequência, artilharia); num *ano*, presenças e campanha; em *Sempre*, o volume de carreira (presenças, tempo em quadra) vem primeiro. Na partida única o +/− abre em qualquer filtro (D-45). Os filtros são uma família só (D-114): dois seletores segmentados empilhados — Jogador/Racha e o período (Último · 30 dias · ano · Sempre) — e o interruptor "Sem goleiros" alinhado à direita, sem card em volta. Além dos anos e de "desde sempre", o filtro tem **Último mês** (30 dias) e **Último racha**; neste, a aba Racha troca os rankings de temporada por uma leitura da noite (as listas ranqueadas têm a mesma setinha de ordem) — presentes, partidas, gols, minutos de jogo, os times da noite com V/E/D e gols (tocar no time abre a escalação com o mini-badge de patente de cada um, o rodízio de goleiro e **as partidas do time**: resultado, placar, adversários — até o 5v5, quem estava em quadra do outro lado — e a prob. de vitória no apito, D-111; e, discreto sob a contagem, o **resultado realizado × a probabilidade média de vitória no apito** — D-77; o realizado conta **empate como meio**, D-97, porque a chance do Elo já é o placar esperado nessa mesma base), **quem mais ganhou** (vitórias; desempate por menos derrotas — a leitura "quem mais perdeu" é a setinha invertida), artilheiro, quem rendeu acima do esperado, tempo em quadra, menos vazado (mín. 20 min no gol), gols contra e quem subiu/caiu de nível.

**No servidor, a liga vive em partes.** Cada jogador, partida, racha e entrada do log é uma linha própria (payload jsonb de fatos), mais uma linha `live` para o racha em andamento. O app grava só o que mudou (`save_parts`) e recebe só o que mudou desde a versão que conhece (`league_delta`); um gol é ~1 KB subindo e ~1 KB descendo em cada aparelho, independentemente do tamanho do histórico. Nível e estatística nunca vão para o banco.

**Fatos vs. derivados.** `matches` (escalações de largada `startLineups`/`startGks`, trechos, placar, gols com autor/minuto/contra, `events` bruto) e `sessions` são fatos; nível, Elo, forma, gols e contagens em `players` são derivados e `rebuildAll()` os refaz do zero. `log[]` na liga registra toda correção manual (quem, quando, antes → depois) e nunca é apagado. Gol contra: abinha "contra" ao marcar o autor; não conta na artilharia, aparece só na ficha.

**Presença em lote.** Na tela "Quem chegou", segurar um nome e arrastar marca todo mundo por onde o dedo passa (ou desmarca, se o primeiro nome apagou). No computador é clicar e arrastar. O "segurar" existe para não brigar com a rolagem da lista.


**Funciona de verdade, hoje:**

- Múltiplas Ligas isoladas, cada uma com patentes, jogadores, ajustes e histórico próprios
- Escada de 15 degraus com nomes editáveis, histerese e calibração (a proteção pós-promoção foi removida — D-46)
- **Duas patentes por jogador** (linha e goleiro), independentes, com calibração própria
- **Motor por trecho**: cada formação em campo é uma partida, com descarte de trecho curto e peso proporcional
- **Rating 100% invisível em todas as telas**, com opção de esconder até a patente de quem não é admin (o admin vê o Elo cru discreto — D-52)
- Formato 5v5 / 6v6 / 7v7 / 11v11 com sugestão automática de quantidade de times
- Presença, montagem automática equilibrada, troca manual por toque, sorteio aleatório
- Goleiros: fixos por time, rodízio com alternância de lado, improviso no meio da partida
- Partida ao vivo: cronômetro com pausa (vibra e apita quando o tempo bate), gol em um toque (toque duplo não dobra), autor opcional, substituição com trecho próprio, cancelar com confirmação, "chegou agora", desfazer; confirmação em tudo que não tem volta (encerrar racha, apagar partida); dois celulares na mesma partida somam eventos
- Presença ordenada por quem mais aparece, com marcação de goleiro por racha
- Equilíbrio que evita repetir quem já jogou junto, sem abrir mão do equilíbrio
- Vencedor fica, com fila de times, e tela de próxima partida com escalação editável e chance esperada de cada lado
- Contestação, revisão, correção, anulação e recálculo integral
- Ranking agrupado por patente, com escadas separadas de linha e de goleiro, histórico, resumo de fim de racha
- **Destaques dos últimos 30 dias** na tela do racha: top 3 por saldo acima do esperado, artilheiro (quando os gols têm dono), goleiro menos vazado e presença
- **Painel de números**: duelos e parcerias por pessoa (com histórico encontro a encontro), destaques (carrasco, freguês, melhor dupla), quebra ano a ano e rankings do racha no período
- Histórico agrupado por racha, com os rachas do dono do perfil marcados e filtro "só as minhas"
- Contas por usuário e senha; assumir perfil (**Sou eu**) e papéis por conta — as ações de conta do admin valem no servidor (D-62)
- Entrar numa liga por **código com aprovação do admin**; membros, contas e pedidos em Jogadores → Pendências
- **Sequências** (maior série de vitórias, atual e recorde) nos rankings
- Editar nome, "costuma ir ao gol", conta e permissão pela ficha do jogador (rascunho + Salvar); **opiniões sobre o nível** de quem lança, um toque por pessoa, na ficha ou na tela "Minhas opiniões" (D-95)
- **Juntar dois cadastros** da mesma pessoa (admin), reversível pela ficha ("Separar de novo")
- **Corrigir escalação e trocas** de partida encerrada, reescrevendo os trechos (D-61); registro de correções por liga
- Exportar/importar a liga inteira em JSON, com migração automática de ligas gravadas por versões anteriores
- **Tudo no Supabase** (Postgres + Auth + Realtime): sync incremental por versão, só fatos no banco, tempo real entre os celulares do racha, com batida de rede de reserva e prazo de 12 s por pedido
- **Cópia da liga no aparelho** (D-102): abre sem sinal, continua lançando, sobe o que ficou pendente quando a rede volta; a cópia é da conta (some ao sair)

**Ainda não existe (v2):**

- Entrar por **link de convite** ou **convite direto com busca** (seção 7.3) — hoje só o código com aprovação
- **Entrar** sem sinal com a sessão vencida (a cópia local exige estar logado; a sessão renova sozinha enquanto o app está aberto, então isso só acontece depois de dias fechado)
- Recuperação de senha e e-mail de verdade
- Papel de escrita valendo no servidor para a gravação da liga (`save_parts` só exige ser membro — D-62)
- Temporadas com reset parcial
- Gráfico de evolução da patente ao longo do tempo
- Motivo escrito na contestação e aviso para os admins
- Rivalidade por trio/quarteto e exportar o painel de números

## Como o backend está montado (e o que falta)

O app roda contra o **Supabase** (Postgres + Auth + Realtime) com o esquema intermediário de `supabase/schema.sql`: a liga vive em **partes** (`league_players`, `league_matches`, `league_sessions`, `league_live`, `league_log`), o cliente grava só o que mudou (`save_parts`) e recebe só o que mudou (`league_delta`), com trava otimista por versão. O **alvo relacional completo** — trechos, gols e vínculos como linhas próprias, papel de escrita no servidor — está em **[Banco de dados](banco-de-dados.md)**; o resumo:

As **estatísticas não são guardadas**: duelos, parcerias, presenças e aproveitamento são derivados dos trechos na hora de desenhar a tela. Não existe contador para desincronizar — corrigir uma partida de três semanas atrás conserta o painel junto.

**O que fica guardado em cada partida** (e por que importa): placar e resultado, a **lista de trechos** (cada um com escalação dos dois lados, goleiro de cada lado, duração, peso, placar próprio e se conta), gols com autor, **o modo do racha** (que define o K) e o **id da sessão** (que alimenta a contagem de rachas da calibração). Com isso, o histórico é auto-suficiente: dá para recalcular a liga inteira do zero sem depender de nenhuma configuração atual.

```
profiles       (id, handle, nome)
ligas          (id, nome, codigo, entrada_livre, cfg_json)
liga_members   (liga_id, user_id, player_id, papel, status)   ← unique(liga_id,player_id): 1 membro = 1 jogador
liga_invites   (id, liga_id, tipo, token, para_user, player_id, expira_em, status)
join_requests  (id, liga_id, user_id, status)
players        (id, liga_id, nome, rating_linha, rank_linha, rating_gol, rank_gol, costuma_gol, removido)
sessions       (id, liga_id, data, modo, formato)
matches        (id, liga_id, session_id, ordem, modo, formato, placar, resultado, deltas_json, anulada)
stints         (id, match_id, ordem, ini_ms, dur_ms, peso, conta, lineups_json, gks_json, placar, resultado)
goals          (id, match_id, stint_id, player_id NULL, lado, t_ms)
disputes       (id, match_id, user_id, motivo, ts)
audit_log      (id, liga_id, actor, acao, alvo, payload, ts)
```

O vínculo conta↔jogador mora em `liga_members`, e não em `players`: é uma `unique (liga_id, player_id)` que
garante, no banco, que **um membro é um jogador só**. Jogador sem linha em `liga_members` é perfil sem dono.

O motor (`splitStints`, `stintPart`, `computeElo`, `updateRank`, `applyMatch`, `rebuildAll`, `buildTeams`, `pairCounts`, `statsLiga`, `encontros`, `statsAnos`) é todo função pura, sem DOM — hoje roda no cliente (`rebuildAll` a cada delta) e pode subir para o servidor sem reescrita quando fizer sentido. Offline: a liga fica copiada no aparelho (`cacheAgora`/`cacheLoad`, só fatos + a diferença para o que o servidor conhece) e o que não subiu sobe quando a rede volta; a carga inicial pede só o delta desde a cópia (D-102).

**Arquivar, não remover (D-128).** Jogador com histórico só se arquiva (`p.arq`), pela ficha; some do elenco e fica no histórico; reativa pela ficha ou pelo card "Arquivados" dos ajustes. Apagar de vez só sem histórico. Na ficha o nome e a descrição (`bio`) se editam no cabeçalho por quem lança; gol, permissão, arquivar e apagar são só do admin (bloco Admin no fim); "Sou eu" só sem perfil; os ajustes de quem não é admin são só leitura.
