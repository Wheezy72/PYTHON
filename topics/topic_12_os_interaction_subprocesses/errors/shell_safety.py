"""Shell safety validators."""
def reject_shell_string(command):
    if isinstance(command, str): raise TypeError("use argument lists instead of shell strings")
    return tuple(command)
