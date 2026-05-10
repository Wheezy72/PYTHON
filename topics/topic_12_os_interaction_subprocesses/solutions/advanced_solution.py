"""Advanced solution for Topic 12."""
from topics.topic_12_os_interaction_subprocesses.concepts.subprocess_runner import run_command
from topics.topic_12_os_interaction_subprocesses.dsa.process_history import ProcessHistory

def supervise_commands(commands):
    history=ProcessHistory(); outputs=[]
    for command in commands:
        result=run_command(command); history.add(command, result.returncode); outputs.append(result.stdout)
    return {"outputs":tuple(outputs), "failures":history.failures(), "count":len(history)}
