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
   [`supabase/schema.sql`](supabase/schema.sql) → **Run**.
   Cria as tabelas, a RLS, as funções e liga o Realtime. Pode rodar de novo sem quebrar.
   Se você já tinha aplicado uma versão anterior, rode de novo: a versão atual
   adiciona `league_requests` (entrada por código passa por aprovação do admin),
   as funções de contas da liga, e
   **remove a policy de UPDATE direto** em `leagues` — toda gravação passa pelo
   `save_league` (compare-and-swap), então um cliente não consegue mais pular a
   trava de versão gravando direto na tabela.

3. **Authentication → Sign In / Providers → Email**:
   - **Confirm email**: **desligado**  ← sem isso ninguém entra, porque o e-mail é fictício
   - **Allow new users to sign up**: ligado

4. **Project Settings → API**, copie:
   - **Project URL**
   - chave **anon public**

5. Cole as duas em [`config.js`](config.js):

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
3. Aba **Ajustes** → o **código de convite** de 6 letras está no topo. Compartilhe.
4. Cada pessoa cria a conta dela e usa **Entrar com um código**. Isso gera um
   **pedido**: o admin aprova em **Jogadores → Membros** e a liga aparece para a
   pessoa na hora (ela vê "Aguardando aprovação" na home até lá).
5. Em **Jogadores**, cada um abre o próprio nome e toca em **assumir perfil** para
   vincular a conta ao jogador.

Com o racha rolando, quem está com a tela aberta acompanha placar, cronômetro e
substituições em tempo real. O indicador no canto inferior esquerdo mostra
`salvando` e avisa `sem conexão` quando a gravação falha (ela é repetida sozinha).

---

## O que esperar deste ambiente

É um ambiente de **teste**, e algumas coisas são propositalmente frouxas:

- **Sem verificação de conta.** Usuário e senha viram `usuario@raxa.app` internamente (domínio fictício; precisa ter TLD real porque o Supabase recusa `.local`).
  Não existe recuperação de senha: senha perdida, conta perdida.
- **Permissão de papel só na interface.** Os papéis (admin, editor, lançador,
  jogador) mudam o que a tela oferece, mas no banco **qualquer membro da liga
  consegue gravar a liga inteira** — a RLS protege a fronteira entre ligas, não
  dentro delas. Aplicar papel no servidor exige o esquema relacional de
  `BANCO-DE-DADOS.md`.
- **Última gravação vence, por liga.** Duas pessoas mexendo ao mesmo tempo: quem
  gravar depois, com a versão certa, fica; quem estava com a versão velha recebe o
  estado do servidor e perde a alteração local (a tela avisa
  *"Atualizado por outra pessoa"*). Na prática só uma pessoa conduz o racha.
- **Não funciona offline.** O protótipo funcionava; esta versão precisa de rede.
  Se a quadra não tiver sinal, é um problema real a resolver antes de valer como produto.
- **O projeto gratuito do Supabase hiberna** depois de ~7 dias sem nenhum acesso.
  O primeiro acesso depois disso demora alguns segundos a mais. Nada se perde.

---

## Testes

```bash
python scripts/test.py    # motor: rating, patentes, trechos, estatísticas
python scripts/smoke.py   # todas as telas e fluxos, num DOM falso
python scripts/sync.py    # contas, RLS, trava otimista e tempo real (Supabase falso)
```

`sync.py` roda contra um Supabase de mentira em memória, então não precisa de rede
nem de projeto configurado.
