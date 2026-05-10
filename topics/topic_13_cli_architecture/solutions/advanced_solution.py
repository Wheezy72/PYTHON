"""Advanced solution for Topic 13."""
from topics.topic_13_cli_architecture.solutions.entry_solution import parse_cli
from topics.topic_13_cli_architecture.solutions.mid_solution import build_router

def run_cli(argv):
    args=parse_cli(argv); return build_router().dispatch(args.command, args)
