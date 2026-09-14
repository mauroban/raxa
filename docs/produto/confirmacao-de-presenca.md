# Confirmação de presença — a lista do racha no app

> Parte da documentação do Raxa — índice em [docs/README.md](../README.md).
> Decisões em [chamada e confirmação](../decisoes/chamada-e-confirmacao.md) (D-165, D-166).

A liga tem um racha fixo na semana (dia e hora). Alguns dias antes a **lista abre** e cada um se
confirma pelo app, **na linha ou no gol**. Cada papel tem o seu máximo; quem passa dele fica na
**espera**. É o que hoje acontece no grupo do WhatsApp, só que com uma fonte de verdade e sem
alguém contando nomes.

## 1. O admin marca uma vez

Em **Ajustes → Confirmação de presença**: liga o interruptor, escolhe o **dia da semana**, a
**hora**, as **vagas na linha**, as **vagas no gol** e **quantos dias antes** a lista abre
(padrão 4). As vagas vêm sugeridas pelo formato: 5v5 sugere 12 na linha e 2 no gol (três times de
linha e um goleiro em cada gol); 6v6, 15 + 2; 7v7, 18 + 2; 11v11, 20 + 2.

É recorrente: o admin não cria nada por semana. Quem não é admin vê o resumo ("confirmação qui 19h ·
12 na linha + 2 no gol") no cartão de formato dos Ajustes.

## 2. O que cada um vê na aba Racha

O cartão **Próximo racha** é a aba Racha enquanto não há racha em andamento (D-167): sem "Próximo passo" nem destaques — **Iniciar racha** mora na barra de baixo, para quem lança.

- **Lista fechada:** só a data e quando abre ("A lista abre seg 14/09").
- **Lista aberta, sem confirmar:** dois botões, **Vou** (grande) e **Vou no gol**. Um toque
  confirma; nada de rascunho, nada de "tem certeza".
- **Confirmado:** "Você vai na linha · 5º" (verde) ou "Você é o 2º da espera da linha" (dourado),
  com **ir para o gol** / **ir para a linha** e **Não vou**.
- **As duas listas**, Linha e Gol, com os nomes numerados na ordem de chegada. O corte é visual:
  quem está dentro tem o chip aceso; abaixo, em cinza, **Espera**.
- **Compartilhar** gera o texto pronto para o grupo (data, Linha 12/14 com os nomes numerados,
  espera, Gol, e o endereço do app). O grupo vira espelho do app, não o contrário.

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
- **Confirmar não é presença.** Quem conta para a patente é quem esteve na quadra, como sempre.
- **Só quem está no cadastro entra na lista;** arquivado some dela.
- **Sem sinal há 20 s, o botão não grava** (a regra de leitura do racha, D-104): o app avisa em
  vez de fingir.

## 4. Quem lança confirma pelos outros

Nem todo mundo vai abrir o app — e a lista do grupo não pode continuar em paralelo. Então **lançador,
moderador e admin** têm **+ Confirmar alguém**: uma folha com a busca e, em cada nome, **Linha** e
**Gol**. Um toque confirma e a folha continua aberta, porque é ação repetida ("o Bruninho e o Igor
mandaram no grupo"). O chip mostra discretamente **por mauro** quando foi outra pessoa que confirmou.

Tocar num nome da lista (o próprio, ou qualquer um para quem lança) abre a folha da pessoa:
**Passar para o gol / a linha** e **Tirar da lista**.

O **admin** ainda tem **Cancelar este racha** (feriado, chuva): a data pula, o cartão passa para a
semana seguinte e fica um aviso com **desfazer** até a data passar. A lista daquela data continua
guardada.

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
quem está dentro das duas listas, e o goleiro confirmado entra com a luva acesa. Quem está na espera
**não entra marcado**, mas sobe para logo abaixo dos marcados na grade — se apareceu, é um toque.
A partir daí vale a grade como sempre: quem chegou, chegou. O racha guarda a qual chamada
pertenceu.

Com racha em andamento, o cartão da chamada some — a tela é a do racha.

## 7. O que ficou de fora, de propósito

Lembrete (não há notificação: o app é uma página web), pagamento, chat e uma estatística de "quem
confirmou e não veio". Essa última é a única que volta depois: sai de graça da diferença entre a
lista e a presença, e é um problema social real de racha.
