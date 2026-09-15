# Ideias para o futuro — anotadas de leve

> Parte da documentação do Raxa — índice em [docs/README.md](../README.md).
> Nada aqui é decisão nem requisito: é lembrete. Quando uma ideia virar trabalho, ela sai daqui e
> ganha documento de produto, D-NN e RF. Anotado em 2026-09-14.

## 1. Quadras e horário

- **Endereço no cadastro de cada pessoa.** Hoje só a quadra da liga tem endereço (D-179). Com o
  endereço (ou o bairro) de cada jogador dá para saber onde a galera mora.
- **Quadras de aluguel cadastradas no app**, com agenda de horários livres. O app sugere, para a
  hora que o grupo quer jogar, a quadra que tem horário livre e **atende melhor a maioria pela
  distância**.
- **Reserva de horário** pelo app e, talvez, **pagamento da quadra** pelo app (rateio entre os
  confirmados é o caso natural: a lista da chamada já diz quem vai).

## 2. Contratar goleiro (ou jogador de linha) do nível do racha

- Um racha sem goleiro contrata um pelo app; o mesmo para completar a linha.
- O nível do contratado **naquele racha** é estimado cruzando ligas: quem joga em mais de uma liga
  é uma aresta entre elas (grafo de rachas com jogadores em comum). Pelos caminhos entre a liga do
  contratado e a liga contratante dá para transportar o Elo, com **maior ou menor confiança**
  conforme o número e a qualidade das arestas (a mesma ideia de confiança que já existe na
  calibração, D-82).
- **Pagamento do contratado pelo app** e **nota do contratante ao contratado depois do pagamento**
  (só quem pagou avalia; só depois de pago).

## 3. Por que isso importa

O app ajudaria os dois lados: divulgação e ocupação das quadras da cidade, e manter a cultura de
racha viva (racha que não fecha goleiro ou não fecha quadra morre).

## 4. Monetização — hipóteses, não decisão

O que orienta (ver [princípios](principios.md)): a quadra é o lugar; um toque grava; quem joga não
pode pagar para ver o próprio nível. Cobrar do jogador comum pelo que o app já faz de graça mata a
adoção e a cultura que a ideia quer manter viva. As hipóteses, na ordem em que parecem fazer
sentido:

1. **Comissão sobre transação** (o mais alinhado). O app só ganha quando alguém ganhou também:
   uma taxa sobre a reserva da quadra e sobre o cachê do goleiro/jogador contratado. Quem paga a
   taxa é a quadra ou o contratado (que recebeu trabalho pelo app), não o racha. Depende de o
   marketplace existir (seções 1 e 2) e de volume de reservas: é a aposta longa.
2. **Assinatura da quadra** (B2B). A quadra paga um valor fixo por mês para aparecer com agenda,
   receber reservas e ter a página dela dentro do app — o app é canal de venda de horário ocioso.
   Fácil de explicar, fácil de cobrar, e não toca no jogador. Provavelmente a primeira receita
   real, porque precisa de poucas quadras para valer.
3. **Plano da liga** (opcional, barato, por liga e não por pessoa). Coisas que o grupo inteiro
   quer e ninguém individualmente: histórico ilimitado, exportação, destaques do mês compartilháveis,
   mais de N ligas por conta, camisa/escudo. O admin paga (ou rateia) como paga a quadra. Cuidado:
   nunca colocar nível, chamada ou partida ao vivo atrás do plano — é o que faz o racha usar o app.
4. **Rateio com taxa**: o app cobra a quadra dos confirmados (Pix) e repassa; uma taxa pequena por
   cobrança. Resolve a dor real de "quem ainda não pagou" da chamada. Só faz sentido com pagamento
   já dentro do app (seção 1), e o custo do Pix/meio de pagamento come parte da margem.
5. **Patrocínio local** (lojas de material esportivo, bares perto da quadra) no fim do racha ou nos
   destaques do mês. Pouco dinheiro, ruído na tela — só se vier de graça com a base grande.

O que **não** fazer: anúncio genérico dentro das telas do dia (a tela do racha é usada com a bola
rolando); cobrar por jogador; vender dados dos jogadores.

Sequência plausível: primeiro base de rachas e quadras usando de graça (a chamada já traz o grupo
inteiro para o app), depois assinatura de quadra (2), depois pagamento e comissão (1 e 4) quando
houver volume, e contratação de jogador (seção 2) por último porque depende do grafo entre ligas
ter densidade.
