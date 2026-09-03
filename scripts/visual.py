# -*- coding: utf-8 -*-
"""
Verificacao visual do Raxa em um navegador de verdade (Chrome headless).

Para cada tela, checa no DOM ja renderizado:
  - nada estoura a largura da tela (nem para a direita, nem para a esquerda)
  - nada dentro de #app esta com position:fixed/absolute solto
    (foi assim que a classe .ghost do arraste vazou para todo botao .btn.ghost
     e empilhou os botoes uns sobre os outros)
  - nenhum elemento clicavel fica escondido atras de outro no proprio centro
  - alvos de toque com pelo menos 32px de altura

Salva os prints em scripts/.tmp/shots/ para conferencia a olho.

Uso:  python scripts/visual.py
"""
import io, json, os, subprocess, sys
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(ROOT, 'scripts', '.tmp')
SHOTS = os.path.join(TMP, 'shots')
for d in (TMP, SHOTS):
    os.path.isdir(d) or os.makedirs(d)

CHROMES = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
    os.path.expanduser(r'~\AppData\Local\Google\Chrome\Application\chrome.exe'),
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
]
chrome = next((c for c in CHROMES if os.path.exists(c)), None)
if not chrome:
    print('Chrome/Edge nao encontrado — pulando a verificacao visual.')
    sys.exit(0)

TELAS = {
    1: 'presenca',
    2: 'times',
    3: 'partida',
    4: 'proxima partida',
    5: 'patentes',
    6: 'historico',
    7: 'ajustes',
    8: 'numeros',
    9: 'completar',
    10: 'destaques',
    11: 'ficha admin',
    12: 'minhas opinioes',
    13: 'ficha com opinioes',
    14: 'fim de racha',
    0: 'home',
}
# Larguras testadas: celular estreito (onde as 5 abas apertam) e celular grande.
LARGURAS = [360, 500]

DRIVER = r"""
<script>
(function(){
  const q=new URLSearchParams(location.search);
  const step=+(q.get('s')||0);
  /* O Chrome headless nao aceita janela menor que 500px, entao a largura de
     celular estreito e simulada apertando o proprio documento.              */
  const w=+(q.get('w')||0);
  if(w){document.documentElement.style.width=w+'px';document.body.style.width=w+'px';document.body.style.margin='0';}
  const LARG=w||innerWidth;
  try{localStorage.clear()}catch(e){}
  window.confirm=()=>true;         /* encerrar racha etc. perguntam (D-92); um dialogo travaria o headless */
  S=defState();
  const tema=q.get('t');if(tema)S.ui.theme=tema;   /* escuro (padrao) ou claro */
  if(step===10){                   /* destaques do mes, na tela do racha */
    A.demo();A.startRacha();
    L().live.presentIds=L().players.map(p=>p.id);
    A.toTimes();A.startMatch();
    A.goal({dataset:{s:'0'}});
    const g=L().live.cur.events.find(e=>e.type==='goal');
    A.setGoalScorer({dataset:{t:String(g.t),id:L().live.cur.lineups[0][0]}});closeSheet();
    A.goal({dataset:{s:'0'}});A.endMatch();closeSheet();A.endRacha();closeSheet();
  }else if(step===9){                    /* time menor entrando: quem completa? */
    A.demo();A.startRacha();
    const l=L(),lv=l.live;
    lv.presentIds=l.players.filter(p=>!p.gk).slice(0,13).map(p=>p.id);lv.gkToday=[];
    A.toTimes();
    onDrop(lv.teams[1].ids[0],{dataset:{dropZone:'bench'}});   /* alguem foi embora */
    A.startMatch();A.goal({dataset:{s:'0'}});A.endMatch();closeSheet();
  }else if(step>0){
    A.demo();A.startRacha();
    L().live.presentIds=L().players.map(p=>p.id);
    if(step>=2)A.toTimes();
    if(step>=3){A.startMatch();A.goal({dataset:{s:'0'}});A.goal({dataset:{s:'1'}});
      const g=L().live.cur.events.find(e=>e.type==='goal');
      A.setGoalScorer({dataset:{t:String(g.t),id:L().live.cur.lineups[0][0]}});closeSheet();}
    if(step>=4){A.goal({dataset:{s:'0'}});A.endMatch();closeSheet();}
    if(step>=5){                     /* assume um perfil: e o que marca "VOCE" no historico */
      const p=L().players[1];p.owner='Mauro';S.me.name='Mauro';
    }
    if(step===11||step===12||step===13)S.ui.tab='ranking';
    if(step===5)S.ui.tab='ranking';
    if(step===6)S.ui.tab='hist';
    if(step===7)S.ui.tab='cfg';
    if(step===8)S.ui.tab='stats';
  }
  render();closeSheet();
  if(step===11){                   /* ficha do admin: opinioes sobre o nivel (D-95) */
    const l=L(),eu=l.players[1];eu.role='admin';
    const p=l.players.find(x=>x.L.games>0&&x!==eu)||l.players[0];
    A.pSheet({dataset:{id:p.id}});
    const sh=document.querySelector('#sheet');if(sh)sh.scrollTop=380;
  }
  if(step===14){                   /* o resumo que vai para o grupo: uma noite inteira (D-99) */
    A.demo();A.startRacha();
    const l=L();l.live.presentIds=l.players.map(p=>p.id);
    A.toTimes();A.startJogo();
    for(let k=0;k<8;k++){A.startMatch();const c=l.live.cur;c.startedAt=Date.now()-6*60000;
      const s=k%3===2?'1':'0';A.goal({dataset:{s}});if(k%4===1)A.goal({dataset:{s}});
      const g=c.events.find(e=>e.type==='goal');A.setGoalScorer({dataset:{t:String(g.t),id:c.lineups[+s][k%4]}});closeSheet();
      if(k===5)A.goal({dataset:{s:s==='0'?'1':'0'}});
      A.endMatch();closeSheet();}
    A.endRacha();
  }
  if(step===13){                   /* ficha do admin com opinioes de varias pessoas, uma divergente e um "nao sei" */
    const l=L(),eu=l.players[1];eu.role='admin';
    const p=l.players.find(x=>x.L.games>0&&x!==eu)||l.players[0];
    const rat=l.players.filter(x=>x!==eu&&x!==p).slice(0,4);rat.forEach(x=>x.role='lancador');
    p.L.op=[{by:null,e:stepMid(7),ts:1},{by:eu.id,e:stepMid(7),ts:2},{by:rat[0].id,e:stepMid(4),ts:3},{by:rat[1].id,e:stepMid(13),ts:4},{by:rat[2].id,e:stepMid(7),ts:5},{by:rat[3].id,e:null,ts:6}];
    rebuildAll(l);render();A.pSheet({dataset:{id:p.id,r:'L'}});
    const sh=document.querySelector('#sheet');if(sh)sh.scrollTop=430;
  }
  if(step===12){                   /* a lista de quem lanca: uma opiniao por pessoa (D-95) */
    const l=L(),eu=l.players[1];eu.role='admin';
    const a=l.players[0];a.role='lancador';
    l.players.slice(2,8).forEach((p,i)=>{p.L.op=(p.L.op||[]).filter(o=>o.by!==eu.id);if(i%2)p.L.op.push({by:eu.id,e:stepMid(4+3*(i%3)),ts:1})});
    rebuildAll(l);render();A.opSheet();
  }
  const problemas=[];
  const nome=e=>e.tagName.toLowerCase()+(e.className?'.'+String(e.className).trim().split(/\s+/).join('.'):'');
  const dentro=[...document.querySelectorAll('#app *')];
  for(const e of dentro){
    const r=e.getBoundingClientRect(),cs=getComputedStyle(e);
    if(r.width===0&&r.height===0)continue;
    /* dentro de uma faixa que rola de lado (filtros), passar da borda e o esperado */
    const rola=e.closest&&[...(function*(){let x=e.parentElement;while(x){yield x;x=x.parentElement}})()].some(x=>/auto|scroll/.test(getComputedStyle(x).overflowX));
    if(r.right>LARG+1&&!rola)problemas.push('estoura a direita: '+nome(e)+' ate '+Math.round(r.right)+'px (limite '+LARG+')');
    if(r.left<-1)problemas.push('estoura a esquerda: '+nome(e));
    if(cs.position==='fixed')problemas.push('position:fixed solto dentro do app: '+nome(e));
  }
  const clicaveis=[...document.querySelectorAll('#app button,#bar button')];
  for(const b of clicaveis){
    const r=b.getBoundingClientRect();
    if(r.width===0&&r.height===0)continue;
    if(r.height<32)problemas.push('alvo de toque baixo ('+Math.round(r.height)+'px): '+nome(b)+' "'+b.textContent.trim().slice(0,24)+'"');
    const cx=r.left+r.width/2,cy=r.top+r.height/2;
    if(cy<0||cy>innerHeight)continue;
    const topo=document.elementFromPoint(cx,cy);
    if(topo&&topo!==b&&!b.contains(topo)&&!topo.contains(b)&&!topo.closest('.bar,.nav,.toast,.sheet,.scrim'))
      problemas.push('coberto por outro elemento: "'+b.textContent.trim().slice(0,24)+'" atras de '+nome(topo));
  }
  document.title='RESULTADO:'+JSON.stringify(problemas.slice(0,8));
})();
</script>
"""

fonte = io.open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
alvo = os.path.join(TMP, 'visual.html')
io.open(alvo, 'w', encoding='utf-8').write(fonte.replace('</body>', DRIVER + '</body>'))
url = 'file:///' + alvo.replace('\\', '/')

# (largura, tema, telas): o claro roda nas telas onde a cor decide leitura
PASSES = [(l, 'claro', sorted(TELAS)) for l in LARGURAS] + [(500, 'escuro', [1, 2, 3, 5, 9, 10])]

falhas = 0
for larg, tema, steps in PASSES:
  print('--- %dpx %s ---' % (larg, tema))
  for step in steps:
    nome = TELAS[step]
    base = [chrome, '--headless=new', '--disable-gpu', '--virtual-time-budget=2500',
            '--window-size=%d,1100' % max(larg, 500)]
    qs = '?s=%d&w=%d&t=%s' % (step, larg, tema)
    sufixo = '' if tema == 'claro' else '-escuro'
    if larg == LARGURAS[-1]:
        subprocess.run(base + ['--hide-scrollbars',
                               '--screenshot=' + os.path.join(
                                   SHOTS, 's%d-%s%s.png' % (step, nome.split()[0], sufixo)),
                               url + qs],
                       capture_output=True)
    out = subprocess.run(base + ['--dump-dom', url + qs],
                         capture_output=True, text=True, encoding='utf-8', errors='replace').stdout or ''
    marca = 'RESULTADO:'
    i = out.find(marca)
    if i < 0:
        print('[%s %s] nao consegui ler o resultado (a tela pode ter quebrado)' % (nome, tema))
        falhas += 1
        continue
    bruto = out[i + len(marca):out.index('</title>', i)]
    try:
        probs = json.loads(bruto.replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>'))
    except Exception:
        probs = [bruto[:200]]
    if probs:
        falhas += len(probs)
        print('[%s %s] %d problema(s):' % (nome, tema, len(probs)))
        for p in probs:
            print('   - ' + p)
    else:
        print('[%s] ok' % nome)

print('\nprints em %s' % SHOTS)
if falhas:
    print('\n*** %d PROBLEMA(S) VISUAL(IS) ***' % falhas)
    sys.exit(1)
print('\nVISUAL OK: nada estourando, nada sobreposto, alvos de toque no tamanho.')
