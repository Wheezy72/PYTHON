"""Advanced solution for Topic 09."""
from topics.topic_09_file_systems_streams.dsa.event_log_file import EventLogFile
from topics.topic_09_file_systems_streams.dsa.replay_stream import replay_window
def persist_and_replay(path, events, limit=2):
    log = EventLogFile(path).write(events)
    all_events = log.read_all()
    return {"events": all_events, "recent": replay_window(all_events, limit), "count": len(all_events)}
