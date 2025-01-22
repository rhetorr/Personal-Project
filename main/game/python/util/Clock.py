import time as clock
class Clock:
    def __init__(self):
        self.last_timestamp = clock.time
        self.doing_timeout = False
    def time() -> float:
        return clock.time
    def elapsed_since(old_time: float) -> float:
        return clock.time - old_time
    def timeout(self, duration: float) -> bool:
        if not self.doing_timeout:
            self.last_timestamp = clock.time
        done = self.doing_timeout and clock.time - self.last_timestamp > duration
        self.doing_timeout = not done
        return done