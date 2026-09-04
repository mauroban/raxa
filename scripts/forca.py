# -*- coding: utf-8 -*-
"""
Time montado NA MAO (sem o app): que diferenca de nivel MEDIO mostrado garante que um
time e mais forte de verdade? Reusa a liga simulada do converge.py (motor real, mesmo
modelo de racha) e, no fim, sorteia milhares de divisoes 5v5 entre os 20, comparando a
diferenca das medias MOSTRADAS (Elo de hoje) com a das medias VERDADEIRAS.

Uso:  python scripts/forca.py [bom|misto|nada] [rachas] [ligas]
Celula: % em que o lado mostrado e o mais forte de verdade; % em que e >= meia divisao
melhor; % >= 1 divisao melhor; chance real de vitoria do lado mostrado. 1 div = 67 pts.
"""
import io, os, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = io.open(os.path.join(ROOT, 'scripts', 'converge.py'), encoding='utf-8').read()
html = io.open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
js = html.split('<script>')[1].split('</script>')[0]
core = js.split('/* @@FIM-DO-MOTOR@@')[0].replace('const save=()=>{saveUI();markDirty(S.active)}', 'const save=()=>{}')
core = core.replace('function kFor(liga,km,tr){', 'let kFor=function(liga,km,tr){')
sim = src.split('sim = r"""')[1].split('"""')[0]
sim = sim.split("console.log('cenário: '")[0]           # fica só com as funcoes (runLiga inclusive)
sim = sim.replace("  return out;\n}", "  return {out,liga,truth,freq};\n}")
driver = r"""
const DIV=67;
const faixas=[[0,0.5],[0.5,1],[1,1.5],[1.5,2],[2,3],[3,99]];   // em divisoes de diferenca MOSTRADA
const acc=faixas.map(()=>({n:0,certo:0,meiaDiv:0,umaDiv:0,pv:0}));
const expWin=d=>1/(1+Math.pow(10,-d/400));
for(let L=0;L<LIGAS;L++){
  const {liga,truth}=runLiga(REGRAS['motor (como está no index.html)']);
  const ps=liga.players;
  for(let k=0;k<3000;k++){
    const ids=ps.map(p=>p.id).sort(()=>Math.random()-.5).slice(0,10);
    const A=ids.slice(0,5),B=ids.slice(5);
    const m=(arr,f)=>arr.reduce((s,id)=>s+f(id),0)/arr.length;
    const disp=m(A,id=>P(liga,id).L.elo)-m(B,id=>P(liga,id).L.elo);
    const real=m(A,id=>truth[id])-m(B,id=>truth[id]);
    const d=Math.abs(disp)/DIV,sg=Math.sign(disp)||1;
    const i=faixas.findIndex(f=>d>=f[0]&&d<f[1]);if(i<0)continue;
    const a=acc[i];a.n++;
    if(sg*real>0)a.certo++;
    if(sg*real>=DIV/2)a.meiaDiv++;
    if(sg*real>=DIV)a.umaDiv++;
    a.pv+=expWin(sg*real);
  }
}
console.log('cenário '+CEN+' · '+RACHAS+' rachas · '+LIGAS+' ligas · 5v5 sorteado entre os 20');
console.log('diferença MOSTRADA entre as médias | o lado mostrado é o mais forte de verdade | é ≥ meia divisão melhor | é ≥ 1 divisão melhor | chance real de vitória');
faixas.forEach((f,i)=>{const a=acc[i];if(!a.n)return;
  const lab=(f[1]>10?'≥ '+f[0]:f[0]+' a '+f[1])+' div';
  console.log(lab.padEnd(34)+'| '+(100*a.certo/a.n).toFixed(0).padStart(3)+'% | '+(100*a.meiaDiv/a.n).toFixed(0).padStart(3)+'% | '+(100*a.umaDiv/a.n).toFixed(0).padStart(3)+'% | '+(100*a.pv/a.n).toFixed(0)+'%  (n='+a.n+')')});
"""
OUT = os.path.join(ROOT, 'scripts', '.tmp'); os.path.isdir(OUT) or os.makedirs(OUT)
f = os.path.join(OUT, 'forca.js')
io.open(f, 'w', encoding='utf-8').write(core + '\n' + sim + driver)
r = subprocess.run(['node', f] + sys.argv[1:], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=1800)
print(r.stdout)
if r.returncode: print(r.stderr[-2000:]); sys.exit(1)
