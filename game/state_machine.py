from enum import Enum, auto


class GameState(Enum):
    WAITING_FOR_MATCH = auto()
    VS_SCREEN = auto()
    PLAYING = auto()
    MATCH_ENDED = auto()


class GameStateMachine:    
    def __init__(self):
        self.state = GameState.WAITING_FOR_MATCH
    
    def update(self, frame, detectors):
        """
        Update state based on current frame.
        
        Args:
            frame: Current BGR frame
            detectors: Dict with "vs" detector (add more as needed)
        
        Returns:
            Event string if state changed, None otherwise
        """
        if self.state == GameState.WAITING_FOR_MATCH:
            if detectors["vs"].detect(frame):
                self.state = GameState.VS_SCREEN
                return "match_found"
        
        elif self.state == GameState.VS_SCREEN:
            # VS screen disappears when match starts
            if not detectors["vs"].detect(frame):
                self.state = GameState.PLAYING
                return "game_started"
        
        elif self.state == GameState.PLAYING:
            # Add end screen detection here when ready
            # if detectors["end_screen"].detect(frame):
            #     self.state = GameState.MATCH_ENDED
            #     return "match_ended"
            pass
        
        elif self.state == GameState.MATCH_ENDED:
            # Add lobby detection to reset
            # if detectors["lobby"].detect(frame):
            #     self.state = GameState.WAITING_FOR_MATCH
            #     return "back_to_lobby"
            pass
        
        return None
    
    def reset(self):
        """Reset to waiting state."""
        self.state = GameState.WAITING_FOR_MATCH
    
    def is_playing(self):
        """Check if currently in a match."""
        return self.state == GameState.PLAYING