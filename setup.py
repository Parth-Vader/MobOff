from setuptools import setup

setup(
        name='MobOff',
        version='0.1',
        py_modules=['moboff'],
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
