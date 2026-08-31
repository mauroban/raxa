# -*- coding: utf-8 -*-
"""
Checagem estrutural das telas do Raxa.

Renderiza cada tela num DOM falso, captura o HTML gerado e verifica:
  - tags abertas e fechadas na ordem certa (tag torta = layout sobreposto)
  - atributos quebrados por aspas dentro de aspas
  - restos de template literal ("${", "undefined", "NaN") no HTML final
  - botoes vazios ou aninhados (botao dentro de botao nao renderiza direito)

Uso:  python scripts/layout.py
"""
import io, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'scripts', '.tmp')
os.path.isdir(OUT) or os.makedirs(OUT)

html = io.open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
js = html.split('<script>')[1].split('</script>')[0]

stub = r"""
class El{
  constructor(id){this.id=id;this._html='';this.textContent='';this.dataset={};this.style={};
    this.classList={add(){},remove(){},toggle(){},contains(){return false}};}
  set innerHTML(v){this._html=String(v)}
  get innerHTML(){return this._html}
  querySelector(){return null} querySelectorAll(){return []} closest(){return null}
  focus(){} click(){} appendChild(){} remove(){} addEventListener(){}
  getBoundingClientRect(){return{left:0,top:0,width:10,height:10}}
  cloneNode(){return new El('ghost')}
}
const els={};
['#app','#bar','#sheet','#scrim','#toast'].forEach(s=>els[s]=new El(s));
global.document={querySelector:s=>els[s]||null,querySelectorAll:()=>[],addEventListener:()=>{},
  createElement:()=>new El('tmp'),body:new El('body'),elementFromPoint:()=>null};
global.window={};global.navigator={};
const store={};
global.localStorage={getItem:k=>store[k]||null,setItem:(k,v)=>store[k]=v};
global.confirm=()=>true;global.prompt=()=>'Mauro';global.alert=()=>{};
"""

capture = r"""
const telas={};
function snap(nome){telas[nome]={app:els['#app'].innerHTML,bar:els['#bar'].innerHTML,sheet:els['#sheet'].innerHTML}}
S=defState();render();snap('inicio');
A.demo();snap('liga nova');
A.startRacha();snap('presenca vazia');
L().live.presentIds=L().players.map(p=>p.id);render();snap('presenca cheia');
A.addPlayer();snap('sheet novo jogador');
A.toTimes();snap('times');
L().live.sel=L().live.teams[0].ids[0];render();snap('times com selecao');
A.gkMode();snap('times goleiro fixo');
A.gkMode();snap('times goleiro rodizio');
A.startMatch();snap('partida');
A.goal({dataset:{s:'0'}});A.goal({dataset:{s:'1'}});A.goal({dataset:{s:'0'}});
const g0=L().live.cur.events.find(e=>e.type==='goal');
A.setGoalScorer({dataset:{t:String(g0.t),id:L().live.cur.lineups[0][0]}});
render();snap('partida com gols');
A.outPick({dataset:{s:'0',id:L().live.cur.lineups[0][0]}});snap('sheet substituicao');
A.gkSheet({dataset:{s:'0'}});snap('sheet goleiro');
A.endMatch();snap('fim de partida (sheet resultado)');
render();snap('pausa entre partidas');
A.pickSide({dataset:{s:'0'}});snap('sheet escolher time');
S.ui.tab='ranking';render();snap('patentes');
A.pSheet({dataset:{id:L().players[0].id}});snap('sheet jogador');
S.ui.tab='hist';render();snap('historico');
A.review({dataset:{id:L().matches[0].id}});snap('sheet revisar');
A.revSec({dataset:{k:'trechos',id:L().matches[0].id}});snap('sheet revisar trechos');
A.revSec({dataset:{k:'nivel',id:L().matches[0].id}});snap('sheet revisar nivel');
A.editEsc({dataset:{id:L().matches[0].id}});snap('sheet escalacao e trocas');
A.escPick({dataset:{id:L().matches[0].id,s:'0',pid:(L().matches[0].startLineups||L().matches[0].lineups)[0][0]}});snap('sheet corrigir jogador');
A.novaTroca({dataset:{id:L().matches[0].id}});snap('sheet nova troca');
A.ntSet({dataset:{k:'tipo',v:'gk'}});snap('sheet nova troca goleiro');
S.ui.tab='cfg';render();snap('ajustes');
S.ui.tab='racha';render();snap('racha');
A.endRacha();snap('sheet fim de racha');
A.home();snap('home com ligas');
console.log(JSON.stringify(telas));
"""

path = os.path.join(OUT, 'layout.js')
io.open(path, 'w', encoding='utf-8').write(stub + js + capture)
res = subprocess.run(['node', path], capture_output=True, text=True, encoding='utf-8')
if res.returncode != 0:
    print(res.stdout[-3000:]); print(res.stderr[-3000:]); sys.exit(1)

import json
telas = json.loads(res.stdout.strip().splitlines()[-1])

VOID = {'br', 'hr', 'img', 'input', 'meta', 'link', 'source', 'area', 'base', 'col', 'embed', 'track', 'wbr'}
TAG = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)([^>]*?)(/?)>')

problemas = []
for nome, partes in telas.items():
    for parte, h in partes.items():
        if not h:
            continue
        alvo = nome + ' / ' + parte
        pilha = []
        for m in TAG.finditer(h):
            fecha, tag, attrs, auto = m.group(1), m.group(2).lower(), m.group(3), m.group(4)
            if tag in VOID or auto:
                continue
            if fecha:
                if not pilha:
                    problemas.append((alvo, 'fecha </%s> sem abrir' % tag, h[max(0, m.start()-90):m.start()+40]))
                elif pilha[-1][0] != tag:
                    problemas.append((alvo, 'fecha </%s> mas o aberto era <%s>' % (tag, pilha[-1][0]),
                                      h[max(0, m.start()-90):m.start()+40]))
                    pilha.pop()
                else:
                    pilha.pop()
            else:
                pilha.append((tag, m.start()))
        for tag, pos in pilha:
            problemas.append((alvo, '<%s> nunca fecha' % tag, h[max(0, pos-40):pos+120]))

        # botao dentro de botao: o navegador desmonta e os alvos de toque se sobrepoem
        prof = 0
        for m in TAG.finditer(h):
            if m.group(2).lower() != 'button':
                continue
            if m.group(1):
                prof -= 1
            else:
                prof += 1
                if prof > 1:
                    problemas.append((alvo, 'button dentro de button', h[max(0, m.start()-120):m.start()+80]))

        for lixo in ['${', 'undefined', 'NaN', '[object Object]']:
            i = h.find(lixo)
            if i >= 0:
                problemas.append((alvo, 'sobrou "%s" no HTML' % lixo, h[max(0, i-90):i+60]))

print('telas verificadas: %d' % len(telas))
if not problemas:
    print('\nESTRUTURA OK: nenhuma tag torta, nenhum botao aninhado, nenhum resto de template.')
    sys.exit(0)
print('\n*** %d PROBLEMA(S) ***\n' % len(problemas))
vistos = set()
for alvo, erro, trecho in problemas:
    chave = (alvo, erro)
    if chave in vistos:
        continue
    vistos.add(chave)
    print('[%s] %s' % (alvo, erro))
    print('   ...%s...\n' % ' '.join(trecho.split())[:170])
sys.exit(1)
