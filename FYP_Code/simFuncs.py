import pymunk as pm
import sys, random
import pygame
from pygame.locals import *
import pymunk.pygame_util
import math
import scipy.spatial
import numpy as np


def createArena():
    arenaBody = pm.Body(0,0,body_type=pm.Body.STATIC)
    arenaBody.position = (300,300)
    arenaBody.friction = 0
    arenaBody.moment =pm.inf
    arena = pm.Circle(arenaBody, 245,(0,0))
    arena.sensor = True
    arena.color=(255,255,255)
    arena.layers = 0

    return arena


def randomMovement(bot,speed):
    if math.degrees(bot.body.angle)>0 and math.degrees(bot.body.angle) <360:
        bot.body.angle+=math.radians(random.randint(0,360))
        bot.body.velocity = [speed*math.cos(bot.body.angle),speed*math.sin(bot.body.angle)]
    elif math.degrees(bot.body.angle)<=0:
        bot.body.angle+= math.radians(10)
        bot.body.velocity = [speed*math.cos(bot.body.angle),speed*math.sin(bot.body.angle)]
    elif math.degrees(bot.body.angle)>=360:
        bot.body.angle+= math.radians(-10)
        bot.body.velocity = [speed*math.cos(bot.body.angle),speed*math.sin(bot.body.angle)]

def outOfBounds(bot, arenaBody):
    if ((bot.body.position[0] - arenaBody.position[0])**2 + (bot.body.position[1] - arenaBody.position[1])**2) >= 245**2:
        bot.color = (255,0,0)
        return True
    else:
        return False

def getDistanceFromCent(bot):
    botX,botY = bot.body.position
    botPos = [botX,botY]
    distance = float(scipy.spatial.distance.euclidean(botPos,[300,300]))
    return distance
        
    #print(distance)
    return distance

def calcDistPen(dist):
    if dist<=200 and dist>=0:
        return 0
    elif dist<=245 and dist >=0:
        return 1
    else:
        return float("inf") #???

def botColStop(arbiter,space,data):
    print("separated")

def botCollision(arbiter,space,data):
    print("collision")
    
    
def getRandPos():
    angle = np.random.rand()*np.pi*2
    x = (np.cos(angle)*245)+300
    y = (np.sin(angle)*245)+300
    return[x,y]