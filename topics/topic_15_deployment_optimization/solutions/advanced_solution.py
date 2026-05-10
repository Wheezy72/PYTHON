"""Advanced solution for Topic 15."""
from topics.topic_15_deployment_optimization.concepts.profiling import profile_callable
from topics.topic_15_deployment_optimization.dsa.benchmark_table import BenchmarkTable

def deployment_report(func, *args):
    result, profile = profile_callable(func, *args); table=BenchmarkTable(); table.add(func.__name__, 0.0); return {"result":result, "profile_contains":func.__name__ in profile, "fastest":table.fastest()}
