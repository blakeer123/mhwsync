from flask import Flask, request, json, jsonify
import logging

app = Flask(__name__)

fh = logging.FileHandler("log.log", mode='a', encoding=None, delay=False)
fh.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))

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

class monster:
    def __init__(self):
        self.__parts = dict()
        self.__ailments = dict()

    def addpart(self, id):
        self.__parts[id] = 1707
        
    def addailment(self, id):
        self.__ailments[id] = 0

    def deletepart(self, index):
        if len(self.__parts) < index + 1:
            return "false"
        self.__parts.pop(index)
        return "true"
    
    def deleteailment(self, index):
        if len(self.__ailments) < index + 1:
            return "false"
        self.__ailments.pop(index)
        return "true"
    
    def deleteallparts(self):
        self.__parts.clear()
        return "true"

    def deleteallailments(self):
        self.__ailments.clear()
        return "true"

    def getparts(self):
        return self.__parts

    def getailments(self):
        return self.__ailments

    def getpart(self, index):
        if len(self.__parts) < index + 1:
            return None
        return self.__parts[index]
        
    def getailment(self, index):
        if len(self.__ailments) < index + 1:
            return None
        return self.__ailments[index]

    def getpartcount(self):
        return len(self.__parts)
        
    def getailmentcount(self):
        return len(self.__ailments)

    def setparthp(self, id, hp):
        self.__parts[id] = hp

    def setailmenthp(self, id, hp):
        self.__ailments[id] = hp


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


    def getmonster(self, index):
        return self.__monsters[index]


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
        "/session/<id>/monster/<index>/part/<index>/create": "creates new part",
        "/session/<id>/monster/<index>/part/<index>": "retrieves info about part",
        "/session/<id>/monster/<index>/part/<index>/hp": "gets part hp",
        "/session/<id>/monster/<index>/part/<index>/hp/<value>": "sets part hp to <value>",
        "/session/<id>/monster/<index>/ailments": "lists registered ailments of monster",
        "/session/<id>/monster/<index>/ailment/<index>/add": "creates new ailment",
        "/session/<id>/monster/<index>/ailment/<index>": "retrieves info about ailment",
        "/session/<id>/monster/<index>/ailment/<index>/hp": "gets ailment hp",
        "/session/<id>/monster/<index>/ailment/<index>/hp/<value>": "sets ailment hp to <value>",
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
    return str(mon.getparts())

@app.route('/session/<string:id>/monster/<int:index>/replace')
def replacemonster(id, index):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    session = sessions[session_dict[id]]
    if session is None:
        return "false"
    return str(session.createmonster(index))

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
    return str(mon.getparts())

@app.route('/session/<string:id>/monster/<int:index>/partcount')
def getpartcount(id, index):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getmonster(index)
    if mon is None:
        return "false"
    return str(mon.getpartcount())

@app.route('/session/<string:id>/monster/<int:index>/part/<int:partid>/create')
def createpart(id, index, partid):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getmonster(index)
    if mon is None:
        return "false"
    mon.addpart(partid)
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
    return str(parts[partindex])

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
    return str(part)

@app.route('/session/<string:id>/monster/<int:index>/part/<int:partindex>/hp/<int:value>')
def setparthp(id, index, partindex, value):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getmonster(index)
    if mon is None:
        return "false"
    mon.setparthp(partindex, value)
    return "true"

@app.route('/session/<string:id>/monster/<int:index>/ailments')
def getailments(id, index):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getmonster(index)
    if mon is None:
        return "false"
    return str(mon.getailments())

@app.route('/session/<string:id>/monster/<int:index>/ailmentcount')
def getailmentcount(id, index):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getmonster(index)
    if mon is None:
        return "false"
    return str(mon.getailmentcount())

@app.route('/session/<string:id>/monster/<int:index>/ailment/<int:ailmentid>/create')
def createailment(id, index, ailmentid):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getmonster(index)
    if mon is None:
        return "false"
    mon.addailment(ailmentid)
    return "true"

@app.route('/session/<string:id>/monster/<int:index>/ailment/<int:ailmentindex>')
def getailment(id, index, ailmentindex):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getmonster(index)
    if mon is None:
        return "false"
    ailments = mon.getailments()
    if len(ailments) == 0:
        return "false"
    return str(ailments[ailmenttindex])

@app.route('/session/<string:id>/monster/<int:index>/ailment/<int:ailmentindex>/hp')
def getailmenthp(id, index, ailmentindex):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getmonster(index)
    if mon is None:
        return "false"
    ailment = mon.getailment(ailmentindex)
    if ailment is None:
        return "false"
    return str(ailment)

@app.route('/session/<string:id>/monster/<int:index>/ailment/<int:ailmentindex>/hp/<int:value>')
def setailmenthp(id, index, ailmentindex, value):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getmonster(index)
    if mon is None:
        return "false"
    mon.setailmenthp(ailmentindex, value)
    return "true"

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
