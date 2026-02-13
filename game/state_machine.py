import time
from enum import Enum, auto


class GameState(Enum):
    WAITING_FOR_MATCH = auto()
    VS_SCREEN = auto()
    PLAYING = auto()
    MATCH_ENDED = auto()


class GameStateMachine:
    MIN_PLAY_DURATION = 30  # seconds before checking for match end

    def __init__(self):
        self.state = GameState.WAITING_FOR_MATCH
        self._play_start_time = None

    def update(self, frame, vs_detector):
        """
        Update state based on current frame.

        Args:
            frame: Current BGR frame
            vs_detector: VSDetector instance

        Returns:
            Event string if state changed, None otherwise
        """
        if self.state == GameState.WAITING_FOR_MATCH:
            if vs_detector.detect(frame):
                self.state = GameState.VS_SCREEN
                return "match_found"

        elif self.state == GameState.VS_SCREEN:
            if not vs_detector.detect(frame):
                self.state = GameState.PLAYING
                self._play_start_time = time.monotonic()
                return "game_started"

        elif self.state == GameState.PLAYING:
            if self._play_start_time is not None:
                elapsed = time.monotonic() - self._play_start_time
                if elapsed >= self.MIN_PLAY_DURATION:
                    if vs_detector.detect(frame):
                        self.state = GameState.MATCH_ENDED
                        return "match_ended"

        elif self.state == GameState.MATCH_ENDED:
            self.state = GameState.VS_SCREEN
            return "new_match_found"

        return None

    def reset(self):
        """Reset to waiting state."""
        self.state = GameState.WAITING_FOR_MATCH
        self._play_start_time = None

    def is_playing(self):
        """Check if currently in a match."""
        return self.state == GameState.PLAYING
