from funciones.server import *
from funciones.player import *
from funciones.whitelist import *
import os, json, time, random
from flask import Flask, request, send_file
from datetime import datetime
from mcstatus import MinecraftServer

mypass = "123"
servidor = MinecraftServer.lookup("localhost")

app = Flask(__name__)

@app.route("/install", methods = ["POST"])
def install():
    password="null"
    if "pass" in request.headers:
        password=request.headers["pass"]
    if (password==mypass):
        try:
            os.system("cp funciones/server.properties .")
            os.system("wget {} -O server.jar".format(request.get_json()["url"]))
            os.system("mkdir saves backups")
            open("eula.txt","w").write("eula=true")
            open("start.sh","w").write("#!/bin/bash\njava -Xms{}M -Xmx{}M -jar server.jar nogui".format(request.get_json()["min_memory"],request.get_json()["max_memory"]))
            os.system("chmod +x start.sh")
            startMinecraft()
            return "Installed"
        except KeyError:
            return "Bad request", 404
    else:
        return "Unauthorized", 401

@app.route("/server", methods= ["GET"])
def server():
    password="null"
    if "pass" in request.headers:
        password=request.headers["pass"]
    if (password==mypass):
        if(request.args.get("action")=="status"):
            try:
                status=servidor.status()
                query=servidor.query()
                query.players.online
                return {"Ping":status.latency, "Players-Names":"{}".format(", ".join(query.players.names)), "Players":status.players.online}
            except:
                return "Server shutdown", 503
        elif(request.args.get("action")=="msg"):
            sendMessage(request.args.get("condition"))
            return "Server started", 202
        elif(request.args.get("action")=="start"):
            startMinecraft()
            return "Server started", 202
        elif(request.args.get("action")=="stop"):
            stopMinecraft()
            return "Server stoped", 200
        elif(request.args.get("action")=="restart"):
            stopMinecraft()
            startMinecraft()
            return "Server restarted", 202
        elif(request.args.get("action")=="weather"):
            setWeather(request.args.get("condition"))
            return "Weather " + request.args.get("condition"), 200
        elif(request.args.get("action")=="daytime"):
            setDaytime(request.args.get("condition"))
            return "Time is " + request.args.get("action")=="daytime", 200
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
        if(request.args.get("action")=="add"):
            wl_add(request.args.get("name"))
            return request.args.get("name") + " added to whitelist", 200
        elif(request.args.get("action")=="op"):
            operator(request.args.get("name"))
            return request.args.get("name") + " is op", 200
        elif(request.args.get("action")=="deop"):
            deoperator(request.args.get("name"))
            return request.args.get("name") + " is deop", 200
        elif(request.args.get("action")=="survival"):
            survival(request.args.get("name"))
            return request.args.get("name") + " is " + request.args.get("action"), 200
        elif(request.args.get("action")=="creative"):
            creative(request.args.get("name"))
            return request.args.get("name") + " is " + request.args.get("action"), 200
        elif(request.args.get("action")=="spectator"):
            spectator(request.args.get("name"))
            return request.args.get("name") + " is " + request.args.get("action"), 200
        elif(request.args.get("action")=="kick"):
            kick(request.args.get("name"))
            return request.args.get("name") + " is " + request.args.get("action")+"ed", 200
        elif(request.args.get("action")=="ban"):
            ban(request.args.get("name"))
            return request.args.get("name") + " is " + request.args.get("action")+"ned", 200
        elif(request.args.get("action")=="unban"):
            unban(request.args.get("name"))
            return request.args.get("name") + " is " + request.args.get("action")+"ned", 200
        elif(request.args.get("action")=="poor"):
            poor(request.args.get("name"))
            return request.args.get("action") + " for " + request.args.get("name"), 200
        elif(request.args.get("action")=="wood"):
            wood(request.args.get("name"))
            return request.args.get("action") + " for " + request.args.get("name"), 200
        elif(request.args.get("action")=="iron"):
            iron(request.args.get("name"))
            return request.args.get("action") + " for " + request.args.get("name"), 200
        elif(request.args.get("action")=="diamond"):
            diamond(request.args.get("name"))
            return request.args.get("action") + " for " + request.args.get("name"), 200
        elif(request.args.get("action")=="god"):
            god(request.args.get("name"))
            return request.args.get("action") + " for " + request.args.get("name"), 200
        else:
            return "Bad request", 400
    else:
        return "Unauthorized", 401

@app.route("/lists", methods = ["GET"])
def lists():
    password="null"
    if "pass" in request.headers:
        password=request.headers["pass"]
    if (password==mypass):
        if(request.args.get("map")):
            if(os.path.isdir("backups/{}".format(request.args.get("map")))):
                return json.dumps(sorted(os.listdir("backups/" + request.args.get("map")), reverse=True), indent=1), 200
            else:
                return "Backup not found", 404
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
    password="null"
    if "pass" in request.headers:
        password=request.headers["pass"]
    if (password==mypass):
        if(request.args.get("backup")):
            mapa=request.args.get("backup").split("-")[0]
            if(os.path.isfile("backups/{}/{}".format(mapa,request.args.get("backup")))):
                return send_file("backups/{}/{}".format(mapa, request.args.get("backup")), attachment_filename=request.args.get("backup"), as_attachment=True, mimetype="application/tar+gzip")
            else:
                return "File not found", 404
        elif(request.args.get("mapa") and not request.args.get("backup")):
            fecha=datetime.now().strftime("%Y_%m_%d_%H_%M")
            if(os.path.isdir("saves/{}".format(request.args.get("mapa")))):
                os.system("mkdir -p backups/{} && tar -czf backups/{}/{}-{}.tar.gz -C saves/{} .".format(request.args.get("mapa"),request.args.get("mapa"),request.args.get("mapa"),fecha,request.args.get("mapa")))
                return send_file("backups/{}/{}-{}.tar.gz".format(request.args.get("mapa"), request.args.get("mapa"),fecha), attachment_filename=request.args.get("backup"), as_attachment=True, mimetype="application/tar+gzip")
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
                os.system("mkdir -p backups/{}".format(mapa))
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
    password="null"
    if "pass" in request.headers:
        password=request.headers["pass"]
    if (password==mypass):
        properties = open("server.properties").read()
        return properties, 200
    else:
        return "Unauthorized", 401

@app.route("/properties", methods = ["PUT"])
def setProperties():
    password="null"
    if "pass" in request.headers:
        password=request.headers["pass"]
    if (password==mypass):
        open("server.properties","w").write(request.get_data().decode().replace("\n",""))
        properties = open("server.properties").read()
        return properties, 201
    else:
        return "Unauthorized", 401

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

@app.route("/test", methods= ["GET"])
def test():
    sendMessage("Hola chicos")
    return {"Status":"Server Crazy", "Date": datetime.now().strftime("%d-%m-%Y_%H:%M")}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345, debug=True)