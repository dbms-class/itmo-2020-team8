-- part1
-- Таблица адресов всех зданий
CREATE TABLE Address(
  -- улица
  street        TEXT NOT NULL,
  -- дом
  house         INT NOT NULL,
  -- ключ-пара
  primary key (street, house)
);

CREATE TYPE BuildingType AS ENUM (
 'жилой дом',
 'административное здание'
 'бассеин',
 'столовая'
 'спортивная площадка'
 );

-- Таблица обьектов, расположеных на територи
CREATE TABLE Facility (
  -- идентификатор адреса обьекта
  id            SERIAL PRIMARY KEY,
  --  функциональное предназначение
  type          BuildingType,
  -- опциональное название
  name          TEXT,
  -- улица
  street        TEXT NOT NULL,
  -- дом
  house         INT NOT NULL,
  FOREIGN KEY (street, house) REFERENCES Address(street, house)
)	;

-- Таблица руководителей делегаций
CREATE TABLE Manager (
  -- идентификатор руководителя
  id SERIAL PRIMARY KEY,
  -- имя руководителя
  name          TEXT NOT NULL ,
  -- телефон
  phone         TEXT NOT NULL
);

-- Таблица национальных делегаций
CREATE TABLE Delegation	(
  -- идентификатор делегации
  id            SERIAL PRIMARY KEY,
  -- идентификатор руководителя делегации, по нему узнаем данные менеджера
  manager_id    INT UNIQUE NOT NULL REFERENCES Manager(id),
  -- идентификатор обьекта в котором расположен штаб, здание где находится штаб
  address_id    INT NOT NULL REFERENCES Facility(id),
  -- название страны из которой прибыла делегация
  country       TEXT NOT NULL
);

CREATE TYPE GenderType AS ENUM (
 'male',
 'female'
);

-- Таблица с информацией по волонтерам
CREATE TABLE IF NOT EXISTS Volunteer(
  id           serial PRIMARY KEY,                                 -- номер карточки волонтера, чтобы он был уникально идентифицирован и связан с атлетами
  name         TEXT NOT NULL CHECK(name != ''),                          -- имя волонтера, оно не должно быть пустым
  phone        VARCHAR(11) NOT NULL UNIQUE     -- номер телефона волонтера, регулярка для того, чтобы была, она допускает довольно интересные телефонные номера
);

-- Таблица участников соревнований
CREATE TABLE Athletes (
  -- карточка с уникальным номером
  id            serial PRIMARY KEY,
  -- имя участника
  name          TEXT NOT NULL,
  -- пол участника
  gender        GenderType,
  -- рост участника
  height        INT CHECK(height >= 0 AND height <= 300),
  -- вес участника
  weight        INT CHECK(weight >= 0 AND weight <= 400),
  -- возраст участника
  age           INT  CHECK(age > 0 AND age <= 150),
  -- идентификатор делигации, у каждого участника должна быть делегация, а из делегации можно восстановить кто руководитель этого спортсмена
  delegation_id INT NOT NULL REFERENCES Delegation(id),
  -- идентификатор прикрепленного волонтера, можем узнать кто прикреплен к участнику
  volonteer_id  INT NOT NULL REFERENCES Volunteer(id),
  -- улица
  street        TEXT,
  -- дом
  house         INT,
  FOREIGN KEY (street, house) REFERENCES Address(street, house)
);

-- part2

-- Справочник
create table Sport (
  id serial primary key,
  -- name - представляет название спортивной дисциплины
  name VARCHAR(200) not null UNIQUE
);

-- Таблица: соревнование
create table Competition (
  id serial primary key,
  -- название соревнования, причем 2 соревнований с одинаковым именем не существует
  name VARCHAR(100) not null,
  -- дата проведения соревнования
  day timestamp not null,
  -- место проведения соревнования
  facility_id int not null references Facility(id),
  -- название спортивной дисциплины по которому проводиться данное соревнование
  sport_id int not null references Sport(id),
  -- в одно время в одном здании не могут проводиться несколько соревнований
  UNIQUE (day, facility_id)
);

-- Таблица: Медали
create table Medal (
    -- спортсмен, получивший медаль
  Athletes_id int not null references Athletes(id),
  -- соревнование
  competition_id int not null references Competition(id),
  -- номинал медали
  value int not null check ( value >= 1 AND  value <= 3),
  -- спортсмен не может получить 2 медали за одно соревнование
  UNIQUE(Athletes_id, competition_id)
);


-- Таблица: спортсмены, отображает множество спортсменов на спортивные дисциплины, в которых они участвуют в соревнованиях
create table Athletes_Sport (
  -- спортсмен
  Athletes_id int not null references Athletes(id),
  -- спортивная дисциплина в которых данный спорсмен участвует
  sport_id int not null references Sport(id)
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
  Athletes_id int references Athletes(id),
  -- соревнование на которое собрались участники
  competition_id int not null references Competition(id)
);



-- part3

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
  datetime     timestamp NOT NULL,                     -- время дата выдачи задачи(должна по идее быть автогенерированной на момент записи)
  description  TEXT NOT NULL            -- описание задачи для волонтера(по умолчанию будет пустым)
);

