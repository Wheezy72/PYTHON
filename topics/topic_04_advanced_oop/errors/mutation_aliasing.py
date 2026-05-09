"""Object mutation and aliasing demonstrations."""
def unsafe_attach_tag(event, tag):
    event.setdefault("tags", []).append(tag)
    return event

def safe_attach_tag(event, tag):
    copied = dict(event)
    copied["tags"] = (*tuple(event.get("tags", ())), tag)
    return copied
