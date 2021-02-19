# heavily based and influenced by https://github.com/int-brain-lab/iblrig.git
import json
import os
import re
import subprocess
import sys
from pathlib import Path
import argparse
import shutil


# helper functions =====================================================
root_path = Path.cwd()
hostname = os.environ['COMPUTERNAME']
project_path = root_path / ("maxland_"+hostname)
sys.path.append(os.path.join(os.getcwd(),'scripts'))


if sys.platform not in ["Windows", "windows", "win32"]:
    print("\nERROR: Unsupported OS\nInstallation might not work!")



# check for preexisting environments and get path =====================
def get_env():
    '''get environment path if maxland environment exists'''
    all_envs = subprocess.check_output(["conda", "env", "list", "--json"])
    all_envs = json.loads(all_envs.decode("utf-8"))
    maxland_env = [x for x in all_envs["envs"] if 'maxland' in x]
    maxland_env = maxland_env[0] if maxland_env else None
    return maxland_env


def get_python_execs_env():
    '''get python.exe und pip.exe for maxland environment'''
    env = get_env()
    pip = os.path.join(env, "Scripts", "pip.exe")
    python = os.path.join(env, "python.exe")
    return python, pip



# installing new neviornment =========================================
def install_environment():
    '''create conda environment'''
    print("\nINFO: create anaconda environment maxland:")
    print("-" * 79)
    # Checks id env is already installed
    env = get_env()
    create_command = "conda create -y -n maxland python=3.6"
    remove_command = "conda env remove -y -n malxand"
    # Installes the anaconda environment
    if env:
        print(
            "Found pre-existing environment in {}".format(env),
            "\nDo you want to reinstall the environment? (y/n):",
        )
        user_input = input()
        if user_input == "y":
            os.system(remove_command)
            return 
        elif user_input != "n" and user_input != "y":
            print("Please answer 'y' or 'n'")
            return install_environment()
        elif user_input == "n":
            return
    else:
        os.system(create_command)
        os.system(
            "conda activate maxland && python -m pip install --upgrade pip"
        )  # noqa
    print("-" * 79)
    print("Anaconda environment maxland installed\n")


def check_dependencies():
    # Check if Git and conda are installed
    print("\n\nINFO: Checking for dependencies:")
    print("-" * 79)
    try:
        subprocess.check_output(["git", "--version"])
        os.system("git --version")
        print("git... OK")
        os.system("conda -V")
        print("conda... OK")
        os.system("pip -V")
        print("pip... OK")
        # update conda and packages
        os.system(
            "conda activate maxland && conda update -y -n base -c defaults conda && conda update -y --all"
        )
    except Exception as err:
        print(err, "\nEither git, conda, or pip were not found.\n")
        return
    print("-" * 79 + "\n")
    print("All dependencies OK.")


def install_dependencies():
    print("\n\nINFO: Installing required python packages")
    # install python packages
    os.system("conda activate maxland && pip install -r requirements.txt -U")
    os.system("conda activate maxland && pip install -e .")
    # install custom scripts and modules
    os.system("conda activate maxland && python setup.py install clean --all")
    # clean up build
    shutil.rmtree(root_path/'Maxland.egg-info')
    shutil.rmtree(root_path/'dist')
    print("-" * 79)
    print("Requirements sucessfully installed in maxland\n")



# create default project folder =====================================================
def configure_env_params():
    '''create a project folder for this computer in main maxland folder drive for pybpod'''
    print(f"\n\nINFO: Setting up default project folder in {project_path}")
    print("-" * 79)
    env = get_env()
    if env is None:
        msg = "Can't configure project folder, conda environment maxland not found"
        raise ValueError(msg)
    python = get_python_execs_env()
    if project_path.exists():
        print(
            f"Found previous configuration in {str(project_path)}",
            "\nDo you want to update config? (y/n)",
        )
        user_input = input()
        if user_input == "n":
            return
        elif user_input == "y":
             os.system("conda activate maxland && cd scripts && python populate_project.py")  
        elif user_input != "n" and user_input != "y":
            print("\n Please select either y of n")
            return configure_env_params()
    else:
        project_path.mkdir(parents=True, exist_ok=True)
        os.system("conda activate maxland && cd scripts && python populate_project.py")  

 
def create_launcher():
    """depending on os move bat, or sh file fore lounching maxland to desktop
    """
    os.system("cd scripts && copy maxland.bat C:\\Users\\%USERNAME%\\Desktop")

# main loop ========================================================================
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
        check_dependencies()
        install_environment()
        install_dependencies()
        configure_env_params()
        create_launcher()
        print("\n\nINFO: maxland installed, you should be good to go!")
    except IOError as msg:
        print(msg, "\n\nSOMETHING IS WRONG!")





