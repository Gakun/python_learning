"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

ROUND = 0
# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    #global ROUND
    #print '\nROUND: ', ROUND
    #print board
    #ROUND += 1
    if board.check_win() == provided.PLAYERX:
        #print 'Leaf'
        return 1, (-1, -1)
    if board.check_win() == provided.PLAYERO:
        #print 'Leaf'
        return -1, (-1, -1)
    if board.check_win() == provided.DRAW:
        #print 'Leaf'
        return 0, (-1, -1)
    else:
        #print 'Branch'
        poss_move = board.get_empty_squares()
        #print poss_move
        max_score = -1
        real_score = max_score * SCORES[player]
        best_move = (-1, -1)
        for move in poss_move:
            new_board = board.clone()
            new_board.move(move[0], move[1], player)
            result = mm_move(new_board, provided.switch_player(player))
            score= result[0]
            trans_score = score * SCORES[player]
            #print trans_score
            if trans_score == 1:
                return score, move

            elif trans_score > max_score:
                max_score = trans_score
                real_score = score
                best_move = move
        
        return real_score, best_move

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(move_wrapper, 1, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)

#test_board = provided.TTTBoard(3)
#test_board.move(0, 1, provided.PLAYERX)
#test_board.move(1, 1, provided.PLAYERX)
#test_board.move(2, 2, provided.PLAYERX)
#test_board.move(0, 0, provided.PLAYERO)
#test_board.move(1, 0, provided.PLAYERO)
#test_board.move(2, 1, provided.PLAYERO)
#print test_board
#print mm_move(test_board, provided.PLAYERX)