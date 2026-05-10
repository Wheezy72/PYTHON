# Entry challenge: Length-prefixed event frames

Build a small SentinelFlow framing exercise that proves an event dictionary can
travel through a socket-safe byte protocol and arrive unchanged.

## Goal

Create the entry-level solution behavior for a function named
`round_trip_event`. The function receives one event dictionary, encodes it into a
length-prefixed JSON frame, then decodes that frame back into a dictionary.

## Input

Use a plain SentinelFlow event dictionary such as:

- event id: `evt-1001`
- source: `sensor.edge-7`
- severity: `4`
- message: `temperature threshold crossed`

The event may include extra JSON-compatible fields.

## Expected behavior

- Produce a dictionary equal to the original event.
- Encode the JSON payload as bytes before decoding it again.
- Prefix the payload with a four-byte big-endian payload length.
- Reject malformed frames through the framing helpers rather than silently
  accepting bad input.
- Keep the implementation in the matching solution module, not in this prompt.

## Complexity questions

- Why is encoding or decoding O(b), where b is the payload byte length?
- Why does the frame need O(b) space?
- Why is a length prefix useful for TCP streams that may split payloads over
  multiple reads?
