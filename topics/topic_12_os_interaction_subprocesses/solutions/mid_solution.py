"""Mid solution for Topic 12."""
from topics.topic_12_os_interaction_subprocesses.concepts.subprocess_runner import run_command
from topics.topic_12_os_interaction_subprocesses.errors.process_errors import require_success

def run_checked(args):
    return require_success(run_command(args)).stdout
