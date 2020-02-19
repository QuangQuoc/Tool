CREATE DATABASE IF NOT exists InstagramDb character set 'utf8' collate 'utf8_unicode_ci';
use InstagramDb;
create table if not exists Account(
	Id Int auto_increment,
	UserName varchar(255) not null,
    Password varchar(255) not null,
    primary key (Id)
);

create table if not exists Follower(
	Id int auto_increment,
    UserName varchar(255) not null,
    HashTagId int null,
    primary key (Id)
);

create table if not exists Follow(
	Id int auto_increment,
    AccountId int not null,
    FollowerId int not null,
    Status bool default true,
    FollowDate Date null,
    UnFollowDate Date null,
    primary key (Id)
);

create table if not exists HashTag(
	Id int auto_increment,
    Name varchar(255) not null,
    ChuDe Text null,
    primary key (Id)
);
