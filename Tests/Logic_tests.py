import pytest
import numpy as np
from unittest.mock import Mock, patch
import pygame
from Logic.game import (
    GameLogic,
)
from Logic.piece import GamePiece


@pytest.fixture
def game_logic():
    """Provides a GameLogic instance for testing."""
    game = GameLogic(rows=2, cols=2)
    game.piece_alignment = np.array([[2, 0], [0, 1]])
    game.piece_position = np.array([[1, 0], [0, 1]])

    return GameLogic(rows=8, cols=8)


@pytest.fixture
def mock_piece():
    """Mock a piece with minimal attributes for testing piece interactions."""
    mock = Mock()
    mock.hash = 1
    mock.color = 2  # 1 represents WHITE_PIECE
    mock.position = (0, 0)
    mock.get_valid_moves.return_value = {(1, 0), (1, 1)}
    return mock


@pytest.fixture
def mock_openai():
    """Mock the ChatOpenAI class for testing."""
    mock = Mock()
    mock.predict.return_value = "w1=(0, 0)->(1, 1)"
    return mock


class TestGameLogic:
    """
    Test cases for GameLogic class.

    This class contains test methods to verify the behavior of the GameLogic class, which manages the game state
    and rules for piece interactions.

    Fixtures:
        - mock_piece: Mocks a piece with minimal attributes for testing piece interactions.

    Test Methods:
        - test_handle_press_select_and_move_piece: Test selecting a piece and moving it to a valid position.
        - test_get_all_possible_moves: Test that all possible moves are correctly identified for the current player.
        - test_apply_action: Test applying an action translates to the correct piece movement.
        - test_game_over_conditions: Test the game over conditions are correctly set.
    """

    def test_handle_press_select_and_move_piece(self, game_logic, mock_piece):
        """Test selecting a piece and moving it to a valid position."""
        # Arrange
        game_logic.pieces[(0, 0)] = mock_piece
        game_logic.handle_press(0, 0)  # Select piece
        # Act
        game_logic.handle_press(1, 1)  # Attempt to move to (1, 1)
        # Assert
        assert (1, 1) in game_logic.pieces
        assert game_logic.piece_position[1][1] == mock_piece.hash
        assert game_logic.selected_piece is None

    def test_get_all_possible_moves(self, game_logic, mock_piece):
        """Test that all possible moves are correctly identified for the current player."""
        # Arrange
        game_logic.pieces[(0, 0)] = mock_piece
        game_logic.turn = mock_piece.color  # Ensure it's the mock piece's turn
        # Act
        possible_moves = game_logic.get_all_possible_moves()
        # Assert
        assert f"w{mock_piece.hash}={(0, 0)}->{(1, 1)}" in possible_moves

    def test_apply_action(self, game_logic, mock_piece):
        """Test applying an action translates to the correct piece movement."""
        # Arrange
        game_logic.pieces[(0, 0)] = mock_piece
        mock_piece.id = 0  # Mock piece ID
        action = (
            mock_piece.id * (game_logic.rows * game_logic.cols)
            + 1 * game_logic.rows
            + 1
        )
        # Act
        game_logic.apply_action(action)
        # Assert
        assert game_logic.piece_position[1][1] == mock_piece.hash

    def test_game_over_conditions(self, game_logic, mock_piece):
        """Test the game over conditions are correctly set."""
        # Arrange
        game_logic.pieces[(0, 0)] = mock_piece
        game_logic.pieces[(1, 1)] = mock_piece
        game_logic.pieces[(1, 1)].is_king = True
        # Act
        game_logic.handle_press(0, 0)  # Select the king piece
        game_logic.handle_press(1, 1)  # Move and capture the king piece
        # Assert
        assert game_logic.game_over
        assert game_logic.winner is not None

    # Test ai_move method to ensure it generates valid moves
    @patch("Logic.game.llm")
    @patch("Logic.game.GameLogic.get_all_possible_moves")
    def test_ai_move(self, mock_get_moves, mock_llm, game_logic):
        # Configure mock_get_moves behavior
        mock_get_moves.return_value = ["b1=(0, 0)->(1, 1)"]  # Mocking a list of moves

        # Configure mock_llm behavior
        mock_llm.predict.return_value = "b1=(0, 0)->(1, 1)"

        # Call ai_move method
        game_logic.ai_move()

        # Assert that the mock_llm method was called
        mock_llm.predict.assert_called_once()

    # Test get_current_game_state method to ensure it returns the correct state
    def test_get_current_game_state(self, game_logic):
        state = game_logic.get_current_game_state()
        assert isinstance(state, tuple)
        assert isinstance(state[0], np.ndarray)
        assert isinstance(state[1], np.ndarray)

    # Test board_to_string method to ensure it returns a valid string representation of the board
    def test_board_to_string(self, game_logic):
        board_str = game_logic.board_to_string()
        assert isinstance(board_str, str)

    # Test clone method to ensure that the cloned game state is independent of the original
    def test_clone(self, game_logic):
        clone = game_logic.clone()
        assert clone is not game_logic
        assert np.array_equal(clone.piece_position, game_logic.piece_position)
        assert np.array_equal(clone.piece_alignment, game_logic.piece_alignment)


@pytest.fixture
def mock_piece_image():
    """Mock the pygame.Surface for a piece's image."""
    return Mock(spec=pygame.Surface)


@pytest.fixture
def knight_movement():
    """Example movement array for a knight piece."""
    # This is a simplified example.
    movement = np.zeros((15, 15))
    movement[6, 7] = 15
    movement[5, 6] = 15
    movement[5, 8] = 15
    movement[4, 5] = 15
    movement[4, 9] = 15
    movement[3, 4] = 15

    return movement


@pytest.fixture
def game_piece(mock_piece_image, knight_movement):
    """Provides a GamePiece instance for testing."""
    return GamePiece(
        piece=mock_piece_image,
        movement=knight_movement,
        name="Knight",
        phased_movement=True,
    )


class TestGamePiece:
    """
    Test cases for the GamePiece class.

    This class contains test methods to verify the behavior of the GamePiece class, which represents a game piece
    with its movement capabilities and other attributes.

    Fixtures:
        - mock_piece_image: Mocked pygame.Surface for a piece's image.
        - knight_movement: Example movement array for a knight piece.

    Test Methods:
        - test_get_valid_moves: Test that the piece correctly identifies valid moves.
        - test_copy: Test that the copy method creates a distinct copy of the piece.
    """

    def test_get_valid_moves(self, game_piece):
        """Test that the piece correctly identifies valid moves."""
        # Mock board, position, and alignment
        board = np.zeros((8, 8))
        board[3, 3] = 1  # Mock the piece's position
        board[1, 4] = 2  # Mock an opposing piece in a position the knight can capture
        position = (3, 3)
        alignment = np.zeros((8, 8))
        alignment[3, 3] = 1
        alignment[1, 4] = 2

        # Get valid moves
        valid_moves = game_piece.get_valid_moves(board, position, alignment)

        # Expected valid moves
        expected_moves = {(1, 4), (1, 2)}

        # Assertion
        assert all(move in valid_moves for move in expected_moves)

    def test_copy(self, game_piece):
        """Test that the copy method creates a distinct copy of the piece."""
        # Copy the piece
        piece_copy = game_piece.copy()

        # Assertions
        assert piece_copy is not game_piece
        assert piece_copy.name == game_piece.name
        assert np.array_equal(piece_copy.movement, game_piece.movement)
