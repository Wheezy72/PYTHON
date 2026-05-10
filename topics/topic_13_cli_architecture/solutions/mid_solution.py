"""Mid solution for Topic 13."""
from topics.topic_13_cli_architecture.dsa.command_router import CommandRouter

def build_router():
    router=CommandRouter(); router.register("status", lambda args: {"status":"ok", "json":getattr(args,"json",False)}); router.register("ingest", lambda args: {"ingested_from":args.source}); return router
