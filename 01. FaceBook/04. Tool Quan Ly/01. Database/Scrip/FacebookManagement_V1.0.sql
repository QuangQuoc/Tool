Create table Account 
(
	ID int,
    Status boolean default false,
    UserName varchar(255) Not null,
    UserId varchar(255),
    PassWord varchar(255) Not null,
    CreatedDate date
);

Create table Cookies
(
	Id int,
    Status boolean default false,
    Data varchar(65535),
    AccountId int
);

create table NewFeedHistory 
(
	Id int,
    AccountId int,
    RunTime datetime
);

create table AddFriendHistory(
	Id int,
    AccountId int,
    AddTime datetime,
    AddFriendTypeId int
);

create table AddFriendType 
(
	Id int,
    Type Text(255)
);

create table Regulations
(
	Id int,
    ActionId int,
    TimesOfDay int,
    WorkingTime text(1024),
    Priority int,
    LimitedTime datetime
);

Create table Action
(
	Id int,
    Action Text(255)
);


ALTER DATABASE FacebookManagement CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

ALTER TABLE AddFriendType CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

ALTER TABLE table_name CHANGE column_name column_name VARCHAR(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

