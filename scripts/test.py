# -*- coding: utf-8 -*-
"""
Suite de testes do motor de patentes do Raxa.

Extrai o bloco de logica de index.html (tudo antes do bloco RENDER, que nao
depende do DOM), injeta um harness e roda em Node.

Uso:  python scripts/test.py
"""
import io, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'scripts', '.tmp')
os.path.isdir(OUT) or os.makedirs(OUT)

html = io.open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
js = html.split('<script>')[1].split('</script>')[0]
io.open(os.path.join(OUT, 'full.js'), 'w', encoding='utf-8').write(js)

core = js.split('   RENDER')[0]
core = core.replace("try{S=JSON.parse(localStorage.getItem(KEY))||defState()}catch(e){S=defState()}", "S=defState();")
core = core.replace("const save=()=>localStorage.setItem(KEY,JSON.stringify(S));", "const save=()=>{};")

harness = r"""
/* ---------------- harness ---------------- */
let _i=0; const nid=()=>'p'+(++_i);
function mk(name,elo,gk){return{id:nid(),name,gk:!!gk,L:newTrack(elo),G:newTrack(elo),
  goals:0,sessions:0,lastSession:null,owner:null,role:'lancador'};}
const liga={id:'x',name:'t',cfg:defCfg(),players:[],matches:[],sessions:[],live:null};
[['Rafa',1810,0],['Leo',1720,0],['Bruno',1660,0],['Dudu',1600,0],['Matheus',1560,0],['Gabriel',1530,0],
 ['Thiago',1500,0],['Pedro',1480,0],['Caio',1450,0],['Vitor',1420,0],['Jhonny',1380,0],['Sergio',1330,0],
 ['Marcelo',1280,0],['Paulo',1180,0],['Nenem',1500,1],['Tiago',1500,1]].forEach(a=>liga.players.push(mk(a[0],a[1],a[2])));
S.ligas=[liga];S.active=liga.id;
let fails=0;
function ok(c,m){ if(!c){fails++;console.log('  FALHOU: '+m);} else console.log('  ok: '+m); }

const MIN=60000;
let CLOCK=new Date(new Date().getFullYear(),0,2,9,0,0).getTime();
/* Monta uma partida como o app monta: escalacao de largada, eventos com o
   tempo relativo (at, em ms) e duracao total.                               */
function partida(lineA,lineB,o){
  o=o||{};
  const t0=(CLOCK+=30*MIN),dur=o.dur||7*MIN;
  const c={a:0,b:1,startedAt:t0,score:o.score||[1,0],
    events:(o.events||[]).map(e=>Object.assign({},e,{t:t0+e.at})),
    lineups:[[...(o.fimA||lineA)],[...(o.fimB||lineB)]],
    startLineups:[[...lineA],[...lineB]],
    gks:o.gks?[...o.gks]:[null,null],startGks:o.gks?[...o.gks]:[null,null]};
  const stints=splitStints(c,t0+dur,liga.cfg);
  return {c,stints,t0,dur};
}
function lanca(lineA,lineB,result,o){
  o=o||{};
  const {c,stints,t0,dur}=partida(lineA,lineB,o);
  if(o.resultados)stints.forEach((s,i)=>{if(o.resultados[i]!==undefined)s.result=o.resultados[i]});
  else stints.forEach(s=>s.result=result);
  const m={id:'m'+liga.matches.length,ts:t0+dur,startedAt:t0,endedAt:t0+dur,sessionId:o.sid||'s1',
    mode:o.mode,names:['Time A','Time B'],teamIdx:[0,1],
    lineups:c.lineups.map(x=>[...x]),startLineups:[[...lineA],[...lineB]],
    gks:c.gks,stints,score:o.score||[1,0],result,
    goals:o.goals===undefined?[{pid:lineA[0],side:0}]:o.goals,disputes:[],voided:false};
  applyMatch(liga,m);liga.matches.push(m);
  return m;
}
const elo=(id,role)=>rt(P(liga,id),role||'L').elo;

console.log('\n[1] escada de patentes');
ok(rankLabel(liga,stepOf(1500))==='Prata 1','1500 (padrao de entrada) = Prata 1, na media da escada');
ok(Math.round(1500-stepMin(0))===400&&Math.round(stepMin(TOP+1)-1500)===400,'a entrada fica no centro: 400 pontos para cada lado');
ok(rankLabel(liga,11)==='Ouro 3'&&rankLabel(liga,9)==='Ouro 1','no topo: Ouro 3 e o melhor, Ouro 1 o primeiro degrau');
ok(rankLabel(liga,0)==='Ferro 1','o degrau mais baixo da escada e Ferro 1');
ok(patOf(stepOf(1499))===1&&patOf(stepOf(1500))===2,'corte Bronze/Prata em 1500');
ok(patOf(stepOf(1699))===2&&patOf(stepOf(1700))===3,'corte Prata/Ouro em 1700');
ok(patOf(stepOf(1900))===3&&stepOf(1900)===11,'acima de 1900 fica preso em Ouro 3 (escada tem 4 niveis)');
ok(stepOf(500)===0&&stepOf(9000)===11,'extremos ficam presos no primeiro/ultimo degrau');
ok(Math.round(stepMin(3)-stepMin(0))===200,'patente tem 200 pontos (intervalo de classe do Elo)');

console.log('\n[2] equilibrio de times');
const ids=liga.players.map(p=>p.id);
for(const n of [2,3,4]){
  const t=buildTeams(liga,ids,n);
  const avgs=t.map(x=>teamAvg(liga,x)),diff=Math.max(...avgs)-Math.min(...avgs);
  const gks=t.map(x=>x.ids.filter(i=>P(liga,i).gk).length),sizes=t.map(x=>x.ids.length);
  console.log('  '+n+' times: diff='+Math.round(diff)+' gks='+gks.join('/')+' tam='+sizes.join('/'));
  ok(diff<=40,'diferenca de nivel <= 40 com '+n+' times');
  ok(Math.max(...sizes)-Math.min(...sizes)<=1,'times de tamanho parelho');
  ok(Math.max(...gks)-Math.min(...gks)<=1,'goleiros distribuidos');
  ok(t.flatMap(x=>x.ids).length===ids.length,'ninguem sumiu nem duplicou');
}

console.log('\n[2b] equilibrar varia, e quem fica de fora tambem sai equilibrado');
{
  const ids13=liga.players.filter(p=>!p.gk).slice(0,13).map(p=>p.id);
  const todos=ids13.map(id=>P(liga,id));
  const mediaGeral=todos.reduce((a,p)=>a+p.L.elo,0)/todos.length;
  const piores=[...todos].sort((a,b)=>a.L.elo-b.L.elo).slice(0,3).reduce((a,p)=>a+p.L.elo,0)/3;
  const arranjos={},difs=[],forasMedia=[];let n=0;
  for(let i=0;i<14;i++){
    const t=buildTeams(liga,ids13,2,[5,5],[],true);
    const chave=t.map(x=>x.ids.slice().sort().join(',')).sort().join('|');
    if(!arranjos[chave]){arranjos[chave]=1;n++}
    const avgs=t.map(x=>teamAvg(liga,x));
    difs.push(Math.max(...avgs)-Math.min(...avgs));
    const dentro=t.reduce((a,x)=>a.concat(x.ids),[]);
    const fora=ids13.filter(id=>dentro.indexOf(id)<0);
    forasMedia.push(fora.reduce((a,id)=>a+P(liga,id).L.elo,0)/fora.length);
  }
  const mediaFora=forasMedia.reduce((a,b)=>a+b,0)/forasMedia.length;
  console.log('  14 montagens: '+n+' arranjos diferentes, pior desequilibrio '+Math.round(Math.max(...difs)));
  console.log('  nivel medio de quem fica de fora: '+Math.round(mediaFora)
    +' | media do racha: '+Math.round(mediaGeral)+' | media dos 3 piores: '+Math.round(piores));
  ok(n>=4,'equilibrar de novo devolve outro arranjo (o ruido de montagem varia)');
  ok(Math.max(...difs)<=40,'e todos os arranjos continuam equilibrados de verdade');
  ok(Math.abs(mediaFora-mediaGeral)<60,'quem fica de fora tem o nivel medio do racha, nao o fundo dele');
  ok(mediaFora-piores>60,'a fila nao e a lista dos piores');
}

console.log('\n[3] tamanho dos times respeita o formato');
liga.cfg.format=5;liga.cfg.matchMode='curtas';
const gk2=liga.players.filter(p=>p.gk).map(p=>p.id);
const linha=liga.players.filter(p=>!p.gk).map(p=>p.id);
function monta(nLinha,nGk,modo){
  liga.cfg.matchMode=modo||'curtas';
  const ids=[...linha.slice(0,nLinha),...gk2.slice(0,nGk)];
  const pl=planTeams(liga,ids);
  const curto=(modo||'curtas')!=='unica';
  const times=buildTeams(liga,pl.ids,pl.n,pl.caps,pl.gkIds,curto);
  const dentro=times.reduce((a,t)=>a+t.ids.length,0);
  return {pl,times,tam:times.map(t=>t.ids.length),fora:pl.ids.length-dentro};
}
let r3=monta(12,2);
console.log('  5v5, 12 de linha + 2 goleiros: '+r3.pl.n+' times de '+r3.tam.join('/')+' (linha por time = '+r3.pl.per+')');
ok(r3.pl.rotating&&r3.pl.gkPool.length===2,'2 goleiros para 3 times viram rodizio');
ok(r3.pl.per===4,'no 5v5 com goleiro rodando, o time tem 4 de linha');
ok(r3.pl.n===3&&r3.tam.every(x=>x===4),'3 times completos de 4');

r3=monta(11,2);
console.log('  5v5, 11 de linha + 2 goleiros: times de '+r3.tam.join('/')+' e '+r3.fora+' de fora');
ok(r3.pl.n===2&&r3.tam.every(x=>x===5),'11 de linha nao viram 3 times: 2 times cheios (4 de linha + goleiro)');
ok(r3.fora===3,'os 3 que sobram ficam de fora, nao viram time de 3');

r3=monta(10,2);
console.log('  5v5, 10 de linha + 2 goleiros: '+r3.pl.n+' times de '+r3.tam.join('/')+' e '+r3.fora+' de fora, rodizio='+r3.pl.rotating);
ok(r3.pl.n===2&&!r3.pl.rotating&&r3.tam.every(x=>x===5),'2 goleiros para 2 times: 4 de linha + goleiro fixo em cada = 5v5');
ok(r3.fora===2,'e 2 de fora — ninguem joga com um a menos');

r3=monta(8,2);
console.log('  5v5, 8 de linha + 2 goleiros: '+r3.pl.n+' times de '+r3.tam.join('/')+', rodizio='+r3.pl.rotating);
ok(!r3.pl.rotating&&r3.pl.per===5,'2 goleiros para 2 times: cada um fica fixo no seu time');
ok(r3.pl.n===2&&r3.tam.every(x=>x===5),'10 pessoas em 2 times de 5, goleiro incluso');

r3=monta(8,0);
console.log('  5v5 sem goleiro marcado, 8 presentes: times de '+r3.tam.join('/')+' (alvo por time = '+r3.pl.per+')');
ok(r3.pl.per===5,'sem rodizio, o alvo do time e 5');
ok(r3.tam.every(x=>x===4),'so quando nao da dois times cheios e que se joga com menos: 4v4, nunca 5x4');

r3=monta(13,0);
console.log('  5v5 sem goleiro, 13 presentes: times de '+r3.tam.join('/')+' e '+r3.fora+' de fora');
ok(r3.pl.n===2&&r3.tam.every(x=>x===5),'13 sem goleiro: 2 times de 5, e nao 5/5/3');
ok(r3.fora===3,'os outros 3 ficam de fora e entram trocando');

r3=monta(14,2,'unica');
console.log('  partida unica, 14 de linha + 2 goleiros: times de '+r3.tam.join('/')+', em quadra = '+r3.pl.per);
ok(r3.pl.n===2&&r3.tam.every(x=>x===8),'partida unica: todo mundo dividido em 2 times');
ok(r3.pl.per===5,'5 em quadra por time, o resto e reserva');
liga.cfg.matchMode='curtas';

{
  const lvGk={gkPool:[...gk2],gkFlip:0,teams:[{ids:[]},{ids:[]},{ids:[]}],lastWinner:null,lastGks:{},nextGks:null};
  liga.cfg.winnerStays=true;
  const g1=commitGks(liga,lvGk,[0,1]);
  console.log('  partida 1: '+g1.map(x=>nameOf(liga,x)).join(' x '));
  ok(g1[0]===gk2[0]&&g1[1]===gk2[1],'2 goleiros no rodizio: um para cada lado');
  lvGk.lastWinner=0;lvGk.lastGks={0:g1[0],1:g1[1]};             // time 0 venceu com g1[0] no gol
  const p2=planGks(liga,lvGk,[0,2]);
  ok(p2.gks[0]===g1[0]&&p2.fica[0],'o goleiro do time que venceu fica com ele');
  ok(p2.gks[1]===g1[1],'com 2 goleiros, o outro lado fica com o segundo');
  const lv3={gkPool:['gA','gB','gC'],gkFlip:0,teams:[{ids:[]},{ids:[]},{ids:[]}],lastWinner:null,lastGks:{},nextGks:null};
  const h1=commitGks(liga,lv3,[0,1]);                            // gA x gB; fila vira gC,gA,gB
  lv3.lastWinner=1;lv3.lastGks={0:h1[0],1:h1[1]};
  const h2=planGks(liga,lv3,[1,2]);
  ok(h2.gks[0]==='gB'&&h2.fica[0]&&h2.gks[1]==='gC','3 goleiros: o do vencedor fica, o lado que troca recebe quem esperava (gC)');
  lv3.nextGks={pair:[1,2],gks:['gB','gA']};
  ok(planGks(liga,lv3,[1,2]).gks[1]==='gA'&&planGks(liga,lv3,[1,2]).manual,'escolha manual na pre-partida vence a sugestao');
  ok(!planGks(liga,lv3,[2,1]).manual,'a escolha manual so vale para aquele confronto');
}
liga.cfg.format=7;
ok(planTeams(liga,[...linha.slice(0,12),...gk2]).n===2,'7v7 com 12 de linha da 2 times');
liga.cfg.format=5;

console.log('\n[4] rating: expectativa, simetria e zebra');
const A5=['p1','p2','p3','p4','p5'], B5=['p10','p11','p12','p13','p14'];
const part=stintPart({lineups:[A5,B5],gks:[null,null]});
ok(Object.keys(part).length===10&&Object.values(part).every(x=>x.w===1&&x.role==='L'),'10 jogadores de linha, todos com peso 1');
const r=computeElo(liga,part,0), dA=r.deltas['p1'], dB=r.deltas['p10'];
console.log('  medias '+Math.round(r.avg[0])+' vs '+Math.round(r.avg[1])+' | chance do A='+(r.exp[0]*100).toFixed(1)+'% | dA='+dA+' dB='+dB);
ok(dA>0&&dB<0,'vencedor sobe, perdedor desce');
ok(dA+dB===0,'movimento simetrico entre os times');
const rU=computeElo(liga,part,1);
ok(Math.abs(rU.deltas['p10'])>Math.abs(dA),'zebra rende mais que o favorito confirmar');
const rd=computeElo(liga,part,'draw');
ok(rd.deltas['p1']<0&&rd.deltas['p10']>0,'empate: favorito perde, azarao ganha');
ok(KMODE.curtas.base>12,'racha curto (10 a 15 partidas por noite) pesa mais que na calibragem antiga de 25 partidas');
const divisao=stepMin(1)-stepMin(0);
const vitLiq=divisao/(KMODE.curtas.base/2);
console.log('  K='+KMODE.curtas.base+': subir uma divisao pede ~'+vitLiq.toFixed(1)+' vitorias liquidas');
ok(vitLiq>=3&&vitLiq<=5,'meia noite boa (3 a 5 vitorias liquidas) vale uma divisao');
{ /* Ferro 1 estabelecido (fora da calibracao) que vence 7 seguidas em times parelhos: tem que subir 2 divisoes na noite */
  const f=mk('Ferro1',stepMid(0),0);f.L.games=40;f.L.sessions=8;f.L.def=true;f.L.rank=0;liga.players.push(f);
  const par=[];for(let i=0;i<9;i++){const q=mk('Par'+i,stepMid(0),0);q.L.games=40;q.L.sessions=8;q.L.rank=0;liga.players.push(q);par.push(q.id)}
  const meu=[f.id,...par.slice(0,4)],eles=par.slice(4,9);
  const r0=f.L.rank;
  /* o balanceador remonta os times a cada partida para ficar ~50/50: aqui os outros voltam ao nivel de origem */
  for(let i=0;i<7;i++){par.forEach(id=>{const q=P(liga,id);q.L.elo=stepMid(0)});lanca(meu,eles,0,{sid:'noite-ferro'})}
  console.log('  Ferro 1 vencendo 7 seguidas: '+rankLabel(liga,r0)+' -> '+rankLabel(liga,f.L.rank)+' ('+Math.round(f.L.elo-stepMid(0))+' pts)');
  ok(f.L.rank-r0>=2,'7 vitorias seguidas em times parelhos sobem pelo menos 2 divisoes (antes: 1)');
  ok(streakK(f.L)===STREAK_K,'sequencia de 4+ liga o acelerador de K');
  ok(streakK({form:['V','E','V','V','D','V','E','V','V','V']})===STREAK_K,'7V-1D em 10 (com empates no meio) tambem liga o acelerador');
  ok(streakK({form:['V','D','V','E','D','V','D','V','D','E']})===1,'forma misturada nao liga');
  const km=KMODE.curtas;
  ok(kFor(km,{games:20})===km.base&&kFor(km,{games:60})===km.base,'ate 60 partidas o K e cheio');
  ok(kFor(km,{games:120})<km.base&&kFor(km,{games:120})>km.min,'com 120 partidas o K ja caiu, mas nao no piso');
  ok(kFor(km,{games:400})===km.min,'veterano de 400 partidas fica no piso (24)');
  /* veterano mal calibrado: K no piso, mas o acelerador o tira de la */
  const v=mk('Vet',stepMid(0),0);v.L.games=400;v.L.sessions=60;v.L.def=true;v.L.rank=0;liga.players.push(v);
  const meu2=[v.id,...par.slice(0,4)];
  for(let i=0;i<7;i++){par.forEach(id=>{const q=P(liga,id);q.L.elo=stepMid(0)});lanca(meu2,eles,0,{sid:'noite-vet'})}
  console.log('  veterano (400 partidas) vencendo 7 seguidas: '+rankLabel(liga,0)+' -> '+rankLabel(liga,v.L.rank)+' ('+Math.round(v.L.elo-stepMid(0))+' pts)');
  ok(v.L.rank>=1,'veterano preso la embaixo sobe pelo menos 1 divisao numa noite perfeita');
}

console.log('\n[5] trechos: cada formacao em campo e uma partida');
let pt=partida(A5,B5,{dur:8*MIN,events:[{at:4*MIN,type:'sub',side:0,out:'p1',in:'p6'}],fimA:['p6','p2','p3','p4','p5']});
console.log('  8 min com troca aos 4: '+pt.stints.length+' trechos de peso '+pt.stints.map(s=>s.w).join(' / '));
ok(pt.stints.length===2,'a substituicao fecha um trecho e abre outro');
ok(Math.abs(pt.stints[0].w-0.5)<0.01&&Math.abs(pt.stints[1].w-0.5)<0.01,'cada trecho vale metade da partida');
ok(pt.stints.every(s=>s.counted),'trecho de 4 min conta');
ok(pt.stints[0].lineups[0].includes('p1')&&pt.stints[1].lineups[0].includes('p6'),'o trecho novo tem o set novo de jogadores');
ok(Math.abs(pt.stints[0].w+pt.stints[1].w-1)<0.01,'os trechos somados valem uma partida — 2 trechos nao valem em dobro');

pt=partida(A5,B5,{dur:8*MIN,events:[{at:2*MIN,type:'sub',side:0,out:'p1',in:'p6'}],fimA:['p6','p2','p3','p4','p5']});
console.log('  8 min com troca aos 2: contam '+pt.stints.filter(s=>s.counted).length+' de '+pt.stints.length+' trechos');
ok(!pt.stints[0].counted,'trecho cortado por troca com menos de 4 min e descartado');
ok(pt.stints[1].counted,'o trecho que termina no apito conta sempre');
ok(Math.abs(pt.stints[1].w-1)<0.01,'o peso do trecho descartado e redistribuido: a partida continua valendo 1');

/* O minimo e relativo: num racha de 7 min, 4 min fixos fariam qualquer troca
   descartar quase a partida inteira.                                        */
pt=partida(A5,B5,{dur:7*MIN,events:[{at:3.5*MIN,type:'sub',side:0,out:'p1',in:'p6'}],fimA:['p6','p2','p3','p4','p5']});
ok(pt.stints.every(s=>s.counted),'partida de 7 min com troca na metade: os dois trechos contam');
ok(Math.abs(pt.stints[0].w+pt.stints[1].w-1)<0.01,'e continuam somando uma partida');

/* Protecao pos-promocao: a unidade e o trecho, como em todo o resto do motor. */
liga.matches.length=0;rebuildAll(liga);
const prot=P(liga,'p2');prot.L.protect=3;
lanca(A5,B5,0,{dur:10*MIN,events:[{at:5*MIN,type:'sub',side:0,out:'p1',in:'p6'}],fimA:['p6','p2','p3','p4','p5']});
ok(prot.L.protect===1,'a protecao e contada em trechos: 2 trechos gastam 2');
liga.matches.length=0;rebuildAll(liga);

pt=partida(A5,B5,{dur:10*MIN,
  events:[{at:3*MIN,type:'goal',side:0},{at:5*MIN,type:'sub',side:0,out:'p1',in:'p6'},{at:7*MIN,type:'goal',side:1}],
  fimA:['p6','p2','p3','p4','p5'],score:[1,1]});
ok(pt.stints[0].score[0]===1&&pt.stints[0].score[1]===0&&pt.stints[0].result===0,'o 1o trecho fica com o gol que aconteceu nele');
ok(pt.stints[1].score[1]===1&&pt.stints[1].result===1,'o placar volta a zero na troca — o 2o trecho e do time que marcou depois');

liga.matches.length=0;rebuildAll(liga);
lanca(A5,B5,undefined,{dur:10*MIN,score:[1,1],goals:[],resultados:[0,1],
  events:[{at:5*MIN,type:'sub',side:0,out:'p1',in:'p6'}],fimA:['p6','p2','p3','p4','p5']});
console.log('  p1 (saiu no meio) '+(elo('p1')-P(liga,'p1').L.base)+' | p6 (entrou) '+(elo('p6')-P(liga,'p6').L.base)+' | p2 (jogou tudo) '+(elo('p2')-P(liga,'p2').L.base));
ok(elo('p1')>P(liga,'p1').L.base,'quem saiu leva so o trecho que jogou — e nele o time venceu');
ok(elo('p6')<P(liga,'p6').L.base,'quem entrou leva so o trecho dele — e nele o time perdeu');
ok(P(liga,'p1').L.games===1&&P(liga,'p2').L.games===2,'quem jogou os dois trechos conta dois; quem jogou um, conta um');
liga.matches.length=0;rebuildAll(liga);

console.log('\n[6] calibracao');
liga.players.forEach(p=>{p.L.games=20;p.L.sessions=6});
const novato=mk('Novato',1500,0);liga.players.push(novato);
const partN=stintPart({lineups:[[novato.id,'p2','p3'],['p10','p11','p12']],gks:[null,null]});
const rn=computeElo(liga,partN,0);
ok(Math.abs(rn.deltas[novato.id])>Math.abs(rn.deltas['p2']),'novato anda mais rapido ('+rn.deltas[novato.id]+' vs '+rn.deltas['p2']+')');
const cal=mk('Cal',1500,0);
ok(calibrando(liga,cal,cal.L),'quem chega esta calibrando');
const CG=liga.cfg.calGames,CR=liga.cfg.calRachas;
ok(CG===CAL_GAMES&&CR===CAL_RACHAS,'calibracao e fixa: '+CG+' partidas ou '+CR+' rachas, sem opcao por liga');
cal.L.games=CG-1;cal.L.sessions=CR-1;
ok(calibrando(liga,cal,cal.L),(CG-1)+' partidas em '+(CR-1)+' rachas: ainda calibrando');
cal.L.games=CG;
ok(!calibrando(liga,cal,cal.L),CG+' partidas encerra a calibracao');
cal.L.games=6;cal.L.sessions=CR;
ok(!calibrando(liga,cal,cal.L),CR+' rachas encerra a calibracao mesmo com poucas partidas');
/* a calibracao precisa corrigir um cadastro errado em uma ou duas noites */
const errado=mk('Errado',1500,0);liga.players.push(errado);
let ganho=0;for(let i=0;i<12;i++){const r=computeElo(liga,stintPart({lineups:[[errado.id,'p2','p3'],['p10','p11','p12']],gks:[null,null]}),0,'curtas');ganho+=r.deltas[errado.id]}
liga.players.pop();
ok(ganho>=STEP*2,'12 vitorias em calibracao ja sobem mais de duas divisoes ('+Math.round(ganho)+' pts)');
ok(calibrando(liga,cal,cal.G),'a patente de goleiro dele continua calibrando — sao trilhas separadas');
liga.players.forEach(p=>{['L','G'].forEach(k=>{p[k].games=0;p[k].sessions=0})});

console.log('\n[7] histerese: nao pode virar ioio');
const cut=stepMin(8);
const h=mk('Limite',Math.round(cut)-5,0);h.L.games=30;h.L.sessions=9;liga.players.push(h);h.L.rank=7;
h.L.elo=Math.round(cut)+10; updateRank(liga,h,h.L);
ok(h.L.rank===7,'passar o corte por pouco (menos que a margem) NAO promove');
h.L.elo=Math.round(cut)+25; updateRank(liga,h,h.L);
ok(h.L.rank===8,'passar o corte com folga promove');
ok(h.L.protect===liga.cfg.protectMatches,'quem sobe ganha protecao de '+liga.cfg.protectMatches+' partidas');
h.L.elo=Math.round(cut)-40;
let stayed=true;
for(let i=0;i<liga.cfg.protectMatches;i++){updateRank(liga,h,h.L);if(h.L.rank!==8)stayed=false;}
ok(stayed,'nao cai enquanto esta protegido');
updateRank(liga,h,h.L);
ok(h.L.rank===7,'depois da protecao, cai de verdade');
let flips=0,prev=h.L.rank;
for(let i=0;i<12;i++){h.L.elo=Math.round(cut)+(i%2?12:-12);updateRank(liga,h,h.L);if(h.L.rank!==prev){flips++;prev=h.L.rank}}
console.log('  oscilando +-12 pontos em volta do corte: '+flips+' mudanca(s) de patente');
ok(flips===0,'oscilacao dentro da margem nao mexe na patente');

console.log('\n[8] aplicar / recalcular / anular');
liga.matches.length=0;rebuildAll(liga);
const m1=lanca(A5,B5,0), m2=lanca(A5,B5,1), m3=lanca(A5,B5,0);
const snapOf=()=>liga.players.map(p=>p.L.elo+':'+p.L.rank+':'+p.L.games+':'+p.L.w+':'+p.G.elo+':'+p.G.games+':'+p.goals).join('|');
const snap=snapOf();
rebuildAll(liga);
ok(snap===snapOf(),'recalculo do zero bate com o incremental');
ok(P(liga,'p1').L.games===3&&P(liga,'p1').goals===3,'partidas e gols contabilizados');
m2.voided=true;rebuildAll(liga);
ok(P(liga,'p1').L.games===2,'partida anulada nao conta');
m2.voided=false;rebuildAll(liga);
ok(snap===snapOf(),'reativar devolve o estado exato');
liga.matches.length=0;rebuildAll(liga);
ok(liga.players.every(p=>p.L.elo===p.L.base&&p.L.rank===stepOf(p.L.base)),'sem partidas, todos voltam ao nivel de entrada');
ok(liga.players.every(p=>!p.sessions),'contagem de rachas tambem zera');

console.log('');console.log('[8b] contagem de rachas por jogador');
liga.matches.length=0;
['r1','r1','r1','r2'].forEach(sid=>lanca(A5,B5,0,{sid}));
rebuildAll(liga);
ok(P(liga,'p1').L.games===4&&P(liga,'p1').sessions===2,'4 partidas em 2 rachas contam como 2 rachas');
liga.matches.length=0;rebuildAll(liga);

console.log('');console.log('[8c] o formato e do racha, nao da liga');
const partM=stintPart({lineups:[A5,B5],gks:[null,null]});
const dCurta=computeElo(liga,partM,0,'curtas').deltas['p1'];
const dUnica=computeElo(liga,partM,0,'unica').deltas['p1'];
console.log('  mesma vitoria: racha curto move '+dCurta+', racha de partida unica move '+dUnica);
ok(Math.abs(dUnica)>Math.abs(dCurta),'partida unica pesa mais que uma partida curta');
const mCurta=lanca(A5,B5,0,{mode:'curtas',sid:'rA'}), mUnica=lanca(A5,B5,0,{mode:'unica',sid:'rB'});
rebuildAll(liga);
console.log('  historico misto: racha curto '+mCurta.deltas['p1']+' | racha longo '+mUnica.deltas['p1']);
ok(Math.abs(mUnica.deltas['p1'])>Math.abs(mCurta.deltas['p1']),'no mesmo historico, cada partida mantem o peso do seu racha');
const congelado=JSON.stringify(mCurta.deltas);
liga.cfg.matchMode='unica';rebuildAll(liga);
ok(JSON.stringify(mCurta.deltas)===congelado,'mudar o padrao da liga nao mexe em partida ja jogada');
liga.cfg.matchMode='curtas';
liga.matches.length=0;rebuildAll(liga);

console.log('\n[9] goleiro tem patente propria');
const gk=P(liga,gk2[0]);
lanca([gk.id,'p2','p3'],['p10','p11','p12'],0,{gks:[gk.id,null]});
console.log('  patente de gol: '+(gk.G.elo-gk.G.base)+' | patente de linha: '+(gk.L.elo-gk.L.base));
ok(gk.G.elo>gk.G.base,'o goleiro ganha patente de goleiro quando o lado dele vence');
ok(gk.L.elo===gk.L.base&&gk.L.games===0,'a patente de linha dele nao se mexe');
ok(P(liga,'p2').L.elo>P(liga,'p2').L.base,'os de linha continuam pontuando na trilha de linha');
const dedo=P(liga,'p11');
lanca(['p2','p3','p4'],[dedo.id,'p12','p13'],0,{gks:[null,dedo.id]});
ok(dedo.G.games===1&&dedo.G.elo<dedo.G.base,'quem improvisa no gol mexe a patente de goleiro, nao a de linha');
ok(!P(liga,gk2[0]).gk===false,'o cadastro so diz quem costuma ir ao gol');
liga.matches.length=0;rebuildAll(liga);

console.log('\n[10] equilibrio primeiro, panelinha depois');
liga.cfg.avoidRepeat=true;
liga.matches.length=0;
/* 10 jogadores do mesmo nivel: com o equilibrio empatado, quem decide e a
   repeticao de duplas. Os 3 rachas anteriores foram sempre com os mesmos times. */
const iguais=[];for(let i=0;i<10;i++){const q=mk('Igual'+i,1500,0);liga.players.push(q);iguais.push(q.id)}
const velhoA=iguais.filter((_,i)=>i%2===0),velhoB=iguais.filter((_,i)=>i%2===1);
for(let i=0;i<3;i++)lanca(velhoA,velhoB,'draw',{sid:'rr'+i,goals:[]});
const pc=pairCounts(liga);
ok(pc[pairKey(velhoA[0],velhoA[1])]===3,'dupla que jogou junta em 3 rachas conta 3');
/* 30 montagens de cada lado: com o ruido de montagem, uma amostra pequena
   as vezes empata por acaso e o teste vira moeda.                        */
const conta=ids=>{let n=0;
  for(let t=0;t<30;t++)buildTeams(liga,ids,2).forEach(x=>{
    for(let i=0;i<x.ids.length;i++)for(let j=i+1;j<x.ids.length;j++)n+=(pc[pairKey(x.ids[i],x.ids[j])]||0)});
  return n};
const evitando=conta(iguais);
liga.cfg.avoidRepeat=false;const semEvitar=conta(iguais);liga.cfg.avoidRepeat=true;
console.log('  duplas repetidas em 30 montagens: '+evitando+' evitando, '+semEvitar+' sem evitar');
ok(evitando<semEvitar,'entre arranjos igualmente equilibrados, o app separa quem sempre joga junto');
let pior=0;
const dez=linha.slice(0,10);
for(let t=0;t<12;t++){
  const avgs=buildTeams(liga,dez,2).map(x=>teamAvg(liga,x));
  pior=Math.max(pior,Math.abs(avgs[0]-avgs[1]));
}
console.log('  com niveis diferentes, pior desequilibrio em 12 montagens: '+Math.round(pior));
ok(pior<=40,'e o equilibrio continua sendo a prioridade');
liga.matches.length=0;rebuildAll(liga);

console.log('\n[11] duelos, parcerias e numeros');
liga.matches.length=0;rebuildAll(liga);
lanca(A5,B5,0,{sid:'d1'});lanca(A5,B5,0,{sid:'d1'});lanca(A5,B5,1,{sid:'d2'});
let SL=statsLiga(liga,'sempre');
ok(SL.J['p1'].jogos===3&&SL.J['p1'].v===2&&SL.J['p1'].d===1,'3 partidas do p1: 2V 1D');
ok(SL.J['p1'].nR===2,'as 3 partidas aconteceram em 2 rachas');
ok(SL.DU['p1']['p10'].n===3&&SL.DU['p1']['p10'].v===2,'duelo p1 x p10: 3 confrontos, 2 vitorias do p1');
ok(SL.DU['p10']['p1'].v===1&&SL.DU['p10']['p1'].d===2,'do outro lado, o espelho exato');
ok(SL.PA['p1']['p2'].n===3&&SL.PA['p1']['p2'].v===2,'parceria p1+p2 conta os 3 jogos juntos');
ok(!SL.DU['p1']['p2'],'quem joga do seu lado nao vira duelo');
ok(!SL.PA['p1']['p10'],'quem joga contra nao vira parceria');
ok(!SL.DU['p1']['p1']&&!SL.PA['p1']['p1'],'ninguem duela nem faz dupla consigo mesmo');
const enc=encontros(liga,'p1','p10','sempre',false);
console.log('  historico do duelo: '+enc.map(x=>x.res+' '+x.placar.join('-')+' ('+x.fmt+')').join(' | '));
ok(enc.length===3,'o historico do duelo traz os 3 encontros');
ok(enc.every(x=>x.fmt==='5v5'),'cada encontro guarda o formato em que aconteceu');
ok(enc.filter(x=>x.res==='V').length===2,'e o resultado pelo lado de quem esta olhando');

liga.matches.length=0;rebuildAll(liga);
lanca(['p1','p2','p3'],['p10','p11'],0,{sid:'f1'});
const desigual=statsLiga(liga,'sempre');
ok(desigual.DU['p1']['p10'].n===1&&desigual.PA['p10']['p11'].n===1,'3 contra 2 conta igual: o que vale e quem estava em quadra');
const enc12=encontros(liga,'p1','p10','sempre',false);
ok(enc12.length===1&&enc12[0].fmt==='3v2','o formato do encontro sai do tamanho real dos lados');

liga.matches.length=0;rebuildAll(liga);
lanca(A5,B5,undefined,{dur:10*MIN,resultados:[0,1],
  events:[{at:5*MIN,type:'sub',side:0,out:'p1',in:'p6'}],fimA:['p6','p2','p3','p4','p5']});
const comSub=statsLiga(liga,'sempre');
ok(comSub.DU['p1']['p10'].n===1&&comSub.DU['p1']['p10'].v===1,'quem saiu duela so no trecho que jogou');
ok(comSub.DU['p6']['p10'].n===1&&comSub.DU['p6']['p10'].d===1,'quem entrou leva so o trecho dele');
ok(!comSub.PA['p1']['p6'],'quem se substituiu nunca esteve em quadra junto');

liga.matches.length=0;rebuildAll(liga);
lanca(A5,B5,0,{sid:'novo'});
const velho=lanca(A5,B5,1,{sid:'velho'});
velho.ts=new Date(ANO_ATUAL()-1,5,1).getTime();
rebuildAll(liga);
ok(statsLiga(liga,'ano').J['p1'].jogos===1,'partida do ano passado fica fora do ano atual');
ok(statsLiga(liga,'sempre').J['p1'].jogos===2,'mas continua no total de sempre');
const anos=statsAnos(liga,'p1');
console.log('  ano a ano do p1: '+anos.map(a=>a.ano+' ('+a.jogos+'j '+a.v+'V)').join(' | '));
ok(anos.length===2&&anos[0].ano===ANO_ATUAL(),'ano a ano separa as temporadas, mais recente primeiro');
ok(anos[0].v===1&&anos[1].d===1,'cada ano com o seu retrospecto');
liga.matches.length=0;rebuildAll(liga);

console.log('\n[13] destaques do periodo: quem rendeu acima do esperado');
liga.matches.length=0;rebuildAll(liga);
const mFav=lanca(A5,B5,0,{goals:[]});                       // o favorito confirma
const soma=Object.keys(mFav.over).reduce((a,k)=>a+mFav.over[k],0);
console.log('  favorito vence: p1 rende '+mFav.over['p1'].toFixed(2)+' | soma da partida '+soma.toFixed(3));
ok(Math.abs(soma)<0.001,'o que um lado ganha acima do esperado o outro perde: a partida soma zero');
ok(mFav.over['p1']>0&&mFav.over['p1']<0.5,'favorito que confirma rende pouco');
liga.matches.length=0;rebuildAll(liga);
const mZeb=lanca(A5,B5,1,{goals:[]});                       // a zebra
console.log('  zebra vence: p10 rende '+mZeb.over['p10'].toFixed(2));
ok(mZeb.over['p10']>0.5,'ganhar de quem e mais forte rende muito');
ok(mZeb.over['p10']>mFav.over['p1'],'e rende mais do que confirmar favoritismo');

liga.matches.length=0;rebuildAll(liga);
for(let i=0;i<24;i++)lanca(A5,B5,1,{sid:'d'+(i%3),goals:[{pid:'p10',side:1},{pid:'p10',side:1}]});
const D=destaques(liga,5000);
console.log('  top do periodo: '+D.top.map(x=>P(liga,x.pid).name+' '+x.over.toFixed(1)).join(' | '));
ok(D.partidas===24&&D.nR===3,'conta partidas e rachas do periodo');
ok(D.top.length===3&&D.top.every(x=>B5.indexOf(x.pid)>=0),'quem venceu o time mais forte domina o top 3');
ok(D.artilheiro&&D.artilheiro.pid==='p10'&&D.artilheiro.gols===48,'artilheiro do periodo, quando os gols tem dono');

/* os melhores do racha: a escada, so entre quem apareceu no periodo */
ok(D.melhores.length===3,'tres melhores do racha');
ok(D.melhores.every(x=>[...A5,...B5].indexOf(x.pid)>=0),'so entra quem apareceu no periodo');
const degraus=D.melhores.map(x=>rt(P(liga,x.pid),x.val).rank);
console.log('  melhores: '+D.melhores.map(x=>P(liga,x.pid).name+' ('+rankLabel(liga,rt(P(liga,x.pid),x.val).rank)+')').join(' | '));
ok(degraus[0]>=degraus[1]&&degraus[1]>=degraus[2],'ordenados do maior degrau para o menor');
ok(D.melhores.every(x=>temPatente(P(liga,x.pid),x.val)),'ninguem sem patente na valencia entra na lista');

/* piso duplo: uma noite boa nao faz destaque do mes */
liga.matches.length=0;rebuildAll(liga);
for(let i=0;i<19;i++)lanca(A5,B5,1,{sid:'q'+(i%2),goals:[]});
ok(destaques(liga,5000).top.length===0,'com menos de 20 partidas no periodo, ninguem vira destaque');
liga.matches.length=0;rebuildAll(liga);
for(let i=0;i<30;i++)lanca(A5,B5,1,{sid:'so-um-racha',goals:[]});
ok(destaques(liga,5000).top.length===0,'e 30 partidas em um racha so tambem nao valem');
const overAntes=JSON.stringify(liga.matches.map(m=>m.over));
rebuildAll(liga);
ok(JSON.stringify(liga.matches.map(m=>m.over))===overAntes,'recalculo do zero devolve o mesmo acima do esperado');

liga.matches.length=0;rebuildAll(liga);
for(let i=0;i<24;i++)lanca(A5,B5,0,{sid:'e'+(i%3),goals:[{pid:null,side:0},{pid:null,side:0}]});
ok(!destaques(liga,5000).artilheiro,'sem autor na maioria dos gols, nao inventa artilheiro');

liga.matches.length=0;rebuildAll(liga);
const gA=gk2[0],gB=gk2[1],lA=[...A5.slice(0,4),gA],lB=[...B5.slice(0,4),gB];
for(let i=0;i<2;i++)lanca(lA,lB,0,{sid:'g'+i,gks:[gA,gB],score:[2,0],goals:[],
  events:[{at:1*MIN,type:'goal',side:0},{at:2*MIN,type:'goal',side:0}]});
const DG=destaques(liga,5000);
console.log('  goleiros: '+DG.gente.filter(x=>x.jogosG).map(x=>P(liga,x.pid).name+' '+x.sofridos+' em '+x.jogosG).join(' | '));
ok(DG.goleiro&&DG.goleiro.pid===gA,'menos vazado: o goleiro com menos gols sofridos por partida');
ok(DG.goleiro.sofridos===0&&DG.goleiro.jogosG===2,'e a conta sai dos trechos em que ele estava no gol');

liga.matches.length=0;rebuildAll(liga);
ok(destaques(liga,30).partidas===0,'sem partida no periodo, o bloco nao inventa destaque');

console.log('\n[12] desempenho');
const t1=Date.now();
for(let i=0;i<400;i++)lanca(A5,B5,i%3===0?1:0);
rebuildAll(liga);
console.log('  '+liga.matches.length+' partidas recalculadas em '+(Date.now()-t1)+' ms');
ok(Date.now()-t1<2000,'recalculo integral abaixo de 2 s');
const t2=Date.now();const painel=statsLiga(liga,'sempre');
console.log('  painel de numeros (duelos e parcerias de todos) em '+(Date.now()-t2)+' ms');
ok(Date.now()-t2<300,'painel de numeros abaixo de 300 ms com '+liga.matches.length+' partidas');
ok(Object.keys(painel.DU).length>0,'e ele volta com duelos preenchidos');

console.log('\n[14] gol contra');
{
  const gA=P(liga,A5[0]).goals,gB=P(liga,B5[0]).goals;
  const jbAntes=(statsLiga(liga,'sempre').J[B5[0]]||{gols:0}).gols;
  lanca(A5,B5,0,{score:[2,0],goals:[{pid:A5[0],side:0},{pid:B5[0],side:0,own:true}]});
  ok(P(liga,A5[0]).goals===gA+1,'gol normal conta para o autor');
  ok(P(liga,B5[0]).goals===gB,'gol contra NAO conta como gol do autor');
  ok(P(liga,B5[0]).gc===1,'gol contra fica registrado a parte (gc)');
  rebuildAll(liga);
  ok(P(liga,B5[0]).gc===1&&P(liga,B5[0]).goals===gB,'e sobrevive ao recalculo');
  ok((statsLiga(liga,'sempre').J[B5[0]]||{gols:0}).gols===jbAntes,'artilharia do painel ignora o gol contra');
}

console.log('\n[15] dupla inseparavel');
{
  const x=mk('Cola1',stepMid(6),0),y=mk('Cola2',stepMid(6),0);liga.players.push(x,y);
  const outros=[];for(let i=0;i<8;i++){const q=mk('Out'+i,stepMid(6),0);liga.players.push(q);outros.push(q.id)}
  for(let i=0;i<45;i++)lanca([x.id,y.id,...outros.slice(0,3)],outros.slice(3,8),i%2,{sid:'s-cola'+Math.floor(i/8)});
  const j=inseparaveis(liga);
  ok(j.some(d=>(d.a===x.id&&d.b===y.id)||(d.a===y.id&&d.b===x.id)),'45 partidas sempre juntos: a dupla e apontada');
  ok(x.L.elo===y.L.elo,'e de fato os dois tem o mesmo elo — o motivo do aviso');
  ok(!j.some(d=>d.a===outros[0]&&d.b===outros[1]&&d.pct<JUNTOS_PCT),'quem tambem jogou separado nao e apontado');
}

console.log(fails?'\n*** '+fails+' FALHA(S) ***':'\nTODOS OS TESTES PASSARAM');
process.exit(fails?1:0);
"""

io.open(os.path.join(OUT, 'core.js'), 'w', encoding='utf-8').write(core + harness)

if subprocess.run(['node', '--check', os.path.join(OUT, 'full.js')]).returncode != 0:
    print('ERRO DE SINTAXE em index.html')
    sys.exit(1)
print('sintaxe do index.html: ok')
sys.exit(subprocess.run(['node', os.path.join(OUT, 'core.js')]).returncode)
