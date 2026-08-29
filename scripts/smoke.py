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
function step(label,fn){
  try{fn();console.log('  ok: '+label)}
  catch(e){fails++;console.log('  QUEBROU em "'+label+'": '+e.message+'\n    '+String(e.stack).split('\n')[1])}
}
console.log('\n[smoke] telas e fluxo completo');
step('tela inicial (sem ligas)',()=>{S=defState();render()});
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
step('trocar formato para 7v7',()=>A.setFormat({dataset:{v:'7'}}));
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
step('formato 11v11',()=>A.setFormat({dataset:{v:'11'}}));
step('modo partida unica',()=>A.setMatchMode({dataset:{v:'unica'}}));
step('partida unica com goleiro fixo: escalacao sem vaga fantasma',()=>{
  const l=L(),lv=l.live;lv.stage='jogo';lv.cur=null;
  const gks=l.players.filter(p=>p.gk).slice(0,2).map(p=>p.id);
  lv.presentIds=[...new Set(gks.concat(l.players.filter(p=>!p.gk).slice(0,10).map(p=>p.id)))];lv.gkToday=gks.slice();
  A.setFormat({dataset:{v:'5'}});applyPlan(l,lv);
  if((lv.gkPool||[]).length)throw new Error('com um goleiro por time nao deveria haver rodizio');
  render();
  if(/pl  empty|＋ completar|>vaga</.test(document.querySelector('#app').innerHTML))throw new Error('escalacao mostra vaga que nao existe (goleiro fixo conta como um dos 5)');
  A.setFormat({dataset:{v:'11'}});
});
step('modo varias curtas',()=>A.setMatchMode({dataset:{v:'curtas'}}));
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
  A.leaveRacha({dataset:{id}});
  if(c.lineups[1].length!==antes-1)throw new Error('deveria ter saido da quadra');
  if(lv.presentIds.length!==tam-1||lv.presentIds.includes(id))throw new Error('deveria ter saido da presenca');
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
step('corrigir patente',()=>A.setRank({dataset:{id:L().players[0].id,s:'10'}}));
step('assumir perfil: o primeiro vinculado vira admin',()=>{
  A.claim({dataset:{id:L().players[0].id}});
  if(L().players[0].role!=='admin')throw new Error('primeiro perfil vinculado deveria ser admin, veio '+L().players[0].role);
  if(!souAdmin(L()))throw new Error('souAdmin deveria ser true');
});
step('nao da para tirar o ultimo admin',()=>{
  A.setRole({dataset:{id:L().players[0].id,r:'jogador'}});
  if(L().players[0].role!=='admin')throw new Error('o ultimo admin foi rebaixado');
});
step('quem nao e admin nao revisa nem corrige patente',()=>{
  const l=L(),m=l.matches[0];const eu=l.players[0];
  eu.role='lancador';l.players[1].owner='outro';l.players[1].role='admin';   // agora o admin e outra pessoa
  if(souAdmin(l))throw new Error('ainda admin');
  const antes=m.result;A.fixResult({dataset:{id:m.id,r:antes==='draw'?'0':'draw'}});
  if(m.result!==antes)throw new Error('lancador corrigiu resultado');
  const r0=eu.L.rank;A.bumpRank({dataset:{id:eu.id,r:'L',d:'1'}});
  if(eu.L.rank!==r0)throw new Error('lancador mexeu na propria patente');
  S.ui.tab='hist';render();if(/data-a="review"/.test(document.querySelector('#app').innerHTML))throw new Error('botao Revisar aparece para lancador');
  eu.role='admin';l.players[1].owner=null;l.players[1].role='lancador';S.ui.tab='racha';render();
});
step('aba numeros',()=>{S.ui.tab='stats';render()});
step('numeros: trocar de periodo',()=>{A.statsPer({dataset:{v:'sempre'}});A.statsPer({dataset:{v:String(new Date().getFullYear())}});A.statsPer({dataset:{v:'2019'}});A.statsPer({dataset:{v:'ano'}})});
step('numeros: ultimo racha e ultimo mes',()=>{
  A.statsTab({dataset:{v:'racha'}});
  A.statsPer({dataset:{v:'racha'}});
  const h=els['#app'].innerHTML;
  if(!/Racha de /.test(h)||!/Destaques da noite/.test(h))throw new Error('aba racha no periodo "ultimo racha" sem os cards proprios');
  if(/Rankings/.test(h))throw new Error('ranking de temporada nao cabe no ultimo racha');
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
  A.histRacha({dataset:{id:''}});
  if(viewHist(l).indexOf('rachaRow')<0)throw new Error('nao voltou para a lista de rachas');
});
step('contestar partida',()=>A.contest({dataset:{id:L().matches[0].id}}));
step('revisar partida',()=>A.review({dataset:{id:L().matches[0].id}}));
step('corrigir resultado',()=>A.fixResult({dataset:{id:L().matches[0].id,r:'draw'}}));
step('anular partida',()=>A.voidMatch({dataset:{id:L().matches[0].id}}));
step('reativar partida',()=>A.voidMatch({dataset:{id:L().matches[0].id}}));
step('aba ajustes',()=>{S.ui.tab='cfg';render()});
step('partida unica nao aceita 3 times',()=>{A.setMatchMode({dataset:{v:'unica'}});const antes=L().live.teams.length;A.nteams({dataset:{v:'3'}});if(L().live.teams.length!==antes)throw new Error('mexeu nos times na partida unica');L().live.stage='times';A.setMatchMode({dataset:{v:'unica'}});if(L().live.teams.length!==2)throw new Error('ao montar times na partida unica deveria dar 2, deu '+L().live.teams.length);A.setMatchMode({dataset:{v:'curtas'}});L().live.stage='jogo';});
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
  L().live.nextPair=par;joga(2);                          // A×C, C ganha → fila D,B,A
  par=suggestPair(L(),L().live);
  if(par.join()!=='2,3')throw new Error('depois de A×C (C ganhou) esperava C×D, veio '+par.join('x'));
  L().live.nextPair=par;joga(3);                          // C×D, D ganha → fila B,A,C
  {const lv=L().live;if(!(lv.lastStay&&lv.lastStay.length===1&&lv.lastStay[0]===3))throw new Error('lastStay deveria ser o vencedor (D)')}
  par=suggestPair(L(),L().live);
  if(par.join()!=='3,1')throw new Error('depois de C×D (D ganhou) esperava D×B, veio '+par.join('x'));
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
    if(par[0]!==2)throw new Error('a proxima deveria comecar pelo C que ficou, veio '+par.join('x'));
    const gp=planGks(L(),lv2,par);
    if(lv2.gkPool.length&&lv2.lastGks[2]&&!(gp.gks[0]===lv2.lastGks[2]&&gp.fica[0]))throw new Error('o goleiro do time que ficou no empate deveria ficar');
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
