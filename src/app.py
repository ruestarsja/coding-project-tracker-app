import json
import os

class App():
    
    def __init__(self):

        self.__CATEGORIES = [
            "active",
            "occasional",
            "hiatused",
            "backlogged",
            "completed",
            "abandoned"
        ]
        self.__FIELDS = [
            "name",
            "category",
            "description"
        ]

        self.__projects_json_dir_path:str = "data/"
        self.__projects_json_file_name:str = "projects.json"
        self.__projects_json_file_path:str = self.__projects_json_dir_path + self.__projects_json_file_name
        self.__projects:dict = {}
        self.__unsaved_changes = False
    
    def call_isolated(self, function, *args):
        self.load_projects_json()
        output = function(*args)
        self.dump_projects_json()
        return output
    
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
            try:
                os.makedirs(self.__projects_json_dir_path)
            except FileExistsError:
                pass
            with open(self.__projects_json_file_path, 'w') as projects_json_file:
                json.dump(self.__projects, projects_json_file, indent=4)
            self.__unsaved_changes = False
            return True
        return False
    
    def create_project(self, project_name:str, category:str="backlogged", description:str="") -> bool:
        if project_name not in self.__projects and category in self.__CATEGORIES:
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

    def edit_project_name(self, existing_project_name:str, new_project_name:str) -> bool:
        if existing_project_name in self.__projects and new_project_name not in self.__projects:
            self.__projects[new_project_name] = self.__projects[existing_project_name]
            del self.__projects[existing_project_name]
            self.__unsaved_changes = True
            return True
        return False

    def edit_project_category(self, project_name:str, new_category:str) -> bool:
        if project_name in self.__projects and new_category in self.__CATEGORIES:
            self.__projects[project_name]["category"] = new_category
            self.__unsaved_changes = True
            return True
        return False
    
    def edit_project_description(self, project_name:str, new_description:str) -> bool:
        if project_name in self.__projects:
            self.__projects[project_name]["description"] = new_description
            self.__unsaved_changes = True
            return True
        return False
    
    def edit_project(self, project_name:str, field_to_edit:str, new_value:str) -> bool:
        match field_to_edit:
            case "name":
                return self.edit_project_name(project_name, new_value)
            case "category":
                return self.edit_project_category(project_name, new_value)
            case "description":
                return self.edit_project_description(project_name, new_value)
            case _:
                if field_to_edit in self.__FIELDS:
                    raise NotImplementedError(f"edit_project() currently does not support the '{field_to_edit}' field. Please make sure you are on the latest version. If you are, please submit a bug report.")
                else:
                    return False
    
    def get_project_name(self, project_name:str) -> str|None:
        if project_name in self.__projects:
            return project_name
        return None

    def get_project_category(self, project_name:str) -> str|None:
        if project_name in self.__projects:
            return self.__projects[project_name].get("category")
        return None

    def get_project_description(self, project_name:str) -> str|None:
        if project_name in self.__projects:
            return self.__projects[project_name].get("description")
        return None
    
    def get_project_field(self, project_name:str, field:str) -> str|None:
        match field:
            case "name":
                return self.get_project_name(project_name)
            case "category":
                return self.get_project_category(project_name)
            case "description":
                return self.get_project_description(project_name)
            case _:
                return None

    def get_project_fields(self, project_name:str, fields:list) -> dict:
        project_fields:dict = {}
        for field in fields:
            project_fields[field] = self.get_project_field(project_name, field)
        return project_fields
    
    def get_project(self, project_name:str) -> dict:
        return self.get_project_fields(project_name, self.__FIELDS)

    def list_category_compact(self, category:str) -> list:
        category_list:list = []
        for project_name in self.__projects.keys():
            if self.get_project_category(project_name) == category:
                category_list.append(project_name)
        return category_list

    def list_category_get_fields(self, category:str, fields:list[str]) -> dict:
        category_dict:dict = {}
        for project_name in self.__projects.keys():
            if self.get_project_category(project_name) == category:
                category_dict[project_name] = self.get_project_fields(project_name, fields)
        return category_dict

    def list_category_verbose(self, category:str) -> dict:
        category_dict:dict = {}
        for project_name in self.__projects.keys():
            if self.get_project_category(project_name) == category:
                category_dict[project_name] = self.get_project(project_name)
        return category_dict

    def list_categories_compact(self, categories:list[str]) -> dict:
        categories_dict:dict = {}
        for category in categories:
            categories_dict[category] = self.list_category_compact(category)
        return categories_dict

    def list_categories_get_fields(self, categories:list[str], fields:list[str]) -> dict:
        categories_dict:dict = {}
        for category in categories:
            categories_dict[category] = self.list_category_get_fields(category, fields)
        return categories_dict

    def list_categories_verbose(self, categories:list[str]) -> dict:
        categories_dict:dict = {}
        for category in categories:
            categories_dict[category] = self.list_category_verbose(category)
        return categories_dict
    
    def list_all_compact(self) -> dict:
        return self.list_categories_compact(self.__CATEGORIES)

    def list_all_get_fields(self, fields:list[str]) -> dict:
        return self.list_categories_get_fields(self.__CATEGORIES, fields)

    def list_all_verbose(self) -> dict:
        return self.list_categories_verbose(self.__CATEGORIES)
