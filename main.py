import os
from intall_requirements import check_requirements
from CommandLineFPS import CommandLineFPS

if __name__ == '__main__':
    # Run requirements if needed
    requirements_file = 'requirements.txt'
    check_requirements(requirements_file, os.path.dirname(os.path.realpath(__file__)))
    # Start Application
    CommandLineFPS()
    