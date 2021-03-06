#!/usr/bin/python3
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
import pickle

# Convert to UpperCase
upper.toUpper(globalVariables.inputcsv)
# Replace T with U
os.system('sed -i s/T/U/g '+globalVariables.inputcsv)

def main():
    count=1
    outputList=[]

    globalVariables.rawScoreMatrix = pickle.load(open(globalVariables.scoreMatrixFile,"rb"))
    globalVariables.states = pickle.load(open(globalVariables.statesFile,"rb"))
    globalVariables.timedStates = pickle.load(open(globalVariables.timedStatesFile,"rb"))
    # print(globalVariables.rawScoreMatrix)
    # print(globalVariables.states)
    # print(globalVariables.timedStates)
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

if __name__ == '__main__':
    sys.exit(main())
