# Requisitos funcionais — Raxa

Produto em [DOCUMENTACAO.md](DOCUMENTACAO.md) · regras de quadra em [REGRAS-DO-RACHA.md](REGRAS-DO-RACHA.md) · modelo de dados da v2 em [BANCO-DE-DADOS.md](BANCO-DE-DADOS.md).

Legenda de status: **✅ v1** implementado no protótipo (`index.html`) · **🔶 v1 parcial** existe, mas simulado localmente · **⬜ v2** planejado.
Prioridade: **P0** o produto não existe sem isso · **P1** importante · **P2** desejável.

---

## RF-01 — Ligas (contexto de racha)

| # | Requisito | Pri | Status |
|---|---|---|---|
| RF-01.1 | Criar uma Liga com nome livre | P0 | ✅ v1 |
| RF-01.2 | Manter várias Ligas independentes no mesmo aparelho/conta, com patentes, jogadores, ajustes e histórico isolados | P0 | ✅ v1 |
| RF-01.3 | Um mesmo jogador pode existir em várias Ligas com patentes independentes, sem qualquer cruzamento de dados entre elas | P0 | ✅ v1 |
| RF-01.4 | Exportar uma Liga inteira em JSON e importá-la em outro aparelho | P1 | ✅ v1 |
| RF-01.5 | Apagar uma Liga, com confirmação explícita | P1 | ✅ v1 |
| RF-01.6 | Entrar em uma Liga por **link de convite** gerado pelo admin, com validade e revogação | P0 | ⬜ v2 |
| RF-01.6b | Entrar em uma Liga digitando o **código** de 6 caracteres: gera pedido para o admin aprovar (ou entrada direta, se a Liga marcar *entrada livre*) | P0 | ⬜ v2 |
| RF-01.6c | O admin **busca a pessoa dentro do app** (por `@usuário` ou nome) e convida direto, podendo já apontar qual perfil é dela | P0 | ⬜ v2 |
| RF-01.6d | Nos três caminhos, ninguém entra sem aceitar o convite e sem o admin ter aberto a porta | P0 | ⬜ v2 |

**Critério de aceite (RF-01.3):** alterar a patente de um jogador na Liga A não produz nenhuma mudança observável na Liga B.

---

## RF-02 — Jogadores

| # | Requisito | Pri | Status |
|---|---|---|---|
| RF-02.1 | Cadastrar jogador com nome, sem sair da tela em que se está | P0 | ✅ v1 |
| RF-02.2 | Definir a patente inicial no cadastro, escolhendo entre as 5 patentes (entra na divisão 2) | P0 | ✅ v1 |
| RF-02.3 | Marcar no cadastro que a pessoa **costuma ir ao gol** — só como sugestão para a presença | P1 | ✅ v1 |
| RF-02.4 | Buscar jogador por nome em lista de até ~50 nomes | P1 | ✅ v1 |
| RF-02.5 | Corrigir a patente de um jogador (admin), escolhendo o degrau ou movendo ±1 divisão | P1 | ✅ v1 |
| RF-02.6 | Remover jogador preservando o histórico das partidas em que ele jogou | P2 | ✅ v1 |
| RF-02.7 | Ver a ficha do jogador: **as duas patentes** (linha e goleiro), partidas, aproveitamento, gols, melhor patente, V/E/D separados por papel, forma recente | P1 | ✅ v1 |
| RF-02.8 | Editar o nome e o "costuma ir ao gol" de quem já está cadastrado | P2 | ⬜ v2 |

**Critério de aceite (RF-02.1):** cadastrar um jogador durante a presença exige nome + 1 toque em patente + "Cadastrar", e o jogador já entra marcado como presente.

---

## RF-03 — Patentes e progressão

| # | Requisito | Pri | Status |
|---|---|---|---|
| RF-03.1 | Toda pessoa tem **duas patentes por Liga** — linha e goleiro — cada uma numa escada de 5 patentes × 3 divisões, independentes entre si | P0 | ✅ v1 |
| RF-03.1c | Quem **nunca jogou** numa das valências não tem patente nela: fica fora daquela escada e a ficha diz "sem patente". Se entrar naquela posição, vale o **nível de entrada padrão** até construir a própria | P0 | ✅ v1 |
| RF-03.1d | O palpite de patente do cadastro vale só para a valência em que a pessoa vai jogar (linha, ou gol se marcada como goleiro) | P0 | ✅ v1 |
| RF-03.1b | A patente que se move é a do **papel que a pessoa fez naquele trecho**: quem estava no gol move a de goleiro, o resto move a de linha | P0 | ✅ v1 |
| RF-03.2 | **O rating numérico nunca é exibido**, para nenhum papel, em nenhuma tela — nem o valor, nem a distância para o corte, nem a variação da partida | P0 | ✅ v1 |
| RF-03.3 | A patente muda **apenas** em função de vitória, empate e derrota, considerando o nível do próprio time e o do adversário | P0 | ✅ v1 |
| RF-03.3b | A unidade de cálculo é o **trecho** (formação em campo), não a partida: toda substituição ou troca de goleiro fecha um trecho, o placar volta a zero e vale o set novo de jogadores | P0 | ✅ v1 |
| RF-03.3c | Trecho encerrado por substituição só conta se durou **pelo menos** o mínimo configurado (padrão 4 min) **ou um terço da partida, o que for menor**; o trecho que termina no apito conta sempre | P0 | ✅ v1 |
| RF-03.3d | O peso de um trecho é a fração da partida que ele ocupou; os trechos que contam somam exatamente uma partida — o peso do descartado é redistribuído entre eles | P0 | ✅ v1 |
| RF-03.3e | O tempo pausado não conta na duração da partida nem na dos trechos | P1 | ✅ v1 |
| RF-03.4 | Gols, assistências e defesas não influenciam a patente | P0 | ✅ v1 |
| RF-03.5 | Promoção exige ultrapassar o corte com margem; rebaixamento exige cair abaixo do corte com margem (histerese). A margem vale em todo degrau — de divisão e de patente | P0 | ✅ v1 |
| RF-03.6 | ~~Proteção pós-promoção~~ — removida em 28/08/2026 (D-46): num racha de 10–15 partidas não se percebia | — | ❌ removido |
| RF-03.7 | Jogador novo fica em calibração até 15 partidas (liga de várias curtas, D-53) ou 3 rachas (liga de partida única), com K dobrado (64) e sem margem | P0 | ✅ v1 |
| RF-03.7b | A calibração vale **por patente**: veterano de linha que vai ao gol pela primeira vez calibra a patente de goleiro do zero | P1 | ✅ v1 |
| RF-03.8 | Quem entra ou sai no meio da partida só é afetado pelos trechos que jogou — o que o time fez com ele no banco não conta | P0 | ✅ v1 |
| RF-03.9 | Goleiro ganha e perde patente como todo mundo, pelo lado que defendeu, **na escada de goleiro**. Não existe interruptor de "goleiro fora do ranking" | P1 | ✅ v1 |
| RF-03.10 | O peso de cada partida sai automaticamente do modo do racha; K (64/32, D-55), margem e calibração são fixos e iguais em toda liga — ninguém configura rating | P1 | ✅ v1 |
| RF-03.11 | Os nomes das 5 patentes são editáveis por Liga | P2 | ✅ v1 |
| RF-03.12 | Mudança de patente **não** é exibida entre partidas: aparece só no resumo do fim do racha | P1 | ✅ v1 |
| RF-03.13 | Temporadas com reset parcial de patente | P2 | ⬜ v2 |
| RF-03.14 | O admin escolhe se as patentes são visíveis para todos (padrão) ou só para ele; escondidas, as estatísticas continuam abertas e o equilíbrio continua funcionando | P1 | 🔶 v1 parcial |

**Critério de aceite (RF-03.3b/3.3c):** uma partida de 8 min com substituição aos 4 vira 2 trechos de peso 0,5; a mesma partida com substituição aos 2 descarta o primeiro trecho e conta só o segundo. Coberto por teste.

**Critério de aceite (RF-03.5/3.6):** um jogador oscilando ±12 pontos internos em volta de um corte não muda de patente nenhuma vez em 12 partidas; e um jogador recém-promovido que despenca não cai antes de N partidas.

---

## RF-04 — Racha (sessão)

| # | Requisito | Pri | Status |
|---|---|---|---|
| RF-04.1 | Iniciar um racha em 1 toque | P0 | ✅ v1 |
| RF-04.2 | Escolher o formato: 5v5, 6v6, 7v7, 11v11 | P0 | ✅ v1 |
| RF-04.2b | Escolher o **modo** do racha: **várias curtas** (time de fora esperando, vencedor fica) ou **partida única** (sempre 2 times fixos com reservas) | P0 | ✅ v1 |
| RF-04.2c | O modo é **de cada racha**, não da liga: o histórico pode misturar rachas curtos e longos | P0 | ✅ v1 |
| RF-04.2d | Cada partida grava o modo do racha em que foi jogada, e o recálculo usa esse valor | P0 | ✅ v1 |
| RF-04.2e | Mudar o modo padrão da liga não altera nenhuma partida já jogada | P0 | ✅ v1 |
| RF-04.3 | Marcar presença tocando nos nomes, com contador visível e presentes no topo | P0 | ✅ v1 |
| RF-04.3b | A lista de jogadores vem ordenada por **quem tem mais presenças em rachas** | P1 | ✅ v1 |
| RF-04.3c | Marcar na presença **quem veio para ser goleiro hoje**, com 1 toque por pessoa, independente do cadastro | P0 | ✅ v1 |
| RF-04.3d | Trocar quem está no gol durante o racha, em partidas específicas | P0 | ✅ v1 |
| RF-04.4 | Adicionar quem chegou atrasado durante o racha, mandando direto para um time, para o rodízio de goleiros ou **para o fim da fila** | P0 | ✅ v1 |
| RF-04.5 | Retomar o racha em andamento após fechar e reabrir o app | P0 | ✅ v1 |
| RF-04.6 | Encerrar o racha com resumo: partidas, artilheiro e mudanças de patente | P1 | ✅ v1 |
| RF-04.7 | Cancelar o racha preservando no histórico as partidas já lançadas | P2 | ✅ v1 |

**Critério de aceite (RF-04.2c/2d/2e):** duas partidas no mesmo histórico, uma de racha curto e outra de racha de partida única, mantêm pesos diferentes depois de um recálculo integral; e alterar o padrão da liga deixa os deltas das partidas antigas idênticos. Coberto por teste.

---

## RF-05 — Montagem de times

| # | Requisito | Pri | Status |
|---|---|---|---|
| RF-05.1 | Sugerir a quantidade de times a partir do formato e da quantidade de presentes | P1 | ✅ v1 |
| RF-05.2 | Forçar 2, 3 ou 4 times — **limitado a quantos times CHEIOS cabem**: o botão que não cabe fica apagado, e nem forçando sai time incompleto | P1 | ✅ v1 |
| RF-05.3 | Montar times equilibrados por nível em 1 toque | P0 | ✅ v1 |
| RF-05.3b | Cada time tem o número de jogadores do formato (N, ou N−1 de linha quando o goleiro reveza) | P0 | ✅ v1 |
| RF-05.3c | Os dois times que entram juntos têm sempre o mesmo número de jogadores — nunca 5x4, nunca 5x3 | P0 | ✅ v1 |
| RF-05.3g | Time que ficou curto (alguém saiu, alguém foi movido) é **completado com quem está de fora** até igualar o outro; só quando não há ninguém de fora os dois entram menores | P0 | ✅ v1 |
| RF-05.3h | O app sugere quem completa (quem menos jogou na noite), mas **o usuário escolhe**: tirar, trocar por outro ou jogar sem completar | P0 | ✅ v1 |
| RF-05.3i | Quem completa joga aquela partida pelo time que o chamou e **volta para o time dele** quando ela acaba | P0 | ✅ v1 |
| RF-05.3j | Quem não cabe num time forma a **fila** (de pessoas, não de times): ao fim da partida quem perdeu sai, a fila entra no lugar e quem sai vai para o fim | P0 | ✅ v1 |
| RF-05.3k | Quando a fila não dá para trocar o time inteiro, **alguns do time que saiu ficam para completar**; sai quem mais jogou na noite | P0 | ✅ v1 |
| RF-05.3l | ~~Girar a fila na mão em 1 toque~~ — removido (D-32): trocar qualquer time na tela da próxima partida cobre o caso | — | ❌ removido |
| RF-05.3d | No racha curto **todo time é cheio** (do tamanho do formato): o app monta quantos times inteiros couberem e quem sobra fica **de fora**, num banco compartilhado. Não existe time menor esperando a vez, e reserva presa a um time só existe na partida única | P0 | ✅ v1 |
| RF-05.3e | Na partida única são sempre 2 times, com todos divididos entre eles: N titulares + reservas | P0 | ✅ v1 |
| RF-05.3f | Time incompleto é sinalizado na tela de times e na partida, com atalho para chamar alguém | P1 | ✅ v1 |
| RF-05.4 | Distribuir goleiros: um por time quando houver quantidade suficiente | P0 | ✅ v1 |
| RF-05.5 | Colocar goleiros em rodízio quando houver menos goleiros que times | P0 | ✅ v1 |
| RF-05.6 | Alternar entre goleiros em rodízio e goleiros fixos nos times, **nos dois sentidos e em um toque**, com o controle sempre visível | P1 | ✅ v1 |
| RF-05.6b | Mandar um jogador selecionado para o rodízio de goleiros | P2 | ✅ v1 |
| RF-05.7 | Trocar jogadores de time arrastando um sobre o outro, ou arrastando para um time, para "fora" ou para o rodízio de goleiros | P0 | ✅ v1 |
| RF-05.7b | Quem está de fora aparece em card próprio, com contador, sempre visível — nunca escondido | P0 | ✅ v1 |
| RF-05.7c | Indicação persistente de quem está selecionado, com cancelar | P1 | ✅ v1 |
| RF-05.7d | O mesmo por toque, para quem preferir (toca em um, toca no outro / toca no time) | P0 | ✅ v1 |
| RF-05.8 | Sortear times ignorando o nível (aleatório puro) | P2 | ✅ v1 |
| RF-05.9 | Mostrar o equilíbrio dos times **sem número**: barra de equilíbrio e veredito textual ("Times equilibrados", "Leve vantagem: Time B") | P0 | ✅ v1 |
| RF-05.10 | Refazer os times no meio do racha | P1 | ✅ v1 |
| RF-05.11 | Evitar juntar de novo quem já jogou junto em outros rachas, **sem prejudicar o equilíbrio** (critério de desempate, margem imperceptível) | P1 | ✅ v1 |
| RF-05.13 | Tocar em **Equilibrar** de novo devolve um arranjo **diferente e igualmente equilibrado** — não o mesmo de sempre | P1 | ✅ v1 |
| RF-05.14 | Quem fica de fora também é equilibrado: a fila é uma fatia que atravessa todos os níveis, nunca os piores do racha | P0 | ✅ v1 |
| RF-05.15 | A variação vem de ruído aplicado **só na montagem**: chance de vitória, barra de equilíbrio e veredito usam o nível real | P0 | ✅ v1 |
| RF-05.12 | O nível usado no equilíbrio é o do papel: goleiro do dia entra pela patente de goleiro | P0 | ✅ v1 |

**Critério de aceite (RF-05.3):** com 16 presentes, a diferença de nível médio entre times fica abaixo de 40 pontos internos em 2, 3 e 4 times, e nenhum jogador some ou duplica.

**Critério de aceite (RF-05.13/5.14/5.15):** 14 montagens seguidas dos mesmos 13 presentes dão pelo menos 4 arranjos distintos, todos com diferença de nível real abaixo de 40; e o nível médio de quem fica de fora fica próximo do nível médio do racha, longe da média dos piores. Coberto por teste.

**Critério de aceite (RF-05.11):** com 10 jogadores de mesmo nível que jogaram 3 rachas nos mesmos times, montar os times de novo reduz a repetição de duplas em relação ao equilíbrio puro, e a diferença de nível continua abaixo de 40. Coberto por teste.

**Critério de aceite (RF-05.3b/3c/3d):** no 5v5, 12 de linha + 2 goleiros ⇒ 3 times de 4 com goleiros revezando e ninguém de fora; 10 de linha + 2 goleiros ⇒ 2 times de 5 (4 + goleiro) e 2 de fora; 13 sem goleiro ⇒ 2 times de 5 e 3 de fora; 8 presentes ⇒ 4v4. Todos cobertos por teste.

**Critério de aceite (RF-05.3j/3k):** com 13 no 5v5 (2 times de 5 e fila de 3), encerrar uma partida faz entrarem os 3 da fila no time que perdeu, ficarem 2 dos que jogaram, e os 3 que saíram irem para o fim da fila. Coberto por teste.

**Critério de aceite (RF-05.3g/3h/3i):** tirando alguém de um time de 5, a partida ainda entra 5v5 com um emprestado de fora; o empréstimo acaba com a partida (o time volta a ter 4); e desligar o completar faz os dois lados entrarem com 4. Coberto por teste.

---

## RF-06 — Partida ao vivo

| # | Requisito | Pri | Status |
|---|---|---|---|
| RF-06.1 | Iniciar a partida em 1 toque, com escalações já prontas: entram os titulares, reservas ficam disponíveis | P0 | ✅ v1 |
| RF-06.1b | O time que está esperando não entra na frente de quem ainda não jogou | P1 | ✅ v1 |
| RF-06.2 | **Encerrar a partida em 1 toque**, gravando o resultado que está no placar; o botão mostra o resultado antes de confirmar | P0 | ✅ v1 |
| RF-06.2b | Nem o 0-0 pergunta: é gravado como empate; encerrar leva direto para a tela de próxima partida, com um aviso curto do placar | P0 | ✅ v1 |
| RF-06.2c | Corrigir/anular resultado fica no **Histórico → Revisar**, fora do fluxo do racha; no racha existe apenas "Desfazer a última" | P1 | ✅ v1 |
| RF-06.3 | Marcar gol em 1 toque no bloco do time | P0 | ✅ v1 |
| RF-06.4 | Registrar o autor do gol de forma opcional e não bloqueante, com opção de pular e desaparecimento automático | P1 | ✅ v1 |
| RF-06.5 | Gols listados com minuto e autor, cada um com botão de remover | P0 | ✅ v1 |
| RF-06.5b | Corrigir ou preencher o autor de um gol já registrado, tocando no nome | P1 | ✅ v1 |
| RF-06.6 | Cronômetro com o alvo configurado na Liga (gols/minutos — o alvo é da Liga, o modo é do racha) e sinal visual quando o alvo é atingido | P1 | ✅ v1 |
| RF-06.7 | Substituir em 2 toques a partir de qualquer ponta: tocando em quem está em quadra ou em quem está no banco | P0 | ✅ v1 |
| RF-06.7b | Escalação, reservas do time e quem está fora visíveis na própria tela da partida, com o time de origem | P0 | ✅ v1 |
| RF-06.7c | As escalações definidas entram por padrão em toda partida, sem reconfirmação | P0 | ✅ v1 |
| RF-06.7d | Trocar titular por reserva do mesmo time apenas inverte os dois, sem desmanchar o time | P0 | ✅ v1 |
| RF-06.8 | Definir/trocar o goleiro de cada lado durante a partida, inclusive improvisando alguém da linha | P0 | ✅ v1 |
| RF-06.9 | O vencedor sai do placar, sem pergunta nem confirmação — empate incluso; sobrepor o resultado só no Histórico → Revisar | P0 | ✅ v1 |
| RF-06.10 | "Vencedor fica" e a fila são **sugestão**: o app propõe o próximo confronto já montado | P0 | ✅ v1 |
| RF-06.10b | Trocar qualquer um dos dois times que vão entrar, em 2 toques, sem obedecer à fila | P0 | ✅ v1 |
| RF-06.10c | Entre partidas, uma **tela de próxima partida** (não um modal) mostra o confronto, a chance de cada lado e as duas escalações | P0 | ✅ v1 |
| RF-06.10d | Editar a escalação dos dois times que vão entrar antes do apito, por toque ou arraste, puxando gente de outro time ou de fora | P0 | ✅ v1 |
| RF-06.11 | Desfazer a última partida inteira, revertendo patentes | P0 | ✅ v1 |
| RF-06.11c | `↶` na barra da partida desfaz o último evento (gol, substituição, pausa) e, sem eventos, a última partida | P1 | ✅ v1 |
| RF-06.11d | "Encerrar racha" **não fica na barra durante a partida**, para não disputar espaço com o "Fim" | P0 | ✅ v1 |
| RF-06.18 | Tirar o último gol de um time em 1 toque, no próprio bloco do placar (`−`) | P1 | ✅ v1 |
| RF-06.11b | Substituir arrastando um nome sobre o outro, com o toque como caminho alternativo | P1 | ✅ v1 |
| RF-06.12 | Lançar partida retroativamente (sem cronômetro): entra como um trecho só, peso 1 — é o que acontece com qualquer partida encerrada com menos de 45 s de relógio | P2 | ✅ v1 |
| RF-06.13 | **Pausar e retomar** a partida em 1 toque; o tempo parado não conta | P1 | ✅ v1 |
| RF-06.14 | **Cancelar** a partida em andamento, com confirmação, descartando gols e tempo | P1 | ✅ v1 |
| RF-06.15 | Empate com 3 ou 4 times: **os dois times saem** e entram os próximos da fila | P1 | ✅ v1 |
| RF-06.16 | Mostrar a **chance esperada de vitória de cada lado**, sem destaque, na tela da partida e na tela de próxima partida; escondida quando as patentes estão fechadas | P2 | ✅ v1 |
| RF-06.17 | Indicar na tela quando a partida está em um trecho novo, com o placar do trecho | P2 | ✅ v1 |

**Critério de aceite (RF-06.2):** do fim do jogo ao lançamento completo com patentes aplicadas não deve haver mais de dois toques nem nenhum campo obrigatório de texto.

---

## RF-07 — Histórico, contestação e correção

| # | Requisito | Pri | Status |
|---|---|---|---|
| RF-07.1 | Listar o histórico **agrupado por racha**: uma linha por noite (data, partidas, gols, contestações) e as partidas só depois de abrir o racha | P0 | ✅ v1 |
| RF-07.1b | Dentro do racha: data, times, placar e resultado de cada partida, com contestar e revisar | P0 | ✅ v1 |
| RF-07.1c | Os rachas em que o dono do perfil jogou vêm marcados na lista, com quantas partidas foram dele | P1 | ✅ v1 |
| RF-07.2 | Qualquer participante pode contestar uma partida, uma vez por pessoa (em v1, identificada pelo nome deste aparelho) | P0 | 🔶 v1 parcial |
| RF-07.3 | Exibir o número de contestações na partida e um aviso no topo do histórico | P0 | ✅ v1 |
| RF-07.4 | Configurar o limite de contestações e o efeito ao atingi-lo: apenas sinalizar ou suspender o efeito da partida | P1 | ✅ v1 |
| RF-07.4b | A revisão mostra a partida inteira: resumo, quem jogou de cada lado (tempo em quadra, papel, gols, +/−, entrou/saiu), linha do tempo (gols, substituições, trocas de goleiro, pausas), trechos com escalação e peso, e efeito no nível | P1 | ✅ v1 |
| RF-07.5 | Admin pode manter, corrigir o resultado, anular ou apagar uma partida | P0 | ✅ v1 |
| RF-07.5b | Admin pode corrigir a **escalação de largada** (quem começou, goleiro, quem era quem) e as **trocas** (editar, apagar, criar) de uma partida encerrada; os trechos são refeitos e a liga recalculada | P1 | ✅ v1 |
| RF-07.6 | Toda correção, anulação ou exclusão recalcula a Liga inteira do zero, sem resíduo | P0 | ✅ v1 |
| RF-07.7 | Partida anulada permanece visível no histórico, marcada e sem efeito nas patentes | P1 | ✅ v1 |
| RF-07.8 | Registrar quem contestou e quando | P1 | 🔶 v1 parcial |
| RF-07.9 | Exigir motivo na contestação e notificar os admins | P2 | ⬜ v2 |

**Critério de aceite (RF-07.6):** anular e reativar uma partida antiga devolve exatamente o mesmo estado de todos os jogadores (rating, patente, partidas, vitórias, gols).

---

## RF-08 — Ranking e estatísticas

| # | Requisito | Pri | Status |
|---|---|---|---|
| RF-08.1 | Ranking agrupado por patente, com a divisão de cada jogador | P0 | ✅ v1 |
| RF-08.1b | Alternar entre o **ranking de linha** e o **ranking de goleiro** em 1 toque | P1 | ✅ v1 |
| RF-08.1c | Com as patentes fechadas, a aba mostra só estatísticas (rachas, partidas, gols) | P1 | ✅ v1 |
| RF-08.2 | Exibir V/E/D, gols e forma recente por jogador | P1 | ✅ v1 |
| RF-08.3 | Marcar visualmente quem ainda está calibrando | P1 | ✅ v1 |
| RF-08.4 | A ordenação do ranking não pode revelar o rating: dentro da mesma divisão, ordena por aproveitamento e nome | P0 | ✅ v1 |
| RF-08.5 | Resumo do racha: partidas, artilheiro e mudanças de patente | P1 | ✅ v1 |
| RF-08.8 | Tela do racha mostra os **destaques dos últimos 30 dias**, e não o topo histórico da liga | P1 | ✅ v1 |
| RF-08.8b | Primeiro destaque: **os melhores do racha** — maior patente entre quem apareceu no período, cada um pela valência que mais jogou, na mesma ordem do ranking | P1 | ✅ v1 |
| RF-08.8c | Cada linha do pódio diz o que cada número é: rachas, partidas e % de vitórias no período | P1 | ✅ v1 |
| RF-08.9 | O destaque é o **saldo acima do esperado** (resultado menos a chance do confronto, por trecho), com piso de **2 rachas ou 15 partidas** no período (D-69) — não aproveitamento nem vitória pura | P1 | ✅ v1 |
| RF-08.10 | **Artilheiro do período** só aparece se metade ou mais dos gols tiverem autor; senão o card diz quantos ficaram sem dono | P1 | ✅ v1 |
| RF-08.11 | **Goleiro menos vazado**: gols sofridos por partida nos trechos em que a pessoa estava no gol | P1 | ✅ v1 |
| RF-08.12 | Com as patentes fechadas, o destaque cai para vitórias no período | P1 | ✅ v1 |
| RF-08.6 | Confronto direto e "melhor dupla" | P1 | ✅ v1 (ver RF-11) |
| RF-08.7 | Gráfico de evolução de patente ao longo do tempo | P2 | ⬜ v2 |

---

## RF-09 — Contas, perfis e permissões

| # | Requisito | Pri | Status |
|---|---|---|---|
| RF-09.1 | Perfis nascem "sem dono" e acumulam patente e estatística normalmente | P0 | ✅ v1 |
| RF-09.2 | Um usuário pode assumir um perfil sem dono dentro de uma Liga, herdando todo o histórico anterior | P0 | 🔶 v1 parcial |
| RF-09.2b | **Um membro corresponde a exatamente um jogador** na Liga: nem conta com dois perfis, nem perfil de duas contas — garantido no banco, não só na tela | P0 | ⬜ v2 |
| RF-09.3 | Um usuário acompanha, em um só lugar, suas patentes em todas as Ligas de que participa | P1 | ⬜ v2 |
| RF-09.4 | Admin pode vincular e desvincular um perfil de uma conta; desvinculado, o perfil volta a ser "sem dono" | P1 | 🔶 v1 parcial |
| RF-09.5 | Papéis: Admin, Editor, Lançador e Jogador, atribuíveis pelo admin | P0 | 🔶 v1 parcial |
| RF-09.6 | Novo membro entra como Lançador por padrão | P1 | 🔶 v1 parcial |
| RF-09.7 | As permissões são aplicadas de fato no servidor | P0 | ⬜ v2 |
| RF-09.8 | O admin **remove um membro** sem apagar o jogador: histórico, patente e estatística ficam; só o acesso sai | P0 | ⬜ v2 |
| RF-09.9 | O admin revoga convite, aprova ou recusa pedido de entrada, e vê a lista de convites e pedidos pendentes | P0 | ⬜ v2 |
| RF-09.10 | Uma Liga nunca fica sem admin: passar o papel adiante é obrigatório antes de sair ou rebaixar o último admin | P1 | ⬜ v2 |
| RF-09.11 | Toda ação sobre membros fica registrada: quem fez, em quem, quando | P2 | ⬜ v2 |

**Modelo de dados:** o esquema que sustenta membros, convites e papéis está em [BANCO-DE-DADOS.md](BANCO-DE-DADOS.md) — o vínculo 1:1 de RF-09.2b é uma `unique (liga_id, player_id)` em `liga_members`.

**Nota:** em v1 conta, papéis e reivindicação existem no modelo de dados e na interface, mas valem apenas no aparelho — não há autenticação. O único papel de fato aplicado hoje é o de admin, na visibilidade das patentes (RF-03.14); os demais só viram regra com o backend (RF-09.7). Pelo mesmo motivo, "uma contestação por pessoa" (RF-07.2) hoje é "uma por nome de aparelho".

---

## RF-10 — Sincronização e dados

| # | Requisito | Pri | Status |
|---|---|---|---|
| RF-10.1 | Os dados persistem no servidor (Postgres, por conta); no aparelho fica só a preferência de tela | P0 | ✅ v1 |
| RF-10.2 | O app funciona integralmente sem internet | P0 | ⬜ v2 — a versão com backend precisa de rede (DEPLOY.md) |
| RF-10.3 | Sincronização entre aparelhos, com vários lançadores no mesmo racha (delta por versão + tempo real) | P0 | ✅ v1 |
| RF-10.4 | Fila de sincronização offline com resolução determinística de conflitos | P1 | ⬜ v2 |
| RF-10.5 | Migração automática de dados salvos por versões anteriores do app | P1 | ✅ v1 |

---

## RF-11 — Números, duelos e parcerias

A unidade de todas as contas desta seção é o **trecho**: dois jogadores se "enfrentaram" quando estiveram em quadra ao mesmo tempo, em lados opostos — em qualquer formato (1v1, 5v5, 3v2).

| # | Requisito | Pri | Status |
|---|---|---|---|
| RF-11.1 | Painel de números de uma pessoa: rachas, partidas, aproveitamento (pontos: V=3, E=1 — D-69), vitórias, gols e partidas no gol | P1 | ✅ v1 |
| RF-11.2 | Filtrar o painel por período: **ano atual** ou **desde sempre** | P1 | ✅ v1 |
| RF-11.3 | Quebra **ano a ano** (rachas, partidas, gols, aproveitamento por temporada) | P2 | ✅ v1 |
| RF-11.4 | **Duelos**: quantas vezes enfrentou cada pessoa, com V/E/D e aproveitamento | P1 | ✅ v1 |
| RF-11.5 | Histórico de um duelo, encontro a encontro: data, placar, formato (5v5, 3v2…) e resultado | P1 | ✅ v1 |
| RF-11.6 | **Parcerias**: quantas vezes jogou do lado de cada pessoa, com V/E/D, e o histórico ao toque | P1 | ✅ v1 |
| RF-11.7 | Destaques: **maior carrasco**, **freguês**, **mais jogou junto** e **melhor dupla** | P1 | ✅ v1 |
| RF-11.8 | Rankings do racha no período: mais presenças, mais vitórias, maior aproveitamento e artilharia | P1 | ✅ v1 |
| RF-11.9 | O ranking de aproveitamento exige um mínimo de partidas no período (10), escrito na tela | P1 | ✅ v1 |
| RF-11.9b | Os destaques pessoais (carrasco, freguês, melhor dupla) têm piso próprio: 10 ou 10% das partidas da pessoa, o que for menor, nunca abaixo de 3 | P1 | ✅ v1 |
| RF-11.10 | Ver os números de qualquer jogador da liga, não só os próprios | P2 | ✅ v1 |
| RF-11.11 | Substituição é respeitada: só contam os trechos em que a pessoa estava em quadra | P0 | ✅ v1 |
| RF-11.12 | Nenhuma estatística agregada é gravada — todas são derivadas do histórico a cada tela. A partida guarda só a saída do próprio motor (deltas e acima do esperado), refeita a cada recálculo | P0 | ✅ v1 |
| RF-11.13 | Marcar no histórico as partidas de quem assumiu o perfil no aparelho, com o resultado pelo lado dele | P1 | ✅ v1 |
| RF-11.14 | Filtrar o histórico por **só as minhas** | P2 | ✅ v1 |
| RF-11.15 | Sequências (maior série de vitórias, atual e recorde) — ✅ v1; rivalidade por trio/quarteto e exportar o painel — ⬜ v2 | P2 | ◐ parcial |

**Critério de aceite (RF-11.4/11.5):** a soma de V/E/D de um duelo é igual ao número de confrontos, e o histórico do duelo tem exatamente essa quantidade de linhas. Coberto por teste.

**Critério de aceite (RF-11.11):** numa partida de 10 min com substituição aos 5, quem saiu tem 1 confronto contra cada adversário e quem entrou também — e os dois nunca aparecem como parceiros. Coberto por teste.
