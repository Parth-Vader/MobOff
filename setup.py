import os

from setuptools import setup
from setuptools import find_packages

setup(
        name='MobOff',
        version='0.2',
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
		moboff=mainscript:cli
		''',
)

os.system('chmod a+x mainscript.py')
os.system('export PATH=mainscript.py:$PATH')
