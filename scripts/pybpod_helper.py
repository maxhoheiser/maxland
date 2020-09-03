import json
import os
import re
import subprocess
import sys
from pathlib import Path
import argparse
import shutil
from pybpodgui_api.models.project import Project


class pybpod_helper():
    def __init__(self, root_path, project_path):
        self.root_path = root_path
        self.project_path = project_path
        self.project = Project()
        self.hostname = os.environ['COMPUTERNAME']

    def populate_project_folder(self):
        """copy all the necessary files for the bpod setup to the folder of this setup"""        
        # create project
        self.create_project()
        # boards
        print("Creating: Bpod board")
        board = self.create_board()

        # create project.json files
        user, subject = self.create_defaults()

        # tasks
        # gambl task
        exp_gamble = self.create_experiment("gamble_task")
        #   habituatin
        #   training
        task_name = 'gamble_task_training'
        self.create_task(task_name)
        self.create_setup(exp_gamble, task_name, board, subject)
        #   recording

        # choice task
        self.create_experiment("choice_task")
        #   habituation
        #   training
        #   recording

        # calibration, administer reward etc
        self.create_experiment("calibration_etc")


        print("Creating: default usersettings, user, and subject")
        self.create_defaults()
        # create project.json files



    # helper functions for task folder createion =======================================

    def create_task(self, task_name):
        """copy files for given task to poject dir

        Args:
            task_name (str): name of the task
        """        
        print(f"Creating {task_name} setup")
        task = self.project.find_task(task_name)
        if task != None:
            print(
                f"Found task config file in {str(self.project_path)}/{str(task_name)}",
                "\nDo you want to overwrite config? (y/n)",
            )
            user_input = input()
            if user_input == "n":
                return
            elif user_input == "y":
                # copy files to new task
                src = self.root_path/"tasks"/task_name
                dest = self.project_path/"tasks"/task_name
                task = self.project.create_task()
                task.name = task_name
                self.project.save(self.project_path)
                self.copytree(src, dest)
                print(f"Created task: {task_name}")
        else:
            # copy files to new task
            src = self.root_path/"tasks"/task_name
            dest = self.project_path/"tasks"/task_name
            task = self.project.create_task()
            task.name = task_name
            self.project.save(self.project_path)
            self.copytree(src, dest)
            print(f"Created task: {task_name}")


    def create_board(self):
        """create new bpod board for new setup

        Returns:
            bpod.board:
        """        
        if not self.project.boards:
            # copy files to new board
            board = self.project.create_board()
            board.name = ("board_"+self.hostname)
            self.project.save(self.project_path)
            print("Created borad")
        else:
            print("Board already exists")
            board = self.project.boards[0].name
        return board


    def create_experiment(self,exp_name):
        """create new experiment for setup

        Args:
            exp_name (str): name of the experiment to create

        Returns:
            bpod.experiment:
        """        
        exp = self.project.create_experiment()
        exp.name = exp_name
        self.project.save(self.project_path)
        print(f"Created experiment: {exp.name}")
        return exp


    def create_setup(self, experiment, setup_name, board, subject):
        """create new setup for setup

        Args:
            experiment (bpod.experiment): experminet under which the setup is created
            setup_name (str): name of the setup
            board (bpod.board): board which will be added as default to the setup
            subject (bpod.subject): subject which will be added as default to the setup
        """        
        # create experiment
        setup = experiment.create_setup()
        setup.name = setup_name
        setup.task = setup_name
        setup + subject
        setup.detached = True
        self.project.save(self.project_path)


    def create_defaults(self):
        """routine to create default elements for new bpod setup
                user: create new default user - test_user
                subject: create new default subject - test_subject

        Returns:
            bpod.user:
            bpod.subject:
        """        
        # copy usersettings
        src = self.root_path/("scripts/user_settings.py")
        dest = self.project_path/"user_settings.py"
        shutil.copy(src, dest)
        # add default prject to user settings
        with open(dest, 'a') as f:
            f.write(f"\nDEFAULT_PROJECT_PATH = \"{self.project_path}\"\n")
        # create default user
        if self.project.find_user("test_user") is None:
            user = self.project.create_user()
            user.name = "test_user"
            self.project.save(self.project_path)
            print(f"  Created: default user {user.name}")
        else:
            user = self.project.find_user("test_user")
            print(f"  Skipping creation: User {user.name} already exists")
        # create default subject
        subject_name = "test_subject"
        subject = self.project.find_subject(subject_name)
        if subject is None:
            subject = self.project.create_subject()
            subject.name = subject_name
            self.project.save(self.project_path)
            print(f"  Created subject: {subject_name}")
        else:
            print(f"Skipping creation: Subject <{subject.name}> already exists")
        return user, subject


    def create_project(self):
        """create maxland project for new setup"""        
        print("Creating default project")
        try:
            self.project.load(self.project_path)
            print(f"  Skipping creation: IBL project found in: {self.project_path}")
        except:  # noqa
            self.project.name = ("maxland_"+self.hostname)
            self.project.save(self.project_path)
            print(f"Created: project maxland_{self.hostname}")


    def copytree(self, src, dst, symlinks=False, ignore=None):
        """helper function to copy all files from one directory to another

        Args:
            src (os.path): path to source folder
            dst (os.path): path to destination folder
            symlinks (bool, optional): dont copy but use symbolic links to original files. Defaults to False.
            ignore (list, optional): ignore items in source. Defaults to None.
        """        
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                copytree(s, d, symlinks, ignore)
            elif item in os.listdir(dst):
                os.remove(d)
                shutil.copy2(s, d)
            else:
                shutil.copy2(s, d)

