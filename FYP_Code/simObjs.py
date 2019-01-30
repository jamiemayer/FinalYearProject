import pymunk as pm
import sys, random
import pygame
from pygame.locals import *
import pymunk.pygame_util
import math
import scipy.spatial
import os


class Bot:
    'Class for bot objects. Includes sensors and actuation values.'
    #----- Instance Variables -----#
    body = None
    shape = None
    sensorL = None
    sensorR = None
    sensorC = None
    speed = None
    angle = None
    
    #----- Methods -----#
    def __init__(self,x,y,angle):
        bodyMoment = pm.moment_for_circle(2,0,20,(0,0))
        self.body = pm.Body(2, bodyMoment, body_type = pm.Body.DYNAMIC)
        self.body.position = (x,y)
        self.body.angle = math.radians(angle)
        self.body.center_of_gravity = ((-.5,0))
        self.angle = angle
        
        self.shape = pm.Circle(self.body,20,(0,0))
        self.shape._set_collision_type(1)
        self.shape.cache_bb()
        self.shape.elasticity = 1
        
        #self.sensorL = pm.Segment(self.body,(10,0),(40,35), .8)
        self.sensorL = pm.Segment(self.body,(10,0),(240,210), .9)
        self.sensorL._set_collision_type(2)
        self.sensorL.color = (50,50,50)
        #self.sensorL.sensor = True
        self.sensorL._set_sensor(True)
        self.sensorL.mass = 0
        #self.sensorR = pm.Segment(self.body, (10,0),(40,-35),.8)
        self.sensorR = pm.Segment(self.body, (10,0),(240,-210),.9)
        self.sensorR._set_collision_type(2)
        self.sensorR.color = (50,50,50)    
        #self.sensorR.sensor = True
        self.sensorR._set_sensor(True)
        self.sensorR.mass = 0
        
    def addSensorC(self):
        self.sensorC = pm.Segment(self.body,(10,0),(320,0),0.9)
        self.sensorC._set_collision_type(2)
        self.sensorC.color = (50,50,50)
        self.sensorC.sensor = True

    def setSpeed(self,speed):
        self.body.velocity = [speed*math.cos(self.body.angle),speed*math.sin(self.body.angle)]
        #self.body.update_velocity(self.body,(0,0),0.95,0.01)
        self.speed = speed
        
    def setAngle(self, angle):
        self.body.angle = math.radians(angle)
        self.angle = angle
    
    def getBody(self):
        return self.body
    
    def getSensors(self):
        if self.sensorC == None:
            return self.sensorL, self.sensorR
        else:
            return self.sensorL, self.sensorR, self.sensorC
        
    def getShape(self):
        return self.shape
    
    def getSpeed(self):
        return self.speed
    
    def getAngle(self):
        return self.angle
    
    
#----- Bot collision Handler -----#
class botCol:
    bot1 = None
    bot2 = None
    hitter = None
    hitee = None
    
    def __init__(self,bot1,bot2):
        self.bot1 = bot1
        self.bot2 = bot2
    
    def botHit(self,arbiter,space,data):
        print 'Engaged!'
        return True
    def preSolve(self,arbiter,space,data):
        return True
    def postSolve(self, arbiter,space,data):
        h = arbiter._get_shapes()[0]
        if h == self.bot1.shape:
            self.hitter = 'bot1'
        elif h == self.bot2.shape:
            self.hitter = 'bot2'
        pass
    def separate(self,arbiter,space,data):
        print 'separate'
        self.hitter = None
        pass
    def getHitter(self):
        return self.hitter
    
#----- Sensor Handler Class -----#
class senseCol:
    b1L = 0
    b1R = 0
    b1C = 0
    b2L = 0
    b2R = 0
    b2C = 0
    bot1 = None
    bot2 = None
    
    def __init__(self,bot1,bot2):
        self.bot1 = bot1
        self.bot2 = bot2
        
    def sensorHit(self,arbiter,space,data):
        return True
    def preSolve(self,arbiter,space,data):
        #print(arbiter._get_shapes())
        if arbiter._get_shapes()[0] == self.bot1.sensorL:
            if arbiter._get_shapes()[1] == self.bot2.shape:
                self.b1L = 1
        elif arbiter._get_shapes()[0] == self.bot1.sensorR:
            if arbiter._get_shapes()[1] == self.bot2.shape:
                self.b1R = 1
        elif arbiter._get_shapes()[0] == self.bot1.sensorC:
            if arbiter._get_shapes()[1] == self.bot2.shape:
                self.b1C = 1
        elif arbiter._get_shapes()[0] == self.bot2.sensorL:
            if arbiter._get_shapes()[1] == self.bot1.shape:
                self.b2L = 1
        elif arbiter._get_shapes()[0] == self.bot2.sensorR:
            if arbiter._get_shapes()[1] == self.bot1.shape:
                self.b2R = 1
        elif arbiter._get_shapes()[0] == self.bot2.sensorC:
            if arbiter._get_shapes()[1] == self.bot1.shape:
                self.b2C = 1    
        
        return True
    def postSolve(self, arbiter,space,data):
        pass
    def separate(self,arbiter,space,data):
        if arbiter._get_shapes()[0] == self.bot1.sensorL:
            self.b1L = 0
        elif arbiter._get_shapes()[0] == self.bot1.sensorR:
            self.b1R = 0
        elif arbiter._get_shapes()[0] == self.bot2.sensorL:
            self.b2L = 0
        elif arbiter._get_shapes()[0] == self.bot2.sensorR:
            self.b2R = 0
    def getSenseVals(self):
        return [self.b1L,self.b1R,self.b2L,self.b2R]