import subprocess
import sys
import os
import fileinput

def install(requirements_file: 'string'):
    """This function is used to installed the modules indicated in the requirements file

    Args:
        requirements_file (string): Requirements file
    """
    output = subprocess.check_output([sys.executable, "-m", "pip", "install", "-r", f"./{requirements_file}"])

def check_requirements(requirements_file: 'string', requirements_installed_flag: 'integer', invoking_script: 'string'):
    """This function is used to check whether or not the requirements listed in the
       requirements files have been installed. If they haven't then they will be
       installed and the enviroment variable FPyS_REQUIREMENTS will be set to 1
       indicating the requirements installation have been done.

    Args:
        requirements_file (string): Requirements file
        requirements_installed_flag (integer): flag that tells whether the requirements have to be installed or not
        invoking_script (string): absolute path of the script that is invoking this method
    """
    print(invoking_script)
    if not requirements_installed_flag:
        install(requirements_file)
        text_to_search = "check_requirements('requirements.txt', 0, f'{os.path.dirname(os.path.realpath(__file__))}/{os.path.basename(__file__)}')"
        replacement_text = "check_requirements('requirements.txt', 1, f'{os.path.dirname(os.path.realpath(__file__))}/{os.path.basename(__file__)}')"
        with fileinput.FileInput(invoking_script, inplace=True) as file:
            for line in file:
                print(line.replace(text_to_search, replacement_text), end='')
