import pygame
import numpy as np
from dataclasses import dataclass
import os
import collections
import random
import sys
import pyspiel

from open_spiel.python.algorithms.alpha_zero import alpha_zero
from open_spiel.python.algorithms.alpha_zero import model as model_lib
from open_spiel.python.utils import spawn
from open_spiel.python.algorithms import mcts
from open_spiel.python.algorithms.alpha_zero import evaluator as az_evaluator
from open_spiel.python.algorithms.alpha_zero import model as az_model
from open_spiel.python.bots import gtp
from open_spiel.python.bots import human
from open_spiel.python.bots import uniform_random
from open_spiel.python.games import mini_chess, mini_chess_helper
from Logic.piece import GamePiece
from Logic.game import GameLogic

_NUM_PLAYERS = 2
BOARD_ROWS, BOARD_COLS = 8, 8
BOX_COLOR = (217, 217, 217)

BLACK_PIECE = 1
WHITE_PIECE = 2


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
        self.game = game
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

    def clone(self):
        """Clones the current state."""
        return MiniChessState(self.game, self.game_logic.clone())


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


"""
Below is an altered version of the examples/alpha_zero.py file that is filled with all the
completed flags for the hyperparameters that are going to be used for the mini chess game.

Since the default values were using estimates for the original alphazero paper, something built on much more
data with a much larger action space, I had to change the values to be more appropriate for the mini chess game.
"""


def return_default_az_values(
    name="mini_chess",
    game="mini_chess",
    uct_c=2,
    max_simulations=20,
    train_batch_size=2**5,
    replay_buffer_size=2**8,
    replay_buffer_reuse=3,
    learning_rate=0.1,
    weight_decay=0.0001,
    policy_epsilon=0.25,
    policy_alpha=1,
    temperature=1,
    temperature_drop=10,
    nn_model="mlp",
    nn_width=16,
    nn_depth=5,
    path="./Checkpoints/",
    checkpoint_freq=1,
    actors=2,
    evaluators=1,
    evaluation_window=25,
    eval_levels=7,
    max_steps=0,
    quiet=True,
    verbose=False,
):
    """
    This function returns the default values for the hyperparameters that are going to be used for the
    mini chess game. The default values are based on the implementation of the alpha zero algorithm
    in the open spiel framework.
    """
    return {
        "game": game,
        "uct_c": uct_c,
        "max_simulations": max_simulations,
        "train_batch_size": train_batch_size,
        "replay_buffer_size": replay_buffer_size,
        "replay_buffer_reuse": replay_buffer_reuse,
        "learning_rate": learning_rate,
        "weight_decay": weight_decay,
        "policy_epsilon": policy_epsilon,
        "policy_alpha": policy_alpha,
        "temperature": temperature,
        "temperature_drop": temperature_drop,
        "nn_model": nn_model,
        "nn_width": nn_width,
        "nn_depth": nn_depth,
        "path": path + f"{name}_az/",
        "checkpoint_freq": checkpoint_freq,
        "actors": actors,
        "evaluators": evaluators,
        "evaluation_window": evaluation_window,
        "eval_levels": eval_levels,
        "max_steps": max_steps,
        "quiet": quiet,
        "verbose": verbose,
    }


def debug_alpha_zero(game: pyspiel.Game, default_values: dict):
    config = alpha_zero.Config(
        game=default_values["game"],
        path=default_values["path"],
        learning_rate=default_values["learning_rate"],
        weight_decay=default_values["weight_decay"],
        train_batch_size=default_values["train_batch_size"],
        replay_buffer_size=default_values["replay_buffer_size"],
        replay_buffer_reuse=default_values["replay_buffer_reuse"],
        max_steps=default_values["max_steps"],
        checkpoint_freq=default_values["checkpoint_freq"],
        actors=default_values["actors"],
        evaluators=default_values["evaluators"],
        uct_c=default_values["uct_c"],
        max_simulations=default_values["max_simulations"],
        policy_alpha=default_values["policy_alpha"],
        policy_epsilon=default_values["policy_epsilon"],
        temperature=default_values["temperature"],
        temperature_drop=default_values["temperature_drop"],
        evaluation_window=default_values["evaluation_window"],
        nn_model=default_values["nn_model"],
        nn_width=default_values["nn_width"],
        nn_depth=default_values["nn_depth"],
        eval_levels=default_values["eval_levels"],
        observation_shape=None,
        output_size=None,
        quiet=default_values["quiet"],
    )
    alpha_zero.alpha_zero(
        config, game=game
    )  # this uses open_spiel's built in alpha zero algorithm slightly modified
    # to allow for the game instance to be inputted directly instead of having to build it in separately into the library


"""
This is an altered version of the examples/mcts.py file that is filled with all the
completed flags for the required information for the mcts agent to run on the mini chess game.

In this case, it uses the az_model which is essentially a checkpoint created through prior training with
the alpha zero algorithm. The actual implementation has been abstracted well enough that just by running this
you can play against a well-trained mcts agent on this tiny board from the command line.
"""

mcts_flags = {
    "game": "tic_tac_toe",
    "player1": "human",
    "player2": "az",
    "gtp_path": None,
    "gtp_cmd": [],
    "az_path": "./Checkpoints/",
    "uct_c": 2,
    "rollout_count": 1,
    "max_simulations": 1000,
    "num_games": 1,
    "seed": None,
    "random_first": False,
    "solve": True,
    "quiet": False,
    "verbose": False,
}


def _opt_print(*args, **kwargs):
    if not mcts_flags["quiet"]:
        print(*args, **kwargs)


def _init_bot(bot_type, game, player_id):
    """Initializes a bot by type."""
    rng = np.random.RandomState(mcts_flags["seed"])
    if bot_type == "mcts":
        evaluator = mcts.RandomRolloutEvaluator(mcts_flags["rollout_count"], rng)
        return mcts.MCTSBot(
            game,
            mcts_flags["uct_c"],
            mcts_flags["max_simulations"],
            evaluator,
            random_state=rng,
            solve=mcts_flags["solve"],
            verbose=mcts_flags["verbose"],
        )
    if bot_type == "az":
        model = az_model.Model.from_checkpoint(mcts_flags["az_path"])
        evaluator = az_evaluator.AlphaZeroEvaluator(game, model)
        return mcts.MCTSBot(
            game,
            mcts_flags["uct_c"],
            mcts_flags["max_simulations"],
            evaluator,
            random_state=rng,
            child_selection_fn=mcts.SearchNode.puct_value,
            solve=mcts_flags["solve"],
            verbose=mcts_flags["verbose"],
        )
    if bot_type == "random":
        return uniform_random.UniformRandomBot(player_id, rng)
    if bot_type == "human":
        return human.HumanBot()
    if bot_type == "gtp":
        bot = gtp.GTPBot(game, mcts_flags["gtp_path"])
        for cmd in mcts_flags["gtp_cmd"]:
            bot.gtp_cmd(cmd)
        return bot
    raise ValueError("Invalid bot type: %s" % bot_type)


def _get_action(state, action_str):
    for action in state.legal_actions():
        if action_str == state.action_to_string(state.current_player(), action):
            return action
    return None


def _play_game(game, bots, initial_actions):
    """Plays one game."""
    state = game.new_initial_state()
    _opt_print("Initial state:\n{}".format(state))

    history = []

    if mcts_flags["random_first"]:
        assert not initial_actions
        initial_actions = [
            state.action_to_string(
                state.current_player(), random.choice(state.legal_actions())
            )
        ]

    for action_str in initial_actions:
        action = _get_action(state, action_str)
        if action is None:
            sys.exit("Invalid action: {}".format(action_str))

        history.append(action_str)
        for bot in bots:
            bot.inform_action(state, state.current_player(), action)
        state.apply_action(action)
        _opt_print("Forced action", action_str)
        _opt_print("Next state:\n{}".format(state))

    while not state.is_terminal():
        current_player = state.current_player()
        # The state can be three different types: chance node,
        # simultaneous node, or decision node
        if state.is_chance_node():
            # Chance node: sample an outcome
            outcomes = state.chance_outcomes()
            num_actions = len(outcomes)
            _opt_print("Chance node, got " + str(num_actions) + " outcomes")
            action_list, prob_list = zip(*outcomes)
            action = np.random.choice(action_list, p=prob_list)
            action_str = state.action_to_string(current_player, action)
            _opt_print("Sampled action: ", action_str)
        elif state.is_simultaneous_node():
            raise ValueError("Game cannot have simultaneous nodes.")
        else:
            # Decision node: sample action for the single current player
            bot = bots[current_player]
            action = bot.step(state)
            action_str = state.action_to_string(current_player, action)
            _opt_print(
                "Player {} sampled action: {}".format(current_player, action_str)
            )

        for i, bot in enumerate(bots):
            if i != current_player:
                bot.inform_action(state, current_player, action)
        history.append(action_str)
        state.apply_action(action)

        _opt_print("Next state:\n{}".format(state))

    # Game is now done. Print return for each player
    returns = state.returns()
    print("Returns:", " ".join(map(str, returns)), ", Game actions:", " ".join(history))

    for bot in bots:
        bot.restart()

    return returns, history


def debug_mcts_evaluator(argv, game: pyspiel.Game = None, **kwargs):
    for (
        k,
        v,
    ) in (
        kwargs.items()
    ):  # this is to allow for dynamically changing the flags from where the files getting run
        mcts_flags[k] = v
    if game == None:
        game = pyspiel.load_game(mcts_flags["game"])
    if game.num_players() > 2:
        sys.exit("This game requires more players than the example can handle.")
    bots = [
        _init_bot(mcts_flags["player1"], game, 0),
        _init_bot(mcts_flags["player2"], game, 1),
    ]
    histories = collections.defaultdict(int)
    overall_returns = [0, 0]
    overall_wins = [0, 0]
    game_num = 0
    try:
        for game_num in range(mcts_flags["num_games"]):
            returns, history = _play_game(game, bots, argv[1:])
            histories[" ".join(history)] += 1
            for i, v in enumerate(returns):
                overall_returns[i] += v
                if v > 0:
                    overall_wins[i] += 1
    except (KeyboardInterrupt, EOFError):
        game_num -= 1
        print("Caught a KeyboardInterrupt, stopping early.")
    print("Number of games played:", game_num + 1)
    print("Number of distinct games played:", len(histories))
    print("Players:", mcts_flags["player1"], mcts_flags["player2"])
    print("Overall wins", overall_wins)
    print("Overall returns", overall_returns)
