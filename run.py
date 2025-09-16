from src.app import App
import src.cli

import sys

def main():
    subcommands = (
        "new",
        "del",
        "edit",
        "get",
        "list"
    )

    run = 'gui'

    if len(sys.argv) > 1 and sys.argv[1] in subcommands:
        run = 'cli'
    else:
        for arg in sys.argv[1:]:
            match arg:
                case "--help" | "-h":
                    run = None
                    print(f"{sys.argv[0]} help will be shown here before release version.")
                case "--version" | "-v":
                    run = None
                    print(f"{sys.argv[0]} is not yet released.")
                case _:
                    run = None
                    raise ValueError(f"unknown argument '{arg}'")

    if run == 'gui':
        # launch gui
        print("The GUI would be launched now, if there was one.")
        print("But there's not.")
        print("So you just get this message instead.")
    elif run == 'cli':
        src.cli.run_command(sys.argv[1:])
    

if __name__ == "__main__":
    main()
