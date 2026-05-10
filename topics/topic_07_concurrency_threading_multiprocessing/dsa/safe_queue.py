"""FIFO queue draining."""
def drain_queue(queue):
    output = []
    while not queue.empty():
        output.append(queue.get())
    return tuple(output)
