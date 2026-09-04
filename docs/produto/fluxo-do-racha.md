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
- Busca instantânea e **"+ Novo jogador"** que cadastra sem sair da tela (nome + patente + costuma ir ao gol).

## 2. Times — 1 toque

O app calcula sozinho quantos times cabem: no formato NvN cada time tem N−1 de linha quando os goleiros revezam. **12 de linha + 2 goleiros em 5v5 → 3 times de 4 + 2 goleiros no rodízio.** Dá para forçar 2, 3 ou 4 times.

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

**Quantos por time.** No formato NvN cada time entra com N. Quando os goleiros revezam, o time é de N−1 de linha mais o goleiro da vez. A partir daí:

- **time é sempre cheio.** No 5v5 se joga 5 contra 5 — não existe time de 3 esperando a vez, nem lado com um a menos. O app monta quantos times **inteiros** couberem: 10 de linha + 2 goleiros no 5v5 são **2 times de 4 + goleiro** e **2 de fora**, nunca 3 times de 4, 3 e 3;
- **quem não completa um time fica de fora**, num banco compartilhado, e entra por substituição ou completando quem ficou curto. No racha curto ninguém é reserva de um time específico — isso só existe na **partida única**, onde os dois times são fixos a noite inteira;
- **os dois times que entram juntos têm sempre o mesmo número.** Se um time ficou curto (alguém foi embora, alguém foi movido), ele é **completado com quem está de fora** (veja abaixo);
- **só se joga com menos quando não dá dois times cheios**: 8 pessoas no 5v5 viram 4v4, com aviso na tela — e nunca 5x3;
- na **partida única** são **sempre 2 times**: todo mundo dividido entre eles, N em quadra e o resto como reserva do próprio time;
- na **partida única**, dentro do time os **primeiros da lista são os titulares** e o resto aparece marcado como reserva; no racha curto isso não existe — todo mundo do time entra.

| Presentes (formato 5v5) | O que o app monta |
|---|---|
| 12 de linha + 2 goleiros | 3 times de 4, goleiros revezando — ninguém de fora |
| 11 de linha + 2 goleiros | 2 times de 5 (4 + goleiro fixo) e **3 de fora** |
| 10 de linha + 2 goleiros | 2 times de 5 (4 + goleiro fixo) e **2 de fora** |
| 13 sem goleiro marcado | 2 times de 5 e **3 de fora** |
| 16 de linha + 3 goleiros | 4 times de 4, goleiros revezando |
| 8 pessoas | 4v4 — único caso em que se joga com menos, e a tela avisa |
| Partida única, 10 de linha + 2 goleiros | 2 times de 6: 5 em quadra + 1 reserva cada |

**A fila — o "de próximo".** Quem não coube num time inteiro não fica parado: forma a **fila**, e a fila é de pessoas, não de times. Ao fim de cada partida o ciclo é o de todo racha: **quem ganhou fica, quem perdeu sai, e a fila entra no lugar de quem saiu** — primeiro quem está esperando há mais tempo. Se a fila não dá para trocar o time inteiro, **alguns do time que perdeu ficam para completar**: entram 3, ficam 2, normalmente o goleiro e mais um. Quem sai vai para o fim da fila, e sai quem mais jogou na noite — é o que faz a roda girar parelha.

No empate com 2 times ninguém sai automaticamente; se a galera combinar outra coisa, é trocar os times na tela da próxima partida — toque ou arraste (não há botão de girar a fila, D-32). O ciclo inteiro está em [Regras do racha](regras-do-racha.md).

**Completar o time que ficou curto.** Times nascem cheios, mas racha é racha: alguém vai embora no meio, alguém é puxado para outro time. Quando o time da vez entra com menos gente que o outro, ninguém joga em inferioridade e ninguém senta: a tela da próxima partida mostra **quem completa**, escolhido entre os que estão de fora — normalmente quem acabou de sair. Quem completa **joga aquela partida por aquele time e volta para o dele depois**; o rating enxerga isso naturalmente, porque a unidade é o trecho e o trecho guarda quem estava em quadra.

O app **sugere** quem completa (quem menos jogou na noite, para a fila girar), mas **quem decide é você**: toque no nome para tirar e escolher outro, ou toque em *Jogar 4v4 assim* para os dois lados entrarem menores.

Se mesmo assim um time entra incompleto, a tela avisa (“jogando 4v4 — puxe alguém de fora para fechar 5v5”) em vez de esconder o problema.

Cada cartão de time mostra, ao lado do nome, a **patente média do time** (D-87) — a média dos níveis de quem está nele (goleiro pela patente de goleiro), no mesmo badge da escada. É a leitura rápida de "esse time está de que tamanho?" antes da barra de equilíbrio; some com as patentes fechadas (D-52), como tudo que expõe nível.

**Mexer nos times é a operação mais frequente depois da presença**, então ela é a mais visível da tela:

- todos os nomes ficam em botões grandes, e **quem está de fora tem card próprio com contador** — nunca escondido; na montagem os times ficam **lado a lado, em duas colunas, um nome por linha** (D-98), para todos caberem na tela do celular sem nome quebrando;
- **arraste um nome sobre o outro para trocar de lugar**, ou arraste para dentro de um time, para o card "fora" ou para o card de goleiros — no celular, segure um instante antes de arrastar;
- quem preferir tocar: toca em um jogador e em outro para trocar; toca no espaço de um time (ou no card "fora") para mover;
- quem está selecionado fica marcado no próprio nome (tocar nele de novo desmarca) — sem faixa de aviso (D-101);
- "Equilibrar" refaz tudo, 🎲 sorteia ignorando o nível, e os botões 2/3/4 times remontam na hora.

## 3. Durante — 1 toque por partida

Cronômetro grande, dois blocos coloridos e os slots de goleiro:

- **Tocar no bloco do time = +1 gol.** Aparece uma tirinha logo abaixo do placar com os nomes daquele time para marcar o autor — toca ou ignora, ela some sozinha em 10 s. **Nunca bloqueia.** Enquanto houver **gol sem autor**, um aviso discreto fica abaixo do placar ("⚠️ 1 gol sem autor — toque para marcar") e abre a escolha do autor (D-101).
- **Os gols ficam listados abaixo do placar**, com minuto e autor: `3'12 — Rodrigo ✕`. Toque no nome para corrigir o autor (ou colocar um que você tinha pulado), e no **✕** para apagar aquele gol específico. É mais direto que um "desfazer" cego, porque você vê exatamente o que está removendo.
- O cronômetro mostra o alvo configurado na Liga ("2 gols ou 7 min") e pisca quando bate. Quando o **tempo** bate, o celular também **vibra e apita**, uma vez por partida: a tela está no chão da quadra e ninguém está olhando para ela. O alvo de gols não apita — é um toque da própria pessoa. O **alvo** é a única coisa que continua sendo da Liga; o **modo** (curtas ou única) é de cada racha.
- **Encerrar é um toque só, e o botão já diz o resultado**: `✓ Fim · Time A 2-1`. Ele grava exatamente o que está no placar e **não pergunta nada** — nem no 0-0, que é gravado como empate. Ninguém precisa tocar no time que venceu: os gols já disseram.
- **Fim sem querer tem volta.** Na tela seguinte, o bloco de partidas de hoje mostra **"↩ Voltar a partida"** enquanto a próxima não começa: apaga o registro e devolve a partida ao relógio exatamente como estava — gols, escalações, times, fila e goleiros do rodízio voltam ao lugar, e o tempo parado entre o Fim e a volta entra como pausa (o relógio não conta o intervalo). É diferente do "↶ Desfazer a última", que apaga a partida de vez, sem devolvê-la ao relógio. Logo depois do Fim, o aviso do placar fica **7 s** na tela com um **↩ voltar** — o erro mais comum se desfaz sem rolar até o bloco de partidas; começar outra partida fecha o aviso.
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
- **Entre uma partida e outra existe uma tela inteira: a próxima partida.** Não é um modal que some — é a tela padrão do racha enquanto nada está rolando, e ela mostra:
  - o confronto `Time A VS Time C`, com a **chance de cada lado** e o retrospecto de hoje;
  - **as duas escalações que vão entrar**, editáveis ali mesmo: toque num nome e depois no outro para trocar de lugar (ou arraste), inclusive puxando alguém de um time que está esperando ou de fora;
  - quem está de fora, agrupado por time, e o rodízio de goleiros da vez;
  - `＋ Chegou agora`, `🚑 Foi embora` e `Refazer times` (reequilibrar é refazer os times — não há botão separado).
- **Quem entra é sugestão, não regra.** Tocar em qualquer um dos dois lados troca aquele time por outro (até o 5v5 a folha mostra **os nomes de quem joga** em cada time, não só o apelido da cor — D-60/D-71). O app sugere seguindo "vencedor fica" e a fila de quem está esperando — e **quem venceu (ou ficou no empate) continua do mesmo lado da quadra** em que jogou (D-71); só o lado de quem saiu troca. Mas você decide — inclusive repetir o mesmo confronto ou pular a vez de alguém. Só depois de conferir tudo é que você toca em **▶ Começar partida**.
- **Substituição: toque ou arraste.** Arraste o nome de quem está fora sobre quem está em quadra e a troca acontece (no celular: segure o nome por um instante e arraste; no computador, arraste direto). Ou toque: o primeiro toque **marca** o nome (em quadra ou fora), quem pode ser o par dele ganha um tracejado verde e a dica abaixo da escalação diz o próximo passo ("Sai Fulano — toque em quem entra" / "Fulano entra — toque em quem sai"); o segundo toque, no par, faz a troca. Tocar no mesmo nome desmarca; tocar em outro do mesmo lado só move a marca. Não há folha no meio: escalação e quem está fora ficam na tela o tempo todo (D-103). Segurar um nome e soltar sem arrastar vale como toque. Trocar titular por reserva do mesmo time só inverte os dois.
- **Trocar o goleiro é tocar no slot 🧤.** A folha oferece quem está no rodízio e a opção de improvisar alguém do time. Escolher **o goleiro do outro lado** (marcado como *do outro lado*) faz os dois **trocarem de lugar por inteiro**: cada um passa para o gol e para a escalação do lado novo — inclusive na lista de autor do gol e na conta dos trechos. O mesmo vale no slot 🧤 da tela de próxima partida. `↶` desfaz a troca inteira.
- **Toda troca fecha um trecho** e a tela avisa em letra pequena: `Trecho 2 desde a última troca · 1-0 em 3'20`. O placar do trecho novo é o que vale para quem entrou (seção 3.4).
- **"Chegou agora"** (o atrasado): marca presença e manda direto para um time — ou para o rodízio de goleiros — no meio do racha.
- **"Foi embora"** (toque no botão, ou **arraste o nome até ele** — a confirmação é a mesma): quem já jogou hoje (ou está em quadra) sai contando presença (D-49). Quem **ainda não jogou** ganha a escolha: *🚑 Foi embora — esteve no racha* (conta presença) ou *✕ Marquei errado — não veio* (sai sem contar). Presença marcada por engano depois de montar os times não pode virar frequência.
- **Dois celulares na mesma partida.** O racha em andamento é um bloco só no servidor; quando os dois gravam quase juntos, o que chegou depois recebe o estado do outro. Se os dois estão na **mesma partida** (mesmo apito), os eventos se **somam**: gol de um e gol do outro ficam os dois, placar e escalação são refeitos a partir da largada, e autor marcado só aqui vai junto. Se os dois marcaram gol **do mesmo time com menos de 8 s de diferença**, é o mesmo gol visto de dois lugares: conta **um só** (com o autor, se um dos dois marcou) e o aviso diz "um gol foi marcado nos dois celulares: contei um só — se foram gols diferentes, toque de novo". A mesma substituição ou o mesmo goleiro lançados nos dois (em menos de 60 s) também viram um lance só, e uma troca repetida nunca duplica ninguém em quadra (D-104). Se o outro celular já encerrou a partida, vale o dele: o gol atrasado daqui se perde e o aviso diz exatamente isso ("1 gol lançado aqui não entrou: a partida já tinha sido encerrada no outro celular"). Partida **começada aqui sem sinal** não some quando o outro celular só mexeu na presença enquanto isso: ela fica, com os gols, por cima do que veio de lá (D-102). Fora da partida (presença, times) continua valendo o que chegou por último.
- **Sinal ruim na quadra.** A liga inteira fica **guardada no aparelho** (só fatos, como no servidor) a cada mudança. Sem sinal, o gol entra na tela, o canto de baixo diz *"sem conexão · guardado no aparelho"*, e tudo sobe quando a rede volta — inclusive se o navegador matou a aba no meio e o app foi reaberto ainda sem sinal: abre com a cópia, continua lançando, sincroniza depois. Quem só está olhando também vê *"sem conexão"* quando o aparelho cai, para saber que a tela pode estar velha. Nenhum pedido ao servidor fica pendurado mais de 12 s. E, além do aviso em tempo real, a liga aberta é conferida por conta própria a cada 5 s com o racha ao vivo (60 s fora dele) — o celular que dormiu no bolso não fica com o placar velho (D-102).
- **Sem sinal há mais de 20 s: só leitura.** Consistência vale mais que continuar lançando às cegas (D-104). Quando o app **constata** que está sem sinal (pedido que falhou, prazo estourado, o aparelho avisou que caiu) e o último contato bom passou de 20 s, os botões de lançar apagam, o canto de baixo diz *"sem sinal · só leitura"* e qualquer toque responde "Sem sinal há 35 s: só leitura até a conexão voltar, para o placar não divergir do outro celular". O que foi lançado dentro dos 20 s fica guardado e sobe. Silêncio não trava (quem está com rede e parado continua normal); a batida de 5 s é o que descobre a queda. Volta sozinho no primeiro contato bom. É a régua comum de app com interação ao vivo: batida a cada poucos segundos, "caiu" depois de 3–4 batidas perdidas.
- **"Desfazer a última"** fica no bloco de partidas de hoje e reverte a partida inteira, patentes incluídas.

## 4. Depois — o resumo

Dá para **cancelar o racha** em vez de encerrar: as partidas já lançadas continuam no histórico e valendo, só a sessão some. Encerrar e cancelar **perguntam antes**: encerrar não tem volta e o botão fica ao lado do "Começar partida"; a pergunta diz quantas partidas foram registradas e, se houver partida rolando, que ela será descartada.

Ao encerrar, o **resumo da noite** (D-99): data e tempo de bola rolando; partidas, gols, pessoas e minutos; **os times da noite** (nomes até o 5v5, V/E/D com vitórias em verde e derrotas em vermelho, gols marcados e sofridos, e o realizado × esperado quando os níveis estão abertos); **artilheiros** (top 3); **quem mais ganhou** (top 3, com E/D e aproveitamento); e **quem subiu** (seta verde) e **quem caiu** (seta vermelha) de nível, cada um com o badge de onde saiu → onde chegou. É o único momento em que o app fala de patente durante um racha, e é de propósito: no fim, vira comemoração; no meio, viraria discussão. É a tela que vai para o grupo do WhatsApp.
