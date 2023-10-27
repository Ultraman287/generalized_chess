import pygame
import numpy as np
from dataclasses import dataclass
import os

from Helpers.interactive_box import InteractiveBox


class PlayChess(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(207, 66, 386, 58)
        self.text = "Play Chess"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = (217, 217, 217)

    def handle_event(self, event):
        """Handles events for the interactive box"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return "game_options_screen"


class CreateCustomBoard(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(207, 183, 386, 58)
        self.text = "Create Custom Board"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = (217, 217, 217)

    def handle_event(self, event):
        """Handles events for the interactive box"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return "board_options_screen"


class CreateCustomPiece(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(207, 300, 386, 58)
        self.text = "Create Custom Piece"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = (217, 217, 217)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return "piece_select_screen"


class AITools(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(207, 417, 386, 58)
        self.text = "AI Tools"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = (217, 217, 217)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return "ai_tools_screen"


class MainMenuScreen:
    def __init__(self) -> None:
        self.custom_piece_button = CreateCustomPiece()
        self.custom_board_button = CreateCustomBoard()
        self.play_chess_button = PlayChess()
        self.ai_tools_button = AITools()

    def handle_event(self, event):
        return (
            self.custom_piece_button.handle_event(event)
            or self.custom_board_button.handle_event(event)
            or self.play_chess_button.handle_event(event)
            or self.ai_tools_button.handle_event(event)
        )

    def reset(self):
        pass

    def update(self, screen):
        screen.fill((198, 198, 198))
        self.custom_piece_button.draw(screen)
        self.custom_board_button.draw(screen)
        self.play_chess_button.draw(screen)
        self.ai_tools_button.draw(screen)
        pygame.display.flip()
