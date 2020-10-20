CREATE TABLE Athlete (
  id            INT NOT NULL PRIMARY KEY,
  card_number   INT NOT NULL UNIQUE,
  name          TEXT NOT NULL,
  gender        TEXT NOT NULL,
  height        INT NOT NULL CHECK(height >= 0 AND height <= 300), 
  weight        INT NOT NULL CHECK(weight >= 0 AND weight <= 200), 
  age           INT NOT NULL CHECK(age > 0 AND age <= 150), 
  delegation_id INT UNIQUE REFERENCES Delegation(id),
  address_id    INT REFERENCES Address(id),
  volonteer_id  INT NOT NULL REFERENCES Volunteer(id)
)
CREATE TABLE Delegation	(
  id            INT NOT NULL PRIMARY KEY,
  manager_id    INT NOT NULL REFERENCES Manager(id),
  address_id    INT NOT NULL REFERENCES Address(id)
)
CREATE TABLE Manager (
  id            INT NOT NULL PRIMARY KEY,
  name          TEXT NOT NULL ,
  phone         TEXT NOT NULL	
)	
CREATE TABLE Facility (
  id            INT NOT NULL PRIMARY KEY,
  address_id    INT NOT NULL REFERENCES Address(id),
  type          NOT NULL VARHAR(20)
  name          TEXT,
)	
	
CREATE TABLE Address(
  id            INT NOT NULL PRIMARY KEY,
  street        TEXT NOT NULL, 
  house         TEXT NOT NULL
)

CREATE TABLE IF NOT EXISTS Volunteer(
  id           SERIAL PRIMARY KEY,
  card_numbrer INT NOT NULL UNIQUE,
  first_name   VARCHAR(200) NOT NULL,
  second_name  VARCHAR(200) NOT NULL,
  phone        VARCHAR(11) NOT NULL CHECK(phone ~ '^[0-9 ]*$'),
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