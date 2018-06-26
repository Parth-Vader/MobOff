import os

from setuptools import setup
from setuptools import find_packages

# read dependencies from requirements.txt
def read_requirements(filepath):
    """Parses a dependency file"""
    with open(filepath) as requirements:
        required = requirements.read().splitlines()
        required = [item for item in required if not item.startswith('#')]
    return required

required = read_requirements('requirements.txt')

setup(
        name='MobOff',
        version='0.2.2',
        py_modules=['moboff', 'download_utils'],
        packages=find_packages(),
        description='Download youtube music and send to devices',
        author='Parth Verma',
        author_email='vermaparth97@gmail.com',
        url="https://github.com/parth-vader/MobOff",
        download_url='https://codeload.github.com/Parth-Vader/MobOff/tar.gz/0.2.2',
        license="MIT License",
        install_requires=required,
        entry_points='''
		[console_scripts]
		moboff=moboff:cli
		''',
)

os.system('chmod a+x moboff.py')
os.system('export PATH=moboff.py:$PATH')
