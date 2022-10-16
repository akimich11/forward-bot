create sequence queue_id_seq
    as integer;

create sequence user_queue_id_seq
    as integer;

create sequence poll_option_id_seq
    as integer;

create sequence user_vote_id_seq
    as integer;

create table departments
(
    id      integer not null
        constraint department_pk
            primary key,
    chat_id integer,
    name    text


);


create table polls
(
    id            char(50) not null
        constraint poll_pk
            primary key,
    department_id integer
        constraint poll_department_id_fk
            references departments
            on update cascade on delete cascade,
    question      text,
    created_at    timestamp
);

create table users
(
    id             integer not null
        constraint user_pk
            primary key,

    first_name     text,
    last_name      varchar(20),
    department_id  integer
        constraint user_department_id_fk
            references departments
            on update cascade on delete cascade,
    sub_department char(3),
    is_admin       smallint,
    skips_month    integer,
    skips_semester integer,
    birthday       timestamp
);

create unique index user_last_name_uindex
    on users (last_name);

create table queues
(
    id            integer default nextval('queue_id_seq'::regclass) not null
        constraint queue_pk
            primary key,
    department_id integer
        constraint queue_department_id_fk
            references departments
            on update cascade on delete cascade,
    name          text,
    is_last       smallint
);

alter sequence queue_id_seq owned by queues.id;

create table scheduled_polls
(
    id            integer not null
        constraint poll_schedule_pk
            primary key,
    department_id integer
        constraint poll_schedule_department_id_fk
            references departments
            on update cascade on delete cascade,
    question      text,
    is_multi      smallint,
    weekday       char(9),
    utc_time      timestamp
);

create table poll_options
(
    id      integer default nextval('poll_option_id_seq'::regclass) not null
        constraint poll_option_pk
            primary key,
    poll_id char(50)
        constraint poll_option_poll_id_fk
            references polls
            on update cascade on delete cascade,
    text    text
);

alter sequence poll_option_id_seq owned by poll_options.id;

create table queue_positions
(
    id       integer default nextval('user_queue_id_seq'::regclass) not null
        constraint user_queue_pk
            primary key,
    user_id  integer
        constraint user_queue_user_id_fk
            references users
            on update cascade on delete cascade,
    queue_id integer
        constraint user_queue_queue_id_fk
            references queues
            on update cascade on delete cascade,
    position integer
);

alter sequence user_queue_id_seq owned by queue_positions.id;

create table users_poll_options
(
    id        integer default nextval('user_vote_id_seq'::regclass) not null
        constraint user_vote_pk
            primary key,
    user_id   integer
        constraint user_vote_user_id_fk
            references users
            on update cascade on delete cascade,
    option_id integer
        constraint user_vote_poll_option_id_fk
            references poll_options
            on update cascade on delete cascade
);

alter sequence user_vote_id_seq owned by users_poll_options.id;

create table timetables
(
    id             serial
        constraint timetables_pk
            primary key,
    department_id  integer
        constraint timetables_departments_id_fk
            references departments
            on update cascade on delete cascade,
    sub_department varchar(255) default NULL::character varying,
    weekday        varchar(255),
    start_time     time,
    subject        varchar(255),
    auditory       varchar(255),
    type           char
);
