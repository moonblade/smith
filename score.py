#Module for score related stuff
import globalVariables
def initScoreMatrix(seq1, seq2):
    globalVariables.rawScoreMatrix = {'A':{'A':-3,'C':-3,'G':-3,'U':5},'C':{'A':-3,'C':-3,'G':5,'U':-3},'G':{'A':-3,'C':5,'G':-3,'U':2},'U':{'A':5,'C':-3,'G':2,'U':-3}}

    rows = len(globalVariables.seq1) + 1
    cols = len(globalVariables.seq2) + 1

    scoreMatrix = [[0 for col in range(cols)] for row in range(rows)]

    # Fill the scoring matrix.
    maxScore = 0
    maxPos   = None    # The row and columbn of the highest score in matrix.
    for i in range(1, rows):
        for j in range(1, cols):
            score = calculateScore(scoreMatrix, i, j)
            if score > maxScore:
                maxScore = score
                maxPos   = (i, j)

            scoreMatrix[i][j] = score

    assert maxPos is not None, 'the x, y position with the highest score was not found'

    return scoreMatrix, maxPos

def calculateScore(matrix, x, y):
    '''Calculate score for a given x, y position in the scoring matrix.

    The score is based on the up, left, and upper-left neighbors.
    '''
    diagonalScore = matrix[x - 1][y - 1] + globalVariables.rawScoreMatrix[globalVariables.seq1[x-1]][globalVariables.seq2[y-1]]
    upScore   = matrix[x - 1][y] + globalVariables.gap
    leftScore = matrix[x][y - 1] + globalVariables.gap

    return max(0, diagonalScore, upScore, leftScore)

def traceback(scoreMatrix, startPosition):
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
            alignedSequenceOne.append(globalVariables.seq1[x - 1])
            alignedSequenceTwo.append(globalVariables.seq2[y - 1])
            x -= 1
            y -= 1
        elif move == UP:
            alignedSequenceOne.append(globalVariables.seq1[x - 1])
            alignedSequenceTwo.append('-')
            x -= 1
        else:
            alignedSequenceOne.append('-')
            alignedSequenceTwo.append(globalVariables.seq2[y - 1])
            y -= 1

        move = nextMove(scoreMatrix, x, y)

    alignedSequenceOne.append(globalVariables.seq1[x - 1])
    alignedSequenceTwo.append(globalVariables.seq1[y - 1])

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
