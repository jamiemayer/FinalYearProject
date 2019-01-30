import pymunk as pm
import sys, random
import pygame
from pygame.locals import *
import pymunk.pygame_util
import math
import scipy.spatial
from simFuncs import *
from simObjs import *

#---------- Main Method ----------#
def sim(w,theta,randIn, displayOn, pos,ssName):
    pygame.init() #initialize all imported pygame modules
    if displayOn:
        screen = pygame.display.set_mode((600,600)) #set screen size (pixels)
    
    pygame.display.set_caption("Simulation") # Window Caption - Unimportant
    clock = pygame.time.Clock() 
    speed = 20
    #----- Create Space -----#    
    space = pm.Space()
    space.damping = 0.95 

    #----- Create Bots -----# (Params = xLoc, yLoc, Angle)
    #bot1 = Bot(pos1[0],pos1[1],np.random.randint(1,high = 360))
    bot1 = Bot(pos[0],pos[1],pos[2])
    bot2 = Bot(500,300,180)
    bot1.setSpeed(speed) #makes bot1 move
    
    # add objects to sim space
    space.add(bot1.getBody(), bot1.getShape(), [sensor for sensor in bot1.getSensors()])
    #----- Collision Handlers -----#
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
    y[:,0]=([bot1.getSpeed()/25,bot1.getAngle()/360,bot1Dist/270,randIn[0],randIn[1]])
    y = np.array(y)
    #y= y.reshape(3,1)
    y = np.matrix(y)
    w = np.matrix(w)
    #----- Fitness Variables -----#
    oob = False
    timeStayedIn = 0
    #posVec = []
    points = []
    points.append((pos[0],pos[1]))
    #----- Simulation Loop -----#
    for i in range(1,len(time)):
        if displayOn:
            screen.fill((255,255,255)) # Set background colour
            draw_options = pm.pygame_util.DrawOptions(screen)        
            boundary = pygame.draw.circle(screen, (250,0,0), (300,300), 250, 5)
            if i>1:
                pygame.draw.lines(screen,(0,0,0),False,points,1)
        bot1Dist = getDistanceFromCent(bot1.getShape())

        bot2Dist = getDistanceFromCent(bot2.getShape())
        bot1DistPen = calcDistPen(bot1Dist)
        bot2DistPen = calcDistPen(bot2Dist)
        sensorVals = sh.getSenseVals()

        inputs = [sensorVals[0],sensorVals[1],bot1DistPen,1,1]       
        inputs = np.array(inputs)
        inputs = inputs.reshape(5,1)
        y[:,i] = y[:,i-1]+dt*(-y[:,i-1]+np.tanh(w*(y[:,i-1])+theta+inputs))
        bot1.setAngle(np.mod(y[:,i][1].item()*360,360))
        bot1.setSpeed(y[:,i][0].item()*25)
        if bot1Dist > 250:
            oob = True     
        if not oob:
            timeStayedIn += dt
        if displayOn:
            bot1Pos = pm.pygame_util.to_pygame(bot1.body.position,screen)
            points.append(bot1Pos)
        
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
    
    return y, oob, timeStayedIn