from setuptools import setup

setup(
    name='12306',
    version = '1.0',
    py_modules=['12306', 'stations'],
    install_requires=['requests', 'docopt', 'prettytable', 'colorama'],
    entry_points={
        'console_scripts': ['tickets=tickets:cli']
    }
)