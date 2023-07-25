import pygame
import numpy as np
from dataclasses import dataclass
import os

from Helpers.interactive_box import InteractiveBox


class CreateNewPiece(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(207, 191, 386, 58)
        self.text = "Create New Piece"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = (217, 217, 217)

    def handle_event(self, event):
        """Handles events for the interactive box"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return "piece_draw_screen"


class EditExistingPiece(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(207, 316, 386, 58)
        self.text = "Edit Existing Piece"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = (217, 217, 217)

    def handle_event(self, event):
        """Handles events for the interactive box"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return "piece_existing_screen"


class PieceSelectScreen:
    def __init__(self) -> None:
        self.new_piece_button = CreateNewPiece()
        self.edit_piece_button = EditExistingPiece()

    def handle_event(self, event):
        # self.new_piece_button.handle_event(event)
        # self.edit_piece_button.handle_event(event)
        return self.new_piece_button.handle_event(
            event
        ) or self.edit_piece_button.handle_event(event)

    def reset(self):
        pass

    def update(self, screen):
        screen.fill((198, 198, 198))
        self.new_piece_button.draw(screen)
        self.edit_piece_button.draw(screen)
        pygame.display.flip()
