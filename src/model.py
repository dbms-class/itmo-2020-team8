from functools import partial
import random
from src.webapp import global_pool


def all_volunteers():
    db = global_pool.getconn()
    try:
        cur = db.cursor()
        cur.execute('SELECT id FROM Volunteer')
        result = []
        for p in cur.fetchall():
            result.append(Volunteer(p[0]))
        return result
    finally:
        global_pool.putconn(db)


class Volunteer:
    def __init__(self, id):
        self.id = id

    def name(self):
        db = global_pool.getconn()
        try:
            cur = db.cursor()
            cur.execute(f"SELECT name FROM Volunteer WHERE id={self.id}")
            return cur.fetchone()[0]
        finally:
            global_pool.putconn(db)


def all_athletes():
    db = global_pool.getconn()
    try:
        cur = db.cursor()
        cur.execute('SELECT id FROM Athletes')
        result = []
        for p in cur.fetchall():
            result.append(Athlete(p[0]))
        return result
    finally:
        global_pool.putconn(db)


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
    db = global_pool.getconn()
    try:
        cur = db.cursor()
        country_id = get_country_id(cur, country)
        if country_id is None:
            return False
        if is_number(sportsman):
            # спортсмен с sportsman_id уже существует в базе данных
            # поэтому обновим значения country и volonteer_id у спортсмена с идентификатором sportsman_id
            sportsman_id = int(sportsman)
            print("Before", sportsman_id, country_id, volonteer_id)
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
        global_pool.putconn(db)


def check_first_cond(volonter_1, volonter_2):
    delegation_ids_1 = get_delegation_ids_by_volonter(volonter_1.id)
    delegation_ids_2 = get_delegation_ids_by_volonter(volonter_2.id)
    return len(delegation_ids_1.intersection(delegation_ids_2))


def get_volunter_tasks(volonter_id):
    db = global_pool.getconn()
    try:
        cur = db.cursor()
        cur.execute(f"""select id, datetime from volunteertask where volunteer_id={volonter_id};""")
        result = set()
        for p in cur.fetchall():
            result.add(VolunterTask(p[0]))
        return result
    finally:
        global_pool.putconn(db)


def check_second_cond(progul_task, volunter_tasks):
    for volunter_task in volunter_tasks:
        if abs(volunter_task.datetime_hours() - progul_task.datetime_hours()) > 1:
            return False
    return True


def get_count_next_tasks(from_time, volunter_tasks):
    count = 0
    for volunter_task in volunter_tasks:
        if volunter_task.datetime_hours() > from_time:
            count += 1
    return count


def assign_another_volunter(progul_id, must_assigned_volunter_tasks):
    volunter_candidates_1_level = list(filter(partial(check_first_cond, Volunteer(progul_id)),
                                              all_volunteers()))
    answ = []
    for task in must_assigned_volunter_tasks:
        volunter_candidates_2_level = []
        volunter_next_task_count = []
        for volonter in volunter_candidates_1_level:
            volunter_tasks = get_volunter_tasks(volonter.id)
            if check_second_cond(task, volunter_tasks):
                volunter_candidates_2_level.append(volonter)
                volunter_next_task_count.append(get_count_next_tasks(task.datetime_hours(), volunter_tasks))
        if len(volunter_candidates_2_level) == 0:
            raise RuntimeError(f"Not volunters for task with id = {task.id}")
        # find min count between volunters
        volunter_candidates_3_level = []
        min_count_tasks = min(volunter_next_task_count)
        for idx, volonter in enumerate(volunter_candidates_2_level):
            if volunter_next_task_count[idx] == min_count_tasks:
                volunter_candidates_3_level.append(volonter)
        # choose random candidate
        random_volonter = random.choice(volunter_candidates_3_level)
        # Todo (return named tuple)
        answ.append((task.id, random_volonter.name(), random_volonter.id))

    return answ


class VolunterTask:
    def __init__(self, id):
        self.id = id

    def datetime_hours(self):
        db = global_pool.getconn()
        try:
            cur = db.cursor()
            cur.execute(f"SELECT extract(hours from datetime) FROM volunteertask WHERE id={self.id}")
            return cur.fetchone()[0]
        finally:
            global_pool.putconn(db)


def get_delegation_ids_by_volonter(volonter_id):
    db = global_pool.getconn()
    try:
        cur = db.cursor()
        cur.execute(f"""select delegation.id from athletes Join 
                        delegation on athletes.country_id = delegation.country_id
                        where volonteer_id={volonter_id};""")
        result = set()
        for p in cur.fetchall():
            result.add(p[0])
        return result
    finally:
        global_pool.putconn(db)


class Athlete:
    def __init__(self, id):
        self.id = id

    def name(self):
        db = global_pool.getconn()
        try:
            cur = db.cursor()
            cur.execute(f"SELECT name FROM Athletes WHERE id={self.id}")
            return cur.fetchone()[0]
        finally:
            global_pool.putconn(db)
