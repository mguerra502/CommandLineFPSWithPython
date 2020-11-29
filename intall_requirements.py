from pathlib import Path
import subprocess
import sys
import os

def install(requirements_file: 'string'):
    """This function is used to installed the modules indicated in the requirements file

    Args:
        requirements_file (string): Requirements file
    """
    output = subprocess.check_output([sys.executable, "-m", "pip", "install", "-r", f"{requirements_file}"])

    return output

def check_requirements(requirements_file_mask: 'string', requirements_dir_mask: 'string'):
    """This function is used to check whether or not the required modules to run the application are installed.
       When the modules are installed a file called INSTALLED.txt will be created in the current directory. If
       this file exists it is assumed that the required modules are installed.

    Args:
        requirements_file (string): Requirements file name
        requirements_dir (string): Requirements file directory
    """
    requirements_file = Path(f'{requirements_dir_mask}/INSTALLED.txt')
    if not requirements_file.is_file():
        output = install(f'{requirements_dir_mask}/{requirements_file_mask}')
        installed_file = open(f'{requirements_dir_mask}/INSTALLED.txt', "w")
        installed_file.write(output.decode('utf-8'))
        installed_file.close()
