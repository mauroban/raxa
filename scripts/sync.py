# -*- coding: utf-8 -*-
"""
Teste da camada de backend do Raxa: contas, RLS, trava otimista e tempo real.

Roda o index.html inteiro em um DOM falso, com um Supabase falso em memoria que
imita o schema de supabase/schema.sql (create_league, join_league, league_delta/save_parts
com compare-and-swap, RLS por associacao). Assim da para exercitar login,
criacao de liga, sincronizacao, conflito entre dois aparelhos e realtime sem
depender da rede.

Uso:  python scripts/sync.py
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
    this.value='';this.classList={add(){},remove(){},toggle(){},contains(){return false}};}
  set innerHTML(v){this._html=String(v)}
  get innerHTML(){return this._html}
  querySelector(){return null} querySelectorAll(){return []} closest(){return null}
  focus(){} click(){} appendChild(){} addEventListener(){} insertAdjacentHTML(){}
}
const els={};
['#app','#bar','#sheet','#scrim','#toast'].forEach(s=>els[s]=new El(s));
global.document={
  querySelector:s=>els[s]||null,
  querySelectorAll:()=>[],
  addEventListener:()=>{},
  createElement:()=>new El('tmp'),
  body:new El('body'),
  activeElement:{tagName:'BODY'},
  visibilityState:'visible',
};
global.window={};
global.navigator={};
const store={};
global.localStorage={getItem:k=>(k in store?store[k]:null),setItem:(k,v)=>store[k]=String(v),
                     removeItem:k=>{delete store[k]}};
global.confirm=()=>true;
global.prompt=()=>'Mauro';
global.alert=()=>{};

/* -------- Supabase falso: um Postgres de mentira, com RLS de mentira -------- */
const DB={users:[],profiles:[],leagues:[],members:[],requests:[],players:[],matches:[],sessions:[],live:{},log:[]};
function delta(lid,since){
  const l=DB.leagues.find(x=>x.id===lid);
  const rows=t=>DB[t].filter(r=>r.league_id===lid&&r.v>since&&(since>0||!r.deleted)).map(r=>({id:r.id,data:jclone(r.data),deleted:r.deleted}));
  const lv=DB.live[lid];
  return {id:lid,version:l.version,name:l.name,code:l.code,cfg:jclone(l.cfg),players:rows('players'),matches:rows('matches'),
    sessions:rows('sessions'),live:lv&&lv.v>since?{data:jclone(lv.data)}:null,log:DB.log.filter(r=>r.league_id===lid&&r.v>since).map(r=>jclone(r.data))};
}
function applyParts(lid,parts,nv){
  ['players','matches','sessions'].forEach(t=>(parts[t]||[]).forEach(r=>{
    const i=DB[t].findIndex(x=>x.league_id===lid&&x.id===r.id);
    if(r.deleted){if(i>=0){DB[t][i].deleted=true;DB[t][i].v=nv}return}
    const row={league_id:lid,id:r.id,data:jclone(r.data),v:nv,deleted:false};
    if(i>=0)DB[t][i]=row;else DB[t].push(row)}));
  if(parts.live)DB.live[lid]={data:parts.live.clear?null:jclone(parts.live.data),v:nv};
  (parts.log||[]).forEach(e=>DB.log.push({league_id:lid,data:jclone(e),v:nv}));
  const l=DB.leagues.find(x=>x.id===lid);
  if(parts.name)l.name=parts.name;if(parts.cfg)l.cfg=jclone(parts.cfg);
}
let RT=[];                                  // assinantes de realtime
const uuid=(n=>()=>'uuid-'+(++n))(0);
const jclone=o=>JSON.parse(JSON.stringify(o));
let CODEN=0;

function emit(ev,row){ RT.forEach(fn=>fn({eventType:ev,new:row?{id:row.id}:null,old:row?{id:row.id}:null})) }
function emitM(ev,row){ RT.forEach(fn=>fn({eventType:ev,new:ev==='INSERT'?row:null,old:ev==='DELETE'?row:null})) }

function fakeClient(){
  let session=null;
  const uidNow=()=>session&&session.user.id;
  const isMember=lid=>!!(uidNow()&&DB.members.some(m=>m.league_id===lid&&m.user_id===uidNow()));

  const rpcs={
    create_league({p_name,p_data}){
      if(!uidNow())return{data:null,error:{message:'nao autenticado'}};
      const d=p_data||{};
      const row={id:uuid(),name:(p_name||'').trim()||'Meu racha',code:'COD'+(++CODEN),owner_id:uidNow(),cfg:jclone(d.cfg||{}),version:2};
      DB.leagues.push(row);
      applyParts(row.id,{players:(d.players||[]).map(p=>({id:p.id,data:p})),matches:(d.matches||[]).map(m=>({id:m.id,data:m})),
        sessions:(d.sessions||[]).map(x=>({id:x.id,data:x})),live:{data:d.live||null},log:d.log||[]},2);
      DB.members.push({league_id:row.id,user_id:uidNow()});
      emit('INSERT',row);
      return{data:jclone(row),error:null};
    },
    join_league({p_code}){
      if(!uidNow())return{data:null,error:{message:'nao autenticado'}};
      const row=DB.leagues.find(l=>l.code===String(p_code).trim().toUpperCase());
      if(!row)return{data:null,error:{message:'codigo nao encontrado'}};
      if(DB.members.some(m=>m.league_id===row.id&&m.user_id===uidNow()))
        return{data:{status:'member',league:jclone(row)},error:null};
      if(!DB.requests.some(r=>r.league_id===row.id&&r.user_id===uidNow()))
        DB.requests.push({league_id:row.id,user_id:uidNow(),requested_at:new Date().toISOString()});
      return{data:{status:'pending',id:row.id,name:row.name},error:null};
    },
    my_requests(){
      return{data:DB.requests.filter(r=>r.user_id===uidNow()).map(r=>({league_id:r.league_id,name:DB.leagues.find(l=>l.id===r.league_id).name,requested_at:r.requested_at})),error:null};
    },
    cancel_request({p_id}){DB.requests=DB.requests.filter(r=>!(r.league_id===p_id&&r.user_id===uidNow()));return{data:null,error:null}},
    league_accounts({p_id}){
      const l=DB.leagues.find(x=>x.id===p_id);if(!l||l.owner_id!==uidNow())return{data:[],error:null};
      const un=u=>(DB.profiles.find(p=>p.id===u)||{}).username||'?';
      return{data:DB.requests.filter(r=>r.league_id===p_id).map(r=>({user_id:r.user_id,username:un(r.user_id),joined_at:r.requested_at,is_owner:false,pending:true}))
        .concat(DB.members.filter(m=>m.league_id===p_id).map(m=>({user_id:m.user_id,username:un(m.user_id),joined_at:new Date().toISOString(),is_owner:m.user_id===l.owner_id,pending:false}))),error:null};
    },
    approve_request({p_id,p_user}){
      const l=DB.leagues.find(x=>x.id===p_id);if(!l||l.owner_id!==uidNow())return{data:null,error:{message:'so o admin aprova entrada'}};
      if(!DB.requests.some(r=>r.league_id===p_id&&r.user_id===p_user))return{data:null,error:{message:'pedido nao encontrado'}};
      DB.requests=DB.requests.filter(r=>!(r.league_id===p_id&&r.user_id===p_user));
      const row={league_id:p_id,user_id:p_user};DB.members.push(row);emitM('INSERT',row);
      return{data:null,error:null};
    },
    reject_request({p_id,p_user}){DB.requests=DB.requests.filter(r=>!(r.league_id===p_id&&r.user_id===p_user));return{data:null,error:null}},
    remove_member({p_id,p_user}){
      const row={league_id:p_id,user_id:p_user};
      DB.members=DB.members.filter(m=>!(m.league_id===p_id&&m.user_id===p_user));emitM('DELETE',row);
      return{data:null,error:null};
    },
    league_delta({p_id,p_since}){
      if(!uidNow())return{data:null,error:{message:'nao autenticado'}};
      if(!isMember(p_id))return{data:null,error:{message:'nao e membro desta liga'}};
      return{data:delta(p_id,p_since||0),error:null};
    },
    save_parts({p_id,p_version,p_parts}){
      if(!uidNow())return{data:null,error:{message:'nao autenticado'}};
      if(!isMember(p_id))return{data:null,error:{message:'nao e membro desta liga'}};
      const row=DB.leagues.find(l=>l.id===p_id);
      if(!row)return{data:null,error:{message:'liga nao existe'}};
      if(row.version!==p_version)
        return{data:{ok:false,version:row.version,delta:delta(p_id,p_version)},error:null};
      row.version++;
      applyParts(p_id,p_parts||{},row.version);
      emit('UPDATE',row);
      return{data:{ok:true,version:row.version,name:row.name,code:row.code},error:null};
    },
    league_size({p_id}){return{data:{players:DB.players.filter(p=>p.league_id===p_id&&!p.deleted).length,matches:DB.matches.filter(m=>m.league_id===p_id&&!m.deleted).length,sessions:0,log:DB.log.filter(x=>x.league_id===p_id).length,bytes:1234},error:null}},
    leave_league({p_id}){
      DB.members=DB.members.filter(m=>!(m.league_id===p_id&&m.user_id===uidNow()));
      return{data:null,error:null};
    }
  };

  class Q{
    constructor(t){this.t=t;this.op='select';this.f={}}
    select(){this.op='select';return this}
    delete(){this.op='delete';return this}
    eq(k,v){this.f[k]=v;return this}
    order(){return this}
    maybeSingle(){this.single=true;return this.run()}
    then(res,rej){return this.run().then(res,rej)}
    async run(){
      let rows=DB[this.t==='leagues'?'leagues':this.t==='profiles'?'profiles':'members'];
      rows=rows.filter(r=>Object.keys(this.f).every(k=>r[k]===this.f[k]));
      if(this.t==='leagues')rows=rows.filter(r=>isMember(r.id));            // RLS
      if(this.op==='delete'){
        const alvo=rows.filter(r=>r.owner_id===uidNow());                   // so o dono apaga
        alvo.forEach(r=>{DB.leagues=DB.leagues.filter(x=>x.id!==r.id);emit('DELETE',r)});
        return{data:null,error:null};
      }
      const out=jclone(rows);
      return{data:this.single?(out[0]||null):out,error:null};
    }
  }

  return{
    auth:{
      async getSession(){return{data:{session},error:null}},
      async signUp({email,password,options}){
        if(DB.users.some(u=>u.email===email))return{data:{session:null},error:{message:'User already registered'}};
        if(String(password).length<6)return{data:{session:null},error:{message:'Password should be at least 6 characters.'}};
        const u={id:uuid(),email,password};
        DB.users.push(u);
        DB.profiles.push({id:u.id,username:(options&&options.data&&options.data.username)||email.split('@')[0]});
        session={user:{id:u.id,email:u.email}};
        return{data:{session},error:null};
      },
      async signInWithPassword({email,password}){
        const u=DB.users.find(x=>x.email===email&&x.password===password);
        if(!u)return{data:{session:null},error:{message:'Invalid login credentials'}};
        session={user:{id:u.id,email:u.email}};
        return{data:{session},error:null};
      },
      async signOut(){session=null;return{error:null}}
    },
    from:t=>new Q(t),
    async rpc(name,args){
      const f=rpcs[name];
      if(!f)return{data:null,error:{message:'rpc '+name+' nao existe'}};
      return f(args||{});
    },
    channel(){const self={on(_e,_f,cb){RT.push(cb);return self},subscribe(){return self}};return self},
    removeChannel(){RT=[]}
  };
}
global.window.supabase={createClient:()=>fakeClient()};
global.window.RAXA_CFG={url:'http://fake.supabase.co',anonKey:'anon'};
"""

teste = r"""
/* -------- teste -------- */
let fails=0;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
function ok(label,cond,extra){
  if(cond)console.log('  ok: '+label);
  else{fails++;console.log('  FALHOU: '+label+(extra?' -> '+extra:''))}
}
async function step(label,fn){
  try{await fn()}
  catch(e){fails++;console.log('  QUEBROU em "'+label+'": '+e.message+'\n    '+String(e.stack).split('\n')[1])}
}
const srv=id=>DB.leagues.find(l=>l.id===id);
const val=(el,v)=>{els[el]=Object.assign(els[el]||new El(el),{value:v});return els[el]};

(async()=>{

console.log('\n[sync] conta');
await step('boot sem sessao cai na tela de entrar',async()=>{
  await boot();
  ok('tela de login desenhada',/Criar conta/.test(els['#app'].innerHTML));
  ok('nada de liga carregada',S.ligas.length===0);
});

await step('senha curta e recusada',async()=>{
  authMode='criar';val('#au','mauro');val('#ap','123');
  await A.doSignup();
  ok('recusou senha de 3 caracteres',DB.users.length===0&&/6 caracteres/.test(els['#app'].innerHTML));
});

await step('criar conta entra direto',async()=>{
  authMode='criar';val('#au','mauro');val('#ap','segredo1');
  await A.doSignup();
  ok('usuario criado',DB.users.length===1);
  ok('perfil criado com o username',DB.profiles[0].username==='mauro');
  ok('sem e-mail de verdade',/@raxa\.app$/.test(DB.users[0].email));
  ok('ME preenchido',ME&&ME.username==='mauro');
  ok('S.me.name e a conta',S.me.name==='mauro');
});

console.log('\n[sync] liga vai para o banco');
let ligaId=null;
await step('criar liga de exemplo',async()=>{
  await A.demo();
  await sleep(50);
  ligaId=S.active;
  ok('liga existe no servidor',!!srv(ligaId));
  ok('id do servidor virou o id local',/^uuid-/.test(ligaId));
  const nP=DB.players.filter(p=>p.league_id===ligaId&&!p.deleted).length;
  ok('19 jogadores gravados, um por linha',nP===19,nP+' jogadores');
  ok('a linha do jogador guarda so fatos (sem elo/rank/forma)',(()=>{const d=DB.players.find(p=>p.league_id===ligaId).data;return d.L&&d.L.elo===undefined&&d.L.rank===undefined&&d.goals===undefined})());
  ok('dono e quem criou',srv(ligaId).owner_id===ME.id);
  ok('virou membro',DB.members.length===1);
  ok('ganhou codigo de convite',!!srv(ligaId).code);
});

await step('mexer no racha sobe para o servidor',async()=>{
  const v0=srv(ligaId).version;
  A.startRacha();
  L().players.slice(0,10).forEach(p=>A.pres({dataset:{id:p.id}}));
  render();
  await sleep(700);                                   // deixa o debounce rodar
  ok('versao subiu',srv(ligaId).version>v0,'v'+v0+' -> v'+srv(ligaId).version);
  ok('presenca chegou no banco, na linha do live',DB.live[ligaId].data.presentIds.length===10,
     JSON.stringify((DB.live[ligaId].data||{}).presentIds||[]).slice(0,40));
});

await step('save() sem mudanca nao gasta gravacao',async()=>{
  const v0=srv(ligaId).version;
  A.tab({dataset:{v:'ranking'}});                     // so troca de aba
  await sleep(700);
  ok('trocar de aba nao gravou',srv(ligaId).version===v0,'versao foi para '+srv(ligaId).version);
});

console.log('\n[sync] segundo aparelho');
const codigo=srv(ligaId).code;
await step('outra conta entra pelo codigo',async()=>{
  await A.logout();
  ok('deslogou',ME===null&&S.ligas.length===0);
  authMode='criar';val('#au','luis');val('#ap','segredo2');
  await A.doSignup();
  ok('luis entrou',ME.username==='luis');
  ok('luis nao ve a liga dos outros',S.ligas.length===0,S.ligas.length+' ligas');
  val('#jc',codigo);
  await A.doJoin();
  ok('o codigo gera um PEDIDO, nao entrada',S.active===null&&S.ligas.length===0&&PEND.length===1,'ligas='+S.ligas.length+' pend='+PEND.length);
  ok('no servidor, luis nao e membro',!DB.members.some(m=>m.league_id===ligaId&&m.user_id===ME.id));
});

await step('o admin ve o pedido e aprova',async()=>{
  const luisId=ME.id;
  await A.logout();
  val('#au','mauro');val('#ap','segredo1');authMode='entrar';
  await A.doLogin();
  A.openLiga({dataset:{id:ligaId}});
  A.tab({dataset:{v:'ranking'}});
  await loadAccounts(ligaId);
  ok('o card Membros mostra o pedido',/pediu para entrar/.test(els['#app'].innerHTML));
  await A.accApprove({dataset:{u:luisId}});
  ok('luis virou membro no servidor',DB.members.some(m=>m.league_id===ligaId&&m.user_id===luisId));
  ok('o pedido sumiu',!DB.requests.length);
  await A.logout();
  val('#au','luis');val('#ap','segredo2');
  await A.doLogin();
  ok('luis agora ve a liga',S.ligas.length===1&&PEND.length===0,'ligas='+S.ligas.length+' pend='+PEND.length);
  A.openLiga({dataset:{id:ligaId}});
  ok('recebeu os 19 jogadores',L().players.length===19,L().players.length+'');
  ok('recebeu a presenca do racha',L().live&&L().live.presentIds.length===10);
});

await step('o que o luis grava, o mauro le',async()=>{
  const alguem=L().players[10].id;
  A.pres({dataset:{id:alguem}});
  await sleep(700);
  ok('11 presentes no servidor',DB.live[ligaId].data.presentIds.length===11);
  await A.logout();
  val('#au','mauro');val('#ap','segredo1');authMode='entrar';
  await A.doLogin();
  ok('mauro voltou',ME.username==='mauro');
  ok('mauro ve a liga',S.ligas.length===1);
  ok('depois de trocar de conta, cai na lista de ligas',S.active===null);
  A.openLiga({dataset:{id:ligaId}});
  ok('mauro ve os 11 presentes',L().live.presentIds.length===11,
     (L().live?L().live.presentIds.length:'sem live')+'');
});

console.log('\n[sync] conflito entre dois aparelhos');
await step('gravacao velha nao atropela a nova',async()=>{
  /* alguem gravou no servidor enquanto este aparelho estava mexendo */
  const row=srv(ligaId);
  row.cfg=JSON.parse(JSON.stringify(row.cfg));
  row.cfg.stintMin=9;                                 // mudanca de outro aparelho
  row.name='Racha renomeado';
  row.version++;
  const vServ=row.version;
  const alvoAntes=L().cfg.targetGoals;
  L().cfg.targetGoals=alvoAntes+3;                    // mudanca local, em cima do estado ja velho
  save();
  await sleep(700);
  ok('o servidor nao foi atropelado',srv(ligaId).cfg.stintMin===9,
     'stintMin='+srv(ligaId).cfg.stintMin);
  ok('a tela se realinhou com o servidor',L().cfg.stintMin===9,'stintMin='+L().cfg.stintMin);
  ok('e pegou o nome novo',L().name==='Racha renomeado',L().name);
  ok('a alteracao local em cima do estado velho foi descartada',L().cfg.targetGoals===alvoAntes,
     'targetGoals='+L().cfg.targetGoals);
  ok('a versao local acompanhou',VER[ligaId]===srv(ligaId).version,'local v'+VER[ligaId]+' servidor v'+srv(ligaId).version);
});

console.log('\n[sync] tempo real');
await step('mudanca de fora chega sem recarregar',async()=>{
  const row=srv(ligaId);
  row.cfg=JSON.parse(JSON.stringify(row.cfg));
  row.cfg.targetMin=99;
  row.version++;
  emit('UPDATE',row);
  await sleep(300);
  ok('a tela pegou a mudanca',L().cfg.targetMin===99,'targetMin='+L().cfg.targetMin);
});

await step('o eco da propria gravacao nao redesenha a toa',async()=>{
  L().cfg.targetMin=8;
  save();
  await sleep(700);
  ok('o valor local sobreviveu',L().cfg.targetMin===8,'targetMin='+L().cfg.targetMin);
  ok('e chegou no servidor',srv(ligaId).cfg.targetMin===8);
});

console.log('\n[sync] gravacao incremental');
await step('um gol so grava o live, nao a liga inteira',async()=>{
  const chamadas=[];const rpc0=sb.rpc.bind(sb);
  sb.rpc=(n,a)=>{chamadas.push([n,a]);return rpc0(n,a)};
  A.toTimes();await sleep(700);A.startJogo();await sleep(700);chamadas.length=0;
  A.startMatch();await sleep(700);
  const salvas=chamadas.filter(c=>c[0]==='save_parts');
  ok('gravou via save_parts',salvas.length>=1);
  const parts=salvas[0][1].p_parts;
  ok('so a parte live foi',!!parts.live&&!parts.players&&!parts.matches&&!parts.cfg,Object.keys(parts).join(','));
  sb.rpc=rpc0;
});
await step('a partida encerrada vira uma linha nova em matches',async()=>{
  const n0=DB.matches.filter(m=>m.league_id===ligaId).length;
  A.goal({dataset:{s:'0'}});A.finish({dataset:{}});await sleep(700);
  const rows=DB.matches.filter(m=>m.league_id===ligaId);
  ok('uma partida a mais no banco',rows.length===n0+1,rows.length+'');
  const d=rows[rows.length-1].data;
  ok('a linha da partida guarda os fatos (eventos, gols com hora)',Array.isArray(d.events)&&Array.isArray(d.goals)&&d.goals[0].t>0);
  ok('e nao guarda o derivado (deltas/moves)',d.deltas===undefined&&d.moves===undefined);
  ok('o jogador que subiu de nivel continua so com fatos na linha dele',DB.players.filter(p=>p.league_id===ligaId).every(p=>p.data.L.elo===undefined));
});
await step('o outro aparelho recebe so o delta',async()=>{
  const d=delta(ligaId,VER[ligaId]-1);
  ok('delta desde a versao anterior tem 1 partida e o live',d.matches.length===1&&!!d.live,'matches='+d.matches.length);
  ok('e nao manda os 19 jogadores de novo',d.players.length===0,'players='+d.players.length);
});

console.log('\n[sync] recarregar a pagina');
await step('boot com sessao viva restaura tudo',async()=>{
  const antes=JSON.stringify(L().players.map(p=>p.name));
  S=defState();ME=null;
  await boot();
  ok('voltou logado, sem pedir senha',!!ME&&ME.username==='mauro');
  ok('a liga voltou',S.ligas.length===1);
  ok('os jogadores voltaram iguais',JSON.stringify(L().players.map(p=>p.name))===antes);
  ok('a ultima liga aberta foi lembrada',S.active===ligaId);
});

console.log('\n[sync] sair da liga e apagar');
await step('quem nao e dono so sai',async()=>{
  await A.logout();
  val('#au','luis');val('#ap','segredo2');authMode='entrar';
  await A.doLogin();
  S.active=ligaId;
  await A.delLiga();
  ok('a liga continua de pe',!!srv(ligaId));
  ok('mas o luis saiu',!DB.members.some(m=>m.user_id===ME.id&&m.league_id===ligaId));
  ok('e sumiu da tela dele',S.ligas.length===0);
});

await step('o dono apaga de verdade',async()=>{
  await A.logout();
  val('#au','mauro');val('#ap','segredo1');authMode='entrar';
  await A.doLogin();
  S.active=ligaId;
  await A.delLiga();
  ok('sumiu do banco',!srv(ligaId));
  ok('sumiu da tela',S.ligas.length===0);
});

console.log(fails?'\n*** '+fails+' FALHA(S) ***':'\nSYNC OK: backend, contas e sincronizacao');
process.exit(fails?1:0);
})();
"""

out = os.path.join(SP, 'sync.js')
io.open(out, 'w', encoding='utf-8').write(stub + js + teste)
sys.exit(subprocess.run(['node', out]).returncode)
