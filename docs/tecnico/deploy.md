# Deploy — ambiente de teste, custo zero

Duas peças: **Supabase** (Postgres + contas + tempo real) e um **host estático**
para o `index.html`. As duas rodam no plano gratuito, sem cartão.

Tempo total: ~10 minutos.

---

## 1. Banco (Supabase)

1. Crie a conta em <https://supabase.com> → **New project**.
   Escolha a região mais perto (`South America (São Paulo)`), defina a senha do
   banco e espere ~2 min subir.

2. **SQL Editor** → **New query** → cole o conteúdo de
   [`supabase/schema.sql`](../../supabase/schema.sql) → **Run**.
   Cria as tabelas, a RLS, as funções e liga o Realtime. Pode rodar de novo sem quebrar.
   Se você já tinha aplicado uma versão anterior, rode de novo: a versão atual
   usa **tabelas por entidade** (`league_players`, `league_matches`,
   `league_sessions`, `league_live`, `league_log`) com sync incremental —
   ligas antigas migram sozinhas na primeira leitura —, `league_requests`
   (entrada por código passa por aprovação do admin) e as funções de contas
   da liga. Não existe policy de UPDATE direto em `leagues`: toda gravação
   passa pelo `save_parts` (compare-and-swap). A rodada atual (31/08/2026,
   D-62) ainda **corrige quem é admin no servidor** (`is_league_admin` lia
   `leagues.data`, que a migração esvazia — na prática todo membro passava
   por admin nos RPCs de aprovar/remover conta), restringe a leitura de
   `profiles` ao próprio perfil (username é metade da credencial), remove o
   `save_league` legado e faz `migrate_league` sair antes do lock quando a
   liga já migrou (senão toda leitura serializava os aparelhos do racha).

3. **Authentication → Sign In / Providers → Email**:
   - **Confirm email**: **desligado**  ← sem isso ninguém entra, porque o e-mail é fictício
   - **Allow new users to sign up**: ligado

4. **Project Settings → API**, copie:
   - **Project URL**
   - chave **anon public**

5. Cole as duas em [`config.js`](../../config.js):

   ```js
   window.RAXA_CFG = {
     url:     "https://xxxxxxxx.supabase.co",
     anonKey: "eyJhbGciOi..."
   };
   ```

> A `anon key` é pública de propósito — ela vai para o navegador de todo mundo.
> Quem protege os dados é a RLS: sem estar logado não se lê nada, e logado só se
> enxerga liga em que você é membro. A chave **`service_role` nunca** entra aqui.

---

## 2. Site

Só precisam ir para o ar dois arquivos: `index.html` e `config.js`.

### Netlify Drop (mais rápido)

Ponha os dois numa pasta e arraste em <https://app.netlify.com/drop>.
Sai uma URL HTTPS na hora. Para o link não expirar, crie a conta gratuita.

### Cloudflare Pages / Vercel / GitHub Pages

Qualquer um serve — é um site estático sem build.
No GitHub Pages, lembre que o repositório precisa ser público no plano gratuito.

```bash
git init && git add . && git commit -m "raxa com backend"
gh repo create raxa --public --source=. --push
gh api -X POST repos/:owner/raxa/pages -f "source[branch]=main" -f "source[path]=/"
```

---

## 3. Testar com o grupo

1. Abra a URL, **Criar conta**, usuário e senha (mínimo 6 caracteres).
2. **+ Nova liga** — ou **Carregar o racha de sábado** para já vir com 19 nomes.
3. Aba **Ajustes** → o **código de convite** de 6 caracteres está no topo. Compartilhe.
4. Cada pessoa cria a conta dela e usa **Entrar com um código**. Isso gera um
   **pedido**: o admin aprova em **Jogadores → Membros** e a liga aparece para a
   pessoa na hora (ela vê "Aguardando aprovação" na home até lá).
5. Em **Jogadores**, cada um abre o próprio nome e toca em **Sou eu** para
   vincular a conta ao jogador.

Com o racha rolando, quem está com a tela aberta acompanha placar, cronômetro e
substituições em tempo real. O indicador no canto inferior esquerdo mostra
`salvando` e avisa `sem conexão` quando a gravação falha (ela é repetida sozinha).

---

## O que esperar deste ambiente

É um ambiente de **teste**, e algumas coisas são propositalmente frouxas:

- **Sem verificação de conta.** Usuário e senha viram `usuario@raxa.app` internamente (domínio fictício; precisa ter TLD real porque o Supabase recusa `.local`).
  Não existe recuperação de senha: senha perdida, conta perdida.
- **Papel de escrita só na interface.** As ações de ADMIN sobre contas
  (aprovar pedido, vincular, remover, listar) valem no servidor
  (`is_league_admin` lê os jogadores em `league_players`), mas o `save_parts`
  só exige ser **membro**: qualquer membro consegue, pela API, gravar a liga
  inteira. É deliberado por ora — jogador também grava (contestar, assumir o
  próprio perfil), e separar o que cada papel pode mudar exige validar o
  conteúdo do diff, que é o esquema relacional de [Banco de dados](banco-de-dados.md).
- **Última gravação vence, por entidade.** Duas pessoas mexendo ao mesmo tempo: quem
  gravar depois, com a versão certa, fica; quem estava com a versão velha recebe o
  delta do servidor, perde a alteração local **só nas partes que o outro também
  mexeu** e reenvia o resto (a tela avisa *"Atualizado por outra pessoa"*).
- **Sinal caindo na quadra é esperado — até 20 s.** A liga fica copiada no aparelho
  (localStorage, por conta); sem rede o app abre com a cópia e sobe o que ficou pendente
  quando a rede volta. Cada pedido ao servidor tem prazo de 12 s. Passados **20 s sem
  nenhum contato bom** (constatado pela batida de 5 s do racha ao vivo), o app vira **só
  leitura** até a conexão voltar — consistência entre os celulares vale mais (D-104).
  O que ainda exige rede é **entrar** (login) e a primeira carga de uma liga que o
  aparelho nunca viu.
- **Apagar liga é só do dono, e só sem outros membros** (policy `leagues_delete` +
  função `has_other_members`, D-105). Quem não é dono só sai.
- **O projeto gratuito do Supabase hiberna** depois de ~7 dias sem nenhum acesso.
  O primeiro acesso depois disso demora alguns segundos a mais. Nada se perde.

---

## Testes

```bash
python scripts/test.py    # motor: rating, patentes, trechos, estatísticas
python scripts/smoke.py   # todas as telas e fluxos, num DOM falso
python scripts/sync.py    # contas, RLS, trava otimista e tempo real (Supabase falso)
python scripts/layout.py  # estrutura do HTML gerado (tags, botões aninhados)
python scripts/visual.py  # opcional: Chrome/Edge headless, salva prints
```

`sync.py` roda contra um Supabase de mentira em memória, então não precisa de rede
nem de projeto configurado.
