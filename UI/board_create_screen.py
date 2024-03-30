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

"""
This is the Board creation screen that has the following UI elements:
    - Name box
    - Save button
    - Delete button
    - Back button
    - Input box
    - Select box
    - Currently selected box
    - Rows box
    - Cols box
    
    
    This screen is used to create a new board or edit an existing board. You can scroll through the different pieces saved within the database 
    and place them on the board. You can also flip the pieces by clicking on them. You can also delete pieces by right clicking on them.
"""


class BoxName(InteractiveBox):
    """
    This is the box that allows the user to enter the name of the board

    Attributes:
        rect (pygame.Rect): The rectangular area of the box
        text (str): The current text entered in the box
        text_color (tuple): The color of the text
        active (bool): Indicates if the box is currently active (being edited)
        color_active (tuple): The color of the box when active
        color_inactive (tuple): The color of the box when inactive

    Methods:
        handle_event(event): Handles events for the interactive box
    """

    def __init__(self):
        self.rect = pygame.Rect(381, 35, 270, 50)
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


class BoxCols(InteractiveBox):
    """
    Represents a box for entering the number of columns on the chess board.

    Attributes:
    - rect: A pygame.Rect object representing the position and size of the box.
    - text: A string representing the text displayed in the box.
    - text_color: A tuple representing the RGB color value of the text.
    - active: A boolean indicating whether the box is currently active or not.
    - color_active: A tuple representing the RGB color value of the box when active.
    - color_inactive: A tuple representing the RGB color value of the box when inactive.
    """

    def __init__(self):
        self.rect = pygame.Rect(655, 35, 50, 25)
        self.text = "Cols"
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
                    if self.text.isdigit():
                        globals()["BOARD_COLS"] = int(self.text)
                    # BOARD_COLS = int(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if self.text == "Cols":
                        self.text = ""
                    self.text += event.unicode

    def draw(self, screen, font_size=18):
        return super().draw(screen, font_size)

    def update(self, screen, font_size=18):
        return super().update(screen, font_size)


class BoxRows(InteractiveBox):
    """
    Represents a box for entering the number of rows on the chess board.

    Attributes:
    - rect: pygame.Rect object representing the position and size of the box
    - text: string representing the text displayed in the box
    - text_color: tuple representing the RGB color value of the text
    - active: boolean indicating whether the box is currently active or not
    - color_active: tuple representing the RGB color value of the box when active
    - color_inactive: tuple representing the RGB color value of the box when inactive

    Methods:
    - handle_event(event): handles events for the interactive box
    - draw(screen, font_size): draws the box on the screen with the specified font size
    - update(screen, font_size): updates the box on the screen with the specified font size
    """

    def __init__(self):
        self.rect = pygame.Rect(655, 60, 50, 25)
        self.text = "Rows"
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
                    if self.text.isdigit():
                        globals()["BOARD_ROWS"] = int(self.text)
                    # BOARD_ROWS = int(self.text)

                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if self.text == "Rows":
                        self.text = ""
                    self.text += event.unicode

    def draw(self, screen, font_size=18):
        return super().draw(screen, font_size)

    def update(self, screen, font_size=18):
        return super().update(screen, font_size)


class BoxInput(InteractiveBox):
    def __init__(self, mesh=None, alignment=None):
        """
        Initializes the BoardCreateScreen object.

        Args:
            mesh (numpy.ndarray, optional): The piece position mesh. Defaults to None.
            alignment (numpy.ndarray, optional): The piece alignment mesh. Defaults to None.
        """
        self.rect = pygame.Rect(272, 113, 460, 460)
        self.pieces = {}
        self.piece_position_mesh = (
            mesh if mesh is not None else np.zeros((BOARD_ROWS, BOARD_COLS))
        )
        self.piece_alignment_mesh = (
            alignment if alignment is not None else np.zeros((BOARD_ROWS, BOARD_COLS))
        )
        self.chessboard = np.indices((BOARD_COLS, BOARD_ROWS)).sum(axis=0) % 2
        self.kings = []

    def draw(self, screen):
        # Scaling up the mesh to fit the box

        surf = pygame.surfarray.make_surface(self.chessboard)
        surf = pygame.transform.scale(surf, (self.rect.width, self.rect.height))
        # surf = pygame.transform.flip(surf, True, False)

        screen.blit(surf, self.rect)

        pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)

        width_difference = self.rect.width // BOARD_COLS - self.rect.width // 10
        height_difference = self.rect.height // BOARD_ROWS - self.rect.height // 10

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
                    + position[1] * self.rect.width // BOARD_COLS,
                    height_difference // 2
                    + self.rect.top
                    + position[0] * self.rect.height // BOARD_ROWS,
                ),
            )

            if piece.is_king == True:
                pygame.draw.circle(
                    screen,
                    (255, 0, 0),
                    (
                        width_difference // 2
                        + self.rect.left
                        + position[1] * self.rect.width // BOARD_COLS
                        + self.rect.width // 16,
                        height_difference // 2
                        + self.rect.top
                        + position[0] * self.rect.height // BOARD_ROWS
                        + self.rect.height // 16,
                    ),
                    self.rect.width // 80,
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

                    x, y = event.pos
                    row = (y - self.rect.top) // -(-self.rect.height // BOARD_ROWS)
                    col = (x - self.rect.left) // -(-self.rect.width // BOARD_COLS)

                    if 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
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
                                self.pieces[(row, col)] = (
                                    piece.copy()
                                )  # Storing the piece object for faster access
                                print(f"Piece placed at {row}, {col}")

                        elif event.button == 3:
                            self.piece_position_mesh[row][col] = 0
                            self.piece_alignment_mesh[row][col] = 0
                            self.pieces.pop((row, col), None)

                        elif event.button == 2:
                            if (row, col) in self.kings:
                                self.kings.remove((row, col))
                                self.pieces[(row, col)].is_king = False
                            else:
                                self.kings.append((row, col))
                                self.pieces[(row, col)].is_king = True

    def get_pieces_from_hash(self, piece_dictionary):
        """Gets the pieces from the hashes stored in the pickle file"""

        with open(os.path.join(os.getcwd(), "pieces.pkl"), "rb") as f:
            hash_to_piece = pickle.load(f)

            pieces = np.where(self.piece_position_mesh != 0)

            for i, piece in enumerate(zip(pieces[0], pieces[1])):
                r, c = piece
                self.pieces[(r, c)] = piece_dictionary[
                    hash_to_piece[self.piece_position_mesh[r][c]]
                ].copy()


class BoxSelect(InteractiveBox):
    """
    A class representing a box for selecting pieces in a chess game.

    Attributes:
    - rect: A pygame.Rect object representing the dimensions and position of the box.
    - text: A string representing the text inside the box.
    - text_color: A tuple representing the RGB color value of the text.
    - active: A boolean indicating whether the box is currently active or not.
    - color_active: A tuple representing the RGB color value of the box when active.
    - color_inactive: A tuple representing the RGB color value of the box when inactive.
    - y_offset: An integer representing the vertical offset of the pieces inside the box.
    - pieces: A list of IndividualPiece objects representing the available pieces.
    - piece_dictionary: A dictionary mapping piece names to IndividualPiece objects.
    - pieces_surface: A pygame.Surface object representing the surface containing the pieces.

    Methods:
    - get_all_pieces(): Gets all the pieces from the Pieces folder.
    - handle_event(event): Handles the events related to the box.
    - draw(screen): Draws the box and the pieces on the screen.
    - update(screen): Updates the box and the pieces on the screen.
    """

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


class BoxSave(InteractiveBox):
    """
    A class representing a save button box.

    Attributes:
    - rect: A pygame.Rect object representing the position and size of the box.
    - text: A string representing the text displayed on the box.
    - text_color: A tuple representing the RGB color value of the text.
    - active: A boolean indicating whether the box is currently active.
    - color_active: A tuple representing the RGB color value of the box when active.
    - color_inactive: A tuple representing the RGB color value of the box when inactive.
    """

    def __init__(self):
        self.rect = pygame.Rect(163, 35, 93, 50)
        self.text = "Save"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = BOX_COLOR

    def handle_event(self, event, function=None):
        """
        Handles the event triggered by the user.

        Parameters:
        - event: A pygame event object representing the event triggered by the user.
        - function: An optional function to be called when the box is clicked.

        Returns:
        - None
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                if function is not None:
                    function()
        else:
            self.active = False


class BoxBack(InteractiveBox):
    """
    Represents a back button on the board create screen.

    Attributes:
    - rect: A pygame.Rect object representing the position and size of the button.
    - text: A string representing the text displayed on the button.
    - text_color: A tuple representing the RGB color value of the button text.
    - active: A boolean indicating whether the button is currently active.
    - color_active: A tuple representing the RGB color value of the button when active.
    - color_inactive: A tuple representing the RGB color value of the button when inactive.
    - previous_window: A string representing the name of the previous window.

    Methods:
    - handle_event(event): Handles the pygame event and returns the name of the previous window if the button is clicked.
    """

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


class BoxDelete(InteractiveBox):
    """
    Represents a box for deleting a chess board.

    Attributes:
        rect (pygame.Rect): The rectangular area of the box.
        text (str): The text displayed on the box.
        text_color (tuple): The color of the text.
        active (bool): Indicates if the box is active.
        color_active (tuple): The color of the box when active.
        color_inactive (tuple): The color of the box when inactive.
        previous_window (str): The name of the previous window.

    Methods:
        handle_event(event): Handles the event triggered by the user.
    """

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


class BoxCurrentlySelected(InteractiveBox):
    """
    Represents a box that displays the currently selected item.

    Attributes:
        rect (pygame.Rect): The rectangular area of the box.
        text (str): The text to be displayed in the box.
        text_color (tuple): The color of the text.
        active (bool): Indicates whether the box is active or not.
        color_active (tuple): The color of the box when active.
        color_inactive (tuple): The color of the box when inactive.
    """

    def __init__(self):
        self.rect = pygame.Rect(352, 96, 300, 18)
        self.text = "Current Selected: "
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = BOX_COLOR

    def draw(self, screen):
        """
        Draws the box on the screen.

        Args:
            screen (pygame.Surface): The surface to draw on.
        """
        pygame.draw.rect(screen, self.color_inactive, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)
        font = pygame.font.Font(None, 18)

        text_draw = font.render(self.text, 1, self.text_color)
        screen.blit(text_draw, (self.rect.left + 5, self.rect.top + 5))

    def update(self, screen):
        """
        Updates the box on the screen.

        Args:
            screen (pygame.Surface): The surface to update on.
        """
        self.draw(screen)


class BoardCreateScreen:
    def __init__(
        self,
        rows: int = BOARD_ROWS,
        cols: int = BOARD_COLS,
    ):
        """
        Initializes the BoardCreateScreen object.

        Args:
            rows (int): The number of rows on the board. Defaults to BOARD_ROWS.
            cols (int): The number of columns on the board. Defaults to BOARD_COLS.
        """
        self.rows = rows
        self.cols = cols
        self.piece_alignment = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.piece_position_mesh = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.current_mode: str = "draw"
        self.box_name = BoxName()
        self.selected_piece = None
        self.box_back = BoxBack()
        self.box_save = BoxSave()
        self.box_input = BoxInput()
        self.box_delete = BoxDelete()
        self.box_select = BoxSelect()
        self.box_currently_selected = BoxCurrentlySelected()
        self.box_rows = BoxRows()
        self.box_cols = BoxCols()
        self.old_row_col = (BOARD_ROWS, BOARD_COLS)

    def draw(self, screen):
        """Draws the make piece window"""

        self.box_name.draw(screen)
        self.box_back.draw(screen)
        self.box_save.draw(screen)
        self.box_input.draw(screen)
        self.box_delete.draw(screen)
        self.box_select.draw(screen)
        self.box_currently_selected.draw(screen)
        self.box_rows.draw(screen)
        self.box_cols.draw(screen)

    def handle_event(self, event):
        """Handles events for the make piece window"""

        self.box_name.handle_event(event)
        self.box_save.handle_event(event, self.save)
        self.box_delete.handle_event(event)
        self.box_select.handle_event(event)
        self.box_rows.handle_event(event)
        self.box_cols.handle_event(event)

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
        if self.old_row_col != (BOARD_ROWS, BOARD_COLS):
            if self.piece_position.shape != (BOARD_ROWS, BOARD_COLS):
                self.box_input = BoxInput()
                self.piece_position = self.box_input.piece_position_mesh
                self.piece_alignment = self.box_input.piece_alignment_mesh
                self.old_row_col = (BOARD_ROWS, BOARD_COLS)

        self.box_name.update(screen)
        self.box_back.update(screen)
        self.box_save.update(screen)
        self.box_input.update(screen)
        self.box_delete.update(screen)
        self.box_select.update(screen)
        self.box_currently_selected.update(screen)
        self.box_rows.update(screen)
        self.box_cols.update(screen)

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
            globals()["BOARD_ROWS"], globals()["BOARD_COLS"] = np.load(
                os.path.join(os.getcwd(), "Boards", name)
            )["row_col"]
            # self.box_input.pieces = {}
            # self.box_input.piece_position_mesh = self.piece_position
            # self.box_input.piece_alignment_mesh = self.piece_alignment
            self.box_input = BoxInput(
                mesh=self.piece_position, alignment=self.piece_alignment
            )
            self.box_input.get_pieces_from_hash(self.box_select.piece_dictionary)
            self.box_input.kings = [
                (i[0], i[1])
                for i in np.load(os.path.join(os.getcwd(), "Boards", name))["kings"]
            ]
            for r, c in self.box_input.kings:
                self.box_input.pieces[(r, c)].is_king = True
            self.box_back.previous_window = "board_options_screen"
        else:
            self.box_name.text = "Enter Name"
            self.piece_position = np.zeros((BOARD_ROWS, BOARD_COLS))
            self.piece_alignment = np.zeros((BOARD_ROWS, BOARD_COLS))
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
            kings=self.box_input.kings,
            row_col=[BOARD_ROWS, BOARD_COLS],
        )
