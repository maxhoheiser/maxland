# populate project script
from pathlib import Path
import sys
#import pybpod_helper

from pybpod_helper import pybpod_helper

import os


if __name__ == "__main__":
    root_path = Path.cwd().parent
    hostname = os.environ['COMPUTERNAME']
    project_path = root_path.parent / ("maxland_"+hostname)
    helper = pybpod_helper(root_path, project_path)
    helper.populate_project_folder()
    print("Create default project folder done")
