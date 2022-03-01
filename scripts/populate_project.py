import os
import platform
from pathlib import Path

from pybpod_helper import pybpod_helper


def check_exist(project_path):
    # check if folder already exists
    if project_path.exists() and os.listdir(project_path):
        print(
            f"Found previous configuration in {str(project_path)}",
            "\nDo you want to update config? \nALL FILES WILL BE DELETED ! (y/n)",
        )
        user_input = input()
        if user_input == "n":
            return
        elif user_input == "y":
            os.system(f"del {project_path}\\*.* /s /q && rmdir {project_path}\\ /s /q")
        elif user_input != "n" and user_input != "y":
            print("\n Please select either y of n")
            return check_exist()


if __name__ == "__main__":
    root_path = Path.cwd().parent
    hostname = platform.node()
    project_path = root_path / ("maxland_" + hostname)
    check_exist(project_path)

    helper = pybpod_helper(root_path, project_path)
    helper.populate_project_folder()
    print("Create default project folder done")
