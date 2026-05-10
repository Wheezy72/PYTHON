"""Argparse command construction."""
import argparse

def build_parser():
    parser=argparse.ArgumentParser(prog="sentinelflow")
    sub=parser.add_subparsers(dest="command", required=True)
    ingest=sub.add_parser("ingest"); ingest.add_argument("source")
    status=sub.add_parser("status"); status.add_argument("--json", action="store_true")
    return parser
