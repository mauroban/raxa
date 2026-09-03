# -*- coding: utf-8 -*-
"""
Calibra o SINAL DE CONFIANÇA na patente (D-113) com o motor real.

Mesma simulação do converge.py (D-82): grupo de 20 com habilidade verdadeira
escondida, presença variável, times montados pelo app, vencedor fica, 12
partidas curtas por racha. No fim de cada racha, para cada pessoa que já saiu
da calibração, olhamos os sinais candidatos e se a patente mostrada bate com a
verdadeira. Saída, por sinal: em quantos casos ele acende (cobertura) e, quando
acende, a chance de a patente estar certa (precisão) e de estar a ±1 divisão.

Sinais candidatos:
  - só volume: partidas jogadas ≥ 15 / 30 / 45 (K no piso) / 90
  - circulação: das últimas N partidas, quantas terminaram na patente atual
  - distância do Elo à borda da patente
  - combinações

E uma segunda tabela, por PARES: quando a diferença mostrada entre duas pessoas
é de d divisões, o de cima é de fato mais forte? A diferença real também é de
uma patente inteira? (É a régua de "3 divisões separam de verdade?")

Resultado registrado na D-113: nenhum sinal separa quem está na patente certa
(a ±2 divisões todo mundo calibrado já está — 97% com palpites bons); 3
divisões mostradas dizem "mais forte" em 91–96% dos pares.

Uso:  python scripts/confianca.py [misto|bom|nada] [rachas] [ligas]
"""
import io, os, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'scripts', '.tmp')
os.path.isdir(OUT) or os.makedirs(OUT)
html = io.open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
js = html.split('<script>')[1].split('</script>')[0]
core = js.split('/* @@FIM-DO-MOTOR@@')[0].replace('const save=()=>{saveUI();markDirty(S.active)}', 'const save=()=>{}')

sim = r"""
const CEN=process.argv[2]||'misto',RACHAS=parseInt(process.argv[3]||'60'),LIGAS=parseInt(process.argv[4]||'60');
const POOL=20,PART=12;
let _i=0;const nid=()=>'p'+(++_i);
function gauss(){let u=0,v=0;while(!u)u=Math.random();while(!v)v=Math.random();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v)}
function poisson(l){let L=Math.exp(-l),k=0,p=1;do{k++;p*=Math.random()}while(p>L);return k-1}
function resultado(ta,tb){const r=Math.pow(10,(ta-tb)/400),la=0.5*r/(1+r),lb=0.5/(1+r);let ga=0,gb=0;
  for(let m=0;m<7&&ga<2&&gb<2;m++){ga+=poisson(la);gb+=poisson(lb)}return ga===gb?'draw':(ga>gb?0:1)}
function mk(name,elo,def){return{id:nid(),name,gk:false,L:newTrack(elo,def),G:newTrack(1500),goals:0,sessions:0,lastSession:null,owner:null,role:'lancador'};}
/* sinais candidatos: (nome, função(games, hist, rank) -> acende?) */
const circ=(h,rank,n)=>h.slice(-n).filter(r=>patOf(r)===patOf(rank)).length;
const SINais=[
  ['≥15 partidas (saiu da calibração)',(g,h,r)=>g>=15],
  ['≥30 partidas',(g,h,r)=>g>=30],
  ['≥45 partidas (K no piso)',(g,h,r)=>g>=45],
  ['≥90 partidas',(g,h,r)=>g>=90],
  ['≥150 partidas',(g,h,r)=>g>=150],
  ['circ: >14 das últimas 20',(g,h,r)=>circ(h,r,20)>14],
  ['circ: >17 das últimas 20',(g,h,r)=>circ(h,r,20)>17],
  ['circ: >20 das últimas 30',(g,h,r)=>circ(h,r,30)>20],
  ['circ: >24 das últimas 30',(g,h,r)=>circ(h,r,30)>24],
  ['circ: >27 das últimas 30',(g,h,r)=>circ(h,r,30)>27],
  ['circ: ≥40 das últimas 50',(g,h,r)=>circ(h,r,50)>=40],
  ['circ: ≥45 das últimas 50',(g,h,r)=>circ(h,r,50)>=45],
  ['circ: ≥48 das últimas 50',(g,h,r)=>circ(h,r,50)>=48],
  ['circ: ≥72 das últimas 80',(g,h,r)=>circ(h,r,80)>=72],
  ['K no piso E >24 das últimas 30',(g,h,r)=>g>=45&&circ(h,r,30)>24],
  ['K no piso E ≥45 das últimas 50',(g,h,r)=>g>=45&&circ(h,r,50)>=45],
  ['≥90 partidas E ≥45 das últimas 50',(g,h,r)=>g>=90&&circ(h,r,50)>=45],
  ['Elo ≥40 pts da borda da patente',(g,h,r,e)=>borda(r,e)>=40],
  ['Elo ≥60 pts da borda',(g,h,r,e)=>borda(r,e)>=60],
  ['Elo ≥80 pts da borda',(g,h,r,e)=>borda(r,e)>=80],
  ['K no piso E ≥40 da borda',(g,h,r,e)=>g>=45&&borda(r,e)>=40],
  ['K no piso E ≥60 da borda',(g,h,r,e)=>g>=45&&borda(r,e)>=60],
  ['K no piso E ≥60 da borda E >24/30',(g,h,r,e)=>g>=45&&borda(r,e)>=60&&circ(h,r,30)>24],
  ['≥90 partidas E ≥60 da borda',(g,h,r,e)=>g>=90&&borda(r,e)>=60],
];
/* distância do Elo à borda mais próxima da patente atual (patente = 3 degraus = 200 pts) */
const borda=(rank,elo)=>{const k=patOf(rank),lo=stepMin(k*3),hi=stepMin(k*3+3);return Math.min(elo-lo,hi-elo)};
const acc=SINais.map(()=>({n:0,pat:0,div:0,div2:0}));let base={n:0,pat:0,div:0,div2:0};
/* pares: diferença MOSTRADA de d divisões entre duas pessoas calibradas → o de cima é de fato
   mais forte? a diferença real também é de d ou mais? (D-113: "3 divisões separam de verdade?") */
const PARES={};const par=d=>PARES[d]||(PARES[d]={n:0,ordem:0,real3:0,real1:0,mediaReal:0});
function runLiga(){
  const liga={id:'x',name:'t',cfg:defCfg(),players:[],matches:[],sessions:[],live:null};
  const truth={},freq={},hist={};
  for(let i=0;i<POOL;i++){
    const t=clamp(Math.round(1500+gauss()*200),1000,1999);
    let elo,def=true;
    if(CEN==='nada'){elo=1500;def=false}
    else{const ruim=(CEN==='misto'&&i<5);const e=ruim?(Math.random()<.5?-3:3):(Math.random()<.5?0:(Math.random()<.5?-1:1));elo=stepMid(clamp(stepOf(t)+e,0,TOP));}
    const p=mk('j'+i,elo,def);truth[p.id]=t;hist[p.id]=[];
    freq[p.id]=i<4?0.33:0.6+0.35*Math.random();
    liga.players.push(p);
  }
  S.ligas=[liga];S.active=liga.id;
  for(let r=0;r<RACHAS;r++){
    let ids=liga.players.filter(p=>Math.random()<freq[p.id]).map(p=>p.id);
    while(ids.length<13){const p=liga.players[Math.floor(Math.random()*POOL)];if(ids.indexOf(p.id)<0)ids.push(p.id)}
    ids=ids.slice(0,18);
    const montar=()=>{const n=ids.length>=16?4:3;const t=buildTeams(liga,ids,n,null,[],false);return (t.teams||t).map(x=>(x.ids||x).map(y=>y.id||y)).filter(x=>x.length)};
    let T=montar();
    const remonta=Math.random()<.25;let fila=T.map((_,i)=>i);
    for(let k=0;k<PART;k++){
      if(remonta&&k===Math.floor(PART/2)){T=montar();fila=T.map((_,i)=>i)}
      const a=fila[0],b=fila[1];
      const part={};T[a].forEach(id=>part[id]={side:0,w:1,role:'L'});T[b].forEach(id=>part[id]={side:1,w:1,role:'L'});
      const avg=t=>t.reduce((s,id)=>s+truth[id],0)/t.length;
      const res=resultado(avg(T[a]),avg(T[b]));
      const c=computeElo(liga,part,res,'curtas',1);
      for(const id in part){const p=P(liga,id),tr=p.L;tr.elo+=c.deltas[id]||0;updateRank(liga,p,tr);tr.games++;
        hist[id].push(tr.rank);if(hist[id].length>80)hist[id].shift();}
      fila.shift();fila.shift();
      if(res===0){fila.push(b);fila.unshift(a)}else if(res===1){fila.push(a);fila.unshift(b)}
      else if(T.length>=4){fila.push(a);fila.push(b)}else{fila.push(a);fila.unshift(b)}
    }
    /* avaliação no fim do racha: a patente mostrada bate com a verdadeira? (verdade
       centrada na média da liga, como o converge — Elo é soma zero)            */
    const el=liga.players.map(p=>p.L.elo),tv=liga.players.map(p=>truth[p.id]);
    const meanE=el.reduce((a,b)=>a+b,0)/POOL,meanT=tv.reduce((a,b)=>a+b,0)/POOL;
    liga.players.forEach(p=>{const tr=p.L;if(calibrando(liga,p,tr))return;
      const st=stepOf(truth[p.id]-meanT+meanE),pat=patOf(tr.rank)===patOf(st),div=Math.abs(tr.rank-st)<=1,div2=Math.abs(tr.rank-st)<=2;
      base.n++;if(pat)base.pat++;if(div)base.div++;if(div2)base.div2++;
      SINais.forEach((s,i)=>{if(s[1](tr.games,hist[p.id],tr.rank,tr.elo)){acc[i].n++;if(pat)acc[i].pat++;if(div)acc[i].div++;if(div2)acc[i].div2++}});
    });
    const cal=liga.players.filter(p=>!calibrando(liga,p,p.L));
    for(let i=0;i<cal.length;i++)for(let j=0;j<cal.length;j++){if(i===j)continue;
      const a=cal[i],b=cal[j],d=a.L.rank-b.L.rank;if(d<1)continue;
      const real=(truth[a.id]-truth[b.id])/STEP,x=par(Math.min(d,5));
      x.n++;if(real>0)x.ordem++;if(real>=3)x.real3++;if(real>=1)x.real1++;x.mediaReal+=real;}
  }
}
for(let l=0;l<LIGAS;l++)runLiga();
const pc=(a,b)=>b?String(Math.round(100*a/b)).padStart(3)+'%':'  —';
console.log('cenário: '+CEN+' · '+LIGAS+' ligas × '+RACHAS+' rachas · avaliação no fim de cada racha, só quem já calibrou ('+base.n+' pessoa-rachas)');
console.log('sinal'.padEnd(40)+'| acende | patente certa | ±1 divisão | ±2 divisões');
console.log('todos que já calibraram (base)'.padEnd(40)+'|  100%  |     '+pc(base.pat,base.n)+'      |    '+pc(base.div,base.n)+'    |    '+pc(base.div2,base.n));
console.log('\npares com diferença MOSTRADA de d divisões (5 = 5 ou mais):');
console.log('d'.padEnd(4)+'| pares | o de cima é mais forte | real ≥1 div | real ≥3 div (uma patente) | diferença real média (div)');
Object.keys(PARES).sort().forEach(d=>{const x=PARES[d];console.log(String(d).padEnd(4)+'| '+String(x.n).padStart(6)+'|        '+pc(x.ordem,x.n)+'           |    '+pc(x.real1,x.n)+'    |         '+pc(x.real3,x.n)+'            |   '+(x.mediaReal/x.n).toFixed(1))});
SINais.forEach((s,i)=>{const a=acc[i];console.log(s[0].padEnd(40)+'| '+pc(a.n,base.n)+'   |     '+pc(a.pat,a.n)+'      |    '+pc(a.div,a.n)+'    |    '+pc(a.div2,a.n))});
"""
f = os.path.join(OUT, 'confianca.js')
io.open(f, 'w', encoding='utf-8').write(core + '\n' + sim)
r = subprocess.run(['node', f] + sys.argv[1:], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=1800)
print(r.stdout)
if r.returncode:
    print(r.stderr[-2000:])
    sys.exit(1)
