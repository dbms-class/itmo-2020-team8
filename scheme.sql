-- part1 
CREATE TABLE Athlete (
  id           SERIAL PRIMARY KEY,
  card_number   INT NOT NULL UNIQUE,
  name          TEXT NOT NULL,
  gender        TEXT NOT NULL,
  height        INT NOT NULL CHECK(height >= 0 AND height <= 300), 
  weight        INT NOT NULL CHECK(weight >= 0 AND weight <= 200), 
  age           INT NOT NULL CHECK(age > 0 AND age <= 150), 
  delegation_id INT UNIQUE REFERENCES Delegation(id),
  address_id    INT REFERENCES Address(id),
  volonteer_id  INT NOT NULL REFERENCES Volunteer(id)
);
CREATE TABLE Delegation	(
  id            SERIAL PRIMARY KEY,
  manager_id    INT NOT NULL REFERENCES Manager(id),
  address_id    INT NOT NULL REFERENCES Address(id)
);
CREATE TABLE Manager (
  id            SERIAL PRIMARY KEY,
  name          TEXT NOT NULL ,
  phone         TEXT NOT NULL CHECK(phone ~ '^[0-9]*$')
)	;
CREATE TABLE Facility (
  id            SERIAL PRIMARY KEY,
  address_id    INT NOT NULL REFERENCES Address(id),
  type          NOT NULL VARHAR(20)
  name          TEXT,
)	;
	
CREATE TABLE Address(
  id            SERIAL PRIMARY KEY,
  street        TEXT NOT NULL, 
  house         TEXT NOT NULL
);
-- part2

create table Sportsmans ( 
  athlete_id int not null references Athlete,
  sport_id int not null references Sport
);


create table Competition (
  id serial primary key,
  name text not null UNIQUE,
  date date not null,
  facility_id int not null references Facility(id)
);

create table Medal (
  athlete_id int not null references Athlete(id),
  competition_id int not null references Competition(id),
  value int not null check ( value >= 1 AND  value <= 3),
  sport_id int not null references Sport(id)
);

create table Sport (
  id serial primary key,
  name text not null UNIQUE
);

create table Area (
  sport_id int not null references Sport(id),
  facility_id int not null references Facility(id)
);

create table Participant (
  athlete_id int references Athlete,
  volunteer_id int references Volunteer,
  competition_id int references Competition not null,
  is_athlete bool not null,
  CHECK ( (is_athlete and volunteer_id is null) || (not is_athlete and volunteer_id is not null))
);
-- part3 
CREATE TABLE IF NOT EXISTS Volunteer(
  id           SERIAL PRIMARY KEY,
  card_numbrer INT NOT NULL UNIQUE,
  name         TEXT NOT NULL,
  phone        VARCHAR(11) NOT NULL CHECK(phone ~ '^[0-9]*$'),
);

CREATE TABLE IF NOT EXISTS VolunteerTask(
  id           SERIAL PRIMARY KEY,
  volunteer_id NOT NULL REFERENCES Volunteer(id),
  transport_id NOT NULL REFERENCES Trasnport(id),
  datetime     NOT NULL TIMESTAMPTZ,
  description  TEXT DEFAULT ""
);

CREATE TABLE IF NOT EXISTS Transport(
  id SERIAL  PRIMARY KEY,
  reg_number VARCHAR(10) NOT NULL,
  capacity   INT NOT NULL DEFAULT 0 CHECK(capacity >= 0)
);