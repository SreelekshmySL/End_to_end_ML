from setuptools import find_packages,setup
from typing import List

def get_requirements(filepath:str)-> List[str]:
    '''
    this funcion will return a list of requirements
    '''
    HYPHEN_E = '-e .'
    with open(filepath) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace('\n','') for req in requirements]

    if HYPHEN_E in requirements:
        requirements.remove(HYPHEN_E)
    return requirements



setup(
name="EndtoEndML",
version='0.0.1',
author="sreelekshmy",
author_email="slsreelekhmy@gmail.com",
packages=find_packages(),
install_requires = get_requirements('requirements.txt'))