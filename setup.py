import os

from setuptools import setup
from setuptools import find_packages

setup(
        name='MobOff',
        version='0.2.1',
        py_modules=['moboff'],
        packages=find_packages(),
        description = 'Download youtube music and send to devices',
        author = 'Parth Verma',
        author_email = 'vermaparth97@gmail.com',
        url = "https://github.com/parth-vader/MobOff",
        download_url = 'https://codeload.github.com/Parth-Vader/MobOff/tar.gz/0.2',
        license = "MIT License",
        install_requires=[
            'pushbullet.py',
            'youtube_dl',
            'Click',
        ],
        entry_points='''
		[console_scripts]
		moboff=moboff:cli
		''',
)

os.system('chmod a+x moboff.py')
os.system('export PATH=moboff.py:$PATH')
