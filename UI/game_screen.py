import pygame
import numpy as np
from dataclasses import dataclass
import os
import math
import pickle
import hashlib
from Helpers.interactive_box import InteractiveBox
from UI.piece_existing_screen import IndividualPiece
from UI.board_create_screen import PIECE_HEIGHT, PIECE_WIDTH, BLACK_PIECE, WHITE_PIECE
from Logic.piece import GamePiece
from Logic.game import GameLogic


BOX_COLOR = (217, 217, 217)


class BoxBack(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(57, 79, 146, 58)
        self.text = "Back"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = BOX_COLOR
        self.previous_window = "game_options_screen"

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return self.previous_window


class BoxMode(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(57, 169, 146, 58)
        self.text = "Mode"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = BOX_COLOR

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                print("mode")


class BoxUndo(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(57, 259, 146, 58)
        self.text = "Undo"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = BOX_COLOR

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                print("undo")


class BoxRedo(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(57, 349, 146, 58)
        self.text = "Redo"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = BOX_COLOR

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                print("redo")


class BoxSave(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(57, 439, 146, 58)
        self.text = "Save"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = BOX_COLOR

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                print("save")


class BoxInput:
    def __init__(self, row=8, col=8):
        self.rect = pygame.Rect(259, 79, 460, 460)
        self.chessboard = np.indices((row, col)).sum(axis=0) % 2
        self.game = GameLogic(rows=row, cols=col)
        self.rows, self.cols = row, col

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # Calculate the row and column indices corresponding to the mouse click
                mesh_size = self.game.piece_position.shape[0]
                x, y = event.pos
                row = (y - self.rect.top) // -(-self.rect.height // mesh_size)
                col = (x - self.rect.left) // -(-self.rect.width // mesh_size)

                print(f"row: {row}, col: {col}")

                self.game.handle_press(row, col)

    def draw(self, screen):
        if self.game.game_over:
            font = pygame.font.SysFont("Arial", 40)
            text = font.render(
                f"Game Over! {self.game.winner} wins!", True, (255, 255, 255)
            )
            screen.blit(
                text,
                (
                    self.rect.left + self.rect.width // 2 - text.get_width() // 2,
                    self.rect.top + self.rect.height // 2 - text.get_height() // 2,
                ),
            )
        else:
            surf = pygame.surfarray.make_surface(self.chessboard)
            surf = pygame.transform.scale(surf, (self.rect.width, self.rect.height))
            # surf = pygame.transform.flip(surf, True, False)

            screen.blit(surf, self.rect)

            pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)

            width_difference = self.rect.width // self.cols - self.rect.width // int(
                self.cols * 1.2
            )
            height_difference = self.rect.height // self.rows - self.rect.height // int(
                self.rows * 1.2
            )

            for position, piece in self.game.pieces.items():
                surf = pygame.transform.scale(
                    piece.piece,
                    (
                        self.rect.width // int(self.cols * 1.2),
                        self.rect.height // int(self.rows * 1.2),
                    ),
                )
                if self.game.piece_alignment[position[0]][position[1]] == BLACK_PIECE:
                    surf = pygame.transform.flip(surf, True, True)

                screen.blit(
                    surf,
                    (
                        width_difference // 2
                        + self.rect.left
                        + position[1] * self.rect.width // self.cols,
                        height_difference // 2
                        + self.rect.top
                        + position[0] * self.rect.height // self.rows,
                    ),
                )

                if piece.is_king:
                    pygame.draw.circle(
                        screen,
                        (255, 0, 0),
                        (
                            width_difference // 2
                            + self.rect.left
                            + position[1] * self.rect.width // self.cols
                            + self.rect.width // (self.cols * 2),
                            height_difference // 2
                            + self.rect.top
                            + position[0] * self.rect.height // self.rows
                            + self.rect.height // (self.rows * 2),
                        ),
                        self.rect.width // 80,
                    )

            # Adding a low opacity white rectangle to the selected piece

            if self.game.selected_piece is not None:
                selected_filter = pygame.Surface(
                    (
                        self.rect.width // int(self.cols * 1.2),
                        self.rect.height // int(self.rows * 1.2),
                    )
                )
                selected_filter.set_alpha(100)
                selected_filter.fill((255, 255, 255))
                screen.blit(
                    selected_filter,
                    (
                        width_difference // 2
                        + self.rect.left
                        + self.game.selected_piece.position[1]
                        * self.rect.width
                        // self.cols,
                        height_difference // 2
                        + self.rect.top
                        + self.game.selected_piece.position[0]
                        * self.rect.height
                        // self.rows,
                    ),
                )

            # Adding a low opacity green rectangle to the valid moves

            for position in self.game.piece_can_move_to:
                valid_move_filter = pygame.Surface(
                    (
                        self.rect.width // int(self.cols * 1.2),
                        self.rect.height // int(self.rows * 1.2),
                    )
                )
                valid_move_filter.set_alpha(100)
                valid_move_filter.fill((0, 255, 0))
                screen.blit(
                    valid_move_filter,
                    (
                        width_difference // 2
                        + self.rect.left
                        + position[1] * self.rect.width // self.cols,
                        height_difference // 2
                        + self.rect.top
                        + position[0] * self.rect.height // self.rows,
                    ),
                )

    def update(self, screen):
        self.draw(screen)


class GameScreen:
    def __init__(self):
        self.back = BoxBack()
        self.mode = BoxMode()
        self.undo = BoxUndo()
        self.redo = BoxRedo()
        self.save = BoxSave()
        self.screen = BoxInput()
        self.boxes = [
            self.back,
            self.mode,
            self.undo,
            self.redo,
            self.save,
            self.screen,
        ]
        self.piece_alignment = np.zeros((8, 8))
        self.piece_position = np.zeros((8, 8))
        self.piece_dictionary = {}
        self.get_all_pieces()

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
                True
                if np.load(os.path.join(os.getcwd(), "Pieces", piece))["type_movement"][
                    0
                ]
                == 1
                else False,
            )
            self.pieces.append(cur_piece)
            self.piece_dictionary[cur_piece.name] = cur_piece

    def handle_event(self, event):
        for box in self.boxes:
            next_window = box.handle_event(event)
            if next_window:
                return next_window

    def update(self, screen):
        for box in self.boxes:
            box.update(screen)

    def reset(self, name, history=None):
        if history is None:
            self.piece_alignment = np.load(os.path.join(os.getcwd(), "Boards", name))[
                "piece_alignment"
            ]
            self.piece_position = np.load(os.path.join(os.getcwd(), "Boards", name))[
                "piece_position"
            ]

            # print(self.boxes[5].game.kings)
            print(np.load(os.path.join(os.getcwd(), "Boards", name))["kings"])
            rows, cols = np.load(os.path.join(os.getcwd(), "Boards", name))["row_col"]
            self.boxes[5] = BoxInput(rows, cols)
            self.boxes[5].game.kings = (
                (i[0], i[1])
                for i in np.load(os.path.join(os.getcwd(), "Boards", name))["kings"]
            )
            self.boxes[5].game.piece_alignment = self.piece_alignment
            self.boxes[5].game.piece_position = self.piece_position
            self.boxes[5].game.get_pieces_from_hash(self.piece_dictionary)
            self.boxes[5].game.game_over = False
