from open_spiel.python.games import mini_chess
import pyspiel

pyspiel.register_game(mini_chess._GAME_TYPE, mini_chess.MiniChessGame)
game = pyspiel.load_game("python_mini_chess")
mini_chess.debug_main(game)
