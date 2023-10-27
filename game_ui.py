import pygame
import thorpy
import os
import sys

import hashlib

with open(".env", "r") as f:
    for line in f:
        key, value = line.split("=")
        os.environ[key.strip()] = value.strip()


pygame.init()

from UI.main_menu_screen import MainMenuScreen
from UI.piece_draw_screen import MakePiece
from UI.piece_select_screen import PieceSelectScreen
from UI.piece_existing_screen import PieceExistingScreen
from UI.board_options_screen import BoardOptionsScreen
from UI.board_existing_screen import BoardExistingScreen
from UI.board_create_screen import BoardCreateScreen
from UI.game_screen import GameScreen
from UI.game_options_screen import GameOptionsScreen
from UI.game_existing_screen import GameExistingScreen
from UI.ai_tools_screen import AIToolsScreen
from UI.ai_train_screen import AITrainScreen
from UI.ai_play_screen import AIPlayScreen


global CURRENT_WINDOW
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (198, 198, 198)

CURRENT_WINDOW = "main_menu_screen"
screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True
clock = pygame.time.Clock()
screen.fill(BACKGROUND_COLOR)


windows = {
    "main_menu_screen": MainMenuScreen(),
    "piece_draw_screen": MakePiece(),
    "piece_select_screen": PieceSelectScreen(),
    "piece_existing_screen": PieceExistingScreen(),
    "board_options_screen": BoardOptionsScreen(),
    "board_existing_screen": BoardExistingScreen(),
    "board_create_screen": BoardCreateScreen(),
    "game_screen": GameScreen(),
    "game_options_screen": GameOptionsScreen(),
    "game_existing_screen": GameExistingScreen(),
    "ai_tools_screen": AIToolsScreen(),
    "ai_train_screen": AITrainScreen(),
    "ai_play_screen": AIPlayScreen(),
}

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        next_window = windows[CURRENT_WINDOW].handle_event(event)
        if next_window:
            if type(next_window) == tuple:
                CURRENT_WINDOW = next_window[0]
                screen.fill(BACKGROUND_COLOR)
                windows[CURRENT_WINDOW].reset(next_window[1])
            else:
                CURRENT_WINDOW = next_window
                screen.fill(BACKGROUND_COLOR)
                windows[CURRENT_WINDOW].reset()
    windows[CURRENT_WINDOW].update(screen)

    pygame.display.flip()


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
