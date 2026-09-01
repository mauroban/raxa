# -*- coding: utf-8 -*-
"""
Smoke test de interface do Raxa: roda index.html inteiro em um DOM falso,
percorre todas as telas e fluxos, e falha se alguma tela quebrar.
Cobre tambem a leitura de dados gravados por versoes anteriores do app.

Uso:  python scripts/smoke.py
"""
import io, os, subprocess, sys
SP = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.tmp')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.path.isdir(SP) or os.makedirs(SP)
html = io.open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
js = html.split('<script>')[1].split('</script>')[0]

stub = r"""
/* -------- DOM falso -------- */
class El{
  constructor(id){this.id=id;this._html='';this.textContent='';this.dataset={};this.style={};
    this.classList={_s:new Set(),add(){},remove(){},toggle(){},contains(){return false}};}
  set innerHTML(v){this._html=String(v);if(/undefined|NaN|\[object Object\]/.test(this._html))
    console.log('  ATENCAO: html suspeito em #'+this.id+' -> '+this._html.match(/.{0,80}(undefined|NaN|\[object Object\]).{0,40}/)[0]);}
  get innerHTML(){return this._html}
  querySelector(){return null} querySelectorAll(){return []} closest(){return null}
  focus(){} click(){} appendChild(){} addEventListener(){}
}
const els={};
['#app','#bar','#sheet','#scrim','#toast'].forEach(s=>els[s]=new El(s));
global.document={
  querySelector:s=>els[s]||null,
  querySelectorAll:()=>[],
  addEventListener:()=>{},
  createElement:()=>new El('tmp'),
};
global.window={};
global.navigator={};
const store={};
global.localStorage={getItem:k=>store[k]||null,setItem:(k,v)=>store[k]=v};
global.confirm=()=>true;
global.prompt=()=>'Mauro';
global.alert=()=>{};
"""

smoke = r"""
/* -------- smoke -------- */
let fails=0;
let saiuNoMeio=null;
function step(label,fn){
  try{fn();console.log('  ok: '+label)}
  catch(e){fails++;console.log('  QUEBROU em "'+label+'": '+e.message+'\n    '+String(e.stack).split('\n')[1])}
}
console.log('\n[smoke] telas e fluxo completo');
step('tela inicial (sem ligas)',()=>{S=defState();render()});
/* formato e modo sao fixos por liga (D-44): o roteiro muda o cfg direto,
   reproduzindo o que a acao antiga fazia */
const setFormat=v=>{const l=L();l.cfg.format=+v;if(l.live&&l.live.stage==='times')applyPlan(l,l.live);save();render()};
const setMatchMode=v=>{const l=L();l.cfg.matchMode=v;if(l.live)l.live.mode=v;
  if(v==='unica'){l.cfg.targetGoals=0;l.cfg.targetMin=50;l.cfg.winnerStays=false}
  else{l.cfg.targetGoals=2;l.cfg.targetMin=7;l.cfg.winnerStays=true}
  if(l.live&&l.live.stage==='times')applyPlan(l,l.live);save();render()};
step('toda acao tem classificacao de papel',()=>{
  /* acoes fora dos dois conjuntos rodam para qualquer membro; as LIVRES sao
     as que (a) so olham/preferencia, (b) tem checagem interna de papel
     (fixResult, voidMatch, escSalvar, pdSave, acc*...), ou (c) sao de conta.
     Acao nova cai aqui ate alguem classifica-la de proposito. */
  const LIVRES=new Set(['home','openLiga','tab','closeSheet','newLiga','novaSheet','novaOpt','pickPat','togGk',
    'contest','review','revSec','editEsc','escPick','escGk','escDel','escSwap','escAdd','escAddDo','evPick','evSet','evDel',
    'novaTroca','ntSet','ntOk','escSalvar','escDescartar','goalScorerM','setGoalScorerM','fixResult','voidMatch',
    'clearDisputes','delMatch','pSheet','pdRank','pdBump','pdGk','pdRole','pdOwner','pdCancel','pdSave','rankRole',
    'statsPer','statsTab','statsSemGk','rachaTime','statsSec','histMine','histRacha','statsWho','setStatsWho','duelo',
    'toggleDispute','setTheme','export','import','authMode','doLogin','doSignup','logout','demo','joinLiga','doJoin','statsInv','ppPage',
    'cancelPend','delLiga','copyCode','doImport','accSheet','accLink','accUnlink','accCreate','accApprove','accReject','accRemove']);
  const todas=Object.keys(A);
  const soltas=todas.filter(k=>!ACOES_LANCAR.has(k)&&!ACOES_ADMIN.has(k)&&!LIVRES.has(k));
  if(soltas.length)throw new Error('acao sem classificacao de papel (poe em ACOES_LANCAR/ADMIN ou em LIVRES aqui): '+soltas.join(', '));
  const fantasmas=[...ACOES_LANCAR,...ACOES_ADMIN].filter(k=>!(k in A));
  if(fantasmas.length)throw new Error('acao listada nos conjuntos que nao existe em A: '+fantasmas.join(', '));
});
step('criar liga de exemplo',()=>A.demo());
step('iniciar racha',()=>A.startRacha());
step('marcar todos presentes',()=>{L().players.forEach(p=>A.pres({dataset:{id:p.id}}));render()});
step('quem veio de goleiro sai do cadastro e vira escolha do dia',()=>{
  const lv=L().live;
  if(lv.gkToday.length!==3)throw new Error('esperava 3 goleiros marcados, veio '+lv.gkToday.length);
  const alguem=L().players.find(p=>!p.gk).id;
  A.presGk({dataset:{id:alguem}});
  if(lv.gkToday.indexOf(alguem)<0)throw new Error('nao marcou goleiro do dia');
  A.presGk({dataset:{id:alguem}});
  if(lv.gkToday.indexOf(alguem)>=0)throw new Error('nao desmarcou');
});
step('chip de presenca mostra o nivel do papel de hoje: gol com luva acesa, linha apagada (D-81)',()=>{
  const l=L(),lv=l.live,p=l.players.find(x=>!x.gk&&temPatente(l,x,'L'));
  if(!p)throw new Error('precisa de alguem de linha com nivel');
  p.G.def=true;p.G.rank=TOP;p.G.elo=stepMid(TOP);        /* Diamante 3 no gol, so para o teste */
  const lRank=rankLabel(l,p.L.rank),gRank=rankLabel(l,TOP);
  const chip=()=>{const h=viewPresenca(l,lv);const i=h.indexOf('data-id="'+p.id+'"');return h.slice(i,i+600)};
  if(chip().indexOf(gRank)>=0||chip().indexOf(lRank)<0)throw new Error('luva apagada: esperava '+lRank);
  A.presGk({dataset:{id:p.id}});
  if(chip().indexOf(gRank)<0||chip().indexOf(lRank)>=0)throw new Error('luva acesa: esperava '+gRank+', veio '+chip());
  A.presGk({dataset:{id:p.id}});
  if(chip().indexOf(lRank)<0)throw new Error('desmarcou e nao voltou para '+lRank);
  /* ainda nao marcado: vale o costume — quem costuma ir ao gol mostra o do gol */
  A.pres({dataset:{id:p.id}});
  if(lv.presentIds.indexOf(p.id)>=0)throw new Error('esperava tirar da presenca');
  if(chip().indexOf(lRank)<0)throw new Error('fora da presenca, sem costume de gol: esperava '+lRank);
  p.gk=true;
  if(chip().indexOf(gRank)<0)throw new Error('fora da presenca, costuma ir ao gol: esperava '+gRank);
  p.G.def=false;p.G.elo=l.cfg.startElo;p.G.rank=stepOf(p.G.elo);p.G.games=0;
  if(chip().indexOf(lRank)<0)throw new Error('costuma ir ao gol mas sem nivel no gol: esperava cair para '+lRank);
  p.gk=false;A.pres({dataset:{id:p.id}});
  if(lv.presentIds.indexOf(p.id)<0)throw new Error('esperava devolver a presenca');
});
step('montar times',()=>A.toTimes());
step('lista real: 19 presentes no 5v5 viram 4 times de 4 + 3 goleiros no rodizio',()=>{
  const lv=L().live;
  if(L().players.length!==19)throw new Error('esperava 19 jogadores no exemplo');
  if(lv.gkPool.length!==3)throw new Error('esperava 3 goleiros no rodizio, veio '+lv.gkPool.length);
  if(lv.teams.length!==4)throw new Error('esperava 4 times, veio '+lv.teams.length);
  if(!lv.teams.every(t=>t.ids.length===4))throw new Error('times de '+lv.teams.map(t=>t.ids.length).join('/'));
});
step('nova liga escolhe formato e modo na criacao',()=>{
  A.newLiga();A.novaOpt({dataset:{k:'format',v:'7'}});A.novaOpt({dataset:{k:'modo',v:'unica'}});NOVA.nome='Sete';
  const antes=S.ligas.length;A.saveLiga();
  if(S.ligas.length!==antes+1)throw new Error('liga nao foi criada');
  const l=L();if(l.cfg.format!==7||l.cfg.matchMode!=='unica'||l.cfg.targetGoals!==0)throw new Error('cfg da liga nova nao respeitou a folha: '+JSON.stringify(l.cfg));
  S.ligas.pop();S.active=S.ligas[S.ligas.length-1].id;render();
});
step('trocar formato para 7v7',()=>setFormat(7));
step('forcar 3 times: com 16 na linha no 7v7 so cabem 2 cheios',()=>{
  A.nteams({dataset:{v:'3'}});
  const lv=L().live;
  if(lv.teams.length!==2)throw new Error('esperava 2 times cheios, veio '+lv.teams.length);
  if(!lv.teams.every(t=>t.ids.length===lv.per))
    throw new Error('nem forcando pode sair time incompleto: '+lv.teams.map(t=>t.ids.length).join('/'));
});
step('equilibrar de novo',()=>A.balance());
step('sortear aleatorio',()=>A.shuffle());
step('equilibrar',()=>A.balance());
step('comecar racha: cai na tela de proxima partida, sem relogio',()=>{
  A.startJogo();
  const lv=L().live;
  if(lv.stage!=='jogo'||lv.cur)throw new Error('esperava stage jogo sem partida em andamento');
  if(!/Próxima partida/.test(els['#app'].innerHTML))throw new Error('tela de proxima partida nao apareceu');
  if(!/Começar partida/.test(els['#bar'].innerHTML))throw new Error('barra deveria oferecer Começar partida');
});
step('comecar partida',()=>A.startMatch());
step('os dois lados entram com o mesmo numero (4 de linha + goleiro)',()=>{
  const c=L().live.cur;
  if(c.lineups[0].length!==c.lineups[1].length)throw new Error('lados desiguais: '+c.lineups[0].length+' x '+c.lineups[1].length);
  if(!c.gks[0]||!c.gks[1])throw new Error('faltou goleiro em um dos lados');
  const lv=L().live,alvo=lv.per+(lv.gkPool.length?1:0);
  if(c.lineups[0].length!==alvo)throw new Error('esperava '+alvo+' em quadra, veio '+c.lineups[0].length);
});
step('gol do time A',()=>A.goal({dataset:{s:'0'}}));
step('marcar autor do gol',()=>A.scorer({dataset:{id:L().live.cur.lineups[0][0]}}));
step('gol do time B',()=>A.goal({dataset:{s:'1'}}));
step('remover gol do time B',()=>A.ungoal({dataset:{s:'1'}}));
step('abrir troca de goleiro',()=>A.gkSheet({dataset:{s:'0'}}));
step('definir goleiro improvisado',()=>A.setGk({dataset:{s:'0',id:L().live.cur.lineups[0][1]}}));
step('trocar o goleiro de um time pelo do outro: os dois trocam de lugar',()=>{
  const c=L().live.cur,a=c.gks[0],b=c.gks[1];
  A.setGk({dataset:{s:'0',id:b}});
  if(c.gks[0]!==b||c.gks[1]!==a)throw new Error('goleiros nao trocaram: '+c.gks);
  if(!c.lineups[0].includes(b)||c.lineups[1].includes(b))throw new Error('goleiro novo nao mudou de escalacao');
  if(!c.lineups[1].includes(a)||c.lineups[0].includes(a))throw new Error('goleiro antigo nao foi para o outro lado');
  A.goal({dataset:{s:'0'}});
  A.scorer({dataset:{id:b}});                     // agora ele e do time: da para marcar o gol dele
  const g=[...c.events].reverse().find(e=>e.type==='goal');
  if(g.pid!==b)throw new Error('gol do goleiro trocado nao foi atribuido');
  A.delGoal({dataset:{t:String(g.t)}});
  A.undo();                                       // desfaz a troca: cada um volta ao seu lado
  if(c.gks[0]!==a||c.gks[1]!==b)throw new Error('undo nao devolveu os goleiros: '+c.gks);
  if(!c.lineups[0].includes(a)||!c.lineups[1].includes(b)||c.lineups[0].includes(b)||c.lineups[1].includes(a))
    throw new Error('undo nao devolveu as escalacoes');
});
step('troca gravada pela versao antiga (sem mover escalacao) e curada ao recarregar',()=>{
  const c=L().live.cur,a=c.gks[0],b=c.gks[1];
  c.gks=[b,a];c.events.push({t:Date.now(),type:'gk',side:0,id:b,gks:[b,a]});   // como a versao antiga gravava
  normalize(S);
  const c2=L().live.cur;
  if(!c2.lineups[0].includes(b)||!c2.lineups[1].includes(a)||c2.lineups[0].includes(a)||c2.lineups[1].includes(b))
    throw new Error('normalize nao curou a escalacao');
  A.undo();                                       // desfazer o evento antigo tambem volta os lados
  const c3=L().live.cur;
  if(c3.gks[0]!==a||c3.gks[1]!==b||!c3.lineups[0].includes(a)||!c3.lineups[1].includes(b))
    throw new Error('undo do evento antigo nao devolveu os lados');
});
step('abrir substituicao (toque em quem esta em quadra)',()=>A.outPick({dataset:{s:'0',id:L().live.cur.lineups[0][0]}}));
step('abrir substituicao (toque em quem esta fora)',()=>{
  const b=benchList(L(),L().live);if(b.length)A.inPick({dataset:{id:b[0].id}});
});

step('corrigir autor do gol pela lista',()=>{
  const c=L().live.cur,g=c.events.find(e=>e.type==='goal');
  A.goalScorer({dataset:{t:String(g.t)}});
  A.setGoalScorer({dataset:{t:String(g.t),id:c.lineups[g.side][1]}});
  if(c.events.find(e=>e.t===g.t).pid!==c.lineups[g.side][1])throw new Error('autor nao mudou');
});
step('remover um gol pela lista',()=>{
  const c=L().live.cur,antes=c.score[0]+c.score[1];
  const g=c.events.find(e=>e.type==='goal');
  A.delGoal({dataset:{t:String(g.t)}});
  if(c.score[0]+c.score[1]!==antes-1)throw new Error('placar nao caiu');
});
step('arrastar reserva sobre titular substitui',()=>{
  const lv=L().live,c=lv.cur,fora=benchList(L(),lv);
  if(!fora.length)return;
  const antes=c.lineups[0][0];
  onDrop(fora[0].id,{dataset:{dropPlayer:antes}});
  if(!c.lineups[0].includes(fora[0].id))throw new Error('arraste nao substituiu');
});
step('arrastar alguem que ja esta em quadra nao faz nada',()=>{
  const c=L().live.cur,antes=JSON.stringify(c.lineups);
  onDrop(c.lineups[0][0],{dataset:{dropPlayer:c.lineups[1][0]}});
  if(JSON.stringify(c.lineups)!==antes)throw new Error('mexeu onde nao devia');
});
step('encerrar pelo placar (1 toque)',()=>{
  const c=L().live.cur;
  if(c.score[0]===c.score[1])A.goal({dataset:{s:'0'}});
  const gols=c.score[0]+c.score[1];
  A.endMatch();
  if(L().live.cur)throw new Error('a partida nao encerrou');
  const m=L().matches[L().matches.length-1];
  if(m.goals.length!==gols)throw new Error('gol sem autor sumiu do registro: '+m.goals.length+' de '+gols);
  if(m.goals.some(g=>g.pid===undefined))throw new Error('gol sem autor precisa ter pid nulo, nao undefined');
});
step('o fim foi sem querer: voltar a partida devolve relogio, gols e times',()=>{
  const l=L(),lv=l.live;
  const n=l.matches.length,mid=lv.matchIds[lv.matchIds.length-1];
  if(!lv.lastEnd||lv.lastEnd.mid!==mid)throw new Error('o fim nao deixou instantaneo');
  if(!/Voltar a partida/.test(els['#app'].innerHTML))throw new Error('botao de voltar nao apareceu');
  const golsAntes=lv.lastEnd.cur.events.filter(e=>e.type==='goal').length;
  const timesAntes=JSON.stringify(lv.lastEnd.teams);
  A.voltarPartida();
  if(!lv.cur)throw new Error('a partida nao voltou ao relogio');
  if(l.matches.length!==n-1)throw new Error('o registro nao foi apagado');
  if(lv.matchIds.includes(mid))throw new Error('a partida ainda esta na lista de hoje');
  if(lv.cur.events.filter(e=>e.type==='goal').length!==golsAntes)throw new Error('gols se perderam na volta');
  if(JSON.stringify(lv.teams.map(t=>t.ids))!==timesAntes)throw new Error('times nao voltaram como estavam');
  const evs=lv.cur.events;
  if(evs[evs.length-2].type!=='pause'||evs[evs.length-1].type!=='resume')throw new Error('o intervalo do fim devia entrar como pausa');
  if(lv.cur.paused)throw new Error('devia voltar rodando');
  A.endMatch();                        // registra de novo para o fluxo seguir
  if(lv.cur)throw new Error('nao encerrou de novo');
  if(l.matches.length!==n)throw new Error('o novo fim nao registrou');
});
step('nada de modal de patente entre partidas',()=>{
  if(typeof showResult!=='undefined')throw new Error('o modal de fim de partida deveria ter sumido');
  if(L().live.cur)throw new Error('devia estar entre partidas');
});
step('tela de proxima partida, com escalacao editavel antes do apito',()=>{
  const lv=L().live,html=viewProxima(L(),lv);
  if(html.indexOf('Próxima partida')<0)throw new Error('nao renderizou a tela de proxima partida');
  if(html.indexOf('de chance')<0)throw new Error('faltou a chance esperada de cada lado');
  const pair=lv.nextPair||suggestPair(L(),lv);
  if(pair[0]===pair[1])return;
  const a=lv.teams[pair[0]].ids[0],b=lv.teams[pair[1]].ids[0];
  A.sel({dataset:{id:a},classList:{toggle(){}}});
  A.sel({dataset:{id:b},classList:{toggle(){}}});
  if(lv.teams[pair[0]].ids.indexOf(b)<0||lv.teams[pair[1]].ids.indexOf(a)<0)
    throw new Error('trocar jogador antes do apito nao funcionou');
});
step('0-0 encerra em 1 toque, como empate',()=>{
  A.startMatch();
  const n=L().matches.length;
  A.endMatch();
  if(L().live.cur)throw new Error('nao encerrou');
  const m=L().matches[L().matches.length-1];
  if(L().matches.length!==n+1||m.result!=='draw')throw new Error('0-0 devia virar empate');
});
step('empate com 3+ times tira os dois de quadra',()=>{
  const lv=L().live;
  if(lv.teams.length>2&&lv.queue.length<2)throw new Error('os dois deviam ter ido para a fila');
});
step('pausar e retomar a partida',()=>{
  A.startMatch();
  const c=L().live.cur;
  A.pauseMatch();
  if(!c.paused)throw new Error('nao pausou');
  A.pauseMatch();
  if(c.paused)throw new Error('nao retomou');
});
step('cancelar a partida descarta tudo',()=>{
  const n=L().matches.length;
  A.goal({dataset:{s:'0'}});
  A.cancelMatch();
  if(L().live.cur)throw new Error('nao cancelou');
  if(L().matches.length!==n)throw new Error('cancelada nao pode entrar no historico');
});
step('substituicao vira trecho proprio',()=>{
  A.startMatch();
  const lv=L().live,c=lv.cur;
  c.startedAt=Date.now()-8*60000;                        // 8 min de partida
  A.goal({dataset:{s:'0'}});
  const fora=benchList(L(),lv);
  if(fora.length){
    c.events.push({t:Date.now()-3*60000,type:'sub',side:0,out:c.lineups[0][0],in:fora[0].id,gks:[...c.gks]});
    const k=c.lineups[0].indexOf(c.lineups[0][0]);c.lineups[0][k]=fora[0].id;
  }
  const st=splitStints(c,Date.now(),L().cfg);
  if(fora.length&&st.length!==2)throw new Error('esperava 2 trechos, veio '+st.length);
  A.goal({dataset:{s:'1'}});
  A.endMatch();
  const m=L().matches[L().matches.length-1];
  if(fora.length&&(!m.stints||m.stints.length!==2))throw new Error('a partida nao gravou os trechos');
});
step('escolher qual time entra',()=>{
  const lv=L().live;
  if(lv.teams.length>2){
    A.pickSide({dataset:{s:'0'}});
    A.setSide({dataset:{s:'0',i:'2'}});
    if(lv.nextPair[0]!==2)throw new Error('escolha nao aplicada');
  }
});
step('proxima partida entra com o time escolhido',()=>{
  const lv=L().live,querido=lv.nextPair?lv.nextPair[0]:null;
  A.startMatch();
  if(querido!=null&&lv.cur.a!==querido)throw new Error('entrou outro time');
});
step('chegou atrasado (sheet)',()=>A.lateSheet());
step('desfazer',()=>A.undo());
step('encerrar segunda partida',()=>{A.goal({dataset:{s:'1'}});A.finish({dataset:{r:'1'}})});
step('formato 11v11',()=>setFormat(11));
step('modo partida unica',()=>setMatchMode('unica'));
step('partida unica com goleiro fixo: escalacao sem vaga fantasma',()=>{
  const l=L(),lv=l.live;lv.stage='jogo';lv.cur=null;
  const gks=l.players.filter(p=>p.gk).slice(0,2).map(p=>p.id);
  lv.presentIds=[...new Set(gks.concat(l.players.filter(p=>!p.gk).slice(0,10).map(p=>p.id)))];lv.gkToday=gks.slice();
  setFormat(5);applyPlan(l,lv);
  if((lv.gkPool||[]).length)throw new Error('com um goleiro por time nao deveria haver rodizio');
  render();
  if(/pl  empty|＋ completar|>vaga</.test(document.querySelector('#app').innerHTML))throw new Error('escalacao mostra vaga que nao existe (goleiro fixo conta como um dos 5)');
  setFormat(11);
});
step('modo varias curtas',()=>setMatchMode('curtas'));
step('comecar partida para as substituicoes',()=>A.startMatch());
step('substituir tocando em quem esta em quadra',()=>{
  A.outPick({dataset:{s:'0',id:L().live.cur.lineups[0][0]}});
  const fora=benchList(L(),L().live);
  if(fora.length)A.doSub({dataset:{s:'0',out:L().live.cur.lineups[0][0],id:fora[0].id}});
});
step('substituicao nao mexe no time: quem entrou emprestado nao vira titular',()=>{
  const lv=L().live,c=lv.cur;if(!c)return;
  const ti=c.a,t=lv.teams[ti],emprestado=c.lineups[0].find(id=>!t.ids.includes(id));
  if(emprestado&&t.ids.includes(emprestado))throw new Error('o emprestado entrou no time');
  lv.teams.forEach((tt,i)=>{if(tt.ids.length!==tt.ids.filter(Boolean).length)throw new Error('time com buraco')});
});
step('foi embora no meio da partida: sai de tudo, a partida segue com um a menos',()=>{
  const lv=L().live,c=lv.cur;if(!c)return;
  const id=c.lineups[1][c.lineups[1].length-1],antes=c.lineups[1].length,tam=lv.presentIds.length;
  saiuNoMeio=id;
  A.leaveRacha({dataset:{id}});
  if(c.lineups[1].length!==antes-1)throw new Error('deveria ter saido da quadra');
  if(lv.presentIds.length!==tam-1||lv.presentIds.includes(id))throw new Error('deveria ter saido da presenca');
  if(!(lv.leftIds||[]).includes(id))throw new Error('quem saiu deveria ficar registrado como presente do racha');
  if(lv.teams.some(t=>t.ids.includes(id)))throw new Error('deveria ter saido do time');
  const st=splitStints(c,Date.now()+60000,L().cfg);
  if(st[st.length-1].lineups[1].includes(id))throw new Error('o trecho seguinte ainda conta com ele');
});
step('quem nao e do time original leva o icone de substituto',()=>{
  const lv=L().live,c=lv.cur;if(!c)return;render();
  const ti=c.a,orig=lv.teams[ti].orig||[];
  const estranho=c.lineups[0].find(id=>!orig.includes(id)&&id!==c.gks[0]);
  if(estranho&&!/⇄/.test(els['#app'].innerHTML))throw new Error('substituto sem o icone ⇄');
});
step('substituir tocando em quem esta fora',()=>{
  const fora=benchList(L(),L().live);
  if(fora.length){A.inPick({dataset:{id:fora[0].id}});
    A.doSub({dataset:{s:'1',out:L().live.cur.lineups[1][0],id:fora[0].id}});}
});
step('ninguem duplicado apos substituicoes',()=>{
  const c=L().live.cur,todos=[...c.lineups[0],...c.lineups[1]];
  if(new Set(todos).size!==todos.length)throw new Error('jogador em dois times ao mesmo tempo');
});
step('voltar para a tela de times',()=>A.teamsBack());
step('tirar goleiros do rodizio (fixos)',()=>A.gkMode());
step('voltar para o rodizio de goleiros',()=>A.gkMode());
step('selecionar jogador e mandar para o rodizio',()=>{
  const alguem=L().live.teams[0].ids[0];
  A.sel({dataset:{id:alguem},classList:{toggle(){}}});
  A.toPool({dataset:{}});
});
step('arrastar entre times troca os dois de lugar',()=>{
  const lv=L().live,a=lv.teams[0].ids[0],b=lv.teams[1].ids[0];
  onDrop(a,{dataset:{dropPlayer:b}});
  if(!lv.teams[0].ids.includes(b)||!lv.teams[1].ids.includes(a))throw new Error('a troca nao aconteceu');
});
step('arrastar para o card de fora tira do time',()=>{
  const lv=L().live,x=lv.teams[0].ids[0];
  onDrop(x,{dataset:{dropZone:'bench'}});
  if(lv.teams.some(t=>t.ids.includes(x)))throw new Error('continuou escalado');
});
step('cancelar selecao',()=>{A.sel({dataset:{id:L().live.teams[0].ids[0]},classList:{toggle(){}}});A.clearSel()});
step('recomecar partida',()=>A.startMatch());
step('aba patentes',()=>{S.ui.tab='ranking';render()});
step('ficha do jogador',()=>A.pSheet({dataset:{id:L().players[0].id}}));
step('corrigir nivel de quem ja jogou mexe no BASE e reaplica o historico (D-74)',()=>{
  const l=L(),p=l.players.find(x=>x.L.games>0)||l.players[0];
  A.pSheet({dataset:{id:p.id}});A.pdRank({dataset:{s:'10'}});A.pdSave();
  if(Math.round(p.L.base)!==Math.round(stepMid(10)))throw new Error('base nao virou o meio do degrau: '+p.L.base);
  if(!p.L.def)throw new Error('def deveria ligar');
  const e1=p.L.elo;rebuildAll(l);
  if(p.L.elo!==e1)throw new Error('recalculo nao e estavel depois da correcao');
  if(p.L.games>0&&(l.log[l.log.length-1]||{}).desde!=='entrada')throw new Error('log nao guardou que a correcao e desde a entrada');
});
step('corrigir nivel de quem NUNCA jogou entra direto no degrau',()=>{
  const l=L(),p=l.players.find(x=>!x.L.games);
  if(!p)return;
  A.pSheet({dataset:{id:p.id}});A.pdRank({dataset:{s:'4'}});A.pdSave();
  if(p.L.rank!==4||Math.round(p.L.elo)!==Math.round(stepMid(4)))throw new Error('sem historico, o degrau escolhido deveria valer na hora');
});
step('assumir perfil (Sou eu): o primeiro vinculado vira admin',()=>{
  S.me.name=S.me.name||'tester';
  A.pSheet({dataset:{id:L().players[0].id}});A.pdOwner();A.pdSave();
  if(L().players[0].owner!==S.me.name)throw new Error('perfil nao foi vinculado');
  if(L().players[0].role!=='admin')throw new Error('primeiro perfil vinculado deveria ser admin, veio '+L().players[0].role);
  if(!souAdmin(L()))throw new Error('souAdmin deveria ser true');
});
step('nao da para tirar o ultimo admin',()=>{
  A.pSheet({dataset:{id:L().players[0].id}});A.pdRole({dataset:{r:'jogador'}});A.pdSave();
  if(L().players[0].role!=='admin')throw new Error('o ultimo admin foi rebaixado');
  A.pdCancel();
});
step('admin ve o elo cru, discreto, na escada',()=>{
  if(viewEscada(L()).indexOf('Elo — só o admin vê')<0)throw new Error('elo sutil nao apareceu para o admin');
});
step('quem nao e admin nao revisa nem corrige patente',()=>{
  const l=L(),m=l.matches[0];const eu=l.players[0];
  eu.role='lancador';l.players[1].owner='outro';l.players[1].role='admin';   // agora o admin e outra pessoa
  if(souAdmin(l))throw new Error('ainda admin');
  if(viewEscada(l).indexOf('Elo — só o admin vê')>=0)throw new Error('quem nao e admin nao pode ver o elo cru');
  const antes=m.result;A.fixResult({dataset:{id:m.id,r:antes==='draw'?'0':'draw'}});
  if(m.result!==antes)throw new Error('lancador corrigiu resultado');
  const r0=eu.L.rank;A.pSheet({dataset:{id:eu.id,r:'L'}});A.pdBump({dataset:{d:'1'}});A.pdSave();
  if(eu.L.rank!==r0)throw new Error('lancador mexeu na propria patente');
  A.pdCancel();
  S.ui.tab='hist';render();if(/data-a="review"/.test(document.querySelector('#app').innerHTML))throw new Error('botao Revisar aparece para lancador');
  eu.role='admin';l.players[1].owner=null;l.players[1].role='lancador';S.ui.tab='racha';render();
});
step('aba numeros',()=>{S.ui.tab='stats';render()});
step('numeros: trocar de periodo',()=>{A.statsPer({dataset:{v:'sempre'}});A.statsPer({dataset:{v:String(new Date().getFullYear())}});A.statsPer({dataset:{v:'2019'}});A.statsPer({dataset:{v:'ano'}})});
step('inverter um ranking pela setinha e voltar',()=>{
  S.ui.statsTab='racha';A.statsPer({dataset:{v:'sempre'}});
  A.statsInv({dataset:{k:'vit'}});
  if(!S.ui.statsInv.vit)throw new Error('statsInv nao marcou');
  if(document.querySelector('#app').innerHTML.indexOf('↑')<0)throw new Error('setinha invertida nao apareceu');
  A.statsInv({dataset:{k:'vit'}});
  if(S.ui.statsInv.vit)throw new Error('statsInv nao desmarcou');
});
step('numeros: ultimo racha e ultimo mes',()=>{
  A.statsTab({dataset:{v:'racha'}});
  A.statsPer({dataset:{v:'racha'}});
  const h=els['#app'].innerHTML;
  if(!/Racha de /.test(h)||!/Destaques da noite/.test(h))throw new Error('aba racha no periodo "ultimo racha" sem os cards proprios');
  /* a % de vitorias realizada sempre sai; o "(esp.)" depende de m.pre cobrir a
     escalacao inteira (trecho curto descartado pode tirar — D-75), entao nao e exigido */
  if(/Times do racha/.test(h)&&!/% V/.test(h))throw new Error('faltou a % de vitorias discreta na linha dos times');
  if(/Rankings/.test(h))throw new Error('ranking de temporada nao cabe no ultimo racha');
  A.statsInv({dataset:{k:'rvenc'}});
  if(els['#app'].innerHTML.indexOf('↑')<0)throw new Error('setinha invertida nao apareceu no card da noite');
  A.statsInv({dataset:{k:'rvenc'}});
  A.statsPer({dataset:{v:'mes'}});
  if(!/no último mês/.test(els['#app'].innerHTML))throw new Error('periodo ultimo mes nao aplicou');
  A.statsPer({dataset:{v:'ano'}});A.statsTab({dataset:{v:'jogador'}});
});
step('revisao: corrigir autor de gol de partida encerrada',()=>{
  const l=L(),m=[...l.matches].reverse().find(x=>(x.goals||[]).length);
  if(!m)return;
  A.review({dataset:{id:m.id}});
  if(!/corrigir o autor/.test(els['#sheet'].innerHTML))throw new Error('revisao sem a lista de gols');
  A.goalScorerM({dataset:{id:m.id,i:'0'}});
  const em=new Set();matchStints(l,m).forEach(st=>(st.lineups[m.goals[0].side]||[]).forEach(id=>em.add(id)));
  const novo=[...em].find(id=>id!==m.goals[0].pid);
  const antes=P(l,novo).goals;
  A.setGoalScorerM({dataset:{id:m.id,i:'0',pid:novo,own:'0'}});
  if(m.goals[0].pid!==novo)throw new Error('autor nao mudou');
  if(P(l,novo).goals!==antes+1)throw new Error('o gol nao foi recontado para o novo autor');
  if(!l.log.some(e=>e.a==='goal'))throw new Error('correcao de autor sem registro no log');
});
step('numeros: abas jogador/racha e listas compactas',()=>{
  A.statsTab({dataset:{v:'racha'}});
  const h=els['#app'].innerHTML;
  if(!/Rankings/.test(h)||!/Mais tempo em quadra/.test(h)||!/Gols a cada 10 min/.test(h))throw new Error('aba racha sem rankings novos');
  if(/Duelos —/.test(h))throw new Error('duelos nao deveriam estar na aba racha');
  A.statsSec({dataset:{k:'pres'}});A.statsSec({dataset:{k:'pres'}});
  A.statsTab({dataset:{v:'jogador'}});
  const h2=els['#app'].innerHTML;
  if(!/Duelos —/.test(h2)||!/minutos/.test(h2))throw new Error('aba jogador sem duelos/minutos');
});
step('numeros: trocar de jogador',()=>{A.statsWho();A.setStatsWho({dataset:{id:L().players[3].id}})});
step('duelos e parcerias batem com o historico',()=>{
  const l=L(),who=statsWhoId(l),SL=statsLiga(l,'sempre');
  const rivais=Object.keys(SL.DU[who]||{});
  if(!rivais.length)throw new Error('ninguem enfrentou ninguem');
  const r=rivais[0],d=SL.DU[who][r];
  if(d.n!==d.v+d.e+d.d)throw new Error('V/E/D nao soma o total de confrontos');
  if(encontros(l,who,r,'sempre',false).length!==d.n)throw new Error('historico do duelo nao bate com o total');
  A.duelo({dataset:{id:r,m:'0'}});
  const mates=Object.keys(SL.PA[who]||{});
  if(mates.length)A.duelo({dataset:{id:mates[0],m:'1'}});
});
step('aba historico',()=>{S.ui.tab='hist';render()});
step('historico agrupa por racha e marca os que sao seus',()=>{
  const l=L(),eu=euId(l);
  if(!eu)throw new Error('ninguem assumiu perfil neste aparelho');
  const jogou=l.matches.filter(m=>ladoNaPartida(l,m,eu)!==null).length;
  const lista=viewHist(l);
  if(lista.indexOf('rachaRow')<0)throw new Error('a aba jogos devia listar rachas, nao partidas');
  if(lista.indexOf('data-a="contest"')>=0)throw new Error('partida solta nao aparece antes de abrir o racha');
  if(jogou&&lista.indexOf('VOCÊ')<0)throw new Error('nao marcou os rachas do dono do perfil');
  A.histMine({dataset:{v:'1'}});render();
  A.histMine({dataset:{v:'0'}});render();
});
step('abrir um racha mostra as partidas dele',()=>{
  const l=L(),sid=l.matches[l.matches.length-1].sessionId||('avulso-'+new Date(l.matches[l.matches.length-1].ts).toDateString());
  A.histRacha({dataset:{id:sid}});
  const dentro=viewHist(l);
  if(dentro.indexOf('data-a="contest"')<0)throw new Error('nao abriu as partidas do racha');
  if(dentro.indexOf('Todos os rachas')<0)throw new Error('faltou o caminho de volta');
  /* ate o 5v5 a partida e identificada por quem jogou; acima disso, pelo nome do time */
  const fmt=l.cfg.format,m0=l.matches[l.matches.length-1];
  const pri=esc(nomesCurtos(l,(m0.startLineups||m0.lineups)[0]).join(', '));
  l.cfg.format=5;
  if(viewHist(l).indexOf(pri)<0)throw new Error('no 5v5 o historico devia mostrar quem jogou');
  l.cfg.format=11;
  if(viewHist(l).indexOf(pri)>=0)throw new Error('acima do 5v5 a lista de nomes nao cabe no historico');
  if(viewHist(l).indexOf(esc(m0.names[0]))<0)throw new Error('sem a lista, o historico precisa do nome do time');
  l.cfg.format=fmt;
  A.histRacha({dataset:{id:''}});
  if(viewHist(l).indexOf('rachaRow')<0)throw new Error('nao voltou para a lista de rachas');
});
step('contestar partida',()=>A.contest({dataset:{id:L().matches[0].id}}));
step('revisar partida mostra a partida inteira',()=>{
  const l=L(),m=l.matches[0];
  A.review({dataset:{id:m.id}});
  const h=els['#sheet'].innerHTML;
  if(!/Linha do tempo/.test(h))throw new Error('revisao sem linha do tempo');
  if(!/Trechos/.test(h)||!/Efeito no nível/.test(h))throw new Error('revisao sem trechos ou efeito no nivel');
  if(h.indexOf(m.names[0])<0||h.indexOf(m.names[1])<0)throw new Error('revisao sem os dois times');
  /* quem esteve em quadra tem que aparecer, mesmo sem gol */
  const em=new Set();matchStints(l,m).forEach(st=>[0,1].forEach(sd=>(st.lineups[sd]||[]).forEach(id=>em.add(id))));
  const ficha=fichaPartida(l,m);
  if(ficha.length!==em.size)throw new Error('a ficha nao lista todo mundo que jogou ('+ficha.length+' de '+em.size+')');
  [...em].forEach(id=>{if(h.indexOf(esc(nameOf(l,id)))<0)throw new Error('quem jogou nao aparece na revisao: '+nameOf(l,id))});
  /* trechos e nivel abrem sob demanda */
  if(/conta 100%|descartado/.test(h))throw new Error('trechos deveriam comecar fechados');
  A.revSec({dataset:{k:'trechos',id:m.id}});
  if(!/conta |descartado/.test(els['#sheet'].innerHTML))throw new Error('trechos nao abriram');
  A.revSec({dataset:{k:'nivel',id:m.id}});
  if(!/Efeito no nível/.test(els['#sheet'].innerHTML))throw new Error('efeito no nivel nao abriu');
  A.revSec({dataset:{k:'tempo',id:m.id}});
  if(/toque para corrigir o autor/.test(els['#sheet'].innerHTML))throw new Error('linha do tempo nao fechou');
  A.revSec({dataset:{k:'tempo',id:m.id}});
});
step('ficha da partida conta tempo e gols de quem jogou',()=>{
  const l=L(),m=[...l.matches].reverse().find(x=>(x.events||[]).some(e=>e.type==='sub'))||l.matches[0];
  const ficha=fichaPartida(l,m);
  const gols=ficha.reduce((a,j)=>a+j.gols+j.contra,0);
  const comDono=(m.goals||[]).filter(g=>g.pid).length;
  if(gols!==comDono)throw new Error('gols com autor na ficha ('+gols+') nao batem com a partida ('+comDono+')');
  ficha.forEach(j=>{if(j.min<0||j.trechos<1)throw new Error('tempo em quadra invalido para '+nameOf(l,j.pid))});
  /* numero solto na ponta da linha nao volta: o +/- tem lugar proprio nos rankings.
     (o delta de nivel continua valendo — ele mora na secao "Efeito no nivel") */
  A.review({dataset:{id:m.id}});
  const quemJogou=els['#sheet'].innerHTML.split('Linha do tempo')[0];
  if(/class="val/.test(quemJogou))throw new Error('voltou numero sem rotulo na ficha de quem jogou');
});
step('corrigir resultado',()=>A.fixResult({dataset:{id:L().matches[0].id,r:'draw'}}));
step('anular partida',()=>A.voidMatch({dataset:{id:L().matches[0].id}}));
step('reativar partida',()=>A.voidMatch({dataset:{id:L().matches[0].id}}));
step('aba ajustes',()=>{S.ui.tab='cfg';render()});
step('partida unica nao aceita 3 times',()=>{setMatchMode('unica');const antes=L().live.teams.length;A.nteams({dataset:{v:'3'}});if(L().live.teams.length!==antes)throw new Error('mexeu nos times na partida unica');L().live.stage='times';setMatchMode('unica');if(L().live.teams.length!==2)throw new Error('ao montar times na partida unica deveria dar 2, deu '+L().live.teams.length);setMatchMode('curtas');L().live.stage='jogo';});
step('estabilidade nao e mais opcao da liga',()=>{
  if(A.setStab)throw new Error('setStab ainda existe');
  if(L().cfg.stability!==undefined)throw new Error('cfg.stability ainda existe');
  if(L().cfg.rankMargin!==RANK_MARGIN||L().cfg.protectMatches!==PROTECT)throw new Error('margem/protecao fora do padrao fixo');
});
step('alternar contestacao',()=>A.toggleDispute());
step('ranking de goleiro',()=>{S.ui.tab='ranking';A.rankRole({dataset:{v:'G'}});render();A.rankRole({dataset:{v:'L'}})});
step('patentes so para o admin',()=>{
  A.setVis({dataset:{v:'admin'}});S.ui.tab='ranking';render();
  A.setVis({dataset:{v:'todos'}});render();
});
step('evitar repetir dupla pode ser desligado',()=>{S.ui.tab='cfg';A.toggleCfg({dataset:{k:'avoidRepeat'}});A.toggleCfg({dataset:{k:'avoidRepeat'}})});
step('voltar para o racha',()=>{S.ui.tab='racha';render()});
step('encerrar racha',()=>A.endRacha());
step('sessao guarda presenca desde o comeco e os times como montados',()=>{
  const l=L(),sess=l.sessions[l.sessions.length-1];
  if(!sess)throw new Error('sessao nao gravada');
  if(saiuNoMeio&&!sess.presentIds.includes(saiuNoMeio))throw new Error('quem foi embora no meio sumiu da presenca do racha');
  if(!Array.isArray(sess.teams)||!sess.teams.length)throw new Error('sessao sem os times do racha');
  if(!sess.teams.every(t=>t.name&&Array.isArray(t.ids)&&t.ids.length))throw new Error('time gravado sem nome ou sem escalacao');
});
step('numeros: presentes do ultimo racha contam quem saiu no meio',()=>{
  S.ui.tab='stats';A.statsTab({dataset:{v:'racha'}});A.statsPer({dataset:{v:'racha'}});
  const l=L(),sess=l.sessions[l.sessions.length-1];
  const J=statsLiga(l,'racha:'+sess.id).J;
  const esperado=new Set([...sess.presentIds,...Object.keys(J)]).size;
  if(!new RegExp('<b class="num">'+esperado+'</b><span>presentes</span>').test(els['#app'].innerHTML))
    throw new Error('tile de presentes nao mostra '+esperado);
});
step('times do racha: toque abre a escalacao original',()=>{
  const l=L(),sess=l.sessions[l.sessions.length-1],t=sess.teams[0];
  A.rachaTime({dataset:{sid:sess.id,n:t.name}});
  const sh=els['#sheet'].innerHTML;
  if(sh.indexOf(esc(nameOf(l,t.ids[0])))<0)throw new Error('escalacao original nao apareceu na folha');
  A.closeSheet();
});
step('vitoria e do time que jogou, nao do nome no placar',()=>{
  const l=L();
  const TA=['a1','a2','a3','a4','a5'],TB=['b1','b2','b3','b4','b5'],TC=['c1','c2','c3','c4','c5'];
  const times=[{name:'Time A',ids:TA},{name:'Time B',ids:TB},{name:'Time C',ids:TC}];
  const st=(dur,l0,l1)=>({dur,counted:true,w:1,lineups:[l0.slice(),l1.slice()],gks:[null,null],score:[1,0],result:0,ended:'apito'});
  const part=sts=>({id:'x',ts:Date.now(),names:['Time A','Time B'],score:[1,0],result:0,stints:sts});
  const dono=(m,s)=>(timeDoLado(l,m,s,times)||{name:null}).name;
  if(dono(part([st(420000,TA,TB)]),0)!=='Time A')throw new Error('partida normal deveria contar para o time A');
  if(dono(part([st(420000,TC,TB)]),0)!=='Time C')throw new Error('com o time inteiro trocado, a vitoria e de quem jogou');
  if(dono(part([st(60000,TA,TB),st(540000,TC,TB)]),0)!=='Time C')throw new Error('trocou o time inteiro no meio: conta para quem ficou mais tempo');
  const umaTroca=[TA[0],TA[1],TA[2],TA[3],'z9'];
  if(dono(part([st(60000,TA,TB),st(540000,umaTroca,TB)]),0)!=='Time A')throw new Error('uma substituicao nao tira a vitoria do time');
  const metade=[TA[0],TA[1],TC[0],TC[1],'z9'];
  if(dono(part([st(600000,metade,TB)]),0)!==null)throw new Error('sem maioria de nenhum time, a partida nao conta para time nenhum');
  /* goleiro de rodizio nao e de time nenhum: fica fora da composicao */
  const comGk=timesDoRacha(l,[],{teams:[{name:'X',ids:['a','b','c']}],gkPool:['c']});
  if(comGk[0].ids.indexOf('c')>=0)throw new Error('goleiro do rodizio entrou na composicao do time');
  const doLance=timesDoRacha(l,[{ts:1,names:['X','Y'],startLineups:[['a','b','g'],['d','e','g2']]}],{gkPool:['g']});
  if(doLance[0].ids.indexOf('g')>=0)throw new Error('goleiro do rodizio entrou na composicao vinda da escalacao');
  if(doLance[1].ids.length!==3)throw new Error('goleiro fixo do outro time nao devia sair da composicao');
  /* sem lista de rodizio gravada, vale a evidencia: pegou no gol pelos dois times */
  const stq=(l0,l1,g0,g1)=>({dur:6e5,counted:true,w:1,lineups:[l0,l1],gks:[g0,g1],score:[1,0],result:0,ended:'apito'});
  const semLista=timesDoRacha(l,[
    {ts:1,names:['X','Y'],startLineups:[['a','b','g'],['d','e','h']],stints:[stq(['a','b','g'],['d','e','h'],'g','h')]},
    {ts:2,names:['Y','X'],startLineups:[['d','e','g'],['a','b','h']],stints:[stq(['d','e','g'],['a','b','h'],'g','h')]}],null);
  if(semLista.some(t=>t.ids.indexOf('g')>=0||t.ids.indexOf('h')>=0))
    throw new Error('goleiro que pegou no gol pelos dois times e do rodizio, nao do time');
  /* o card da noite usa isso: nome do time some do titulo, entram os jogadores */
  const fmt=l.cfg.format;l.cfg.format=5;
  A.statsTab({dataset:{v:'racha'}});A.statsPer({dataset:{v:'racha'}});
  const rotulo=()=>((els['#app'].innerHTML).match(/class="rk3 time[^"]*"[\s\S]*?<div class="nm">([^<]*)</)||[])[1]||'';
  if(els['#app'].innerHTML.indexOf('Times do racha')<0)throw new Error('card dos times sumiu');
  if(rotulo().indexOf(', ')<0)throw new Error('ate o 5v5 o time e rotulado pelos jogadores originais, veio "'+rotulo()+'"');
  l.cfg.format=11;render();
  if(rotulo().indexOf(', ')>=0)throw new Error('acima do 5v5 a lista nao cabe: o rotulo devia ser o nome do time');
  l.cfg.format=fmt;
  A.statsPer({dataset:{v:'ano'}});A.statsTab({dataset:{v:'jogador'}});
});
step('rankings da noite abrem ate 10, sem quem-mais-perdeu (a setinha cobre, D-72)',()=>{
  A.statsTab({dataset:{v:'racha'}});A.statsPer({dataset:{v:'racha'}});
  const h=els['#app'].innerHTML;
  if(h.indexOf('Quem mais perdeu')>=0)throw new Error('quem mais perdeu saiu no D-72: a setinha do "quem mais ganhou" cobre a leitura');
  if(h.indexOf('Melhor +/−')<0)throw new Error('o +/- da noite tem que aparecer tambem no racha curto (depois das vitorias)');
  if(h.indexOf('ver até')>=0){A.statsSec({dataset:{k:'rvenc'}});A.statsSec({dataset:{k:'rvenc'}})}
  A.statsPer({dataset:{v:'sempre'}});
  if(els['#app'].innerHTML.indexOf('Mais derrotas')<0)throw new Error('faltou Mais derrotas nos rankings de temporada');
});
step('historico mostra a chance de cada lado no apito',()=>{
  S.ui.tab='hist';render();
  const g=rachasDe(L(),L().matches)[0];
  A.histRacha({dataset:{id:g.id}});
  if(!/chance no apito/.test(els['#app'].innerHTML))throw new Error('chance ao lado do placar nao apareceu nas partidas do racha aberto');
  A.histRacha({dataset:{id:''}});S.ui.tab='stats';render();
});
step('partida a partida na tela do jogador, com paginacao',()=>{
  A.statsTab({dataset:{v:'jogador'}});A.statsPer({dataset:{v:'sempre'}});
  const h=els['#app'].innerHTML;
  if(!/Partida a partida/.test(h))throw new Error('secao partida a partida nao apareceu');
  if(!/prob\. de vitória/.test(h))throw new Error('o rotulo prob. de vitoria deveria aparecer');
  if(/data-a="ppPage"/.test(h)){
    A.ppPage({dataset:{d:'1'}});
    if(!S.ui.ppPage)throw new Error('paginacao nao avancou');
    A.ppPage({dataset:{d:'-1'}});
    if(S.ui.ppPage)throw new Error('paginacao nao voltou');
  }
});
step('numeros sem goleiros: liga, redesenha e desliga',()=>{
  A.statsSemGk();
  if(!S.ui.statsSemGk)throw new Error('toggle nao ligou');
  if(!/sem goleiros/.test(els['#app'].innerHTML))throw new Error('chip do toggle sumiu');
  A.statsPer({dataset:{v:'sempre'}});
  A.statsSemGk();
  if(S.ui.statsSemGk)throw new Error('toggle nao desligou');
});
step('corrigir escalacao e trocas: rascunho ate o Salvar',()=>{
  const l=L(),ps=l.players.map(p=>p.id);
  /* partida de 10 min com uma troca aos 4: o relogio do smoke nao anda, entao
     a partida do teste e montada na mao (mesma forma que o app grava)       */
  const fim=Date.now(),ini=fim-600000;
  const A0=ps.slice(0,5),B0=ps.slice(5,10),banco=ps[10];
  const m={id:'edit1',ts:fim,startedAt:ini,endedAt:fim,sessionId:null,mode:'curtas',
    names:['Verde','Preto'],teamIdx:[0,1],
    startLineups:[A0.slice(),B0.slice()],lineups:[A0.slice(),B0.slice()],
    startGks:[A0[4],B0[4]],gks:[A0[4],B0[4]],
    events:[{t:ini+240000,type:'sub',side:0,out:A0[1],in:banco,gks:[A0[4],B0[4]]},
            {t:ini+300000,type:'goal',side:0,pid:banco,own:false}],
    goals:[{pid:banco,side:0,own:false,t:ini+300000,min:300000}],
    score:[1,0],result:0,disputes:[],voided:false};
  l.matches.push(m);recalcPartida(l,m);rebuildAll(l);
  const nT=matchStints(l,m).length;
  if(nT!==2)throw new Error('a partida de teste deveria ter 2 trechos, tem '+nT);
  const real=()=>JSON.stringify([m.startLineups,m.lineups,m.events,m.goals,m.stints]);
  const antesDeTudo=real();
  A.editEsc({dataset:{id:m.id}});
  const h=els['#sheet'].innerHTML;
  if(!/Começaram/.test(h)||!/nova troca/.test(h)||!/Como fica/.test(h))throw new Error('tela de escalacao incompleta');
  if(/Salvar/.test(h))throw new Error('sem mudanca nenhuma nao deveria ter botao de salvar');
  /* era outra pessoa: some da partida inteira, mas so no rascunho */
  const alvo=A0[0],novo=l.players.find(p=>!genteDaPartida(m).has(p.id));
  if(!novo)throw new Error('sem ninguem de fora para trocar');
  A.escSwap({dataset:{id:m.id,s:'0',pid:alvo,por:novo.id}});
  if(!ESC||ESC.mud.length!==1)throw new Error('a mudanca nao entrou na lista do rascunho');
  if(real()!==antesDeTudo)throw new Error('o rascunho mexeu na partida antes de salvar');
  if(!/Salvar 1 mudança/.test(els['#sheet'].innerHTML))throw new Error('faltou o botao de salvar com a conta das mudancas');
  if(JSON.stringify(ESC.m.startLineups).indexOf(alvo)>=0)throw new Error('quem foi trocado ainda aparece no rascunho');
  if(!emQuadraNo(l,ESC.m,0).has(novo.id))throw new Error('quem entrou no lugar nao aparece nos trechos do rascunho');
  /* troca nova no meio da partida vira mais um trecho (na previa) */
  A.novaTroca({dataset:{id:m.id}});
  A.ntSet({dataset:{k:'side',v:'1'}});
  const t=tDoMinuto(ESC.m,ESC.nt.min),emq=escalaEm(l,ESC.m,t,1),livres=foraDeQuadra(l,ESC.m,t);
  if(!emq.length||!livres.length)throw new Error('sem gente para montar a troca nova');
  A.ntSet({dataset:{k:'out',v:emq[0]}});A.ntSet({dataset:{k:'in',v:livres[0]}});
  A.ntOk({dataset:{id:m.id}});
  if(matchStints(l,ESC.m).length!==nT+1)throw new Error('a troca nova nao virou trecho');
  if(!emQuadraNo(l,ESC.m,1).has(livres[0]))throw new Error('quem entrou pela troca nova nao esta em quadra');
  /* e apagar a troca devolve os trechos de antes */
  const i=(ESC.m.events||[]).findIndex(e=>e.type==='sub'&&e.in===livres[0]);
  A.evDel({dataset:{id:m.id,i:String(i)}});
  if(matchStints(l,ESC.m).length!==nT)throw new Error('apagar a troca nao devolveu os trechos');
  /* corrigir quem entrou numa troca ja existente */
  const iSub=(ESC.m.events||[]).findIndex(e=>e.type==='sub');
  A.evSet({dataset:{id:m.id,i:String(iSub),k:'in',v:livres[0]}});
  if(!matchStints(l,ESC.m)[1].lineups[0].includes(livres[0]))throw new Error('quem entrou corrigido nao entrou no trecho');
  /* goleiro de largada corrigido vale desde o primeiro trecho */
  const gk=ESC.m.startLineups[0][1];
  A.escGk({dataset:{id:m.id,s:'0',pid:gk}});
  if((matchStints(l,ESC.m)[0].gks||[])[0]!==gk)throw new Error('o goleiro corrigido nao valeu para o primeiro trecho');
  if(stintPart(matchStints(l,ESC.m)[0])[gk].role!=='G')throw new Error('o goleiro corrigido nao conta como goleiro no trecho');
  /* nao jogou: sai da escalacao e perde a autoria dos gols */
  const autor=(ESC.m.goals||[])[0].pid,ladoAutor=ESC.m.startLineups[0].includes(autor)?0:1;
  A.escDel({dataset:{id:m.id,s:String(ladoAutor),pid:autor}});
  if((ESC.m.goals||[])[0].pid)throw new Error('gol de quem nao jogou continuou com autor');
  if(real()!==antesDeTudo)throw new Error('a partida real mudou antes do Salvar');
  /* Salvar: agora sim a partida muda, cada mudanca vira registro e o nivel e refeito */
  const nMud=ESC.mud.length,logAntes=(l.log||[]).filter(e=>e.a==='esc').length;
  A.escSalvar({dataset:{id:m.id}});
  if(ESC)throw new Error('o rascunho deveria acabar no Salvar');
  if(real()===antesDeTudo)throw new Error('o Salvar nao escreveu na partida');
  if((l.log||[]).filter(e=>e.a==='esc').length!==logAntes+nMud)throw new Error('as correcoes nao foram todas para o log');
  if(emQuadraNo(l,m,0).has(alvo))throw new Error('quem foi trocado continua na partida salva');
  if((m.goals||[])[0].pid)throw new Error('a autoria do gol voltou depois de salvar');
  const elos=l.players.map(p=>p.L.elo+'/'+p.G.elo).join(',');
  rebuildAll(l);
  if(l.players.map(p=>p.L.elo+'/'+p.G.elo).join(',')!==elos)throw new Error('o nivel nao bate com o recalculo do zero');
  /* descartar: mexe e volta atras, sem deixar nada */
  const salvo=real();
  A.editEsc({dataset:{id:m.id}});
  A.escAddDo({dataset:{id:m.id,s:'1',pid:alvo}});
  if(!ESC||!ESC.mud.length)throw new Error('a mudanca nao entrou no rascunho');
  A.escDescartar({dataset:{id:m.id}});
  if(ESC)throw new Error('descartar deveria apagar o rascunho');
  if(real()!==salvo)throw new Error('descartar mexeu na partida');
  l.matches=l.matches.filter(x=>x.id!=='edit1');rebuildAll(l);   // o teste nao deixa resto
});
step('partida antiga nao aceita correcao de escalacao',()=>{
  const l=L(),m={id:'velha',ts:Date.now(),names:['A','B'],score:[1,0],result:0,lineups:[[],[]]};
  l.matches.push(m);
  openSheet('<h2>outra folha</h2>');
  A.editEsc({dataset:{id:'velha'}});
  if(/Escalação e trocas/.test(els['#sheet'].innerHTML))throw new Error('abriu a tela para partida sem cronometro');
  l.matches.pop();
});
step('voltar para home',()=>A.home());

/* estado salvo pela versao antiga (schema v1) sendo lido pela versao nova */
console.log('\n[smoke] de proximo: fila, vencedor fica, completar');
step('13 na linha no 5v5: 2 times cheios de 5 e 3 na fila',()=>{
  S=defState();A.demo();A.startRacha();
  const l=L(),lv=l.live;
  lv.presentIds=l.players.filter(p=>!p.gk).slice(0,13).map(p=>p.id);
  lv.gkToday=[];
  A.toTimes();
  const t=L().live.teams;
  if(t.length!==2)throw new Error('time so existe cheio: esperava 2 times, veio '+t.length);
  if(!t.every(x=>x.ids.length===5))throw new Error('times nao cheios: '+t.map(x=>x.ids.length).join('/'));
  if(filaDe(lv).length!==3)throw new Error('os 3 que sobram tem que virar fila');
});
step('quem ganhou fica, quem perdeu roda com a fila (entram 3, ficam 2)',()=>{
  const lv=L().live,antesA=lv.teams[0].ids.slice(),antesB=lv.teams[1].ids.slice(),fila=filaDe(lv).slice();
  A.startMatch();A.goal({dataset:{s:'0'}});A.finish({dataset:{r:'0'}});
  const A2=lv.teams[0].ids,B2=lv.teams[1].ids;
  if(A2.join()!==antesA.join())throw new Error('o time que ganhou tinha que ficar inteiro');
  if(B2.length!==5)throw new Error('o time que entra tem que estar cheio: '+B2.length);
  const entraram=B2.filter(id=>antesB.indexOf(id)<0);
  if(entraram.length!==3)throw new Error('esperava 3 entrando da fila, veio '+entraram.length);
  if(!entraram.every(id=>fila.indexOf(id)>=0))throw new Error('entrou alguem que nao estava na fila');
  const nova=filaDe(lv);
  if(nova.length!==3||!nova.every(id=>antesB.indexOf(id)>=0))
    throw new Error('quem saiu tem que ir para o fim da fila');
  render();
});
step('4 times: quem espera ha mais tempo joga antes (A×B, A×C, C×D, ...)',()=>{
  const salvo=S;S=defState();A.demo();A.startRacha();
  const l=L(),lv=l.live;
  lv.presentIds=l.players.map(p=>p.id);lv.gkToday=l.players.filter(p=>p.gk).map(p=>p.id);
  A.toTimes();if(L().live.teams.length!==4)A.nteams({dataset:{v:'4'}});
  try{
  if(L().live.teams.length!==4)throw new Error('esperava 4 times, veio '+L().live.teams.length);
  const nomes=()=>L().live.cur?[L().live.cur.a,L().live.cur.b].join('x'):'-';
  const joga=(vencedor)=>{A.startMatch();const c=L().live.cur;const s=vencedor===c.a?0:1;A.goal({dataset:{s:String(s)}});A.finish({dataset:{r:String(s)}})};
  L().live.nextPair=[0,1];joga(0);                        // A×B, A ganha → fila C,D,B
  let par=suggestPair(L(),L().live);
  if(par.join()!=='0,2')throw new Error('depois de A×B esperava A×C, veio '+par.join('x'));
  L().live.nextPair=par;joga(2);                          // A×C, C ganha (do lado direito) → fila D,B,A
  par=suggestPair(L(),L().live);
  if(par.join()!=='3,2')throw new Error('C ganhou do lado direito e fica NELE (D-71): esperava D×C, veio '+par.join('x'));
  L().live.nextPair=par;joga(3);                          // D×C, D ganha (do lado esquerdo) → fila B,A,C
  {const lv=L().live;if(!(lv.lastStay&&lv.lastStay.length===1&&lv.lastStay[0]===3))throw new Error('lastStay deveria ser o vencedor (D)')}
  par=suggestPair(L(),L().live);
  if(par.join()!=='3,1')throw new Error('D ganhou do lado esquerdo e fica nele: esperava D×B, veio '+par.join('x'));
  }finally{S=salvo;render()}
});
step('3 times e empate: um time fica (o que entrou por ultimo) e o goleiro fica com ele',()=>{
  const salvo=S;S=defState();A.demo();A.startRacha();
  const l=L(),lv=l.live;
  lv.presentIds=l.players.filter(p=>!p.gk).slice(0,12).map(p=>p.id).concat(l.players.filter(p=>p.gk).slice(0,2).map(p=>p.id));
  lv.gkToday=l.players.filter(p=>p.gk).slice(0,2).map(p=>p.id);
  A.toTimes();if(L().live.teams.length!==3)A.nteams({dataset:{v:'3'}});
  try{
    if(L().live.teams.length!==3)throw new Error('esperava 3 times, veio '+L().live.teams.length);
    L().live.nextPair=[0,1];A.startMatch();
    A.goal({dataset:{s:'0'}});A.finish({dataset:{r:'0'}});      // A vence B → A fica, C entra
    let par=suggestPair(L(),L().live);
    if(par.join()!=='0,2')throw new Error('esperava A×C, veio '+par.join('x'));
    L().live.nextPair=par;A.startMatch();A.finish({dataset:{r:'draw'}}); // A×C empata → C fica (entrou por ultimo), A sai
    const lv2=L().live;
    if(!(lv2.lastStay&&lv2.lastStay.length===1&&lv2.lastStay[0]===2))throw new Error('no empate com 3 times, C (o que entrou) deveria ficar');
    par=suggestPair(L(),lv2);
    if(par[1]!==2)throw new Error('C ficou no empate e continua do lado direito (D-71), veio '+par.join('x'));
    const gp=planGks(L(),lv2,par);
    if(lv2.gkPool.length&&lv2.lastGks[2]&&!(gp.gks[1]===lv2.lastGks[2]&&gp.fica[1]))throw new Error('o goleiro do time que ficou no empate deveria ficar');
  }finally{S=salvo;render()}
});
step('sem botao de girar: a troca na mao e toque/arraste entre fila e time',()=>{
  const lv=L().live;render();
  if(/Girar no/.test(els['#app'].innerHTML))throw new Error('botao de girar ainda aparece');
  const fila=filaDe(lv),tit=lv.teams[1].ids[0];
  if(fila.length){onDrop(fila[0],{dataset:{dropPlayer:tit}});
    if(!lv.teams[1].ids.includes(fila[0]))throw new Error('arrastar da fila sobre um titular nao trocou');
    onDrop(tit,{dataset:{dropPlayer:fila[0]}});}
});
step('alguem vai embora e o time fica curto',()=>{
  const lv=L().live,x=lv.teams[1].ids[0];
  onDrop(x,{dataset:{dropZone:'bench'}});
  if(lv.teams[1].ids.length!==4)throw new Error('o time deveria ter ficado com 4');
});
step('time curto mostra uma vaga no cartao; tocar nela puxa alguem da fila',()=>{
  const lv=L().live;
  if(lv.stage==='jogo'){A.endMatch&&0;}
  render();
  const h=els['#app'].innerHTML;
  if(!/＋ vaga|＋ completar|tp big emp/.test(h))throw new Error('cartao do time curto sem vaga nem emprestado');
  if(lv.stage!=='jogo'){
    const antes=lv.teams[1].ids.length,fila=filaDe(lv);
    A.slotPick({dataset:{i:'1'}});
    if(!/Vaga no/.test(els['#sheet'].innerHTML))throw new Error('folha da vaga nao abriu');
    A.slotSet({dataset:{i:'1',id:fila[0]}});
    if(lv.teams[1].ids.length!==antes+1||!lv.teams[1].ids.includes(fila[0]))throw new Error('a vaga nao foi preenchida');
    onDrop(fila[0],{dataset:{dropZone:'bench'}});   // devolve para os passos seguintes
  }
});
step('a partida ainda entra 5v5: o time curto e completado por quem esta na fila',()=>{
  A.startMatch();
  const c=L().live.cur;
  if(c.lineups[0].length!==c.lineups[1].length)
    throw new Error('lados desiguais: '+c.lineups[0].length+'x'+c.lineups[1].length);
  if(c.lineups[0].length!==5)throw new Error('nao se joga com menos de 5: veio '+c.lineups[0].length);
  const todos=[...c.lineups[0],...c.lineups[1]];
  if(new Set(todos).size!==todos.length)throw new Error('alguem entrou nos dois lados');
  if(!c.fill[0].length&&!c.fill[1].length)throw new Error('ninguem completou o time curto');
});
step('quem completa joga emprestado: o time nao muda durante a partida',()=>{
  const lv=L().live,emprestado=[...lv.cur.fill[0],...lv.cur.fill[1]][0];
  if(lv.teams.some(t=>t.ids.indexOf(emprestado)>=0))
    throw new Error('o emprestimo nao pode mexer no time');
  A.finish({dataset:{r:'0'}});
  render();
});
step('o usuario escolhe quem completa',()=>{
  const l=L(),lv=l.live;
  const x=lv.teams[1].ids[0];onDrop(x,{dataset:{dropZone:'bench'}});   /* deixa o time curto de novo */
  const pair=(lv.nextPair||suggestPair(l,lv)).slice();
  const f=fillDe(l,lv,pair),sd=f[0].length?0:1;
  if(!f[sd].length)throw new Error('nao veio sugestao de quem completa');
  const sugerido=f[sd][0];
  A.fillDel({dataset:{sd:String(sd),id:sugerido}});
  const outro=candidatosFill(l,lv,pair,[]).filter(id=>id!==sugerido)[0];
  A.fillSet({dataset:{sd:String(sd),id:outro}});
  if(L().live.fill[sd].indexOf(outro)<0)throw new Error('a escolha do usuario nao ficou de pe');
  A.startMatch();
  if(L().live.cur.lineups[sd].indexOf(outro)<0)throw new Error('quem foi escolhido nao entrou');
  A.finish({dataset:{r:'draw'}});
});
step('da para jogar sem completar: os dois lados entram menores e iguais',()=>{
  const lv=L().live,x=lv.teams[1].ids[0];onDrop(x,{dataset:{dropZone:'bench'}});
  A.fillOff();
  A.startMatch();
  const c=L().live.cur;
  if(c.lineups[0].length!==c.lineups[1].length)throw new Error('lados desiguais sem completar');
  if(c.fill[0].length||c.fill[1].length)throw new Error('completou mesmo com o completar desligado');
  A.finish({dataset:{r:'draw'}});
});

console.log('\n[smoke] dados antigos no localStorage');
const antigo={v:1,me:{id:'x',name:''},active:'old',ui:{tab:'racha'},ligas:[{id:'old',name:'Antiga',
  cfg:{startElo:1500,kNew:40,kBase:24,placement:5,tiers:[1700,1600,1450,1350],tierNames:['a','b','c','d','e'],
       targetGoals:2,targetMin:7,winnerStays:true,askScorer:true,gkOutOfElo:false,teamCount:2},
  players:[{id:'a1',name:'Velho',gk:false,elo:1520,peak:1520,games:3,w:2,l:1,d:0,goals:1,form:['V'],owner:null,role:'lancador'}],
  matches:[],sessions:[],live:null}]};
localStorage.setItem('raxa_v1',JSON.stringify(antigo));
step('carregar estado antigo e renderizar',()=>{
  S=normalize(JSON.parse(localStorage.getItem('raxa_v1')));
  render();
  S.active='old';S.ui.tab='ranking';render();
  S.ui.tab='cfg';render();
  const p=L().players[0];
  if(!p.L||!p.G)throw new Error('nao migrou para duas trilhas');
  if(p.L.elo!==1520||p.L.games!==3)throw new Error('perdeu o historico na migracao');
  if(p.G.def||p.G.games!==0)throw new Error('quem nunca pegou no gol nao pode ter patente de goleiro');
  if(p.G.elo!==1500)throw new Error('sem patente, a valencia entra no nivel padrao (1500), nao na patente da linha');
});

console.log(fails?'\n*** '+fails+' TELA(S) QUEBRADA(S) ***':'\nSMOKE OK: nenhuma tela quebrou');
process.exit(fails?1:0);
"""

out = os.path.join(SP, 'smoke.js')
io.open(out, 'w', encoding='utf-8').write(stub + js + smoke)
sys.exit(subprocess.run(['node', out]).returncode)
