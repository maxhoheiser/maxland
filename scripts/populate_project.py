# populate project script
from pathlib import Path
import sys
#import pybpod_helper

from pybpod_helper import pybpod_helper

import os


def check_exist(project_path):
    # check if folder already exists
    if project_path.exists():
        print(
            f"Found previous configuration in {str(project_path)}",
            "\nDo you want to update config? (y/n)\nALL FILES WILL BE DELETED !!",
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
    hostname = os.environ['COMPUTERNAME']
    project_path = root_path / ("maxland_"+hostname)
    check_exist(project_path)

    helper = pybpod_helper(root_path, project_path)
    helper.populate_project_folder()
    print("Create default project folder done")
