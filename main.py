#!/bin/python
import argparse
import os
import re
import sys
import state
import timedStates
import score
import globalVariables
import pprint
import csv
import upper

# Convert to UpperCase
upper.toUpper(globalVariables.csvFile)
# Replace T with U
os.system('sed -i s/T/U/g '+globalVariables.csvFile)

def main():
    # for later looping
    score.initRawScoreMatrix()
    with open(globalVariables.csvFile, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        names=reader.fieldnames
        for row in reader:
            # Assuming that the sequences will be in the first two rows
            # Compute probabilities with sequence 1 and reverse of sequence 2
            doStuff(row[names[0]],row[names[1]][::-1])
    globalVariables.timedStates=timedStates.initTimedStates(globalVariables.states)

    # print(globalVariables.stateList)
    # print(globalVariables.emissionList)
    
    pp = pprint.PrettyPrinter(depth=6)
    # pp.pprint(globalVariables.states)
    # pp.pprint(globalVariables.timedStates[6])
    count=1
    outputList=[]
    with open(globalVariables.inputcsv, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        names=reader.fieldnames
        for row in reader:
            # Assuming that the sequences will be in the first two rows
            # Compute probabilities with sequence 1 and reverse of sequence 2
            seq1=row[names[0]]
            seq2=row[names[1]]
            scoreMatrix, startPos = score.initScoreMatrix(seq1,seq2)
            alinedOne, alinedTwo = score.traceback(scoreMatrix, startPos, seq1,seq2)
            alignmentString=score.alignment_string(alinedOne,alinedTwo)
            place=globalVariables.reverseEndIndex-globalVariables.reverseStartIndex-1
            stateNeeded=state.getState(alinedOne[::-1][place],alinedTwo[::-1][place])
            print(count)
            print(alinedOne)
            print(alignmentString)
            print(alinedTwo)
            print()
            outputList.append(str(count)+","+stateNeeded+","+str(globalVariables.timedStates[place][stateNeeded]['probability']))
            count+=1
    print()
    for line in outputList:
        print(line)
def doStuff(seq1,seq2):
    # Initialize the scoring matrix.
    scoreMatrix, startPos = score.initScoreMatrix(seq1,seq2)
    oneAligned, twoAligned = score.traceback(scoreMatrix, startPos, seq1,seq2)

    assert len(oneAligned) == len(twoAligned), 'aligned strings are not the same size'
    # print(oneAligned)
    # print(twoAligned)

    state.initStates()
    state.initProbabilities(oneAligned,twoAligned)
    
if __name__ == '__main__':
    sys.exit(main())
