import pymysql
from flask import Flask, request, json, jsonify
from werkzeug.exceptions import HTTPException
from flaskext.mysql import MySQL
import logging
app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = '192.168.178.40'
app.config['MYSQL_DATABASE_USER'] = 'password'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'mhw-sync'

mysql = MySQL(app)

fh = logging.FileHandler("log.log", mode='a', encoding=None, delay=False)
fh.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
app.logger.addHandler(fh)
app.logger.setLevel(10)


def dbgmsg(msg):
    app.logger.debug(msg)


def errmsg(msg):
    app.logger.error(msg)


dbgmsg("server started")

"""
loglevels:
CRITICAL 50
ERROR 40
WARNING 30
INFO 20
DEBUG 10
NOTSET 0
"""


"""
@app.route('/processcommand', methods=["GET"])
def processcommand():
    dbgmsg(request.full_path)
    try:
        json = request.json
        command = json["command"]
        if command == "createSession":
            pass
        elif command == "joinSession":
            pass
        elif command == "createMonster":
            pass
        elif command ==



    except Exception as e:
        return handle_exception(e, request.full_path)
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

"""


@app.route("/")
def overview():
    return {
        "/sessions": "lists all sessions",
        "/session/<id>": "retrieves info about session",
        "/session/<id>/create": "creates session",
        "/session/<id>/join": "joins session (playercount++) if playercount < 4",
        "/session/<id>/leave": "leaves session (playercount--) if playercount > 0",
        "/session/<id>/delete": "deletes session if playercount == 0",
        "/session/<id>/forcedelete": "delete session",
        "/session/<id>/monsters": "lists monsters",
        "/session/<id>/monster/<index>": "retrieves info about monster if index >= 0 && index <= 2",
        "/session/<id>/monster/<index>/create": "creates new monster",
        "/session/<id>/monster/<index>/delete": "deletes monster",
        "/session/<id>/monster/<index>/parts": "lists registered parts of monster",
        "/session/<id>/monster/<index>/part/<id>": "retrieves info about part",


    }


@app.route('/sessions')
def sessions():
    dbgmsg(request.full_path + " called")
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * from sessions;")
        sessions = cursor.fetchall()
        return jsonify(sessions)
    except Exception as e:
        return handle_exception(e, request.full_path)
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass


@app.route('/session/<string:id>')
@app.route('/session/<string:id>/')
def sessioninfo(id):
    dbgmsg(request.full_path + " called")
    try:
        query = "SELECT * FROM sessions WHERE idstring = %s;"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(query, id)
        session = cursor.fetchone()
        if not session:
            raise ValueError("Session does not exist")
        query = "SELECT * FROM monsters WHERE session = %s"
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query, session[0])
        return {
            "errorcode": 0,
            "message": "success",
            "playercount": session[2],
            "monstercount": session[3]
        }
    except Exception as e:
        return handle_exception(e, request.full_path)
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass


@app.route('/session/<string:id>/create')
def createsession(id):
    dbgmsg(request.full_path + " called")
    try:
        query = "INSERT INTO sessions(idstring) VALUES(%s);"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(query, id)
        conn.commit()
        return {
            "errorcode": 0,
            "message": "success",
        }
    except Exception as e:
        return handle_exception(e, request.full_path)
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass


@app.route('/session/<string:id>/join')
def joinsession(id):
    dbgmsg(request.full_path + " called")
    try:
        query = "SELECT playercount FROM sessions WHERE idstring = %s;"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(query, id)
        playercount = cursor.fetchone()
        if not playercount:
            raise ValueError("Session does not exist")
        if playercount[0] >= 4:
            raise Exception("Session full")
        query = "UPDATE sessions SET playercount = playercount + 1 WHERE idstring = %s;"
        cursor.execute(query, id)
        conn.commit()
        return {
            "errorcode": 0,
            "message": "success"
        }
    except Exception as e:
        return handle_exception(e, request.full_path)
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass


@app.route('/session/<string:id>/leave')
def leavesession(id):
    dbgmsg(request.full_path + " called")
    try:
        query = "SELECT playercount FROM sessions WHERE idstring = %s;"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(query, id)
        playercount = cursor.fetchone()
        if not playercount:
            raise ValueError("Session does not exist")
        if playercount[0] == 0:
            raise Exception("Session already empty")
        query = "UPDATE sessions SET playercount = playercount - 1 WHERE idstring = %s;"
        cursor.execute(query, id)
        conn.commit()
        return {
            "errorcode": 0,
            "message": "success"
        }
    except Exception as e:
        return handle_exception(e, request.full_path)
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass


@app.route('/session/<string:id>/delete')
def deletesession(id):
    dbgmsg(request.full_path + " called")
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT playercount, id FROM sessions WHERE idstring = %s;"
        cursor.execute(query, id)
        result = cursor.fetchone()
        if result[0] > 0:
            raise Exception("Session not empty")
        query = "DELETE FROM parts WHERE session = %s"
        cursor.execute(query, result[1])
        query = "DELETE FROM monsters WHERE session = %s;"
        cursor.execute(query, result[1])
        query = "DELETE FROM sessions WHERE id = %s;"
        cursor.execute(query, result[1])
        conn.commit()
        return {
            "errorcode": 0,
            "message": "success"
        }
    except Exception as e:
        return handle_exception(e, request.full_path)
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass

@app.route('/session/<string:id>/forcedelete')
def forcedeletesession(id):
    dbgmsg(request.full_path + " called")
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT id FROM sessions WHERE idstring = %s;"
        cursor.execute(query, id)
        result = cursor.fetchone()
        query = "DELETE FROM parts WHERE session = %s"
        cursor.execute(query, result[0])
        query = "DELETE FROM monsters WHERE session = %s;"
        cursor.execute(query, result[0])
        query = "DELETE FROM sessions WHERE id = %s;"
        cursor.execute(query, result[0])
        conn.commit()
        return {
            "errorcode": 0,
            "message": "success"
        }
    except Exception as e:
        return handle_exception(e, request.full_path)
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass


            pass


@app.route('/session/<string:id>/monsters')
def monsters(id):
    dbgmsg(request.full_path + " called")
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT * FROM sessions WHERE idstring = %s;"
        cursor.execute(query, id)
        session = cursor.fetchone()
        if not session:
            raise ValueError("Session does not exist")
        query = "SELECT * FROM monsters WHERE session = %s;"
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query, session[0])
        monsters = cursor.fetchall()
        return {
            "errorcode": 0,
            "message": "success",
            "monsterlist": monsters
        }
    except Exception as e:
        return handle_exception(e, request.full_path)
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass


@app.route('/session/<string:id>/monster/<int:index>')
@app.route('/session/<string:id>/monster/<int:index>/')
def getmonster(id, index):
    dbgmsg(request.full_path + " called")
    try:
        if index < 0 or index > 2:
            raise ValueError("Monster index invalid (only 0-2 are valid)")
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT id from sessions WHERE idstring = %s;"
        cursor.execute(query, id)
        session = cursor.fetchone()
        if not session:
            raise ValueError("Session does not exist")
        query = "SELECT * FROM monsters WHERE session = %s AND idx = %s;"
        cursor.execute(query, (session[0], index))
        monster = cursor.fetchone()
        if not monster:
            raise ValueError("Monster does not exist")
        return {
            "errorcode": 0,
            "message": "success",
            "monster": monster
        }
    except Exception as e:
        return handle_exception(e, request.full_path)
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass


@app.route('/session/<string:id>/monster/<int:index>/create')
def createmonster(id, index):
    dbgmsg(request.full_path + " called")
    try:
        if index < 0 or index > 2:
            raise ValueError("Monster index invalid (only 0-2 are valid)")
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT * FROM sessions WHERE idstring=%s;"
        cursor.execute(query, id)
        session = cursor.fetchone()
        if not session:
            raise ValueError("Session does not exist")
        if session[3] >= 3:
            raise Exception("monstercount already 3")
        query = "SELECT * FROM monsters WHERE session = %s AND idx = %s;"
        if cursor.execute(query, (session[0], index)) > 0:
            raise Exception("A monster with this index already exists")
        query = "INSERT INTO monsters(session, idx) VALUES(%s, %s);"
        cursor.execute(query, (session[0], index))
        conn.commit()
        return {
            "errorcode": 0,
            "message": "success"
        }
    except Exception as e:
        return handle_exception(e, request.full_path)
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass


@app.route('/session/<string:id>/monster/<int:index>/delete')
def deletemonster(id, index):
    dbgmsg(request.full_path + " called")
    try:
        if index < 0 or index > 2:
            raise ValueError("Monster index invalid (only 0-2 are valid)")
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT * FROM sessions WHERE idstring=%s;"
        cursor.execute(query, id)
        session = cursor.fetchone()
        if not session:
            raise ValueError("Session does not exist")
        query = "SELECT id FROM monsters WHERE session = %s AND idx = %s;"
        if cursor.execute(query, (session[0], index)) == 0:
            raise ValueError("Monster does not exist")
        result = cursor.fetchone()
        query = "DELETE FROM monsters WHERE id = %s;"
        cursor.execute(query, result[0])
        conn.commit()
        return {
            "errorcode": 0,
            "message": "success"
        }
    except Exception as e:
        return handle_exception(e, request.full_path)
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass


@app.route('/session/<string:id>/monster/<int:index>/parts')
def getparts(id, index):
    dbgmsg(request.full_path + " called")
    try:
        if index < 0 or index > 2:
            raise ValueError("Monster index invalid (only 0-2 are valid)")
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT id from sessions WHERE idstring = %s;"
        cursor.execute(query, id)
        session = cursor.fetchone()
        if not session:
            raise ValueError("Session does not exist")
        query = "SELECT id FROM monsters WHERE session = %s AND idx = %s;"
        cursor.execute(query, (session[0], index))
        monster = cursor.fetchone()
        if not monster:
            raise ValueError("Monster does not exist")
        query = "SELECT * FROM parts WHERE monsteruid = %s;"
        cursor.execute(query, monster[0])
        parts = cursor.fetchall()
        return {
            "errorcode": 0,
            "message": "success",
            "partlist": parts
        }
    except Exception as e:
        return handle_exception(e, request.full_path)
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass

@app.route('/session/<string:id>/monster/<int:index>/part/<int:partid>')
@app.route('/session/<string:id>/monster/<int:index>/part/<int:partid>/')
def getpart(id, index, partid):
    dbgmsg(request.full_path + " called")
    try:
        if index < 0 or index > 2:
            raise ValueError("Monster index invalid (only 0-2 are valid)")
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT id from sessions WHERE idstring = %s;"
        cursor.execute(query, id)
        session = cursor.fetchone()
        if not session:
            raise ValueError("Session does not exist")
        query = "SELECT id FROM monsters WHERE session = %s AND idx = %s;"
        cursor.execute(query, (session[0], index))
        monster = cursor.fetchone()
        if not monster:
            raise ValueError("Monster does not exist")
        query = "SELECT * FROM parts WHERE monsteruid = %s AND idx = %s;"
        cursor.execute(query, (monster[0], partid))
        part = cursor.fetchall()
        if not part:
            raise ValueError("Part does not exist")
        return {
            "errorcode": 0,
            "message": "success",
            "part": part
        }
    except Exception as e:
        return handle_exception(e, request.full_path)
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass


@app.route('/session/<string:id>/monster/<int:index>/part/<int:partindex>/create')
def createpart(id, index, partindex):
    dbgmsg(request.full_path + " called")
    try:
        if index < 0 or index > 2:
            raise ValueError("Monster index invalid (only 0-2 are valid)")
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT id from sessions WHERE idstring = %s;"
        cursor.execute(query, id)
        session = cursor.fetchone()
        if not session:
            raise ValueError("Session does not exist")
        cursor.execute("SELECT id FROM monsters WHERE session = %s AND idx = %s;", (session[0], index))
        monster = cursor.fetchone()
        if not monster:
            raise ValueError("Monster does not exist")
        if cursor.execute("SELECT * FROM parts WHERE monsteruid = %s AND idx = %s;", (monster[0], partindex)):
            raise Exception("Part already exists")
        query = "INSERT INTO parts(session, monsteruid, idx) VALUES(%s, %s, %s);"
        cursor.execute(query, (session[0], monster[0], partindex))
        conn.commit()
        return {
            "errorcode": 0,
            "message": "success"
        }
    except Exception as e:
        return handle_exception(e, request.full_path)
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    errmsg("error 404: " + request.url)
    return response


@app.errorhandler(Exception)
def handle_exception(e, source="app-errorhandler"):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    try:
        msg = {
            "errorcode": 1,
            "message": repr(e),
            "source": source
        }
        response = jsonify(msg)
        response.status_code = 500
        errmsg(msg)
        return response
    except:
        return "exception during exception handling!"


if __name__ == "__main__":
    app.run()
