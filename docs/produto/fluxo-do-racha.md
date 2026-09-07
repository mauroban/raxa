# Fluxo de uso — antes, times, durante, depois

> Parte da documentação do Raxa — índice em [docs/README.md](../README.md).


## 1. Antes — 30 segundos

**Formato.** Um toque: `5v5` (futsal), `6v6` (society), `7v7` (fut7), `11v11` (campo). O formato define quantos cabem por time e é usado para sugerir a quantidade de times.

**Como vai ser hoje.** Dois modelos de racha, um toque:

| Modo | O que muda |
|---|---|
| **Várias curtas** *(padrão)* | alvo de 2 gols ou 7 min, vencedor fica em quadra (empate: com 4 times os dois saem; com 3, fica o que entrou por último — D-39), cada partida pesa pouco no rating — **10 a 15 partidas por noite** |
| **Partida única** | **sempre 2 times**, fixos, com titulares e reservas; uma partida longa (50 min, sem alvo de gols); substituição é a operação principal; cada partida pesa muito mais |

Os dois convivem na mesma Liga: o modo é do racha, não do grupo.

**Presença.** Grade com todos os jogadores da Liga, em **duas colunas mesmo no celular estreito** — chips compactos (42px, nome em 13px com reticências) para o cenário real de "50 cadastrados, achar os 18 de hoje" caber na tela (D-88). A busca tem um **✕** que limpa o campo num toque (achou um, limpa, procura o próximo). Toca no nome de quem chegou — e no arrasto (segurar e pintar), quando o dedo chega à borda da tela ela **rola sozinha**, marcando quem passa por baixo.  Uma Liga pode ter 50 cadastrados e 14 presentes, e o contador fica grande no topo. Os presentes sobem para o começo da lista **quando a tela é redesenhada** — marcar presença não reordena nada embaixo do seu dedo, senão marcar 14 pessoas seguidas viraria uma caça ao nome que pulou de lugar.

- **A lista vem ordenada por quem mais aparece nos rachas.** Quem joga toda semana está sempre nas primeiras linhas; quem apareceu uma vez em março fica no fim. É o que faz achar a galera de sempre sem usar a busca.
- **Ao lado de cada nome tem um 🧤:** toque nele para dizer que essa pessoa **veio para ser goleiro hoje**. Quem tem o hábito já entra marcado, e dá para mudar a qualquer momento — inclusive no meio do racha, em partidas específicas.
- **O badge do chip é o nível do papel de hoje** (D-81), no formato compacto de cor + riscos (sem o nome da patente — com 50 nomes em duas colunas, o nome do nível comia o do jogador; D-88): com o 🧤 aceso aparece a patente de goleiro; apagado, a de linha. Troca na hora ao tocar no 🧤. Quem não tem nível naquele papel fica sem badge. Antes de marcar presença vale o **padrão da pessoa**: quem costuma ir ao gol mostra a de goleiro, o resto a de linha (sem nível no papel de costume, mostra o outro).
- Busca instantânea e **"+ Novo jogador"** que cadastra sem sair da tela (nome + descrição opcional — apelido, amigo de quem — + patente + costuma ir ao gol).

## 2. Times — 1 toque

O app calcula sozinho quantos times **inteiros** cabem e mostra todos na montagem: no formato NvN cada time é N−1 de linha mais o goleiro (ou N de linha, sem goleiro marcado). **12 de linha + 2 goleiros em 5v5 → 3 times de 4 + goleiro nos dois primeiros.** Dá para forçar 2, 3 ou 4 times, dentro do que cabe cheio. **Ao começar o racha, os dois primeiros times são os lados da quadra e os outros viram a fila, na ordem** — uma fila só, de pessoas (D-129).

**"Equilibrar"** faz:
1. distribui goleiros (um por time) ou separa o rodízio — cada goleiro entra na conta pela **patente de goleiro** dele, e os de linha pela de linha;
2. **escolhe quem fica de fora**, quando sobra gente: uma fatia que atravessa todos os níveis, um sorteado de cada faixa. A fila tem que ser tão equilibrada quanto os times — jogar os piores todos para fora seria o pior jeito de montar um racha;
3. **sorteia o draft com um ruído pequeno no nível de cada um** e monta pelo guloso: o melhor disponível cai sempre no time mais fraco que ainda tem vaga;
4. algumas centenas de trocas 1:1 buscando minimizar a diferença de nível entre os times — e essa parte usa o **nível de verdade**, sem ruído nenhum, preservando tamanho e goleiros;
5. **desmancha panelinha**: uma segunda rodada de trocas que separa quem já jogou junto em outros rachas — mas **só aceita trocas que não estragam o equilíbrio** (margem de 8 pontos internos, invisível em quadra). A prioridade é o equilíbrio; a repetição é critério de desempate.

**Por que o ruído.** Com gente parelha não existe *um* arranjo equilibrado — existem dezenas. Sem ruído, tocar em "Equilibrar" de novo devolveria exatamente os mesmos times, e a única saída seria o sorteio no dádo. Com ele, cada toque dá um arranjo **diferente e igualmente equilibrado**: nos testes, 14 montagens seguidas dão 13 ou 14 times distintos, todos com menos de 10 pontos internos de diferença.

O ruído vive **só dentro do montador**. A chance de vitória do confronto, a barra de equilíbrio e o veredito ("Times equilibrados") usam sempre o nível real — o que você lê na tela não é chutado.

Por que isso importa: se os mesmos quatro caem sempre no mesmo time, o Elo deles vira o Elo *do time* e ninguém descobre o nível individual de ninguém. Misturar as duplas é o que faz a patente convergir para a pessoa.

O resultado aparece **sem número nenhum**: uma barra de equilíbrio e o veredito ("Times equilibrados" / "Leve vantagem: Time B").

**Quantos por lado.** No formato NvN cada lado entra com N: N−1 de linha e o goleiro. A partir daí:

- **lado é sempre cheio.** No 5v5 se joga 5 contra 5. Se a fila tem gente, um lado curto é completado na hora pela frente dela; só se joga com menos quando não há ninguém na fila — e aí os dois lados entram menores e iguais, com aviso;
- **quem não está nos dois lados é a fila**, uma só, de pessoas, na ordem de quem está fora há mais tempo. Ela nasce dos times da montagem (o Time C inteiro, depois o D, depois quem ficou de fora), então o grupo que entra primeiro é um time parelho — e, se ninguém improvisar, os times de sempre entram e saem intactos a noite toda;
- na **partida única** são **sempre 2 times**: todo mundo dividido entre eles, N em quadra e o resto como reserva do próprio time — o único lugar onde existe reserva de time.

| Presentes (formato 5v5) | O que o app monta |
|---|---|
| 10 de linha + 2 goleiros | dois lados de 4 + goleiro, fila de 2 |
| 12 de linha + 2 goleiros | montagem: 3 times, A e B com goleiro e C com 4 de linha; no racha: dois lados de 4 + goleiro, fila de 4 (o Time C, que entra com o goleiro do lado) |
| 13 de linha + 2 goleiros | dois lados de 4 + goleiro, fila de 5 |
| 12 de linha + 3 goleiros | 3 times de 4 + goleiro; o goleiro sai e entra com o time |
| 13 sem goleiro marcado | dois lados de 5, fila de 3 |
| 8 pessoas | 4v4 — único caso em que se joga com menos, e a tela avisa |
| Partida única, 10 de linha + 2 goleiros | 2 times de 6: 5 em quadra + 1 reserva cada |

**A roda.** Ao fim de cada partida: **quem ganhou fica; do lado que perdeu sai quem está há mais tempo em quadra, tantos quantos a fila puder repor; entra quem está há mais tempo fora; quem saiu vai para o fim da fila.** O goleiro do lado só roda se há goleiro esperando na fila. Empate: a fila repõe os dois lados inteiros → os dois saem; senão fica o lado que está há menos tempo em quadra e o outro roda o que a fila repuser; sem ninguém na fila, jogam de novo. O ciclo inteiro está em [Regras do racha](regras-do-racha.md).

**Lado curto.** Alguém foi embora, alguém saiu para a fila: a frente da fila entra no lugar **na hora**, com aviso e desfazer. Não há empréstimo — quem entra, entra, e o rating enxerga isso naturalmente, porque a unidade é o trecho. Sem ninguém na fila, a **vaga tracejada fica à vista** ("＋ vaga · entra o próximo"): um toque nela põe o próximo da fila; um toque num nome e depois nela põe quem você escolher.

**Refazer times** no meio do racha começa uma rodada nova de verdade: lados e fila remontados, sem "🧤 fica" nem resumo da partida anterior (D-122).

**Mexer nos times é a operação mais frequente depois da presença**, então ela é a mais visível da tela:

- todos os nomes ficam em botões grandes, e **quem está de fora tem card próprio com contador** — nunca escondido; na montagem os times ficam **lado a lado, em duas colunas, um nome por linha** (D-98), para todos caberem na tela do celular sem nome quebrando;
- **arraste um nome sobre o outro para trocar de lugar**, ou arraste para dentro de um time, para o card "fora" ou para o card de goleiros — no celular, segure um instante antes de arrastar;
- quem preferir tocar: toca em um jogador e em outro para trocar; toca no espaço de um time (ou no card "fora") para mover;
- quem está selecionado fica marcado no próprio nome (tocar nele de novo desmarca) — sem faixa de aviso (D-101);
- "Equilibrar" refaz tudo, 🎲 sorteia ignorando o nível, e os botões 2/3/4 times remontam na hora; quem ficou de fora aparece numerado, na ordem em que vai entrar depois dos times.

## 3. Durante — 1 toque por partida

Cronômetro grande, dois blocos coloridos e os slots de goleiro:

- **Tocar no bloco do time = +1 gol.** Aparece uma tirinha logo abaixo do placar com os nomes daquele time para marcar o autor — toca ou ignora, ela some sozinha em 10 s. **Nunca bloqueia.** Enquanto houver **gol sem autor**, um aviso discreto fica abaixo do placar ("⚠️ 1 gol sem autor — toque para marcar") e abre a escolha do autor (D-101).
- **Os gols ficam listados abaixo do placar**, com minuto e autor: `3'12 — Rodrigo ✕`. Toque no nome para corrigir o autor (ou colocar um que você tinha pulado), e no **✕** para apagar aquele gol específico. É mais direto que um "desfazer" cego, porque você vê exatamente o que está removendo.
- O cronômetro mostra o alvo configurado na Liga ("2 gols ou 7 min") e pisca quando bate. Quando o **tempo** bate, o celular também **vibra e apita**, uma vez por partida: a tela está no chão da quadra e ninguém está olhando para ela. O alvo de gols não apita — é um toque da própria pessoa. O **alvo** é a única coisa que continua sendo da Liga; o **modo** (curtas ou única) é de cada racha.
- **Encerrar é um toque só, e o botão já diz o resultado**: `✓ Fim · Time A 2-1`. Ele grava exatamente o que está no placar e **não pergunta nada** — nem no 0-0, que é gravado como empate. Ninguém precisa tocar no time que venceu: os gols já disseram.
- **Fim sem querer tem volta, e ela fica à vista.** A tela seguinte abre com um cartão fixo no topo: o **placar registrado** e o botão **↩ Voltar a partida**, que ficam ali até a próxima começar (D-129) — nada de aviso que some em 7 s. Voltar apaga o registro e devolve a partida ao relógio exatamente como estava — gols, escalações, lados, fila e goleiros voltam ao lugar, e o tempo parado entre o Fim e a volta entra como pausa (o relógio não conta o intervalo). É diferente do "↶ Desfazer a última", que apaga a partida de vez, sem devolvê-la ao relógio. No mesmo cartão, a linha "Saem X, Y → fim da fila · Entram Z, W" diz o que a roda fez.
- **Pausar e cancelar** ficam no topo, como ícones ao lado do relógio: `⏸` congela o relógio (bola na rua, discussão, chuva) e o tempo parado não conta para nada — nem para a duração dos trechos. `✕` joga fora a partida inteira, e **pede confirmação** antes, porque não tem volta. Cancelar devolve o rodízio de goleiros a como estava antes da largada e deixa o **mesmo confronto** sugerido — cancelar quase sempre é "recomeça essa".
- **A barra de baixo tem duas coisas e só duas**: `↶` (desfaz o último gol, troca ou pausa — e, se não houver nada na partida, oferece apagar a partida anterior, **perguntando antes** com o placar dela: um ↶ por reflexo aos 10 s da partida nova não pode apagar a anterior em silêncio) e `✓ Fim · placar`. **"Encerrar racha" não mora aqui**: com o próximo time entrando, um toque errado do lado do "Fim" não pode acabar com a noite. Ele fica na tela entre partidas.
- **O placar é o maior elemento da tela** e ocupa a metade de baixo, no alcance do polegar: tocar no bloco do time é gol, e o `−` no canto tira o último gol daquele lado sem precisar rolar até a lista. O `−` fica numa **zona morta**: tocar perto dele, mas fora, não faz nada (antes virava gol — o contrário da intenção). E **toque duplo não é dois gols**: o segundo toque em menos de 0,6 s é ignorado.
- **A chance de vitória de cada lado** aparece embaixo do placar, em letra pequena: `52% de chance`. É a expectativa do Elo para aquele confronto, atualizada conforme entra e sai gente. Fala do **confronto**, nunca de uma pessoa — e some junto com as patentes quando a liga escolhe deixá-las só para o admin.
- Patentes aplicadas na hora, **trecho por trecho**: quem entrou no meio leva só o que aconteceu depois que entrou. Mas **entre uma partida e outra o app não fala de patente**: encerrar leva direto para a tela da próxima partida, com um aviso curto do placar registrado. Quem subiu e quem caiu aparece **no fim do racha** (seção 4.4) — no meio do jogo isso vira assunto, e assunto atrasa a próxima bola.
- Cada partida do histórico mostra a **chance de cada lado no apito**, colada à esquerda do placar (até o 5v5, o % de cada time na linha dele; acima, `62% × 38%` ao lado do placar único), calculada com o nível que cada um tinha **naquele momento** — é % de confronto, a mesma da pré-partida, e some junto com as patentes quando a liga as fecha (D-75).
- **Racha rolando aparece em todo lugar** (D-100): um selo vermelho pulsando "● ao vivo" na aba Jogos (na linha do racha de hoje e dentro dele), na lista de ligas ("montando" enquanto ainda é presença/times), e um ponto vermelho na aba Racha quando você está em outra aba.
- No histórico (aba **Jogos**), as partidas ficam **agrupadas por racha**: uma linha por noite com data, quantas partidas, quantos gols e as contestações — e as partidas aparecem depois de tocar no racha. Uma noite de 12 partidas é uma linha, não doze.
- **Até o 5v5, a partida é identificada por quem jogou, não pela cor do colete**: cada lado aparece como a lista dos primeiros nomes da escalação de largada, com os gols daquele lado ao lado, e o nome do time fica no "venceu ..." da linha de baixo. A fonte é menor para caber; se ainda não couber, o nome quebra para a linha seguinte — nome cortado no meio seria pior. Em ligas maiores (7v7, 11v11) a lista não cabe e vale o nome do time, com o placar no formato `2 - 1`.
- Se o resultado saiu errado: **"Desfazer a última"** no bloco de partidas de hoje resolve, depois de confirmar com o placar (apagar não tem volta, e o botão mora ao lado do "Voltar a partida", que tem); correção fina (mudar o vencedor, anular, apagar) fica no **Histórico → Revisar**, onde dá para olhar com calma depois.
- **Empate: com 4 times os dois saem; com 3, um fica — o que entrou por último** (o que já estava sai, D-39). Não dá para o "vencedor fica" decidir sozinho quando ninguém venceu; com 4 times deixar os dois faria a fila nunca andar, e com 3 tirar os dois esvaziaria a quadra. Com 2 times, empate não muda nada — eles jogam de novo.
- **Entre uma partida e outra existe uma tela inteira: a próxima partida.** Não é um modal que some — é a tela padrão do racha enquanto nada está rolando (D-129), e ela mostra, nesta ordem:
  - **o placar registrado e o ↩ Voltar a partida**, num cartão fixo no topo até a próxima começar, com a linha "Saem X, Y → fim da fila · Entram Z, W";
  - **os dois lados que vão entrar**, com a chance de cada um junto do nome (`Time A (52%)`), "fica" sob o lado que ficou e a etiqueta **entrou** em quem acabou de entrar; editáveis ali mesmo, por toque ou arraste;
  - **a fila, numerada**, com o risco "entram no próximo" separando quem entra no próximo giro de quem espera mais um ("depois"); o goleiro que espera aparece com o 🧤, junto do time dele. O card não tem título: o risco "entram no próximo" já diz o que é. A partida ao vivo mostra a mesma fila, com o mesmo corte;
  - `＋ Chegou`, `🚑 Foi embora` e `Refazer times`.
  A tela em repouso não explica nada: a dica só aparece com um nome marcado, dizendo o próximo passo, e leva o **↶ desfazer** de qualquer mexida na mão.
- **Quem entra é sugestão, não regra.** O app sugere seguindo a roda — e quem venceu continua do mesmo lado da quadra em que jogou (D-71). Mas você decide: qualquer nome troca de lugar em dois toques, inclusive repetir quem acabou de sair. Só depois de conferir tudo é que você toca em **▶ Começar partida**.
- **Substituição: toque ou arraste — e ela vale para o lado (D-129).** Quem saiu vai para o fim da fila; quem entrou é do lado: se o lado ganha, fica; se perde e tem que sair, volta para o lugar que tinha na fila, sem perder a vez. O `↶` desfaz lado e fila junto. Arraste o nome de quem está fora sobre quem está em quadra e a troca acontece (no celular: segure o nome por um instante e arraste; no computador, arraste direto). Ou toque: o primeiro toque **marca** o nome (em quadra ou fora), quem pode ser o par dele ganha um tracejado verde e a dica abaixo da escalação diz o próximo passo ("Sai Fulano — toque em quem entra" / "Fulano entra — toque em quem sai"); o segundo toque, no par, faz a troca. Tocar no mesmo nome desmarca; tocar em outro do mesmo lado só move a marca. Não há folha no meio: escalação e quem está fora ficam na tela o tempo todo (D-103). Segurar um nome e soltar sem arrastar vale como toque. Trocar titular por reserva do mesmo time só inverte os dois.
- **O 🧤 é um slot como os outros (D-117).** Não tem folha de goleiro: o slot do gol entra na mesma gramática de toque/arraste, e uma **vaga** de linha (tracejada, "＋ vaga") também. Os pares que resolvem:
  - **alguém de fora → 🧤**: entra no gol; quem estava no gol sai de quadra. É o caso mais comum (o goleiro do rodízio que estava descansando, ou qualquer um da fila). Quem está descansando no rodízio aparece entre os de fora, no grupo **🧤 Rodízio**, e entra por toque como todo mundo — no gol ou na linha;
  - **alguém de fora → 🧤 vazio**: entra no gol sem ninguém sair;
  - **alguém de fora → vaga**: entra na linha sem ninguém sair;
  - **de linha ⇄ 🧤 do mesmo lado**: trocam de papel — um vai para o gol e o goleiro volta para a linha; **ninguém sai e o time não fica com um a menos**;
  - **de linha → 🧤 vazio** (o goleiro foi embora ou nunca teve): vai para o gol e a **vaga da linha já fica marcada** — o próximo toque, em quem está fora, fecha o time;
  - **🧤 → vaga do mesmo lado**: o goleiro vai para a linha e o gol fica vazio;
  - **🧤 ⇄ 🧤 do outro lado**: os dois **trocam de lugar por inteiro** — cada um passa para o gol e para a escalação do lado novo, inclusive na lista de autor do gol e na conta dos trechos (D-47).
  A dica abaixo da escalação diz o que a marca pede ("Fulano sai do gol — toque em quem vai para o gol", "Gol vazio — toque em quem vai para o gol", "Vaga na linha — toque em quem entra"). Quem entra no lugar do goleiro **é o goleiro**, venha do rodízio ou não. `↶` desfaz qualquer um desses lances inteiro.
- **Na pré-partida vale a mesma gramática (D-123, D-129)** — sem folha de goleiro: toque ou arraste, com o 🧤, o gol vazio e a vaga como slots, e o tracejado verde mostrando o par. O que muda é que ali não há partida rodando, então o toque mexe no **estado da rodada**:
  - **nome ⇄ nome** (em quadra, na fila, entre os dois lados): **trocam de lugar de vez** — na fila, quem troca assume a **posição** do outro;
  - **nome em quadra → fila** (arrastar até o card, ou o link "sai para a fila, entra Fulano" na dica): vai para o fim da fila e a frente da fila entra no lugar na hora;
  - **de fora → vaga**: entra de vez; **vaga tocada sem marca**: entra o próximo da fila;
  - **de fora → 🧤** com goleiro fixo: entra no lado no lugar do goleiro (ganha o 🧤 do dia) e o antigo vai para a fila com o 🧤; com um goleiro só (rodízio) é o goleiro **só desta partida**, e o do rodízio descansa na fila, de onde volta com um toque;
  - **de linha ⇄ 🧤 do mesmo lado**: trocam de papel nesta partida. Com rodízio, quem improvisa deixa a **vaga de linha** e a frente da fila entra nela na hora (D-122);
  - **🧤 ⇄ 🧤 entre lados**: trocam de gol (com goleiro fixo, trocam de lado); **🧤 → vaga do mesmo lado**: o goleiro joga na linha e o gol fica vazio.
  A dica diz o próximo passo e, com o 🧤 marcado, leva a **"outras opções"** (a folha antiga: sem goleiro definido, voltar à sugestão).
- **Toda troca fecha um trecho** e a tela avisa em letra pequena: `Trecho 2 desde a última troca · 1-0 em 3'20`. O placar do trecho novo é o que vale para quem entrou (seção 3.4).
- **"Chegou"** (o atrasado): marca presença e vai para o **fim da fila** — ou, com "🧤 Veio para o gol", espera na fila com o 🧤 e entra no gol de quem perder (D-122/D-129). Com um goleiro só no racha, entra no rodízio.
- **"Foi embora"** (toque no botão com o nome marcado, ou **arraste o nome até ele** — a confirmação é a mesma): quem já jogou hoje (ou está em quadra) sai contando presença (D-49). Quem **ainda não jogou** ganha a escolha: *🚑 Foi embora — esteve no racha* (conta presença) ou *✕ Marquei errado — não veio* (sai sem contar). Na pré-partida, **a frente da fila entra na vaga na hora** (o aviso diz quem) e o ↶ desfazer devolve tudo. Quem estava **em quadra** sai da partida sem ninguém no lugar, e o `↶` desfaz a saída **inteira**: volta à escalação na mesma posição, à presença, ao lado, à fila e ao 🧤 do dia (D-122). Se a pessoa era o **goleiro escolhido na mão** para a próxima partida, a escolha cai e vale de novo a sugestão do app.
- **Dois celulares na mesma partida.** O racha em andamento é um bloco só no servidor; quando os dois gravam quase juntos, o que chegou depois recebe o estado do outro. Se os dois estão na **mesma partida** (mesmo apito), os eventos se **somam**: gol de um e gol do outro ficam os dois, placar e escalação são refeitos a partir da largada, e autor marcado só aqui vai junto. Se os dois marcaram gol **do mesmo time com menos de 8 s de diferença**, é o mesmo gol visto de dois lugares: conta **um só** (com o autor, se um dos dois marcou) e o aviso diz "um gol foi marcado nos dois celulares: contei um só — se foram gols diferentes, toque de novo". A mesma substituição ou o mesmo goleiro lançados nos dois (em menos de 60 s) também viram um lance só, e uma troca repetida nunca duplica ninguém em quadra (D-104). Se o outro celular já encerrou a partida, vale o dele: o gol atrasado daqui se perde e o aviso diz exatamente isso ("1 gol lançado aqui não entrou: a partida já tinha sido encerrada no outro celular"). Partida **começada aqui sem sinal** não some quando o outro celular só mexeu na presença enquanto isso: ela fica, com os gols, por cima do que veio de lá (D-102). Fora da partida (presença, times) continua valendo o que chegou por último.
- **Sinal ruim na quadra.** A liga inteira fica **guardada no aparelho** (só fatos, como no servidor) a cada mudança. Sem sinal, o gol entra na tela, o canto de baixo diz *"sem conexão · guardado no aparelho"*, e tudo sobe quando a rede volta — inclusive se o navegador matou a aba no meio e o app foi reaberto ainda sem sinal: abre com a cópia, continua lançando, sincroniza depois. Quem só está olhando também vê *"sem conexão"* quando o aparelho cai, para saber que a tela pode estar velha. Nenhum pedido ao servidor fica pendurado mais de 12 s. E, além do aviso em tempo real, a liga aberta é conferida por conta própria a cada 5 s com o racha ao vivo (60 s fora dele) — o celular que dormiu no bolso não fica com o placar velho (D-102).
- **Sem sinal há mais de 20 s: só leitura.** Consistência vale mais que continuar lançando às cegas (D-104). Quando o app **constata** que está sem sinal (pedido que falhou, prazo estourado, o aparelho avisou que caiu) e o último contato bom passou de 20 s, os botões de lançar apagam, o canto de baixo diz *"sem sinal · só leitura"* e qualquer toque responde "Sem sinal há 35 s: só leitura até a conexão voltar, para o placar não divergir do outro celular". O que foi lançado dentro dos 20 s fica guardado e sobe. Silêncio não trava (quem está com rede e parado continua normal); a batida de 5 s é o que descobre a queda. Volta sozinho no primeiro contato bom. É a régua comum de app com interação ao vivo: batida a cada poucos segundos, "caiu" depois de 3–4 batidas perdidas.
- **"Desfazer a última"** fica no bloco de partidas de hoje e reverte a partida inteira, patentes incluídas.

## 4. Depois — o resumo

Dá para **cancelar o racha** em vez de encerrar: as partidas já lançadas continuam no histórico e valendo, só a sessão some. Encerrar e cancelar **perguntam antes**: encerrar não tem volta e o botão fica ao lado do "Começar partida"; a pergunta diz quantas partidas foram registradas e, se houver partida rolando, que ela será descartada.

Ao encerrar, o **resumo da noite** (D-99): data e tempo de bola rolando; partidas, gols, pessoas e minutos; **os times da noite** (nomes até o 5v5, V/E/D com vitórias em verde e derrotas em vermelho, gols marcados e sofridos, e o realizado × esperado quando os níveis estão abertos); **artilheiros** (top 3); **quem mais ganhou** (top 3, com E/D e aproveitamento); e **quem subiu** (seta verde) e **quem caiu** (seta vermelha) de nível, cada um com o badge de onde saiu → onde chegou. É o único momento em que o app fala de patente durante um racha, e é de propósito: no fim, vira comemoração; no meio, viraria discussão. É a tela que vai para o grupo do WhatsApp.
