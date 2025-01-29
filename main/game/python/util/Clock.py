import time as clock
from .mathextra import MathModule
class StopWatch:
    def __init__(self):
        self.last_timestamp = self.time()
        self.doing_timeout = False
    def time(self) -> float:
        return MathModule.round_to(clock.time(), 0.001)
    def elapsed_since(self, old_time: float) -> float:
        return self.time() - old_time
    def timeout(self, duration: float) -> bool:
        if not self.doing_timeout:
            self.last_timestamp = self.time()
        done = ((self.time() - self.last_timestamp) > duration)
        self.doing_timeout = not done
        return done