# Regras do racha — como a noite roda

> As regras de quadra que o app segue: quem entra, quem sai, quem fica, quem completa.
> Nada aqui é sobre patente ou rating — isso está em [Patentes](patentes.md).
> Requisitos correspondentes em [Requisitos funcionais](requisitos-funcionais.md) (RF-05 e RF-06)
> · o porquê de cada regra em [decisões](../decisoes/README.md).

---

## 1. Dois jeitos de jogar, e só dois

| Modo | Como é | O que o app faz |
|---|---|---|
| **Várias curtas** *(padrão)* | 10 a 15 partidas por noite, alvo de 2 gols ou 7 min, **vencedor fica** | monta os times, cuida da **fila** e sugere o próximo confronto |
| **Partida única** | uma partida longa (50 min), **2 times fixos** a noite inteira | divide todo mundo em 2 times com titulares e **reservas**, e sai do caminho |

O modo é escolhido na abertura de cada racha — a mesma liga pode ter quinta longa e sábado curto.

---

## 2. Racha curto: a roda

**Quem ganhou fica. Do lado que perdeu, sai quem está há mais tempo em quadra. Entra quem está há mais
tempo fora.** É a regra inteira (D-129).

### 2.1 Dois lados e uma fila só

**Na montagem, times inteiros.** O app monta quantos times cheios couberem — A, B, C, D — e mostra todos,
porque equilibrar bem continua sendo o ponto; quem não completa um time fica de fora. Dá para forçar 2, 3
ou 4, dentro do que cabe. **Ao começar o racha, a quadra vira dois lados e uma fila só.** Os dois primeiros
times entram; os outros viram a fila, na ordem em que foram montados, junto com quem estava de fora. Daí em
diante não existe "Time C esperando", reserva de time nem empréstimo: a fila é **de pessoas**, na ordem de
quem está fora há mais tempo, e só a roda gira. Em alguns dias ela gira redondo, sempre os mesmos times; na
maioria o improviso chega em algum momento, e a roda é feita para ele.

| Presentes (5v5) | Cada lado | Fila | Quando um lado perde |
|---|---|---|---|
| 8 de linha + 2 goleiros | 4 + goleiro | 0 | ninguém sai: jogam de novo |
| 10 de linha + 2 goleiros | 4 + goleiro | 2 | saem 2, entram 2 |
| 11 de linha + 2 goleiros | 4 + goleiro | 3 | saem 3, ficam o goleiro e mais um |
| 12 de linha + 2 goleiros | 4 + goleiro | 4 | sai o lado inteiro, entram 4 — os times de sempre, intactos |
| 13 de linha + 2 goleiros | 4 + goleiro | 5 | saem 4, entram 4, um espera mais uma |
| 12 de linha + 3 goleiros | 4 + goleiro | 4 + 🧤 | saem 4 e o goleiro; entram 4 e o goleiro que esperava |
| 13 sem goleiro marcado | 5 | 3 | saem 3, ficam 2 |
| 8 pessoas no total | 4v4 — único caso em que se joga com menos, e a tela avisa | 0 | — |

Quando a conta fecha em 3 ou 4 times inteiros, a roda faz os grupos entrarem e saírem intactos sozinha —
é o racha de 3 times de sempre. Quando não fecha, os grupos giram uma pessoa por vez, e a tela mostra
exatamente isso, com nomes.

**A fila também é equilibrada.** Quem sobra não é "os piores": o montador monta grupos inteiros e
parelhos, os dois primeiros são os lados e os outros viram a fila, na ordem — o grupo que entra primeiro é
um time parelho. Cada toque em **Equilibrar** varia o arranjo, então ninguém fica marcado como o eterno
reserva.

**Reserva de time não existe no racha curto.** Só na partida única, onde os dois times são fixos a noite toda.

### 2.2 A roda

Ao fim de cada partida:

1. **Quem ganhou fica em quadra**, inteiro.
2. **Do lado que perdeu sai quem está há mais tempo em quadra** — tantos quantos a fila puder repor.
   Desempate: quem mais jogou hoje.
3. **Entra a frente da fila**: quem está fora há mais tempo.
4. **Quem saiu vai para o fim da fila.**
5. **Goleiro:** o goleiro do lado só roda se há goleiro esperando na fila — aí o de quem perdeu sai e o que
   esperava entra no gol.

Exemplo real, 13 pessoas no 5v5 (dois lados de 5, fila de 3):

```
Lado A 5  x  5 Lado B          fila: Rodrigo, Gleik, Maike
A ganha ─────────────────────────────────────────────────
Lado A fica inteiro
Lado B: saem 3 (os que estão há mais tempo em quadra)  →  fim da fila
        ficam 2 (o goleiro e mais um)
        entram Rodrigo, Gleik e Maike
Lado A 5  x  5 Lado B (novo)   fila: os 3 que saíram
```

**Empate:** a fila repõe os dois lados inteiros → os dois saem; repõe um lado → sai o que está há mais
tempo em quadra; não repõe nenhum → ninguém sai, jogam de novo. Com 3 times de sempre isso é "fica o que
entrou por último"; com 4, "os dois saem"; com 2, "jogam de novo" — D-39 continua valendo, dito em pessoas.

**Depois do Fim, a tela diz o que a roda fez.** O placar registrado fica num cartão fixo no topo, com o
**↩ Voltar a partida** ao lado, até a próxima começar; embaixo, "Saem X, Y → fim da fila · Entram Z, W".
Quem entrou aparece marcado no lado. Nada de aviso que some.

### 2.3 Mexer na mão: cansado, foi embora, chegou

Racha é racha: alguém cansa, alguém sai por qualquer razão. Tudo é toque ou arraste, com a mesma
gramática da partida ao vivo, e tudo tem **↶ desfazer**:

- **nome em quadra sobre nome da fila**: trocam de lugar — quem sai assume a posição de quem entrou;
- **nome em quadra sobre a fila** (ou o link "sai para a fila, entra Fulano" que aparece com o nome
  marcado): vai para o fim da fila e **a frente da fila entra no lugar** na hora;
- **dois nomes da fila**: trocam de ordem;
- **Foi embora** (com um nome marcado, é ele): a frente da fila entra na vaga na hora. Sem ninguém na
  fila, a **vaga fica à vista** ("＋ vaga · entra o próximo") e os dois lados entram menores e iguais;
  quem chega entra nela num toque — na vaga, para o próximo da fila; no nome e depois na vaga, para quem
  você escolher;
- **Chegou**: fim da fila — ou, com o 🧤, espera na fila e entra no gol de quem perder.

A tela em repouso não explica nada; a dica só aparece com um nome marcado, dizendo o próximo passo.

### 2.4 Quem entra é sugestão, não regra

O app propõe a roda. **Racha real não obedece fila; obedece o que a galera combinou.** Qualquer nome
troca de lugar em dois toques, antes do apito.

---

## 3. Goleiro

- **Goleiro é papel do dia, não atributo da pessoa.** Quem veio para o gol se marca na presença (🧤), e isso
  muda de racha para racha — e no meio do racha.
- **Um goleiro por time** (3 goleiros e 3 times, 4 e 4) → **o goleiro sai e entra com o time.** Não é
  rodízio: o time da fila entra inteiro, goleiro junto, e o de quem perdeu vai para a fila inteiro.
- **Menos goleiros que times, mas dois ou mais** → um em cada lado, e ele fica com o lado; o time sem
  goleiro (o C, o D) é N−1 de linha e entra com o goleiro do lado. Se em algum momento há um goleiro
  esperando na fila, ele entra no gol de quem perder, e o de quem perdeu vai para a fila. É a mesma roda
  dos dois casos acima: o goleiro roda quando há goleiro para entrar.
- **Um goleiro só** → ele reveza: fica com o lado que venceu; no resto, troca de lado. Do outro lado
  alguém da linha improvisa (a tela mostra o gol vazio para você escolher).
- Racha em que todo mundo reveza no gol: não marque ninguém, e escolha o goleiro na tela da partida.
- **Com um goleiro só (rodízio), ele é sempre além dos N−1 de linha.** Quem do lado vai para o gol deixa
  uma **vaga de linha**, e a frente da fila entra nela na hora (D-117, D-129).

---

## 4. Partida única (modo longo)

- **Sempre 2 times**, montados com todo mundo: N titulares e o resto como **reserva do próprio time**.
- **Cada time se vira com os seus**: substituição livre, quantas quiser, a qualquer momento.
- Sem fila, sem "vencedor fica", sem completar de fora — não tem de onde puxar, e não precisa.
- A partida é longa (50 min por padrão, sem alvo de gols) e **pesa bem mais** na patente, porque é uma só.

---

## 5. Patente: uma por valência, e só se jogou

- Cada pessoa tem **duas patentes independentes**: uma de **linha** e uma de **goleiro**.
- **Quem nunca jogou numa das duas simplesmente não tem patente ali.** O cara é Ouro na linha e nunca
  pegou no gol? Ele não tem patente de goleiro — não aparece na escada de goleiro, e a ficha dele diz
  *"sem patente no gol"*.
- **Se ele for para o gol no meio do jogo sem ter patente**, entra valendo o **nível de entrada padrão**
  (o mesmo de quem acabou de ser cadastrado) e começa a construir a patente de goleiro dali em diante,
  em calibração. O contrário vale igual: goleiro que resolve jogar na linha.
- O palpite do cadastro vale **só para a valência em que a pessoa vai jogar**. Cadastrar um Ouro de linha
  não faz dele um Ouro no gol.

---

## 6. Destaques do mês

A tela do racha mostra os **últimos 30 dias**, em duas listas:

1. **Os melhores do racha** — maior patente entre quem apareceu no período (pela valência que mais jogou);
2. **Quem mais rendeu além do esperado** — a conta já desconta a dificuldade dos confrontos.

Mais o artilheiro, o goleiro menos vazado e quem mais apareceu. Cada linha diz `X rachas · Y partidas · Z% de vitórias`.

- para entrar na lista do "além do esperado": **2 rachas e 20 partidas** no período — noite boa sozinha não vira destaque do mês;
- **artilheiro** só aparece se metade ou mais dos gols tiverem autor;
- **menos vazado** é gol sofrido por partida, contado só nos trechos em que a pessoa estava no gol.

---

## 7. O que o app decide e o que é sempre seu

| O app faz sozinho | Você decide sempre |
|---|---|
| montar dois lados equilibrados e a fila em fatias parelhas | quem joga de que lado |
| girar a roda: quem sai, quem entra, e dizer isso na tela | trocar qualquer nome, por toque ou arraste, com desfazer |
| completar um lado curto pela frente da fila | quem entra na vaga |
| pôr o goleiro que espera no gol de quem perdeu | quem pega no gol, a qualquer momento |

Nenhuma dessas sugestões bloqueia nada. Se a decisão do app não bate com o que a galera combinou na quadra,
a galera ganha — em dois toques.
