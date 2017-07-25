"""
    Monte Carlo Tic-Tac-Toe Player
    """

import random
import poc_ttt_gui
import poc_ttt_provided as provided
#import poc_simpletest as test

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
# Add your functions here.


def mc_trial(board, player):
    """
        This function takes a current board and the next player to move.
        Randomly select next move and switch between the player until the game
        is over
        """
    while board.check_win() is None:
        empty_squares = board.get_empty_squares()
        move = random.choice(empty_squares)
        board.move(move[0], move[1], player)
        player = provided.switch_player(player)




def mc_update_scores(scores, board, player):
    """
        Calculate the score of each square of the given board and update the
        original gird of scores.
        """
    player_win = board.check_win()
    dim = board.get_dim()
    
    if player_win != provided.DRAW:
        if player == player_win:
            for row in range(dim):
                for col in range(dim):
                    square = board.square(row, col)
                    if square != provided.EMPTY:
                        if square == player:
                            scores[row][col] += SCORE_CURRENT
                        elif square != player:
                            scores[row][col] -= SCORE_OTHER
        elif player != player_win:
            for row in range(dim):
                for col in range(dim):
                    square = board.square(row, col)
                    if square != provided.EMPTY:
                        if square == player:
                            scores[row][col] -= SCORE_CURRENT
                        elif square != player:
                            scores[row][col] += SCORE_OTHER


def get_best_move(board, scores):
    """select a random move based on the current board and calculated scores
        of each cell
        """
    move_list = board.get_empty_squares()
    if len(move_list) != 0:
        score_list = [scores[square[0]][square[1]] for square in move_list]
        max_score = max(score_list)
        best_move_list = [move_list[index] for index in range(len(score_list)) if score_list[index] == max_score]
        best_move = random.choice(best_move_list)
        return best_move
    
    else:
        pass




def mc_move(board, player, trials):
    """
        This function takes a current board, which player the machine player is,
        and the number of trials to run.
        Play the move selected by the get_best_move function
        """
    dim = board.get_dim()
    scores = [[0 for dummy_col in range(dim)] for dummy_row in range(dim)]
    for dummy_trial in range(trials):
        trial_board = board.clone()
        mc_trial(trial_board, player)
        mc_update_scores(scores, trial_board, player)
    
    best_move = get_best_move(board, scores)
    print scores
    print best_move
    return best_move

# Test game with the console or the GUI.  Uncomment whichever
# you prefer.  Both should be commented out when you submit
# for testing to save time.
def test1():
    """
        test the function mc_trial
        """
    test_board = provided.TTTBoard(2, False)
    print test_board
    
    print mc_trial(test_board, provided.PLAYERX)


def test2():
    """
        test the function mc_update_scores
        """
    dim = 4
    board = provided.TTTBoard(dim, False)
    scores = [[0 for col in range(dim)] for row in range(dim)]
    print scores
    test_board = mc_trial(board, provided.PLAYERX)
    print test_board
    mc_update_scores(scores, test_board, provided.PLAYERX)
    print scores

def test3():
    """
        test the funciont get_best_move
        """
    dim = 4
    board = provided.TTTBoard(dim, False)
    scores = [[random.randint(-4, 4) for col in range(dim)] for row in range(dim)]
    print board
    print scores
    print get_best_move(board, scores)

def test4():
    """
        test the function mc_move
        """
    dim = 2
    board = provided.TTTBoard(dim, False)
    print board
    for times in range(2):
        mc_move(board, provided.PLAYERX, NTRIALS)
        print board
        mc_move(board, provided.PLAYERO, NTRIALS)
        print board


provided.play_game(mc_move, NTRIALS, False)
poc_ttt_gui.run_gui(4, provided.PLAYERX, mc_move, NTRIALS, False)
