# Contas, perfis e permissões

> Parte da documentação do Raxa — índice em [docs/README.md](../README.md).


## 1. Um membro é um jogador — e só um

A regra que organiza tudo nesta seção: **dentro de uma Liga, uma conta corresponde a exatamente um perfil de jogador.** Não existe conta com dois perfis na mesma Liga, nem perfil dividido entre duas contas. Isso é o que faz "quantas vezes eu joguei contra o Rodrigo" ter uma resposta única.

Fora dessa regra, tudo continua valendo: a mesma pessoa tem **patentes independentes em cada Liga**, e um perfil pode existir muito antes de a pessoa ter conta.

## 2. Perfil sem dono

Quando alguém cadastra "Bruninho" na tela de presença, nasce um **perfil sem dono**: existe, joga, acumula patente e estatística, mas não pertence a nenhuma conta. Esse é o caso normal — num racha de 16, metade nunca vai abrir o app.

Quando o Bruninho entra na Liga, ele vê os perfis sem dono e **assume o seu**, já com todo o histórico anterior. A partir daí acompanha as próprias patentes em todas as Ligas dele num lugar só. Se alguém assumir o perfil errado, o admin desfaz o vínculo com um toque e o perfil volta a ficar sem dono.

## 3. Entrar numa Liga: três caminhos, uma regra

| Caminho | Como é | Quando serve |
|---|---|---|
| **Link de convite** — *ainda não existe (v2)* | o admin gera o link e joga no grupo do WhatsApp; quem abre escolhe o próprio perfil e entra | começar uma Liga, chamar a galera toda de uma vez |
| **Código da Liga** | código curto de 6 caracteres (`RXA7Q2`), visível nos ajustes; quem digita **pede para entrar** e o admin aprova em Membros — **implementado** | alguém que ouviu falar do racha e quer entrar |
| **Busca dentro do app** — *ainda não existe (v2)* | o admin procura a pessoa por `@usuário` ou nome e convida direto — já apontando qual perfil é dela | o mais comum: a pessoa já joga há meses e só agora criou conta |

A regra única, nos três: **ninguém entra sem aceitar, e ninguém entra sem o admin querer.** Hoje só o código existe, e ele **gera pedido, não entrada** — o admin aprova em Membros. O link com vencimento, a entrada livre e o convite direto de uso único são desenho da v2.

Convidar já pode **reservar o perfil**: quem aceita cai direto no lugar certo — *"você é o Bruninho, 42 partidas, Prata 2"* — em vez de escolher numa lista e errar.

## 4. O admin manda nos membros

Controle total, sem meio-termo, porque um racha tem dono:

- convidar, revogar convite, aprovar ou recusar pedido;
- **vincular e desvincular** um perfil de uma conta;
- trocar o papel de qualquer membro;
- **remover um membro** — o jogador e todo o histórico dele **ficam**; só o acesso sai;
- cadastrar jogador sem conta nenhuma (o caso normal);
- passar o admin adiante — uma Liga nunca fica sem admin;
- **apagar a Liga** — só o **dono** (quem criou), só quando **não há nenhum outro membro**, e digitando o nome da Liga; a regra vale também no banco (D-105). Quem não é dono tem "Sair da liga" no mesmo lugar.

Toda ação de membro fica registrada: quem fez, em quem, quando.

## 5. Papéis

| Papel | Pode |
|---|---|
| **Admin** | Tudo: configurar a liga (os ajustes são só dele — os outros papéis veem o formato e a aparência, sem controles, D-128), revisar/corrigir/anular partidas, cadastrar e **arquivar** jogadores (remover de vez só cadastro sem histórico — D-128), juntar cadastros, dar papéis (rebaixar a Jogador é o que tira o peso das opiniões de alguém — D-121), ver na ficha tudo que um membro opinou sobre os outros (D-124) |
| **Moderador** | O que o lançador faz, mais corrigir o resultado de partidas (anular, revisar contestação e apagar são só do admin) |
| **Lançador** | Conduzir o racha: presença, times, partidas, gols, cadastrar jogador, **editar nome, descrição e hábito de gol** de qualquer jogador (D-128) — e **opinar sobre o nível** de entrada de qualquer um (como moderador e admin) |
| **Jogador** | **Padrão de quem entra.** Vê ranking, histórico e as próprias estatísticas; vincula o próprio perfil; pode contestar; pode dar opinião sobre nível, mas ela **só passa a valer** quando for Lançador ou acima (D-121). Não lança nada |

O padrão de quem entra é **Jogador**: só olha. O admin dá **Lançador** a quem conduz o racha (quem está com o celular na mão). Conta ainda sem perfil vinculado também é tratada como Jogador.

**Visibilidade das patentes** (seção 3.8) é decisão do admin: todo mundo vê, ou só ele. Em v1, sem backend, isso vale por aparelho — a checagem já é por papel, e é a mesma que o servidor vai aplicar na v2. No app hoje o que está de fato aplicado é: **admin** = revisar/anular/apagar partida, dar papel, vincular/desvincular conta de outra pessoa, gerenciar contas da liga; **editor** = corrigir resultado de partida (nível é só admin); **lançador** = tudo que é conduzir o racha; **jogador** = só leitura (a checagem é central, no despachante de ações — `ACOES_LANCAR`/`ACOES_ADMIN`).

**Contas sem jogador.** Quem entra na liga pelo código vira *conta* antes de ser *jogador*. Para o admin, o card **Pendências** (aba Jogadores) lista as contas — com jogador ou sem —, e é ali que ele vincula a conta a um perfil sem dono, cria um jogador com o nome da conta ou tira a conta da liga (o jogador e o histórico ficam). Os outros membros veem só os jogadores e se cada um tem perfil atrelado.

## 7. Arquivar jogador (D-128)

**Não existe mais "remover jogador" para quem tem histórico.** Remover apagava o cadastro, as opiniões dele e sobre ele, e recalculava o nível de todo mundo (a expectativa é do time: sem ele nas partidas em que jogou, a conta de todos muda). No lugar, **Arquivar** (só o admin, na ficha): a pessoa ganha a marca de arquivada e some da presença, do "Chegou", dos times, das escadas, de *Minhas opiniões* e das listas de escolha — mas o cadastro, as duas patentes, as opiniões recebidas e as dadas, as partidas e as presenças ficam como estão. As opiniões que ela deu deixam de valer enquanto arquivada (quem saiu não conta, D-121) e voltam a valer ao reativar. O histórico continua mostrando o nome dela. Quem está em quadra não se arquiva (tire da partida primeiro).

**Reativar** fica na própria ficha (faixa "arquivado em …") e os arquivados aparecem num card dos ajustes do admin. **Apagar cadastro** só existe para quem **nunca jogou nem esteve em racha nenhum** — cadastro por engano; para os outros, o botão nem aparece, e a ação recusa.

**A ficha, de cima para baixo:** cabeçalho com o **nome editável no próprio nome** e, embaixo, uma **descrição** discreta (apelido, "amigo do Matheus", como chegou — até 120 caracteres; quem lança edita, os outros leem) → nível (cartões Linha/Gol, entrada, "Dar a minha opinião") → números → as linhas de **costuma ir ao gol** (quem lança), **conta** e **permissão** (só admin) → Cancelar/Salvar → bloco **Admin** (opiniões que deu, juntar cadastros, arquivar, apagar). Quem pode o quê: **nome, descrição e hábito de gol, quem lança** (lançador, moderador, admin); **qualquer outra alteração** — permissão, arquivar, reativar, apagar — **só o admin**; a conta, o próprio dono ("Sou eu" só aparece para quem ainda não tem perfil nesta liga; desvincular, o dono ou o admin).

**Ajustes por papel.** Os controles da liga (quem vê os níveis, nomes dos níveis, alvo, trecho mínimo, contestação, exportar/importar) são só do admin. Os outros papéis veem o formato e o alvo da liga, como o nível anda, a aparência do aparelho e "Sair da liga". *Minhas opiniões* não diz mais se a opinião da pessoa vale ou não: isso é conta da liga, não dela.
