# -*- coding: utf-8 -*-
"""
Convergência da patente de GOLEIRO partindo do desconhecido, com o motor real.
Liga inteira com palpite EXATO (def=true no degrau verdadeiro); o sujeito entra
sem nível (1500, def=false). Goleiro joga TODAS as partidas da noite (rodízio),
ora num gol, ora no outro — máxima mistura de companheiros e adversários.
Comparação: mesmo sujeito como jogador de LINHA sem palpite (entra nos times,
joga só quando o time dele está em quadra).
Uso: python converge_gk.py [ligas]
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
const LIGAS=parseInt(process.argv[2]||'300'),RACHAS=40,PART=12,NLIN=16;
let _i=0;const nid=()=>'p'+(++_i);
function gauss(){let u=0,v=0;while(!u)u=Math.random();while(!v)v=Math.random();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v)}
function poisson(l){let L=Math.exp(-l),k=0,p=1;do{k++;p*=Math.random()}while(p>L);return k-1}
function resultado(ta,tb){const r=Math.pow(10,(ta-tb)/400),la=0.5*r/(1+r),lb=0.5/(1+r);let ga=0,gb=0;
  for(let m=0;m<7&&ga<2&&gb<2;m++){ga+=poisson(la);gb+=poisson(lb)}return ga===gb?'draw':(ga>gb?0:1)}
function mk(name,eloL,defL,eloG,defG){return{id:nid(),name,gk:false,L:newTrack(eloL,defL),G:newTrack(eloG,defG),goals:0,sessions:0,lastSession:null,owner:null,role:'lancador'};}

/* cenários: o sujeito é goleiro (joga tudo, alterna o gol) ou linha (entra num time) */
const CEN=[
  {nome:'goleiro sem palpite, vem sempre (rodízio, joga as 12)',tipo:'G',freq:1},
  {nome:'goleiro sem palpite, vem 1 racha em 3',tipo:'G',freq:1/3},
  {nome:'linha sem palpite, vem sempre (comparação)',tipo:'L',freq:1},
];
function runLiga(cen){
  const liga={id:'x',name:'t',cfg:defCfg(),players:[],matches:[],sessions:[],live:null};
  const truth={};
  /* 16 de linha com palpite exato */
  for(let i=0;i<NLIN;i++){
    const t=clamp(Math.round(1500+gauss()*200),1000,1999);
    const p=mk('j'+i,stepMid(stepOf(t)),true,1500,false);
    truth[p.id]=t;liga.players.push(p);
  }
  /* dois goleiros de apoio com palpite exato no gol */
  const gks=[];
  for(let i=0;i<2;i++){
    const t=clamp(Math.round(1500+gauss()*200),1000,1999);
    const g=mk('gkDef'+i,1500,false,stepMid(stepOf(t)),true);
    truth[g.id]=t;gks.push(g);liga.players.push(g);
  }
  /* o sujeito: sem nível na valência que interessa */
  let subj,truthS=clamp(Math.round(1500+gauss()*200),1000,1999);
  if(cen.tipo==='G'){subj=mk('alvo',1500,false,1500,false);gks.unshift(subj)}
  else{subj=mk('alvo',1500,false,1500,false)}
  truth[subj.id]=truthS;liga.players.push(subj);
  S.ligas=[liga];S.active=liga.id;
  const lin=liga.players.filter(p=>p!==subj&&gks.indexOf(p)<0);
  const serie=[];
  for(let r=0;r<RACHAS;r++){
    const vem=Math.random()<cen.freq;
    /* presentes: 12–15 de linha (+ sujeito se for linha e vier) */
    let ids=lin.filter(()=>Math.random()<0.8).map(p=>p.id);
    while(ids.length<12)  {const p=lin[Math.floor(Math.random()*lin.length)];if(ids.indexOf(p.id)<0)ids.push(p.id)}
    ids=ids.slice(0,15);
    if(cen.tipo==='L'&&vem)ids.push(subj.id);
    const gPres=cen.tipo==='G'?(vem?[subj,gks[1]]:[gks[1],gks[2]]):[gks[0],gks[1]];
    const montar=()=>{const n=ids.length>=16?4:3;const t=buildTeams(liga,ids,n,null,[],false);return (t.teams||t).map(x=>(x.ids||x).map(y=>y.id||y)).filter(x=>x.length)};
    let T=montar(),fila=T.map((_,i)=>i);
    for(let k=0;k<PART;k++){
      const a=fila[0],b=fila[1];
      const part={};T[a].forEach(id=>part[id]={side:0,w:1,role:'L'});T[b].forEach(id=>part[id]={side:1,w:1,role:'L'});
      /* um goleiro em cada gol; alternam de lado a cada partida (rodízio) */
      const g0=gPres[k%2],g1=gPres[(k+1)%2];
      part[g0.id]={side:0,w:1,role:'G'};part[g1.id]={side:1,w:1,role:'G'};
      const tru=(tid,g)=>{const s=T[tid].reduce((x,id)=>x+truth[id],0)+truth[g.id];return s/(T[tid].length+1)};
      const res=resultado(tru(a,g0),tru(b,g1));
      const c=computeElo(liga,part,res,'curtas',1);
      for(const id in part){const p=P(liga,id),tr=rt(p,part[id].role);tr.elo+=c.deltas[id]||0;updateRank(liga,p,tr);tr.games++}
      fila.shift();fila.shift();
      if(res===0){fila.push(b);fila.unshift(a)}else if(res===1){fila.push(a);fila.unshift(b)}
      else if(T.length>=4){fila.push(a);fila.push(b)}else{fila.push(a);fila.unshift(b)}
    }
    /* referencial: média da liga de linha (deriva do soma-zero) */
    const meanE=lin.reduce((s,p)=>s+p.L.elo,0)/lin.length,meanT=lin.reduce((s,p)=>s+truth[p.id],0)/lin.length;
    const tr=cen.tipo==='G'?subj.G:subj.L;
    const ref=stepOf(truthS-meanT+meanE);
    serie.push({d:Math.abs(tr.rank-ref),err:Math.abs((tr.elo-meanE)-(truthS-meanT)),games:tr.games,longe:Math.abs(stepOf(truthS)-stepOf(1500))>=3});
  }
  return serie;
}
const CHK=[3,7,12,25,39],MES=['1 mês','2 meses','3 meses','6 meses','9 meses'];
console.log(LIGAS+' ligas por cenário · 16 de linha + 2 goleiros, todos com palpite EXATO · sujeito entra sem nível (1500) · 12 partidas/racha · racha semanal');
console.log('célula = %±1 divisão · erro médio (pts) · partidas do sujeito  —  [entre colchetes: só sujeitos ≥1 patente longe de Prata]');
console.log(''.padEnd(52)+'| '+MES.map(m=>m.padEnd(16)).join('| '));
for(const cen of CEN){
  const acc=CHK.map(()=>({ok:0,err:0,g:0,n:0,okL:0,nL:0}));
  for(let l=0;l<LIGAS;l++){
    const s=runLiga(cen);
    CHK.forEach((c,i)=>{const x=s[c];acc[i].n++;acc[i].err+=x.err;acc[i].g+=x.games;
      if(x.d<=1)acc[i].ok++;
      if(x.longe){acc[i].nL++;if(x.d<=1)acc[i].okL++}});
  }
  const cel=i=>{const a=acc[i];return (Math.round(100*a.ok/a.n)+'%·'+Math.round(a.err/a.n)+'·'+Math.round(a.g/a.n)+'j'+(a.nL?' ['+Math.round(100*a.okL/a.nL)+'%]':'')).padEnd(16)};
  console.log(cen.nome.padEnd(52)+'| '+CHK.map((_,i)=>cel(i)).join('| '));
}
"""
f = os.path.join(OUT, 'converge_gk.js')
io.open(f, 'w', encoding='utf-8').write(core + '\n' + sim)
r = subprocess.run(['node', f] + sys.argv[1:], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=1200)
print(r.stdout)
if r.returncode: print(r.stderr[-3000:]); sys.exit(1)
