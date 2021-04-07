import os, time

def startMinecraft():
    os.system("screen -S minecraft -dm bash start.sh")
    return True

def stopMinecraft():
    sendMessage("Vamos a parar el servidor en 10 segundos.")
    time.sleep(10)
    os.system("screen -S minecraft -p 0 -X stuff 'kick @a^M'")
    os.system("screen -S minecraft -p 0 -X stuff 'save-all^M'")
    time.sleep(3)
    os.system("screen -S minecraft -p 0 -X stuff 'stop^M'")
    return True

def sendMessage(text):
    os.system("screen -S minecraft -p 0 -X stuff 'say {}^M'".format(text))
    return True

def setWeather(weather):
    os.system("screen -S minecraft -p 0 -X stuff 'weather {}^M'".format(weather))
    return True

def setDaytime(daytime):
    os.system("screen -S minecraft -p 0 -X stuff 'time set {}^M'".format(daytime))
    return True