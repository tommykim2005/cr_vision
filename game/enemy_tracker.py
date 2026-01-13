import time
from .troop_costs import TROOP_COSTS

"""Tracks enemy elixir and card cycle."""
class EnemyTracker:
    # Elixir regen rates (seconds per 1 elixir)
    REGEN_NORMAL = 2.8
    REGEN_DOUBLE = 1.4
    REGEN_TRIPLE = 0.9

    def __init__(self, start_elixir=5):
        self.start_elixir = start_elixir
        self.max_elixir = 10.0

        self.elixir = start_elixir
        self.last_update_time = None
        self.match_start_time = None

        # Cycle tracking
        self.card_history = []
        self.deck = []
        self.cycle = []

    def start_match(self):
        """Reset tracker for new match."""
        self.elixir = self.start_elixir
        self.match_start_time = time.time()
        self.last_update_time = time.time()
        self.card_history = []
        self.deck = []
        self.cycle = []

    def _get_regen_rate(self):
        """Get current regen rate based on game phase."""
        if self.match_start_time is None:
            return self.REGEN_NORMAL

        elapsed = time.time() - self.match_start_time

        # Standard match is 3 minutes (180s)
        # Double elixir starts at 2:00 remaining (60s elapsed)
        # Triple elixir starts at 1:00 remaining (120s elapsed)
        if elapsed >= 120:
            return self.REGEN_TRIPLE
        elif elapsed >= 60:
            return self.REGEN_DOUBLE
        else:
            return self.REGEN_NORMAL

    def update(self):
        """Call each frame to regenerate elixir based on real elapsed time."""
        now = time.time()

        if self.last_update_time is None:
            self.last_update_time = now
            return

        elapsed = now - self.last_update_time
        regen_rate = self._get_regen_rate()
        elixir_gained = elapsed / regen_rate

        self.elixir = min(self.max_elixir, self.elixir + elixir_gained)
        self.last_update_time = now
    
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