# Estudos — simulações com o motor real

> Parte da documentação do Raxa — índice em [docs/README.md](../README.md).

Todos os estudos importam o motor de verdade do `index.html` (`computeElo`, `updateRank`, `buildTeams`, `calibrando`) e o rodam no Node contra ligas simuladas: 20 pessoas com **habilidade verdadeira escondida** ~N(1500, 200), presença variável (13–18 por racha; quatro que vêm a cada 3 semanas), times montados pelo app pelo Elo atual, vencedor fica, remontagem em 25% dos rachas, 12 partidas curtas com gols Poisson (2 gols ou 7 min). Um racha por semana: 3 meses ≈ 13 rachas, 6 meses ≈ 26.

Três cenários de palpite de entrada: **bom** (todo mundo a ±1 divisão da verdade), **misto** (5 em 20 errados por uma patente inteira), **nada** (todo mundo em 1500, sem palpite).

Regra da casa: **qualquer mudança em K, margem, calibração ou no texto que compara duas pessoas passa por aqui antes** — a régua é o número medido, não a intuição.

## converge.py — as patentes convergem? (D-82, D-83)

`python scripts/converge.py [bom|misto|nada]`

Pergunta: com que rapidez e até onde a escada mostrada chega perto da verdade, em cada regra de K?

O que ficou: **K decrescente por incerteza** (sem palpite 64 → 16, com palpite 32 → 16, ao longo de 45 partidas; depois piso 20) foi a melhor ou empatada em todos os cenários — misto 75% / bom 85% / sem palpite 74% dentro de ±1 divisão em 40 rachas. K fixo 32 corrói o palpite bom (73% de patente certa no 1º racha → 57% no 30º). Bônus de sequência e K por surpresa perdem em tudo. Um jogador errado por uma patente inteira numa liga bem calibrada leva ~6 meses para chegar a uma divisão do lugar; esporádico (1 em 3 rachas) não converge com dados — só correção humana. Cansaço fica fora do rating. Detalhe e números completos em [D-82](../decisoes/motor-de-patente.md#d-82) e [D-83](../decisoes/motor-de-patente.md#d-83).

**Palpite ruim (cenário `ruim`, 04/09/2026):** todo mundo entra com uma patente **sorteada**, sem relação com a verdade, e a saída ganha a linha *sobra da entrada* (inclinação do erro de hoje sobre o erro do palpite: 1 = o erro inteiro ainda está lá, 0 = as opiniões deixaram de importar). `python scripts/converge.py ruim 120 40`, motor atual: sobra **95% no racha 3 · 68% no 20 · 37% no 40 · 15% no 60 · ~0% no 80** — as opiniões deixam de ser lidas no nível por volta do racha 60–80 (15–18 meses de racha semanal). Mas o estrago fica: no racha 120 a liga que começou com palpite sorteado está em **44% ±1 div, erro 155 pts**, contra **71–77% e 66–80 pts** da liga sem palpite nenhum (que já está aí no racha 40) e 66–79% da liga com palpite bom. Motivo: a expectativa é do time, então o erro de um entra na atualização dos outros quatro; o palpite errado "vaza" para todo mundo e o ruído que ele semeia sobrevive muito depois de a correlação sumir. Palpite bom: sobra 82% no racha 3 · 42% no 20 · 23% no 40 · ~10% do 60 em diante — a entrada certa também some, mas enquanto está lá segura a liga em 85–89% nos primeiros meses. Leitura: **palpite ruim é pior que nenhum, e por muito tempo** — quando as opiniões não são confiáveis, deixar sem nível (K alto, sem viés) vence de longe; e uma entrada grosseiramente errada só se corrige rápido pela mão do admin na ficha.

## confianca.py — dá para dizer quem está na patente certa? (D-113)

`python scripts/confianca.py [bom|misto|nada] [rachas] [ligas]`

Pergunta: existe um sinal observável (volume de partidas, circulação na patente, distância à borda) que separe quem está na patente certa de quem não está — para acender um "calibrado com confiança"?

O que ficou: **não.** Quem já calibrou está a ±2 divisões da verdade em 97% (bom) / 92% (misto); a ±1, 80% / 69%; na patente exata, 71% / 66%. Nenhum sinal muda o ±1 nem o ±2; 150 partidas acertam o mesmo que 15. Decisão: nenhum símbolo além do "calibrando". A mesma rodada mediu pares: quando A aparece **d divisões acima** de B num retrato, A é de fato mais forte em d=1: 72% / 66% · d=2: 87% / 81% · **d=3: 96% / 91%** · d=4: 99% / 97%; a diferença real é de uma patente inteira em só um terço dos pares a d=3. [D-113](../decisoes/motor-de-patente.md#d-113).

## consistencia.py — e se a diferença se mantém por um trimestre? (D-115)

`python scripts/consistencia.py [bom|misto|nada] [meses1] [meses2] [ligas]`

Pergunta: depois de 3 meses de racha, mais 3 meses; se ao longo do 2º trimestre a **menor** diferença mostrada entre A e B foi de X divisões, A é mais forte? É uma patente inteira melhor?

O que ficou (bom / misto / nada): A é mais forte — X=1: **88% / 80% / 78%** · X=2: **96% / 90% / 88%** · X=3: **99% / 95% / 94%** · X=4: 100% / 98% / 97%. Uma patente inteira melhor — X=1: 14% / 18% / 34% · X=2: 32% / 31% / 49% · X=3: **55% / 48% / 64%** · X=4: 77% / 67% / 78% · X≥5: 97% / 91% / 92%. Leitura: **um trimestre de consistência vale cerca de uma divisão a mais no retrato** (1 mantida ≈ 2 no retrato, 2 mantidas ≈ 3, 3 mantidas ≈ 4). A ordem pode ser afirmada a partir de 2 divisões mantidas; "uma patente inteira melhor" continua sem garantia (3 mantidas dão cara ou coroa; precisa de 5). Dobrar o período rende 3–5 pontos, não mais — o ruído é do dado (um resultado 5v5 dividido entre dez), não da amostra. [D-115](../decisoes/motor-de-patente.md#d-115).

## Como acrescentar um estudo

Um script em `scripts/`, com docstring dizendo a pergunta e o uso; uma seção aqui com pergunta, comando, o número que ficou e o link da decisão; a decisão (D-NN) no arquivo de tema em `docs/decisoes/` com os números completos. Guardar saídas em `scripts/.tmp/` (fora do git).
