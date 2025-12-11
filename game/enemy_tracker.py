import time
from .troop_costs import TROOP_COSTS

"""Tracks enemy elixir and card cycle."""
class EnemyTracker:
    # Initial constructor -> elixer, max_elixer, fps, regen_per_frame, card_history, deck, cycle
    def __init__(self, start_elixir=5, fps=10):
        self.elixir = start_elixir
        self.max_elixir = 10.0
        self.fps = fps  # Estimated frames per second
        self.regen_per_frame = 1 / (2.8 * fps)  # Elixir per frame
        
        # Cycle tracking
        self.card_history = []
        self.deck = []
        self.cycle = []
    
    def start_match(self):
        """Reset tracker for new match."""
        self.elixir = 5.0
        self.card_history = []
        self.deck = []
        self.cycle = []
    
    def update(self):
        """Call every frame to regenerate elixir."""
        self.elixir = min(self.max_elixir, self.elixir + self.regen_per_frame)
    
    def set_fps(self, fps):
        """Update FPS if you measure it."""
        self.fps = fps
        self.regen_per_frame = 1 / (2.8 * fps)
    
    def register_card(self, card_name):
        """Register an enemy card deployment."""
        cost = TROOP_COSTS.get(card_name, 0)
        self.elixir = max(0, self.elixir - cost)
        
        self.card_history.append({
            "card": card_name,
            "cost": cost
        })
        
        if card_name not in self.deck:
            self.deck.append(card_name)
        
        if card_name in self.cycle:
            self.cycle.remove(card_name)
        self.cycle.append(card_name)
        if len(self.cycle) > 4:
            self.cycle.pop(0)
    
    def get_status(self):
        return {
            "elixir": round(self.elixir, 1),
            "deck": self.deck,
            "cycle": self.cycle,
            "cards_played": len(self.card_history)
        }
    
    def get_hand_prediction(self):
        if len(self.deck) < 5:
            return None
        return [c for c in self.deck if c not in self.cycle]