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
            raise SyntaxError("too few arguments")
        case 1 | 2 | 3:
            output = __app.call_isolated(__app.create_project, *args)
        case _:
            raise SyntaxError("too many arguments")
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
            raise SyntaxError("too few arguments")
        case 1:
            output = __app.call_isolated(__app.delete_project, *args)
        case _:
            raise SyntaxError("too many arguments")
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
            raise SyntaxError("too few arguments")
        case 3:
            output = __app.call_isolated(__app.edit_project, *args)
        case _:
            raise SyntaxError("too many arguments")
    match output:
        case True:
            print(f"Updated project '{args[0]}' field '{args[1]}' to value '{args[2]}'")
        case False:
            print(f"Failed to update project '{args[0]}' field '{args[1]}' to value '{args[2]}' (maybe it doesn't exist, the field doesn't exist, or the value is invalid?)")
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
            raise SyntaxError("too few arguments")
        case 1:
            output = __app.call_isolated(__app.get_project, *args)
        case 2:
            output = __app.call_isolated(__app.get_project_field, *args)
        case _:
            output = __app.call_isolated(__app.get_project_fields, args[0], args[1:])
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
    style = 'compact'
    use_all_categories = False
    categories = []
    fields = []
    i:int = 0
    while i < len(args) and args[i][0] != '-':
        match args[i]:
            case 'all':
                use_all_categories = True
            case _:
                categories.append(args[i])
        i += 1
    if len(categories) == 0:
        use_all_categories = True
    if i < len(args):
        match args[i]:
            case '--compact' | '-c':
                style = 'compact'
            case '--get' | '-g':
                style = 'get'
            case '--verbose' | '-v':
                style = 'verbose'
            case _:
                raise ValueError(f"unknown flag '{args[i]}'")
        i += 1
    while i < len(args):
        fields.append(args[i])
        i += 1
    match style:
        case 'compact':
            if len(fields) > 0:
                raise SyntaxError("compact flag does not take args")
            match use_all_categories:
                case True:
                    output = __app.call_isolated(__app.list_all_compact)
                case False:
                    match len(categories):
                        case 1:
                            output = __app.call_isolated(__app.list_category_compact, categories[0])
                        case _:
                            output = __app.call_isolated(__app.list_categories_compact, categories)
        case 'get':
            if len(fields) == 0:
                raise SyntaxError("get flag must take at least one arg")
            match use_all_categories:
                case True:
                    output = __app.call_isolated(__app.list_all_get_fields, fields)
                case False:
                    match len(categories):
                        case 1:
                            output = __app.call_isolated(__app.list_category_get_fields, categories[0], fields)
                        case _:
                            output = __app.call_isolated(__app.list_categories_get_fields, categories, fields)
        case 'verbose':
            if len(fields) > 0:
                raise SyntaxError("verbose flag does not take args")
            match use_all_categories:
                case True:
                    output = __app.call_isolated(__app.list_all_verbose)
                case False:
                    match len(categories):
                        case 1:
                            output = __app.call_isolated(__app.list_category_verbose, categories[0])
                        case _:
                            output = __app.call_isolated(__app.list_categories_verbose, categories)
    print(json.dumps(output, indent=4))
