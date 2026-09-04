# Conceitos — o problema e a nomenclatura

> Parte da documentação do Raxa — índice em [docs/README.md](../README.md).

## 1. O problema

Todo racha tem os mesmos três atritos:

1. **Dividir os times leva 10 minutos** e sempre gera discussão ("esse time tá muito forte").
2. **Ninguém registra nada.** No fim do ano ninguém sabe quem ganhou mais, quem fez mais gol, quem evoluiu.
3. **Registrar dá trabalho.** Um racha que troca a cada 2 gols ou 7 minutos tem **10 a 15 partidas por noite**. Qualquer app que peça mais de 2 toques por partida morre no primeiro dia.

A regra de ouro do produto:

> **Ninguém precisa dizer quem ganhou.**
> Você marca os gols enquanto eles acontecem (1 toque cada) e toca em **Fim**. O placar decide o resultado — inclusive o 0-0, que é empate. Autor do gol, substituições, nomes de time, goleiro: tudo opcional, nada bloqueia o fluxo.

## 2. Conceitos e nomenclatura

| Conceito | Nome adotado | O que é |
|---|---|---|
| Contexto de racha | **Liga** | O universo isolado de patentes. Todo jogador, ranking e histórico vive dentro de uma Liga. |
| O evento do dia | **Racha** (sessão) | "Quinta 20h, quadra do Zé". Agrupa as partidas daquela noite. |
| Confronto | **Partida** | Time A x Time B, do apito ao apito, com um placar. |
| Formação em campo | **Trecho** | O pedaço da partida em que os 10 (ou 8, ou 14) em quadra são exatamente os mesmos. Toda substituição fecha um trecho e abre outro. **É o trecho que move patente**; vitória e derrota, porém, são da partida. |
| Pessoa dentro da liga | **Jogador** | Perfil com patente, estatísticas e histórico. |
| Conta de verdade | **Usuário** | Login que pode *assumir* perfis de Jogador em Ligas diferentes. |

**Por que "Liga" e não "racha"?** Porque o nível não pertence ao evento, pertence ao grupo de pessoas. Se você joga terça no society e quinta no futsal com **as mesmas pessoas**, é a mesma Liga com dois rachas por semana. Se a galera de quinta é outra, é **outra Liga** — e o mesmo jogador terá patentes independentes nas duas. Isso é proposital: Ouro na pelada do trabalho não é Ouro no fut7 competitivo de domingo.

*Alternativas descartadas: Panela, Circuito, Roda, Comunidade, Grupo.*
