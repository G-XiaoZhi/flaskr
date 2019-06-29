DROP TABLE IF EXISTS entries;
create table entries (
id integer primary key autoincrement,
title varchar(64) not null,
content text not null,
create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);