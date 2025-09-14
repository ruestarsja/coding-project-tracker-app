from src.cli import CLI as Interface
from src.constants import CMD

import json
import os
import sys

class App():

    __projects_json_file_name: str = "data/projects.json"

    def __init__(self):
        self.__projects:dict = {}
        self.__interface_command_data:dict = {}
        self.__interface:Interface = Interface(self.__interface_command_data)

    def run(self):
        self.__start()
        running = True
        while running:
            next_interface_command:int = self.__interface.get_command()
            match (next_interface_command):
                case CMD.NONE:
                    pass
                case CMD.EXIT:
                    running = False
                case CMD.CREATE_PROJECT:
                    print(f"Create project with data {self.__interface_command_data}")
                case _:
                    print(f"Unrecognized command id {next_interface_command}")
                    
        self.__stop()

    def __start(self):
        try:
            self.__load_projects_json()
        except FileNotFoundError:
            pass
        self.__interface.start()


    def __stop(self):
        if not self.__projects == {}:
            self.__dump_projects_json()
        self.__interface.stop()

    def __load_projects_json(self):
        with open(self.__projects_json_file_name, 'r') as projects_json_file:
            self.__projects = json.load(projects_json_file)

    def __dump_projects_json(self):
        try:
            with open(self.__projects_json_file_name, 'w') as projects_json_file:
                json.dump(self.__projects, projects_json_file, indent=4, sort_keys=True)
        except FileNotFoundError:
            os.makedirs("data")
            self.__dump_projects_json()


if __name__ == "__main__":
    app = App()
    app.run()