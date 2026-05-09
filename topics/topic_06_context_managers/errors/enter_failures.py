"""Failed-enter cleanup pattern."""
class FailingEnter:
    def __init__(self, log):
        self.log = log
    def __enter__(self):
        self.log.append("enter-start")
        self.log.append("cleanup")
        raise RuntimeError("enter failed")
    def __exit__(self, exc_type, exc, tb):
        self.log.append("exit")
        return False
