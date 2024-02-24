import pygame
import numpy as np
from dataclasses import dataclass
import os
from Helpers.interactive_box import InteractiveBox
import pyspiel

from open_spiel.python.games import mini_chess, mini_chess_helper
from Logic.piece import GamePiece
from Logic.game import GameLogic

BOARD_ROWS, BOARD_COLS = 8, 8
BOX_COLOR = (217, 217, 217)

BLACK_PIECE = 1
WHITE_PIECE = 2


class BackButton(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(15, 200, 700, 100)
        self.text = "Back"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = (217, 217, 217)

    def handle_event(self, event):
        """Handles events for the interactive box"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return "ai_select_screen"

    def draw(self, screen):
        super().draw(screen, font_size=15)


class TrainButton(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(15, 500, 700, 100)
        self.text = "Train AI"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = (217, 217, 217)

    def handle_event(self, event, game=None):
        """Handles events for the interactive box"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if game:
                    mini_chess_helper.debug_main(game)

    def draw(self, screen):
        super().draw(screen, font_size=15)


class AITrainScreen:
    def __init__(self) -> None:
        self.back_button = BackButton()
        self.time_button = InteractiveBox(
            pygame.Rect(15, 400, 700, 100),
            "TRAIN AI",
            (250, 220, 220),
        )
        self.train_button = TrainButton()
        self.pyspiel_game = None
        self.piece_dictionary = {}

    def handle_event(self, event):

        self.train_button.handle_event(event, self.pyspiel_game)
        return self.back_button.handle_event(event)

    def get_all_pieces(self):
        """Gets all the pieces from the Pieces folder"""
        self.pieces = []
        pieces = os.listdir(os.path.join(os.getcwd(), "Pieces"))
        for i, piece in enumerate(pieces):
            cur_piece = GamePiece(
                pygame.surfarray.make_surface(
                    np.load(os.path.join(os.getcwd(), "Pieces", piece))["drawing"]
                ),
                np.transpose(
                    np.load(os.path.join(os.getcwd(), "Pieces", piece))["movement"]
                ),  # HACKY SOLUTION FOR NOW
                piece[:-4],
                (
                    True
                    if np.load(os.path.join(os.getcwd(), "Pieces", piece))[
                        "type_movement"
                    ][0]
                    == 1
                    else False
                ),
            )
            self.pieces.append(cur_piece)
            self.piece_dictionary[cur_piece.name] = cur_piece

    def reset(self, name: str = None):
        if name is not None:
            name_text = name.split("/")[-1][:-4]
            piece_alignment = np.load(os.path.join(os.getcwd(), "Boards", name))[
                "piece_alignment"
            ]
            piece_position = np.load(os.path.join(os.getcwd(), "Boards", name))[
                "piece_position"
            ]
            globals()["BOARD_ROWS"], globals()["BOARD_COLS"] = np.load(
                os.path.join(os.getcwd(), "Boards", name)
            )["row_col"]
            self.game = GameLogic(rows=BOARD_ROWS, cols=BOARD_COLS)
            self.game.kings = (
                (i[0], i[1])
                for i in np.load(os.path.join(os.getcwd(), "Boards", name))["kings"]
            )
            self.game.piece_alignment, self.game.initial_piece_alignment = (
                piece_alignment,
                piece_alignment,
            )
            self.game.piece_position, self.game.initial_piece_position = (
                piece_position,
                piece_position,
            )
            self.get_all_pieces()
            self.game.get_pieces_from_hash(self.piece_dictionary)
            self.game.game_over = False
            self.game.name = name_text

            _GAME_TYPE = game_type(name_text)
            _GAME_INFO = game_info(len(self.pieces) * BOARD_COLS * BOARD_ROWS)
            game = MiniChessGame(
                _GAME_TYPE=_GAME_TYPE,
                _GAME_INFO=_GAME_INFO,
                game_logic=self.game,
                num_pieces=len(self.pieces),
                rows=BOARD_ROWS,
                cols=BOARD_COLS,
            )
            self.pyspiel_game = game

    def update(self, screen):
        screen.fill((198, 198, 198))
        self.back_button.draw(screen)
        self.time_button.draw(screen)
        self.train_button.draw(screen)
        pygame.display.flip()


_NUM_PLAYERS = 2


def game_type(name):
    return pyspiel.GameType(
        short_name=name,
        long_name=name,
        dynamics=pyspiel.GameType.Dynamics.SEQUENTIAL,
        chance_mode=pyspiel.GameType.ChanceMode.DETERMINISTIC,
        information=pyspiel.GameType.Information.PERFECT_INFORMATION,
        utility=pyspiel.GameType.Utility.ZERO_SUM,
        reward_model=pyspiel.GameType.RewardModel.TERMINAL,
        max_num_players=_NUM_PLAYERS,
        min_num_players=_NUM_PLAYERS,
        provides_information_state_string=True,
        provides_information_state_tensor=False,
        provides_observation_string=True,
        provides_observation_tensor=True,
        parameter_specification={},
    )


def game_info(num_distinct_actions, max_game_length=50):
    return pyspiel.GameInfo(
        num_distinct_actions=num_distinct_actions,
        max_chance_outcomes=0,
        num_players=2,
        min_utility=-1.0,
        max_utility=1.0,
        utility_sum=0.0,
        max_game_length=50,
    )


class MiniChessGame(pyspiel.Game):
    """A Python version of Mini Chess.
    The class inherets from pyspiel.Game which contains the scaffolding for the basic functions
    that each game implemented within the open spiel framework must have.
    """

    def __init__(
        self,
        params=None,
        _GAME_TYPE=None,
        _GAME_INFO=None,
        game_logic: GameLogic = None,
        num_pieces: int = 13,
        rows: int = 4,
        cols: int = 4,
    ):
        super().__init__(_GAME_TYPE, _GAME_INFO, params or dict())
        self.game_logic = game_logic
        self.num_pieces = num_pieces
        self.rows = rows
        self.cols = cols

    def new_initial_state(self):
        """Returns a state corresponding to the start of a game."""
        return MiniChessState(self, self.game_logic)

    def make_py_observer(self, iig_obs_type=None, params=None):
        """Returns an object used for observing game state.
        An observer is used to get information about the game state. This is done in the
        form of a tensor which is a 1-D array of floats and a dictionary of views onto the
        tensor. The tensor is indexed by (cell state, row, column). The cell state is a
        one-hot encoding of the piece type and color. The row and column are the position
        of the piece on the board. The dictionary is indexed by strings and is used to
        access the tensor. The strings are the names of the views. The only view is
        "observation" which is the tensor itself.
        """

        return BoardObserver(self.num_pieces, self.rows, self.cols)


class MiniChessState(pyspiel.State):
    """A state object that implements logic underneath for the working of the game
    It keeps track of the current player, the current board state, and whether or not
    the game is over. It also has functions for getting the current player, the legal
    actions, applying an action, and checking if the game is over.
    ."""

    def __init__(
        self,
        game,
        game_logic: GameLogic,
    ):
        """Constructor; should only be called by Game.new_initial_state."""
        super().__init__(game)
        self.game_logic = game_logic

    # OpenSpiel (PySpiel) API functions are below. This is the standard set that
    # should be implemented by every perfect-information sequential-move game.

    def current_player(self):
        """Returns id of the next player to move, or TERMINAL if game is over."""
        cur_player = 0 if self.game_logic.turn == WHITE_PIECE else 1
        return pyspiel.PlayerId.TERMINAL if self.game_logic.game_over else cur_player

    def _legal_actions(self, player):
        """Returns a list of legal actions, sorted in ascending order."""
        return self.game_logic.get_all_possible_moves_action_space()

    def _apply_action(self, action):
        """Applies the specified action to the state.
        This function essentially maps the integer action to the corresponding effect it should
        have on the state of the game. This is done by finding the corresponding piece and movement
        of the piece on the board and then search for where the piece initiatially was and updating the
        board accordingly. The current player is then updated and the game is checked to see if it is over.
        This is easily done by checking if there is only one king left on the board.


        Complexity wise this function is O(m*n) where m is the number of rows and n is the number of columns.
        This is because the function loops through the board to find the piece that is being moved and then
        loops through the board again to find the piece that is being captured. The function could be made
        more efficient by keeping track of the location of the pieces and then updating the board accordingly
        but this would require more memory and would be more complicated to implement.
        """
        self.game_logic.apply_action(action)

    def _action_to_string(self, player, action):
        """Action -> string.
        This just gets the string representation of the action.
        """
        return self.game_logic.action_to_string(action)

    def is_terminal(self):
        """Returns True if the game is over."""
        return self.game_logic.game_over

    def returns(self):
        """Total reward for each player over the course of the game so far."""
        return [1, -1] if self.game_logic.winner == "White" else [-1, 1]

    def __str__(self):
        """String for debug purposes. No particular semantics are required."""
        return self.game_logic.board_to_string()


class BoardObserver:
    """Observer, conforming to the PyObserver interface (see observation.py)."""

    def __init__(self, num_pieces, rows, cols):
        """Initializes an empty observation tensor."""
        # if params:
        #     raise ValueError(f"Observation parameters not supported; passed {params}")
        # The observation should contain a 1-D tensor in `self.tensor` and a
        # dictionary of views onto the tensor, which may be of any shape.
        # Here the observation is indexed `(cell state, row, column)`.
        """
    There are 13 possible pieces that can be on the board with the 4 separate pawns, 8 special
    pieces and empty spaces. The observation is a 1-D tensor of size 208 which is 13*4*4. The
    """
        self.num_pieces = num_pieces
        self.rows = rows
        self.cols = cols
        self.tensor = np.zeros((num_pieces + 1, rows, cols), np.float32)
        self.dict = {
            "observation": np.reshape(self.tensor, (num_pieces + 1, rows, cols))
        }

    def set_from(self, state: MiniChessState, player):
        """Updates `tensor` and `dict` to reflect `state` from PoV of `player`."""
        del player
        # We update the observation via the shaped tensor since indexing is more
        # convenient than with the 1-D tensor. Both are views onto the same memory.
        obs = self.dict["observation"]
        obs.fill(0)

        for piece in state.game_logic.pieces.values():
            obs[piece.id, piece.position[0], piece.position[1]] = 1

        for r in range(self.rows):
            for c in range(self.cols):
                if state.game_logic.piece_position[r, c] == 0:
                    obs[self.num_pieces, r, c] = 1

    def string_from(self, state: MiniChessState, player):
        """Observation of `state` from the PoV of `player`, as a string."""
        del player
        return state.game_logic.board_to_string()


# Register the game with the OpenSpiel library
