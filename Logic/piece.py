import pygame
import numpy as np
from dataclasses import dataclass
import os
import math

import hashlib

from UI.piece_draw_screen import TOTAL_EXPECTED_PIECES, PHASE, WALK


class GamePiece:
    def __init__(self, piece: pygame.Surface, movement: np.ndarray, name: str):
        self.piece = piece
        self.movement = movement
        self.name = name
        self.hash = (
            int(hashlib.sha1(self.name.encode()).hexdigest(), 16)
            % TOTAL_EXPECTED_PIECES
        )
        self.position = None
        self.color = None

    def get_valid_moves(self, board, position):
        """Returns a list of valid moves for the piece"""
        print(self.movement)
        print(np.where(self.movement == PHASE))
        return [(4, 4)]
