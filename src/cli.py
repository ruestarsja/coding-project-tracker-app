from src.app import App

import json

__app = App()

def run_command(args:list):

    # python3 run.py <subcommand> <args>
    #
    # subcommand: the subcommand to run; this value must be one of: new, del, edit, get, list
    #
    #       args: the arguments for the relative subcommand; see below for specifics for each
    #             subcommand

    subcommand = args[0]
    match subcommand:
        case "new":
            __new(args[1:])
        case "del":
            __del(args[1:])
        case "edit":
            __edit(args[1:])
        case "get":
            __get(args[1:])
        case "list":
            __list(args[1:])
        case _:
            raise ValueError(f"unknown subcommand '{subcommand}'")

def __new(args:list):

    # python3 run.py new <project_name>[ <category>[ <description>]]
    #
    # project_name: the name of the new project; this serves as the project id and must be unique
    #               to each project
    #
    #     category: the category the project falls in (defaults to backlogged); this value must be
    #               one of: active, occasional, hiatused, backlogged, completed, abandoned
    #
    #  description: an optional text description of the project

    output = None
    match len(args):
        case 0:
            raise ValueError("too few arguments")
        case 1 | 2 | 3:
            output = __app.call_isolated(__app.create_project, args)
        case _:
            raise ValueError("too many arguments")
    match output:
        case True:
            print(f"Created new project '{args[0]}'")
        case False:
            print(f"Failed to create new project '{args[0]}' (maybe it already exists?)")
        case _:
            print(f"WARNING: Received unexpected return value {output} from App.create_project()")

def __del(args:list):

    # python3 run.py del <project_name>
    #
    # project_name: the name of the project to delete; this serves as the project id and is unique
    #               to each project

    output = None
    match len(args):
        case 0:
            raise ValueError("too few arguments")
        case 1:
            output = __app.call_isolated(__app.delete_project, args)
        case _:
            raise ValueError("too many arguments")
    match output:
        case True:
            print(f"Deleted project '{args[0]}'")
        case False:
            print(f"Failed to delete project '{args[0]}' (maybe it doesn't exist?)")
        case _:
            print(f"WARNING: Received unexpected return value {output} from App.delete_project()")

def __edit(args:list):

    # python3 run.py edit <project_name> <field> <new_value>
    #
    # project_name: the name of the project to edit; this serves as the project id and is unique to
    #               each project
    #
    #        field: the name of the field to edit; this value must be one of: name, category,
    #               description
    #
    #    new_value: the value to put into the specified field, in place of the existing one; this
    #               value may be restricted depending on the specified field

    output = None
    match len(args):
        case 0 | 1 | 2:
            raise ValueError("too few arguments")
        case 3:
            match args[1]:
                case "name":
                    output = __app.call_isolated(__app.update_project_name, [args[0], args[2]])
                case "category":
                    output = __app.call_isolated(__app.update_project_category, [args[0], args[2]])
                case "description":
                    output = __app.call_isolated(__app.update_project_description, [args[0], args[2]])
                case _:
                    raise ValueError(f"unknown field '{args[1]}'")
        case _:
            raise ValueError("too many arguments")
    match output:
        case True:
            print(f"Updated project '{args[0]}' field '{args[1]}' to value '{args[2]}'")
        case False:
            print(f"Failed to update project '{args[0]}' field '{args[1]}' to value '{args[2]}' (maybe it doesn't exist, or the specified value is invalid?)")
        case _:
            print(f"WARNING: Received unexpected return value {output} from one of App.update_project_<>() functions")

def __get(args:list):

    # python3 run.py get <project_name>[ <field>[...]]
    #
    # project_name: the name of the project to get information from; this serves as the project id
    #               and is unique to each project
    #
    #        field: the name of the field(s) to get information from; may specify multiple. if none
    #               are specified, gets all fields from the specified project

    output = None
    match len(args):
        case 0:
            raise ValueError("too few arguments")
        case 1:
            output = __app.call_isolated(__app.get_project_info, args)
        case 2:
            match args[1]:
                case "name":
                    output = __app.call_isolated(__app.get_project_name, [args[0]])
                case "category":
                    output = __app.call_isolated(__app.get_project_category, [args[0]])
                case "description":
                    output = __app.call_isolated(__app.get_project_description, [args[0]])
        case _:
            output = __app.call_isolated(__app.get_project_fields, [args[0], args[1:]])
    match output:
        case None:
            print(f"Failed to fetch fields from project '{args[0]}' (maybe it doesn't exist, or the specified fields are invalid?)")
        case _:
            print(json.dumps(output, indent=4))

def __list(args:list):

    # python3 run.py list [<category>[...]|all] [<flags>]
    #
    #           category: the category (or categories) to list projects from; this value must be
    #                     one of: active, occasional, hiatused, backlogged, completed, abandoned;
    #                     may be substituted with 'all' (default all)
    #
    #      --compact, -c: don't include any fields from each project (this is the default)
    #
    # --get <field>[...], include the specified fields from each project
    #    -g <field>[...]:
    #
    #      --verbose, -v: include all fields from each project

    output = None
    match len(args):
        case 0:
            output = {}
            for category in __app.VALID_CATEGORIES:
                output[category] = __app.call_isolated(__app.get_category_project_names, [category])
        case _:
            category_args:list = []
            style:str = 'compact'
            field_args:list = []
            if args[0] == "all" or args[0][0] == '-':
                category_args = __app.VALID_CATEGORIES
            i:int = 0
            while i < len(args) and args[i][0] != '-':
                category_args.append(args[i])
                i += 1
            if i < len(args):
                match args[i]:
                    case "--compact" | "-c":
                        style = 'compact'
                    case "--verbose" | "-v":
                        style = 'verbose'
                    case "--get" | "-g":
                        style = 'get'
                    case _:
                        raise ValueError(f"unknown flag '{args[i]}'")
                i += 1
            while i < len(args):
                field_args.append(args[i])
                i += 1
            match style:
                case 'compact':
                    if len(field_args) != 0:
                        raise ValueError(f"flag '{args[-1 - len(field_args)]}' does not take args")
                    output = {}
                    for category in category_args:
                        output[category] = __app.call_isolated(__app.get_category_project_names, [category])
                case 'verbose':
                    if len(field_args) != 0:
                        raise ValueError(f"flag '{args[-1 - len(field_args)]}' does not take args")
                    output = {}
                    for category in category_args:
                        output[category] = __app.call_isolated(__app.get_category_projects, [category])
                case 'get':
                    if len(field_args) == 0:
                        raise ValueError(f"flag '{args[-1]}' takes at least one arg")
                    output = {}
                    for category in category_args:
                        category_project_names:list = __app.call_isolated(__app.get_category_project_names, [category])
                        category_projects:dict = {}
                        for project_name in category_project_names:
                            category_projects[project_name] = __app.call_isolated(__app.get_project_fields, [project_name, field_args])
                        output[category] = category_projects

    # getting individual projects may have returned None if asking for invalid fields; these get
    # baked in rather than handled, so here, i check for them to handle it
    if type(output) == dict and output != {}:
        first_category:dict|list = output[list(output.keys())[0]]
        if type(first_category) == dict and first_category != {}:
            first_project:dict|None = first_category[list(first_category.keys())[0]]
            if first_project == None:
                output = None

    match output:
        case None:
            print("ya done fucked up son")
        case _:
            print(json.dumps(output, indent=4))
