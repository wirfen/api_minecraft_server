import os
from funciones.player import *

def wl_activation(action):
    os.system("screen -S minecraft -p 0 -X stuff 'whitelist {}^M'".format(action))
    os.system("screen -S minecraft -p 0 -X stuff 'whitelist reload^M'")
    return True

def wl_add(name):
    os.system("screen -S minecraft -p 0 -X stuff 'whitelist add {}^M'".format(name))
    os.system("screen -S minecraft -p 0 -X stuff 'whitelist reload^M'")
    return True

def wl_remove(name):
    os.system("screen -S minecraft -p 0 -X stuff 'whitelist add {}^M'".format(name))
    os.system("screen -S minecraft -p 0 -X stuff 'whitelist reload^M'")
    return True