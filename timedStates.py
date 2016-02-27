# TimedStates Module
import globalVariables
from state import getTransitionProbability
from state import getEmissionProbability
import copy

def getTotalProabilityToState(instance,state):
    probabilityToState=0
    for iteratorState in instance:
        if(state in instance[iteratorState]['transitions']):
            probabilityToState+=instance[iteratorState]['transitions'][state]
    return probabilityToState

def getTimedTransitionProbability(timedStates,state,destinationState,time):
    return getTotalProabilityToState(timedStates[time-1],state)*getTransitionProbability(state,destinationState)

def getTimedEmissionProbability(timedStates,state,emission,time):
    return timedStates[time][state]['probability']*getEmissionProbability(state,emission)

def initTimedStates(states):
    states=copy.deepcopy(states)
    timedStates=[]
    # Convert to only probabilities
    for state in states['in']['transitions']:
        states['in']['transitions'][state]=states['in']['transitions'][state]['probability']
    states['in']['probability']=1.0
    for emission in globalVariables.emissionList:
        states['in']['emissions'][emission]=0.0
    states['in']={'in':states['in']}

    timedStates.append(states['in'])
    runningTill=globalVariables.reverseEndIndex-globalVariables.reverseStartIndex
    for x in range(1,runningTill):
        newState={}
        for state in globalVariables.stateList:
            newState[state]={}
            newState[state]['transitions']={}
            newState[state]['emissions']={}
            newState[state]['probability']=getTotalProabilityToState(timedStates[x-1],state)
            for destinationState in globalVariables.stateList:
                newState[state]['transitions'][destinationState]=getTimedTransitionProbability(timedStates,state,destinationState,x)
        timedStates.append(newState)
        for state in globalVariables.stateList:
            for emission in globalVariables.emissionList:
                timedStates[x][state]['emissions'][emission]=getTimedEmissionProbability(timedStates,state,emission,x)

    finalState={'emissions':{},'probability':getTotalProabilityToState(timedStates[runningTill-1],'out'),'transitions':{}}
    for emission in globalVariables.emissionList:
        finalState['emissions'][emission]=0.0
    for state in globalVariables.stateList:
        finalState['transitions'][state]=0.0
    timedStates.append({'out':finalState})
    return timedStates    
