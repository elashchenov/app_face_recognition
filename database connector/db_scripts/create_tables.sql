--create table device
CREATE TABLE IF NOT EXISTS public.device (
    id         bigserial primary key,
    name       varchar(500) not null
);
commit;

--create table users
CREATE TABLE IF NOT EXISTS public.users (
    id         bigserial primary key,
    name       varchar(500) not null,
    surname    varchar(500) not null,
    username   varchar(500) not null,
    email      varchar(500) not null,
    password   varchar(500) not null,
    device_id  integer not null,
    constraint fk_device foreign key (device_id) references public.device(id) on delete cascade
);
commit;

--create table journal
CREATE TABLE IF NOT EXISTS public.journal (
    id         bigserial primary key,
    user_id    integer not null,
    date_login date not null,
    constraint fk_user foreign key (user_id) references public.users(id) on delete cascade
);
commit;

--create table photos
CREATE TABLE IF NOT EXISTS public.photos (
    id         bigserial primary key,
    image      bytea NOT null,
    user_id    integer not null,
    constraint fk_user foreign key (user_id) references public.users(id) on delete cascade
);
commit;