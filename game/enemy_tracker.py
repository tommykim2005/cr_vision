import time
from .troop_costs import TROOP_COSTS


class EnemyTracker:
    """Tracks enemy elixir and card cycle."""
    
    def __init__(self, start_elixir=5):
        self.elixir = start_elixir
        self.max_elixir = 10.0
        self.regen_rate = 1 / 2.8  # Elixir per second
        self.last_update = None
        
        # Cycle tracking
        self.card_history = []
        self.deck = []   # All unique cards seen (max 8)
        self.cycle = []  # Last 4 cards played
    
    def start_match(self):
        """Reset tracker for new match."""
        self.elixir = 5.0
        self.last_update = time.time()
        self.card_history = []
        self.deck = []
        self.cycle = []
    
    def update(self):
        """Call every frame to regenerate elixir."""
        if self.last_update is None:
            self.last_update = time.time()
            return
        
        now = time.time()
        delta = now - self.last_update
        self.elixir = min(self.max_elixir, self.elixir + delta * self.regen_rate)
        self.last_update = now
    
    def register_card(self, card_name):
        """Register an enemy card deployment."""
        cost = TROOP_COSTS.get(card_name, 0)
        self.elixir = max(0, self.elixir - cost)
        
        self.card_history.append({
            "card": card_name,
            "time": time.time(),
            "cost": cost
        })
        
        # Update deck (max 8 cards)
        if card_name not in self.deck:
            self.deck.append(card_name)
        
        # Update cycle (last 4 played)
        if card_name in self.cycle:
            self.cycle.remove(card_name)
        self.cycle.append(card_name)
        if len(self.cycle) > 4:
            self.cycle.pop(0)
    
    def get_status(self):
        """Get current enemy status."""
        return {
            "elixir": round(self.elixir, 1),
            "deck": self.deck,
            "cycle": self.cycle,
            "cards_played": len(self.card_history)
        }
    
    def get_hand_prediction(self):
        """Predict what cards are currently in enemy hand."""
        if len(self.deck) < 5:
            return None
        
        # Cards not in current cycle are in hand
        in_hand = [c for c in self.deck if c not in self.cycle]
        return in_hand