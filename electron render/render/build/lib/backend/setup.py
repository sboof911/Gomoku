import pathlib, os, subprocess

# Install dependencies from requirements.txt
requeriements_path = pathlib.Path(__file__).parent / 'requirements.txt'
subprocess.check_call(['pip', 'install', '-r', requeriements_path.absolute()])
from setuptools import setup, find_packages, Command

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
        os.environ['FLASK_APP'] = 'backend.server'
        subprocess.check_call(['flask', 'run', '--port', '5000'])

setup(
    name='Gomoku',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Flask==3.1.0',
        'numpy==2.1.2',
    ],
    entry_points={
        'console_scripts': [
            'start-server=backend.server:main',
        ],
    },
    cmdclass={
        'run_flask_dev': RunFlaskDevCommand,
    },
)