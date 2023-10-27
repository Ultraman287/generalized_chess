from UI.board_create_screen import PIECE_HEIGHT, PIECE_WIDTH, BLACK_PIECE, WHITE_PIECE


def get_next_move_prompt(
    init_piece_position, init_piece_alignment, game_history, possible_moves, past_games
):
    """Returns a string that is used to prompt the AI to make a move"""
    piece_array = [
        ["" for _ in range(init_piece_position.shape[1])]
        for _ in range(init_piece_position.shape[0])
    ]

    for i in range(init_piece_position.shape[0]):
        for j in range(init_piece_position.shape[1]):
            if init_piece_position[i, j] != 0:
                color = "w" if init_piece_alignment[i, j] == WHITE_PIECE else "b"
                piece_array[i][j] = f"{color}{int(init_piece_position[i, j])}"

    history = "\n".join(game_history)
    possible_moves = "\n".join(possible_moves)

    return f"""

    You are an AI designed to play a game of chess.
    
    This is a modified version of chess. The rules are the same, but the pieces and board are different.
    
    Initially, the board looks like this:
    
    {piece_array}
    
    Below is a list of games that have been played in the past with the same pieces and board that shows the moves that were made alongside
    the result of the game. You can use this to help you make your move.
    
    {past_games}
    
    
    Here is the history of the game so far:
    
    {history}
    
    Here are the possible moves you can make:
    
    {possible_moves}
    
    Please enter your next move in the format: <piece><row><col> -> <row><col>
    """
