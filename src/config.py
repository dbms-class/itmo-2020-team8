from src.model import *
from random import randint

ADDRESS_COUNT = 50
ATHLETE_COUNT = 500
VOLONTEER_COUNT = 100
TRANSPORT_COUNT = 200
VOLONTEER_TASK_COUNT = 400
COUNTRY_COUNT = 16 # TODO (IvanKozlov98) depends from function!


def wrap_str(string):
    return f'\'{string}\''


def my_insert(query):
    db = pgpool.getconn()
    try:
        cur = db.cursor()
        cur.execute(query)
        db.commit()
        return cur.rowcount
    finally:
        pgpool.putconn(db)


def add_some_countries():
    my_insert("""INSERT INTO Countries (name) VALUES ('Russia'), 
                                    ('England'),
                                    ('Holland'),
                                    ('Cameroon'),
                                    ('USA'),
                                    ('Japan'),
                                    ('China'),
                                    ('Germany'),
                                    ('France'),
                                    ('Belgium'),
                                    ('Belarus'),
                                    ('North Korea'),
                                    ('South Korea'),
                                    ('Canada'),
                                    ('Brazil'),
                                    ('Ireland');
    """)


def get_rand_num(l=1, r=10000):
    return randint(l, r)


def add_random_address(n):
    some_street = 'Some street'
    sql_query = "INSERT INTO address (street, house) VALUES "
    for idx in range(n):
        sql_query += f'({wrap_str(some_street)}, {get_rand_num()}),'
    sql_query = sql_query[:-1] + ';'

    return my_insert(sql_query)


def get_rand_phone_number(len):
    random_number = ""
    for idx in range(len):
        random_number += str(get_rand_num() % 10)
    return wrap_str(random_number)


def get_random_volonteer():
    return wrap_str(f'Volunteer{get_rand_num()}')


def add_random_volonteers(n):
    sql_query = "INSERT INTO Volunteer (name, phone) VALUES "
    for idx in range(n):
        sql_query += f'({get_random_volonteer()}, {get_rand_phone_number(11)}),'
    sql_query = sql_query[:-1] + ';'

    return my_insert(sql_query)


def get_random_name_athlete():
    return wrap_str(f'Sportsman{get_rand_num()}')


def get_random_gender():
    return wrap_str('male') if get_rand_num() % 2 else wrap_str('female')


def add_random_athletes(n):
    sql_query = "INSERT INTO athletes " \
                "(name, gender, height, weight, " \
                "age, country_id, volonteer_id, address_id) VALUES "
    for idx in range(n):
        sql_query += f'({get_random_name_athlete()}, ' \
                     f'{get_random_gender()},' \
                     f'{get_rand_num(1, 100)},' \
                     f'{get_rand_num(1, 100)},' \
                     f'{get_rand_num(1, 100)},' \
                     f'{get_rand_num(1, COUNTRY_COUNT)},' \
                     f'{get_rand_num(1, VOLONTEER_COUNT)},' \
                     f'{get_rand_num(1, ADDRESS_COUNT)}),'
    sql_query = sql_query[:-1] + ';'

    return my_insert(sql_query)


def add_some_transport(n):
    sql_query = "INSERT INTO transport (id, capacity) VALUES "
    for idx in range(n):
        sql_query += f'({str(get_rand_num(1, 1000000))}, {get_rand_num(10, 100)}),'
    sql_query = sql_query[:-1] + ';'

    return my_insert(sql_query)


def get_random_timestamp():
    return """timestamp '2014-01-10 20:00:00' + random() * (timestamp '2014-01-20 20:00:00' -
                   timestamp '2014-01-10 10:00:00')"""

def add_volonteer_tasks(n):
    sql_query = "INSERT INTO volunteertask (volunteer_id, datetime, description) VALUES "
    description = "some to do"
    for idx in range(n):
        sql_query += f"""({get_rand_num(1, VOLONTEER_COUNT)},
                 {get_random_timestamp()},
                 {wrap_str(description)}),"""
    sql_query = sql_query[:-1] + ';'

    return my_insert(sql_query)


if __name__ == '__main__':
    # add_random_address(ADDRESS_COUNT)
    # add_some_countries()
    # add_random_volonteers(VOLONTEER_COUNT)
    # add_random_athletes(ATHLETE_COUNT)
    # add_some_transport(TRANSPORT_COUNT)
    # add_volonteer_tasks(VOLONTEER_TASK_COUNT)
    pass