from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from waitress import serve
from database import *



app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def getDbString(jsonStr, key):
    val = jsonStr.get(key)
    if val is None:
        return 0
    else:
        return val


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