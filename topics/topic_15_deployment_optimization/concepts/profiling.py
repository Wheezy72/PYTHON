"""Profiling helper."""
import cProfile, pstats, io

def profile_callable(func, *args, **kwargs):
    profiler=cProfile.Profile(); profiler.enable(); result=func(*args, **kwargs); profiler.disable(); stream=io.StringIO(); pstats.Stats(profiler, stream=stream).sort_stats("cumtime").print_stats(5); return result, stream.getvalue()
