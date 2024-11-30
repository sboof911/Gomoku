import os, subprocess, sys
from setuptools import setup, find_packages, Command

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

class RunFlaskDevCommand(Command):
    """A custom command to run Flask in development mode."""
    description = 'Run Flask server in development mode'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.environ['FLASK_ENV'] = 'development'
        os.environ['FLASK_APP'] = 'server'
        subprocess.check_call(['flask', 'run', '--port', '5000'])

setup(
    name='Gomoku',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Flask==3.1.0',
        'numpy==2.1.2',
        'flask_cors==5.0.0'
    ],
    entry_points={
        'console_scripts': [
            'start-server=server:main',
        ],
    },
    cmdclass={
        'dev': RunFlaskDevCommand,
    },
)