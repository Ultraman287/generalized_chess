import pygame
from UI.piece_draw_screen import MakePiece
from UI.piece_select_screen import PieceSelectScreen

global CURRENT_WINDOW
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (198, 198, 198)

CURRENT_WINDOW = "piece_select_screen"
screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True
clock = pygame.time.Clock()
screen.fill(BACKGROUND_COLOR)
pygame.init()


windows = {
    "piece_draw_screen": MakePiece(
        8,
        8,
    ),
    "piece_select_screen": PieceSelectScreen(),
}

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        next_window = windows[CURRENT_WINDOW].handle_event(event)
        if next_window:
            CURRENT_WINDOW = next_window
            screen.fill(BACKGROUND_COLOR)
    windows[CURRENT_WINDOW].update(screen)

    pygame.display.flip()
