# itmo-2020-team8

# 1 
CREATE TABLE Athlete (
  id            INT NOT NULL PRIMARY KEY,
  card_number   INT NOT NULL UNIQUE,
  name          TEXT NOT NULL,
  gender        TEXT NOT NULL,
  height        INT, 
  weight        INT NOT NULL CHECK(weight >= 0 AND), 
  age           INT, 
  delegation_id INT UNIQUE REFERENCES Delegation(id),
  address_id    INT REFERENCES Adress(id),
  volonteer_id  INT NOT NULL REFERENCES Volunteer(id)
}
CREATE TABLE Delegation	{
  id            INT   NOT NULL PRIMARY KEY,
  manager_id    INT   NOT NULL,
  address_id    INT
}
CREATE TABLE Manager {
  id            INT   NOT NULL PRIMARY KEY,
  name          TEXT  NOT NULL ,
  phone         TEXT  NOT NULL	
}		
CREATE TABLE Facility {
  id            INT   NOT NULL PRIMARY KEY,
  address_id    INT  NOT NULLT,
  type          NOT NULL VARHAR(20)
  name          TEXT  NOT NULL,
}	
	
CREATE TABLE Adress{
  - адрес_id
  - улица	
  - дом	
}







# 2 

Соревнование(
  id
  название
  дата
  время
  объект
)

Cписки людей на соревнованании(
  id соревнованания
  id спортсмена/волонтера?
)

Медаль(
  спортсмен
  id соревнование
  номинал медали
)

Площадки(
  спорт
  объект
)


---- 

# 3 Volunteers

CREATE TABLE IF NOT EXISTS Volunteer(
 id           SERIAL PRIMARY KEY,
 card_numbrer INT NOT NULL UNIQUE, 
 name         VARCHAR(200) NOT NULL,
 phone        VARCHAR(11) NOT NULL,
);

CREATE TABLE IF NOT EXISTS VolunteerTask(
 id           SERIAL PRIMARY KEY,
 volunteer_id NOT NULL REFERENCES Volunteer(id),
 transport_id NOT NULL REFERENCES Trasnport(id), 
 datetime     TIMESTAMPTZ,
 description  TEXT DEFAULT ""
);

CREATE TABLE IF NOT EXISTS Transport(
 id         SERIAL PRIMARY KEY,
 reg_number NOT NULL VARHAR(10),
 capacity   INT NOT NULL DEFAULT 0 CHECK(capacity >= 0)
);