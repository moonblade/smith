#!/bin/python
import argparse
import os
import re
import sys
import state
import score
import globalVariables
import pprint

def main():
    # for later looping
    for seq1,seq2 in zip(globalVariables.seq1,globalVariables.seq2):
        doStuff(seq1,seq2)
    pp = pprint.PrettyPrinter(depth=6)
    pp.pprint(globalVariables.states)
    # print(globalVariables.states)


def doStuff(seq1,seq2):
    # Initialize the scoring matrix.
    scoreMatrix, startPos = score.initScoreMatrix(seq1,seq2)
    oneAligned, twoAligned = score.traceback(scoreMatrix, startPos, seq1,seq2)

    assert len(oneAligned) == len(twoAligned), 'aligned strings are not the same size'
    print(oneAligned)
    print(twoAligned)

    state.initStates()
    state.initProbabilities(oneAligned,twoAligned)
    
if __name__ == '__main__':
    sys.exit(main())
