import json

class App():
    
    def __init__(self):

        self.__VALID_CATEGORIES = [
            "active",
            "occasional",
            "hiatused",
            "backlogged",
            "completed",
            "abandoned"
        ]

        self.__projects_json_file_path:str = "data/projects.json"
        self.__projects:dict = {}
        self.__unsaved_changes = False
    
    def load_projects_json(self) -> bool:
        try:
            with open(self.__projects_json_file_path, 'r') as projects_json_file:
                self.__projects = json.load(projects_json_file)
            self.__unsaved_changes = False
            return True
        except FileNotFoundError:
            return False

    def dump_projects_json(self) -> bool:
        if self.__unsaved_changes:
            with open(self.__projects_json_file_path, 'w') as projects_json_file:
                json.dump(self.__projects, projects_json_file)
            self.__unsaved_changes = False
            return True
        return False
    
    def create_project(self, project_name:str, category:str="backlogged", description:str="") -> bool:
        if project_name not in self.__projects:
            self.__projects[project_name] = {
                "category": category,
                "description": description
            }
            self.__unsaved_changes = True
            return True
        return False

    def delete_project(self, project_name:str) -> bool:
        if project_name in self.__projects:
            del self.__projects[project_name]
            self.__unsaved_changes = True
            return True
        return False

    def update_project_name(self, existing_project_name:str, new_project_name:str) -> bool:
        if existing_project_name in self.__projects and new_project_name not in self.__projects:
            self.__projects[new_project_name] = self.__projects[existing_project_name]
            del self.__projects[existing_project_name]
            self.__unsaved_changes = True
            return True
        return False

    def update_project_category(self, project_name:str, new_category:str) -> bool:
        if project_name in self.__projects and new_category in self.__VALID_CATEGORIES:
            self.__projects[project_name]["category"] = new_category
            self.__unsaved_changes = True
            return True
        return False
    
    def update_project_description(self, project_name:str, new_description:str) -> bool:
        if project_name in self.__projects:
            self.__projects[project_name]["description"] = new_description
            self.__unsaved_changes = True
            return True
        return False

    def get_project_info(self, project_name:str) -> dict|None:
        return self.__projects.get(project_name)

    def get_project_category(self, project_name:str) -> str|None:
        if project_name in self.__projects:
            return self.__projects[project_name].get("category")
        return None

    def get_project_description(self, project_name:str) -> str|None:
        if project_name in self.__projects:
            return self.__projects[project_name].get("description")
        return None
    
    def get_projects(self) -> dict:
        return self.__projects
    
    def get_category_projects(self, category:str) -> dict:
        category_projects:dict = {}
        for project_name, project_dict in self.__projects.items():
            if project_dict.get("category") == category:
                category_projects[project_name] = project_dict
        return category_projects
