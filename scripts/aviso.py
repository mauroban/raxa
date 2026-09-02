# -*- coding: utf-8 -*-
"""Régua da D-94: o aviso "revisar palpite?" (D-83, removido) apontava quem estava
uma patente fora? Mesmo modelo do converge.py (cenário poucos/misto), motor real, com
o ranking de surpresa da D-83 reimplementado aqui (3 pontas de cada lado, últimos 8
rachas, soma de resultado − esperado por √partidas, mínimo 10 partidas).

Uso:  python scripts/aviso.py [poucos|misto] [rachas] [ligas] [remontagens por noite]
Saída: em que racha o errado é apontado pela primeira vez; taxa por racha de errado
× certo apontados; persistência em k dos últimos 8; deriva do Elo como alternativa."""
import io, os, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.path.isdir(os.path.join(ROOT,'scripts','.tmp')) or os.makedirs(os.path.join(ROOT,'scripts','.tmp'))
html = io.open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
js = html.split('<script>')[1].split('</script>')[0]
core = js.split('/* @@FIM-DO-MOTOR@@')[0].replace('const save=()=>{saveUI();markDirty(S.active)}', 'const save=()=>{}')
sim = r"""
/* o ranking de surpresa da D-83, como era no index.html antes da D-94 */
const REVISAR_RACHAS=8, REVISAR_MIN=10, REVISAR_PONTAS=3;
function rankingSurpresa(liga,role){
  const ms=(liga.matches||[]).filter(m=>!m.voided&&m.overR).sort((a,b)=>a.ts-b.ts);
  const sids=[];ms.forEach(m=>{const sid=m.sessionId||m.id;if(sids.indexOf(sid)<0)sids.push(sid)});
  const ult=sids.slice(-REVISAR_RACHAS),acc={};
  ms.forEach(m=>{if(ult.indexOf(m.sessionId||m.id)<0)return;
    for(const k in m.overR){if(k.slice(-1)!==role)continue;const pid=k.slice(0,-1);const a=acc[pid]||(acc[pid]={pid,soma:0,n:0});a.soma+=m.overR[k];a.n++}});
  const lista=Object.keys(acc).map(pid=>acc[pid]).filter(a=>a.n>=REVISAR_MIN).map(a=>({pid:a.pid,soma:a.soma,n:a.n,z:a.soma/Math.sqrt(a.n)})).sort((a,b)=>b.z-a.z);
  const out={total:lista.length,rachas:ult.length,pos:{}};
  lista.forEach((a,i)=>out.pos[a.pid]={pos:i+1,n:a.n,soma:a.soma});
  return out;
}
const revisar=(liga,p,role,rv)=>{const x=rv.pos[p.id];
  if(!x||rv.total<2*REVISAR_PONTAS||!temPatente(liga,p,role))return 0;return x.pos<=REVISAR_PONTAS?1:x.pos>rv.total-REVISAR_PONTAS?-1:0};
const CEN=process.argv[2]||'poucos',RACHAS=parseInt(process.argv[3]||'40'),LIGAS=parseInt(process.argv[4]||'200');
const POOL=20,PART=12,MIX=parseInt(process.argv[5]||'-1');   // -1 = como no converge.py (25% remonta no meio); 0..3 = remontagens certas por noite
let _i=0;const nid=()=>'p'+(++_i);
function gauss(){let u=0,v=0;while(!u)u=Math.random();while(!v)v=Math.random();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v)}
function poisson(l){let L=Math.exp(-l),k=0,p=1;do{k++;p*=Math.random()}while(p>L);return k-1}
function resultado(ta,tb){const r=Math.pow(10,(ta-tb)/400),la=0.5*r/(1+r),lb=0.5/(1+r);let ga=0,gb=0;
  for(let m=0;m<7&&ga<2&&gb<2;m++){ga+=poisson(la);gb+=poisson(lb)}return ga===gb?'draw':(ga>gb?0:1)}
function mk(name,elo,def){return{id:nid(),name,gk:false,L:newTrack(elo,def),G:newTrack(1500),goals:0,sessions:0,lastSession:null,owner:null,role:'lancador'};}
const primeiro=[],primeiroSub=[],primeiroSup=[],falsos=Array.from({length:RACHAS},()=>0),flagPersist=[];
const LIM=[34,50,67,100],drift={},conv={};let nJust=0,nW=0,nWe=0,fW=0,fWe=0,nC=0,fC=0,nWin=0,nCin=0;const sensW={2:0,3:0,4:0,5:0,6:0},fpC={2:0,3:0,4:0,5:0,6:0};
for(let l=0;l<LIGAS;l++){
  const liga={id:'x',name:'t',cfg:defCfg(),players:[],matches:[],sessions:[],live:null};
  const truth={},freq={},errados={};
  for(let i=0;i<POOL;i++){
    const t=clamp(Math.round(1500+gauss()*200),1000,1999);
    const ruim=(CEN==='misto'&&i<5)||(CEN==='poucos'&&(i===4||i===5));
    const e=ruim?(Math.random()<.5?-3:3):(Math.random()<.5?0:(Math.random()<.5?-1:1));
    const elo=stepMid(clamp(stepOf(t)+e,0,TOP));
    const p=mk('j'+i,elo,true);truth[p.id]=t;liga.players.push(p);
    freq[p.id]=i<4?0.33:0.6+0.35*Math.random();
    if(Math.abs(stepOf(elo)-stepOf(t))>=2)errados[p.id]=stepOf(elo)>stepOf(t)?-1:1;   // -1 superestimado (deve cair), +1 subestimado
  }
  S.ligas=[liga];S.active=liga.id;
  const flagAt={},flagCnt={},hist={};
  for(let r=0;r<RACHAS;r++){
    let ids=liga.players.filter(p=>Math.random()<freq[p.id]).map(p=>p.id);
    while(ids.length<13){const p=liga.players[Math.floor(Math.random()*POOL)];if(ids.indexOf(p.id)<0)ids.push(p.id)}
    ids=ids.slice(0,18);
    const montar=()=>{const n=ids.length>=16?4:3;const t=buildTeams(liga,ids,n,null,[],false);return (t.teams||t).map(x=>(x.ids||x).map(y=>y.id||y)).filter(x=>x.length)};
    let T=montar();
    const remonta=MIX<0?Math.random()<.25:false;let fila=T.map((_,i)=>i);
    const pontos=MIX>0?Array.from({length:MIX},(_,j)=>Math.round(PART*(j+1)/(MIX+1))):[];
    for(let k=0;k<PART;k++){
      if((remonta&&k===Math.floor(PART/2))||pontos.includes(k)){T=montar();fila=T.map((_,i)=>i)}
      const a=fila[0],b=fila[1];
      const part={};T[a].forEach(id=>part[id]={side:0,w:1,role:'L'});T[b].forEach(id=>part[id]={side:1,w:1,role:'L'});
      const avg=t=>t.reduce((s,id)=>s+truth[id],0)/t.length;
      const res=resultado(avg(T[a]),avg(T[b]));
      const c=computeElo(liga,part,res,'curtas',1);
      const overR={};
      for(const id in part){const p=P(liga,id),tr=p.L;tr.elo+=c.deltas[id]||0;updateRank(liga,p,tr);tr.games++;
        const sd=part[id].side,Sv=res==='draw'?.5:(res===sd?1:0);overR[id+'L']=Sv-c.exp[sd]}
      liga.matches.push({id:'m'+liga.matches.length,ts:r*1e6+k,sessionId:'s'+r,overR,voided:false});
      fila.shift();fila.shift();
      if(res===0){fila.push(b);fila.unshift(a)}else if(res===1){fila.push(a);fila.unshift(b)}
      else if(T.length>=4){fila.push(a);fila.push(b)}else{fila.push(a);fila.unshift(b)}
    }
    [10,20,40].forEach(rr=>{if(r+1!==rr)return;liga.players.forEach(p=>{if(!errados[p.id])return;const C=conv[rr]=conv[rr]||{ok:0,n:0};C.n++;
      const el=liga.players.map(x=>x.L.elo),tv=liga.players.map(x=>truth[x.id]);const mE=el.reduce((a,b)=>a+b,0)/POOL,mT=tv.reduce((a,b)=>a+b,0)/POOL;
      if(Math.abs(p.L.rank-stepOf(truth[p.id]-mT+mE))<=1)C.ok++})});
    const rv=rankingSurpresa(liga,'L');
    liga.players.forEach(p=>{const d=revisar(liga,p,'L',rv);
      (hist[p.id]=hist[p.id]||[]).push(d);
      const aindaErrado=errados[p.id]&&Math.abs(p.L.rank-stepOf(truth[p.id]))>=2;
      if(errados[p.id]){nW++;if(aindaErrado)nWe++;if(d===errados[p.id]){fW++;if(aindaErrado)fWe++}}else{nC++;if(d!==0)fC++}
      if(r>=7){const ult=hist[p.id].slice(-8);
        if(errados[p.id]){const k=ult.filter(x=>x===errados[p.id]).length;for(let t=2;t<=6;t++)if(k>=t)sensW[t]++;nWin++}
        else{const k=Math.max(ult.filter(x=>x===1).length,ult.filter(x=>x===-1).length);for(let t=2;t<=6;t++)if(k>=t)fpC[t]++;nCin++}}
      /* alternativa: a deriva do próprio Elo em relação ao palpite de entrada */
      const der=p.L.elo-p.L.base;
      [[8,'r8'],[16,'r16'],[24,'r24']].forEach(([rr,k])=>{if(r+1!==rr)return;
        LIM.forEach(lim=>{const key=k+'|'+lim;const D=drift[key]=drift[key]||{w:0,nw:0,c:0,nc:0};
          if(errados[p.id]){D.nw++;if(der*errados[p.id]>=lim)D.w++}else{D.nc++;if(Math.abs(der)>=lim)D.c++}})});
      if(errados[p.id]){if(d===errados[p.id]){flagCnt[p.id]=(flagCnt[p.id]||0)+1;if(flagAt[p.id]===undefined)flagAt[p.id]=r+1}}
      else if(d!==0){falsos[r]++;nJust++}
    });
  }
  for(const id in errados){const f=flagAt[id]===undefined?Infinity:flagAt[id];primeiro.push(f);(errados[id]>0?primeiroSub:primeiroSup).push(f);
    if(flagAt[id]!==undefined)flagPersist.push(flagCnt[id]/(RACHAS-flagAt[id]+1))}
}
const q=(arr,p)=>{const s=[...arr].sort((a,b)=>a-b);return s[Math.min(s.length-1,Math.floor(p*s.length))]};
const fmt=arr=>`25%: ${q(arr,.25)} · mediana: ${q(arr,.5)} · 75%: ${q(arr,.75)} · nunca em ${RACHAS}: ${Math.round(100*arr.filter(x=>x===Infinity).length/arr.length)}%`;
const ate=(arr,n)=>Math.round(100*arr.filter(x=>x<=n).length/arr.length)+'%';
console.log('MIX='+MIX+' · errado dentro de ±1 div no racha 10/20/40: '+[10,20,40].map(rr=>rr+':'+(conv[rr]?Math.round(100*conv[rr].ok/conv[rr].n)+'%':'-')).join(' '));
console.log('cenário '+CEN+' · '+LIGAS+' ligas · racha em que o aviso aponta o errado pela primeira vez (na direção certa):');
console.log('  todos os errados  → '+fmt(primeiro));
console.log('  subestimado (📈)  → '+fmt(primeiroSub));
console.log('  superestimado (📉)→ '+fmt(primeiroSup));
console.log('  já apontado até o racha 4/8/12/16/24: '+[4,8,12,16,24].map(n=>n+':'+ate(primeiro,n)).join('  '));
console.log('  depois do primeiro aviso, fica apontado em '+Math.round(100*flagPersist.reduce((a,b)=>a+b,0)/flagPersist.length)+'% dos rachas seguintes');
console.log('  por racha: errado apontado na direção certa em '+Math.round(100*fW/nW)+'% dos rachas ('+Math.round(100*fWe/nWe)+'% enquanto ainda está 2+ divisões fora); pessoa certa apontada numa direção qualquer em '+Math.round(100*fC/nC)+'%');
console.log('  "apontado em k dos últimos 8 rachas, na mesma direção" — sensibilidade (errado) × falso positivo (certo):');
for(let t=2;t<=6;t++)console.log('    k≥'+t+': errado '+Math.round(100*sensW[t]/nWin)+'% · certo '+Math.round(100*fpC[t]/nCin)+'%');
console.log('  ALTERNATIVA — deriva do Elo desde a entrada (|elo−base| ≥ limite): sensibilidade (errado, direção certa) × falso positivo (certo):');
[[8,'r8'],[16,'r16'],[24,'r24']].forEach(([rr,k])=>console.log('    racha '+rr+': '+LIM.map(lim=>{const D=drift[k+'|'+lim];return lim+'pts → errado '+Math.round(100*D.w/D.nw)+'% · certo '+Math.round(100*D.c/D.nc)+'%'}).join(' | ')));
console.log('  falsos positivos: gente certa (±1 div) apontada por racha, média = '+(nJust/LIGAS/RACHAS).toFixed(2)+' pessoas (de '+(CEN==='poucos'?18:15)+')');
"""
f = os.path.join(ROOT, 'scripts', '.tmp', 'aviso.js')
io.open(f, 'w', encoding='utf-8').write(core + '\n' + sim)
r = subprocess.run(['node', f] + sys.argv[1:], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=1800)
print(r.stdout)
if r.returncode: print(r.stderr[-2000:]); sys.exit(1)
