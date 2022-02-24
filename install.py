import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

root_path = Path.cwd()
hostname = os.environ["COMPUTERNAME"]
project_path_default = root_path / ("maxland_" + hostname)
sys.path.append(os.path.join(os.getcwd(), "scripts"))

if sys.platform not in ["Windows", "windows", "win32"]:
    print("\nERROR: Unsupported OS\nInstallation might not work!")


def get_maxland_env_path():
    """get environment path if maxland environment exists"""
    all_envs = subprocess.check_output(["conda", "env", "list", "--json"])
    all_envs = json.loads(all_envs.decode("utf-8"))
    maxland_env = [x for x in all_envs["envs"] if "maxland" in x]
    maxland_env = maxland_env[0] if maxland_env else None
    return maxland_env


def get_python_path():
    """get python.exe und pip.exe for maxland environment"""
    maxland_env = get_maxland_env_path()
    pip = os.path.join(maxland_env, "Scripts", "pip.exe")
    python = os.path.join(maxland_env, "python.exe")
    return python, pip


def install_maxland_env():
    create_command = "conda create -y -n maxland python=3.8"
    os.system(create_command)
    os.system("conda activate maxland && python -m pip install --upgrade pip")


def remove_maxland_env():
    remove_command = "conda env remove -y -n maxland"
    os.system(remove_command)


def create_maxland_env():
    print("\nINFO: create anaconda environment maxland:")
    maxland_env = get_maxland_env_path()
    if maxland_env:
        print(
            f"Found pre-existing environment in {maxland_env}",
            "\nDo you want to reinstall the environment? (y/n):",
        )
        user_input = input()
        if user_input == "y":
            remove_maxland_env()
            install_maxland_env()
            return
        if user_input not in ("n", "y"):
            print("Please answer 'y' or 'n'")
            return create_maxland_env()
        if user_input == "n":
            return
    else:
        install_maxland_env()
    print("Anaconda environment maxland installed\n")


def check_pre_dependencies():
    print("\n\nINFO: Checking for dependencies:")
    try:
        subprocess.check_output(["git", "--version"])
        os.system("git --version")
        print("git... OK")
        os.system("conda -V")
        print("conda... OK")
        os.system("pip -V")
        print("pip... OK")
        # update conda and packages
        os.system("conda activate maxland && conda update -y -n base -c defaults conda && conda update -y --all")
    except Exception as err:
        print(
            err,
            "\nEither git, conda, or pip were not found.\nplease install them and run the script again",
        )
        return
    print("All dependencies OK.")


def install_dependencies():
    print("\n\nINFO: Installing required python packages")
    os.system("conda activate maxland && pip install -e .")
    print("Requirements successfully installed in maxland\n")


def create_project_folder(project_folder_path):
    """create a project folder for this computer in main maxland folder drive for pybpod"""
    print(f"\n\nINFO: Setting up default project folder in {project_folder_path}")
    env = get_maxland_env_path()
    if env is None:
        msg = "Can't configure project folder, conda environment maxland not found"
        raise ValueError(msg)
    if project_folder_path.exists():
        print(
            f"Found previous configuration in {str(project_folder_path)}",
            "\nDo you want to update config? (y/n)",
        )
        user_input = input()
        if user_input == "n":
            return
        if user_input == "y":
            os.system("conda activate maxland && cd scripts && python populate_project.py")
            return
        if user_input not in ("y", "n"):
            print("\n Please select either y of n")
            return create_project_folder(project_folder_path)
    else:
        project_folder_path.mkdir(parents=True, exist_ok=True)
        os.system("conda activate maxland && cd scripts && python populate_project.py")


def get_project_folder(default_project_folder_path):
    print(
        f"\nDo you want to use the default path: {default_project_folder_path}, if not, you can enter a valid path to install to? (y/valid path)"
    )
    user_input = input()
    if user_input == "y":
        return default_project_folder_path
    else:
        try:
            new_project_folder_path = Path(user_input)
        except Exception as e:
            print("Please choose a valid path")
            return get_project_folder(default_project_folder_path)
        if new_project_folder_path.exists() and len(os.listdir(new_project_folder_path)) != 0:
            print(f"The project folder path: {new_project_folder_path} is not empty, do want to continue anyway (y/n)?")
            user_input_second = input()
            if user_input_second == "y":
                return new_project_folder_path
            else:
                return get_project_folder(default_project_folder_path)


def create_desctop_shortcut():
    """depending on os move bat, or sh file fore launching maxland to desktop"""
    os.system("cd scripts && copy maxland.bat C:\\Users\\%USERNAME%\\Desktop")


if __name__ == "__main__":
    ALLOWED_ACTIONS = ["new", "y"]
    parser = argparse.ArgumentParser(description="Install Maxland")
    parser.add_argument(
        "--new",
        required=False,
        default=False,
        action="store_true",
        help="Use new install procedure",
    )
    args = parser.parse_args()

    try:
        check_pre_dependencies()
        create_maxland_env()
        install_dependencies()
        project_folder_actual = get_project_folder(project_path_default)
        create_project_folder(project_folder_actual)
        create_desctop_shortcut()
        print("\n\nINFO: maxland installed, you should be good to go!")
    except OSError as msg:
        print(msg, "\n\nSOMETHING IS WRONG!")
