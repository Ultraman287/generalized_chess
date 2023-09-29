import pygame
import numpy as np
from dataclasses import dataclass
import os
import math

import hashlib

from UI.piece_draw_screen import TOTAL_EXPECTED_PIECES, PHASE, WALK, BLACK, WHITE


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
        self.is_king = False

    def get_valid_moves(self, board, position, alignment):
        """Returns a list of valid moves for the piece"""

        movement_map = self.movement[
            15 - position[0] - 8 : 15 - position[0],
            15 - position[1] - 8 : 15 - position[1],
        ]
        valid_moves = []

        for row in range(movement_map.shape[0]):
            for col in range(movement_map.shape[1]):
                if movement_map[row, col] == 15:
                    if board[row, col] == 0:
                        valid_moves.append((row, col))
                    else:
                        if alignment[row, col] != self.color:
                            valid_moves.append((row, col))

        return valid_moves

    def copy(self):
        return GamePiece(self.piece, self.movement, self.name)
