# Advanced challenge: streaming ingestion

Build the matching solution module for SentinelFlow streaming. Keep processing lazy where possible, bound memory by batch size, and describe complexity.

Requirements:
- Do not materialize the full stream unless the challenge explicitly asks for replay.
- Handle exhausted streams deliberately.
- Use clear errors for invalid stream inputs.
