from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from waitress import serve
from database import *
from flask_jwt_extended import create_access_token, unset_jwt_cookies, jwt_required, JWTManager, get_jwt_identity
import time



# app = Flask(__name__, static_folder="build/static", template_folder="build")
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["JWT_SECRET_KEY"] = "ffwemdingATW"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
jwt = JWTManager(app)


def getDbString(jsonStr, key):
    val = jsonStr.get(key)
    if val is None:
        return 0
    else:
        return val

# @app.route("/")
# def hello():
#     return render_template('index.html')

@app.route('/token', methods=["POST"])
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    # Encode PW sha256
    #encodedPW = sha256(password.encode('utf-8')).hexdigest()
    conn1 = createConnection()
    # IF count > 0 -> User is allowed
    count = executeSQL(conn1, "SELECT COUNT(*) FROM pers WHERE USERNAME=? AND PASSWORD=?", username, password).fetchone()[0]
    conn1.close()
    if (count == 0):
        return {"msg": "Wrong username or password"}, 401

    access_token = create_access_token(identity=username)
    response = {"access_token":access_token, }
    return response

# Logout user from system
@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    # Invalid JWT
    unset_jwt_cookies(response)
    return response

@app.route("/loggedUser", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    conn = createConnection()
    userDataDB = executeSQL(conn, "SELECT PERS_NO, FUNCTION_NO FROM pers WHERE USERNAME=?", current_user).fetchone()
    conn.close()

    return jsonify({'persNo': userDataDB[0], 'functionNo': userDataDB[1]})

@app.route('/pers', methods = ['GET'])
@cross_origin()
def getPers():
    conn = createConnection()
    cur = executeSQL(conn, "select PERS_NO, FIRSTNAME, LASTNAME from pers where IS_ACTIVE=1 order by LASTNAME")
    persTupel = cur.fetchall()
    destroyConnection(conn)
    pers = []
    for val in persTupel:
        pers.append({'persNo': val[0], 'firstname': val[1], 'lastname': val[2]})

    response = jsonify(pers)
    return response

@app.route('/persExtra', methods = ['GET'])
@cross_origin()
def getPersExtra():
    conn = createConnection()
    cur = executeSQL(conn, "select p.PERS_NO, p.FIRSTNAME, p.LASTNAME, p.USERNAME, f.FUNCTION_NO, f.FUNCTION_NAME, ac.CITY_NO, ac.CITY_NAME from pers p inner join atemschutzpflegestelle_cities ac on p.city_no = ac.CITY_NO inner join function f on p.FUNCTION_NO = f.FUNCTION_NO where p.IS_ACTIVE=1 order by p.LASTNAME")
    persTupel = cur.fetchall()
    destroyConnection(conn)
    pers = []
    for val in persTupel:
        pers.append({'persNo': val[0], 'firstname': val[1], 'lastname': val[2], 'username': val[3], 'functionNo': val[4], 'functionName': val[5], 'cityNo': val[6], 'cityName': val[7]})

    response = jsonify(pers)
    return response

@app.route('/cities', methods = ['GET'])
@cross_origin()
def getCities():
    conn = createConnection()
    cur = executeSQL(conn, "select CITY_NO, CITY_NAME from atemschutzpflegestelle_cities where IS_ACTIVE=1 order by CITY_NAME")
    persTupel = cur.fetchall()
    destroyConnection(conn)
    pers = []
    for val in persTupel:
        pers.append({'cityNo': val[0], 'name': val[1]})

    response = jsonify(pers)
    return response

@app.route('/function', methods = ['GET'])
@cross_origin()
def getFunction():
    conn = createConnection()
    cur = executeSQL(conn, "select FUNCTION_NO, FUNCTION_NAME from function order by FUNCTION_NO")
    persTupel = cur.fetchall()
    destroyConnection(conn)
    pers = []
    for val in persTupel:
        pers.append({'functionNo': val[0], 'functionName': val[1]})

    response = jsonify(pers)
    return response

@app.route('/search', methods = ['POST'])
@cross_origin()
def getSearch():
    persNo = request.json['persNo']
    conn = createConnection()
    cur = executeSQL(conn, "select d.DATA_NO , ac.CITY_NAME, d.DATE_WORK, d.TIME_WORK , d.FLASCHEN_FUELLEN , d.FLASCHEN_TUEV , d.MASKEN_REINIGEN , d.MASKEN_PRUEFEN , d.LA_REINIGEN , d.LA_PRUEFEN , d.GERAETE_PRUEFEN , d.GERAETE_REINIGEN, d.BEMERKUNG from atemschutzpflegestelle_data d left join atemschutzpflegestelle_cities ac on d.CITY_NO=ac.CITY_NO where PERS_NO = ? order by d.DATE_WORK desc", persNo)
    persTupel = cur.fetchall()
    destroyConnection(conn)
    pers = []
    for val in persTupel:
        dateTupel = str(val[2]).split('-')
        dateStrGer = dateTupel[2] + '.' + dateTupel[1] + '.' + dateTupel[0]
        pers.append({'key': val[0], 'city': val[1], 'dateWork': dateStrGer, 'timeWork': val[3], 'flaschenFuellen': val[4], 'flaschenTUEV': val[5], 'maskenPruefen': val[7], 'maskenReinigen': val[6], 'laPruefen': val[9], 'laReinigen': val[8], 'gereatPruefen': val[10], 'gereatReinigen': val[11], 'bemerkung': val[12]})

    response = jsonify(pers)
    return response

@app.route('/createEntry',  methods = ['PUT'])
@cross_origin()
def createEntry():
    jsonStr = request.json

    conn = createConnection()
    sql = "INSERT INTO atemschutzpflegestelle_data (CITY_NO, FLASCHEN_FUELLEN, MASKEN_PRUEFEN, GERAETE_PRUEFEN, PERS_NO, TIME_WORK, DATE_WORK, FLASCHEN_TUEV, MASKEN_REINIGEN, LA_PRUEFEN, LA_REINIGEN, GERAETE_REINIGEN, BEMERKUNG) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)"
    cursor = executeSQL(conn, sql, jsonStr.get("city"), getDbString(jsonStr, "flaschenFuellen"), getDbString(jsonStr, "maskenPruefen"), getDbString(jsonStr, "geraetePruefen"), jsonStr.get("user"), jsonStr.get("arbeitszeit"), jsonStr.get("dateWork").split('T')[0], getDbString(jsonStr, "flaschenTUEV"), getDbString(jsonStr, "maskenReinigen"), getDbString(jsonStr, "laPruefen"), getDbString(jsonStr, "laReinigen"), getDbString(jsonStr, "geraeteReinigen"), jsonStr.get("bemerkung"),)
    dataID = cursor.lastrowid
    conn.commit()
    conn.close()

    conn2 = createConnection()
    sql = "INSERT INTO atemschutzpflegestelle_nr (DATA_NO, FLASCHEN_FUELLEN_NR, FLASCHEN_TUEV_NR, MASKEN_PRUEFEN_NR, MASKEN_REINIGEN_NR, LA_PRUEFEN_NR, LA_REINIGEN_NR, GERAETE_PRUEFEN_NR, GERAETE_REINIGEN_NR) VALUES(?,?,?,?,?,?,?,?,?)"
    executeSQL(conn2, sql, dataID, jsonStr.get("flaschenFuellenNr"), jsonStr.get("flaschenTUEVNr"), jsonStr.get("maskenPruefenNr"), jsonStr.get("maskenReinigenNr"), jsonStr.get("laPruefenNr"), jsonStr.get("laReinigenNr"), jsonStr.get("geraetePruefenNr"), jsonStr.get("geraeteReinigenNr"))
    conn2.commit()
    conn2.close()
    return jsonify(1)

@app.route('/deleteEntry',  methods = ['DELETE'])
@cross_origin()
def deleteEntry():
    jsonStr = request.json

    conn = createConnection()
    sql = "DELETE FROM atemschutzpflegestelle_data WHERE DATA_NO = ?"
    executeSQL(conn, sql, jsonStr.get("dataNo"))
    conn.commit()
    conn.close()
    return jsonify(1)

@app.route('/updateEntry',  methods = ['POST'])
@cross_origin()
def updateEntry():
    jsonStr = request.json

    conn = createConnection()
    sql = "UPDATE atemschutzpflegestelle_data SET FLASCHEN_FUELLEN = ?, MASKEN_PRUEFEN = ?, GERAETE_PRUEFEN = ?, TIME_WORK = ?, FLASCHEN_TUEV = ?, MASKEN_REINIGEN = ?, LA_PRUEFEN = ?, LA_REINIGEN = ?, GERAETE_REINIGEN = ?, BEMERKUNG = ? where DATA_NO = ?"
    executeSQL(conn, sql, getDbString(jsonStr, "flaschenFuellen"), getDbString(jsonStr, "maskenPruefen"), getDbString(jsonStr, "geraetePruefen"), jsonStr.get("arbeitszeit"), getDbString(jsonStr, "flaschenTUEV"), getDbString(jsonStr, "maskenReinigen"), getDbString(jsonStr, "laPruefen"), getDbString(jsonStr, "laReinigen"), getDbString(jsonStr, "geraeteReinigen"), jsonStr.get("bemerkung"), jsonStr.get("dataNo"))
    conn.commit()
    conn.close()
    return jsonify(1)

@app.route('/createExtraEntry',  methods = ['PUT'])
@cross_origin()
def createExtraEntry():
    jsonStr = request.json

    conn = createConnection()
    sql = "INSERT INTO atemschutzpflegestelle_data (CITY_NO, FLASCHEN_FUELLEN, MASKEN_PRUEFEN, GERAETE_PRUEFEN, PERS_NO, TIME_WORK, DATE_WORK, FLASCHEN_TUEV, MASKEN_REINIGEN, LA_PRUEFEN, LA_REINIGEN, GERAETE_REINIGEN, BEMERKUNG) VALUES(0,0,0,0,?,?,?,0,0,0,0,0,?)"
    executeSQL(conn, sql, jsonStr.get("user"), jsonStr.get("arbeitszeit"), jsonStr.get("dateWork").split('T')[0], jsonStr.get("bemerkung"))
    conn.commit()
    conn.close()
    return jsonify(1)

@app.route('/updateUser',  methods = ['POST'])
@cross_origin()
def updateUser():
    jsonStr = request.json

    conn = createConnection()
    sql = "UPDATE pers SET FIRSTNAME = ?, LASTNAME = ? where PERS_NO = ?"
    executeSQL(conn, sql, jsonStr.get("firstname"), jsonStr.get("lastname"), jsonStr.get("key"))
    conn.commit()
    conn.close()
    return jsonify(1)

@app.route('/deleteUser',  methods = ['DELETE'])
@cross_origin()
def deleteUser():
    jsonStr = request.json

    conn = createConnection()
    sql = "UPDATE pers SET IS_ACTIVE = 0 where PERS_NO = ?"
    executeSQL(conn, sql, jsonStr.get("userNo"))
    conn.commit()
    conn.close()
    return jsonify(1)

@app.route('/updateCity',  methods = ['POST'])
@cross_origin()
def updateCity():
    jsonStr = request.json

    conn = createConnection()
    sql = "UPDATE atemschutzpflegestelle_cities SET CITY_NAME = ? where CITY_NO = ?"
    executeSQL(conn, sql, jsonStr.get("cityName"), jsonStr.get("key"))
    conn.commit()
    conn.close()
    return jsonify(1)

@app.route('/deleteCity',  methods = ['DELETE'])
@cross_origin()
def deleteCity():
    jsonStr = request.json

    conn = createConnection()
    sql = "UPDATE atemschutzpflegestelle_cities SET IS_ACTIVE = 0 where CITY_NO = ?"
    executeSQL(conn, sql, jsonStr.get("cityNo"))
    conn.commit()
    conn.close()
    return jsonify(1)

app.run(host='0.0.0.0', port=8080)
# serve(app, host='0.0.0.0', port=8080) # for productiv use later