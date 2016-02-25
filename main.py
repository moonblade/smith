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
    score.createRawScoreMatrix()
    score_matrix, start_pos = score.create_score_matrix(globalVariables.seq1,globalVariables.seq2)
    seq1_aligned, seq2_aligned = score.traceback(score_matrix, start_pos)

    assert len(seq1_aligned) == len(seq2_aligned), 'aligned strings are not the same size'
    print(seq1_aligned)
    print(seq2_aligned)


    state.makeStates()
    print(globalVariables.states)

def print_matrix(matrix):
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
