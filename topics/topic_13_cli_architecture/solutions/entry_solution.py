"""Entry solution for Topic 13."""
from topics.topic_13_cli_architecture.concepts.argparse_commands import build_parser

def parse_cli(argv):
    return build_parser().parse_args(argv)
