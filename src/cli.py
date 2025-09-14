from src.constants import DATA_COMMANDS

class CLI():

    def __init__(self, command_data_export:dict):
        self.__command_data_export:dict = command_data_export

    def start(self):
        pass

    def stop(self):
        pass

    def get_command(self):
        command_id:int = int(input("Enter command id: "))
        if command_id in DATA_COMMANDS:
            self.__command_data_export["example"] = "needs command data"
        else:
            self.__command_data_export.clear()
        return command_id