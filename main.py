#!/bin/python
import argparse
import os
import re
import sys
import state
import score
import globalVariables

def main():

    # Initialize the scoring matrix.
    scoreMatrix, startPos = score.initScoreMatrix(globalVariables.seq1,globalVariables.seq2)
    oneAligned, twoAligned = score.traceback(scoreMatrix, startPos)

    assert len(oneAligned) == len(twoAligned), 'aligned strings are not the same size'
    print(oneAligned)
    print(twoAligned)


    state.initStates()
    # print(globalVariables.states)
def printMatrix(matrix):
    '''Print the scoring matrix.

    ex:
    0   0   0   0   0   0
    0   2   1   2   1   2
    0   1   1   1   1   1
    0   0   3   2   3   2
    0   2   2   5   4   5
    0   1   4   4   7   6
    '''
    for row in matrix:
        for col in row:
            print('{0:>4}'.format(col),end="",flush=True)
        print()

if __name__ == '__main__':
    sys.exit(main())
