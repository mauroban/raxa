# Requisitos não funcionais — Raxa

Produto em [docs/produto](./) (índice em [docs/README.md](../README.md)) · modelo de dados da v2 em [Banco de dados](../tecnico/banco-de-dados.md).

Cada requisito traz uma **meta verificável**. Onde a meta ainda não é atingível na versão atual (com backend), está marcado o que fica para a v2.

---

## RNF-01 — Usabilidade (o requisito mais importante do produto)

| # | Requisito | Meta |
|---|---|---|
| RNF-01.1 | Fechar uma partida, depois dos gols já marcados | **1 toque** (`✓ Fim`), sem digitar nada e sem apontar vencedor |
| RNF-01.2 | Do "chegamos na quadra" ao "primeira partida começando" | **≤ 60 segundos** com 14 presentes |
| RNF-01.3 | Marcar um gol | **1 toque**; o autor é opcional e some sozinho em 6 s |
| RNF-01.4 | Nenhum campo de texto obrigatório durante o racha | 0 campos |
| RNF-01.5 | Todo registro feito na quadra pode ser desfeito | gol: remoção individual · partida: "Desfazer a última", com as patentes · substituição: refazer a troca ao contrário (2 toques) · cancelar a partida em andamento é irreversível, por isso pede confirmação |
| RNF-01.6 | Operação com uma mão só, em pé, com o celular na vertical | alvos de toque ≥ 44 px; ações primárias na metade inferior — na partida, o placar (que é o botão de gol) ocupa ~31vh logo acima da barra fixa |
| RNF-01.7 | Nenhuma tela exige rolagem para completar a ação principal | ações primárias em barra fixa no rodapé |
| RNF-01.8 | Erro de toque é recuperável sem perder o racha | confirmação apenas em ações irreversíveis |
| RNF-01.9 | Curva de aprendizado | um novo lançador consegue registrar a primeira partida **sem tutorial** |
| RNF-01.10 | Interromper e descartar a partida em andamento | pausar em 1 toque; cancelar em 1 toque + confirmação |

**Como verificar:** cronometrar um racha real de 12 partidas; contar toques por partida. Fora os gols (1 toque cada, no momento em que acontecem), nenhuma partida pode exigir mais de 1.

---

## RNF-02 — Desempenho

| # | Requisito | Meta |
|---|---|---|
| RNF-02.1 | Abertura do app (carga fria, arquivo local) | **< 1 s** |
| RNF-02.2 | Resposta a qualquer toque | **< 100 ms** percebidos |
| RNF-02.3 | Recálculo integral da Liga (rebuild) | **< 200 ms** para 50 jogadores × 1.000 partidas |
| RNF-02.4 | Montagem de times equilibrados | **< 50 ms** para 30 presentes |
| RNF-02.5 | Tamanho do app | 1 arquivo, **< 180 KB**, sem dependências externas obrigatórias (hoje: ~165 KB) |
| RNF-02.6 | Consumo de bateria durante o racha | sem polling; cronômetro em 1 tick/segundo |
| RNF-02.7 | Painel de números (duelos e parcerias de todo mundo, do zero) | **< 300 ms** para 400 partidas — **coberto por teste** |

---

## RNF-03 — Disponibilidade e operação offline

| # | Requisito | Meta |
|---|---|---|
| RNF-03.1 | O app funciona **sem internet**, do início ao fim do racha | **revisto (D-104):** abre e mostra tudo sem rede (cópia no aparelho, D-102), mas lançar sem sinal vale por 20 s — depois é só leitura até voltar. Consistência entre celulares vale mais que lançar às cegas |
| RNF-03.2 | Nenhum recurso externo é obrigatório para funcionar | fontes web degradam para fontes do sistema |
| RNF-03.3 | Fechar o app ou perder a bateria não perde o racha | estado gravado a cada ação |
| RNF-03.4 | Retomada do racha em andamento após reabrir | automática, sem perguntar nada |
| RNF-03.5 | A sincronização tolera ficar offline por toda a sessão | o que ficou pendente (até 20 s de lances) sobe ao reconectar ou ao reabrir o app; prazo de 12 s por pedido; batida de 5 s ao vivo (D-102/D-104) |

---

## RNF-04 — Confiabilidade e integridade dos dados

| # | Requisito | Meta |
|---|---|---|
| RNF-04.1 | O motor de patentes é determinístico | mesmas partidas ⇒ mesmo resultado, sempre |
| RNF-04.2 | Recálculo do zero é idêntico ao cálculo incremental | igualdade exata de rating, patente, partidas, vitórias e gols — **coberto por teste** |
| RNF-04.3 | Anular e reativar uma partida devolve o estado exato anterior | igualdade exata — **coberto por teste** |
| RNF-04.4 | Nenhuma operação pode fazer um jogador sumir de um time ou aparecer em dois | invariante verificado na montagem — **coberto por teste** |
| RNF-04.5 | Dados corrompidos no armazenamento não travam o app | leitura protegida, com queda para estado inicial |
| RNF-04.6 | O histórico é a fonte da verdade; patentes são derivadas dele | nenhum estado de patente sobrevive a um rebuild |
| RNF-04.7 | Uma partida gravada é imutável quanto ao peso: ela carrega o modo do racha em que foi jogada | mudar configuração da liga não altera resultado passado — **coberto por teste** |
| RNF-04.8 | O histórico é auto-suficiente para recalcular a liga inteira sem depender da configuração atual | modo, sessão, escalações, pesos e resultado ficam na própria partida |
| RNF-04.9 | Estatísticas (duelos, parcerias, presenças, aproveitamento, destaques do mês) não são gravadas em lugar nenhum | calculadas do histórico a cada abertura da tela; a partida guarda só fatos — deltas e acima do esperado são refeitos por `rebuildAll` e nem sobem para o banco (D-63) — **coberto por teste** |

**Estado atual:** suíte de testes cobrindo escada de patentes, equilíbrio, formato e goleiros, expectativa/simetria do rating, **trechos** (corte por substituição, descarte do trecho curto, peso proporcional, placar próprio), calibração por trilha, histerese, rebuild/anulação, **duas patentes por jogador** e **separação de duplas repetidas**; mais um smoke test que percorre todas as telas e falha se qualquer uma quebrar.

---

## RNF-05 — Privacidade do rating

| # | Requisito | Meta |
|---|---|---|
| RNF-05.1 | O rating numérico não aparece em nenhuma tela, para nenhum papel | 0 ocorrências na interface |
| RNF-05.2 | Os pontos de corte entre patentes não são expostos | 0 ocorrências na interface |
| RNF-05.3 | A variação de rating de uma partida não é exibida | apenas "subiu/caiu de patente", e só no resumo do fim do racha |
| RNF-05.4 | Nenhuma ordenação ou barra de progresso deixa o rating inferível | ordenação por patente → aproveitamento → nome |
| RNF-05.5 | O rating só circula em dados técnicos (backup/servidor) | fora do motor, o único lugar onde ele existe é o export em JSON — quem abrir o backup vê o número, e isso é aceito |
| RNF-05.6 | A chance esperada é exibida por **confronto**, nunca por pessoa | uma % por lado, derivada da média dos que estão em quadra; nenhum rating individual é exibido ou isolável em uma tela |
| RNF-05.7 | Com "patentes só para o admin", nenhuma patente aparece para os demais papéis | 0 badges de patente em qualquer tela, para quem não é admin (o admin continua vendo em todas) |

**Como verificar:** buscar por `elo`, `rating` e `pts` em todo o texto renderizado da interface — não pode haver nenhum valor numérico de rating.

---

## RNF-06 — Segurança (v2, com backend)

| # | Requisito | Meta |
|---|---|---|
| RNF-06.1 | Permissões aplicadas no servidor, nunca só na interface | políticas por linha (RLS) |
| RNF-06.2 | Só membros da Liga leem os dados dela | isolamento por `liga_id` |
| RNF-06.3 | Alterações sensíveis são auditáveis | quem lançou, quem corrigiu, quem anulou, quando |
| RNF-06.4 | Reivindicação de perfil não pode ser usada para roubar identidade | vínculo revogável por admin + registro |
| RNF-06.5 | Dados pessoais mínimos | apenas nome/apelido, `@usuário` e e-mail de login |
| RNF-06.6 | Link de convite é credencial: vence e pode ser revogado | validade padrão de 7 dias, revogação imediata, uso contado |
| RNF-06.7 | Convite direto e pedido por código não colocam ninguém dentro sozinhos | entrada exige aceite da pessoa **e** decisão do admin |
| RNF-06.8 | "Um membro é um jogador" é invariante de banco, não de interface | `unique (liga_id, player_id)` em `liga_members` |

---

## RNF-07 — Compatibilidade e portabilidade

| # | Requisito | Meta |
|---|---|---|
| RNF-07.1 | Funciona em navegador de celular Android e iOS atualizados | Chrome e Safari, 2 últimas versões |
| RNF-07.2 | Layout responsivo de 320 px a desktop | sem rolagem horizontal |
| RNF-07.3 | Sem etapa de build, instalação ou servidor para rodar | abrir o arquivo já funciona |
| RNF-07.4 | Os dados são exportáveis em formato aberto e legível | JSON |
| RNF-07.5 | Instalável como app na tela inicial (PWA) | **v2** |

---

## RNF-08 — Acessibilidade e legibilidade em quadra

| # | Requisito | Meta |
|---|---|---|
| RNF-08.1 | Legível sob luz forte de quadra | contraste ≥ 4.5:1 em texto de conteúdo |
| RNF-08.2 | Placar legível a um braço de distância | numeral do placar ≥ 60 px |
| RNF-08.3 | A informação nunca depende só da cor | patente sempre com nome e divisão escritos |
| RNF-08.4 | Retorno tátil nas ações de placar | vibração curta quando disponível |
| RNF-08.5 | Legível no pior caso: celular no sol, quadra descoberta | **tema claro é o padrão**; escuro e automático (pelo sistema) nos ajustes, por aparelho — verificado por teste visual nos dois temas |
| RNF-08.6 | Navegação e ações principais ao alcance do polegar | abas em barra fixa embaixo; barra de ação logo acima; alvos de toque ≥ 44 px |

---

## RNF-09 — Escalabilidade

| # | Requisito | Meta |
|---|---|---|
| RNF-09.1 | Uma Liga suporta o tamanho real de um racha grande | 50+ jogadores cadastrados, 30 presentes |
| RNF-09.2 | Histórico de longo prazo sem degradar a interface | 2.000+ partidas por Liga (as metas de tempo de RNF-02.3 e RNF-02.7 hoje são medidas em 1.000 partidas e 400 — falta medir nesta escala) |
| RNF-09.3 | Várias Ligas por usuário | 10+ |
| RNF-09.4 | Noite típica de racha rápido | 10 a 15 partidas em 2 h (com trechos, 15 a 25 unidades de rating) sem perda de fluidez |

---

## RNF-10 — Manutenibilidade

| # | Requisito | Meta |
|---|---|---|
| RNF-10.1 | O motor de patentes e de estatísticas é isolado do DOM e testável fora do navegador | funções puras: `splitStints`, `stintPart`, `computeElo`, `updateRank`, `applyMatch`, `rebuildAll`, `buildTeams`, `pairCounts`, `statsLiga`, `encontros`, `statsAnos` |
| RNF-10.2 | O motor pode ir para o servidor sem reescrita | mesma função roda em Node — **é assim que os testes rodam hoje** |
| RNF-10.3 | Regras de negócio configuráveis por Liga, sem alterar código | alvo (gols/minutos), trecho mínimo, limite e efeito da contestação, visibilidade das patentes, nomes das patentes, formato (NvN) e modo padrão do racha |
| RNF-10.4 | Mudança de esquema de dados não quebra ligas antigas | versão no estado + normalização na carga — **feito** |
| RNF-10.5 | Suíte de testes executável em um comando | `python scripts/test.py` (motor) e `python scripts/smoke.py` (todas as telas em DOM falso) — ambos extraem o código do próprio `index.html` |
| RNF-10.5b | Regressão visual automatizada: nenhum elemento estourando a tela, sobreposto ou com alvo de toque menor que 32px, verificado em navegador real | `python scripts/visual.py` em 9 telas × 2 larguras (360 px simulado e 500 px) |
| RNF-10.6 | Nenhuma tela pode ficar em branco por erro de renderização | render protegido, com tela de erro e opção de recomeçar |
| RNF-10.7 | Dados gravados por versões anteriores são migrados na carga | normalização automática do estado, sem intervenção do usuário |

---

## RNF-11 — Idioma e conteúdo

| # | Requisito | Meta |
|---|---|---|
| RNF-11.1 | Interface em português do Brasil, com vocabulário de racha | "racha", "peladeiro", "vencedor fica" |
| RNF-11.2 | Nomes de patente adaptáveis ao vocabulário de cada grupo | editáveis por Liga |
| RNF-11.3 | O tom nunca humilha quem está na base da escada | nomes padrão sem xingamento; sem "pior jogador" |
