from psycopg2 import pool
import psycopg2 as pg_driver

pgpool = pool.SimpleConnectionPool(1, 20,
                                   user='postgres',
                                   password="lj,hsqpostgresql",
                                   host='127.0.0.1',
                                   port='5432',
                                   database='postgres'
                                   )



def all_volunteers():
    db = pgpool.getconn()
    try:
        cur = db.cursor()
        cur.execute('SELECT id FROM Volunteer')
        result = []
        for p in cur.fetchall():
            result.append(Volunteer(p[0]))
        return result
    finally:
        pgpool.putconn(db)


class Volunteer:
    def __init__(self, id):
        self.id = id


    def name(self):
        db = pgpool.getconn()
        try:
            cur = db.cursor()
            cur.execute(f"SELECT name FROM Volunteer WHERE id={self.id}")
            return cur.fetchone()[0]
        finally:
            pgpool.putconn(db)


def all_athletes():
    db = pgpool.getconn()
    try:
        cur = db.cursor()
        cur.execute('SELECT id FROM Athletes')
        result = []
        for p in cur.fetchall():
            result.append(Athlete(p[0]))
        return result
    finally:
        pgpool.putconn(db)


def get_country_id(cursor, country_name):
    cursor.execute(f"SELECT id from Countries where name={country_name}")
    res = []
    countries = cursor.fetchall()
    for c in countries:
        res.append(c[0])
    if len(countries) == 0:
        return None
    return res[0]


def is_number(string):
    try:
        val = int(string)
        return True
    except ValueError:
        return False

def register_athletes(sportsman, country, volonteer_id):
    db = pgpool.getconn()
    try:
        cur = db.cursor()
        country_id = get_country_id(cur, country)
        if country_id is None:
            return False
        if is_number(sportsman):
            # спортсмен с sportsman_id уже существует в базе данных
            # поэтому обновим значения country и volonteer_id у спортсмена с идентификатором sportsman_id
            sportsman_id = int(sportsman)
            print("Before", sportsman_id, country_id,  volonteer_id)
            cur.execute(f"""UPDATE Athletes SET country_id={country_id}, 
                                                volonteer_id={volonteer_id} 
                                            WHERE id={sportsman_id}""")
            db.commit()
            return cur.rowcount == 1
        elif isinstance(sportsman, str):
            name_sportsman = sportsman
            # спортсмена с именем name_sportsman в базе данных нет
            # поэтому добавим его в таблицу
            cur.execute(f"""INSERT INTO Athletes (name, country_id, volonteer_id) values 
                        ({name_sportsman}, {country_id}, {volonteer_id})""")
            db.commit()
            return cur.rowcount == 1
        else:
            return False
    finally:
        pgpool.putconn(db)


class Athlete:
    def __init__(self, id):
        self.id = id

    def name(self):
        db = pgpool.getconn()
        try:
            cur = db.cursor()
            cur.execute(f"SELECT name FROM Athletes WHERE id={self.id}")
            return cur.fetchone()[0]
        finally:
            pgpool.putconn(db)

