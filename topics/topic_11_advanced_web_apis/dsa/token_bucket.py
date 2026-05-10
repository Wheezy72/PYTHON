"""Token bucket rate limiter."""
class TokenBucket:
    def __init__(self, capacity):
        if capacity <= 0: raise ValueError("capacity must be positive")
        self.capacity=capacity; self.tokens=capacity
    def allow(self):
        if self.tokens <= 0: return False
        self.tokens -= 1; return True
    def refill(self): self.tokens=self.capacity
