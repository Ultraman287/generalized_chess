import pygame
import numpy as np
from dataclasses import dataclass
import os
import math

import hashlib
from Helpers.interactive_box import InteractiveBox

from UI.board_create_screen import BOARD_ROWS, BOARD_COLS, BLACK_PIECE, WHITE_PIECE

BOX_COLOR = (217, 217, 217)


class BoxBack(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(56, 52, 165, 54)
        self.text = "Back"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = BOX_COLOR

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return "game_options_screen"


class IndividualBoard(InteractiveBox):
    def __init__(self, board, x, y, w, h, name):
        """
        Initialize an IndividualBoard object.

        Args:
        - board: The image of the board.
        - x: The x-coordinate of the top-left corner of the board.
        - y: The y-coordinate of the top-left corner of the board.
        - w: The width of the board.
        - h: The height of the board.
        - name: The name of the board.

        Attributes:
        - rect: The rectangular area occupied by the board.
        - board: The image of the board.
        - name: The name of the board.
        - text_color: The color of the text.
        - active: A flag indicating whether the board is active or not.
        - color: The color of the board when inactive.
        - color_active: The color of the board when active.
        - color_inactive: The color of the board when inactive.
        """
        self.rect = pygame.Rect(x, y, w, h)
        self.board = board
        self.board = pygame.transform.scale(self.board, (w * 0.97, h * 0.8))
        # self.board = pygame.transform.flip(self.board, True, False)
        self.board = pygame.transform.rotate(self.board, 90)
        self.name = name
        self.text_color = (0, 0, 0)
        self.active = False
        self.color = BOX_COLOR
        self.color_active = (250, 220, 220)
        self.color_inactive = BOX_COLOR

    def get_blit(self):
        """
        Returns a surface that represents the board with the name and piece.

        Returns:
        - surface: The surface representing the board.
        """
        text = pygame.font.SysFont("Arial", self.rect.height // 10).render(
            self.name, True, (0, 0, 0)
        )
        piece = pygame.transform.scale(
            self.board, (self.rect.width, self.rect.height * 0.8)
        )
        piece = pygame.transform.flip(piece, True, False)
        surface = pygame.Surface((self.rect.width, self.rect.height))
        surface.fill(self.color)
        surface.blit(piece, (self.rect.width / 2 - piece.get_width() / 2, 0))
        surface.blit(
            text, (self.rect.width / 2 - text.get_width() / 2, self.rect.height * 0.85)
        )
        return surface

    def draw(self, screen: pygame.Surface):
        """
        Draw the board on the screen.

        Args:
        - screen: The surface to draw on.
        """
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (120, 120, 120), self.rect, 2)

        screen.blit(self.board, self.rect)
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (
                self.rect.x,
                self.rect.y + self.rect.height * 0.8,
                self.rect.width * 0.97,
                self.rect.height * 0.2,
            ),
            2,
        )
        text = pygame.font.SysFont("Arial", self.rect.height // 10).render(
            self.name, True, (0, 0, 0)
        )
        screen.blit(  # blit text onto screen
            text,
            (
                self.rect.x + self.rect.width / 2 - text.get_width() / 2,
                self.rect.y + self.rect.height * 0.85,
            ),
        )

    def handle_event(self, event):
        """
        Handle the given event.

        Args:
        - event: The event to handle.

        Returns:
        - A tuple containing the next screen and the name of the board if the board is clicked, otherwise None.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return "game_screen", self.name


class BoxBoards(InteractiveBox):
    """
    A class representing a collection of boards in a box.

    Attributes:
    - rect: A pygame.Rect object representing the dimensions and position of the box.
    - board_names: A list of strings representing the names of the boards.
    - board_objects: A list of IndividualBoard objects representing the boards.

    Methods:
    - __init__(): Initializes the BoxBoards object.
    - get_all_boards(): Retrieves the names of all the boards.
    - draw(screen, font_size): Draws the box and the boards on the screen.
    - handle_event(event): Handles the event triggered by the user.
    - update(screen): Updates the screen with the box and the boards.
    """

    def __init__(self):
        self.rect = pygame.Rect(56, 124, 688, 420)
        self.board_names = []

        self.get_all_boards()
        num_boards = len(self.board_names)
        col_row_ratio = self.rect.width / self.rect.height

        num_cols = math.ceil(np.sqrt(num_boards * col_row_ratio))
        num_rows = math.ceil(num_boards / num_cols)

        self.board_objects = []

        for ind, board in enumerate(self.board_names):
            x = self.rect.x + (ind % num_cols) * self.rect.width / num_cols
            y = self.rect.y + (ind // num_cols) * self.rect.height / num_rows
            w = self.rect.width / num_cols
            h = self.rect.height / num_rows
            name = self.board_names[ind]
            display = pygame.surfarray.make_surface(
                np.load(f"Boards/{name}.npz")["piece_position"]
            )
            print(f"Board: {display}")
            self.board_objects.append(IndividualBoard(display, x, y, w, h, name))

    def get_all_boards(self):
        """
        Retrieves the names of all the boards from the "Boards" directory.
        """
        self.board_names = []
        for file in os.listdir("Boards"):
            if file.endswith(".npz"):
                name = file.split(".")[0]
                self.board_names.append(name)

    def draw(self, screen, font_size=32):
        """
        Draws the box and the boards on the screen.

        Parameters:
        - screen: The pygame screen object to draw on.
        - font_size: The font size for the board names (default: 32).
        """
        pygame.draw.rect(screen, BOX_COLOR, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        for board in self.board_objects:
            board.draw(screen)

    def handle_event(self, event):
        """
        Handles the event triggered by the user.

        Parameters:
        - event: The pygame event object.

        Returns:
        - A tuple containing the screen name and the name of the selected board.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            for board in self.board_objects:
                if board.handle_event(event):
                    return "game_screen", board.name

    def update(self, screen):
        """
        Updates the screen with the box and the boards.

        Parameters:
        - screen: The pygame screen object to update.
        """
        self.draw(screen)


class GameExistingScreen:
    def __init__(self):
        self.boxes = [BoxBack(), BoxBoards()]

    def handle_event(self, event):
        for box in self.boxes:
            handled_event = box.handle_event(event)
            if handled_event == "game_options_screen":
                return "game_options_screen"
            if (
                handled_event
                and type(handled_event) == tuple
                and handled_event[0] == "game_screen"
            ):
                return handled_event[0], handled_event[1] + ".npz"

    def reset(self):
        self.boxes[1].get_all_boards()

    def update(self, screen):
        screen.fill((198, 198, 198))
        for box in self.boxes:
            box.update(screen)
        pygame.display.flip()
