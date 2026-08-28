-- ============================================================================
-- Raxa — esquema de teste (Supabase / Postgres)
--
-- Modelo de DOCUMENTO: cada liga é uma linha, e o objeto de liga do app
-- ({cfg, players, matches, sessions, live}) mora inteiro na coluna `data`.
-- O motor (splitStints, computeElo, rebuildAll) continua rodando no cliente,
-- exatamente como no protótipo — nenhuma regra de produto mudou.
--
-- O esquema relacional definitivo está em BANCO-DE-DADOS.md. Este aqui é o
-- degrau intermediário: contas de verdade, dados compartilhados, sem reescrita.
--
-- Como aplicar: Supabase -> SQL Editor -> cole tudo -> Run.
-- Idempotente: pode rodar de novo sem quebrar.
-- ============================================================================

-- ---------------------------------------------------------------- perfis ---
create table if not exists public.profiles (
  id         uuid primary key references auth.users on delete cascade,
  username   text unique not null,
  created_at timestamptz not null default now()
);

-- ---------------------------------------------------------------- ligas ----
create table if not exists public.leagues (
  id         uuid primary key default gen_random_uuid(),
  name       text   not null default 'Liga',
  code       text   unique not null,
  owner_id   uuid   not null references auth.users on delete cascade,
  data       jsonb  not null default '{}'::jsonb,
  version    bigint not null default 1,   -- trava otimista: quem grava velho perde
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.league_members (
  league_id uuid references public.leagues on delete cascade,
  user_id   uuid references auth.users     on delete cascade,
  joined_at timestamptz not null default now(),
  primary key (league_id, user_id)
);

create index if not exists league_members_user_idx on public.league_members(user_id);

-- ------------------------------------------------ conta nova => perfil -----
-- O username vem no metadata do signUp. Sem verificação, sem e-mail real: o
-- cliente monta <username>@raxa.app só porque o Auth exige formato de e-mail.
create or replace function public.handle_new_user()
returns trigger language plpgsql security definer set search_path = public as $fn$
begin
  insert into public.profiles (id, username)
  values (new.id, coalesce(new.raw_user_meta_data->>'username', split_part(new.email,'@',1)))
  on conflict (id) do nothing;
  return new;
end $fn$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- ------------------------------------------------------- RLS: helpers ------
-- security definer para não recursar na política de `leagues`.
create or replace function public.is_member(lid uuid)
returns boolean language sql security definer stable set search_path = public as $fn$
  select exists (
    select 1 from public.league_members
    where league_id = lid and user_id = auth.uid()
  );
$fn$;

alter table public.profiles       enable row level security;
alter table public.leagues        enable row level security;
alter table public.league_members enable row level security;

drop policy if exists profiles_read   on public.profiles;
drop policy if exists profiles_write  on public.profiles;
drop policy if exists leagues_read    on public.leagues;
drop policy if exists leagues_update  on public.leagues;
drop policy if exists leagues_delete  on public.leagues;
drop policy if exists members_read    on public.league_members;
drop policy if exists members_leave   on public.league_members;

-- Perfil: todo mundo logado lê (para mostrar quem é quem), só o dono escreve.
create policy profiles_read  on public.profiles for select to authenticated using (true);
create policy profiles_write on public.profiles for update to authenticated
  using (id = auth.uid()) with check (id = auth.uid());

-- Liga: só quem é membro enxerga. Criar/entrar/gravar passa pelas funções
-- abaixo (security definer) — NÃO existe policy de UPDATE de propósito: toda
-- gravação tem que passar pelo compare-and-swap de save_league. Um UPDATE
-- direto pela API pularia a trava de versão e atropelaria o racha dos outros.
create policy leagues_read   on public.leagues for select to authenticated using (public.is_member(id));
create policy leagues_delete on public.leagues for delete to authenticated using (owner_id = auth.uid());

-- Membro: cada um só vê o próprio vínculo, e só pode desfazer o próprio.
create policy members_read  on public.league_members for select to authenticated using (user_id = auth.uid());
create policy members_leave on public.league_members for delete to authenticated using (user_id = auth.uid());

-- ------------------------------------------------------- código de convite -
create or replace function public.gen_code()
returns text language plpgsql as $fn$
declare
  alfabeto text := 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';  -- sem O/0, I/1
  c text;
begin
  loop
    c := '';
    for _i in 1..6 loop
      c := c || substr(alfabeto, 1 + floor(random()*length(alfabeto))::int, 1);
    end loop;
    exit when not exists (select 1 from public.leagues where code = c);
  end loop;
  return c;
end $fn$;

-- ------------------------------------------------------------- criar liga --
create or replace function public.create_league(p_name text, p_data jsonb)
returns public.leagues language plpgsql security definer set search_path = public as $fn$
declare l public.leagues;
begin
  if auth.uid() is null then raise exception 'nao autenticado'; end if;
  insert into public.leagues (name, code, owner_id, data)
  values (coalesce(nullif(trim(p_name),''),'Meu racha'), public.gen_code(), auth.uid(), coalesce(p_data,'{}'::jsonb))
  returning * into l;
  insert into public.league_members (league_id, user_id) values (l.id, auth.uid());
  return l;
end $fn$;

-- -------------------------------------------------------------- entrar -----
create or replace function public.join_league(p_code text)
returns public.leagues language plpgsql security definer set search_path = public as $fn$
declare l public.leagues;
begin
  if auth.uid() is null then raise exception 'nao autenticado'; end if;
  select * into l from public.leagues where code = upper(trim(p_code));
  if not found then raise exception 'codigo nao encontrado'; end if;
  insert into public.league_members (league_id, user_id)
  values (l.id, auth.uid()) on conflict do nothing;
  return l;
end $fn$;

-- --------------------------------------------------------------- gravar ----
-- Compare-and-swap. Se a versão que o cliente traz não é a do servidor, alguém
-- gravou no meio do caminho: devolve ok=false + o estado bom, e o cliente se
-- realinha em vez de atropelar o racha de outra pessoa.
create or replace function public.save_league(p_id uuid, p_data jsonb, p_version bigint)
returns jsonb language plpgsql security definer set search_path = public as $fn$
declare cur public.leagues;
begin
  if auth.uid() is null then raise exception 'nao autenticado'; end if;
  if not public.is_member(p_id) then raise exception 'nao e membro desta liga'; end if;

  select * into cur from public.leagues where id = p_id for update;
  if not found then raise exception 'liga nao existe'; end if;

  if cur.version <> p_version then
    return jsonb_build_object('ok', false, 'version', cur.version,
                              'data', cur.data, 'name', cur.name, 'code', cur.code);
  end if;

  update public.leagues
     set data       = p_data,
         name       = coalesce(nullif(trim(p_data->>'name'),''), cur.name),
         version    = cur.version + 1,
         updated_at = now()
   where id = p_id
  returning * into cur;

  return jsonb_build_object('ok', true, 'version', cur.version, 'name', cur.name, 'code', cur.code);
end $fn$;

-- ---------------------------------------------------------------- sair -----
create or replace function public.leave_league(p_id uuid)
returns void language plpgsql security definer set search_path = public as $fn$
begin
  delete from public.league_members where league_id = p_id and user_id = auth.uid();
  -- o dono apagando de fato a liga é DELETE direto na tabela (policy leagues_delete)
end $fn$;

-- ------------------------------------------------------------- realtime ----
-- O cliente não usa o payload (uma liga grande estoura o limite de mensagem):
-- ele só escuta "mudou" e busca a linha de novo.
do $do$
begin
  if not exists (
    select 1 from pg_publication_tables
    where pubname = 'supabase_realtime' and schemaname = 'public' and tablename = 'leagues'
  ) then
    alter publication supabase_realtime add table public.leagues;
  end if;
end $do$;

grant execute on function public.create_league(text, jsonb)       to authenticated;
grant execute on function public.join_league(text)                to authenticated;
grant execute on function public.save_league(uuid, jsonb, bigint) to authenticated;
grant execute on function public.leave_league(uuid)               to authenticated;

-- ------------------------------------------------ contas da liga (admin) ---
-- A policy members_read só mostra o próprio vínculo. O admin precisa ver
-- TODAS as contas que entraram — inclusive as que ainda não vincularam um
-- jogador — para vincular, criar jogador ou remover. Quem é admin vem do
-- documento da liga (mesma regra do cliente: dono, ou jogador vinculado com
-- role=admin; enquanto ninguém vinculou, todo membro é admin).
create or replace function public.is_league_admin(lid uuid)
returns boolean language plpgsql security definer stable set search_path = public as $fn$
declare l public.leagues; me text;
begin
  if auth.uid() is null then return false; end if;
  if not public.is_member(lid) then return false; end if;
  select * into l from public.leagues where id = lid;
  if not found then return false; end if;
  if l.owner_id = auth.uid() then return true; end if;
  select username into me from public.profiles where id = auth.uid();
  if not exists (select 1 from jsonb_array_elements(coalesce(l.data->'players','[]'::jsonb)) p
                 where coalesce(p->>'owner','') <> '') then
    return true;
  end if;
  return exists (select 1 from jsonb_array_elements(coalesce(l.data->'players','[]'::jsonb)) p
                 where p->>'owner' = me and p->>'role' = 'admin');
end $fn$;

create or replace function public.league_accounts(p_id uuid)
returns table(user_id uuid, username text, joined_at timestamptz, is_owner boolean)
language sql security definer stable set search_path = public as $fn$
  select m.user_id, coalesce(pr.username, '?'), m.joined_at, (l.owner_id = m.user_id)
  from public.league_members m
  join public.leagues l on l.id = m.league_id
  left join public.profiles pr on pr.id = m.user_id
  where m.league_id = p_id and public.is_league_admin(p_id)
  order by m.joined_at;
$fn$;

-- Tira uma conta da liga. O jogador (e o histórico) fica; só o acesso sai.
create or replace function public.remove_member(p_id uuid, p_user uuid)
returns void language plpgsql security definer set search_path = public as $fn$
declare l public.leagues;
begin
  if not public.is_league_admin(p_id) then raise exception 'so o admin remove contas'; end if;
  select * into l from public.leagues where id = p_id;
  if l.owner_id = p_user then raise exception 'o dono da liga nao pode ser removido'; end if;
  delete from public.league_members where league_id = p_id and user_id = p_user;
end $fn$;

grant execute on function public.is_league_admin(uuid)        to authenticated;
grant execute on function public.league_accounts(uuid)        to authenticated;
grant execute on function public.remove_member(uuid, uuid)    to authenticated;

-- ------------------------------------------------ pedidos de entrada -------
-- O código não entra mais direto: gera um PEDIDO, e só o admin aprova. Quem
-- pediu vê "aguardando" na home; quando o admin aprova, o vínculo em
-- league_members aparece e o Realtime avisa o aparelho dele.
create table if not exists public.league_requests (
  league_id    uuid references public.leagues on delete cascade,
  user_id      uuid references auth.users     on delete cascade,
  requested_at timestamptz not null default now(),
  primary key (league_id, user_id)
);
alter table public.league_requests enable row level security;
drop policy if exists requests_read   on public.league_requests;
drop policy if exists requests_cancel on public.league_requests;
create policy requests_read   on public.league_requests for select to authenticated using (user_id = auth.uid());
create policy requests_cancel on public.league_requests for delete to authenticated using (user_id = auth.uid());

-- join_league agora devolve jsonb: {status:'member', league:{...}} se já era
-- membro, ou {status:'pending', id, name} depois de registrar o pedido.
drop function if exists public.join_league(text);
create or replace function public.join_league(p_code text)
returns jsonb language plpgsql security definer set search_path = public as $fn$
declare l public.leagues;
begin
  if auth.uid() is null then raise exception 'nao autenticado'; end if;
  select * into l from public.leagues where code = upper(trim(p_code));
  if not found then raise exception 'codigo nao encontrado'; end if;
  if public.is_member(l.id) then
    return jsonb_build_object('status','member','league',to_jsonb(l));
  end if;
  insert into public.league_requests (league_id, user_id)
  values (l.id, auth.uid()) on conflict do nothing;
  return jsonb_build_object('status','pending','id',l.id,'name',l.name);
end $fn$;

-- Meus pedidos pendentes (a liga em si não é legível antes de virar membro).
create or replace function public.my_requests()
returns table(league_id uuid, name text, requested_at timestamptz)
language sql security definer stable set search_path = public as $fn$
  select r.league_id, l.name, r.requested_at
  from public.league_requests r join public.leagues l on l.id = r.league_id
  where r.user_id = auth.uid() order by r.requested_at;
$fn$;

create or replace function public.cancel_request(p_id uuid)
returns void language sql security definer set search_path = public as $fn$
  delete from public.league_requests where league_id = p_id and user_id = auth.uid();
$fn$;

-- league_accounts passa a trazer também quem PEDIU (pending=true), para o
-- admin ver tudo numa lista só.
drop function if exists public.league_accounts(uuid);
create or replace function public.league_accounts(p_id uuid)
returns table(user_id uuid, username text, joined_at timestamptz, is_owner boolean, pending boolean)
language sql security definer stable set search_path = public as $fn$
  select m.user_id, coalesce(pr.username, '?'), m.joined_at, (l.owner_id = m.user_id), false
  from public.league_members m
  join public.leagues l on l.id = m.league_id
  left join public.profiles pr on pr.id = m.user_id
  where m.league_id = p_id and public.is_league_admin(p_id)
  union all
  select r.user_id, coalesce(pr.username, '?'), r.requested_at, false, true
  from public.league_requests r
  left join public.profiles pr on pr.id = r.user_id
  where r.league_id = p_id and public.is_league_admin(p_id)
  order by 5 desc, 3;
$fn$;

create or replace function public.approve_request(p_id uuid, p_user uuid)
returns void language plpgsql security definer set search_path = public as $fn$
begin
  if not public.is_league_admin(p_id) then raise exception 'so o admin aprova entrada'; end if;
  if not exists (select 1 from public.league_requests where league_id = p_id and user_id = p_user) then
    raise exception 'pedido nao encontrado';
  end if;
  insert into public.league_members (league_id, user_id) values (p_id, p_user) on conflict do nothing;
  delete from public.league_requests where league_id = p_id and user_id = p_user;
end $fn$;

create or replace function public.reject_request(p_id uuid, p_user uuid)
returns void language plpgsql security definer set search_path = public as $fn$
begin
  if not public.is_league_admin(p_id) then raise exception 'so o admin recusa entrada'; end if;
  delete from public.league_requests where league_id = p_id and user_id = p_user;
end $fn$;

-- Realtime em league_members: quem foi aprovado (ou removido) fica sabendo na
-- hora. A RLS garante que cada um só recebe o próprio vínculo.
do $do$
begin
  if not exists (
    select 1 from pg_publication_tables
    where pubname = 'supabase_realtime' and schemaname = 'public' and tablename = 'league_members'
  ) then
    alter publication supabase_realtime add table public.league_members;
  end if;
end $do$;

grant execute on function public.join_league(text)                to authenticated;
grant execute on function public.my_requests()                    to authenticated;
grant execute on function public.cancel_request(uuid)             to authenticated;
grant execute on function public.league_accounts(uuid)            to authenticated;
grant execute on function public.approve_request(uuid, uuid)      to authenticated;
grant execute on function public.reject_request(uuid, uuid)       to authenticated;

-- ============================================================================
-- LIGA EM PARTES (substitui o documento único em leagues.data)
--
-- Cada entidade é uma linha com payload jsonb e carrega `v` = versão da liga
-- em que foi gravada. Isso dá sync incremental: o cliente pede "o que mudou
-- desde a versão X" (league_delta) e grava só o que mexeu (save_parts), com a
-- mesma trava otimista de antes (version em leagues). Só FATOS ficam aqui:
-- nível, Elo, forma e estatística são recalculados no cliente (rebuildAll).
--
-- Ligas antigas (documento em leagues.data) migram sozinhas na primeira
-- leitura: migrate_league espalha o documento nas tabelas e esvazia data.
-- ============================================================================
alter table public.leagues add column if not exists cfg      jsonb   not null default '{}'::jsonb;
alter table public.leagues add column if not exists migrated boolean not null default false;

create table if not exists public.league_players (
  league_id uuid   not null references public.leagues on delete cascade,
  id        text   not null,
  data      jsonb  not null,
  v         bigint not null default 1,
  deleted   boolean not null default false,
  primary key (league_id, id)
);
create table if not exists public.league_matches (
  league_id uuid   not null references public.leagues on delete cascade,
  id        text   not null,
  ts        bigint not null default 0,
  data      jsonb  not null,
  v         bigint not null default 1,
  deleted   boolean not null default false,
  primary key (league_id, id)
);
create table if not exists public.league_sessions (
  league_id uuid   not null references public.leagues on delete cascade,
  id        text   not null,
  data      jsonb  not null,
  v         bigint not null default 1,
  deleted   boolean not null default false,
  primary key (league_id, id)
);
create table if not exists public.league_live (
  league_id uuid primary key references public.leagues on delete cascade,
  data      jsonb,                      -- null = sem racha em andamento
  v         bigint not null default 1
);
create table if not exists public.league_log (
  league_id uuid   not null references public.leagues on delete cascade,
  seq       bigserial,
  data      jsonb  not null,
  v         bigint not null default 1,
  primary key (league_id, seq)
);
create index if not exists league_players_v  on public.league_players (league_id, v);
create index if not exists league_matches_v  on public.league_matches (league_id, v);
create index if not exists league_sessions_v on public.league_sessions (league_id, v);
create index if not exists league_log_v      on public.league_log (league_id, v);

-- Tudo passa pelas funções (security definer); sem policy = sem acesso direto.
alter table public.league_players  enable row level security;
alter table public.league_matches  enable row level security;
alter table public.league_sessions enable row level security;
alter table public.league_live     enable row level security;
alter table public.league_log      enable row level security;

-- --------------------------------------------------------------- migração --
create or replace function public.migrate_league(p_id uuid)
returns void language plpgsql security definer set search_path = public as $fn$
declare l public.leagues; nv bigint;
begin
  select * into l from public.leagues where id = p_id for update;
  if not found or l.migrated then return; end if;
  nv := l.version + 1;
  insert into public.league_players (league_id, id, data, v)
    select p_id, p->>'id', p, nv from jsonb_array_elements(coalesce(l.data->'players','[]'::jsonb)) p
    where p ? 'id' on conflict do nothing;
  insert into public.league_matches (league_id, id, ts, data, v)
    select p_id, m->>'id', coalesce((m->>'ts')::bigint,0), m, nv
    from jsonb_array_elements(coalesce(l.data->'matches','[]'::jsonb)) m
    where m ? 'id' on conflict do nothing;
  insert into public.league_sessions (league_id, id, data, v)
    select p_id, s->>'id', s, nv from jsonb_array_elements(coalesce(l.data->'sessions','[]'::jsonb)) s
    where s ? 'id' on conflict do nothing;
  insert into public.league_live (league_id, data, v)
    values (p_id, nullif(l.data->'live','null'::jsonb), nv)
    on conflict (league_id) do update set data = excluded.data, v = excluded.v;
  insert into public.league_log (league_id, data, v)
    select p_id, e, nv from jsonb_array_elements(coalesce(l.data->'log','[]'::jsonb)) e;
  update public.leagues
     set cfg = coalesce(l.data->'cfg','{}'::jsonb), data = '{}'::jsonb, migrated = true,
         version = nv, updated_at = now()
   where id = p_id;
end $fn$;

-- ------------------------------------------------------------------ delta --
-- Tudo que mudou desde p_since (0 = carga inicial). Linhas apagadas vêm com
-- deleted=true para o cliente tirar da tela.
create or replace function public.league_delta(p_id uuid, p_since bigint)
returns jsonb language plpgsql security definer set search_path = public as $fn$
declare l public.leagues; lv public.league_live;
begin
  if auth.uid() is null then raise exception 'nao autenticado'; end if;
  if not public.is_member(p_id) then raise exception 'nao e membro desta liga'; end if;
  perform public.migrate_league(p_id);
  select * into l from public.leagues where id = p_id;
  select * into lv from public.league_live where league_id = p_id;
  return jsonb_build_object(
    'id', l.id, 'version', l.version, 'name', l.name, 'code', l.code, 'cfg', l.cfg,
    'owner', (l.owner_id = auth.uid()),
    'players', coalesce((select jsonb_agg(jsonb_build_object('id',id,'data',data,'deleted',deleted))
                         from public.league_players where league_id = p_id and v > p_since
                           and (p_since > 0 or not deleted)), '[]'::jsonb),
    'matches', coalesce((select jsonb_agg(jsonb_build_object('id',id,'data',data,'deleted',deleted) order by ts)
                         from public.league_matches where league_id = p_id and v > p_since
                           and (p_since > 0 or not deleted)), '[]'::jsonb),
    'sessions', coalesce((select jsonb_agg(jsonb_build_object('id',id,'data',data,'deleted',deleted))
                         from public.league_sessions where league_id = p_id and v > p_since
                           and (p_since > 0 or not deleted)), '[]'::jsonb),
    'live', case when lv.league_id is not null and lv.v > p_since
                 then jsonb_build_object('data', lv.data) else null end,
    'log', coalesce((select jsonb_agg(data order by seq)
                     from public.league_log where league_id = p_id and v > p_since), '[]'::jsonb)
  );
end $fn$;

-- ------------------------------------------------------------------ gravar --
-- p_parts: {name?, cfg?, players:[{id,data}|{id,deleted:true}], matches:[...],
--           sessions:[...], live:{data}|{clear:true}, log:[entrada,...]}
-- Compare-and-swap na versão da liga. Em conflito devolve o delta desde a
-- versão do cliente: ele aplica por cima e reenvia só o que ainda difere.
create or replace function public.save_parts(p_id uuid, p_version bigint, p_parts jsonb)
returns jsonb language plpgsql security definer set search_path = public as $fn$
declare cur public.leagues; nv bigint; r jsonb;
begin
  if auth.uid() is null then raise exception 'nao autenticado'; end if;
  if not public.is_member(p_id) then raise exception 'nao e membro desta liga'; end if;
  perform public.migrate_league(p_id);
  select * into cur from public.leagues where id = p_id for update;
  if not found then raise exception 'liga nao existe'; end if;
  if cur.version <> p_version then
    return jsonb_build_object('ok', false, 'version', cur.version, 'delta', public.league_delta(p_id, p_version));
  end if;
  nv := cur.version + 1;

  for r in select * from jsonb_array_elements(coalesce(p_parts->'players','[]'::jsonb)) loop
    if coalesce((r->>'deleted')::boolean,false) then
      update public.league_players set deleted = true, v = nv where league_id = p_id and id = r->>'id';
    else
      insert into public.league_players (league_id, id, data, v) values (p_id, r->>'id', r->'data', nv)
      on conflict (league_id, id) do update set data = excluded.data, v = nv, deleted = false;
    end if;
  end loop;
  for r in select * from jsonb_array_elements(coalesce(p_parts->'matches','[]'::jsonb)) loop
    if coalesce((r->>'deleted')::boolean,false) then
      update public.league_matches set deleted = true, v = nv where league_id = p_id and id = r->>'id';
    else
      insert into public.league_matches (league_id, id, ts, data, v)
      values (p_id, r->>'id', coalesce((r->'data'->>'ts')::bigint,0), r->'data', nv)
      on conflict (league_id, id) do update set data = excluded.data, ts = excluded.ts, v = nv, deleted = false;
    end if;
  end loop;
  for r in select * from jsonb_array_elements(coalesce(p_parts->'sessions','[]'::jsonb)) loop
    if coalesce((r->>'deleted')::boolean,false) then
      update public.league_sessions set deleted = true, v = nv where league_id = p_id and id = r->>'id';
    else
      insert into public.league_sessions (league_id, id, data, v) values (p_id, r->>'id', r->'data', nv)
      on conflict (league_id, id) do update set data = excluded.data, v = nv, deleted = false;
    end if;
  end loop;
  if p_parts ? 'live' then
    insert into public.league_live (league_id, data, v)
    values (p_id, case when coalesce((p_parts->'live'->>'clear')::boolean,false) then null else p_parts->'live'->'data' end, nv)
    on conflict (league_id) do update set data = excluded.data, v = nv;
  end if;
  insert into public.league_log (league_id, data, v)
    select p_id, e, nv from jsonb_array_elements(coalesce(p_parts->'log','[]'::jsonb)) e;

  update public.leagues
     set name       = coalesce(nullif(trim(p_parts->>'name'),''), cur.name),
         cfg        = coalesce(p_parts->'cfg', cur.cfg),
         version    = nv,
         updated_at = now()
   where id = p_id
  returning * into cur;
  return jsonb_build_object('ok', true, 'version', cur.version, 'name', cur.name, 'code', cur.code);
end $fn$;

-- create_league continua recebendo o documento (é como o app monta a liga
-- nova); a migração espalha nas tabelas na hora.
create or replace function public.create_league(p_name text, p_data jsonb)
returns public.leagues language plpgsql security definer set search_path = public as $fn$
declare l public.leagues;
begin
  if auth.uid() is null then raise exception 'nao autenticado'; end if;
  insert into public.leagues (name, code, owner_id, data)
  values (coalesce(nullif(trim(p_name),''),'Meu racha'), public.gen_code(), auth.uid(), coalesce(p_data,'{}'::jsonb))
  returning * into l;
  insert into public.league_members (league_id, user_id) values (l.id, auth.uid());
  perform public.migrate_league(l.id);
  select * into l from public.leagues where id = l.id;
  return l;
end $fn$;

-- Tamanho real da liga no banco (Ajustes → só o admin vê).
create or replace function public.league_size(p_id uuid)
returns jsonb language sql security definer stable set search_path = public as $fn$
  select jsonb_build_object(
    'players',  (select count(*) from public.league_players  where league_id = p_id and not deleted),
    'matches',  (select count(*) from public.league_matches  where league_id = p_id and not deleted),
    'sessions', (select count(*) from public.league_sessions where league_id = p_id and not deleted),
    'log',      (select count(*) from public.league_log      where league_id = p_id),
    'bytes',    (select coalesce(sum(pg_column_size(data)),0) from public.league_matches  where league_id = p_id)
              + (select coalesce(sum(pg_column_size(data)),0) from public.league_players  where league_id = p_id)
              + (select coalesce(sum(pg_column_size(data)),0) from public.league_sessions where league_id = p_id)
              + (select coalesce(sum(pg_column_size(data)),0) from public.league_log      where league_id = p_id)
              + (select coalesce(pg_column_size(data),0)      from public.league_live     where league_id = p_id)
  ) where public.is_member(p_id);
$fn$;

grant execute on function public.migrate_league(uuid)               to authenticated;
grant execute on function public.league_delta(uuid, bigint)         to authenticated;
grant execute on function public.save_parts(uuid, bigint, jsonb)    to authenticated;
grant execute on function public.league_size(uuid)                  to authenticated;
