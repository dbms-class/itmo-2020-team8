-- part1

-- Таблица адресов всех зданий
CREATE TABLE Building(
  id            SERIAL PRIMARY KEY,
  -- идентификатор здания
  street        TEXT NOT NULL,
  -- улица
  house         TEXT NOT NULL
  -- дом
);

--Таблица обьектов, расположеных на територии
CREATE TABLE Facility (
  id            SERIAL PRIMARY KEY,
  -- идентификатор обьекта
  building_id    INT NOT NULL REFERENCES Building(id),
  -- идентификатор адреса обьекта
  type          VARCHAR(20) NOT NULL,
  --  функциональное предназначение
  name          TEXT
  -- опциональное название
)	;

-- руководители делегаций
CREATE TABLE Manager (
  id            SERIAL PRIMARY KEY,
  -- идентификатор руководителя
  name          TEXT NOT NULL ,
  -- имя руководителя
  phone         TEXT NOT NULL CHECK(phone ~ '^[0-9]*$')
  -- телефон
);

--Таблица национальных делегаций
CREATE TABLE Delegation	(
  id            SERIAL PRIMARY KEY,
  -- идентификатор делегации
  manager_id    INT NOT NULL REFERENCES Manager(id),
  -- идентификатор руководителя делегации, по нему узнаем данные менеджера
  address_id    INT NOT NULL REFERENCES Facility(id),
  -- идентификатор обьекта в котором расположен штаб, здание где находится штаб
  country       TEXT 
  -- название страны из которой прибыла делегация
);

-- Таблица участников соревнований
CREATE TABLE Athlete (
  id            INT PRIMARY KEY,
  -- карточка с уникальным номером
  name          TEXT NOT NULL,
  -- имя участника
  gender        TEXT NOT NULL,
  -- пол участника
  height        INT NOT NULL CHECK(height >= 0 AND height <= 300),
  -- рост участника
  weight        INT NOT NULL CHECK(weight >= 0 AND weight <= 200),
  -- вес участника
  age           INT NOT NULL CHECK(age > 0 AND age <= 150),
  -- возраст участника
  delegation_id INT REFERENCES Delegation(id),
  -- идентификатор делигации, у каждого участника должна быть делегация, а из делегации можно восстановить кто руководитель этого спортсмена
  address_id    INT REFERENCES Building(id),
  -- идентификатор здания в котором живет участник, можем узнать здание
  volonteer_id  INT NOT NULL REFERENCES Volunteer(id)
  -- идентификатор прикрепленного волонтера, можем узнать кто прикреплен к участнику
);


-- part2

-- Таблица: спортсмены, отображает множество спортсменов на спортивные дисциплины, в которых они участвуют в соревнованиях
create table Sportsman (
  -- спортсмен
  athlete_id int not null references Athlete(id),
  -- спортивная дисциплина в которых данный спорсмен участвует
  sport_id int not null references Sport(id)
);

-- Таблица: соревнование
create table Competition (
  id serial primary key,
  -- название соревнования, причем 2 соревнований с одинаковым именем не существует
  name text not null UNIQUE,
  -- дата проведения соревнования
  -- в одно и тоже время не может проводиться 2 соревнования
  date date not null UNIQUE,
  -- место проведения соревнования
  facility_id int not null references Facility(id),
  -- название спортивной дисциплины по которому проводиться данное соревнование
  sport_id int not null references Sport(id)
);


--Таблица: Медали
create table Medal (
    -- спортсмен, получивший медаль
  athlete_id int not null references Athlete(id),
  -- соревнование
  competition_id int not null references Competition(id),
  -- номинал медали
  value int not null check ( value >= 1 AND  value <= 3),
  -- спортивная дисциплина
  sport_id int not null references Sport(id),
  -- спортсмен не может получить 2 медали за одно соревнование
  UNIQUE(athlete_id, competition_id)
);

-- Справочник
create table Sport (
  id serial primary key,
  --name - представляет название спортивной дисциплины
  name text not null UNIQUE
);

-- Площадки для проведения соревнований по дисциплинам
create table Area (
  -- соревнование
  sport_id int not null references Sport(id),
  -- площадка
  facility_id int not null references Facility(id)
);

-- Таблица: Участники соревнований
create table Participant (
  -- спортсмен, который участвует в соревновании competition_id
  athlete_id int references Athlete(id),
  -- волонтер, приглашенный на соревнование
  volunteer_id int references Volunteer(id),
  -- соревнование на которое собрались участники
  competition_id int references Competition(id) not null,
  -- информация о том, является ли участник соревнования спортсменом
  is_athlete bool not null,
  CHECK ( (is_athlete and volunteer_id is null) or (not is_athlete and volunteer_id is not null))
  -- не хотим, чтобы был добавлен
);



-- part3

-- Таблица с информацией по волонтерам
CREATE TABLE IF NOT EXISTS Volunteer(
  id           INT PRIMARY KEY,                                 -- номер карточки волонтера, чтобы он был уникально идентифицирован и связан с атлетами
  name         TEXT NOT NULL CHECK(name != ''),                          -- имя волонтера, оно не должно быть пустым
  phone        VARCHAR(11) NOT NULL UNIQUE CHECK(phone ~ '^[0-9]*$')    -- номер телефона волонтера, регулярка для того, чтобы была, она допускает довольно интересные телефонные номера
);

-- Таблица транспортных средств для спортсменов и всех всех
CREATE TABLE IF NOT EXISTS Transport(
  id         VARCHAR(10) UNIQUE PRIMARY KEY,    -- регистрационный номер ТС (возможно сделать это ключом, потому что это уникальная штука, если номера не перевешивают)
  capacity   INT NOT NULL DEFAULT 0 CHECK(capacity > 0)  -- вместимость человеков в ТС
);

-- Таблица задач для волонтеров
CREATE TABLE IF NOT EXISTS VolunteerTask(
  id           SERIAL PRIMARY KEY,                       -- идентификатор задачи волонтера, чтобы их можно было идентифицировать уникально
  volunteer_id int NOT NULL REFERENCES Volunteer(id),        -- идентификатор волонтера, который на задаче, чтобы задача не могла существовать без исполнителя-волонтера
  transport_id int DEFAULT NULL REFERENCES Transport(id),    -- идентификатор ТС(но его может не быть поэтому по дефолту мы ставим туда NULL), потому что к задаче может быть привязана ТС
  datetime     TIMESTAMPTZ NOT NULL ,                     -- время дата выдачи задачи(должна по идее быть автогенерированной на момент записи)
  description  TEXT NOT NULL            -- описание задачи для волонтера(по умолчанию будет пустым)
);

