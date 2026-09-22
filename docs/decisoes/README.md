# Decisões — o que foi decidido, e por quê

> O código é protótipo; **as decisões não são**. Este arquivo existe para que a v2 não precise
> redescobrir nada: cada decisão traz o motivo, o que foi descartado e onde ela vive hoje
> (documento, código e teste). Quando uma decisão mudar, ela é **reescrita aqui**, com a data nova
> e o motivo da virada — não some.
>
> Regras de quadra em [Regras do racha](../produto/regras-do-racha.md) · produto em [docs/produto](../produto/) (índice em [docs/README.md](../README.md))
> · dados em [Banco de dados](../tecnico/banco-de-dados.md).

---

## Onde está cada decisão

Um arquivo por tema; dentro de cada um, as decisões em ordem de número (que é a ordem do tempo). Números não mudam e não são reaproveitados.

### [Motor de patente](motor-de-patente.md)

- [D-01](motor-de-patente.md#d-01) · A unidade de cálculo é o trecho — sempre
- [D-02](motor-de-patente.md#d-02) · O peso do trecho descartado é redistribuído
- [D-03](motor-de-patente.md#d-03) · O mínimo de trecho é relativo: 4 min ou ⅓ da partida, o que for menor
- [D-04](motor-de-patente.md#d-04) · A variação de patente é fixa e igual em toda liga
- [D-05](motor-de-patente.md#d-05) · Patente por valência só existe se a pessoa jogou nela
- [D-33](motor-de-patente.md#d-33) · K 36/44 e acelerador de sequência; chance igual na pré-partida e ao vivo
- [D-34](motor-de-patente.md#d-34) · K decai com histórico; acelerador também por saldo de forma
- [D-37](motor-de-patente.md#d-37) · Trecho curto sem gol não conta; K dividido por trechos válidos; V/D é da partida
- [D-38](motor-de-patente.md#d-38) · Partida única tem regra de trecho própria
- [D-45](motor-de-patente.md#d-45) · Partida única: nível por confronto, placar por margem; +/- em destaque só nela
- [D-46](motor-de-patente.md#d-46) · Elo clássico: K 40/20, sem acelerador, sem proteção; calibração por modo
- [D-55](motor-de-patente.md#d-55) · K de jogo de time: 64 calibrando / 32 depois; margem de histerese 21
- [D-65](motor-de-patente.md#d-65) · Patente e destaques seguem o critério do modo — como a doc sempre disse
- [D-82](motor-de-patente.md#d-82) · K por incerteza (64/32 → 16) e aviso "revisar palpite?" para o admin — em vez de K fixo 32
- [D-83](motor-de-patente.md#d-83) · Piso do K em 20; aviso de revisão por RANKING (últimos 8 rachas); cansaço fica fora do rating
- [D-110](motor-de-patente.md#d-110) · Gol de goleiro é conta de goleiro; improviso no gol entra uma patente abaixo
- [D-113](motor-de-patente.md#d-113) · Sem "sinal de confiança" na patente: o estudo que decidiu (scripts/confianca.py)
- [D-115](motor-de-patente.md#d-115) · Diferença mantida no tempo vale ~1 divisão a mais que o retrato: o estudo (scripts/consistencia.py)
- [D-155](motor-de-patente.md#d-155) · Mudança de nível num período: nível no início e no fim dele, não o de hoje (`from` em `m.moves`, `movimentos`)

### [Escada, calibração e palpite](escada-calibracao-e-palpite.md)

- [D-24](escada-calibracao-e-palpite.md#d-24) · Os níveis são metais, e na interface "patente" se chama "nível"
- [D-25](escada-calibracao-e-palpite.md#d-25) · Quatro níveis: sai o Diamante
- [D-36](escada-calibracao-e-palpite.md#d-36) · De volta a 5 níveis — Diamante no topo, Prata no meio; sem nível até calibrar
- [D-52](escada-calibracao-e-palpite.md#d-52) · O admin vê o Elo cru, discreto, na aba Jogadores
- [D-53](escada-calibracao-e-palpite.md#d-53) · Calibração do racha curto: 15 partidas (o nível aparece em ~2 rachas)
- [D-57](escada-calibracao-e-palpite.md#d-57) · Na aba Jogadores, o admin vê a escada ordenada por Elo
- [D-73](escada-calibracao-e-palpite.md#d-73) · Corrigir nível "desde a entrada" — o palpite que faltou, com o racha contando por cima
- [D-74](escada-calibracao-e-palpite.md#d-74) · Nada supera fatos: correção de nível só existe no nível de entrada
- [D-79](escada-calibracao-e-palpite.md#d-79) · Divisão 3 finalmente parece rara: o "polido" prometido virou CSS de verdade
- [D-80](escada-calibracao-e-palpite.md#d-80) · Divisão em riscos (I, II, III), não em número — e 3 continua sendo o topo
- [D-86](escada-calibracao-e-palpite.md#d-86) · A ficha deixa claro que o admin edita a ENTRADA — e mostra o HOJE que vai sair, antes de salvar
- [D-90](escada-calibracao-e-palpite.md#d-90) · Nível de goleiro: a régua é a da linha, e a recomendação é NÃO dar palpite
- [D-91](escada-calibracao-e-palpite.md#d-91) · Tirar o palpite vale para qualquer um — o histórico reaplica sem ele
- [D-94](escada-calibracao-e-palpite.md#d-94) · Sai o aviso "revisar palpite?" — ele apontava quem estava certo tanto quanto quem estava errado
- [D-95](escada-calibracao-e-palpite.md#d-95) · A entrada é a junção das opiniões de quem lança; "Editor" vira "Moderador"
- [D-96](escada-calibracao-e-palpite.md#d-96) · Com 3+ opiniões, média aparada (sem a mais alta e a mais baixa), não a mediana pura
- [D-121](escada-calibracao-e-palpite.md#d-121) · Sem anular opinião de uma pessoa; rebaixar a Jogador invalida (não apaga); Jogador também opina
- [D-124](escada-calibracao-e-palpite.md#d-124) · Só o admin vê, na ficha, tudo que um membro opinou sobre os outros (só leitura)
- [D-125](escada-calibracao-e-palpite.md#d-125) · Opinião individual não aparece na ficha de ninguém (nem admin): entrada, contagem e divergência; nota por nome só pelo botão da D-124
- [D-126](escada-calibracao-e-palpite.md#d-126) · Minhas opiniões: a lista ordena sem opinião › Diamante … Ferro › não sei
- [D-127](escada-calibracao-e-palpite.md#d-127) · A opinião só se dá pelo cartão de "Minhas opiniões"; a ficha mostra entrada e hoje e leva ao cartão
- [D-197](escada-calibracao-e-palpite.md#d-197) · Quantas de cada patente e os extremos da divergência: só para moderador ou acima; sem atraso nem mínimo
- [D-196](escada-calibracao-e-palpite.md#d-196) · A ficha não tem mais "Sua opinião: X · mudar ›": induzia a alinhar a nota pela dos outros
- [D-194](escada-calibracao-e-palpite.md#d-194) · Nota a 4+ divisões da entrada marcada na folha do admin; a ficha diz quantas de cada patente, para todo mundo
- [D-177](escada-calibracao-e-palpite.md#d-177) · A média aparada tira um sexto de cada ponta (mínimo uma): os dois terços centrais

### [Times, fila e goleiro](times-fila-e-goleiro.md)

- [D-06](times-fila-e-goleiro.md#d-06) · Time é sempre cheio; quem sobra é fila
- [D-07](times-fila-e-goleiro.md#d-07) · Reserva presa a um time só existe na partida única
- [D-08](times-fila-e-goleiro.md#d-08) · A fila é de pessoas: o "de próximo"
- [D-09](times-fila-e-goleiro.md#d-09) · Time curto é completado, nunca compensado sentando alguém
- [D-10](times-fila-e-goleiro.md#d-10) · Quem fica de fora também é equilibrado
- [D-11](times-fila-e-goleiro.md#d-11) · Ruído na montagem para variar — e só na montagem
- [D-32](times-fila-e-goleiro.md#d-32) · Goleiro do vencedor fica; escolha manual antes do apito; sem "girar"
- [D-35](times-fila-e-goleiro.md#d-35) · O app aponta duplas inseparáveis em vez de fingir que as separa
- [D-39](times-fila-e-goleiro.md#d-39) · Empate com 3 times: um fica; goleiro fica com o time que fica
- [D-42](times-fila-e-goleiro.md#d-42) · Goleiro fixo é um dos N; gols abaixo das substituições
- [D-44](times-fila-e-goleiro.md#d-44) · Formato e modo são da liga, escolhidos na criação
- [D-49](times-fila-e-goleiro.md#d-49) · Presença do racha conta desde o começo, não a foto do fim
- [D-50](times-fila-e-goleiro.md#d-50) · A sessão guarda os times como foram montados; tocar no time mostra a escalação
- [D-56](times-fila-e-goleiro.md#d-56) · Dupla inseparável: aviso a partir de 20 partidas juntos
- [D-71](times-fila-e-goleiro.md#d-71) · Quem fica não troca de lado — e a folha de trocar time fala nomes no 5v5
- [D-77](times-fila-e-goleiro.md#d-77) · Times do racha: % de vitórias realizada × probabilidade de vitória no apito
- [D-87](times-fila-e-goleiro.md#d-87) · Patente média do time no cabeçalho do cartão
- [D-111](times-fila-e-goleiro.md#d-111) · Folha do time do racha: patentes e as partidas do time
- [D-122](times-fila-e-goleiro.md#d-122) · Mexer no elenco no meio do racha: ↶ do "foi embora" devolve a pessoa inteira; goleiro que chega no racha fixo vai para a fila; improvisado no gol não corta quem completa; refazer times zera a rodada
- [D-123](times-fila-e-goleiro.md#d-123) · Pré-partida com a gramática da partida ao vivo: 🧤, gol vazio e vaga são slots (sem folha de goleiro); a vaga fica à vista mesmo "jogando 4v4 assim"
- [D-129](times-fila-e-goleiro.md#d-129) · A roda: dois lados e uma fila só de pessoas; sai quem está há mais tempo em quadra; goleiro que espera entra no gol de quem perder; placar registrado + voltar fixos; sem empréstimo; desfazer na pré-partida
- [D-136](times-fila-e-goleiro.md#d-136) · Empate: com mais que um lado na fila os dois rodam o máximo que der; quando só um rodou, "trocar: fica o outro" no cartão do placar

### [Partida ao vivo e histórico](partida-e-historico.md)

- [D-18](partida-e-historico.md#d-18) · A tela da partida é o placar
- [D-28](partida-e-historico.md#d-28) · Fatos completos na partida, registro de correções, gol contra
- [D-30](partida-e-historico.md#d-30) · Substituição é da partida, não do time; "foi embora" tira a pessoa do racha *(no racha curto, superada por D-129)*
- [D-31](partida-e-historico.md#d-31) · A vaga mora no cartão do time
- [D-47](partida-e-historico.md#d-47) · Trocar o goleiro pelo do outro lado é troca de lugar — gol E escalação
- [D-48](partida-e-historico.md#d-48) · Fim sem querer tem volta: "Voltar a partida"
- [D-58](partida-e-historico.md#d-58) · Revisar é abrir a partida inteira, não só o placar
- [D-59](partida-e-historico.md#d-59) · A vitória é do time que jogou — a composição, não o nome no placar
- [D-60](partida-e-historico.md#d-60) · O time é a lista de quem jogou (até 5v5), no card da noite e no histórico
- [D-61](partida-e-historico.md#d-61) · Escalação e trocas são corrigíveis depois — reescrevendo o que a partida gravou
- [D-64](partida-e-historico.md#d-64) · Racha ao vivo à prova de tela atrasada — e o Voltar devolve a fila de verdade
- [D-75](partida-e-historico.md#d-75) · O histórico mostra a chance de cada lado no apito
- [D-92](partida-e-historico.md#d-92) · Toque errado fora da partida pergunta; dois celulares somam; o celular avisa quando o tempo bate
- [D-99](partida-e-historico.md#d-99) · O resumo do fim do racha conta a noite inteira
- [D-100](partida-e-historico.md#d-100) · O racha em andamento se anuncia: selo "● ao vivo" e ponto vermelho na aba
- [D-101](partida-e-historico.md#d-101) · Sem faixa "Trocando X"; autor do gol no polegar, com aviso enquanto faltar
- [D-103](partida-e-historico.md#d-103) · Substituição por toque sem folha: marca um, toca no par
- [D-117](partida-e-historico.md#d-117) · O 🧤 é um slot como os outros: goleiro entra pela substituição, improvisar não encurta o time
- [D-118](partida-e-historico.md#d-118) · Elo de largada de todos os titulares; efeito no nível por papel
- [D-195](partida-e-historico.md#d-195) · Partida de segundos continua contando inteira (marcação errada faz parte; os resultados valem)
- [D-198](partida-e-historico.md#d-198) · Correção de partida: gol é evento editável (time, minuto, autor, adicionar, apagar); placar e resultado recontados dos gols; sem botões de vencedor
- [D-199](partida-e-historico.md#d-199) · Relógio da partida na correção: início e duração, eventos na mesma fração, recusa horário em cima de outra partida; listas de correção com quem estava no racha primeiro
- [D-200](partida-e-historico.md#d-200) · Partida curta com troca de goleiro: goleiro de largada deduzido desfazendo as trocas; "era outra pessoa" aceita quem entrou por troca e apaga a troca que vira "sai X, entra X"

### [Stats e destaques](stats-e-destaques.md)

- [D-12](stats-e-destaques.md#d-12) · A tela do racha mostra os últimos 30 dias, não o topo histórico
- [D-13](stats-e-destaques.md#d-13) · O critério do destaque é o saldo acima do esperado
- [D-14](stats-e-destaques.md#d-14) · Artilheiro só quando os gols têm dono
- [D-15](stats-e-destaques.md#d-15) · Goleiro menos vazado = gols sofridos por partida, por trecho
- [D-16b](stats-e-destaques.md#d-16b) · O histórico é por racha, não por partida
- [D-43](stats-e-destaques.md#d-43) · +/- é a estatística principal
- [D-51](stats-e-destaques.md#d-51) · Números com a opção "sem goleiros"
- [D-54](stats-e-destaques.md#d-54) · Rankings da noite abrem até 10, e existe "quem mais perdeu"
- [D-69](stats-e-destaques.md#d-69) · Aproveitamento vira pontos (V=3, E=1) — e cada filtro de Stats responde à própria pergunta
- [D-70](stats-e-destaques.md#d-70) · Cada ranking tem uma setinha — e vira o próprio ranking do fim
- [D-72](stats-e-destaques.md#d-72) · "Quem mais perdeu" sai do card da noite — a setinha já conta essa história *(o "Mais derrotas" da temporada também saiu, no D-134)*
- [D-76](stats-e-destaques.md#d-76) · Partida a partida na tela do jogador — com a chance da época e uma bolinha por gol
- [D-97](stats-e-destaques.md#d-97) · No card do último racha, o realizado conta empate como meio — a mesma base da chance
- [D-108](stats-e-destaques.md#d-108) · Stats com cara de painel: gráficos, posição nos rankings, barras e ícones SVG
- [D-109](stats-e-destaques.md#d-109) · Gols por tempo só sobre minutos de linha; destaque nos rankings é o dono do perfil
- [D-112](stats-e-destaques.md#d-112) · Rankings: top 3 limpo na página, lista inteira e ordem numa folha
- [D-114](stats-e-destaques.md#d-114) · Filtros da Stats: uma família só, sem card
- [D-134](stats-e-destaques.md#d-134) · Derrota não é ranking
- [D-135](stats-e-destaques.md#d-135) · Na aba Jogador, linha e gol são duas leituras — não um interruptor
- [D-142](stats-e-destaques.md#d-142) · Os destaques de um racha (setas ‹ › em "Último", botão na aba Jogos) existem para qualquer racha, não só o último
- [D-143](stats-e-destaques.md#d-143) · "Rendeu acima do esperado" é ranking de todo período (30 dias, ano, Sempre) e posição na ficha, não só do racha
- [D-144](stats-e-destaques.md#d-144) · A linha de "Quem mais rendeu" mostra o saldo que a ordena
- [D-145](stats-e-destaques.md#d-145) · Rankings de temporada são taxas (por partida, por racha, a cada 10 min), presença é a exceção, piso de metade dos rachas do período
- [D-146](stats-e-destaques.md#d-146) · "Os melhores do racha" ordena por divisão e, dentro dela, por Elo
- [D-147](stats-e-destaques.md#d-147) · "Quem mais rendeu" nos Destaques também é % por partida
- [D-148](stats-e-destaques.md#d-148) · Tempo em quadra é volume, como presença: total, sem piso
- [D-149](stats-e-destaques.md#d-149) · Período por mês e por ano com setas ‹ ›; gráficos por racha/mês/ano nas duas abas
- [D-150](stats-e-destaques.md#d-150) · Momento na aba Jogador: gols em barra, % acima do esperado em linha, ao longo do tempo
- [D-151](stats-e-destaques.md#d-151) · Momento sem as barras de gol: só a linha
- [D-152](stats-e-destaques.md#d-152) · Momento: valor colado no ponto, área pintada, aproveitamento embaixo do eixo (sem segunda linha)
- [D-153](stats-e-destaques.md#d-153) · Painel da liga em Mês/Ano/Sempre: destaque de cada racha/mês/ano com toque que abre o período, e card de níveis
- [D-154](stats-e-destaques.md#d-154) · Gols por racha no painel da liga; média no título dos gráficos; faixa de patentes sem contagem na legenda
- [D-156](stats-e-destaques.md#d-156) · A faixa de níveis conta o goleiro pela patente de goleiro
- [D-157](stats-e-destaques.md#d-157) · A média dos gráficos por mês ignora os meses sem racha
- [D-158](stats-e-destaques.md#d-158) · Sem os gráficos de colunas por mês e por ano no painel da liga (o mês a mês / ano a ano já conta isso)
- [D-159](stats-e-destaques.md#d-159) · Empate: primeiro o de maior patente; no chip do mês a mês, o nome e um "+N"
- [D-160](stats-e-destaques.md#d-160) · Sem o interruptor "Sem goleiros": o goleiro conta em tudo; rankings de goleiro nunca filtrados
- [D-193](stats-e-destaques.md#d-193) · Taxas por tempo em "por hora", com uma casa decimal (era a cada 10 min)
- [D-201](stats-e-destaques.md#d-201) · Corrigir os times do racha: a montagem gravada na sessão é editável pelo admin (toque no nome, escolha o time); vale nas stats, não em partida nem nível
- [D-202](stats-e-destaques.md#d-202) · Sequência de vitórias zera no empate; sequência de derrotas na ficha (agora e pior do período) e no ranking Pior sequência
- [D-203](stats-e-destaques.md#d-203) · Acima do esperado ganha destaque discreto: linha na ficha abaixo do aproveitamento e primeiro ranking dos gerais em todo período
- [D-208](stats-e-destaques.md#d-208) · Leão do fim do racha: gols por hora de linha no fim (quem começa com 50+ min nas pernas) menos no resto do racha, sem piso de rachas; também no racha aberto e na ficha
- [D-204](interface.md#d-204) · Lista de ligas: o topo de 56 px volta (D-137 zerou `--toph` e esmagava a marca) e o selo ao vivo ganha linha própria
- [D-205](interface.md#d-205) · Lista de ligas: cada cartão mostra a sua patente (ou ⏳ calibrando) naquela liga, respeitando quem vê os níveis
- [D-192](stats-e-destaques.md#d-192) · Com um período só, a linha ‹ 2026 › fica, com as setas apagadas
- [D-191](stats-e-destaques.md#d-191) · Linha do tempo do nível só em Ano e Sempre, sempre com quatro marcos; sem os títulos "Nível na linha" e "Mês a mês"
- [D-190](stats-e-destaques.md#d-190) · Momento sem o aproveitamento embaixo do eixo; resumo do grupo sem minutos
- [D-188](stats-e-destaques.md#d-188) · A aba Jogador de Stats fala do nível: hoje, melhor ou calibrando, e quantas divisões andou no período
- [D-161](stats-e-destaques.md#d-161) · A seta do racha não troca de sub-aba (Jogador fica em Jogador)

### [Interface](interface.md)

- [D-17](interface.md#d-17) · Tema claro é o padrão
- [D-23](interface.md#d-23) · Stats é a segunda aba, e Membros mora nos Ajustes
- [D-40](interface.md#d-40) · Visual da quadra: tinta, coletes e navegação embaixo
- [D-41](interface.md#d-41) · Menos contorno, menos texto
- [D-78](interface.md#d-78) · Variação de nível da noite legível: seta colorida, uma por divisão, e o caminho escrito
- [D-81](interface.md#d-81) · Chip de presença mostra o nível do papel de hoje (🧤 aceso = nível de goleiro)
- [D-84](interface.md#d-84) · A escada só fala de nível: sem gols e sem bolinhas de forma na linha do jogador
- [D-88](interface.md#d-88) · Presença densa no celular: duas colunas, chip menor, e ✕ na busca
- [D-89](interface.md#d-89) · Menos densidade nos números: destaques recolhidos, V/E/D seco, duelos sem ruído, empate divide posição
- [D-98](interface.md#d-98) · Montagem: times em duas colunas, um nome por linha
- [D-106](interface.md#d-106) · Sem emoji no botão de iniciar; bolinha vermelha para gol contra
- [D-107](interface.md#d-107) · Gol volta a ser ⚽ na "partida a partida"; gol contra é o mesmo ⚽, vermelho
- [D-119](interface.md#d-119) · Sem o botão "Carregar o racha de sábado"
- [D-120](interface.md#d-120) · O cartão de opinião cabe na tela do celular
- [D-131](interface.md#d-131) · Ajustes enxutos: só o que se mexe, cartões agrupados, sem texto explicando o óbvio
- [D-133](interface.md#d-133) · O placar é o cabeçalho da coluna do time: cada lado é uma coluna na cor do time, a fila fica fora
- [D-137](interface.md#d-137) · Sem cabeçalho de liga nas telas; nome, números e "Trocar de liga" no primeiro cartão de Ajustes
- [D-138](interface.md#d-138) · Gol: clarão na cor do time e folha "GOL!" por cima da tela com os nomes do lado, gol contra, sem autor e "Não foi gol"; o placar diz sempre "＋ gol"
- [D-139](interface.md#d-139) · Ajustes e Jogadores com menos tamanho: campos de 40 px, formato em linha, 15 nomes por tela
- [D-167](interface.md#d-167) · A aba Racha fora do dia é só a chamada: saem "Próximo passo" e "Destaques · últimos 30 dias"
- [D-168](interface.md#d-168) · Lista da chamada mais densa: chips de 32 px, número à esquerda, badge da patente à direita
- [D-169](interface.md#d-169) · Gol antes da linha; confirmados na frente da grade de presença; Ajustes sem cards colados
- [D-173](interface.md#d-173) · Guia de interface: tamanhos, o que cabe na tela e a ordem de cada tela, num documento só
- [D-174](interface.md#d-174) · Três pequenas do guia: "N de N confirmados" na presença, "Sem racha marcado", folha de leitura na chamada
- [D-175](interface.md#d-175) · Escada de Jogadores em uma linha por pessoa: sem V/E/D, 44 px, 17 nomes por tela
- [D-185](interface.md#d-185) · Filtro de Stats fixo no topo da aba; os títulos deixam de repetir o período
- [D-186](interface.md#d-186) · Textos de ajuda parados saem de sete telas (presença, montagem, partida, próxima, painel, opiniões, quem é você)
- [D-187](interface.md#d-187) · Painel de Stats sem os títulos "O racha", "Níveis" e "Rankings"; sem "toque para abrir"
- [D-189](interface.md#d-189) · Ajustes em linhas: rótulo à esquerda, controle à direita (interruptor, campo curto, segmentado); liga e código num card
- [D-140](times-fila-e-goleiro.md#d-140) · Goleiro é do time só quando a conta fecha (um por time); senão rodízio, um em cada gol — a montagem antiga volta
- [D-162](times-fila-e-goleiro.md#d-162) · Cabeçalho da montagem: "(goleiro reveza)" só com um goleiro; com dois ou mais, "(goleiros à parte)"
- [D-163](times-fila-e-goleiro.md#d-163) · Goleiro é do time pela conta da linha, não pelo "2 times" escolhido na mão

### [Contas, perfis e permissões](contas-e-permissoes.md)

- [D-19](contas-e-permissoes.md#d-19) · Um membro é um jogador — e só um
- [D-20](contas-e-permissoes.md#d-20) · Três caminhos para entrar, uma regra só
- [D-22](contas-e-permissoes.md#d-22) · Revisar é do admin; o primeiro perfil vinculado é o admin
- [D-26](contas-e-permissoes.md#d-26) · Código gera pedido; o admin aprova
- [D-27](contas-e-permissoes.md#d-27) · Quem entra é Jogador; Lançador é dado pelo admin
- [D-62](contas-e-permissoes.md#d-62) · Papel de admin vale no servidor — e a migração para de travar leitura
- [D-85](contas-e-permissoes.md#d-85) · Membros sai da aba Jogadores: papel na linha da escada, e um card só de pendências
- [D-93](contas-e-permissoes.md#d-93) · Juntar dois cadastros da mesma pessoa — reversível pela ficha
- [D-105](contas-e-permissoes.md#d-105) · Apagar liga: só o dono, só sem outros membros, digitando o nome
- [D-128](contas-e-permissoes.md#d-128) · Arquivar em vez de remover jogador; ficha por blocos (olhar → cadastro → admin → arquivar); ajustes e permissão só para o admin; "Sou eu" só sem perfil
- [D-130](contas-e-permissoes.md#d-130) · Trocar o código de convite: botão Novo, o antigo deixa de valer na hora
- [D-132](contas-e-permissoes.md#d-132) · Link de convite (?c=CODIGO): quem abre entra ou cria a conta e o pedido vai sozinho
- [D-141](contas-e-permissoes.md#d-141) · O papel de cada membro (Admin/Moderador/Lançador) só aparece para moderador ou acima
- [D-207](contas-e-permissoes.md#d-207) · Vincular conta é um caminho só (`vinculaConta`): "Sou eu" e "criar meu jogador" também fazem o primeiro vinculado (e o dono) virar admin
- D-164 · *(desfeita em 2026-09-14, no mesmo dia)* senha redefinida pelo dono da liga — o dono de qualquer liga passaria a entrar na conta pessoal de um membro; conta é pessoal, não da liga

### [Chamada e confirmação de presença](chamada-e-confirmacao.md)

- [D-165](chamada-e-confirmacao.md#d-165) · Cada um se confirma pelo app: agenda semanal, linha ou gol, espera derivada, hora do servidor
- [D-166](chamada-e-confirmacao.md#d-166) · "Quem é você nesta liga?": o membro escolhe o próprio perfil ou cria o seu com apelido
- [D-170](chamada-e-confirmacao.md#d-170) · Mais de um racha na semana; vagas próprias de uma data; padrão 12 + 3
- [D-171](chamada-e-confirmacao.md#d-171) · Confirmar, trocar e sair são eventos que ficam; quem faltou e quem saiu em cima da hora
- [D-172](chamada-e-confirmacao.md#d-172) · "Marcar os N confirmados" na grade de presença
- [D-178](chamada-e-confirmacao.md#d-178) · Quem foi confirmado por outro assume com "Confirmo" (sem perder a vez); "Você vai na linha" sem posição; faltou em duas contas
- [D-179](chamada-e-confirmacao.md#d-179) · Endereço da quadra: texto livre nos Ajustes, link do Google Maps no cartão e no texto do grupo
- [D-180](chamada-e-confirmacao.md#d-180) · Endereço com sugestões enquanto digita (Photon/OpenStreetMap), sem chave; guarda a coordenada
- [D-181](chamada-e-confirmacao.md#d-181) · Contador de cada lista só no título dela; "Espera · N"; a linha de contadores embaixo da data saiu
- [D-182](chamada-e-confirmacao.md#d-182) · O endereço fica fora do texto do grupo até a busca ser do Google Maps
- [D-183](chamada-e-confirmacao.md#d-183) · Endereço da quadra removido por inteiro (desfaz D-179, D-180, D-182): a busca do OpenStreetMap era ruim; volta com Google Places
- [D-184](chamada-e-confirmacao.md#d-184) · A lista abre N dias antes a uma hora escolhida pelo admin ("Dias antes" + "Às"; padrão 0h)

### [Dados, sync e código](dados-sync-e-codigo.md)

- [D-16](dados-sync-e-codigo.md#d-16) · Estatística é derivada; o que a partida guarda é saída do motor
- [D-21](dados-sync-e-codigo.md#d-21) · O histórico é a fonte da verdade
- [D-29](dados-sync-e-codigo.md#d-29) · A liga deixa de ser um JSON só: partes por entidade e sync incremental
- [D-63](dados-sync-e-codigo.md#d-63) · Sync sem derivado, sem log dobrado e sem RPC em rajada
- [D-66](dados-sync-e-codigo.md#d-66) · Limpeza: uma definição só por ação, sem sombras e sem texto mentindo
- [D-67](dados-sync-e-codigo.md#d-67) · Fim do monkey-patch — e os contratos com os testes viram texto no código
- [D-68](dados-sync-e-codigo.md#d-68) · A documentação alcança o backend — a [Protótipo](../tecnico/prototipo.md) sai da era do localStorage
- [D-102](dados-sync-e-codigo.md#d-102) · Pronto para a quadra: cópia da liga no aparelho, prazo por pedido, batida de rede e avisos de mesclagem
- [D-104](dados-sync-e-codigo.md#d-104) · Consistência acima de tudo: o mesmo lance conta uma vez, e sem sinal há 20 s é só leitura
- [D-116](dados-sync-e-codigo.md#d-116) · Documentação dividida por assunto em `docs/`, decisões em arquivos por tema
- [D-176](dados-sync-e-codigo.md#d-176) · Edição pendente do jogador (apelido, descrição, opinião) se mescla por campo com a linha que chega do servidor, em vez de sumir

---

## Como registrar uma decisão nova

Uma linha por decisão, nesta ordem: **o que foi decidido** (com a data), **por quê**, **o que foi
descartado** e **onde ela vive** — documento, função e teste. Se não tem teste, diga que não tem.
Decisão sem "por quê" volta a ser discutida em três meses; decisão sem "onde" vira lenda.

**Onde escrever:** no arquivo do tema (acima), no fim; uma linha `<a id="d-nn"></a>` antes do título, e uma linha nova na lista deste índice. Se o tema não existe, crie o arquivo e a seção aqui.
