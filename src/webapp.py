# encoding: UTF-8

# Веб сервер
import cherrypy

from src.connect import parse_cmd_line
from src.connect import create_connection
from src.static import index


@cherrypy.expose
class App(object):
    def __init__(self, args):
        self.args = args

    @cherrypy.expose
    def start(self):
        return "Hello web app"

    @cherrypy.expose
    def index(self):
        return index()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def athletes(self, athlete_id=None):
        with create_connection(self.args) as db:
            cur = db.cursor()
            if athlete_id is None:
                cur.execute("SELECT id, name FROM Athletes")
            else:
                cur.execute("SELECT id, name FROM Athletes id= %s", athlete_id)
            result = []
            athletes = cur.fetchall()
            for c in athletes:
                result.append({"id": c[0], "name": c[1]})
            return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def countries(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("SELECT id, country FROM Delegation")
            result = []
            countries = cur.fetchall()
            for c in countries:
                result.append({"id": c[0], "country": c[1]})
            return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def volunteers(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("SELECT id, name FROM Volunteer")
            result = []
            volunteers = cur.fetchall()
            for c in volunteers:
                result.append({"id": c[0], "name": c[1]})
            return result


cherrypy.config.update({
    'server.socket_host': '0.0.0.0',
    'server.socket_port': 8080,
})
cherrypy.quickstart(App(parse_cmd_line()))
