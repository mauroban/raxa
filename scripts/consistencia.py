# -*- coding: utf-8 -*-
"""
Diferença CONSISTENTE entre duas pessoas: o que ela diz sobre a força real? (D-115)

Complemento da tabela de pares da D-113 (scripts/confianca.py), que olha um retrato
só: "hoje A está d divisões acima de B". Aqui a pergunta é outra: depois de um
1º período de racha (3 meses = 13 rachas semanais), todo mundo continua jogando um
2º período (mais 3 meses). Se, em TODO fim de racha do 2º período, A ficou no mínimo
X divisões acima de B, qual a chance de A ser de fato mais forte? E de ser uma
patente inteira (3 divisões) melhor?

Mesma simulação do converge.py (D-82): grupo de 20 com habilidade verdadeira
escondida, presença variável, times montados pelo app, vencedor fica, 12 partidas
curtas por racha. Só entram pares em que os dois já saíram da calibração no fim do
1º período e os dois jogaram pelo menos um racha no 2º.

"No mínimo X" = a MENOR diferença mostrada ao longo do 2º período foi exatamente X
(5 = 5 ou mais). Tabela principal. Para comparar: o retrato do último racha com d = X
(a régua da D-113 nos mesmos dados) e a leitura acumulada (mínimo ≥ X).

Uso:  python scripts/consistencia.py [misto|bom|nada] [meses1] [meses2] [ligas]
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
const CEN=process.argv[2]||'misto',MESES1=parseFloat(process.argv[3]||'3'),MESES2=parseFloat(process.argv[4]||'3'),LIGAS=parseInt(process.argv[5]||'100');
const R1=Math.round(MESES1*52/12),R2=Math.round(MESES2*52/12); /* racha semanal */
const POOL=20,PART=12;
let _i=0;const nid=()=>'p'+(++_i);
function gauss(){let u=0,v=0;while(!u)u=Math.random();while(!v)v=Math.random();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v)}
function poisson(l){let L=Math.exp(-l),k=0,p=1;do{k++;p*=Math.random()}while(p>L);return k-1}
function resultado(ta,tb){const r=Math.pow(10,(ta-tb)/400),la=0.5*r/(1+r),lb=0.5/(1+r);let ga=0,gb=0;
  for(let m=0;m<7&&ga<2&&gb<2;m++){ga+=poisson(la);gb+=poisson(lb)}return ga===gb?'draw':(ga>gb?0:1)}
function mk(name,elo,def){return{id:nid(),name,gk:false,L:newTrack(elo,def),G:newTrack(1500),goals:0,sessions:0,lastSession:null,owner:null,role:'lancador'};}
const novo=()=>({n:0,ordem:0,real1:0,real3:0,mediaReal:0});
const CONS={},FIM={},FIMX={},EXATO={};const at=(o,d)=>o[d]||(o[d]=novo());
let paresTot=0,paresOk=0;
function runLiga(){
  const liga={id:'x',name:'t',cfg:defCfg(),players:[],matches:[],sessions:[],live:null};
  const truth={},freq={},jogou2={};
  for(let i=0;i<POOL;i++){
    const t=clamp(Math.round(1500+gauss()*200),1000,1999);
    let elo,def=true;
    if(CEN==='nada'){elo=1500;def=false}
    else{const ruim=(CEN==='misto'&&i<5);const e=ruim?(Math.random()<.5?-3:3):(Math.random()<.5?0:(Math.random()<.5?-1:1));elo=stepMid(clamp(stepOf(t)+e,0,TOP));}
    const p=mk('j'+i,elo,def);truth[p.id]=t;jogou2[p.id]=0;
    freq[p.id]=i<4?0.33:0.6+0.35*Math.random();
    liga.players.push(p);
  }
  S.ligas=[liga];S.active=liga.id;
  let cal=null;                         /* quem já calibrou no fim do 1º período */
  const minDiff={};                     /* por par "i,j": menor diferença mostrada no 2º período */
  for(let r=0;r<R1+R2;r++){
    let ids=liga.players.filter(p=>Math.random()<freq[p.id]).map(p=>p.id);
    while(ids.length<13){const p=liga.players[Math.floor(Math.random()*POOL)];if(ids.indexOf(p.id)<0)ids.push(p.id)}
    ids=ids.slice(0,18);
    if(r>=R1)ids.forEach(id=>jogou2[id]++);
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
      for(const id in part){const p=P(liga,id),tr=p.L;tr.elo+=c.deltas[id]||0;updateRank(liga,p,tr);tr.games++;}
      fila.shift();fila.shift();
      if(res===0){fila.push(b);fila.unshift(a)}else if(res===1){fila.push(a);fila.unshift(b)}
      else if(T.length>=4){fila.push(a);fila.push(b)}else{fila.push(a);fila.unshift(b)}
    }
    if(r===R1-1){cal=liga.players.filter(p=>!calibrando(liga,p,p.L));paresTot+=POOL*(POOL-1);}
    if(r>=R1){ /* fim de um racha do 2º período: registra a diferença mostrada de cada par ordenado */
      for(let i=0;i<cal.length;i++)for(let j=0;j<cal.length;j++){if(i===j)continue;
        const k=i+','+j,d=cal[i].L.rank-cal[j].L.rank;
        minDiff[k]=(k in minDiff)?Math.min(minDiff[k],d):d;}
    }
  }
  for(let i=0;i<cal.length;i++)for(let j=0;j<cal.length;j++){if(i===j)continue;
    const a=cal[i],b=cal[j];if(!jogou2[a.id]||!jogou2[b.id])continue;paresOk++;
    const k=i+','+j,real=(truth[a.id]-truth[b.id])/STEP;
    const conta=(o,d)=>{for(let x=1;x<=5;x++)if(d>=x){const q=at(o,x);q.n++;if(real>0)q.ordem++;if(real>=1)q.real1++;if(real>=3)q.real3++;q.mediaReal+=real}};
    conta(CONS,minDiff[k]);                 /* consistente: nunca ficou abaixo de X no 2º período */
    const exato=(o,d)=>{d=Math.min(d,5);if(d>=1){const q=at(o,d);q.n++;if(real>0)q.ordem++;if(real>=1)q.real1++;if(real>=3)q.real3++;q.mediaReal+=real}};
    exato(EXATO,minDiff[k]);                /* PRINCIPAL: a menor diferença do 2º período foi exatamente X */
    exato(FIMX,a.L.rank-b.L.rank);          /* retrato: d exato no fim do 2º período (régua da D-113) */
    conta(FIM,a.L.rank-b.L.rank);           /* retrato acumulado (≥ X no fim) */
  }
}
for(let l=0;l<LIGAS;l++)runLiga();
const pc=(a,b)=>b?String(Math.round(100*a/b)).padStart(3)+'%':'  —';
console.log('cenário: '+CEN+' · '+LIGAS+' ligas · 1º período '+MESES1+' meses ('+R1+' rachas) → 2º período '+MESES2+' meses ('+R2+' rachas) · racha semanal, 12 partidas');
console.log('pares ordenados avaliados: '+paresOk+' de '+paresTot+' ('+pc(paresOk,paresTot)+' — os dois calibrados no fim do 1º período e jogaram no 2º)\n');
const linha=(o,x)=>{const q=at(o,x);return String(q.n).padStart(6)+' |  '+pc(q.ordem,q.n)+'  |  '+pc(q.real1,q.n)+'  |    '+pc(q.real3,q.n)+'    |  '+(q.n?(q.mediaReal/q.n).toFixed(1):'—')};
const cab=' X  |  pares | A > B | ≥1 div | ≥1 patente (3 div) | dif. real média';
console.log('NO MÍNIMO X: a MENOR diferença mostrada entre A e B ao longo do 2º período foi exatamente X divisões');console.log(cab);
for(let x=1;x<=5;x++)console.log(' '+x+(x===5?'+':' ')+' | '+linha(EXATO,x));
console.log('\nRETRATO, para comparar: diferença exatamente X no último racha do 2º período (régua da D-113 nos mesmos dados)');console.log(cab);
for(let x=1;x<=5;x++)console.log(' '+x+(x===5?'+':' ')+' | '+linha(FIMX,x));
console.log('\nACUMULADO: menor diferença do período ≥ X (inclui pares muito mais separados)');console.log(cab);
for(let x=1;x<=5;x++)console.log(' '+x+(x===5?'+':' ')+' | '+linha(CONS,x));
console.log('\nACUMULADO, retrato: diferença no último racha ≥ X');console.log(cab);
for(let x=1;x<=5;x++)console.log(' '+x+(x===5?'+':' ')+' | '+linha(FIM,x));
"""
f = os.path.join(OUT, 'consistencia.js')
io.open(f, 'w', encoding='utf-8').write(core + '\n' + sim)
r = subprocess.run(['node', f] + sys.argv[1:], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=1800)
print(r.stdout)
if r.returncode:
    print(r.stderr[-2000:])
    sys.exit(1)
