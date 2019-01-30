import pickle

def save(fname):
    with open(fname,'w') as f:
        pickle.dump([pop,biases,randIn,fittest],f)
        

def openVars(fname):
    savedVars = pickle.load( open( fname, "r" ) )
    pop = savedVars[0]
    biases = savedVars[1]
    randIn = savedVars[2]
    fittest = savedVars[3]
    return pop,biases,randIn,fittest

#fname =  'great_solution.pickle'

#save(fname)

