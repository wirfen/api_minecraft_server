from funciones.server import *
from funciones.player import *
from funciones.whitelist import *
import os, json, ssl, time, random
from flask import Flask, request, send_file, make_response
from flask_cors import CORS
from datetime import datetime
from mcstatus import MinecraftServer

mypass="123"

servidor = MinecraftServer.lookup("localhost")

app = Flask(__name__)

@app.route("/install", methods = ["POST"])
def install():
    os.system("wget {} -O server.jar".format(request.get_json()["url"]))
    os.system("mkdir saves backups")
    f = open("eula.txt", "w")
    f.write("eula=true")
    f.close()
    f = open("start.sh", "w")
    f.write("#!/bin/bash\njava -Xms{}M -Xmx{}M -jar server.jar nogui".format(request.get_json()["min_memory"],request.get_json()["max_memory"]))
    f.close()
    os.system("cp funciones/server.properties .")
    os.system("chmod +x start.sh")
    startMinecraft()
    return "Installed"

@app.route("/status", methods = ["GET"])
def status():
    password="null"
    if "pass" in request.headers:
        password=request.headers["pass"]
    if (password=="123"):
        try:
            status=servidor.status()
            query=servidor.query()
            return {"Ping":status.latency, "Players-Names":"{}".format(", ".join(query.players.names)), "Players":status.players.online}
        except ConnectionRefusedError:
            return "Server shutdown", 503
    else:
        return "Unauthorized", 401

@app.route("/lists", methods = ["GET"])
def lists():
    password="null"
    if "pass" in request.headers:
        password=request.headers["pass"]
    if (password==mypass):
        backups={}
        if(request.args.get("map")):
            if(os.path.isdir("backups/{}".format(request.args.get("map")))):
                return json.dumps(sorted(os.listdir("backups/" + request.args.get("map")), reverse=True), indent=1), 200
            else:
                return "Map not found", 404
        else:
            return json.dumps(sorted(os.listdir("saves")), indent=1), 200
    else:
        return "Unauthorized", 401

@app.route("/makebackup", methods = ["PUT"])
def makebackup():
    password="null"
    if "pass" in request.headers:
        password=request.headers["pass"]
    if (password==mypass):
        if(request.args.get("mapa") and os.path.isdir("saves/" + request.args.get("mapa"))):
            mapa=request.args.get("mapa")
            fecha=datetime.now().strftime("%Y_%m_%d_%H_%M")
            sendMessage("Haciendo backup...")
            os.system("mkdir -p backups/{} && tar -czf backups/{}/{}-{}.tar.gz -C saves/{} .".format(mapa,mapa,mapa,fecha,mapa))
            sendMessage("Finished!!")
            return "{}-{}.tar.gz".format(mapa,fecha), 201
        else:
            return "Map not found", 404
    else:
        return "Unauthorized", 401

@app.route("/download", methods = ["GET"])
def download():
    print("Algo pasa")
    password="null"
    if "pass" in request.headers:
        password=request.headers["pass"]
    if (True):
        #if(request.args.get("backup") and not request.args.get("mapa")):
        if(request.args.get("backup")):
            print(request.args.get("backup"))
            mapa=request.args.get("backup").split("-")[0]
            if(os.path.isfile("backups/{}/{}".format(mapa,request.args.get("backup")))):
                print("Mecago entodoooo")
                return send_file("backups/{}/{}".format(mapa, request.args.get("backup")), attachment_filename=request.args.get("backup"), as_attachment=True, mimetype="application/tar+gzip")
            else:
                return "File not found", 404
        elif(request.args.get("mapa") and not request.args.get("backup")):
            fecha=datetime.now().strftime("%Y_%m_%d_%H_%M")
            if(os.path.isdir("saves/{}".format(request.args.get("mapa")))):
                os.system("tar -czf backups/{}/{}-{}.tar.gz -C saves/{} .".format(request.args.get("mapa"),request.args.get("mapa"),fecha,request.args.get("mapa")))
                response = make_response(send_file("backups/{}/{}-{}.tar.gz".format(request.args.get("mapa"), request.args.get("mapa"),fecha),"{}-{}.tar.gz".format(request.args.get("mapa"),fecha), as_attachment=True))
                response.headers["Content-Type"] = "application/pene; charset=utf-8"
                return response
            else:
                return "Map not found", 404
        else:
            return "Bad request", 400
    else:
        return "Unauthorized", 401

@app.route("/restore", methods= ["POST"])
def restore():
    password="null"
    if "pass" in request.headers:
        password=request.headers["pass"]
    if (password==mypass):
        # Restauramos un fichero que subamos
        if(request.content_type and not request.args.get("backup")):
            file = request.files["fichero"]
            mapa=file.filename.split("-")[0]
            try:
                stopMinecraft()
                file.save("backups/{}/".format(mapa) + file.filename) #Guardamos el mapa en backups
                os.system("rm -r saves/{}".format(mapa)) #Borramos el mapa
                os.system("mkdir -p saves/{} && tar -xzf backups/{}/{} -C saves/{}".format(mapa, mapa, file.filename, mapa)) #Restauramos el mapa subido
                os.system("sed -i -e '/level-name/c\level-name=saves/{}' server.properties".format(mapa)) # Configuramos el servidor para usar ese mapa
                startMinecraft()
                return "Accepted", 202
            except:
                os.system("rm backups/{}".format(file.filename))
                return "File not supported", 415

	# Restauramos un fichero de backup
        elif(request.args.get("backup") and not request.content_type):
            backup = request.args.get("backup")
            mapa=backup.split("-")[0]
            if(os.path.isfile("backups/{}/{}".format(mapa,backup))):
                stopMinecraft()
                os.system("rm -r saves/{}".format(mapa)) #Borramos el mapa
                os.system("mkdir -p saves/{} && tar -xzf backups/{}/{} -C saves/{}".format(mapa, mapa, backup, mapa)) #Restauramos el mapa de backup
                os.system("sed -i -e '/level-name/c\level-name=saves/{}' server.properties".format(mapa)) # Configuramos el servidor para usar ese mapa
                startMinecraft()
                return "Accepted", 202
            else:
                return "File not found", 404
        else:
            return "Bad request", 400
    else:
        return "Unauthorized", 401

@app.route("/change", methods= ["POST"])
def change():
    password="null"
    if "pass" in request.headers:
        password=request.headers["pass"]
    if (password==mypass):
        if(request.args.get("map")):
            try:
                stopMinecraft()
                os.system("mkdir saves/{}".format(request.args.get("map")))
                os.system("sed -i -e '/level-name/c\level-name=saves/{}' server.properties".format(request.args.get("map"))) #Configuramos el servidor para usar ese mapa
                os.system("sed -i -e '/level-seed/c\level-seed={}' server.properties".format(random.getrandbits(32))) #Generamos una semilla aleatoria
                startMinecraft()
                return "Loading map {}".format(request.args.get("map")), 202
            except:
                return "Map cant be changed", 500
        else:
            return "Map not found", 404
    else:
        return "Unauthorized", 401

@app.route("/properties", methods = ["GET"])
def getProperties():
    properties = open("server.properties").read()
    return properties, 200

@app.route("/properties", methods = ["PUT"])
def setProperties():
    open("server.properties","w").write(request.get_data().decode().replace("\n",""))
    properties = open("server.properties").read()
    return properties, 201

@app.route("/delete", methods= ["DELETE"])
def delete():
    password="null"
    if "pass" in request.headers:
        password=request.headers["pass"]
    if (password==mypass):
        if(request.args.get("backup") and not request.args.get("mapa")):
            mapa=request.args.get("backup").split("-")[0]
            os.system("rm backups/{}/{}".format(mapa, request.args.get("backup")))
            return request.args.get("backup") + " deleted", 200
        elif(request.args.get("mapa") and not request.args.get("backup")):
            stopMinecraft()
            os.system("rm -r saves/{}".format(request.args.get("mapa")))
            startMinecraft()
            return request.args.get("mapa") + " deleted", 200
        elif(request.args.get("mapa") and request.args.get("backup") and request.args.get("mapa") == request.args.get("backup")):
            stopMinecraft()
            os.system("rm -r saves/{}".format(request.args.get("mapa")))
            os.system("rm -r backups/{}".format(request.args.get("backup").split("-")[0], request.args.get("backup")))
            return "{} map and backups deleted".format(request.args.get("mapa"))
        else:
            return "Bad request", 400
    else:
        return "Unauthorized", 401

@app.route("/server", methods= ["GET"])
def server():
    password="null"
    if "pass" in request.headers:
        password=request.headers["pass"]
    if (password==mypass):
        if(request.args.get("action")=="start"):
            startMinecraft()
            return "Accepted", 202
        elif(request.args.get("action")=="stop"): #Parar minecraft
            stopMinecraft()
            return "Ok", 200
        elif(request.args.get("action")=="restart"): #Reiniciar minecraft
            stopMinecraft()
            startMinecraft()
            return "Accepted", 202
        elif(request.args.get("action")=="weather"): #Reiniciar minecraft
            print("Cambiemos el clima")
            setWheater(request.args.get("condition"))
            return "Accepted", 202
        elif(request.args.get("action")=="daytime"): #Reiniciar minecraft
            setDaytime(request.args.get("condition"))
            return "Accepted", 202
        else:
            return "Bad request", 400
    else:
        return "Unauthorized", 401

@app.route("/player", methods= ["GET"])
def player():
    password="null"
    if "pass" in request.headers:
        password=request.headers["pass"]
    if (password==mypass):
        if(request.args.get("action")=="op"):
            operator(request.args.get("name"))
            return "Accepted", 202
        elif(request.args.get("action")=="deop"):
            deoperator(request.args.get("name"))
            return "Accepted", 202
        elif(request.args.get("action")=="survival"):
            survival(request.args.get("name"))
            return "Accepted", 202
        elif(request.args.get("action")=="creative"):
            creative(request.args.get("name"))
            return "Accepted", 202
        elif(request.args.get("action")=="spectator"):
            spectator(request.args.get("name"))
            return "Accepted", 202
        elif(request.args.get("action")=="kick"):
            kick(request.args.get("name"))
            return "Accepted", 202
        elif(request.args.get("action")=="ban"):
            ban(request.args.get("name"))
            return "Accepted", 202
        elif(request.args.get("action")=="unban"):
            unban(request.args.get("name"))
            return "Accepted", 202
        elif(request.args.get("action")=="starter"):
            starter(request.args.get("name"))
            return "Accepted", 202
        elif(request.args.get("action")=="flyer"):
            flyer(request.args.get("name"))
            return "Accepted", 202
        elif(request.args.get("action")=="god"):
            god(request.args.get("name"))
            return "Accepted", 202
        else:
            return "Bad request", 400
    else:
        return "Unauthorized", 401

@app.route("/whitelist", methods= ["GET"])
def whitelist():
    password="null"
    if "pass" in request.headers:
        password=request.headers["pass"]
    if (password==mypass):
        if(request.args.get("action")=="on" or request.args.get("action")=="off"):
            print("Aqui no entro")
            wl_activation(request.args.get("action"))
            return "Accepted", 202
        elif(request.args.get("action")=="add"):
            wl_add(request.args.get("name"))
            return "Accepted", 202
        elif(request.args.get("action")=="add"):
            wl_remove(request.args.get("name"))
            return "Accepted", 202
        else:
            return "Bad request", 400
    else:
        return "Unauthorized", 401

@app.route("/test", methods= ["GET"])
def test():
    sendMessage("Hola chicos")
    return {"Status":"Server stopped", "Date": datetime.now().strftime("%d-%m-%Y_%H:%M")}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345, debug=True)