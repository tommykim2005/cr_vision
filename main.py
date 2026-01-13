import cv2

from core.window_finder import find_window
from core.screen_capture import ScreenCapture
from game.troop_detector import TroopDetector
from game.troop_tracker import TroopTracker
from game.enemy_tracker import EnemyTracker
from game.vs_detector import VSDetector
from game.state_machine import GameStateMachine
from game.troop_costs import TROOP_COSTS

def main():
    # Find BlueStacks window
    monitor = find_window("BlueStacks")
    if not monitor:
        print("ERROR: BlueStacks window not found")
        return
    print(f"Found window: {monitor}")
    
    # Initialize components
    capture = ScreenCapture(monitor)
    detector = TroopDetector("models/best.pt")
    tracker = TroopTracker(min_conf=0.6, required_frames=3, max_gap=3)
    enemy = EnemyTracker(start_elixir=5)
    vs_detector = VSDetector("images/vs_icon.png", threshold=0.75)
    state_machine = GameStateMachine()
    
    detectors = {"vs": vs_detector}
    
    print("Waiting for match...")
    
    while True:
        frame = capture.grab()
        
        # Update state machine
        event = state_machine.update(frame, detectors)
        
        if event == "match_found":
            print("Match found! Waiting for game to start...")
        
        elif event == "game_started":
            print("Game started!")
            enemy.start_match()
        
        # Only track when playing
        if state_machine.is_playing():
            enemy.update()
            
            detections = detector.detect(frame)
            deployments = tracker.process(detections)
            
            for card in deployments:
                enemy.register_card(card)
                cost = TROOP_COSTS.get(card, 0)
                status = enemy.get_status()
                
                print(f"\n{'='*40}")
                print(f"Enemy played: {card} (-{cost} elixir)")
                print(f"Enemy elixir: ~{status['elixir']}")
                print(f"Deck seen: {status['deck']}")
                print(f"Recent cycle: {status['cycle']}")
                print(f"Likely in hand: {enemy.get_hand_prediction()}")
                print(f"{'='*40}")
        
        # Display
        try:
            annotated = detector.get_annotated_frame(frame)
        except ValueError:
            annotated = frame
        
        # Draw status overlay
        if state_machine.is_playing():
            status = enemy.get_status()
            cv2.putText(annotated, f"Enemy Elixir: ~{status['elixir']}", 
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.putText(annotated, f"Cycle: {status['cycle']}", 
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        else:
            cv2.putText(annotated, f"State: {state_machine.state.name}", 
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        
        cv2.imshow("Clash Tracker", annotated)
        
        if cv2.waitKey(1) == ord('q'):
            break
    
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()