import argparse
import os
from pathlib import Path

from maxland.helperfunctions_pybpod import PybpodHelper


def create_bpod_setup(root_path, project_folder_path):
    check_project_exist(project_folder_path)
    helper = PybpodHelper(root_path, project_folder_path)
    helper.populate_project_folder()
    print("Create default project folder done")
    return


def check_project_exist(project_path):
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
            return check_project_exist()


def populate_project_folder(root_path, project_folder_path):
    """create a project folder for this computer in main maxland folder drive for pybpod"""
    print(f"\n\nINFO: Setting up default project folder in {project_folder_path}")

    if project_folder_path.exists() and os.listdir(project_folder_path):
        print(
            f"Found previous configuration in {str(project_folder_path)}",
            "\nDo you want to update config? (y/n)",
        )
        user_input = input()
        if user_input == "n":
            return

        if user_input == "y":
            create_bpod_setup(root_path, project_folder_path)
            return

        if user_input not in ("y", "n"):
            print("\n Please select either y of n")
            return populate_project_folder(root_path, project_folder_path)
    else:
        project_folder_path.mkdir(parents=True, exist_ok=True)
        create_bpod_setup(root_path, project_folder_path)
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Populate Maxland PyBpod Setup")
    parser.add_argument("path", type=str, help="Path to project folder")
    parser.add_argument("root", type=str, help="Path to root folder")

    args = parser.parse_args()

    root_path = Path(args.root)
    project_folder = Path(args.path)

    populate_project_folder(root_path, project_folder)
