def run_command(args:list):
    subcommand = args[0]
    match subcommand:
        case "refresh":
            pass
        case "new":
            pass
        case "del":
            pass
        case "edit":
            pass
        case "get":
            pass
        case "list":
            pass
        case _:
            raise ValueError(f"unknown subcommand '{subcommand}'")

def __refresh():
    pass

def __new():
    pass

def __del():
    pass

def __edit():
    pass

def __get():
    pass

def __list():
    pass
