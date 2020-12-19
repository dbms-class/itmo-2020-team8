# encoding: UTF-8

# Веб сервер
import cherrypy

import psycopg2.pool as pg_pool
from src.connect import parse_cmd_line
from src.static import index
from src.model import *

global_pool = None

@cherrypy.expose
class App(object):
    def __init__(self, args):
        self.args = args
        global global_pool
        global_pool = pg_pool.SimpleConnectionPool(1, 20,
                                           user=args.pg_user,
                                           password=args.pg_password,
                                           host=args.pg_host,
                                           port=args.pg_port,
                                           database=args.pg_database
                                           )

    @cherrypy.expose
    def start(self):
        return "Hello web app"

    @cherrypy.expose
    def index(self):
        return index()


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def register(self, sportsman, country, volonteer_id):
        is_ok = register_athletes(sportsman, country, volonteer_id)
        if not is_ok:
            raise cherrypy.HTTPError(400)


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def volunteer_load(self, volunteer_id=None, sportsman_count=0, total_task_count=0):
        db = global_pool.getconn()
        try:
            cur = db.cursor()
            magic_query = f"""
            with volunteer_to_task_count as (
                select volunteer_id, count(volunteer_id) as task_count from VolunteerTask group by volunteer_id
            ), volunteer_to_sportsman_count as (
                select volonteer_id, count(volonteer_id) as sportsman_count from Athletes group by volonteer_id
            ), volunteer_to_next_task as (
                select id as task_id, volunteertask.volunteer_id, datetime from volunteertask
                Join (
                select volunteer_id, Min(Now() - datetime) as diff from VolunteerTask group by volunteer_id
            ) t on volunteertask.volunteer_id = t.volunteer_id and Now() - datetime = t.diff
            )
            select id, name, sportsman_count, task_count, task_id, datetime from Volunteer
                Join volunteer_to_task_count on id = volunteer_to_task_count.volunteer_id
                Join volunteer_to_sportsman_count on id = volunteer_to_sportsman_count.volonteer_id
                JOIN volunteer_to_next_task on id = volunteer_to_next_task.volunteer_id
                where task_count >= {total_task_count} AND sportsman_count >= {sportsman_count}
            """
            if volunteer_id is None:
                total_magic_query = magic_query + ';'
            else:
                total_magic_query = f"Select * from ({magic_query}) as t where t.id={volunteer_id};"
            cur.execute(total_magic_query)
            result = []
            countries = cur.fetchall()
            for c in countries:
                result.append(
                    {
                        "volunteer_id": c[0],
                       "volunteer_name": c[1],
                       "sportsman_count": c[2],
                       "total_task_count": c[3],
                       "next_task_id": c[4],
                        "next_task_time": str(c[5])
                   }
                )
            return result
        finally:
            global_pool.putconn(db)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def volunteer_unassign(self, volunteer_id, task_ids):
        """
        Предназначается для автоматического переназначения задач
        волонтера на других волонтеров.
        :param volunteer_id: id волонтера Прогульщика
        :param task_ids: список идентификаторов
                        задач, разделённых запятыми.
                        Специальное значение * означает
                        ”все задачи волонтера"
        :return: JSON уазанного ниже вида, где каждый элемент массива
                обозначает, какому Сменщику переназначена задача:
            [
                {
                    ”task_id”: 1,
                    5”new_volunteer_name”: ”Miguel”,
                    ”new_volunteer_id”: 23
                },
            ...
            ]
        """
        volunteer_id = int(volunteer_id)
        if isinstance(task_ids, str) and task_ids == '*':
            all_tasks = get_volunter_tasks(volonter_id=volunteer_id)
        else:
            all_tasks = []
            for task_id in task_ids.split(','):
                all_tasks.append(VolunterTask(int(task_id)))
        answ = assign_another_volunter(volunteer_id, all_tasks)
        result = []
        for c in answ:
            result.append({
                "task_id": c[0],
                "new_volunteer_name": c[1],
                "new_volunteer_id": c[2]
            })
        return result


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def countries(self):
        db = global_pool.getconn()
        try:
            cur = db.cursor()
            cur.execute("SELECT id, name FROM Countries")
            result = []
            countries = cur.fetchall()
            for c in countries:
                result.append({"id": c[0], "country": c[1]})
            return result
        finally:
            global_pool.putconn(db)


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def volunteers(self):
        all_volunteers_ = all_volunteers()
        result = []
        for v in all_volunteers_:
            result.append({"id": v.id, "name": v.name()})
        return result


cherrypy.config.update({
    'server.socket_host': '0.0.0.0',
    'server.socket_port': 8080,
})
cherrypy.quickstart(App(parse_cmd_line()))
