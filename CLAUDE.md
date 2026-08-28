# Raxa — notas para o Claude

App de racha (futebol de várias partidas curtas com nível Elo por jogador). Um arquivo só:
`index.html` (motor + UI), `config.js` (chaves do Supabase), `supabase/schema.sql` (banco).

## Onde está no ar (ambiente de teste)
- **Site:** GitHub Pages do repositório `mauroban/raxa`, branch `main`, raiz →
  https://mauroban.github.io/raxa/ . **Push em `main` = deploy** (1–2 min).
- **Banco/auth/realtime:** projeto Supabase (URL e anon key em `config.js`). O esquema é
  aplicado **à mão** pelo usuário: Supabase → SQL Editor → colar `supabase/schema.sql` → Run
  (idempotente). Sempre que `schema.sql` mudar, avisar que precisa rodar de novo — o app no ar
  quebra até isso acontecer.

## Como publicar uma mudança
1. `python scripts/test.py` (motor) · `python scripts/smoke.py` (telas, DOM falso) ·
   `python scripts/sync.py` (backend com Supabase falso). Os três têm que passar.
2. Atualizar a documentação no mesmo commit: `DOCUMENTACAO.md` (comportamento),
   `DECISOES.md` (nova entrada D-NN: data, o quê, por quê, descartado, onde), `DEPLOY.md`
   (se o SQL mudou), `BANCO-DE-DADOS.md` (modelo).
3. `git commit` + `git push origin main`.

## Dados
Só fatos vão para o banco (jogadores, partidas com trechos/eventos, rachas, live, log de
correções); nível e estatística são recalculados no cliente (`rebuildAll`). Sync incremental por
versão (`league_delta` / `save_parts`). Ver D-29 em `DECISOES.md`.
