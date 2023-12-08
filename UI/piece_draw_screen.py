import pygame
import numpy as np
from dataclasses import dataclass
import os
import pickle
from Helpers.interactive_box import InteractiveBox

import hashlib

BOARD_ROWS, BOARD_COLS = 8, 8
BOX_COLOR = (217, 217, 217)

BLACK, WHITE, CENTER, WALK = 0, 255, 60, 15

TOTAL_EXPECTED_PIECES = 1000


class BoxName(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(340, 43, 320, 50)
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


class BoxPhase(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(670, 43, 100, 50)
        self.text = "Contiguous"
        self.text2 = "Movement"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = BOX_COLOR
        self.type_movement = np.array([0])

    def handle_event(self, event):
        """Handles events for the interactive box"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                if self.type_movement == np.array([0]):
                    self.type_movement = np.array([1])
                    self.text = "Phased"
                else:
                    self.type_movement = np.array([0])
                    self.text = "Contiguous"

    def draw(self, screen):
        super().draw(screen, 16)
        font = pygame.font.Font(None, 16)
        text2 = font.render(self.text2, 1, self.text_color)
        screen.blit(text2, (self.rect.left + 5, self.rect.top + 5 + 16))

    def update(self, screen):
        super().update(screen, 16)
        font = pygame.font.Font(None, 16)
        text2 = font.render(self.text2, 1, self.text_color)
        screen.blit(text2, (self.rect.left + 5, self.rect.top + 5 + 16))


box_phase = BoxPhase()


class BoxDrawandMove(InteractiveBox):
    def __init__(self):
        self.rect_draw = pygame.Rect(73, 184, 186, 65)
        self.rect_move = pygame.Rect(73, 280, 186, 65)
        self.text_draw = "Draw"
        self.text_move = "Move"
        self.text_color = (0, 0, 0)
        self.active_color = (250, 220, 220)
        self.inactive_color = BOX_COLOR
        self.active_draw = True

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.active_color if self.active_draw else self.inactive_color,
            self.rect_draw,
        )
        pygame.draw.rect(screen, (0, 0, 0), self.rect_draw, 2)
        pygame.draw.rect(
            screen,
            self.inactive_color if self.active_draw else self.active_color,
            self.rect_move,
        )
        pygame.draw.rect(screen, (0, 0, 0), self.rect_move, 2)
        font = pygame.font.Font(None, 32)

        text_draw = font.render(self.text_draw, 1, self.text_color)
        screen.blit(text_draw, (self.rect_draw.left + 5, self.rect_draw.top + 5))

        text_move = font.render(self.text_move, 1, self.text_color)
        screen.blit(text_move, (self.rect_move.left + 5, self.rect_move.top + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect_draw.collidepoint(event.pos):
                self.active_draw = True
            elif self.rect_move.collidepoint(event.pos):
                self.active_draw = False

    def update(self, screen):
        pygame.draw.rect(
            screen,
            self.active_color if self.active_draw else self.inactive_color,
            self.rect_draw,
        )
        pygame.draw.rect(screen, (0, 0, 0), self.rect_draw, 2)
        pygame.draw.rect(
            screen,
            self.inactive_color if self.active_draw else self.active_color,
            self.rect_move,
        )
        pygame.draw.rect(screen, (0, 0, 0), self.rect_move, 2)
        font = pygame.font.Font(None, 32)

        text_draw = font.render(self.text_draw, 1, self.text_color)
        screen.blit(text_draw, (self.rect_draw.left + 5, self.rect_draw.top + 5))

        text_move = font.render(self.text_move, 1, self.text_color)
        screen.blit(text_move, (self.rect_move.left + 5, self.rect_move.top + 5))


box_draw_and_move = BoxDrawandMove()


class BoxInput(InteractiveBox):
    def __init__(self, mesh=np.zeros((64, 64))):
        if mesh.shape == (64, 64):
            self.rect = pygame.Rect(331, 116, 448, 448)
        else:
            self.rect = pygame.Rect(331, 116, 420, 420)
        self.current_mesh = mesh

    def draw(self, screen):
        # Scaling up the mesh to fit the box
        x, y = self.current_mesh.shape

        scaled_mesh = np.kron(self.current_mesh, np.ones((-(-420 // x), -(-420 // y))))

        surf = pygame.surfarray.make_surface(scaled_mesh)
        screen.blit(surf, (331, 116))

    def update(self, screen):
        x, y = self.current_mesh.shape
        scaled_mesh = np.kron(self.current_mesh, np.ones((-(-420 // x), -(-420 // y))))

        surf = pygame.surfarray.make_surface(scaled_mesh)
        screen.blit(surf, (331, 116))

    def handle_event(self, event):
        if self.current_mesh.shape == (64, 64):
            if pygame.mouse.get_pressed()[0]:
                try:
                    if self.rect.collidepoint(event.pos):
                        # Calculate the row and column indices corresponding to the mouse click
                        mesh_size = self.current_mesh.shape[0]
                        x, y = event.pos
                        row = (y - self.rect.top) // -(-420 // mesh_size)
                        col = (x - self.rect.left) // -(-420 // mesh_size)

                        # Update the value in the current_mesh to represent the drawing
                        self.current_mesh[col, row] = 255
                except AttributeError:
                    pass
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    # Calculate the row and column indices corresponding to the mouse click
                    mesh_size = self.current_mesh.shape[0]
                    x, y = event.pos
                    row = (y - self.rect.top) // -(-420 // mesh_size)
                    col = (x - self.rect.left) // -(-420 // mesh_size)

                    # Update the value in the current_mesh to represent the drawing
                    if self.current_mesh[col, row] != CENTER:
                        if event.button == 1:
                            self.current_mesh[col, row] = WALK
                            # if self.current_mesh[col, row] == PHASE:
                            #     self.current_mesh[col, row] = WALK
                            # else:
                            #     self.current_mesh[
                            #         col, row
                            #     ] = PHASE  # You can set this value based on your drawing needs
                        if event.button == 3:
                            if self.current_mesh[col, row] == BLACK:
                                self.current_mesh[col, row] = WHITE
                            else:
                                self.current_mesh[col, row] = BLACK


box_input = BoxInput()

movement_matrix = (np.indices((15, 15)).sum(axis=0) % 2) * 255
movement_matrix[7, 7] = 60

box_input_2 = BoxInput(movement_matrix.copy())  # This is the default movement matrix


class BoxSave(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(73, 470, 186, 65)
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
        self.rect = pygame.Rect(73, 375, 186, 65)
        self.text = "Back"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = BOX_COLOR
        self.previous_window = "piece_select_screen"

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return self.previous_window


box_back = BoxBack()


class BoxDelete(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(73, 93, 186, 65)
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
                    os.path.join(os.getcwd(), "Pieces", box_name.text + ".npz")
                ):
                    os.remove(
                        os.path.join(os.getcwd(), "Pieces", box_name.text + ".npz")
                    )
                    with open("pieces.pkl", "rb") as f:
                        pieces = pickle.load(f)
                        pieces[
                            int(hashlib.sha1(box_name.text.encode()).hexdigest(), 16)
                            % TOTAL_EXPECTED_PIECES
                        ] = None


box_delete = BoxDelete()


class MakePiece:
    """
    Represents a class for creating and manipulating chess pieces.

    Attributes:
        rows (int): The number of rows on the chessboard.
        cols (int): The number of columns on the chessboard.
        movement (np.ndarray): The movement matrix of the piece.
        drawing (np.ndarray): The drawing matrix of the piece.
        type_movement (np.ndarray): The type movement matrix of the piece.
        current_mode (str): The current mode of the piece.
        box_name: The box for entering the name of the piece.
        box_draw_and_move: The box for selecting the draw or move mode.
        box_back: The box for going back to the previous window.
        box_save: The box for saving the piece.
        box_input: The box for inputting the drawing matrix.
        box_input_2: The box for inputting the movement matrix.
        box_delete: The box for deleting the piece.
        box_phase: The box for selecting the phase of the piece.
    """

    def __init__(
        self,
        rows: int = 8,
        cols: int = 8,
        movement: np.ndarray = np.zeros((15, 15)),
        drawing: np.ndarray = np.zeros((64, 64)),
    ):
        self.rows = rows
        self.cols = cols
        self.movement = movement
        self.drawing = drawing
        self.type_movement = np.array([0])
        self.current_mode: str = "draw"
        self.box_name = box_name
        self.box_draw_and_move = box_draw_and_move
        self.box_back = box_back
        self.box_save = box_save
        self.box_input = box_input
        self.box_input_2 = box_input_2
        self.box_delete = box_delete
        self.box_phase = box_phase

    def draw(self, screen):
        """Draws the make piece window"""

        self.box_name.draw(screen)
        self.box_draw_and_move.draw(screen)
        self.box_back.draw(screen)
        self.box_save.draw(screen)
        if self.box_draw_and_move.active_draw:
            self.box_input.draw(screen)
        else:
            self.box_input_2.draw(screen)
        self.box_delete.draw(screen)
        self.box_phase.draw(screen)

    def handle_event(self, event):
        """Handles events for the make piece window"""

        self.box_name.handle_event(event)
        self.box_draw_and_move.handle_event(event)
        if self.box_draw_and_move.active_draw:
            self.box_input.handle_event(event)
            self.drawing = self.box_input.current_mesh
        else:
            self.box_input_2.handle_event(event)
            self.movement = self.box_input_2.current_mesh
        self.box_save.handle_event(event, self.save)
        self.box_delete.handle_event(event)
        self.box_phase.handle_event(event)

        self.type_movement = self.box_phase.type_movement

        return self.box_back.handle_event(event)

    def update(self, screen):
        """Updates the make piece window"""

        self.box_name.update(screen)
        self.box_draw_and_move.update(screen)
        self.box_back.update(screen)
        self.box_save.update(screen)
        if self.box_draw_and_move.active_draw:
            self.box_input.update(screen)
        else:
            self.box_input_2.update(screen)
        self.box_delete.update(screen)
        self.box_phase.update(screen)

    def reset(self, name: str = None):
        """
        Resets the make piece window.

        Args:
            name (str): The name of the piece. If provided, loads the piece with the given name.

        Returns:
            None
        """
        if name is not None:
            self.box_name.text = name
            self.box_name.active = False
            self.movement = np.load(os.path.join(os.getcwd(), "Pieces", name + ".npz"))[
                "movement"
            ]
            self.drawing = np.load(os.path.join(os.getcwd(), "Pieces", name + ".npz"))[
                "drawing"
            ]
            self.box_input.current_mesh = self.drawing
            self.box_input_2.current_mesh = self.movement
            self.box_draw_and_move.active_draw = True
            self.box_back.previous_window = "piece_existing_screen"
        else:
            self.box_name.text = "Enter Name"
            self.movement = movement_matrix.copy()
            self.drawing = np.zeros((64, 64))
            self.box_input.current_mesh = self.drawing
            self.box_input_2.current_mesh = self.movement
            self.box_draw_and_move.active_draw = True
            self.box_name.active = False
            self.box_back.previous_window = "piece_select_screen"

    def save(self):
        """Saves the piece to the pieces folder"""

        folder = os.path.join(os.getcwd(), "Pieces")

        file_name = os.path.join(folder, self.box_name.text + ".npz")

        np.savez(
            file_name,
            drawing=self.drawing,
            movement=self.movement,
            type_movement=self.type_movement,
        )
        try:
            with open("pieces.pkl", "rb") as f:
                pieces = pickle.load(f)
                pieces[
                    int(hashlib.sha1(self.box_name.text.encode()).hexdigest(), 16)
                    % TOTAL_EXPECTED_PIECES
                ] = self.box_name.text
        except EOFError:
            pieces = {
                int(hashlib.sha1(self.box_name.text.encode()).hexdigest(), 16)
                % TOTAL_EXPECTED_PIECES: self.box_name.text
            }
        with open("pieces.pkl", "wb") as f:
            pickle.dump(pieces, f)
