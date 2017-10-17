import os

from setuptools import setup
from setuptools import find_packages

setup(
        name='MobOff',
        version='0.1',
        py_modules=['moboff'],
        packages=find_packages(),
        description = 'Download and send videos to devices',
        author = 'Parth Verma',
        author_email = 'vermaparth97@gmail.com',
        url = "https://github.com/parth-vader/moboff",
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
