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
    pickle.dump(globalVariables.states,open(globalVariables.statesFile,"wb"))
    pickle.dump(globalVariables.timedStates,open(globalVariables.timedStatesFile,"wb"))
    pickle.dump(globalVariables.rawScoreMatrix,open(globalVariables.scoreMatrixFile,"wb"))
    # print(globalVariables.stateList)
    # print(globalVariables.emissionList)
    
    # pp.pprint(globalVariables.states)
    # pp.pprint(globalVariables.timedStates[6])

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
