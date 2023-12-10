-- user
create table if not exists "user" (
    id uuid not null primary key default tuid6(),
    created_at timestamptz not null default now(),
    deleted_at timestamptz,
    -- Note, we're not creating a foreign key to auth.users.id because
    -- we want to be able to delete a user from auth.users without
    -- deleting their data from public.user.
    user_id uuid not null unique,
    email text not null unique,
    first_name text,
    last_name text,
    avatar_url text
);
alter table "user" enable row level security;

-- team
create type team_type as enum ('personal', 'organization');
create table if not exists team (
    id uuid not null primary key default tuid6(),
    created_at timestamptz not null default now(),
    deleted_at timestamptz,
    name text not null,
    type team_type not null,
    avatar_url text
);
alter table team enable row level security;

-- team_user join table
create type user_role as enum ('admin', 'member');
create table if not exists team_user (
    team_id uuid not null references team (id),
    user_id uuid not null references "user" (id),
    primary key (team_id, user_id),
    created_at timestamptz not null default now(),
    deleted_at timestamptz,
    role user_role not null default 'member'
);
alter table team_user enable row level security;

/*
 * RLS Policies
 */
-- Helper functions
create or replace function is_deleted(ts timestamptz)
returns boolean
language sql
security definer
as $$
    -- Deleted if deleted_at is more than 1s ago
    select extract(epoch from now() - ts) > 1 and ts is not null;
$$
;

create or replace function user_id()
returns uuid
language sql
security definer
as $$
    select id
    from public."user" as u
    where u.user_id = auth.uid();
$$
;

create or replace function team_ids()
returns setof uuid
language sql
security definer
as $$
    select team_id
    from public.team_user as tu
    where tu.user_id = user_id();
$$
;

create or replace function user_is_team_admin(check_team_id uuid, check_user_id uuid default null)
returns boolean
language sql
security definer
as $$
    select exists(
        select 1
        from public.team_user as tu
        where
            tu.team_id = check_team_id
            and tu.user_id = coalesce(check_user_id, public.user_id())
            and tu.role = 'admin'
    );
$$
;

-- RLS creation functions
create schema if not exists rls;
grant usage
on schema rls
to authenticated
;

create or replace procedure
    rls.create_rls_select_policy(
        schema_name text,
        table_name text,
        using_expression text,
        "column" text default 'id',
        column_type text default 'uuid'
    )
language plpgsql
as $$
declare
  policy_name text;
begin
  -- Create ID return function
  execute format(
    $function$ 
    create or replace function rls.can_read_%s_using()
    returns setof %s
    security definer
    language sql
    as $q$
        select %s
        from %I.%I
        where (%s)
    $q$;
    $function$,
    table_name,
    column_type,
    "column",
    schema_name,
    table_name,
    using_expression
  );

  -- Create policy
  policy_name := format('select: %s.%s', schema_name, table_name);
  execute format(
    'drop policy if exists %I on %I.%I',
    policy_name,
    schema_name,
    table_name
  );
  execute format(
    $policy$
    create policy %I
    on %I.%I
    for select
    to authenticated
    using (%s)
    $policy$,
    policy_name,
    schema_name,
    table_name,
    using_expression
  );
end;
$$
;

create or replace procedure
    rls.create_rls_insert_policy(
        schema_name text,
        table_name text,
        with_check_expression text
    )
language plpgsql
as $$
declare
  policy_name text;
begin
  -- Create policy
  policy_name := format('insert: %s.%s', schema_name, table_name);
  execute format(
    'drop policy if exists %I on %I.%I',
    policy_name,
    schema_name,
    table_name
  );
  execute format(
    $policy$
    create policy %I
    on %I.%I
    for insert
    to authenticated
    with check (%s)
    $policy$,
    policy_name,
    schema_name,
    table_name,
    with_check_expression
  );
end;
$$
;

create or replace procedure
    rls.create_rls_update_policy(
        schema_name text,
        table_name text,
        using_expression text,
        with_check_expression text,
        "column" text default 'id',
        column_type text default 'uuid'
    )
language plpgsql
as $$
declare
  policy_name text;
begin
  -- Create ID return function
  execute format(
    $function$ 
    create or replace function rls.can_update_%s_using()
    returns setof %s
    security definer
    language sql
    as $q$
        select %s
        from %I.%I
        where (%s)
    $q$;
    $function$,
    table_name,
    column_type,
    "column",
    schema_name,
    table_name,
    using_expression
  );

  -- Create policy
  policy_name := format('update: %s.%s', schema_name, table_name);
  execute format(
    'drop policy if exists %I on %I.%I',
    policy_name,
    schema_name,
    table_name
  );
  execute format(
    $policy$
    create policy %I
    on %I.%I
    for update
    to authenticated
    using (%s)
    with check (%s)
    $policy$,
    policy_name,
    schema_name,
    table_name,
    using_expression,
    with_check_expression
  );
end;
$$
;

-- user
create or replace function can_read_user_using(u "user")
returns boolean
security definer
language sql
as $$
    select ( -- User is self
        auth.uid() = u.user_id
        and not is_deleted(u.deleted_at)
    ) or ( -- User in same team
        u.id in (
            select tu.user_id
            from public.team_user as tu
            where tu.team_id in (select * from public.team_ids())
                and not is_deleted(tu.deleted_at)
        )
        and not is_deleted(u.deleted_at)
    );
$$
;

create or replace function can_update_user_using(u "user")
returns boolean
security definer
language sql
as $$
    select ( -- User is self
        auth.uid() = u.user_id
        and not is_deleted(u.deleted_at)
    );
$$
;

create or replace function can_update_user_with_check(u "user")
returns boolean
security definer
language sql
as $$
    select ( -- User is self
        auth.uid() = u.user_id
        and not is_deleted(u.deleted_at)
    );
$$
;

create policy "user: select"
on "user"
for select
to authenticated
using (can_read_user_using("user"));

create policy "user: update"
on "user"
for update
to authenticated
using (can_update_user_using("user"))
with check (can_update_user_with_check("user"));

-- team_user
create or replace function can_read_team_user_using(tu team_user)
returns boolean
security definer
language sql
as $$
    select ( -- User is self
        auth.uid() = tu.user_id
        and not is_deleted(tu.deleted_at)
    ) or ( -- User in same team
        tu.team_id in (select * from public.team_ids())
        and not is_deleted(tu.deleted_at)
    );
$$
;

create or replace function can_update_team_user_using(tu team_user)
returns boolean
security definer
language sql
as $$
    select ( -- User is self
        auth.uid() = tu.user_id
        and not is_deleted(tu.deleted_at)
    ) or ( -- User is admin of team
        public.user_is_team_admin(tu.team_id)
        and not is_deleted(tu.deleted_at)
    );
$$
;

create or replace function can_update_team_user_with_check(tu team_user)
returns boolean
security definer
language sql
as $$
    select ( -- User is self
        auth.uid() = tu.user_id
    ) or ( -- User is admin of team
        public.user_is_team_admin(tu.team_id)
    );
$$
;

create or replace function can_insert_team_user_with_check(tu team_user)
returns boolean
security definer
language sql
as $$
    select ( -- User is admin of team
        public.user_is_team_admin(tu.team_id)
        and not is_deleted(tu.deleted_at)
    );
$$
;

create policy "team_user: select"
on team_user
for select
to authenticated
using (can_read_team_user_using(team_user));

create policy "team_user: update"
on team_user
for update
to authenticated
using (can_update_team_user_using(team_user))
with check (can_update_team_user_with_check(team_user));

create policy "team_user: insert"
on team_user
for insert
to authenticated
with check (can_insert_team_user_with_check(team_user));

-- team
create or replace function can_read_team_using(t team)
returns boolean
security definer
language sql
as $$
    select ( -- User is member of team
        t.id in (select * from public.team_ids())
        and not is_deleted(t.deleted_at)
    );
$$
;

create or replace function can_update_team_using(t team)
returns boolean
security definer
language sql
as $$
    select ( -- User is admin of team
        public.user_is_team_admin(t.id)
        and not is_deleted(t.deleted_at)
    );
$$
;

create or replace function can_update_team_with_check(t team)
returns boolean
security definer
language sql
as $$
    select ( -- User is admin of team
        public.user_is_team_admin(t.id)
    );
$$
;

create or replace function can_insert_team_with_check(t team)
returns boolean
security definer
language sql
as $$
    select ( -- User is admin of team
        public.user_is_team_admin(t.id)
        and not is_deleted(t.deleted_at)
    );
$$
;

create policy "team: select"
on team
for select
to authenticated
using (can_read_team_using(team));

create policy "team: update"
on team
for update
to authenticated
using (can_update_team_using(team))
with check (can_update_team_with_check(team));

create policy "team: insert"
on team
for insert
to authenticated
with check (can_insert_team_with_check(team));
