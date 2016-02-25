#Module for score related stuff
import globalVariables
def createRawScoreMatrix():
    globalVariables.rawScoreMatrix = {'A':{'A':-3,'C':-3,'G':-3,'U':5},'C':{'A':-3,'C':-3,'G':5,'U':-3},'G':{'A':-3,'C':5,'G':-3,'U':2},'U':{'A':5,'C':-3,'G':2,'U':-3}}

def create_score_matrix(seq1, seq2):
    rows = len(globalVariables.seq1) + 1
    cols = len(globalVariables.seq2) + 1

    score_matrix = [[0 for col in range(cols)] for row in range(rows)]

    # Fill the scoring matrix.
    max_score = 0
    max_pos   = None    # The row and columbn of the highest score in matrix.
    for i in range(1, rows):
        for j in range(1, cols):
            score = calc_score(score_matrix, i, j)
            if score > max_score:
                max_score = score
                max_pos   = (i, j)

            score_matrix[i][j] = score

    assert max_pos is not None, 'the x, y position with the highest score was not found'

    return score_matrix, max_pos

def calc_score(matrix, x, y):
    '''Calculate score for a given x, y position in the scoring matrix.

    The score is based on the up, left, and upper-left neighbors.
    '''
    diag_score = matrix[x - 1][y - 1] + globalVariables.rawScoreMatrix[globalVariables.seq1[x-1]][globalVariables.seq2[y-1]]
    up_score   = matrix[x - 1][y] + globalVariables.gap
    left_score = matrix[x][y - 1] + globalVariables.gap

    return max(0, diag_score, up_score, left_score)

def traceback(score_matrix, start_pos):
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
    aligned_seq1 = []
    aligned_seq2 = []
    x, y         = start_pos
    move         = next_move(score_matrix, x, y)
    while move != END:
        if move == DIAG:
            aligned_seq1.append(globalVariables.seq1[x - 1])
            aligned_seq2.append(globalVariables.seq2[y - 1])
            x -= 1
            y -= 1
        elif move == UP:
            aligned_seq1.append(globalVariables.seq1[x - 1])
            aligned_seq2.append('-')
            x -= 1
        else:
            aligned_seq1.append('-')
            aligned_seq2.append(globalVariables.seq2[y - 1])
            y -= 1

        move = next_move(score_matrix, x, y)

    aligned_seq1.append(globalVariables.seq1[x - 1])
    aligned_seq2.append(globalVariables.seq1[y - 1])

    return ''.join(reversed(aligned_seq1)), ''.join(reversed(aligned_seq2))


def next_move(score_matrix, x, y):
    diag = score_matrix[x - 1][y - 1]
    up   = score_matrix[x - 1][y]
    left = score_matrix[x][y - 1]
    if diag >= up and diag >= left:     # Tie goes to the DIAG move.
        return 1 if diag != 0 else 0    # 1 signals a DIAG move. 0 signals the end.
    elif up > diag and up >= left:      # Tie goes to UP move.
        return 2 if up != 0 else 0      # UP move or end.
    elif left > diag and left > up:
        return 3 if left != 0 else 0    # LEFT move or end.
    else:
        # Execution should not reach here.
        raise ValueError('invalid move during traceback')
