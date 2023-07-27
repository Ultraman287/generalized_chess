import pygame
import numpy as np
from dataclasses import dataclass
import os

from Helpers.interactive_box import InteractiveBox
from UI.piece_existing_screen import IndividualPiece
import math

BOARD_ROWS, BOARD_COLS = 8, 8
BOX_COLOR = (217, 217, 217)

PIECE_HEIGHT = 100
PIECE_WIDTH = 140


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
            print(f"Active Draw: {self.active_draw}")

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


class BoxInput(InteractiveBox):
    def __init__(self, mesh=np.zeros((8, 8))):
        self.rect = pygame.Rect(272, 113, 460, 460)

        self.current_mesh = mesh

    def draw(self, screen):
        # Scaling up the mesh to fit the box

        surf = pygame.surfarray.make_surface(self.current_mesh)
        surf = pygame.transform.scale(surf, (self.rect.width, self.rect.height))
        surf = pygame.transform.flip(surf, True, False)

        screen.blit(surf, self.rect)

        pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)

    def update(self, screen):
        surf = pygame.surfarray.make_surface(self.current_mesh)
        surf = pygame.transform.scale(surf, (self.rect.width, self.rect.height))
        surf = pygame.transform.flip(surf, True, False)

        screen.blit(surf, self.rect)

        pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)

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
                    if self.current_mesh[col, row] != 60:
                        if event.button == 1:
                            if self.current_mesh[col, row] == 15:
                                self.current_mesh[col, row] = 20
                            else:
                                self.current_mesh[
                                    col, row
                                ] = 15  # You can set this value based on your drawing needs
                        if event.button == 3:
                            if self.current_mesh[col, row] == 0:
                                self.current_mesh[col, row] = 255
                            else:
                                self.current_mesh[col, row] = 0
                    print(row, col, self.current_mesh[row, col])


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
        self.get_all_pieces()

    def get_all_pieces(self):
        """Gets all the pieces from the Pieces folder"""
        self.pieces = []
        pieces = os.listdir(os.path.join(os.getcwd(), "Pieces"))
        for i, piece in enumerate(pieces):
            self.pieces.append(
                IndividualPiece(
                    pygame.surfarray.make_surface(
                        np.load(os.path.join(os.getcwd(), "Pieces", piece))["drawing"]
                    ),
                    self.rect.x + 40,
                    self.rect.y + 2 + i * PIECE_HEIGHT,
                    PIECE_WIDTH,
                    PIECE_HEIGHT,
                    piece[:-4],
                )
            )
        # updating the pieces surface when the pieces are updated
        self.pieces_surface = pygame.Surface((165, PIECE_HEIGHT * len(self.pieces)))
        for i, piece in enumerate(self.pieces):
            self.pieces_surface.blit(
                piece.get_blit(),
                (self.rect.width / 2 - piece.piece.get_width() / 2, i * PIECE_HEIGHT),
            )
            # self.pieces_surface.blit(
            #     piece.piece,
            #     (self.rect.width / 2 - piece.piece.get_width() / 2, i * PIECE_HEIGHT),
            # )

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
                        print(self.pieces[clicked_piece].name)

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color_inactive, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        ### Drawing the surface with the offset
        screen.blit(self.pieces_surface, self.rect, (0, self.y_offset, 165, 460))
        # screen.blit(self.pieces_surface, self.rect, (0, 0, 165, 460))

    def update(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color_inactive, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        # screen.blit(self.pieces_surface, self.rect, (0, 0, 165, 460))
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
                    os.path.join(os.getcwd(), "Pieces", box_name.text + ".npz")
                ):
                    os.remove(
                        os.path.join(os.getcwd(), "Pieces", box_name.text + ".npz")
                    )


box_delete = BoxDelete()


class BoardCreateScreen:
    def __init__(
        self,
        rows: int = 8,
        cols: int = 8,
        movement: np.ndarray = np.zeros((15, 15)),
        drawing: np.ndarray = np.zeros((64, 64)),
    ):
        self.rows = rows
        self.cols = cols
        self.drawing = drawing
        self.current_mode: str = "draw"
        self.box_name = box_name

        self.box_back = box_back
        self.box_save = box_save
        self.box_input = box_input
        self.box_delete = box_delete
        self.box_select = box_select

    def draw(self, screen):
        """Draws the make piece window"""

        self.box_name.draw(screen)
        self.box_back.draw(screen)
        self.box_save.draw(screen)
        self.box_input.draw(screen)
        self.box_delete.draw(screen)
        self.box_select.draw(screen)

    def handle_event(self, event):
        """Handles events for the make piece window"""

        self.box_name.handle_event(event)
        self.box_input.handle_event(event)
        self.drawing = self.box_input.current_mesh
        self.box_save.handle_event(event, self.save)
        self.box_delete.handle_event(event)
        self.box_select.handle_event(event)

        return self.box_back.handle_event(event)

    def update(self, screen):
        """Updates the make piece window"""

        self.box_name.update(screen)
        self.box_back.update(screen)
        self.box_save.update(screen)
        self.box_input.update(screen)
        self.box_delete.update(screen)
        self.box_select.update(screen)

    def reset(self, name: str = None):
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
            self.box_back.previous_window = "board_existing_screen"
        else:
            self.box_name.text = "Enter Name"
            self.drawing = np.zeros((64, 64))
            self.box_input.current_mesh = self.drawing
            self.box_name.active = False
            self.box_back.previous_window = "board_options_screen"

    def save(self):
        """Saves the piece to the pieces folder"""

        folder = os.path.join(os.getcwd(), "Pieces")

        file_name = os.path.join(folder, self.box_name.text + ".npz")

        np.savez(file_name, drawing=self.drawing, movement=self.movement)
