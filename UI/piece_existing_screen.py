import pygame
import numpy as np
from dataclasses import dataclass
import os
import math

from Helpers.interactive_box import InteractiveBox

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
                return "piece_select_screen"


class IndividualPiece(InteractiveBox):
    def __init__(self, piece, x, y, w, h, name):
        self.rect = pygame.Rect(x, y, w, h)
        self.piece = piece
        self.piece = pygame.transform.scale(self.piece, (w * 0.97, h * 0.8))
        self.piece = pygame.transform.flip(self.piece, True, False)
        self.name = name
        self.text_color = (0, 0, 0)
        self.active = False
        self.color = BOX_COLOR
        self.color_active = (250, 220, 220)
        self.color_inactive = BOX_COLOR
        self.is_white = False
        self.hash = hash(self.name)

    def get_blit(self):
        "Turns the name and piece into a surface"
        text = pygame.font.SysFont("Arial", self.rect.height // 10).render(
            self.name, True, (0, 0, 0)
        )
        piece = pygame.transform.scale(
            self.piece, (self.rect.width, self.rect.height * 0.8)
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
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (120, 120, 120), self.rect, 2)
        screen.blit(self.piece, self.rect)
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return "piece_draw_screen"


class SelectPiece(InteractiveBox):
    def __init__(self, pieces=[], piece_names=[]):
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
            self.pieces.append(IndividualPiece(piece, x, y, w, h, piece_names[ind]))

    def draw(self, screen):
        pygame.draw.rect(screen, BOX_COLOR, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        for piece in self.pieces:
            piece.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for piece in self.pieces:
                if piece.handle_event(event) == "piece_draw_screen":
                    return "piece_draw_screen", piece.name

    def update(self, screen):
        self.draw(screen)


class PieceExistingScreen:
    def __init__(self) -> None:
        self.pieces = [
            pygame.surfarray.make_surface(
                np.load(os.path.join("Pieces", piece))["drawing"]
            )
            for piece in os.listdir("Pieces")
        ]
        self.piece_names = [piece.split(".")[0] for piece in os.listdir("Pieces")]
        self.back_button = BoxBack()
        self.select_piece = SelectPiece(
            pieces=self.pieces, piece_names=self.piece_names
        )

    def handle_event(self, event):
        return self.back_button.handle_event(event) or self.select_piece.handle_event(
            event
        )

    def reset(self):
        self.pieces = [
            pygame.surfarray.make_surface(
                np.load(os.path.join("Pieces", piece))["drawing"]
            )
            for piece in os.listdir("Pieces")
        ]
        self.piece_names = [piece.split(".")[0] for piece in os.listdir("Pieces")]
        self.select_piece = SelectPiece(
            pieces=self.pieces, piece_names=self.piece_names
        )

    def update(self, screen):
        screen.fill((198, 198, 198))
        self.back_button.draw(screen)
        self.select_piece.update(screen)
        pygame.display.flip()
