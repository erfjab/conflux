import os


def clear_terminal():
    osname = os.name
    if osname == "posix":
        command = "clear"
    elif osname == "nt":
        command = "cls"
    else:
        return

    os.system(command)
