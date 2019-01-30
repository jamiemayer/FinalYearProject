# GA.Py
# Main function that has GA

import numpy as np
from FinalYearProject import *
import matplotlib.pyplot as plt
import fightGA as fGA
from varPickle import openVars



def fightFit(tsi,b1h,b2h,b1Ko,b2Ko):
    fit = [0,0]
    # If tsi1 > tsi2 then fit1 will be positive and vice versa
    #fit[0] = tsi[0] - tsi[1]
    #fit[1] = tsi[1] - tsi[0]
    fit[0]+=b1h/1000
    fit[1]+=b2h/1000
    if b1Ko:
        fit[1]+= 100000
    if b2Ko:
        fit[0]+= 100000
    if fit[0]==fit[1]:
        r = np.random.randint(0,2)
        fit[r]+=1
    return fit
    
    
#----call this to evolve to fight----#
def fightGA(popSize,numGens):
    # Import fittest from prev GA
    #pop1,biases1,randIn1,fittest1 = openVars('50_200_1.pickle')
    pop2,biases2,randIn2,fittest2 = openVars('cands1.pickle')
    pop1,biases1,randIn1,fittest1 = openVars('cands2.pickle')
    pop3,biases3,randIn3,fittest3 = openVars('cands3.pickle')
    pop4,biases4,randIn4,fittest4 = openVars('cands4.pickle')
    pop5,biases5,randIn5,fittest5 = openVars('cands5.pickle')
    # Add to new pop
    newPop = []
    newPop.append(pop1[fittest1])
    newPop.append(pop2[fittest2])
    newPop.append(pop3[fittest3])
    newPop.append(pop4[fittest4])
    newPop.append(pop5[fittest5])
    
    ri = randIn1[fittest1]
    randIn = []
    randIn.append(ri)
    ri = randIn2[fittest2]
    randIn.append(ri)
    ri = randIn3[fittest3]
    randIn.append(ri)
    ri = randIn4[fittest4]
    randIn.append(ri)
    ri = randIn5[fittest5]
    randIn.append(ri)
    
    b = biases1[fittest1]
    biases = []
    biases.append(b)
    b = biases2[fittest2]
    biases.append(b)
    b = biases3[fittest3]
    biases.append(b)
    b = biases4[fittest4]
    biases.append(b)    
    b = biases5[fittest5]
    biases.append(b)
    
    nextGen = []
    nextBiases = []
    nextRandIn = []
    fittest = 0
    secondFittest = 0
    bestCand = 0
    bestCand2 = 0
    for i in range(popSize-5):
        for j in range((popSize-5)/5):
            newPop.append(pCrossover(newPop[j]))
            randIn.append(randIn[j]+np.random.randn()/100)
            biases.append(biases[j]+np.random.randn()/100)
    newPop = np.array(newPop)
    biases = np.array(biases)
    randIn = np.array(randIn)
    
    bestFit = 0
    bestFit2 = 0
    
    bestCand = 0
    bestCand2 = 0

    for j in range(popSize*numGens):
        print 'Gen ',j,' start'
        cand1 = np.random.randint(0,popSize)
        cand2 = np.random.randint(0,popSize)
        while cand1 == cand2:
            cand2 = np.random.randint(0,popSize)
        tsi, tsi2,b1h,b2h,b1Ko,b2Ko,y = fGA.sim(newPop[cand1],newPop[cand2],biases[cand1], biases[cand2],randIn[cand1],randIn[cand2],False,(100,300,360),(500,300,180),None)
        fit = fightFit([tsi,tsi2],b1h,b2h,b1Ko,b2Ko)[0]
        fit2 = fightFit([tsi,tsi2],b1h,b2h,b1Ko,b2Ko)[1]
        tsi, tsi2,b1h,b2h,b1Ko,b2Ko,y = fGA.sim(newPop[cand2],newPop[cand1],biases[cand2], biases[cand1],randIn[cand2],randIn[cand1],False,(100,300,360),(500,300,180),None)
        fit += fightFit([tsi,tsi2],b1h,b2h,b1Ko,b2Ko)[1]            
        fit = fit/2
        fit2 += fightFit([tsi,tsi2],b1h,b2h,b1Ko,b2Ko)[0]
        fit2 = fit2/2
        if fit>fit2:
            newPop[cand2] = pCrossover(newPop[cand1])
            biases[cand2] = biases[cand1]+np.random.randn()/100
            randIn[cand2] = randIn[cand1]+np.random.randn()/100
            if fit>bestFit:
                bestFit = fit
                bestCand = cand1
            elif fit>bestFit2:
                bestFit2 = fit
                bestCand2 = cand1
        elif fit2>fit:
            newPop[cand1] = pCrossover(newPop[cand2])
            biases[cand1] = biases[cand2]+np.random.randn()/100
            randIn[cand1] = randIn[cand2]+np.random.randn()/100
            if fit2>bestFit:
                bestFit = fit2
                bestCand = cand2
            elif fit2>bestFit2:
                bestFit2 = fit2
                bestCand2 = cand2

    tsi, tsi2,b1h,b2h,b1Ko,b2Ko,y = fGA.sim(newPop[bestCand],newPop[bestCand2],biases[bestCand], biases[bestCand2],randIn[bestCand],randIn[bestCand2],True,(100,300,360),(500,300,180),'test')
    fGA.sim(newPop[bestCand2],newPop[bestCand2],biases[bestCand2], biases[bestCand],randIn[bestCand2],randIn[bestCand],True,(100,300,360),(500,300,180),'test2')
    return y
    
            

#---- Fitness Function ----#
def fitness(oob,y,tsi):
    fitVal = 0
    if not oob:
        fitVal +=1
    fitVal+=np.mean(y[0])/2
    fitVal += (tsi/400) #time spent inside
    return fitVal



def pCrossover(weightMat):
        return weightMat+(np.random.randn()/100)    

def initPop():
    W = np.random.randn(N,N)
    #W = np.random.uniform(-2.0,2.0,(N,N))           
    
    return W




#-----Evolve to stay inside-----#
N = 5
popSize = 4
numGens = 1

# ----- Initialise weight vectors to random values -----# 
pop = []
for i in range(popSize):
    weights = initPop()
    pop.append(weights)

#biases = [np.random.rand(N,1) for i in range(popSize)]
biases = [0 for i in range(popSize)]
#----- Randomly generated inputs for other 2 nodes, these will be replaced with sensor values when bot trained to fight -----#
randIn = [np.random.randn(2) for i in range(popSize)]


fitnessVals = []
fitOverTime = []

boxPlotVals = []
bestFitness = 0
fittest = 0
for j in range(popSize*numGens):
    #----- Run sim with current weights -----#
    print 'iteration',j
    fitBeforeAv = 0
    rand1 = np.random.randint(0,popSize)
    y,oob,tsi = sim(pop[rand1],biases[rand1],randIn[rand1],False,(100,300,360),None)
    y = np.matrix.tolist(y)
    y = np.array(y)
    fitBeforeAv+=fitness(oob,y,tsi)
    y,oob,tsi = sim(pop[rand1],biases[rand1],randIn[rand1],False,(500,300,180),None)
    y = np.matrix.tolist(y)
    y = np.array(y)
    fitBeforeAv+=fitness(oob,y,tsi)
    cand1Fit = fitBeforeAv/2
    
    fitBeforeAv = 0
    rand2 = np.random.randint(0,popSize)
    while rand1 == rand2:
        rand2 = np.random.randint(0,popSize)
    y,oob,tsi = sim(pop[rand2],biases[rand2],randIn[rand2],False,(100,300,360),None)
    y = np.matrix.tolist(y)
    y = np.array(y)
    fitBeforeAv+=fitness(oob,y,tsi)
    y,oob,tsi = sim(pop[rand2],biases[rand2],randIn[rand2],False,(500,300,180),None)
    y = np.matrix.tolist(y)
    y = np.array(y)
    fitBeforeAv+=fitness(oob,y,tsi)
    cand2Fit = fitBeforeAv/2 
    
 
    if cand1Fit>cand2Fit:
        pop[rand2] = pCrossover(pop[rand1])
        randIn[rand2] = randIn[rand1]+(np.random.randn()/100)
        biases[rand2] = biases[rand1]+(np.random.randn()/100)
        if cand1Fit > bestFitness:
            fittest = rand1
            bestFitness = cand1Fit
                
    elif cand2Fit>cand1Fit:
        pop[rand1] = pCrossover(pop[rand2])
        randIn[rand1] = randIn[rand2]+(np.random.randn()/100)
        biases[rand1] = biases[rand2]+(np.random.randn()/100)
        if cand2Fit>bestFitness:
            fittest = rand2
            bestFitness = cand2Fit

    if np.mod(j,popSize) == 0:
        fitOverTime.append(bestFitness)


plt.plot(fitOverTime)
sim(pop[fittest],biases[fittest],randIn[fittest],True,(100,300,360),"screen1_30_60_3")
sim(pop[fittest],biases[fittest],randIn[fittest],True,(500,300,180),"screen2_30_60_3")
#-----------------------------------------#
