# Advanced challenge: managed ingestion session

Build the matching SentinelFlow context manager solution. Ensure resources close deterministically and exceptions behave according to the prompt.

Requirements:
- Clean up resources on success and failure.
- Keep transaction commits atomic.
- Avoid suppressing unexpected exceptions.
