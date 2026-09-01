# -*- coding: utf-8 -*-
"""
Simulação de convergência das patentes com o MOTOR REAL (D-82).

Importa computeElo/updateRank/buildTeams do index.html e roda ligas inteiras
com habilidade verdadeira escondida, para medir quão perto o nível mostrado
chega do nível real — por regra de atualização e por cenário de palpite.

Uso:  python scripts/converge.py [bom|misto|nada] [rachas] [ligas] [cansaço]
  cansaço = pts que o time perde por partida seguida em quadra (até 3); 0 = sem; 50 = forte
  bom   = todo mundo entra com palpite bom (±1 divisão)
  misto = palpites bons, mas 25% errados em uma patente inteira (e são justamente os esporádicos)
  nada  = ninguém com palpite (todos 1500)

Modelo do racha: grupo de 20 com habilidade ~N(1500, 200); presença variável
(13–18 por noite, quatro que vêm a cada 3 semanas); times montados pelo app
pelo Elo ATUAL; vencedor fica (empate com 4 times: os dois saem); remontagem
no meio da noite em 25% dos rachas; 12 partidas curtas; resultado sorteado
pela habilidade VERDADEIRA com gols Poisson (2 gols ou 7 min). Sem goleiro.

Célula: todos %±1div · erro médio (pts) · esporádicos %±1div · desequilíbrio
REAL entre os times montados (pts de média; entre parênteses, o que o app
montaria sabendo a verdade). "TETO" é um reajuste em lote com todo o histórico
(máxima verossimilhança com prior no palpite): o melhor que dá para extrair dos
mesmos resultados. É a régua para mudar K, margem ou calibração.
"""
import io, os, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'scripts', '.tmp')
os.path.isdir(OUT) or os.makedirs(OUT)
html = io.open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
js = html.split('<script>')[1].split('</script>')[0]
core = js.split('/* @@FIM-DO-MOTOR@@')[0].replace('const save=()=>{saveUI();markDirty(S.active)}', 'const save=()=>{}')
assert 'function kFor(liga,km,tr){' in core, 'kFor mudou de assinatura em index.html; ajuste converge.py'
core = core.replace('function kFor(liga,km,tr){', 'let kFor=function(liga,km,tr){')

sim = r"""
const CEN=process.argv[2]||'misto',RACHAS=parseInt(process.argv[3]||'40'),LIGAS=parseInt(process.argv[4]||'80');
const POOL=20,PART=12,FAD=parseInt(process.argv[5]||'0');
const kForMotor=kFor;
let _i=0;const nid=()=>'p'+(++_i);
function gauss(){let u=0,v=0;while(!u)u=Math.random();while(!v)v=Math.random();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v)}
function poisson(l){let L=Math.exp(-l),k=0,p=1;do{k++;p*=Math.random()}while(p>L);return k-1}
function resultado(ta,tb){const r=Math.pow(10,(ta-tb)/400),la=0.5*r/(1+r),lb=0.5/(1+r);let ga=0,gb=0;
  for(let m=0;m<7&&ga<2&&gb<2;m++){ga+=poisson(la);gb+=poisson(lb)}return ga===gb?'draw':(ga>gb?0:1)}
const REGRAS={
  'motor (como está no index.html)':{k:kForMotor},
  'K fixo 32 (64 nas 15 primeiras) — D-55, antigo':{k:(liga,km,tr)=>(tr.games||0)<15?64:32},
  'K fixo 16 (32 nas 15 primeiras)':{k:(liga,km,tr)=>(tr.games||0)<15?32:16},
  'TETO: reajuste em lote com todo o histórico':{k:()=>0,batch:true},
};
function mk(name,elo,def){return{id:nid(),name,gk:false,L:newTrack(elo,def),G:newTrack(1500),goals:0,sessions:0,lastSession:null,owner:null,role:'lancador'};}
function refit(liga,hist,prior,sig){
  const r={};liga.players.forEach(p=>r[p.id]=p.L.elo);const c=Math.LN10/400;
  for(let it=0;it<40;it++){
    const g={};liga.players.forEach(p=>g[p.id]=-(r[p.id]-prior[p.id])/(sig[p.id]*sig[p.id]));
    for(const m of hist){
      const ra=m.a.reduce((s,id)=>s+r[id],0)/m.a.length,rb=m.b.reduce((s,id)=>s+r[id],0)/m.b.length;
      const E=1/(1+Math.pow(10,(rb-ra)/400)),d=(m.S-E)*c;
      m.a.forEach(id=>g[id]+=d/m.a.length);m.b.forEach(id=>g[id]-=d/m.b.length);
    }
    liga.players.forEach(p=>r[p.id]+=6000*g[p.id]);
  }
  liga.players.forEach(p=>{p.L.elo=r[p.id];updateRank(liga,p,p.L)});
}
function runLiga(R){
  kFor=R.k;
  const liga={id:'x',name:'t',cfg:defCfg(),players:[],matches:[],sessions:[],live:null};
  if(R.batch)liga.cfg.rankMargin=0;
  const truth={},freq={},prior={},sig={};
  for(let i=0;i<POOL;i++){
    const t=clamp(Math.round(1500+gauss()*200),1000,1999);
    let elo,def=true;
    if(CEN==='nada'){elo=1500;def=false}
    else{const ruim=CEN==='misto'&&i<5;const e=ruim?(Math.random()<.5?-3:3):(Math.random()<.5?0:(Math.random()<.5?-1:1));elo=stepMid(clamp(stepOf(t)+e,0,TOP))}
    const p=mk('j'+i,elo,def);truth[p.id]=t;prior[p.id]=elo;sig[p.id]=def?100:300;
    freq[p.id]=i<4?0.33:0.6+0.35*Math.random();
    liga.players.push(p);
  }
  S.ligas=[liga];S.active=liga.id;
  const hist=[],out=[];
  const gap=T=>{let s=0,n=0;for(let i=0;i<T.length;i++)for(let j=i+1;j<T.length;j++){const a=T[i].reduce((x,id)=>x+truth[id],0)/T[i].length,b=T[j].reduce((x,id)=>x+truth[id],0)/T[j].length;s+=Math.abs(a-b);n++}return s/n};
  for(let r=0;r<RACHAS;r++){
    let ids=liga.players.filter(p=>Math.random()<freq[p.id]).map(p=>p.id);
    while(ids.length<13){const p=liga.players[Math.floor(Math.random()*POOL)];if(ids.indexOf(p.id)<0)ids.push(p.id)}
    ids=ids.slice(0,18);
    const montar=()=>{const n=ids.length>=16?4:3;const t=buildTeams(liga,ids,n,null,[],false);return (t.teams||t).map(x=>(x.ids||x).map(y=>y.id||y)).filter(x=>x.length)};
    let T=montar();
    const bk=liga.players.map(p=>p.L.elo);liga.players.forEach(p=>p.L.elo=truth[p.id]);const To=montar();liga.players.forEach((p,i)=>p.L.elo=bk[i]);
    const gReal=gap(T),gOra=gap(To);
    const remonta=Math.random()<.25;let fila=T.map((_,i)=>i);const seguidas=T.map(()=>0);
    for(let k=0;k<PART;k++){
      if(remonta&&k===Math.floor(PART/2)){T=montar();fila=T.map((_,i)=>i)}
      const a=fila[0],b=fila[1];
      const part={};T[a].forEach(id=>part[id]={side:0,w:1,role:'L'});T[b].forEach(id=>part[id]={side:1,w:1,role:'L'});
      const avg=t=>t.reduce((s,id)=>s+truth[id],0)/t.length;
      /* cansaço: cada partida seguida em quadra tira FAD pts do time (até 3); quem sai descansa */
      const res=resultado(avg(T[a])-FAD*Math.min(3,seguidas[a]),avg(T[b])-FAD*Math.min(3,seguidas[b]));
      seguidas[a]++;seguidas[b]++;
      hist.push({a:T[a].slice(),b:T[b].slice(),S:res==='draw'?.5:res===0?1:0});
      if(!R.batch){const c=computeElo(liga,part,res,'curtas',1);
        for(const id in part){const p=P(liga,id),tr=p.L;tr.elo+=c.deltas[id]||0;updateRank(liga,p,tr);tr.games++;}}
      else for(const id in part)P(liga,id).L.games++;
      fila.shift();fila.shift();
      if(res===0){fila.push(b);fila.unshift(a)}else if(res===1){fila.push(a);fila.unshift(b)}
      else if(T.length>=4){fila.push(a);fila.push(b)}else{fila.push(a);fila.unshift(b)}
      if(res===0)seguidas[b]=0;else if(res===1)seguidas[a]=0;else{seguidas[a]=0;if(T.length>=4)seguidas[b]=0}
    }
    if(R.batch)refit(liga,hist,prior,sig);
    const el=liga.players.map(p=>p.L.elo),tv=liga.players.map(p=>truth[p.id]);
    const meanE=el.reduce((a,b)=>a+b,0)/POOL,meanT=tv.reduce((a,b)=>a+b,0)/POOL;
    let ok=0,err=0,okE=0,nE=0;
    liga.players.forEach(p=>{const st=stepOf(truth[p.id]-meanT+meanE);const d=Math.abs(p.L.rank-st),e=Math.abs(p.L.elo-meanE-(truth[p.id]-meanT));
      if(d<=1)ok++;err+=e;if(freq[p.id]<0.4){nE++;if(d<=1)okE++}});
    out.push({ok:ok/POOL,err:err/POOL,okE:okE/nE,gReal,gOra});
  }
  return out;
}
console.log('cenário: '+CEN+' · '+LIGAS+' ligas · 20 no grupo (4 vêm a cada 3 semanas), 13–18 por racha, vencedor fica, remontagem em 25% · cansaço -'+FAD+'/partida seguida');
console.log('célula = todos %±1div · erro pts · esporádicos %±1div · desequilíbrio REAL entre times (pts; entre parênteses, com a verdade)');
console.log('regra'.padEnd(50)+'| racha 3 | racha 5 | racha 10 | racha 20 | racha 40');
for(const nome in REGRAS){
  const acc=Array.from({length:RACHAS},()=>({ok:0,err:0,okE:0,gReal:0,gOra:0}));
  for(let l=0;l<LIGAS;l++){const o=runLiga(REGRAS[nome]);o.forEach((x,i)=>{for(const k in x)acc[i][k]+=x[k]})}
  const cel=i=>{const a=acc[i];return Math.round(100*a.ok/LIGAS)+'%·'+Math.round(a.err/LIGAS)+'·'+Math.round(100*a.okE/LIGAS)+'%·'+Math.round(a.gReal/LIGAS)+'('+Math.round(a.gOra/LIGAS)+')'};
  console.log(nome.padEnd(50)+'| '+[2,4,9,19,39].filter(i=>i<RACHAS).map(cel).join(' | '));
}
"""
f = os.path.join(OUT, 'converge.js')
io.open(f, 'w', encoding='utf-8').write(core + '\n' + sim)
r = subprocess.run(['node', f] + sys.argv[1:], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=1800)
print(r.stdout)
if r.returncode: print(r.stderr[-2000:]); sys.exit(1)
