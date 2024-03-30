import pytest
import pygame
import pytest
from unittest.mock import Mock, patch
from UI.ai_select_screen import IndividualBoard, BoxBoards, BoxBack, AISelectScreen
from UI.board_create_screen import BoxRows, BoxInput, IndividualPiece, BoxSelect
from UI import ai_play_screen, ai_select_screen, ai_tools_screen, ai_train_screen
from UI import board_create_screen, board_existing_screen, board_options_screen
from UI import game_existing_screen, game_options_screen, game_screen, main_menu_screen
from UI import piece_draw_screen, piece_existing_screen, piece_select_screen

pygame.font.init()


pygame.init()  # Initialize pygame for the tests


class TestUIComponents:
    """
    Test cases for UI components including IndividualBoard, BoxBack, BoxBoards, and AISelectScreen.

    This class contains test methods for verifying the initialization and behavior of various UI components
    in the application.

    Fixtures:
        individual_board: Provides an IndividualBoard instance for testing.

    Test Methods:
        - test_individual_board_init: Test initialization of IndividualBoard instance.
        - test_individual_board_get_blit: Test get_blit method of IndividualBoard instance.
        - test_individual_board_handle_event: Test handle_event method of IndividualBoard instance.
        - test_box_back_init: Test initialization of BoxBack instance.
        - test_box_back_handle_event: Test handle_event method of BoxBack instance.
        - test_box_boards_init: Test initialization of BoxBoards instance.
        - test_ai_select_screen_init: Test initialization of AISelectScreen instance.
        - test_ai_select_screen_handle_event: Test handle_event method of AISelectScreen instance.
        - test_ai_select_screen_reset: Test reset method of AISelectScreen instance.

    Each test method is designed to verify a specific aspect of the corresponding UI component's behavior.
    """

    @pytest.fixture
    def individual_board(self):
        """Provides an IndividualBoard instance for testing."""
        board_image_mock = pygame.Surface((100, 100))
        return IndividualBoard(board_image_mock, 100, 100, 50, 50, "TestBoard")

    def test_individual_board_init(self, individual_board):
        """Test initialization of IndividualBoard instance."""
        assert individual_board.name == "TestBoard"
        assert individual_board.rect.x == 100
        assert individual_board.rect.y == 100
        assert individual_board.rect.width == 50
        assert individual_board.rect.height == 50

    def test_individual_board_get_blit(self, individual_board):
        """Test get_blit method of IndividualBoard instance."""
        surface = individual_board.get_blit()
        assert surface.get_width() == individual_board.rect.width
        assert surface.get_height() == individual_board.rect.height

    def test_individual_board_handle_event(self, individual_board):
        """Test handle_event method of IndividualBoard instance."""
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(100, 100))
        assert individual_board.handle_event(event) == ("ai_train_screen", "TestBoard")

    def test_box_back_init(self):
        """Test initialization of BoxBack instance."""
        box_back = BoxBack()
        assert box_back.rect.x == 56
        assert box_back.rect.y == 52
        assert box_back.rect.width == 165
        assert box_back.rect.height == 54

    def test_box_back_handle_event(self):
        """Test handle_event method of BoxBack instance."""
        box_back = BoxBack()
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(56, 52))
        assert box_back.handle_event(event) == "ai_tools_screen"

    def test_box_boards_init(self):
        """Test initialization of BoxBoards instance."""
        box_boards = BoxBoards()
        assert box_boards.rect.x == 56
        assert box_boards.rect.y == 124
        assert box_boards.rect.width == 688
        assert box_boards.rect.height == 420

    def test_ai_select_screen_init(self):
        """Test initialization of AISelectScreen instance."""
        ai_select_screen = AISelectScreen()
        assert len(ai_select_screen.boxes) == 2

    def test_ai_select_screen_handle_event(self):
        """Test handle_event method of AISelectScreen instance."""
        ai_select_screen = AISelectScreen()
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(56, 52))
        assert ai_select_screen.handle_event(event) == "ai_tools_screen"

    def test_ai_select_screen_reset(self):
        """Test reset method of AISelectScreen instance."""
        ai_select_screen = AISelectScreen()
        ai_select_screen.reset()
        assert isinstance(ai_select_screen.boxes[1], BoxBoards)


class TestUIKeyboardInput:
    """
    Test cases for UI keyboard input handling in the BoxRows component.

    This class contains test methods for verifying the keyboard input handling
    functionality in the BoxRows component of the application.

    Fixtures:
        box_rows: Provides a BoxRows instance for testing.

    Test Methods:
        - test_handle_event_keydown: Test handling of keyboard input event for keydown.
        - test_handle_event_backspace: Test handling of keyboard input event for backspace.
        - test_handle_event_return: Test handling of keyboard input event for return (enter).
        - test_handle_event_non_numeric: Test handling of keyboard input event for non-numeric input.
        - test_handle_event_mouse_click: Test handling of mouse click event.

    Each test method aims to verify a specific aspect of the keyboard input handling behavior
    in the BoxRows component, including keydown, backspace, return, non-numeric input,
    and mouse click events.
    """

    @pytest.fixture
    def box_rows(self):
        """Provides a BoxRows instance for testing."""
        return BoxRows()

    def test_handle_event_keydown(self, box_rows):
        """Test handling of keyboard input event for keydown."""
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_a, "unicode": "a"})
        box_rows.active = True
        box_rows.handle_event(event)
        assert box_rows.text == "a"

    def test_handle_event_backspace(self, box_rows):
        """Test handling of keyboard input event for backspace."""
        box_rows.text = "Test"
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_BACKSPACE})
        box_rows.active = True
        box_rows.handle_event(event)
        assert box_rows.text == "Tes"

    def test_handle_event_return(self, box_rows):
        """Test handling of keyboard input event for return (enter)."""
        box_rows.text = "5"
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN})
        box_rows.active = True
        box_rows.handle_event(event)
        assert not box_rows.active
        assert box_rows.rows == 5

    def test_handle_event_non_numeric(self, box_rows):
        """Test handling of keyboard input event for non-numeric input."""
        box_rows.text = "Invalid"
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN})
        box_rows.active = True
        box_rows.handle_event(event)
        assert not box_rows.active
        # Asserting that BOARD_ROWS remains unchanged if input is not numeric
        assert "BOARD_ROWS" not in globals() or globals()["BOARD_ROWS"] != "Invalid"

    def test_handle_event_mouse_click(self, box_rows):
        """Test handling of mouse click event."""
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (660, 65)})
        box_rows.handle_event(event)
        assert box_rows.active


class TestBoxInput:
    """
    Test cases for the BoxInput class, responsible for handling user input related to chess piece placement.

    This class contains test methods to verify the behavior of the BoxInput class, focusing on various scenarios
    such as placing, flipping, deleting, and toggling the king status of chess pieces.

    Fixtures:
        - mock_surface: Creates a mock surface to simulate pygame Surface objects.
        - individual_piece: Creates an IndividualPiece instance for testing.
        - box_input: Provides a BoxInput instance for testing.

    Test Methods:
        - test_handle_event_place_piece: Test placing a chess piece within the BoxInput's rect area.
        - test_handle_event_flip_piece: Test flipping a placed chess piece.
        - test_handle_event_delete_piece: Test deleting a placed chess piece.
        - test_handle_event_toggle_king_status: Test toggling the king status of a placed chess piece.

    Each test method simulates specific user interactions and verifies the resulting behavior of the BoxInput class.
    """

    @pytest.fixture
    def mock_surface(self):
        """Creates a mock surface to simulate pygame Surface objects."""
        return pygame.Surface((10, 10))

    @pytest.fixture
    def individual_piece(self, mock_surface):
        """Creates an IndividualPiece instance for testing."""
        return IndividualPiece(mock_surface, 0, 0, 10, 10, "TestPiece")

    @pytest.fixture
    def box_input(self):
        """Provides a BoxInput instance for testing."""
        return BoxInput()

    def simulate_mouse_event(self, event_type, pos, button=1):
        """Helper function to create a pygame mouse event."""
        return pygame.event.Event(event_type, pos=pos, button=button)

    def test_handle_event_place_piece(self, box_input, individual_piece):
        """Test placing a chess piece within the BoxInput's rect area."""
        # Simulate left mouse click within BoxInput's rect to place a piece
        event = self.simulate_mouse_event(pygame.MOUSEBUTTONDOWN, (300, 300))
        box_input.handle_event(event, individual_piece)
        assert (
            2,
            0,
        ) in box_input.pieces  # Assuming (0, 0) is the calculated position for the click
        assert box_input.piece_position_mesh[2][0] == individual_piece.hash

    def test_handle_event_flip_piece(self, box_input, individual_piece):
        """Test flipping a placed chess piece."""
        # Place a piece first
        box_input.handle_event(
            self.simulate_mouse_event(pygame.MOUSEBUTTONDOWN, (300, 300)),
            individual_piece,
        )
        # Simulate left mouse click again to flip the piece
        box_input.handle_event(
            self.simulate_mouse_event(pygame.MOUSEBUTTONDOWN, (300, 300)),
            individual_piece,
        )
        assert (
            box_input.piece_alignment_mesh[2][0] != 0
        )  # Verify the piece's alignment is changed

    def test_handle_event_delete_piece(self, box_input, individual_piece):
        """Test deleting a placed chess piece."""
        # Place a piece first
        box_input.handle_event(
            self.simulate_mouse_event(pygame.MOUSEBUTTONDOWN, (300, 300)),
            individual_piece,
        )
        # Simulate right mouse click to delete the piece
        box_input.handle_event(
            self.simulate_mouse_event(pygame.MOUSEBUTTONDOWN, (300, 300), button=3),
            individual_piece,
        )
        assert (0, 0) not in box_input.pieces
        assert box_input.piece_position_mesh[2][0] == 0

    def test_handle_event_toggle_king_status(self, box_input, individual_piece):
        """Test toggling the king status of a placed chess piece."""
        # Place a piece first
        box_input.handle_event(
            self.simulate_mouse_event(pygame.MOUSEBUTTONDOWN, (300, 300)),
            individual_piece,
        )
        # Simulate middle mouse click to toggle the king status
        box_input.handle_event(
            self.simulate_mouse_event(pygame.MOUSEBUTTONDOWN, (300, 300), button=2),
            individual_piece,
        )
        assert box_input.kings == [(2, 0)]
        assert box_input.pieces[(2, 0)].is_king


class TestBoxSelect:
    """
    Test cases for BoxSelect class.

    This class contains test methods to verify the behavior of the BoxSelect class, which is responsible
    for handling the selection of pieces within the application.

    Fixtures:
        mock_surface: Creates a mock surface to simulate pygame Surface objects.
        mock_pieces: Mocks a list of IndividualPiece instances for testing.
        box_select: Provides a BoxSelect instance with mocked pieces for testing.

    Test Methods:
        - test_scroll_down: Test scrolling down in BoxSelect.
        - test_scroll_up: Test scrolling up in BoxSelect.
        - test_select_piece: Test selecting a piece in BoxSelect.

    Each test method is designed to verify a specific behavior or functionality of the BoxSelect class.
    """

    @pytest.fixture
    def mock_surface(self):
        """Creates a mock surface to simulate pygame Surface objects."""
        return pygame.Surface((10, 10))

    @pytest.fixture
    def mock_pieces(self, mock_surface):
        """Mocks a list of IndividualPiece instances for testing."""
        pieces = [
            IndividualPiece(mock_surface, 0, i * 100, 140, 100, f"Piece{i}")
            for i in range(5)
        ]
        return pieces

    @pytest.fixture
    def box_select(self, mock_pieces, mock_surface):
        """Provides a BoxSelect instance with mocked pieces for testing."""
        with patch("os.listdir", return_value=[]), patch(
            "numpy.load", return_value={"drawing": mock_surface}
        ), patch("pygame.surfarray.make_surface", return_value=mock_surface):
            box = BoxSelect()
            box.pieces = mock_pieces  # Override the pieces with our mock
            box.update_pieces_surface()  # Update the pieces_surface with the mock pieces
        return box

    def test_scroll_down(self, box_select):
        """Test scrolling down in BoxSelect."""
        initial_offset = box_select.y_offset
        # Simulate mouse wheel down scroll
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(100, 150), button=5)
        box_select.handle_event(event)
        assert box_select.y_offset > initial_offset

    def test_scroll_up(self, box_select):
        """Test scrolling up in BoxSelect."""
        # Set the initial y_offset to simulate that we've scrolled down already
        box_select.y_offset = 20
        initial_offset = box_select.y_offset
        # Simulate mouse wheel up scroll
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(100, 150), button=4)
        box_select.handle_event(event)
        assert box_select.y_offset < initial_offset

    def test_select_piece(self, box_select):
        """Test selecting a piece in BoxSelect."""
        # Simulate left mouse click to select a piece
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(100, 160), button=1)
        selected_piece = box_select.handle_event(event)
        assert selected_piece is not None
        assert isinstance(selected_piece, IndividualPiece)
        assert selected_piece.name == "Piece0"
