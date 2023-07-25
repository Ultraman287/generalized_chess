import pygame
import thorpy
from UI.piece_draw_screen import MakePiece
from UI.piece_select_screen import PieceSelectScreen
from UI.piece_existing_screen import PieceExistingScreen


global CURRENT_WINDOW
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (198, 198, 198)

CURRENT_WINDOW = "piece_select_screen"
screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True
clock = pygame.time.Clock()
screen.fill(BACKGROUND_COLOR)
pygame.init()
thorpy.init(screen, thorpy.theme_classic)  # bind screen to gui elements and set theme

windows = {
    "piece_draw_screen": MakePiece(),
    "piece_select_screen": PieceSelectScreen(),
    "piece_existing_screen": PieceExistingScreen(),
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
