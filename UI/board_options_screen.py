import pygame
import numpy as np
from dataclasses import dataclass
import os
import tkinter
import tkinter.filedialog
from Helpers.interactive_box import InteractiveBox


def prompt_file():
    """Create a Tk file dialog and cleanup when finished"""
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename()
    top.destroy()
    return file_name


class CreateNewBoard(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(207, 132, 386, 58)
        self.text = "Create New Board"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = (217, 217, 217)

    def handle_event(self, event):
        """Handles events for the interactive box"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return "board_create_screen"


class EditExistingBoard(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(207, 271, 386, 58)
        self.text = "Edit Existing Board"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = (217, 217, 217)

    def handle_event(self, event):
        """Handles events for the interactive box"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                file = prompt_file()
                if file:
                    return "board_create_screen", file


class BackButton(InteractiveBox):
    def __init__(self):
        self.rect = pygame.Rect(207, 410, 386, 58)
        self.text = "Back"
        self.text_color = (0, 0, 0)
        self.active = False
        self.color_active = (250, 220, 220)
        self.color_inactive = (217, 217, 217)

    def handle_event(self, event):
        """Handles events for the interactive box"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return "main_menu_screen"


class BoardOptionsScreen:
    def __init__(self) -> None:
        self.new_board_button = CreateNewBoard()
        self.edit_board_button = EditExistingBoard()
        self.back_button = BackButton()

    def handle_event(self, event):
        selected = self.edit_board_button.handle_event(event)
        if selected:
            return selected

        return self.new_board_button.handle_event(
            event
        ) or self.back_button.handle_event(event)

    def reset(self):
        pass

    def update(self, screen):
        screen.fill((198, 198, 198))
        self.new_board_button.draw(screen)
        self.edit_board_button.draw(screen)
        self.back_button.draw(screen)
        pygame.display.flip()
