drop table if exists users;
create table users(
	id integer primary key autoincrement,
	username text not null,
	passwd text not null
);

insert into users (username,passwd) values ('myoung','lfy123'),('ShadowGlint','lfy321');