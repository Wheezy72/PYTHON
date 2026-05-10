"""Environment configuration helpers."""
def read_config(env, key, default=None):
    return env.get(key, default)
