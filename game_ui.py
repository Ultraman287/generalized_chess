import pygame
from UI.piece_draw_screen import MakePiece

WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (198, 198, 198)
CURRENT_WINDOW = "piece_draw_screen"
screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True
clock = pygame.time.Clock()
screen.fill(BACKGROUND_COLOR)
pygame.init()


windows = {
    "piece_draw_screen": MakePiece(
        8,
        8,
    )
}

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        windows[CURRENT_WINDOW].handle_event(event)
    windows[CURRENT_WINDOW].update(screen)
    pygame.display.flip()
