"""Entry solution for Topic 12."""
from topics.topic_12_os_interaction_subprocesses.concepts.environment import read_config

def load_runtime_config(env):
    return {"mode": read_config(env, "SENTINEL_MODE", "dev"), "region": read_config(env, "SENTINEL_REGION", "local")}
