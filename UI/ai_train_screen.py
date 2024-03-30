import pygame
import numpy as np
from dataclasses import dataclass
import os
from Helpers.interactive_box import InteractiveBox
import pyspiel

from open_spiel.python.games import mini_chess, mini_chess_helper
from Logic.piece import GamePiece
from Logic.game import GameLogic
from Helpers.spiel_helper import (
    game_type,
    game_info,
    MiniChessGame,
    MiniChessState,
    BoardObserver,
    return_default_az_values,
    debug_alpha_zero,
)

BOARD_ROWS, BOARD_COLS = 8, 8
BOX_COLOR = (217, 217, 217)

BLACK_PIECE = 1
WHITE_PIECE = 2


class BackButton(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(300, 50, 200, 100)
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
        super().draw(screen, font_size=25)


class TrainButton(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(300, 200, 200, 100)
        self.text = "Train AI"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = (217, 217, 217)

    def handle_event(self, event, game=None, name=None, steps=500):
        """Handles events for the interactive box"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if game:
                    default_values = return_default_az_values(
                        name=name, max_steps=steps
                    )
                    debug_alpha_zero(game, default_values)

    def draw(self, screen):
        super().draw(screen, font_size=25)


class TimeInput(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(300, 400, 200, 50)
        self.text = "Enter number of steps"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = (217, 217, 217)

    def handle_event(self, event):
        """Handles events for the interactive box"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True

        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    if self.text.isdigit():
                        globals()["BOARD_COLS"] = int(self.text)
                    # BOARD_COLS = int(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if self.text == "Enter number of steps":
                        self.text = ""
                    self.text += event.unicode

    def draw(self, screen):
        super().draw(screen, font_size=25)


class TimeButton(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(300, 350, 200, 50)
        self.text = "How long to train?"
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
        super().draw(screen, font_size=25)


class RandomGameButton(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(300, 500, 200, 50)
        self.text = "Random Game"
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
        super().draw(screen, font_size=25)


class PlayButton(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(300, 550, 200, 50)
        self.text = "Play Game"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = (217, 217, 217)

    def handle_event(self, event, game=None, name=None):
        """Handles events for the interactive box"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if game:
                    path = "./Checkpoints/" + name + "_az/checkpoint-0"
                    mini_chess_helper.debug_mcts_evaluator(
                        [],
                        game=game,
                        az_path=path,
                    )

    def draw(self, screen):
        super().draw(screen, font_size=25)


class AITrainScreen:
    def __init__(self) -> None:
        self.back_button = BackButton()
        self.time_button = TimeButton()
        self.train_button = TrainButton()
        self.time_input = TimeInput()
        self.random_game_button = RandomGameButton()
        self.play_button = PlayButton()
        self.pyspiel_game = None
        self.piece_dictionary = {}

    def handle_event(self, event):
        """Handles events for the screen"""
        self.time_input.handle_event(event)
        self.train_button.handle_event(
            event,
            game=self.pyspiel_game,
            name=self.game.name,
            steps=(
                int(self.time_input.text)
                if self.time_input.text != "Enter number of steps"
                else 500
            ),
        )
        self.play_button.handle_event(
            event, game=self.pyspiel_game, name=self.game.name
        )
        self.random_game_button.handle_event(event, game=self.pyspiel_game)
        return self.back_button.handle_event(event)

    def get_all_pieces(self):
        """Gets all the pieces from the Pieces folder"""
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
            _GAME_INFO = game_info(len(self.game.pieces) * BOARD_COLS * BOARD_ROWS)
            game = MiniChessGame(
                _GAME_TYPE=_GAME_TYPE,
                _GAME_INFO=_GAME_INFO,
                game_logic=self.game,
                num_pieces=len(self.game.pieces),
                rows=BOARD_ROWS,
                cols=BOARD_COLS,
            )
            self.pyspiel_game = game

    def update(self, screen):
        screen.fill((198, 198, 198))
        self.back_button.draw(screen)
        self.time_button.draw(screen)
        self.train_button.draw(screen)
        self.time_input.draw(screen)
        self.random_game_button.draw(screen)
        self.play_button.draw(screen)
        pygame.display.flip()
