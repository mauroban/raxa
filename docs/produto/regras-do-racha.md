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

## 2. Racha curto: o "de próximo"

### 2.1 Time é sempre cheio

**No 5v5 se joga 5 contra 5.** Não existe time de 3 esperando a vez, nem lado com um a menos —
quadra no Brasil não tem jogo menor que o formato.

O app monta **quantos times inteiros couberem** e o resto vira **fila**:

| Presentes (5v5) | Times | Fila |
|---|---|---|
| 10 de linha + 2 goleiros | 2 times de 4 + goleiro fixo em cada | 2 |
| 11 de linha + 2 goleiros | 2 times de 5 (4 + goleiro) | 3 |
| 12 de linha + 2 goleiros | 3 times de 4, goleiros revezando | 0 |
| 13 sem goleiro marcado | 2 times de 5 | 3 |
| 16 de linha + 3 goleiros | 4 times de 4, goleiros revezando | 0 |
| 8 pessoas no total | 4v4 — único caso em que se joga com menos, e a tela avisa | 0 |

**A fila também é equilibrada.** Quem sobra não é "os piores": o app escolhe quem espera atravessando
todos os níveis, um de cada faixa. E como cada toque em **Equilibrar** varia o arranjo, ninguém fica marcado
como o eterno reserva.

**Reserva de time não existe no racha curto.** Quem está fora é da *fila*, do racha inteiro — não do banco
de um time específico. Reserva só faz sentido na partida única, onde os dois times são fixos a noite toda.

### 2.2 Vencedor fica, perdedor roda com a fila

O ciclo de toda partida encerrada:

1. **Quem ganhou fica em quadra**, inteiro.
2. **Quem perdeu sai.**
3. **A fila entra no lugar de quem saiu** — quem está esperando há mais tempo entra primeiro.
4. **Se a fila não dá para trocar o time inteiro, alguns do time que perdeu ficam para completar.**
   É o clássico: *entram 3, ficam 2 — normalmente o goleiro e mais um.*
5. **Quem saiu vai para o fim da fila.**

Exemplo real, 13 pessoas no 5v5 (2 times de 5, fila de 3):

```
Time A 5  x  5 Time B          fila: Rodrigo, Gleik, Maike
A ganha ─────────────────────────────────────────────────
Time A fica inteiro
Time B: saem 3 (os que mais jogaram)   →  fim da fila
        ficam 2 (goleiro e mais um)
        entram Rodrigo, Gleik e Maike
Time A 5  x  5 Time B (novo)   fila: os 3 que saíram
```

**Quem sai do time que perdeu:** o app tira quem **mais jogou na noite** — é o que faz a fila girar parelho.
Quem fica é sempre visível na tela da próxima partida, e trocar é um toque.

**Empate:** com 4 times, os dois saem e entram os próximos; com 3, um fica — o que entrou por último
(o que já estava sai). Com 2 times, ninguém sai automaticamente — eles jogam de novo. Se o pessoal
combinar outra coisa (alguém cansado, quem tomou o último gol), é trocar os times na tela da
próxima partida — toque ou arraste.

### 2.3 Quando um time fica curto

Racha é racha: alguém vai embora no meio, alguém é puxado para o outro lado. Quando o time da vez entra
com menos gente que o adversário, **ninguém joga em inferioridade e ninguém senta**:

- o app **completa o time curto com quem está na fila**, sugerindo quem menos jogou na noite;
- **quem escolhe é você** — toque no nome para tirar e escolher outro;
- quem completa **joga aquela partida por aquele time e volta para o dele depois** (é empréstimo, não transferência);
- se preferir, **Jogar 4v4 assim** faz os dois lados entrarem menores, iguais — e a vaga continua à vista, para quem quiser preencher com um toque (D-123).

### 2.4 Quem entra é sugestão, não regra

O app propõe o próximo confronto pelo "vencedor fica" e pela ordem da fila. Trocar qualquer um dos dois
lados custa dois toques, e as escalações são editáveis antes do apito — inclusive puxando gente de outro
time ou da fila. **Racha real não obedece fila; obedece o que a galera combinou.**

---

## 3. Goleiro

- **Goleiro é papel do dia, não atributo da pessoa.** Quem veio para o gol se marca na presença (🧤), e isso
  muda de racha para racha — e no meio do racha.
- **Um goleiro por time ou mais** → cada um fica **fixo** no seu time e não entra na rotação da fila:
  o time roda em volta dele.
- **Menos goleiros que times** → eles ficam **fora dos times**, no rodízio: a cada partida o app escala um
  para cada lado, **alternando os lados** para ninguém ficar preso ao desempenho de um time só.
- Racha em que todo mundo reveza no gol: não marque ninguém, e escolha o goleiro na tela da partida.
- **Com rodízio, o goleiro é sempre além dos N−1 de linha** — venha do rodízio ou improvisado do time.
  Quem do time vai para o gol deixa uma **vaga de linha**, e a vaga aparece para ser fechada com alguém de
  fora; o time nunca fica com um a menos por causa do gol (D-117).

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
| montar times equilibrados e cheios | quem joga em qual time |
| manter a ordem da fila | quem entra e quem fica |
| sugerir o próximo confronto | qual time entra em cada lado |
| sugerir quem completa um time curto | quem completa — ou jogar com menos |
| girar a fila quando um time sai | trocar qualquer time da próxima partida na mão |
| escalar e alternar os goleiros do rodízio | quem pega no gol, a qualquer momento |

Nenhuma dessas sugestões bloqueia nada. Se a decisão do app não bate com o que a galera combinou na quadra,
a galera ganha — em dois toques.
