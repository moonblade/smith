#states module
import globalVariables
# States is a json/ dictionay which contains the states possible in the arrangement
# The emission and transmission probability will be stored in state as well
def initStates():
    # Creates the initial configurations of states
    # Loads all emissions into it
    states={}
    states['in']={'emissions':{},'transmissions':{}}
    states['mismatch']={'emissions':{},'transmissions':{}}
    states['out']={'emissions':{},'transmissions':{}}
    
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
                    states[i+j]={'emissions':{i+j:{'probability':{}}},'transmissions':{}}

    globalVariables.states = states

def getState(x,y):
    # Given an emission x,y finds which state it belongs to
    for i in globalVariables.states:
        if(x+y in globalVariables.states[i]['emissions'] or y+x in globalVariables.states[i]['emissions']):
            return i
    return "error"

def initTransitionProbability(oneAligned,twoAligned):
    oneRequired=oneAligned[::-1][globalVariables.reverseStartIndex:globalVariables.reverseEndIndex]
    twoRequired=twoAligned[::-1][globalVariables.reverseStartIndex:globalVariables.reverseEndIndex]
    # print(oneRequired)
    # print(twoRequired)

    # Count is set up via looping
    # Count for in from first state
    stateList=['in']
    for a,b in zip(oneRequired,twoRequired):
        stateList.append(getState(a,b))
    stateList.append('out')

    oldX=stateList[0]
    for x in stateList[1:]:
        if(x not in globalVariables.states[oldX]['transmissions']):
            globalVariables.states[oldX]['transmissions'][x]={'count':0}
        globalVariables.states[oldX]['transmissions'][x]['count']+=1
        oldX=x

    #loop through and get probability counts
    for state in globalVariables.states:
        for destinationState in globalVariables.states:
            if('transmission' not in globalVariables.states[state]):
                globalVariables.states[state]['transmission']={}
            if(destinationState not in globalVariables.states[state]['transmission']):
                globalVariables.states[state]['transmission'][destinationState]={'count':0}
            probability = (transmissionCount(state,destinationState)+1)/(totalCount(state)+4)
            globalVariables.states[state]['transmission'][destinationState]['probability']=probability

def totalCount(state):
    totalCount = 0
    if('transmission' not in globalVariables.states[state]):
        return 0

    for destination in globalVariables.states[state]['transmission']:
        totalCount+=transmissionCount(state,destination)
    return totalCount

def transmissionCount(state,destination):
    if('transmission' not in globalVariables.states[state]):
        return 0    
    if(destination not in globalVariables.states[state]['transmission']):
        return 0
    return globalVariables.states[state]['transmission'][destination]['count']

def getTransitionProbability(stateX,stateY):
    #get probability from counts
    # if('transmission' in globalVariables.states[state]):
    #     for destination in globalVariables.states[state]['transmission']:
    #         probability = (totalCount(state)+1)/(transmissionCount(destination)+4)
    #         print(state+destination+probability)
    # else:
    #     if()
    #     return 1/4
    pass