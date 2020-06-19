from flask import Flask, request, json, jsonify
import logging

app = Flask(__name__)

fh = logging.FileHandler("log.log", mode='a', encoding=None, delay=False)
fh.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))

app.logger.addHandler(fh)
app.logger.setLevel(30)


"""
loglevels:
CRITICAL 50
ERROR 40
WARNING 30
INFO 20
DEBUG 10
NOTSET 0
"""


def dbgmsg(msg):
    app.logger.debug(msg)


def errmsg(msg):
    app.logger.error(msg)


dbgmsg("server started")


class part:
    def gethp(self):
        return self.__hp

    def sethp(self, value):
        if value > 0:
            self.__hp = value
            return "true"
        return "false"

    __hp = 1701


class monster:
    def __init__(self):
        self.__parts = []

    def addpart(self):
        self.__parts.append(part())

    def deletepart(self, index):
        if len(self.__parts) < index + 1:
            return "false"
        self.__parts.remove(index)
        return "true"

    def deleteallparts(self):
        self.__parts.clear()
        return "true"

    def getparts(self):
        return self.__parts

    def getpartlist(self):
        ret = []
        for entry in self.__parts:
            ret.append(entry.gethp())
        return ret

    def getpart(self, index):
        if len(self.__parts) < index + 1:
            return None
        return self.__parts[index]

    def getpartcount(self):
        return len(self.__parts)


class session:
    def __init__(self):
        self.__monsters = [monster(), monster(), monster()]

    def createmonster(self, index):
        if index >= 0 and index <= 2:
            self.__monsters[index] = monster()
            return "true"
        return "false"

    def getmonsters(self):
        return self.__monsters

    def getmonsterliststring(self):
        return str(self.__monsters[0].getpartlist()) + str(self.__monsters[1].getpartlist()) + str(self.__monsters[2].getpartlist())

    def getmonster(self, index):
        return self.__monsters[index]


"""
    def addmonster(self):
        if(self.__monsters[0] == None):
            self.__monsters[0] = monster()
            return "true"
        elif(self.__monsters[1] == None):
            self.__monsters[1] = monster()
            return "true"
        elif(self.__monsters[2] == None):
            self.__monsters[2] = monster()
            return "true"
        return "false"

    def deletemonster(self, index):
        if index >= 0 and index <= 2 and self.__monsters[index] is not None:
            self.__monsters[index] = None
            return "true"
        return "false"
"""


sessions = []
session_dict = dict()


@app.route("/")
def overview():
    return {
        "/sessions": "lists all sessions",
        "/session/<id>": "retrieves info about session",
        "/session/<id>/create": "creates session",
        "/session/<id>/delete": "deletes session",
        "/session/<id>/monsters": "lists monsters",
        "/session/<id>/monsters/add": "creates new monster",
        "/session/<id>/monster/<index>": "retrieves info about monster",
        "/session/<id>/monster/<index>/delete": "deletes monster",
        "/session/<id>/monster/<index>/parts": "lists registered parts of monster",
        "/session/<id>/monster/<index>/parts/add": "creates new part",
        "/session/<id>/monster/<index>/part/<index>": "retrieves info about part",
        "/session/<id>/monster/<index>/part/<index>/hp": "gets part hp",
        "/session/<id>/monster/<index>/part/<index>/hp/<value>": "sets part hp to <value>",
    }


@app.route('/sessions')
def listsessions():
    dbgmsg(request.full_path + " called")
    return repr(session_dict)


@app.route('/session/<string:id>')
def sessioninfo(id):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    return "true"


@app.route('/session/<string:id>/create')
def createsession(id):
    dbgmsg(request.full_path + " called")
    if id in session_dict:
        return "false"
    index = len(sessions)
    sessions.append(session())
    sessions[index].id = id
    session_dict[id] = index
    return "true"


@app.route('/session/<string:id>/delete')
def deletesession(id):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    sessions.remove(sessions[session_dict[id]])
    session_dict.pop(id)
    return "true"


@app.route("/session/<string:id>/monsters")
def monsters(id):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    return sessions[session_dict[id]].getmonsterliststring()


@app.route('/session/<string:id>/monster/<int:index>')
def getmonster(id, index):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getmonster(index)
    if mon is None:
        return "false"
    return str(mon.getpartlist())


@app.route('/session/<string:id>/monsters/add')
def addmonster(id):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    return sessions[session_dict[id]].addmonster()


@app.route('/session/<string:id>/monster/<int:index>/delete')
def deletemonster(id, index):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    return sessions[session_dict[id]].deletemonster(index)


@app.route('/session/<string:id>/monster/<int:index>/parts')
def getparts(id, index):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getmonster(index)
    if mon is None:
        return "false"
    return str(mon.getpartlist())


@app.route('/session/<string:id>/monster/<int:index>/partcount')
def getpartcount(id, index):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getmonster(index)
    if mon is None:
        return "false"
    return str(mon.getpartcount())


@app.route('/session/<string:id>/monster/<int:index>/parts/add')
def createpart(id, index):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getmonster(index)
    if mon is None:
        return "false"
    mon.addpart()
    return "true"


@app.route('/session/<string:id>/monster/<int:index>/part/<int:partindex>')
def getpart(id, index, partindex):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getmonster(index)
    if mon is None:
        return "false"
    parts = mon.getparts()
    if len(parts) == 0:
        return "false"
    return str(parts[partindex].gethp())


@app.route('/session/<string:id>/monster/<int:index>/part/<int:partindex>/hp')
def getparthp(id, index, partindex):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getmonster(index)
    if mon is None:
        return "false"
    part = mon.getpart(partindex)
    if part is None:
        return "false"
    return str(part.gethp())


@app.route('/session/<string:id>/monster/<int:index>/part/<int:partindex>/hp/<int:value>')
def setparthp(id, index, partindex, value):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getmonster(index)
    if mon is None:
        return "false"
    part = mon.getpart(partindex)
    if part is None:
        return "false"
    return part.sethp(value)


@app.errorhandler(404)
def not_found(error=None):
    errmsg("error 404: " + request.url)
    return "false"


@app.errorhandler(Exception)
def handle_exception(e, source="app-errorhandler"):
    msg = {
        "errorcode": 1,
        "message": repr(e),
        "source": source
    }
    errmsg(msg)
    return "false"


if __name__ == "__main__":
    app.run()
