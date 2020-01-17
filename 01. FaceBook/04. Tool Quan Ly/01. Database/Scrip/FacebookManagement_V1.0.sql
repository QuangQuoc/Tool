Create table Accounts 
(
	ID int NOT NULL,
    Status boolean default false,
    UserName varchar(255) Not null,
    UserId varchar(255),
    PassWord varchar(255) Not null,
    CreatedDate date
);

Create table Cookies
(
	ID int,
    Status boolean default false,
    Data Text(65535),
    AccountId int,
    PRIMARY KEY (Id),
    FOREIGN KEY (AccountId) REFERENCES Account(ID)
);

create table NewFeedHistory 
(
	ID int,
    AccountId int,
    RunTime datetime
);

create table AddFriendHistory
(
	ID int,
    AccountId int,
    AddTime datetime,
    AddFriendTypeId int
);

create table AddFriendType 
(
	Id int,
    KiHieu Varchar(255),
    Ten Text(255)
);

create table Regulation
(
	Id int,
    ActionId int,
    TimesOfDay int,
    WorkingTime text(1024),
    Priority int,
    LimitedTime datetime
);

Create table Groups
(
	ID int,
    Topic text(1024),
    Status boolean default false,
    Name text(1024),
    Quality int,
    Type int
);

Create table AccountGroup
(
	ID int,
    GroupId int,
    UserId int,
    Status int,
    RequestTime Datetime
);

Create table Action
(
	Id int,
    Action Text(255)
);


ALTER DATABASE FacebookManagement CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

ALTER TABLE Account CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# PRIMARY KEY
ALTER TABLE Accounts
ADD PRIMARY KEY (ID);

ALTER TABLE Cookies
ADD PRIMARY KEY (ID);

ALTER TABLE NewFeedHistory
ADD PRIMARY KEY (ID);

ALTER TABLE AddFriendHistory
ADD PRIMARY KEY (ID);

ALTER TABLE Regulation
ADD PRIMARY KEY (ID);

ALTER TABLE Groups
ADD PRIMARY KEY (ID);

ALTER TABLE AccountGroup
ADD PRIMARY KEY (ID);

ALTER TABLE Action
ADD PRIMARY KEY (ID);



#ALTER TABLE table_name CHANGE column_name column_name VARCHAR(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

