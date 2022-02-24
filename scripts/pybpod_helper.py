import os
import shutil

from pybpodgui_api.models.project import Project


class pybpod_helper:
    def __init__(self, root_path, project_path):
        self.root_path = root_path
        self.project_path = project_path
        self.project = Project()
        self.hostname = os.environ["COMPUTERNAME"]

    def populate_project_folder(self):
        self.create_project()

        print("Creating: Bpod board")
        subject = self.create_defaults()

        # gamble task
        experiment_gamble = self.create_experiment("gamble_task")

        task_name = "gamble_task_training"
        self.create_task(task_name)
        self.create_setup(experiment_gamble, task_name, subject)

        task_name = "gamble_task_recording"
        self.create_task(task_name)
        self.create_setup(experiment_gamble, task_name, subject)

        # confidentiality task
        experiment_confidentiality = self.create_experiment("gamble_task")

        task_name = "confidentiality_task_habituation_complex"
        self.create_task(task_name)
        self.create_setup(experiment_confidentiality, task_name, subject)

        task_name = "confidentiality_task_habituation_complex_both_correct"
        self.create_task(task_name)
        self.create_setup(experiment_confidentiality, task_name, subject)

        task_name = "confidentiality_task_habituation_simple"
        self.create_task(task_name)
        self.create_setup(experiment_confidentiality, task_name, subject)

        task_name = "confidentiality_task_training_simple"
        self.create_task(task_name)
        self.create_setup(experiment_confidentiality, task_name, subject)

        # calibration, administer reward etc
        self.create_experiment("calibration_etc")

        print("Creating: default usersettings, user, and subject")
        self.create_defaults()

    def create_task(self, task_name):
        print(f"Creating {task_name} setup")
        task = self.project.find_task(task_name)
        if task is not None:
            print(
                f"Found task config file in {str(self.project_path)}/{str(task_name)}",
                "\nDo you want to overwrite config? (y/n)",
            )
            user_input = input()
            if user_input == "n":
                return
        # copy files to new task
        source_path = self.get_source_of_task_file(task_name)
        destination_path = self.project_path / "tasks" / task_name
        task = self.project.create_task()
        task.name = task_name
        self.project.save(self.project_path)
        self.copytree(source_path, destination_path)
        print(f"Created task: {task_name}")

    def get_source_of_task_file(self, task_name):
        if "gamble" in task_name:
            source_path = self.root_path / "tasks" / "gamble_task" / task_name
            return source_path
        if "confidentiality" in task_name:
            source_path = self.root_path / "tasks" / "confidentiality_task" / task_name
            return source_path

    def create_board(self):
        if not self.project.boards:
            # copy files to new board
            board = self.project.create_board()
            board.name = "board_" + self.hostname
            self.project.save(self.project_path)
            print("Created borad")
        else:
            print("Board already exists")
            board = self.project.boards[0].name
        return board

    def create_experiment(self, experiment_name):
        experiment = self.project.create_experiment()
        experiment.name = experiment_name
        self.project.save(self.project_path)
        print(f"Created experiment: {experiment.name}")
        return experiment

    def create_setup(self, experiment, setup_name, subject):
        """create new setup for setup

        Args:
            experiment (bpod.experiment): experiment under which the setup is created
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
        source_path = self.root_path / ("scripts/user_settings.py")
        destination_path = self.project_path / "user_settings.py"
        shutil.copy(source_path, destination_path)
        # add default prject to user settings
        with open(destination_path, "a") as f:
            f.write(f'\nDEFAULT_PROJECT_PATH = "{self.project_path}"\n')
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
        print("Creating default project")
        try:
            self.project.load(self.project_path)
            print(f"  Skipping creation: maxland project found in: {self.project_path}")
        except:  # noqa
            self.project.name = "maxland_" + self.hostname
            self.project.save(self.project_path)
            print(f"Created: project maxland_{self.hostname}")

    def copytree(self, source_path, destination_path, symlinks=False, ignore=None):
        """helper function to copy all files from one directory to another"""
        for item in os.listdir(source_path):
            s = os.path.join(source_path, item)
            d = os.path.join(destination_path, item)
            if os.path.isdir(s):
                self.copytree(s, d, symlinks, ignore)
            if item in os.listdir(destination_path):
                os.remove(d)
                shutil.copy2(s, d)
            else:
                shutil.copy2(s, d)
