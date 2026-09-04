# Raxa — notas para o Claude

App de racha (futebol de várias partidas curtas com nível Elo por jogador). Um arquivo só:
`index.html` (motor + UI), `config.js` (chaves do Supabase), `supabase/schema.sql` (banco).
Documentação em `docs/`, um arquivo por assunto — **abra só o que a tarefa pede** (mapa abaixo).

## Onde está o quê (docs/)

| Preciso de… | Abrir |
|---|---|
| significado de um termo (liga, racha, trecho, divisão, lançador…) | `docs/produto/conceitos.md` |
| nível: escada, cortes, Elo, K, calibração, anti-ioiô, entrada, goleiro, quem vê, **o que a patente garante** | `docs/produto/patentes.md` |
| telas do dia: presença, montagem, partida ao vivo, fim do racha | `docs/produto/fluxo-do-racha.md` |
| regra de quadra: time cheio, fila, vencedor fica, goleiro, empate | `docs/produto/regras-do-racha.md` |
| Stats, destaques do mês, rankings, duelos, parcerias | `docs/produto/stats.md` |
| revisar / corrigir / anular partida | `docs/produto/contestacao-e-correcao.md` |
| membros, entrada na liga, papéis, admin | `docs/produto/contas-e-permissoes.md` (+ `docs/tecnico/banco-de-dados.md`) |
| princípios de produto (lista curta) | `docs/produto/principios.md` |
| requisitos RF / RNF | `docs/produto/requisitos-funcionais.md` · `requisitos-nao-funcionais.md` |
| o que o protótipo faz hoje / como o backend está montado | `docs/tecnico/prototipo.md` |
| modelo de dados | `docs/tecnico/banco-de-dados.md` |
| subir ambiente, rodar SQL | `docs/tecnico/deploy.md` |
| simulações (converge / confianca / consistencia) e os números que ficaram | `docs/tecnico/estudos.md` |
| **por que** algo é assim | `docs/decisoes/README.md` (índice D-01…) → arquivo do tema |

Decisões por tema em `docs/decisoes/`: `motor-de-patente` · `escada-calibracao-e-palpite` ·
`times-fila-e-goleiro` · `partida-e-historico` · `stats-e-destaques` · `interface` ·
`contas-e-permissoes` · `dados-sync-e-codigo`. Cada D-NN tem âncora `<a id="d-nn"></a>`.

## Onde está no ar (ambiente de teste)
- **Site:** GitHub Pages do repositório `mauroban/raxa`, branch `main`, raiz →
  https://mauroban.github.io/raxa/ . **Push em `main` = deploy** (1–2 min).
- **Banco/auth/realtime:** projeto Supabase (URL e anon key em `config.js`). O esquema é
  aplicado **à mão** pelo usuário: Supabase → SQL Editor → colar `supabase/schema.sql` → Run
  (idempotente). Sempre que `schema.sql` mudar, avisar que precisa rodar de novo — o app no ar
  quebra até isso acontecer.

## Como publicar uma mudança
1. `python scripts/test.py` (motor) · `python scripts/smoke.py` (telas, DOM falso) ·
   `python scripts/sync.py` (backend com Supabase falso) · `python scripts/layout.py`
   (HTML gerado). Os quatro têm que passar. `python scripts/visual.py` (Chrome
   headless, prints) é opcional — rodar quando a mudança mexe em layout/CSS.
   `python scripts/converge.py [bom|misto|nada]` (simulação de convergência com o
   motor real) é a régua para qualquer mudança em K, margem ou calibração (D-82).
2. Atualizar a documentação **no mesmo commit**:
   - o documento de produto do assunto em `docs/produto/` (comportamento);
   - nova entrada **D-NN** no arquivo do tema em `docs/decisoes/` (data, o quê, por quê,
     descartado, onde), com `<a id="d-nn"></a>` antes do título, **e** uma linha no índice
     `docs/decisoes/README.md`;
   - `docs/tecnico/deploy.md` se o SQL mudou · `docs/tecnico/banco-de-dados.md` se o modelo mudou ·
     `docs/tecnico/estudos.md` se um estudo foi criado ou rerodado · `docs/tecnico/prototipo.md`
     se o que existe/não existe mudou.
3. `git commit` + `git push origin main`.

## Dados
Só fatos vão para o banco (jogadores, partidas com trechos/eventos, rachas, live, log de
correções); nível e estatística são recalculados no cliente (`rebuildAll`). Sync incremental por
versão (`league_delta` / `save_parts`). Ver D-29 em `docs/decisoes/dados-sync-e-codigo.md`.
