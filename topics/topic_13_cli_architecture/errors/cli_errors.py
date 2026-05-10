"""CLI error types."""
class CliUsageError(ValueError): pass

def require_command(args):
    if not getattr(args, "command", None): raise CliUsageError("command is required")
    return args
