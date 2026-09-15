# Confirmação de presença — a lista do racha no app

> Parte da documentação do Raxa — índice em [docs/README.md](../README.md).
> Decisões em [chamada e confirmação](../decisoes/chamada-e-confirmacao.md) (D-165, D-166, D-178, D-179).

A liga tem um racha fixo na semana (dia e hora). Alguns dias antes a **lista abre** e cada um se
confirma pelo app, **na linha ou no gol**. Cada papel tem o seu máximo; quem passa dele fica na
**espera**. É o que hoje acontece no grupo do WhatsApp, só que com uma fonte de verdade e sem
alguém contando nomes.

## 1. O admin marca uma vez

Em **Ajustes → Confirmação de presença**: liga o interruptor, escolhe o **dia da semana** e a
**hora** do racha, as **vagas na linha**, as **vagas no gol** e **quantos dias antes** a lista abre
(padrão 4). As vagas vêm sugeridas pelo formato: 5v5 sugere 12 na linha e 3 no gol; 6v6, 15 + 3;
7v7, 18 + 3; 11v11, 20 + 3. E o **endereço da quadra** (D-179): enquanto o admin digita, aparecem
até cinco sugestões de lugares e endereços (busca do OpenStreetMap, sem cadastro, D-180); um toque
escolhe, e o app guarda o endereço legível e a coordenada. Também aceita texto livre. O endereço
aparece embaixo da data no cartão do próximo racha como link que abre o Google Maps. No texto do
compartilhamento ele ainda **não** vai: fica para quando a busca funcionar com o Google Maps
(D-182). Sem endereço, nada aparece.

**Mais de um racha na semana** (D-170): **+ Outro dia na semana** acrescenta uma ocorrência (dia e
hora próprios; o ✕ tira). O padrão é uma vez por semana. As vagas e o "abre N dias antes" são da
liga, iguais para todas as ocorrências. O próximo racha é sempre a ocorrência mais perto ainda por
vir; dois rachas no **mesmo dia** não são suportados (a lista é por data).

É recorrente: o admin não cria nada por semana. Quem não é admin vê o resumo ("confirmação qui 19h,
sáb 10h · 12 na linha + 3 no gol") no cartão de formato dos Ajustes.

## 2. O que cada um vê na aba Racha

O cartão **Próximo racha** é a aba Racha enquanto não há racha em andamento (D-167): sem "Próximo passo" nem destaques — **Iniciar racha** mora na barra de baixo, para quem lança.

- **Lista fechada:** só a data e quando abre ("A lista abre seg 14/09").
- **Lista aberta, sem confirmar:** dois botões, **Vou** (grande) e **Vou no gol**. Um toque
  confirma; nada de rascunho, nada de "tem certeza".
- **Confirmado:** "Você vai na linha" (verde) ou "Você é o 2º da espera da linha" (dourado),
  com **ir para o gol** / **ir para a linha** e **Não vou**. Quem está dentro não vê a posição:
  a ordem só importa na espera (D-178).
- **Confirmado por outra pessoa** ("o Igor mandou no grupo e o lançador pôs na lista"): a própria
  pessoa vê "**mauro confirmou você na linha**" (dourado) com **Confirmo** (grande) e **Não vou**.
  Confirmo é um toque, não muda a vez na fila, e a partir daí a confirmação é dela — é isso que
  separa, depois do racha, quem se comprometeu e faltou de quem foi posto na lista por alguém (D-178).
- **As duas listas**, Gol primeiro e depois Linha (o gol é curto e é o que decide se o racha fecha), com os nomes numerados na ordem de chegada, em chips baixos de
  duas colunas (14 nomes cabem numa tela, D-168) e o **badge da patente** do papel da lista à direita
  (cor + riscos, como na presença; some com os níveis fechados). O contador de cada lista ("Gol ·
  2/3", "Linha · 12/12") fica só no título dela (D-181). O corte é visual: quem está dentro
  tem o chip aceso; abaixo, em cinza, **Espera · N**.
- **Compartilhar** gera o texto pronto para o grupo (data, Gol, Linha 12/14 com os nomes numerados,
  espera, e o endereço do app; o endereço da quadra fica de fora por enquanto, D-182). O grupo vira
  espelho do app, não o contrário.

Quem ainda não tem perfil nesta liga vê antes o cartão **Quem é você nesta liga?** (seção 5): sem
perfil não existe "Vou".

## 3. As regras, em uma frase cada

- **A espera não é estado; é quem passou do máximo.** Todo mundo que confirma entra numa lista só,
  na ordem em que chegou. O máximo corta a lista. Alguém desiste, o próximo sobe sozinho — sem
  promoção manual, sem corrida de "quem clicou primeiro".
- **A hora de chegada é do servidor.** O relógio do celular não decide a fila. Enquanto a gravação
  não volta, o app mostra a ordem pelo relógio local; a resposta do servidor corrige.
- **Trocar de lista é confirmação nova.** Quem vai da linha para o gol (ou o contrário) entra no
  **fim** da outra lista. Regra de uma frase, ninguém contesta.
- **Nada se apaga: cada toque é um evento com hora do servidor** (D-171). Confirmar, trocar de
  lista e sair ficam registrados com quem fez e quando. O estado de alguém numa data é o último
  evento dela. A folha do nome mostra a linha do tempo ("na linha · qui 14:02 · saiu · sáb 18:40 ·
  por mauro").
- **Confirmar não é presença.** Quem conta para a patente é quem esteve na quadra, como sempre.
- **Só quem está no cadastro entra na lista;** arquivado some dela.
- **Sem sinal há 20 s, o botão não grava** (a regra de leitura do racha, D-104): o app avisa em
  vez de fingir.

## 4. Quem lança confirma pelos outros

Nem todo mundo vai abrir o app — e a lista do grupo não pode continuar em paralelo. Então **lançador,
moderador e admin** têm **+ Confirmar alguém**: uma folha com a busca e, em cada nome, **Linha** e
**Gol**. Um toque confirma e a folha continua aberta, porque é ação repetida ("o Bruninho e o Igor
mandaram no grupo"). A folha do nome diz **confirmado por mauro** quando foi outra pessoa que confirmou,
e a linha do tempo mostra "confirmou · qui 18:40" quando a própria pessoa depois assumiu (D-178).

Tocar num nome da lista (o próprio, ou qualquer um para quem lança) abre a folha da pessoa:
**Passar para o gol / a linha** e **Tirar da lista**. O jogador comum abre a folha dos outros só
para ler: posição e linha do tempo, sem botões (D-174).

O **admin** ainda tem, no pé do cartão:

- **Vagas deste racha** (D-170): abre uma folha com linha e gol **só para esta data** — deu 4 na
  espera, o admin sobe a linha de 12 para 16 e mais um time entra; a espera sobe sozinha. O botão
  passa a mostrar "Vagas deste racha · 16 + 3", e **Voltar ao padrão** desfaz. O padrão da liga
  continua em Ajustes; datas passadas são esquecidas na próxima gravação.
- **Cancelar este racha** (feriado, chuva): a data pula, o cartão passa para a próxima ocorrência e
  fica um aviso com **desfazer** até a data passar. A lista daquela data continua guardada.

## 5. Quem é você nesta liga (D-166)

Um membro novo entra pelo link, o admin aprova, e a primeira coisa que ele vê na aba Racha é
**Quem é você nesta liga?**: a grade dos perfis **sem dono** (busca quando há mais de oito), na
ordem de quem mais joga. Toca no nome, confirma "É você? · Sou eu", e o perfil é dele com todo o
histórico. Não achou o nome? **Não estou na lista — criar meu jogador**: escolhe o **apelido** que
usa nesta liga (vem preenchido com o usuário da conta, mas é livre — "Bruninho" numa liga, "Bruno
Costa" na outra) e diz se costuma ir ao gol. O jogador nasce sem nível (o app descobre calibrando),
como qualquer cadastro sem palpite.

Nome repetido é recusado com a dica de tocar nele na lista. O admin continua podendo desfazer um
vínculo errado na ficha ou em Pendências.

## 6. No dia do racha

Quando quem lança toca em **Iniciar racha** no dia da chamada, a presença **já vem marcada** com
quem está dentro das duas listas, e o goleiro confirmado entra com a luva acesa. A linha de dica da
grade mostra **"12 de 14 confirmados"**: quantos dos que estavam dentro já chegaram (D-174). Quem está na espera
**não entra marcado**, mas sobe para logo abaixo dos marcados na grade — se apareceu, é um toque.
A partir daí vale a grade como sempre: quem chegou, chegou. O racha guarda a qual chamada
pertenceu. Se o racha for iniciado com a lista aberta mas **fora do dia** (teste, ou o dia virou),
ninguém entra marcado — mas quem confirmou continua **na frente da grade**, os de dentro antes da
espera (D-169). Enquanto houver confirmado sem marca, a grade tem o botão **Marcar os N confirmados**
(D-172): um toque marca quem está dentro das duas listas, goleiro com a luva; a espera continua a um
toque por nome. O botão some quando não sobra ninguém para marcar.

Com racha em andamento, o cartão da chamada some — a tela é a do racha.

**Quem faltou e quem saiu em cima da hora** (D-171). No resumo do fim do racha e no racha dentro
da aba Jogos aparece o bloco **Chamada**, só quando há o que dizer: **Confirmou e não veio** (estava
dentro da lista no apito, a confirmação era dela mesma, e não está na presença), **Confirmado por
outro e não veio** (idem, mas quem confirmou foi outra pessoa — "Igor (por mauro)" — e ela nunca
tocou em Confirmo; talvez nem soubesse, D-178) e **Saiu em cima da hora** (saiu da lista a menos
de 3 h da hora marcada, com quanto tempo antes e por quem, quando não foi a própria pessoa). O racha
guarda a data da chamada, a hora marcada e o apito para essa conta ser refeita a qualquer momento.

## 7. O que ficou de fora, de propósito

Lembrete (não há notificação: o app é uma página web), pagamento, chat e uma estatística de "quem
confirmou e não veio". Essa última é a única que volta depois: sai de graça da diferença entre a
lista e a presença, e é um problema social real de racha.
