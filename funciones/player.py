import os
from funciones.whitelist import *

def operator(name):
    os.system("screen -S minecraft -p 0 -X stuff 'op {}^M'".format(name))
    return True

def deoperator(name):
    os.system("screen -S minecraft -p 0 -X stuff 'deop {}^M'".format(name))
    return True

def kick(name):
    os.system("screen -S minecraft -p 0 -X stuff 'kick {}^M'".format(name))
    wl_remove(name)
    return True

def ban(name):
    wl_remove(name)
    deoperator(name)
    os.system("screen -S minecraft -p 0 -X stuff 'kill {}^M'".format(name))
    os.system("screen -S minecraft -p 0 -X stuff 'ban {}^M'".format(name))
    return True

def unban(name):
    os.system("screen -S minecraft -p 0 -X stuff 'pardon {}^M'".format(name))
    wl_add(name)
    return True

def survival(name):
    os.system("screen -S minecraft -p 0 -X stuff 'gamemode survival {}^M'".format(name))
    return True

def creative(name):
    os.system("screen -S minecraft -p 0 -X stuff 'gamemode creative {}^M'".format(name))
    return True

def spectator(name):
    os.system("screen -S minecraft -p 0 -X stuff 'gamemode spectator {}^M'".format(name))
    return True

def starter(name):
    os.system("screen -S minecraft -p 0 -X stuff 'clear {}^M'".format(name))
    os.system("screen -S minecraft -p 0 -X stuff 'give {} minecraft:wooden_axe^M'".format(name))
    os.system("screen -S minecraft -p 0 -X stuff 'give {} minecraft:wooden_pickaxe^M'".format(name))
    os.system("screen -S minecraft -p 0 -X stuff 'give {} minecraft:leather_helmet^M'".format(name))
    os.system("screen -S minecraft -p 0 -X stuff 'give {} minecraft:leather_chestplate^M'".format(name))
    os.system("screen -S minecraft -p 0 -X stuff 'give {} minecraft:leather_leggings^M'".format(name))
    os.system("screen -S minecraft -p 0 -X stuff 'give {} minecraft:leather_boots^M'".format(name))
    os.system("screen -S minecraft -p 0 -X stuff 'give {} minecraft:torch 10^M'".format(name))
    os.system("screen -S minecraft -p 0 -X stuff 'give {} minecraft:cooked_beef 10^M'".format(name))
    
def god(name):
    os.system("screen -S minecraft -p 0 -X stuff 'clear {}^M'".format(name))
    os.system("screen -S minecraft -p 0 -X stuff 'give " + name + " netherite_sword{Enchantments:[{id:sharpness,lvl:5},{id:looting,lvl:3},{id:sweeping,lvl:3},{id:unbreaking,lvl:3},{id:mending,lvl:1}]}^M'")
    os.system("screen -S minecraft -p 0 -X stuff 'give " + name + " netherite_pickaxe{Enchantments:[{id:efficiency,lvl:5},{id:fortune,lvl:3},{id:unbreaking,lvl:3},{id:mending,lvl:1}]}^M'")
    os.system("screen -S minecraft -p 0 -X stuff 'give " + name + " netherite_axe{Enchantments:[{id:sharpness,lvl:5},{id:efficiency,lvl:5},{id:silk_touch,lvl:1},{id:unbreaking,lvl:3},{id:mending,lvl:1}]}^M'")
    os.system("screen -S minecraft -p 0 -X stuff 'give " + name + " netherite_helmet{Enchantments:[{id:protection,lvl:4},{id:unbreaking,lvl:3},{id:thorns,lvl:3},{id:respiration,lvl:3},{id:mending,lvl:1}]}^M'")
    os.system("screen -S minecraft -p 0 -X stuff 'give " + name + " netherite_chestplate{Enchantments:[{id:protection,lvl:4},{id:unbreaking,lvl:3},{id:thorns,lvl:3},{id:mending,lvl:1}]}^M'")
    os.system("screen -S minecraft -p 0 -X stuff 'give " + name + " netherite_leggings{Enchantments:[{id:protection,lvl:4},{id:unbreaking,lvl:3},{id:thorns,lvl:3},{id:mending,lvl:1}]}^M'")
    os.system("screen -S minecraft -p 0 -X stuff 'give " + name + " netherite_boots{Enchantments:[{id:protection,lvl:4},{id:unbreaking,lvl:3},{id:thorns,lvl:3},{id:soul_speed,lvl:3},{id:feather_falling,lvl:4},{id:depth_strider,lvl:3},{id:mending,lvl:1}]}^M'")
    os.system("screen -S minecraft -p 0 -X stuff 'give {} minecraft:torch 64^M'".format(name))
    os.system("screen -S minecraft -p 0 -X stuff 'give {} minecraft:cooked_beef 64^M'".format(name))
    os.system("screen -S minecraft -p 0 -X stuff 'give " + name + " shield{Enchantments:[{id:unbreaking,lvl:3},{id:mending,lvl:1}]}^M'")
    os.system("screen -S minecraft -p 0 -X stuff 'give " + name + " netherite_shovel{Enchantments:[{id:efficiency,lvl:5},{id:unbreaking,lvl:3},{id:mending,lvl:1}]} 1^M'")