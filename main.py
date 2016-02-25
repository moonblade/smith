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
    doStuff()

def doStuff():
    # Initialize the scoring matrix.
    scoreMatrix, startPos = score.initScoreMatrix(globalVariables.seq1,globalVariables.seq2)
    oneAligned, twoAligned = score.traceback(scoreMatrix, startPos)

    assert len(oneAligned) == len(twoAligned), 'aligned strings are not the same size'
    # print(oneAligned)
    # print(twoAligned)


    state.initStates()
    state.initTransitionProbability(oneAligned,twoAligned)
    pp = pprint.PrettyPrinter(depth=6)
    pp.pprint(globalVariables.states)
    # print(globalVariables.states)

if __name__ == '__main__':
    sys.exit(main())
