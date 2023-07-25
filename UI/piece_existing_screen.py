import pygame
import numpy as np
from dataclasses import dataclass
import os
import thorpy
import math

from Helpers.interactive_box import InteractiveBox

BOX_COLOR = (217, 217, 217)

pieces = [
    pygame.surfarray.make_surface(np.load(os.path.join("Pieces", piece))["drawing"])
    for piece in os.listdir("Pieces")
]


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
                return "piece_select_screen"


class IndividualPiece(InteractiveBox):
    def __init__(self, piece, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.piece = piece
        self.piece = pygame.transform.scale(self.piece, (w, h))
        self.piece = pygame.transform.flip(self.piece, True, False)
        self.text = ""
        self.text_color = (0, 0, 0)
        self.active = False
        self.color = BOX_COLOR
        self.color_active = (250, 220, 220)
        self.color_inactive = BOX_COLOR

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        screen.blit(self.piece, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return "piece_draw_screen"


class SelectPiece(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(56, 124, 688, 420)

        num_pieces = len(pieces)
        col_row_ratio = self.rect.width / self.rect.height

        num_cols = math.ceil(np.sqrt(num_pieces * col_row_ratio))
        num_rows = math.ceil(num_pieces / num_cols)

        self.pieces = []

        for ind, piece in enumerate(pieces):
            x = (ind % num_cols) * (self.rect.width / num_cols) + self.rect.x
            y = (ind // num_cols) * (self.rect.height / num_rows) + self.rect.y
            w = self.rect.width / num_cols
            h = self.rect.height / num_rows
            self.pieces.append(IndividualPiece(piece, x, y, w, h))

    def draw(self, screen):
        pygame.draw.rect(screen, BOX_COLOR, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        for piece in self.pieces:
            piece.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for piece in self.pieces:
                if piece.handle_event(event) == "piece_draw_screen":
                    return "piece_draw_screen"

    def update(self, screen):
        self.draw(screen)


class PieceExistingScreen:
    def __init__(self) -> None:
        self.back_button = BoxBack()
        self.select_piece = SelectPiece()

    def handle_event(self, event):
        return self.back_button.handle_event(event) or self.select_piece.handle_event(
            event
        )

    def update(self, screen):
        screen.fill((198, 198, 198))
        self.back_button.draw(screen)
        self.select_piece.update(screen)
        pygame.display.flip()
