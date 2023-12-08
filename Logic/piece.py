import pygame
import numpy as np
from dataclasses import dataclass
import os
import math

import hashlib

from UI.piece_draw_screen import TOTAL_EXPECTED_PIECES, WALK, BLACK, WHITE


class GamePiece:
    def __init__(
        self,
        piece: pygame.Surface,
        movement: np.ndarray,
        name: str,
        phased_movement: bool = False,
    ):
        """
        Initializes a Piece object.

        Args:
            piece (pygame.Surface): The image representing the piece.
            movement (np.ndarray): The possible movement directions of the piece.
            name (str): The name of the piece.
            phased_movement (bool, optional): Indicates if the piece has phased movement. Defaults to False.
        """
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
        self.phased_movement = phased_movement

    def get_valid_moves(self, board, position, alignment):
        """Returns a list of valid moves for the piece"""

        movement_map = self.movement[
            15 - position[0] - 8 : 15 - position[0],
            15 - position[1] - 8 : 15 - position[1],
        ]
        valid_moves = []

        if self.phased_movement:
            for row in range(movement_map.shape[0]):
                for col in range(movement_map.shape[1]):
                    if movement_map[row, col] == 15:
                        if board[row, col] == 0:
                            valid_moves.append((row, col))
                        else:
                            if alignment[row, col] != self.color:
                                valid_moves.append((row, col))
        else:
            # This means that the pieces movement needs to be contiguous
            # If movement isn't phased, then a breadth first search can be used to find all valid moves
            # A better way to do this would be to just use rays in the directions the piece can move

            rows, cols = board.shape

            directions = [
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1),
                (1, 1),
                (-1, -1),
                (-1, 1),
                (1, -1),
            ]

            for direction in directions:
                for i in range(1, 8):
                    row = position[0] + direction[0] * i
                    col = position[1] + direction[1] * i
                    if row < 0 or row > rows - 1 or col < 0 or col > cols - 1:
                        break  # Out of bounds
                    if movement_map[row, col] == 15:
                        if board[row, col] == 0:
                            valid_moves.append((row, col))
                        else:
                            if alignment[row, col] != self.color:
                                valid_moves.append((row, col))
                            break

        return valid_moves

    def copy(self):
        return GamePiece(self.piece, self.movement, self.name, self.phased_movement)
