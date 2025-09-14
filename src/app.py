import json
import os
import sys

class App():

    __projects_json_file_name: str = "data/projects.json"

    def __init__(self):
        self.__projects = {}

    def start(self):
        try:
            self.__load_projects_json()
        except FileNotFoundError:
            pass
        self.stop()

    def stop(self):
        if not self.__projects == {}:
            self.__dump_projects_json()

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
    app.start()