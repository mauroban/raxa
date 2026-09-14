# Decisões · Chamada e confirmação de presença

> A lista do racha no app: agenda semanal, confirmar na linha ou no gol, espera, quem lança confirma
> pelos outros, e como um membro novo diz quem ele é. Produto em
> [Confirmação de presença](../produto/confirmacao-de-presenca.md).
> Índice de todas as decisões e regra de registro em [README.md](README.md).

---

<a id="d-165"></a>
### D-165 · Cada um se confirma pelo app: agenda semanal, linha ou gol, espera derivada, hora do servidor
**Quando:** 2026-09-14.
**O quê:** a liga ganha uma **chamada** recorrente (`cfg.chamada`: dia da semana, hora, vagas na
linha, vagas no gol, abre N dias antes, datas puladas). Na aba Racha, fora do dia, o cartão
**Próximo racha** mostra a data, "Vou"/"Vou no gol" para quem tem perfil, as duas listas numeradas
com o corte e a espera, **Compartilhar** (texto para o grupo), **+ Confirmar alguém** para quem
lança e **Cancelar este racha** para o admin. Cada confirmação é uma linha própria no banco
(`league_rsvps`: `{id, dia, pid, papel, by, t, at}`), sincronizada como as outras entidades; o
`at` é **carimbado pelo servidor** em `save_parts` quando a linha chega sem ele, e as linhas
gravadas voltam na resposta para o aparelho ficar com o carimbo certo. A **espera não é estado**:
é quem passou do máximo na ordem do `at`. Trocar de papel apaga o `at` (vai para o fim da outra
lista). No dia, **Iniciar racha** pré-marca a presença com quem está dentro (goleiro com a luva),
sobe a espera na grade sem marcar, e o racha guarda `chamada` (a data). Sem sinal há 20 s o botão
recusa (D-104).
**Por quê:** a lista no WhatsApp é a parte mais trabalhosa do racha e a que mais gera discussão
("eu confirmei antes"). Uma linha por pessoa evita o conflito de dois celulares gravando o mesmo
documento (o `live` já mostrou o custo disso, D-104); a hora do servidor tira o relógio do celular
da disputa; a espera derivada dispensa promoção manual e corrida no banco. Quem lança confirmar
pelos outros é o que impede a lista do grupo de continuar em paralelo enquanto nem todo mundo tem
o app.
**Descartado:** guardar a lista dentro da sessão do racha (documento único, conflito entre
celulares, e o racha ainda não existe quatro dias antes); lista de espera como campo próprio
(precisaria de promoção manual e admite dois estados inconsistentes); notificação (é página web —
o texto compartilhado no grupo faz esse papel); racha extra fora da agenda e lembrete (depois, se
o uso pedir); estatística de "furou" (volta depois, derivada de lista × presença).
**Onde:** motor `chamadaDef`, `proximaChamada`, `chamadaCancelada`, `listaChamada`, `minhaChamada`,
`confirmar`, `desconfirmar`, `textoChamada` (acima de `@@FIM-DO-MOTOR@@`); telas `chamadaCard`,
`cfgChamadaCard`, `chamadaResumo`; ações `A.vou`/`naoVou`/`chamadaChip`/`chamadaTroca`/
`chamadaTirar`/`chamadaAlguem`/`chamadaAdd`/`chamadaShare`/`chamadaOn`/`chamadaDow`/
`chamadaCancelar`/`chamadaVoltar`; `A.startRacha` (pré-marca), `viewPresenca` (ordem), `A.endRacha`
(`chamada` na sessão); sync: entidade `rsvps` em `ENT`, `diffParts`, `applyDelta`, `aplicaRsvps`,
`cacheSnapDiff`; SQL: `league_rsvps`, `league_delta`, `save_parts` (carimbo e retorno), `league_size`
— **rodar o SQL de novo**. Testes: `scripts/test.py` [20], `scripts/smoke.py` (bloco D-165/D-166),
`scripts/sync.py` (carimbo e realtime), `scripts/visual.py` telas 22 e 23 ·
[Confirmação de presença](../produto/confirmacao-de-presenca.md) ·
[Fluxo do racha §1](../produto/fluxo-do-racha.md) · [Banco de dados](../tecnico/banco-de-dados.md).

<a id="d-166"></a>
### D-166 · "Quem é você nesta liga?": o membro escolhe o próprio perfil ou cria o seu com apelido
**Quando:** 2026-09-14.
**O quê:** membro logado sem perfil vinculado nesta liga vê, no topo da aba Racha, o cartão **Quem é
você nesta liga?** com os perfis sem dono (busca a partir de nove nomes, ordem de quem mais joga).
Toque → folha "É você? · Sou eu" → vínculo (`owner`), registrado no log como `link`. **Não estou na
lista — criar meu jogador** abre a folha com o **apelido** (preenchido com o usuário da conta, livre
por liga, até 40 caracteres) e "costumo ir ao gol"; nasce sem nível, papel Jogador, `owner` da
conta, log `newPlayer`. Nome repetido recusa. O cartão some quando há perfil; sem perfil não há
"Vou".
**Por quê:** na prática o caminho "admin aprova e depois vincula em Pendências" travava a pessoa
justamente na hora de confirmar presença — e o admin não sabe qual apelido cada um usa. A pessoa
sabe quem ela é. O apelido por liga já era o modelo (o nome do jogador é da liga), só faltava a
pessoa poder escolhê-lo.
**Descartado:** escolher o perfil no pedido de entrada (exigiria expor a lista de jogadores a quem
ainda não é membro, e uma RPC só para isso); entrada automática pelo link (D-26/D-132 continuam:
o admin aprova, e depois a pessoa se resolve sozinha).
**Onde:** `quemSouCard`, `A.euSou`/`euSouOk`/`euNovo`/`euNovoOk` em `index.html` · teste em
`scripts/smoke.py` (bloco D-165/D-166) e `scripts/visual.py` tela 23 ·
[Contas e permissões §2](../produto/contas-e-permissoes.md) ·
[Confirmação de presença §5](../produto/confirmacao-de-presenca.md).
