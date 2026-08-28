# Raxa

App de patentes e times para futsal, fut7, society e pelada em geral.
Marque quem chegou, os times saem equilibrados sozinhos e **cada partida se registra com um toque** — sem ninguém precisar apontar quem venceu.

```
Abrir a URL no navegador (celular ou desktop), entrar com usuário e senha.
Sem build, sem app store — é uma página só.
```

Os dados ficam no Postgres (Supabase): a mesma liga abre em qualquer aparelho e o
racha em andamento aparece para todo mundo do grupo em tempo real. Para subir o seu,
veja **[DEPLOY.md](DEPLOY.md)** — dá para rodar inteiro no plano gratuito.

Na primeira tela (ou no rodapé da lista de ligas), **"Carregar o racha de sábado"** cria a liga já com a lista real (3 goleiros e 16 de linha), todo mundo no nível de entrada — ajuste quem quiser na aba Jogadores ou deixe as partidas de calibração resolverem.

---

## O que ele faz

- **Liga** = grupo com patentes próprias. A mesma galera em vários rachas = uma liga só.
- **Patentes** em vez de pontos: 5 patentes × 3 divisões (Madeira → Ferro → Bronze → Prata → Ouro). **O rating numérico existe por baixo e nunca é mostrado a ninguém** — e o admin pode fechar até a patente, deixando-a visível só para ele.
- **Duas patentes por pessoa**: uma de linha e uma de goleiro, independentes — e **quem nunca jogou numa das duas não tem patente nela**; se entrar naquela posição, começa do nível padrão. Quem veio para o gol se marca na presença, e isso muda a cada racha.
- **O que move a patente é o trecho, não a partida**: cada formação em campo conta como uma partida própria, com o placar contado a partir da substituição — o mesmo espírito do +/- da NBA. O que o seu time fez enquanto você estava no banco não te afeta.
- **Formato** 5v5, 6v6, 7v7 ou 11v11, e dois **modos** de racha: várias curtas com time de fora, ou uma partida única com 2 times fixos e reservas.
- **Times equilibrados** em um toque: no racha curto **todo time é cheio** (5v5 é 5v5) e quem sobra forma a **fila**. Ao fim de cada partida vale o "de próximo": quem ganhou fica, quem perdeu sai, a fila entra no lugar e alguns ficam para completar. Se um time ficar curto, o app completa com quem está na fila — sugerindo, e deixando você escolher. Entre arranjos igualmente equilibrados, o app separa quem já jogou junto em outros rachas.
- **Partida ao vivo**: gol em um toque, lista de gols com autor e remoção individual, substituição arrastando (ou tocando), pausar e cancelar (com confirmação), "chegou agora" para o atrasado, e **encerrar em 1 toque** com o resultado do placar — 0-0 vira empate, e com 3+ times o empate tira os dois de quadra.
- **Tela de próxima partida** entre um jogo e outro: qual é o confronto, a chance de cada lado e as duas escalações, editáveis ali mesmo antes do apito. Mudança de patente não aparece entre partidas — só no resumo do fim do racha.
- **Destaques do mês** na tela do racha: os três que mais venceram **além do esperado** nos últimos 30 dias (a conta desconta o nível dos dois times), artilheiro quando os gols têm dono, goleiro menos vazado e quem mais apareceu.
- **Stats**: painel com duelos (quem te ganha mais, quem você ganha mais), parcerias, ano a ano, e os rankings do racha no período. Suas partidas ficam marcadas no histórico.
- **Contestação**: qualquer um pode contestar uma partida; admin corrige, anula ou mantém — e a liga inteira é recalculada do zero, sem resíduo.

## Documentação

| Arquivo | Conteúdo |
|---|---|
| [DOCUMENTACAO.md](DOCUMENTACAO.md) | Como o produto funciona, o sistema de patentes, os números/duelos e as decisões de design |
| [REQUISITOS-FUNCIONAIS.md](REQUISITOS-FUNCIONAIS.md) | RF-01 a RF-11, com prioridade, status e critérios de aceite |
| [REQUISITOS-NAO-FUNCIONAIS.md](REQUISITOS-NAO-FUNCIONAIS.md) | RNF-01 a RNF-11, com metas verificáveis |
| [DECISOES.md](DECISOES.md) | O registro das decisões: o que foi decidido, por quê, o que foi descartado e onde vive |
| [REGRAS-DO-RACHA.md](REGRAS-DO-RACHA.md) | As regras de quadra: times cheios, fila do "de próximo", vencedor fica, quem completa, goleiros |
| [BANCO-DE-DADOS.md](BANCO-DE-DADOS.md) | Esquema da v2: contas, membros, convites, partidas, RLS e migração |

## Testes

O motor de patentes é feito de funções puras (sem DOM), então roda direto no Node:

```bash
python scripts/test.py     # motor: escada, equilíbrio, trechos, duas patentes, histerese, recálculo
python scripts/smoke.py    # interface: todas as telas e fluxos em um DOM falso
python scripts/layout.py   # estrutura do HTML gerado: tags, botões aninhados, restos de template
python scripts/visual.py   # navegador de verdade, tema escuro e claro: nada estourando, sobreposto ou pequeno demais (salva prints)
```

Requer `node` e `python` no PATH; o `visual.py` usa o Chrome ou o Edge instalado e é pulado se não achar nenhum. Todos extraem o código do próprio `index.html` — não há cópia de lógica para sair de sincronia.

## Estrutura

```
index.html   o app inteiro (HTML + CSS + JS, sem dependências)
scripts/     testes
*.md         documentação
```

## Estado

Ambiente de **teste** no ar: contas (usuário e senha, sem verificação), ligas por
código de convite, dados no Postgres e sincronização em tempo real entre celulares.
Cada liga é um documento `jsonb` numa linha de `leagues` — o motor (`splitStints`,
`computeElo`, `rebuildAll`) continua rodando no cliente, sem reescrita.

Ainda falta para virar produto: permissões aplicadas no servidor (hoje o papel
admin/editor/lançador é checado só na interface — quem é membro consegue gravar a
liga inteira), e a quebra do documento no esquema relacional de `BANCO-DE-DADOS.md`,
que é o que dá consulta, histórico e RLS por linha de verdade. Caminho em
`DOCUMENTACAO.md` (seção 8.1).
