import time
from .troop_costs import TROOP_COSTS


class EnemyTracker:
    """Tracks enemy elixir and card cycle."""

    ELIXIR_PER_SECOND = 1 / 2.8

    def __init__(self, start_elixir=5):
        self.elixir = start_elixir
        self.max_elixir = 10.0
        self._last_update_time = None

        # Cycle tracking
        self.card_history = []
        self.deck = []
        self.cycle = []

    def start_match(self):
        """Reset tracker for new match."""
        self.elixir = 5.0
        self._last_update_time = time.monotonic()
        self.card_history = []
        self.deck = []
        self.cycle = []

    def update(self):
        """Call every frame to regenerate elixir using wall-clock time."""
        now = time.monotonic()
        if self._last_update_time is not None:
            elapsed = now - self._last_update_time
            self.elixir = min(self.max_elixir,
                              self.elixir + elapsed * self.ELIXIR_PER_SECOND)
        self._last_update_time = now

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
