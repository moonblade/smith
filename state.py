#states module
import globalVariables
# States is a json/ dictionay which contains the states possible in the arrangement
# The emission and transitions probability will be stored in state as well
def initStates():
    # Creates the initial configurations of states
    # Loads all emissions into it
    states= globalVariables.states
    if('in' not in states):
        states['in']={'emissions':{},'transitions':{}}
        globalVariables.stateList.add('in')
    if('mismatch' not in states):
        states['mismatch']={'emissions':{},'transitions':{}}
        globalVariables.stateList.add('mismatch')
    if('out' not in states):
        states['out']={'emissions':{},'transitions':{}}
        globalVariables.stateList.add('out')

    for i in globalVariables.rawScoreMatrix:
        globalVariables.emissionList.add(i+'-')
        globalVariables.emissionList.add('-'+i)
        if(i+'-' not in states['mismatch']['emissions']):
            states['mismatch']['emissions'][i+'-']={'count':0}
        if('-'+i not in states['mismatch']['emissions']):
            states['mismatch']['emissions']['-'+i]={'count':0}
        for j in globalVariables.rawScoreMatrix[i]:
            globalVariables.emissionList.add(j+i)
            globalVariables.emissionList.add(i+j)
            if(j+i in states):
                if(i+j not in states[j+i]['emissions']):
                    states[j+i]['emissions'][i+j]={}
                if('count' not in states[j+i]['emissions'][i+j]):
                    states[j+i]['emissions'][i+j]['count']=0
            else:
                if(globalVariables.rawScoreMatrix[i][j]==globalVariables.mismatch):
                    if(i+j not in states['mismatch']['emissions']):
                        states['mismatch']['emissions'][i+j]={}
                    if('count' not in states['mismatch']['emissions'][i+j]):
                        states['mismatch']['emissions'][i+j]['count']=0
                else:
                    if(i+j not in states):
                        states[i+j]={'emissions':{i+j:{'count':0}},'transitions':{}}
                        globalVariables.stateList.add(i+j)

def getState(x,y):
    # Given an emission x,y finds which state it belongs to
    for i in globalVariables.states:
        if(x+y in globalVariables.states[i]['emissions'] or y+x in globalVariables.states[i]['emissions']):
            return i
    return "error"

def initProbabilities(oneAligned,twoAligned):
    oneRequired=oneAligned[::-1][globalVariables.reverseStartIndex:globalVariables.reverseEndIndex]
    twoRequired=twoAligned[::-1][globalVariables.reverseStartIndex:globalVariables.reverseEndIndex]
    # print(oneRequired)
    # print(twoRequired)

    # Count is set up via looping
    # Count for in from first state
    stateList=['in']
    emissionList=["",]
    for a,b in zip(oneRequired,twoRequired):
        stateList.append(getState(a,b))
        emissionList.append(a+b)
    stateList.append('out')

    for a,b in zip(stateList,emissionList):
        if(b in globalVariables.states[a]['emissions']):
            globalVariables.states[a]['emissions'][b]['count']+=1

    oldX=stateList[0]
    for x in stateList[1:]:
        if(x not in globalVariables.states[oldX]['transitions']):
            globalVariables.states[oldX]['transitions'][x]={'count':0}
        globalVariables.states[oldX]['transitions'][x]['count']+=1
        oldX=x

    #loop through and get probability counts
    for state in globalVariables.states:
        for destinationState in globalVariables.states:
            if('transitions' not in globalVariables.states[state]):
                globalVariables.states[state]['transitions']={}
            if(destinationState not in globalVariables.states[state]['transitions']):
                globalVariables.states[state]['transitions'][destinationState]={'count':0}
            globalVariables.states[state]['transitions'][destinationState]['probability']=getTransitionProbability(state,destinationState)

        for emission in globalVariables.states[state]['emissions']:
            pass

    # find probabilites of emissions
    for state in globalVariables.states:
        for emission in globalVariables.states[state]['emissions']:
            globalVariables.states[state]['emissions'][emission]['probability']=getEmissionProbability(state,emission)

def totalTransitionCount(state):
    totalTransitionCount = 0
    if('transitions' not in globalVariables.states[state]):
        return 0

    for destination in globalVariables.states[state]['transitions']:
        totalTransitionCount+=transitionCount(state,destination)
    return totalTransitionCount

def transitionCount(state,destination):
    if('transitions' not in globalVariables.states[state]):
        return 0    
    if(destination not in globalVariables.states[state]['transitions']):
        return 0
    return globalVariables.states[state]['transitions'][destination]['count']

def getTransitionProbability(state,destinationState):
    # Instead of 0.25 for null, returning zero currently
    if(totalTransitionCount(state)==0):
        return 0
    return (transitionCount(state,destinationState)+1)/(totalTransitionCount(state)+4)
    # return (transitionCount(state,destinationState)/totalTransitionCount(state))

def getTotalEmissionCount(state):
    totalEmissionCount=0
    if('emissions' not in globalVariables.states[state]):
        return 0
    for emission in globalVariables.states[state]['emissions']:
        totalEmissionCount+=getEmissionCount(state,emission)
    return totalEmissionCount

def getEmissionCount(state,emission):
    if(emission not in globalVariables.states[state]['emissions']):
        return 0
    return globalVariables.states[state]['emissions'][emission]['count']

def getEmissionProbability(state,emission):
    if(getTotalEmissionCount(state)==0):
        return 0
    else:
        return getEmissionCount(state,emission)/getTotalEmissionCount(state)
