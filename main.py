import cv2

from core import find_window, ScreenCapture
from game import (TroopDetector, TroopTracker, EnemyTracker,
                  VSDetector, GameStateMachine, TROOP_COSTS)

# Configuration constants
WINDOW_NAME = "BlueStacks"
MODEL_PATH = "models/bestv2.pt"
VS_TEMPLATE_PATH = "images/vs_icon.png"
VS_THRESHOLD = 0.75
TRACKER_MIN_CONF = 0.6
TRACKER_REQUIRED_FRAMES = 3
TRACKER_MAX_GAP = 3
START_ELIXIR = 5
WINDOW_TITLE = "Clash Tracker"


class GameApp:
    def __init__(self):
        self.capture = None
        self.detector = None
        self.tracker = None
        self.enemy = None
        self.vs_detector = None
        self.state_machine = None

    def initialize(self):
        """Find window and create all components. Returns False on failure."""
        monitor = find_window(WINDOW_NAME)
        if not monitor:
            print(f"ERROR: {WINDOW_NAME} window not found")
            return False
        print(f"Found window: {monitor}")

        self.capture = ScreenCapture(monitor)
        self.detector = TroopDetector(MODEL_PATH)
        self.tracker = TroopTracker(
            min_conf=TRACKER_MIN_CONF,
            required_frames=TRACKER_REQUIRED_FRAMES,
            max_gap=TRACKER_MAX_GAP,
            frame_width=monitor["width"],
            frame_height=monitor["height"],
        )
        self.enemy = EnemyTracker(start_elixir=START_ELIXIR)
        self.vs_detector = VSDetector(VS_TEMPLATE_PATH, threshold=VS_THRESHOLD)
        self.state_machine = GameStateMachine()
        return True

    def _handle_event(self, event):
        """React to state machine events."""
        if event == "match_found":
            print("Match found! Waiting for game to start...")

        elif event == "game_started":
            print("Game started!")
            self.enemy.start_match()

        elif event == "match_ended":
            print("Match ended!")
            self.tracker.reset()

        elif event == "new_match_found":
            print("New match found! Waiting for game to start...")

    def _process_frame(self, frame):
        """Run detection, tracking, and print deployments."""
        self.enemy.update()

        detections = self.detector.detect(frame)
        deployments = self.tracker.process(detections)

        for card in deployments:
            self.enemy.register_card(card)
            cost = TROOP_COSTS.get(card, 0)

            print(f"\n{'='*40}")
            print(f"Enemy played: {card} (-{cost} elixir)")
            print(f"Enemy elixir: ~{round(self.enemy.elixir, 1)}")
            print(f"Deck seen: {self.enemy.deck}")
            print(f"Recent cycle: {self.enemy.cycle}")
            print(f"Likely in hand: {self.enemy.get_hand_prediction()}")
            print(f"{'='*40}")

    def _render(self, frame):
        """Annotate frame, draw overlays, and display."""
        if self.state_machine.is_playing() and self.detector.has_results:
            annotated = self.detector.get_annotated_frame()
        else:
            annotated = frame.copy()

        if self.state_machine.is_playing():
            status = self.enemy.get_status()
            cv2.putText(annotated, f"Enemy Elixir: ~{status['elixir']}",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.putText(annotated, f"Cycle: {status['cycle']}",
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        else:
            cv2.putText(annotated, f"State: {self.state_machine.state.name}",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

        cv2.imshow(WINDOW_TITLE, annotated)

    def run(self):
        """Main loop."""
        print("Waiting for match...")

        while True:
            frame = self.capture.grab()

            event = self.state_machine.update(frame, self.vs_detector)
            if event:
                self._handle_event(event)

            if self.state_machine.is_playing():
                self._process_frame(frame)

            self._render(frame)

            if cv2.waitKey(1) == ord('q'):
                break

        cv2.destroyAllWindows()


def main():
    app = GameApp()
    if app.initialize():
        app.run()


if __name__ == "__main__":
    main()
