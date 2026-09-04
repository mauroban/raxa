# Documentação do Raxa — mapa

Um documento por assunto. Leia o que a pergunta pede; nada aqui precisa ser lido em ordem.

## Produto

Como o app se comporta e por quê, na linguagem de quem usa.

| Documento | Quando abrir |
|---|---|
| [conceitos.md](produto/conceitos.md) | Um termo não está claro: liga, racha, partida, trecho, patente, divisão, lançador… |
| [patentes.md](produto/patentes.md) | Qualquer coisa sobre nível: escada, cortes, motor de Elo, K, calibração, anti-ioiô, entrada de quem chega, goleiro, quem vê o quê, e **o que a patente garante** (medido) |
| [fluxo-do-racha.md](produto/fluxo-do-racha.md) | As telas do dia: presença, montagem de times, partida ao vivo, fim do racha |
| [regras-do-racha.md](produto/regras-do-racha.md) | As regras de quadra que o app segue: time cheio, fila do "de próximo", vencedor fica, goleiro, empate |
| [stats.md](produto/stats.md) | Painel, destaques do mês, rankings, duelos, parcerias, mínimo de partidas |
| [contestacao-e-correcao.md](produto/contestacao-e-correcao.md) | Revisar uma partida, corrigir, anular, e o que acontece com a liga depois |
| [contas-e-permissoes.md](produto/contas-e-permissoes.md) | Membro = jogador, entrada na liga, papéis, o que o admin pode |
| [principios.md](produto/principios.md) | Os princípios de produto que valem defender numa discussão (lista curta) |
| [requisitos-funcionais.md](produto/requisitos-funcionais.md) | RF-01 a RF-11 com prioridade, status e critério de aceite |
| [requisitos-nao-funcionais.md](produto/requisitos-nao-funcionais.md) | RNF-01 a RNF-11 com metas verificáveis |

## Técnico

Como está construído e como se opera.

| Documento | Quando abrir |
|---|---|
| [prototipo.md](tecnico/prototipo.md) | O que o `index.html` faz hoje, o que ainda não existe, como o backend está montado |
| [banco-de-dados.md](tecnico/banco-de-dados.md) | Modelo de dados: o esquema intermediário em uso e o alvo relacional |
| [deploy.md](tecnico/deploy.md) | Subir o ambiente (Supabase + GitHub Pages), rodar o SQL, testes |
| [estudos.md](tecnico/estudos.md) | As simulações com o motor real (`scripts/converge.py`, `confianca.py`, `consistencia.py`): o que cada uma mede e o número que ficou |

## Decisões

Por que cada coisa é do jeito que é. [decisoes/README.md](decisoes/README.md) tem o índice de todas (D-01 em diante) e a regra para registrar uma nova; as decisões em si ficam num arquivo por tema:
[motor de patente](decisoes/motor-de-patente.md) · [escada, calibração e palpite](decisoes/escada-calibracao-e-palpite.md) · [times, fila e goleiro](decisoes/times-fila-e-goleiro.md) · [partida e histórico](decisoes/partida-e-historico.md) · [stats e destaques](decisoes/stats-e-destaques.md) · [interface](decisoes/interface.md) · [contas e permissões](decisoes/contas-e-permissoes.md) · [dados, sync e código](decisoes/dados-sync-e-codigo.md).

## Fora daqui

- [`README.md`](../README.md) na raiz: o que o app é e como rodar os testes.
- [`CLAUDE.md`](../CLAUDE.md): notas de trabalho para o assistente (fluxo de publicação e este mapa em versão curta).
