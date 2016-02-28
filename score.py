#Module for score related stuff
import globalVariables
import csv
from state import getState
def initScoreMatrix(seq1, seq2):
    rows = len(seq1) + 1
    cols = len(seq2) + 1

    scoreMatrix = [[0 for col in range(cols)] for row in range(rows)]

    # Fill the scoring matrix.
    maxScore = 0
    maxPos   = None    # The row and columbn of the highest score in matrix.
    for i in range(1, rows):
        for j in range(1, cols):
            score = calculateScore(scoreMatrix, i, j,seq1,seq2)
            if score > maxScore:
                maxScore = score
                maxPos   = (i, j)

            scoreMatrix[i][j] = score

    assert maxPos is not None, 'the x, y position with the highest score was not found'

    return scoreMatrix, maxPos

def initRawScoreMatrix():
    with open(globalVariables.scoreMatrix, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        chars = reader.fieldnames
        globalVariables.rawScoreMatrix={}  
        for row in reader:
            char=row[chars[0]]
            row.pop(chars[0])
            globalVariables.rawScoreMatrix[char]=row
    for sub in globalVariables.rawScoreMatrix:
        for key in globalVariables.rawScoreMatrix[sub]:
            globalVariables.rawScoreMatrix[sub][key] = int(globalVariables.rawScoreMatrix[sub][key])

def calculateScore(matrix, x, y,seq1,seq2):
    '''Calculate score for a given x, y position in the scoring matrix.

    The score is based on the up, left, and upper-left neighbors.
    '''
    diagonalScore = matrix[x - 1][y - 1] + globalVariables.rawScoreMatrix[seq1[x-1]][seq2[y-1]]
    upScore   = matrix[x - 1][y] + globalVariables.gap
    leftScore = matrix[x][y - 1] + globalVariables.gap

    return max(0, diagonalScore, upScore, leftScore)

def traceback(scoreMatrix, startPosition, seq1,seq2):
    '''Find the optimal path through the matrix.

    This function traces a path from the bottom-right to the top-left corner of
    the scoring matrix. Each move corresponds to a match, mismatch, or gap in one
    or both of the sequences being aligned. Moves are determined by the score of
    three adjacent squares: the upper square, the left square, and the diagonal
    upper-left square.

    WHAT EACH MOVE REPRESENTS
        diagonal: match/mismatch
        up:       gap in sequence 1
        left:     gap in sequence 2
    '''

    END, DIAG, UP, LEFT = range(4)
    alignedSequenceOne = []
    alignedSequenceTwo = []
    x, y         = startPosition
    move         = nextMove(scoreMatrix, x, y)
    while move != END:
        if move == DIAG:
            alignedSequenceOne.append(seq1[x - 1])
            alignedSequenceTwo.append(seq2[y - 1])
            x -= 1
            y -= 1
        elif move == UP:
            alignedSequenceOne.append(seq1[x - 1])
            alignedSequenceTwo.append('-')
            x -= 1
        else:
            alignedSequenceOne.append('-')
            alignedSequenceTwo.append(seq2[y - 1])
            y -= 1

        move = nextMove(scoreMatrix, x, y)

    alignedSequenceOne.append(seq1[x - 1])
    alignedSequenceTwo.append(seq1[y - 1])

    return ''.join(reversed(alignedSequenceOne)), ''.join(reversed(alignedSequenceTwo))


def nextMove(scoreMatrix, x, y):
    diag = scoreMatrix[x - 1][y - 1]
    up   = scoreMatrix[x - 1][y]
    left = scoreMatrix[x][y - 1]
    if diag >= up and diag >= left:     # Tie goes to the DIAG move.
        return 1 if diag != 0 else 0    # 1 signals a DIAG move. 0 signals the end.
    elif up > diag and up >= left:      # Tie goes to UP move.
        return 2 if up != 0 else 0      # UP move or end.
    elif left > diag and left > up:
        return 3 if left != 0 else 0    # LEFT move or end.
    else:
        # Execution should not reach here.
        raise ValueError('invalid move during traceback')

def alignment_string(aligned_seq1, aligned_seq2):
    # Build the string as a list of characters to avoid costly string
    # concatenation.
    idents, gaps, mismatches = 0, 0, 0
    alignment_string = []
    for base1, base2 in zip(aligned_seq1, aligned_seq2):
        if (getState(base1,base2)=='mismatch'):
            alignment_string.append(' ')
            gaps += 1
        elif (base1+base2=='CG' or base1+base2=='GC'):
            alignment_string.append(':')
            idents += 1
        else:
            alignment_string.append('|')
            mismatches += 1

    return ''.join(alignment_string)

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
