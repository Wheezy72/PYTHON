"""In-memory stream helpers."""
from io import StringIO
def render_lines(lines):
    buffer = StringIO()
    for line in lines:
        buffer.write(str(line) + "\n")
    return buffer.getvalue()
