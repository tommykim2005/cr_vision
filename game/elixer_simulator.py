import time

class ElixerSimulator:
    def __init__(self, start_elixer = 5):
        self.elixer = start_elixer
        self.last_update = time.time() # starts timer at 0
        self.regen_rate = 1 / 2.8 # elixers per second

    
    def update(self):

        now = time.time() # updates time -> now
        delta = now - self.last_update # now - last update
        self.elixer += delta * self.regen_rate # regen elixer by delta
        self.last_update = now
        if self.elixer > 10:
            self.elixer = 10

    def spend(self, amount):
        self.elixer -= amount

    def get_elixer(self):
        return self.elixer