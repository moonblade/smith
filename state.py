#states module
import globalVariables
def makeStates():
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

def getState(states,x,y):
    pass
