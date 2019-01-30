import pymunk as pm
import sys, random
import pygame
from pygame.locals import *
import pymunk.pygame_util
import math
import scipy.spatial
from simFuncs import *
from simObjs import *
from math import floor
import matplotlib.pyplot as plt

#---------- Main Method ----------#
def sim(w,w2,theta,theta2,randIn,randIn2, displayOn,pos1,pos2,ssName):
    pygame.init() #initialize all imported pygame modules
    if displayOn:
        screen = pygame.display.set_mode((600,600)) #set screen size (pixels)
    
    pygame.display.set_caption("Simulation") 
    clock = pygame.time.Clock() 
    speed = 20
    #----- Create Space -----#    
    space = pm.Space()
    space.damping = 0.95 

    #----- Create Bots -----# (Params = xLoc, yLoc, Angle)
    bot1 = Bot(pos1[0],pos1[1],pos1[2])
    bot2 = Bot(pos2[0],pos2[1],pos2[2])
    bot1.setSpeed(speed) #makes bot1 move
    bot2.setSpeed(speed)
    
    
    # add objects to sim space
    space.add(bot1.getBody(), bot1.getShape(), [sensor for sensor in bot1.getSensors()], bot2.getBody(), bot2.getShape(), [sensor for sensor in bot2.getSensors()])
    

    # BotHandler processes collision between bots. Bots have a collisionShape of 1 so handles collisions between type 1 and type1).
    botHandler = space.add_collision_handler(1,1)
    bc = botCol(bot1,bot2)
    botHandler.begin = bc.botHit
    botHandler.pre_solve = bc.preSolve
    botHandler.post_solve = bc.postSolve
    botHandler.separate = bc.separate
    #Sensor Handler for sensor to bot collisions.
    sensorHandler = space.add_collision_handler(2,1)
    sh = senseCol(bot1,bot2)
    sensorHandler.begin = sh.sensorHit
    sensorHandler.pre_solve = sh.preSolve
    sensorHandler.post_solve = sh.postSolve
    sensorHandler.separate = sh.separate
    
    
    
    bot1Dist = getDistanceFromCent(bot1.getShape())
    bot2Dist = getDistanceFromCent(bot2.getShape())  
    
    

    #----- Time variables -----#
    dt = 0.01 #time slice

    T = 200 # ammount of time to run for

    time = np.arange(0,T,dt)
    
    #----- set initial conditions -----#
    y = np.zeros((5,len(time)))
    y2 = np.zeros((5,len(time)))
    
    y[:,0]=([bot1.getSpeed()/25,bot1.getAngle()/360,bot1Dist/270,randIn[0],randIn[1]])
    y2[:,0]=([bot2.getSpeed()/25,bot2.getAngle()/360,bot2Dist/270,randIn2[0],randIn2[1]])
        
    y = np.array(y)
    y2 = np.array(y2)

    y = np.matrix(y)
    y2 = np.matrix(y2)
    w = np.matrix(w)
    w2 = np.matrix(w2)
    #----- Fitness Variables -----#
    oob = False
    oob2 = False
    timeStayedIn = 0
    timeStayedIn2 = 0
    bot1Hits = 0
    bot2Hits = 0
    points1 = []
    points2 = []
    points1.append((pos1[0],pos1[1]))
    points2.append((pos2[0],pos2[1]))
    b1Ko = False
    b2Ko = False
    #----- Simulation Loop -----#
    for i in range(1,len(time)):
        if displayOn:
            screen.fill((255,255,255)) # Set background colour
            draw_options = pm.pygame_util.DrawOptions(screen)        
            boundary = pygame.draw.circle(screen, (250,0,0), (300,300), 250, 5)
            if i>1:
                pygame.draw.lines(screen,(0,0,200),False,points1,1)
                pygame.draw.lines(screen,(0,0,0),False,points2,1)
        bot1Dist = getDistanceFromCent(bot1.getShape())

        bot2Dist = getDistanceFromCent(bot2.getShape())
        bot1DistPen = calcDistPen(bot1Dist)
        bot2DistPen = calcDistPen(bot2Dist)
        
        sensorVals = sh.getSenseVals()
        inputs = [sensorVals[0],sensorVals[1],bot1DistPen,1,1]
        inputs2 = [sensorVals[2],sensorVals[3],bot2DistPen,1,1]
        
        inputs = np.array(inputs)
        inputs2 = np.array(inputs2)
        
        inputs = inputs.reshape(5,1)
        inputs2 = inputs2.reshape(5,1)
        
        
        #----- Bot1 Controller -----#
        y[:,i] = y[:,i-1]+dt*(-y[:,i-1]+np.tanh(w*(y[:,i-1])+theta+inputs))
        bot1.setAngle(np.mod(y[:,i][1].item()*360,360))
        bot1.setSpeed(y[:,i][0].item()*25)
        
        #----- Bot2 Controller -----#
        y2[:,i] = y2[:,i-1]+dt*(-y2[:,i-1]+np.tanh(w2*(y2[:,i-1])+theta2+inputs2))
        bot2.setAngle(np.mod(y2[:,i][1].item()*360,360))
        bot2.setSpeed(y2[:,i][0].item()*25)
        
        
        if bot1Dist > 250:
            print 'bot1 oob'
            oob = True
        if not oob:
            timeStayedIn += dt
            
        if bot2Dist > 250:
            print 'bot2 oob'
            oob2 = True
        if not oob2:
            timeStayedIn2 += dt
            
        if bc.getHitter() == 'bot1' and not oob:
            bot1Hits +=1
            if oob2 and not b1Ko:
                b2Ko = True
                print "Bot 2 KOed"
        if bc.getHitter() == 'bot2' and not oob2:
            bot2Hits +=1
            if oob and not b2Ko:
                'Bot 1 KOed'
                b1Ko = True
        if displayOn:
            bot1Pos = pm.pygame_util.to_pygame(bot1.body.position,screen)
            points1.append(bot1Pos)
            bot2Pos = pm.pygame_util.to_pygame(bot2.body.position,screen)
            points2.append(bot2Pos)
            
        bot1.shape.cache_bb()
        bot2.shape.cache_bb()
        space.reindex_shapes_for_body(bot1.body)
        space.reindex_shapes_for_body(bot2.body)
        if displayOn:
            space.debug_draw(draw_options)
        
        #----- THIS LINE IS KEY -----#
        space.step(dt) # step function steps the simulation forward one step in time
        #----- -----#
        if displayOn:
            pygame.display.flip() # updates screen
        
        clock.tick() #ticks clock, parameter determines max fps
    if displayOn:    
        pygame.image.save(screen, ssName+".jpeg")          
    pygame.quit()
    return timeStayedIn,timeStayedIn2,bot1Hits,bot2Hits, b1Ko, b2Ko,y
