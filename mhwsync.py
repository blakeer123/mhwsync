from flask import Flask, request, json, jsonify
import logging
import os
import sys

if sys.version_info[0] < 3 or sys.version_info[1] < 7:
    raise Exception("Python 3.7 or higher required")

app = Flask(__name__)

"""
status codes:
0 - OK
1 - session does not exist
2 - session already exists
3 - invalid monster index
4 - part does not exist
5 - ailment does not exist
10 - exception
404 - HTTP 404
"""

ok = {
    "status": 0,
    "value": ""
    }
sessionDoesNotExist = { 
    "status": 1,
    "value": "session does not exist"
    }
sessionAlreadyExists = {
    "status": 2,
    "value": "session already exists"
    }
monsterOutsideRange = { 
    "status": 3,
    "value": "monster outside range"
    }
partOutsideRange = {
   "status": 4,
   "value": "part outside range"
   }
ailmentOutsideRange = {
    "status": 5,
    "value": "ailment outside range"
    }
e404 = {
    "status": 404,
    "value": ""
    }

bufferSize = 50

class monster:
    def __init__(self):
        self.__parts = dict()
        self.__ailments = dict()
        for i in range(bufferSize):
            self.__parts[i] = 0
            self.__ailments[i] = 0

    def clear(self):
        for i in range(bufferSize):
            self.__parts[i] = 0
            self.__ailments[i] = 0

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

    def clearMonster(self, index):
        self.__monsters[index].clear()

    def getMonsters(self):
        return self.__monsters

    def getMonster(self, index):
        return self.__monsters[index]

sessions = []
session_dict = dict()

@app.route('/')
def alive():
    ok["value"] = ""
    return ok

@app.route('/session/<string:id>/exists')
def sessionInfo(id):
    if id in session_dict:
        ok["value"] = ""
        return ok
    return sessionDoesNotExist

@app.route('/session/<string:id>/create')
def createSession(id):
    if id in session_dict:
        return sessionAlreadyExists
    index = len(sessions)
    sessions.append(session())
    sessions[index].id = id
    session_dict[id] = index
    ok["value"] = ""
    return ok

@app.route('/session/<string:id>/delete')
def deleteSession(id):
    if id not in session_dict:
        return sessionDoesNotExist
    sessions.remove(sessions[session_dict[id]])
    session_dict.pop(id)
    ok["value"] = ""
    return ok

@app.route('/session/<string:id>/monster/<int:index>/clear')
def clearMonster(id, index):
    if id not in session_dict:
        return sessionDoesNotExist
    if index not in range(3):
        return monsterOutsideRange
    session = sessions[session_dict[id]]
    session.clearMonster(index)
    ok["value"] = ""
    return ok

@app.route('/session/<string:id>/monster/<int:index>/part/<int:partindex>/hp')
def getPartHP(id, index, partindex):
    if id not in session_dict:
        return sessionDoesNotExist
    if index not in range(3):
        return monsterOutsideRange
    if partindex not in range(bufferSize):
        return partOutsideRange
    mon = sessions[session_dict[id]].getMonster(index)
    part = mon.getPart(partindex)
    if part is None:
        return partOutsideRange
    ok["value"] = str(part)
    return ok

@app.route('/session/<string:id>/monster/<int:index>/part/<int:partindex>/hp/<int:value>')
def setPartHP(id, index, partindex, value):
    if id not in session_dict:
        return sessionDoesNotExist
    if index not in range(3):
        return monsterOutsideRange
    if partindex not in range(bufferSize):
        return partOutsideRange
    mon = sessions[session_dict[id]].getMonster(index)
    mon.setPartHP(partindex, value)
    ok["value"] = ""
    return ok

@app.route('/session/<string:id>/monster/<int:index>/ailment/<int:ailmentindex>/buildup')
def getAilmentBuildup(id, index, ailmentindex):
    if id not in session_dict:
        return sessionDoesNotExist
    if index not in range(3):
        return monsterOutsideRange
    if ailmentindex not in range(bufferSize):
        return ailmentOutsideRange
    mon = sessions[session_dict[id]].getMonster(index)
    ailment = mon.getAilment(ailmentindex)
    if ailment is None:
        return ailmentOutsideRange
    ok["value"] = str(ailment)
    return ok

@app.route('/session/<string:id>/monster/<int:index>/ailment/<int:ailmentindex>/buildup/<int:value>')
def setAilmentBuildup(id, index, ailmentindex, value):
    if id not in session_dict:
        return sessionDoesNotExist
    if index not in range(3):
        return monsterOutsideRange
    if ailmentindex not in range(bufferSize):
        return ailmentOutsideRange
    mon = sessions[session_dict[id]].getMonster(index)
    mon.setAilmentBuildup(ailmentindex, value)
    ok["value"] = ""
    return ok

@app.errorhandler(404)
def not_found(error=None):
    e404["value"] = request.url
    return e404

@app.errorhandler(Exception)
def handle_exception(e, source="app-errorhandler"):
    msg = {
        "status": 10,
        "value": repr(e) + ", source: " + source + ", request: " + request.full_path
        }
    return msg

if __name__ == "__main__":
    app.run()