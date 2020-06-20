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

    def addPart(self, id):
        self.__parts[id] = 1707
        
    def addAilment(self, id):
        self.__ailments[id] = 0

    def deletePart(self, index):
        if len(self.__parts) < index + 1:
            return "false"
        self.__parts.pop(index)
        return "true"
    
    def deleteAilment(self, index):
        if len(self.__ailments) < index + 1:
            return "false"
        self.__ailments.pop(index)
        return "true"
    
    def deleteAllParts(self):
        self.__parts.clear()
        return "true"

    def deleteAllAilments(self):
        self.__ailments.clear()
        return "true"

    def getParts(self):
        return self.__parts

    def getAilments(self):
        return self.__ailments

    def getPart(self, index):
        if len(self.__parts) < index + 1:
            return None
        return self.__parts[index]
        
    def getAilment(self, index):
        if len(self.__ailments) < index + 1:
            return None
        return self.__ailments[index]

    def getPartCount(self):
        return len(self.__parts)
        
    def getAilmentCount(self):
        return len(self.__ailments)

    def setPartHP(self, id, hp):
        self.__parts[id] = hp

    def setAilmentBuildup(self, id, hp):
        self.__ailments[id] = hp


class session:
    def __init__(self):
        self.__monsters = [monster(), monster(), monster()]

    def createMonster(self, index):
        if index >= 0 and index <= 2:
            self.__monsters[index] = monster()
            return "true"
        return "false"

    def getMonsters(self):
        return self.__monsters


    def getMonster(self, index):
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
        "/session/<id>/monster/<index>/ailment/<index>/buildup": "gets ailment buildup",
        "/session/<id>/monster/<index>/ailment/<index>/buildup/<value>": "sets ailment buildup to <value>",
    }

@app.route('/sessions')
def listSessions():
    dbgmsg(request.full_path + " called")
    return repr(session_dict)

@app.route('/session/<string:id>')
def sessionInfo(id):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    return "true"

@app.route('/session/<string:id>/create')
def createSession(id):
    dbgmsg(request.full_path + " called")
    if id in session_dict:
        return "false"
    index = len(sessions)
    sessions.append(session())
    sessions[index].id = id
    session_dict[id] = index
    return "true"

@app.route('/session/<string:id>/delete')
def deleteSession(id):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    sessions.remove(sessions[session_dict[id]])
    session_dict.pop(id)
    return "true"

@app.route('/session/<string:id>/monster/<int:index>')
def getMonster(id, index):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getMonster(index)
    if mon is None:
        return "false"
    return str(mon.getParts())

@app.route('/session/<string:id>/monster/<int:index>/replace')
def replaceMonster(id, index):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    session = sessions[session_dict[id]]
    if session is None:
        return "false"
    return str(session.createMonster(index))

@app.route('/session/<string:id>/monster/<int:index>/delete')
def deleteMonster(id, index):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    return sessions[session_dict[id]].deleteMonster(index)

@app.route('/session/<string:id>/monster/<int:index>/parts')
def getParts(id, index):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getMonster(index)
    if mon is None:
        return "false"
    return str(mon.getParts())

@app.route('/session/<string:id>/monster/<int:index>/partcount')
def getPartCount(id, index):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getMonster(index)
    if mon is None:
        return "false"
    return str(mon.getPartCount())

@app.route('/session/<string:id>/monster/<int:index>/part/<int:partid>/create')
def createPart(id, index, partid):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getMonster(index)
    if mon is None:
        return "false"
    mon.addPart(partid)
    return "true"

@app.route('/session/<string:id>/monster/<int:index>/part/<int:partindex>')
def getPart(id, index, partindex):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getMonster(index)
    if mon is None:
        return "false"
    parts = mon.getParts()
    if len(parts) == 0:
        return "false"
    return str(parts[partindex])

@app.route('/session/<string:id>/monster/<int:index>/part/<int:partindex>/hp')
def getPartHP(id, index, partindex):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getMonster(index)
    if mon is None:
        return "false"
    part = mon.getPart(partindex)
    if part is None:
        return "false"
    return str(part)

@app.route('/session/<string:id>/monster/<int:index>/part/<int:partindex>/hp/<int:value>')
def setPartHP(id, index, partindex, value):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getMonster(index)
    if mon is None:
        return "false"
    mon.setPartHP(partindex, value)
    return "true"

@app.route('/session/<string:id>/monster/<int:index>/ailments')
def getAilments(id, index):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getMonster(index)
    if mon is None:
        return "false"
    return str(mon.getAilments())

@app.route('/session/<string:id>/monster/<int:index>/ailmentcount')
def getAilmentCount(id, index):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getMonster(index)
    if mon is None:
        return "false"
    return str(mon.getAilmentCount())

@app.route('/session/<string:id>/monster/<int:index>/ailment/<int:ailmentid>/create')
def createAilment(id, index, ailmentid):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getMonster(index)
    if mon is None:
        return "false"
    mon.addAilment(ailmentid)
    return "true"

@app.route('/session/<string:id>/monster/<int:index>/ailment/<int:ailmentindex>')
def getAilment(id, index, ailmentindex):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getMonster(index)
    if mon is None:
        return "false"
    ailments = mon.getAilments()
    if len(ailments) == 0:
        return "false"
    return str(ailments[ailmentindex])

@app.route('/session/<string:id>/monster/<int:index>/ailment/<int:ailmentindex>/buildup')
def getAilmentBuildup(id, index, ailmentindex):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getMonster(index)
    if mon is None:
        return "false"
    ailment = mon.getAilment(ailmentindex)
    if ailment is None:
        return "false"
    return str(ailment)

@app.route('/session/<string:id>/monster/<int:index>/ailment/<int:ailmentindex>/buildup/<int:value>')
def setAilmentBuildup(id, index, ailmentindex, value):
    dbgmsg(request.full_path + " called")
    if id not in session_dict:
        return "false"
    mon = sessions[session_dict[id]].getMonster(index)
    if mon is None:
        return "false"
    mon.setAilmentBuildup(ailmentindex, value)
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
