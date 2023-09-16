import pygame
import numpy as np
from dataclasses import dataclass
import os

import hashlib
from Helpers.interactive_box import InteractiveBox
from UI.piece_existing_screen import IndividualPiece
import math
import pickle

BOARD_ROWS, BOARD_COLS = 8, 8
BOX_COLOR = (217, 217, 217)

PIECE_HEIGHT = 100
PIECE_WIDTH = 140

BLACK_PIECE = 1
WHITE_PIECE = 2


class BoxName(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(381, 35, 351, 50)
        self.text = "Enter Name"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = BOX_COLOR

    def handle_event(self, event):
        """Handles events for the interactive box"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True

        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if self.text == "Enter Name":
                        self.text = ""
                    self.text += event.unicode


box_name = BoxName()


class BoxInput(InteractiveBox):
    def __init__(self, mesh=np.zeros((8, 8))):
        self.rect = pygame.Rect(272, 113, 460, 460)
        self.pieces = {}
        self.piece_position_mesh = mesh
        self.piece_alignment_mesh = np.zeros((8, 8))
        self.chessboard = np.indices((8, 8)).sum(axis=0) % 2

    def draw(self, screen):
        # Scaling up the mesh to fit the box

        surf = pygame.surfarray.make_surface(self.chessboard)
        surf = pygame.transform.scale(surf, (self.rect.width, self.rect.height))
        # surf = pygame.transform.flip(surf, True, False)

        screen.blit(surf, self.rect)

        pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)

        width_difference = self.rect.width // 8 - self.rect.width // 10
        height_difference = self.rect.height // 8 - self.rect.height // 10

        for position, piece in self.pieces.items():
            surf = pygame.transform.scale(
                piece.piece, (self.rect.width // 10, self.rect.height // 10)
            )
            if self.piece_alignment_mesh[position[0]][position[1]] == BLACK_PIECE:
                surf = pygame.transform.flip(surf, True, True)

            screen.blit(
                surf,
                (
                    width_difference // 2
                    + self.rect.left
                    + position[1] * self.rect.width // 8,
                    height_difference // 2
                    + self.rect.top
                    + position[0] * self.rect.height // 8,
                ),
            )

    def update(self, screen):
        self.draw(screen)

    def handle_event(self, event, piece: IndividualPiece = None):
        """Handles events for the interactive box
        Each piece is stored as a tuple (piece_name, is_white) in the mesh and the pieces dictionary
        """
        if piece is not None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    # Calculate the row and column indices corresponding to the mouse click
                    mesh_size = self.piece_position_mesh.shape[0]
                    x, y = event.pos
                    row = (y - self.rect.top) // -(-self.rect.height // mesh_size)
                    col = (x - self.rect.left) // -(-self.rect.width // mesh_size)

                    if 0 <= row < mesh_size and 0 <= col < mesh_size:
                        if event.button == 1:
                            if (
                                self.piece_position_mesh[row][col] != 0
                                and self.piece_position_mesh[row][col] == piece.hash
                            ):
                                self.piece_alignment_mesh[row][col] = (
                                    WHITE_PIECE
                                    if self.piece_alignment_mesh[row][col]
                                    == BLACK_PIECE
                                    else BLACK_PIECE
                                )
                                print(f"Piece flipped at {row}, {col}")
                            else:
                                self.piece_position_mesh[row][col] = piece.hash
                                self.piece_alignment_mesh[row][col] = WHITE_PIECE
                                self.pieces[
                                    (row, col)
                                ] = piece  # Storing the piece object for faster access
                                print(f"Piece placed at {row}, {col}")

                        elif event.button == 3:
                            self.piece_position_mesh[row][col] = 0
                            self.piece_alignment_mesh[row][col] = 0
                            self.pieces.pop((row, col), None)

    def get_pieces_from_hash(self, piece_dictionary):
        """Gets the pieces from the hashes stored in the pickle file"""

        with open(os.path.join(os.getcwd(), "pieces.pkl"), "rb") as f:
            hash_to_piece = pickle.load(f)
            print(hash_to_piece)
            print(self.piece_position_mesh)

            pieces = np.where(self.piece_position_mesh != 0)

            for i, piece in enumerate(zip(pieces[0], pieces[1])):
                r, c = piece
                self.pieces[(r, c)] = piece_dictionary[
                    hash_to_piece[self.piece_position_mesh[r][c]]
                ]


box_input = BoxInput()


class BoxSelect(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(67, 113, 165, 460)
        self.text = ""
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = BOX_COLOR
        self.y_offset = 0
        self.pieces = []
        self.piece_dictionary = {}
        self.get_all_pieces()

    def get_all_pieces(self):
        """Gets all the pieces from the Pieces folder"""
        self.pieces = []
        pieces = os.listdir(os.path.join(os.getcwd(), "Pieces"))
        for i, piece in enumerate(pieces):
            cur_piece = IndividualPiece(
                pygame.surfarray.make_surface(
                    np.load(os.path.join(os.getcwd(), "Pieces", piece))["drawing"]
                ),
                self.rect.x + 40,
                self.rect.y + 2 + i * PIECE_HEIGHT,
                PIECE_WIDTH,
                PIECE_HEIGHT,
                piece[:-4],
            )
            self.pieces.append(cur_piece)
            self.piece_dictionary[cur_piece.name] = cur_piece

        # updating the pieces surface when the pieces are updated
        self.pieces_surface = pygame.Surface((165, PIECE_HEIGHT * len(self.pieces)))
        for i, piece in enumerate(self.pieces):
            self.pieces_surface.blit(
                piece.get_blit(),
                (self.rect.width / 2 - piece.piece.get_width() / 2, i * PIECE_HEIGHT),
            )

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if event.button == 5:
                    self.y_offset += 10
                if event.button == 4:
                    self.y_offset -= 10
                    self.y_offset = max(self.y_offset, 0)
                if event.button == 1:
                    # Find which piece was clicked
                    clicked_y = event.pos[1] - self.rect.y + self.y_offset
                    clicked_piece = math.floor(clicked_y / PIECE_HEIGHT)
                    if clicked_piece < len(
                        self.pieces
                    ):  # Handles the case where the user clicks on the bottom of the box
                        return self.pieces[clicked_piece]

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color_inactive, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        ### Drawing the surface with the offset
        screen.blit(self.pieces_surface, self.rect, (0, self.y_offset, 165, 460))

    def update(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color_inactive, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        screen.blit(self.pieces_surface, self.rect, (0, self.y_offset, 165, 460))


box_select = BoxSelect()


class BoxSave(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(163, 35, 93, 50)
        self.text = "Save"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = BOX_COLOR

    def handle_event(self, event, function=None):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                if function is not None:
                    function()
        else:
            self.active = False


box_save = BoxSave()


class BoxBack(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(268, 35, 102, 50)
        self.text = "Back"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = BOX_COLOR
        self.previous_window = "board_options_screen"

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return self.previous_window


box_back = BoxBack()


class BoxDelete(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(21, 35, 132, 50)
        self.text = "Delete"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = (225, 157, 157)
        self.previous_window = "piece_select_screen"

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if os.path.exists(
                    os.path.join(os.getcwd(), "Boards", box_name.text + ".npz")
                ):
                    os.remove(
                        os.path.join(os.getcwd(), "Boards", box_name.text + ".npz")
                    )


box_delete = BoxDelete()


class BoxCurrentlySelected(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(352, 96, 300, 18)
        self.text = "Current Selected: "
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = BOX_COLOR

    def draw(self, screen):
        pygame.draw.rect(screen, self.color_inactive, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)
        font = pygame.font.Font(None, 18)

        text_draw = font.render(self.text, 1, self.text_color)
        screen.blit(text_draw, (self.rect.left + 5, self.rect.top + 5))

    def update(self, screen):
        self.draw(screen)


box_currently_selected = BoxCurrentlySelected()


class BoardCreateScreen:
    def __init__(
        self,
        rows: int = 8,
        cols: int = 8,
    ):
        self.rows = rows
        self.cols = cols
        self.piece_alignment = np.zeros((8, 8))
        self.piece_position_mesh = np.zeros((8, 8))
        self.current_mode: str = "draw"
        self.box_name = box_name
        self.selected_piece = None
        self.box_back = box_back
        self.box_save = box_save
        self.box_input = box_input
        self.box_delete = box_delete
        self.box_select = box_select
        self.box_currently_selected = box_currently_selected

    def draw(self, screen):
        """Draws the make piece window"""

        self.box_name.draw(screen)
        self.box_back.draw(screen)
        self.box_save.draw(screen)
        self.box_input.draw(screen)
        self.box_delete.draw(screen)
        self.box_select.draw(screen)
        self.box_currently_selected.draw(screen)

    def handle_event(self, event):
        """Handles events for the make piece window"""

        self.box_name.handle_event(event)
        self.box_save.handle_event(event, self.save)
        self.box_delete.handle_event(event)
        self.box_select.handle_event(event)

        selection = self.box_select.handle_event(event)
        if selection is not None:
            self.selected_piece = selection
            self.box_currently_selected.text = f"Current Selected: {selection.name}"

        self.box_input.handle_event(event, self.selected_piece)
        self.piece_position = self.box_input.piece_position_mesh
        self.piece_alignment = self.box_input.piece_alignment_mesh

        return self.box_back.handle_event(event)

    def update(self, screen):
        """Updates the make piece window"""

        self.box_name.update(screen)
        self.box_back.update(screen)
        self.box_save.update(screen)
        self.box_input.update(screen)
        self.box_delete.update(screen)
        self.box_select.update(screen)
        self.box_currently_selected.update(screen)

    def reset(self, name: str = None):
        if name is not None:
            self.box_name.text = name.split("/")[-1][:-4]
            self.box_name.active = False
            self.piece_alignment = np.load(os.path.join(os.getcwd(), "Boards", name))[
                "piece_alignment"
            ]
            self.piece_position = np.load(os.path.join(os.getcwd(), "Boards", name))[
                "piece_position"
            ]
            self.box_input.pieces = {}
            self.box_input.piece_position_mesh = self.piece_position
            self.box_input.piece_alignment_mesh = self.piece_alignment
            self.box_input.get_pieces_from_hash(self.box_select.piece_dictionary)
            self.box_back.previous_window = "board_options_screen"
        else:
            self.box_name.text = "Enter Name"
            self.piece_position = np.zeros((8, 8))
            self.piece_alignment = np.zeros((8, 8))
            self.box_input.pieces = {}
            self.box_input.piece_position_mesh = self.piece_position
            self.box_input.piece_alignment_mesh = self.piece_alignment

            self.box_name.active = False
            self.box_back.previous_window = "board_options_screen"

    def save(self):
        """Saves the piece to the Boards folder"""

        folder = os.path.join(os.getcwd(), "Boards")

        file_name = os.path.join(folder, self.box_name.text + ".npz")

        np.savez(
            file_name,
            piece_alignment=self.piece_alignment,
            piece_position=self.piece_position,
        )
