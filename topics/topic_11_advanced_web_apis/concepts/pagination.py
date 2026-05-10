"""Pagination helpers."""
def paginate(items, page_size):
    if page_size <= 0: raise ValueError("page_size must be positive")
    for start in range(0, len(items), page_size):
        yield tuple(items[start:start+page_size])
