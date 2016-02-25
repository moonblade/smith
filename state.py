#states module
import globalVariables
# States is a json/ dictionay which contains the states possible in the arrangement
# The emission and transmission probability will be stored in state as well
def initStates():
    # Creates the initial configurations of states
    # Loads all emissions into it
    states={}
    states['in']={'emissions':{}}
    states['mismatch']={'emissions':{}}
    states['out']={'emissions':{}}
    
    for i in globalVariables.rawScoreMatrix:
        states['mismatch']['emissions'][i+'-']={'probability':{}}
        states['mismatch']['emissions']['-'+i]={'probability':{}}
        for j in globalVariables.rawScoreMatrix[i]:
            if(j+i in states):
                states[j+i]['emissions'][i+j]={}
                states[j+i]['emissions'][i+j]['probability']={}
            else:
                if(globalVariables.rawScoreMatrix[i][j]==globalVariables.mismatch):
                    states['mismatch']['emissions'][i+j]={}
                    states['mismatch']['emissions'][i+j]['probability']={}
                else:
                    states[i+j]={'emissions':{i+j:{'probability':{}}}}

    globalVariables.states = states

def getState(x,y):
    # Given an emission x,y finds which state it belongs to
    for i in globalVariables.states:
        if(x+y in globalVariables.states[i]['emissions'] or y+x in globalVariables.states[i]['emissions']):
            return i
    return "error"

def initTransitionProbability():
    pass
