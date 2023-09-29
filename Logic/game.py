import pygame
import numpy as np
from dataclasses import dataclass
import os
import math
import pickle

import hashlib

from UI.piece_draw_screen import TOTAL_EXPECTED_PIECES, PHASE, WALK, BLACK, WHITE
from UI.board_create_screen import PIECE_HEIGHT, PIECE_WIDTH, BLACK_PIECE, WHITE_PIECE


class GameLogic:
    def __init__(self):
        self.piece_alignment = np.zeros((8, 8))
        self.piece_position = np.zeros((8, 8))
        self.pieces = {}
        self.selected_piece = None
        self.piece_can_move_to = set()
        self.turn = WHITE_PIECE
        self.game_history = []
        self.kings = []
        self.game_over = False
        self.winner = None

    def handle_press(self, row, col):
        mesh_size = self.piece_position.shape[0]
        if 0 <= row < mesh_size and 0 <= col < mesh_size:
            print(f"piece: {self.pieces.get((row, col), None)}")
            if self.selected_piece is not None:
                print(f"Currently the piece is at {self.selected_piece.position}")
                if (row, col) in self.piece_can_move_to:
                    del self.pieces[
                        (
                            self.selected_piece.position[0],
                            self.selected_piece.position[1],
                        )
                    ]
                    if self.pieces.get((row, col), None) is not None:
                        if self.pieces[(row, col)].is_king:
                            self.game_over = True
                            self.winner = (
                                "White"
                                if self.selected_piece.color == WHITE_PIECE
                                else "Black"
                            )

                    self.piece_position[self.selected_piece.position] = 0
                    self.piece_position[row, col] = self.selected_piece.hash
                    self.piece_alignment[self.selected_piece.position] = 0
                    self.piece_alignment[row, col] = self.selected_piece.color
                    self.selected_piece.position = (row, col)
                    print(self.selected_piece.position)
                    self.piece_can_move_to = []
                    self.pieces[(row, col)] = self.selected_piece
                    self.selected_piece = None
                    self.turn = WHITE_PIECE if self.turn == BLACK_PIECE else BLACK_PIECE
                else:
                    self.selected_piece = None
                    self.piece_can_move_to = []
            else:
                self.selected_piece = self.pieces.get((row, col), None)
                print(f"selected piece: {self.selected_piece}")
                if self.selected_piece:
                    if self.selected_piece.color != self.turn:
                        self.selected_piece = None
                        return
                    self.piece_can_move_to = self.selected_piece.get_valid_moves(
                        self.piece_position, (row, col), self.piece_alignment
                    )
                    print(f"piece can move to: {self.piece_can_move_to}")

    def get_pieces_from_hash(self, piece_dictionary):
        """Gets the pieces from the hashes stored in the pickle file"""
        self.pieces = {}

        with open(os.path.join(os.getcwd(), "pieces.pkl"), "rb") as f:
            hash_to_piece = pickle.load(f)
            print(hash_to_piece)
            print(self.piece_position)

            pieces = np.where(self.piece_position != 0)

            for i, piece in enumerate(zip(pieces[0], pieces[1])):
                r, c = piece
                self.pieces[(r, c)] = piece_dictionary[
                    hash_to_piece[self.piece_position[r][c]]
                ].copy()
                self.pieces[(r, c)].position = (r, c)
                self.pieces[(r, c)].color = self.piece_alignment[r][c]
                # When a piece is black, we rotate the movement matrix by 180 degrees to account for the fact that the board is flipped
                if self.pieces[(r, c)].color == BLACK_PIECE:
                    self.pieces[(r, c)].movement = np.rot90(
                        self.pieces[(r, c)].movement, 2
                    )

        # Turning the king pieces into kings

        for king_position in self.kings:
            self.pieces[tuple(king_position)].is_king = True
